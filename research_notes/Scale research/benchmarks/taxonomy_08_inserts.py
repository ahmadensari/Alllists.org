#!/usr/bin/env python3
"""Insert and backfill rates for the membership table designs. Run last: it adds rows to entry, ec and ec_lt (ids above
2,000,000) and removes them again.

  OLTP   one transaction per new entry: 1 entry row + 3 membership rows, pgbench custom scripts, 1 and 4 clients
         A   ec with its three indexes (pkey, one primary per entry, list index)
         A+  the same plus the place-major index
         B   ec_lt: ltree[] copied onto the row, GiST on it
  BACKFILL  copy all 5.96 million memberships into a new indexed table in batches of 50,000 entries (indexes first),
         against: bare table first, then CREATE INDEX CONCURRENTLY. WAL bytes come from EXPLAIN (ANALYZE, WAL), so they
         belong to the statement and not to the whole (shared) server.

  sudo -u postgres env PYTHONPATH=/var/tmp/benchlibs python3 taxonomy_08_inserts.py DBNAME OUTDIR
"""
import json
import re
import subprocess
import sys
import time

import psycopg

DB, OUT = sys.argv[1], sys.argv[2]
assert re.fullmatch(r"bench_taxonomy_[a-z0-9_]+", DB)
conn = psycopg.connect(dbname=DB, user="postgres", autocommit=True)
conn.execute("SET maintenance_work_mem = '512MB'")
results = {}

PRE = r"""
\set eid random(2000001, 2000000000)
\set c3 random(3992, 12391)
\set c1 random(12392, 31000)
\set c2 random(31001, 50000)
\set rr random(0, 16)
\set tt random(0, 11)
"""
ENTRY = (
    "WITH p AS (SELECT 'zz.region_' || lpad(:rr::text, 2, '0') || '.city_' || lpad(:tt::text, 3, '0') AS pp), "
    "e AS (INSERT INTO entry (id, country_code, place_path, publish_state, rank, fresh, name, filler, sort_key) "
    "SELECT :eid, 'zz', pp, 1, 3, 5, 'n', repeat('x', 190), 3005 FROM p RETURNING 1) "
)
SCRIPTS = {
    "A": PRE + ENTRY + "INSERT INTO ec (entry_id, concept_id, role, place_path, published, sort_key) "
    "SELECT :eid, v.cid, v.role, p.pp, true, 3005 FROM p, (VALUES (:c3, 1), (:c1, 2), (:c2, 2)) v(cid, role);\n",
    "B": PRE + ENTRY + "INSERT INTO ec_lt (entry_id, concept_id, role, place_path, published, sort_key, cpaths) "
    "SELECT :eid, v.cid, v.role, p.pp, true, 3005, (SELECT array_agg(path) FROM concept_path WHERE concept_id = v.cid) "
    "FROM p, (VALUES (:c3, 1), (:c1, 2), (:c2, 2)) v(cid, role);\n",
}


def pgbench(script_name, clients, seconds=15):
    path = f"/var/tmp/benchout/ins_{script_name}.sql"
    open(path, "w").write(SCRIPTS[script_name])
    out = subprocess.run(
        ["pgbench", "-n", "-h", "/var/run/postgresql", "-U", "postgres", "-f", path, "-c", str(clients), "-j", str(clients), "-T", str(seconds), DB],  # DB is positional: "-d" means --debug
        capture_output=True, text=True,
    ).stdout
    tps = float(re.search(r"tps = ([0-9.]+)", out).group(1))
    lat = float(re.search(r"latency average = ([0-9.]+) ms", out).group(1))
    fails = re.search(r"number of failed transactions: (\d+)", out)
    return {"clients": clients, "entries_per_s": round(tps, 1), "memberships_per_s": round(3 * tps, 1), "latency_ms": round(lat, 3), "failed": int(fails.group(1)) if fails else 0}


def cleanup():
    t = time.perf_counter()
    for t_ in ("ec", "ec_lt", "entry"):
        col = "id" if t_ == "entry" else "entry_id"
        conn.execute(f"DELETE FROM {t_} WHERE {col} > 2000000")
    for t_ in ("ec", "ec_lt", "entry"):
        conn.execute(f"VACUUM {t_}")
    return round(time.perf_counter() - t, 1)


oltp = []
for variant, label in (("A", "A: ec, 3 indexes"), ("B", "B: ec_lt, ltree[] + GiST")):
    for clients in (1, 4):
        r = pgbench(variant, clients)
        r["design"] = label
        oltp.append(r)
        print(r, flush=True)
    results.setdefault("cleanup_s", []).append(cleanup())
# A+ : add the place-major index
t = time.perf_counter()
conn.execute("CREATE INDEX ec_place_concept ON ec (place_path text_pattern_ops, concept_id) INCLUDE (entry_id, sort_key) WHERE published")
results["place_major_index_build_s"] = round(time.perf_counter() - t, 1)
results["place_major_index_bytes"] = conn.execute("SELECT pg_relation_size('ec_place_concept')").fetchone()[0]
for clients in (1, 4):
    r = pgbench("A", clients)
    r["design"] = "A+: ec, 4 indexes (adds place-major)"
    oltp.append(r)
    print(r, flush=True)
results["cleanup_s"].append(cleanup())
conn.execute("DROP INDEX ec_place_concept")
results["oltp"] = oltp

# ------------------------------------------------------------------ backfill
INS = (
    "INSERT INTO ec_bf (entry_id, concept_id, role, place_path, published, sort_key) "
    "SELECT entry_id, concept_id, role, place_path, published, sort_key FROM ec WHERE entry_id > {lo} AND entry_id <= {hi}"
)


def wal_bytes(sql):
    row = conn.execute("EXPLAIN (ANALYZE, WAL, FORMAT JSON) " + sql).fetchone()[0][0]
    wal = row.get("Plan", {}).get("WAL Bytes", 0) if isinstance(row, dict) else 0
    # WAL Bytes sits at the top of the plan node for a ModifyTable; fall back to a recursive search
    def find(n):
        if isinstance(n, dict):
            if "WAL Bytes" in n:
                return n["WAL Bytes"]
            for v in n.values():
                r = find(v)
                if r:
                    return r
        if isinstance(n, list):
            for v in n:
                r = find(v)
                if r:
                    return r
        return 0
    return find(row)


def backfill(indexes_first):
    conn.execute("DROP TABLE IF EXISTS ec_bf")
    conn.execute("CREATE TABLE ec_bf (entry_id bigint NOT NULL, concept_id int NOT NULL, role smallint NOT NULL, place_path text NOT NULL, published boolean NOT NULL, sort_key int NOT NULL)")
    if indexes_first:
        conn.execute("ALTER TABLE ec_bf ADD PRIMARY KEY (entry_id, concept_id)")
        conn.execute("CREATE UNIQUE INDEX ON ec_bf (entry_id) WHERE role = 1")
        conn.execute("CREATE INDEX ON ec_bf (concept_id, place_path text_pattern_ops) INCLUDE (entry_id, sort_key) WHERE published")
    t0 = time.perf_counter()
    wal = 0
    rows = 0
    batch_times = []
    for lo in range(0, 2_000_000, 50_000):
        t = time.perf_counter()
        sql = INS.format(lo=lo, hi=lo + 50_000)
        wal += wal_bytes(sql)  # EXPLAIN ANALYZE executes the statement
        batch_times.append(time.perf_counter() - t)
    rows = conn.execute("SELECT count(*) FROM ec_bf").fetchone()[0]
    copy_s = time.perf_counter() - t0
    idx_s = 0.0
    if not indexes_first:
        t = time.perf_counter()
        conn.execute("ALTER TABLE ec_bf ADD PRIMARY KEY (entry_id, concept_id)")
        conn.execute("CREATE UNIQUE INDEX CONCURRENTLY ec_bf_primary ON ec_bf (entry_id) WHERE role = 1")
        conn.execute("CREATE INDEX CONCURRENTLY ec_bf_list ON ec_bf (concept_id, place_path text_pattern_ops) INCLUDE (entry_id, sort_key) WHERE published")
        idx_s = time.perf_counter() - t
    return {
        "indexes_first": indexes_first,
        "rows": rows,
        "copy_seconds": round(copy_s, 1),
        "index_seconds_after": round(idx_s, 1),
        "total_seconds": round(copy_s + idx_s, 1),
        "rows_per_second_total": round(rows / (copy_s + idx_s)),
        "wal_gb_copy_statements": round(wal / 1e9, 2),
        "slowest_batch_s": round(max(batch_times), 2),
        "median_batch_s": round(sorted(batch_times)[len(batch_times) // 2], 2),
    }


bf = []
for first in (True, False):
    r = backfill(first)
    bf.append(r)
    print(r, flush=True)
conn.execute("DROP TABLE IF EXISTS ec_bf")
results["backfill"] = bf
json.dump(results, open(f"{OUT}/inserts.json", "w"), indent=1)
print(json.dumps(results, indent=1))
