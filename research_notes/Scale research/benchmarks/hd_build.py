"""High-diversity sensitivity table: entry_1mhd = entry_1m with two near-unique pseudo words appended to every name
(like owner names, street names or branch codes in real data). Tests how index size and typo behaviour move when the
vocabulary is far larger than the synthetic base (131 thousand distinct words at 5M rows). Refuses non-bench_ databases.
Usage: python hd_build.py --db bench_search
"""
import argparse, json, sys, time
import psycopg
ap = argparse.ArgumentParser(); ap.add_argument("--db", required=True)
ap.add_argument("--socket-dir", default="/var/lib/postgresql/bench_pg16"); ap.add_argument("--port", type=int, default=5544)
a = ap.parse_args()
if not a.db.startswith("bench_"): sys.exit("refusing: database name must start with bench_")
con = psycopg.connect(f"host={a.socket_dir} port={a.port} dbname={a.db} user=postgres", autocommit=True); cur = con.cursor()
cur.execute("set maintenance_work_mem='2GB'")
out = {}
def step(name, sql, rel=None):
    t = time.time(); cur.execute(sql); r = {"seconds": round(time.time() - t, 1)}
    if rel: cur.execute("select pg_relation_size(%s::regclass)", [rel]); r["bytes"] = cur.fetchone()[0]
    out[name] = r; print(name, r, flush=True)
step("create", """drop table if exists entry_1mhd, variant_1mhd, words_1mhd;
 create table entry_1mhd as select id, country_code, place_path, concept_id, publish_state,
   name_fold || ' ' || translate(substr(md5(id::text), 1, 8), '0123456789', 'ghjklmnpqr') || ' ' || translate(substr(md5((id * 7919)::text), 1, 6), '0123456789', 'stvwxyzbcd') as name_fold,
   script, level, verified_age_days, completeness, closed, static_score from entry_1m""")
step("pk", "alter table entry_1mhd add primary key (id)")
step("list", "create index entry_1mhd_list on entry_1mhd (country_code, place_path, concept_id, publish_state)")
step("prefix", "create index entry_1mhd_name_pfx on entry_1mhd (name_fold text_pattern_ops)", "entry_1mhd_name_pfx")
step("trgm", "create index entry_1mhd_trgm on entry_1mhd using gin (name_fold gin_trgm_ops)", "entry_1mhd_trgm")
step("tsv_col", "alter table entry_1mhd add column tsv tsvector generated always as (to_tsvector('simple', name_fold)) stored")
step("tsv", "create index entry_1mhd_tsv on entry_1mhd using gin (tsv)", "entry_1mhd_tsv")
step("score", "create index entry_1mhd_score on entry_1mhd (static_score desc) where publish_state = 'published'", "entry_1mhd_score")
step("variant", "create table variant_1mhd as select * from variant_1m")
step("words", "create table words_1mhd as select w as word, count(*)::int as df from entry_1mhd, unnest(string_to_array(name_fold, ' ')) w group by w")
step("words_gin", "create index words_1mhd_trgm on words_1mhd using gin (word gin_trgm_ops)", "words_1mhd_trgm")
cur.execute("vacuum analyze entry_1mhd"); cur.execute("analyze words_1mhd"); cur.execute("analyze variant_1mhd")
cur.execute("select count(*) from words_1mhd"); out["distinct_words"] = cur.fetchone()[0]
cur.execute("select pg_relation_size('entry_1mhd'), avg(length(name_fold)) from entry_1mhd"); r = cur.fetchone(); out["heap_bytes"] = r[0]; out["avg_name_chars"] = float(r[1])
json.dump(out, open("results/hd_build.json", "w"), indent=1)
