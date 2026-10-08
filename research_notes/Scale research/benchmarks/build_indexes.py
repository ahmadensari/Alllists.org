"""Cut a scale table from entry_5m and build the indexes one by one, recording time and size.

Usage: python build_indexes.py --db bench_search --scale 1m|5m
Refuses any database not starting with bench_.
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
n = {"1m": 1_000_000, "5m": 5_000_000}[a.scale]
E, V = f"entry_{a.scale}", f"variant_{a.scale}"
out = {"scale": a.scale, "rows": n, "steps": {}}

def step(cur, name, sql, size_of=None):
    t = time.time(); cur.execute(sql); dt = time.time() - t
    rec = {"seconds": round(dt, 1)}
    if size_of:
        cur.execute("select pg_relation_size(%s::regclass)", [size_of]); rec["bytes"] = cur.fetchone()[0]
    out["steps"][name] = rec
    print(f"{name:28s} {dt:7.1f}s  {rec.get('bytes','')}", flush=True)

with psycopg.connect(f"host={a.socket_dir} port={a.port} dbname={a.db} user=postgres", autocommit=True) as con:
    cur = con.cursor()
    cur.execute("set maintenance_work_mem='2GB'")
    if a.scale == "5m":
        cur.execute(f"alter table entry_5m rename to entry_5m_raw; alter table variant_5m rename to variant_5m_raw")
        cur.execute("""create table entry_5m as select r.*, (1000 * (0.5 * (case r.level when 0 then 0 when 1 then 0.35 when 2 then 0.7 else 1.0 end)
         + 0.3 * r.completeness / 100.0 + 0.2 * (case when r.verified_age_days < 0 then 0 else exp(-r.verified_age_days / 365.0) end)))::int * 1000 + (r.id % 1000) as static_score from entry_5m_raw r; create table variant_5m as select * from variant_5m_raw""")
        cur.execute("drop table entry_5m_raw, variant_5m_raw")
    else:
        step(cur, "cut_entry", f"drop table if exists {E}, {V}; create table {E} as select * from entry_5m where id <= {n}")
        step(cur, "cut_variant", f"create table {V} as select * from variant_5m where entry_id <= {n}")
    step(cur, "heap_pk", f"alter table {E} add primary key (id)", f"{E}_pkey")
    cur.execute(f"select pg_relation_size('{E}'::regclass)"); out["heap_bytes_before_tsv"] = cur.fetchone()[0]
    step(cur, "btree_list_query", f"create index {E}_list on {E} (country_code, place_path, concept_id, publish_state)", f"{E}_list")
    step(cur, "btree_name_prefix", f"create index {E}_name_pfx on {E} (name_fold text_pattern_ops)", f"{E}_name_pfx")
    step(cur, "gin_trgm_name", f"create index {E}_trgm on {E} using gin (name_fold gin_trgm_ops)", f"{E}_trgm")
    step(cur, "add_tsv_column", f"alter table {E} add column tsv tsvector generated always as (to_tsvector('simple', name_fold)) stored")
    step(cur, "gin_tsv", f"create index {E}_tsv on {E} using gin (tsv)", f"{E}_tsv")
    step(cur, "variant_btree", f"create index {V}_eid on {V} (entry_id)", f"{V}_eid")
    step(cur, "variant_gin_trgm", f"create index {V}_trgm on {V} using gin (text_fold gin_trgm_ops)", f"{V}_trgm")
    step(cur, "analyze", f"analyze {E}; analyze {V}")
    cur.execute(f"select pg_relation_size('{E}'::regclass), pg_relation_size('{V}'::regclass)")
    out["heap_bytes_with_tsv"], out["variant_heap_bytes"] = cur.fetchone()
    cur.execute("select count(*) from %s" % E); out["count"] = cur.fetchone()[0]
json.dump(out, open(f"results/build_{a.scale}.json", "w"), indent=1)
