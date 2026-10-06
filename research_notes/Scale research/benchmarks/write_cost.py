"""Write amplification of the search indexes: insert speed into a 1M-row table with no text index, trigram GIN, tsvector GIN, both.

Usage: python write_cost.py --db bench_search   (refuses databases not starting with bench_; creates and drops wc_* tables)
Measures (a) single-row insert transactions (latency p50/p95, rows per second) and (b) batches of 1,000 rows.
New rows are copies of existing entries with fresh ids, so the text distribution is realistic.
"""
import argparse, json, sys, time
import numpy as np, psycopg
ap = argparse.ArgumentParser()
ap.add_argument("--db", required=True)
ap.add_argument("--socket-dir", default="/var/lib/postgresql/bench_pg16"); ap.add_argument("--port", type=int, default=5544)
a = ap.parse_args()
if not a.db.startswith("bench_"): sys.exit("refusing: database name must start with bench_")
con = psycopg.connect(f"host={a.socket_dir} port={a.port} dbname={a.db} user=postgres", autocommit=True); cur = con.cursor()
cur.execute("set maintenance_work_mem='1GB'")
variants = {"no_text_index": [], "trgm_gin": ["create index {t}_trgm on {t} using gin (name_fold gin_trgm_ops)"],
            "tsv_gin": ["create index {t}_tsv on {t} using gin (tsv)"],
            "both": ["create index {t}_trgm on {t} using gin (name_fold gin_trgm_ops)", "create index {t}_tsv on {t} using gin (tsv)"]}
out = {}
cur.execute("select id, country_code, place_path, concept_id, publish_state, name_fold, script, level, verified_age_days, completeness, closed, static_score from entry_1m order by random() limit 20000")
src = cur.fetchall()
for name, ddl in variants.items():
    t = f"wc_{name}"
    cur.execute(f"drop table if exists {t}")
    cur.execute(f"""create table {t} as select id, country_code, place_path, concept_id, publish_state, name_fold, script, level, verified_age_days, completeness, closed, static_score,
                    to_tsvector('simple', name_fold) as tsv from entry_1m""")
    cur.execute(f"alter table {t} add primary key (id)")
    cur.execute(f"create index {t}_list on {t} (country_code, place_path, concept_id, publish_state)")
    for d in ddl: cur.execute(d.format(t=t))
    cur.execute(f"analyze {t}")
    nid = 10_000_000
    # (a) single row per transaction
    lat = []
    for r in src[:5000]:
        nid += 1; t0 = time.perf_counter()
        cur.execute(f"insert into {t} values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, to_tsvector('simple', %s))", (nid,) + r[1:] + (r[5],))
        lat.append((time.perf_counter() - t0) * 1000)
    # (b) batches of 1000
    t0 = time.perf_counter(); n = 0
    for b in range(10):
        rows = src[5000 + b * 1000: 6000 + b * 1000]
        with cur.copy(f"copy {t} from stdin") as cp:
            for r in rows:
                nid += 1; cp.write_row((nid,) + r[1:] + (None,))
        n += len(rows)
    cur.execute(f"update {t} set tsv = to_tsvector('simple', name_fold) where tsv is null")
    dt = time.perf_counter() - t0
    # (c) update of the ranking prior only (a very common change) on 5000 random rows
    t1 = time.perf_counter()
    cur.execute(f"update {t} set static_score = static_score + 1 where id = any(%s)", [[r[0] for r in src[:5000]]])
    upd = time.perf_counter() - t1
    cur.execute(f"select pg_total_relation_size('{t}')"); size = cur.fetchone()[0]
    arr = np.array(lat)
    out[name] = dict(single_insert_p50_ms=round(float(np.percentile(arr, 50)), 3), single_insert_p95_ms=round(float(np.percentile(arr, 95)), 3),
                     single_inserts_per_s=round(len(lat) / (arr.sum() / 1000)), copy_batch_rows_per_s=round(n / dt),
                     update_5000_rows_static_score_s=round(upd, 2), total_table_bytes=size)
    print(name, out[name], flush=True)
    cur.execute(f"drop table {t}")
json.dump(out, open("results/write_cost.json", "w"), indent=1)
