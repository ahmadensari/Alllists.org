"""Add the stored ranking prior (static_score), its partial index and the word dictionary used for typo correction.

Usage: python post_build.py --db bench_search --scale 1m|5m   (refuses any database not starting with bench_)
static_score (0..1000) = 1000 * (0.5 * level_weight + 0.3 * completeness + 0.2 * freshness), see 07 note section 4.
"""
import argparse, json, sys, time
import psycopg

ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True)
ap.add_argument("--scale", choices=["1m", "5m"], required=True)
ap.add_argument("--socket-dir", default="/var/lib/postgresql/bench_pg16")
ap.add_argument("--port", type=int, default=5544)
a = ap.parse_args()
if not a.db.startswith("bench_"):
    sys.exit("refusing: database name must start with bench_")
E = f"entry_{a.scale}"
out = {}
def step(cur, name, sql, rel=None):
    t = time.time(); cur.execute(sql); dt = time.time() - t
    rec = {"seconds": round(dt, 1)}
    if rel:
        cur.execute("select pg_relation_size(%s::regclass)", [rel]); rec["bytes"] = cur.fetchone()[0]
    out[name] = rec; print(f"{name:24s}{dt:8.1f}s {rec.get('bytes','')}", flush=True)
with psycopg.connect(f"host={a.socket_dir} port={a.port} dbname={a.db} user=postgres", autocommit=True) as con:
    cur = con.cursor(); cur.execute("set maintenance_work_mem='2GB'")
    cur.execute("select 1 from information_schema.columns where table_name=%s and column_name='static_score'", [E])
    if cur.fetchone():
        print("static_score already present (computed at cut time)")
    else:
      step(cur, "add_score", f"""alter table {E} add column static_score int;
      update {E} set static_score = (1000 * (0.5 * (case level when 0 then 0 when 1 then 0.35 when 2 then 0.7 else 1.0 end)
         + 0.3 * completeness / 100.0 + 0.2 * (case when verified_age_days < 0 then 0 else exp(-verified_age_days / 365.0) end)))::int
         * 1000 + (id % 1000)""")
    step(cur, "idx_score_partial", f"create index {E}_score on {E} (static_score desc) where publish_state = 'published'", f"{E}_score")
    step(cur, "words_table", f"""drop table if exists words_{a.scale};
      create table words_{a.scale} as select w as word, count(*)::int as df from {E}, unnest(string_to_array(name_fold, ' ')) w group by w""")
    step(cur, "words_gin", f"create index words_{a.scale}_trgm on words_{a.scale} using gin (word gin_trgm_ops)", f"words_{a.scale}_trgm")
    t = time.time(); cur.execute(f"vacuum analyze {E}"); cur.execute(f"analyze words_{a.scale}")
    out["vacuum_analyze"] = {"seconds": round(time.time() - t, 1)}; print("vacuum_analyze", out["vacuum_analyze"], flush=True)
    cur.execute(f"select count(*) from words_{a.scale}"); out["distinct_words"] = cur.fetchone()[0]
    cur.execute(f"select pg_relation_size('words_{a.scale}'::regclass)"); out["words_heap_bytes"] = cur.fetchone()[0]
json.dump(out, open(f"results/post_{a.scale}.json", "w"), indent=1)
