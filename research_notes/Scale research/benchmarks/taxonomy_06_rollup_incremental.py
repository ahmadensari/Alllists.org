#!/usr/bin/env python3
"""Roll-up benchmark, part 2: cost of keeping cells right after entries change. Needs taxonomy_05_rollup_build.py first.

A  cells touched per changed entry: all cells, stored cells (store rule), and the frontier (non-stored cells that need a
   live probe because they might cross 25 members).
B  per-entry incremental update, one client: naive (every cell, upsert) versus store-rule design (update stored cells,
   probe the frontier with LIMIT 26).
C  batch delta: K changed entries applied with one GROUP BY and one UPDATE, per-entry cost against K.
D  contention: 4 concurrent clients, with and without the hot cells (world, country, sector level) left to the batch job.
E  exact recount of every cell of an entry with count(DISTINCT), which is what the current refresh_for_entry does
   (but in SQL, not in Python: a lower bound for the current code).

  sudo -u postgres env PYTHONPATH=/var/tmp/benchlibs python3 taxonomy_06_rollup_incremental.py DBNAME OUTDIR
"""
import json
import multiprocessing as mp
import random
import re
import statistics
import sys
import time

import psycopg

DB, OUT = sys.argv[1], sys.argv[2]
assert re.fullmatch(r"bench_taxonomy_[a-z0-9_]+", DB)


def connect():
    c = psycopg.connect(dbname=DB, user="postgres", autocommit=True)
    c.execute("SET work_mem = '64MB'")
    return c


CELLS_SQL = """
SELECT DISTINCT pp AS place_path, cl.ancestor_id AS concept_id, c.level
FROM ec JOIN concept_closure cl ON cl.descendant_id = ec.concept_id JOIN concept c ON c.id = cl.ancestor_id,
     LATERAL place_prefixes(ec.place_path) pp
WHERE ec.entry_id = %s
"""

conn = connect()
N_ENTRIES = conn.execute("SELECT count(*) FROM entry").fetchone()[0]
rng = random.Random(7)
results = {}
CHECK_SQL = "SELECT sum(published), sum(total), count(*) FROM rollup_cell"
results['checksum_before'] = list(conn.execute(CHECK_SQL).fetchone())


def sample_ids(k):
    return [rng.randint(1, N_ENTRIES) for _ in range(k)]


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(len(xs) * p))]


# ------------------------------------------------------------------ A
all_c, stored_c, frontier_c = [], [], []
stored_set_sql = "SELECT 1 FROM rollup_cell WHERE place_path = %s AND concept_id = %s"
anc_cache = {}


def ancestors(cid):
    if cid not in anc_cache:
        anc_cache[cid] = {r[0] for r in conn.execute("SELECT ancestor_id FROM concept_closure WHERE descendant_id = %s", (cid,)).fetchall()}
    return anc_cache[cid]


def entry_cells(eid):
    rows = conn.execute(CELLS_SQL, (eid,)).fetchall()
    keys = [(r[0], r[1]) for r in rows]
    stored = {
        (r[0], r[1])
        for r in conn.execute(
            "SELECT place_path, concept_id FROM rollup_cell WHERE (place_path, concept_id) IN (SELECT * FROM unnest(%s::text[], %s::int[]))",
            ([k[0] for k in keys], [k[1] for k in keys]),
        ).fetchall()
    }
    return keys, stored


def frontier(keys, stored):
    """Non-stored cells with no more general non-stored cell: (place prefix of it, node ancestor of it)."""
    ns = [k for k in keys if k not in stored]
    out = []
    for (p, c) in ns:
        general = False
        for (p2, c2) in ns:
            if (p2, c2) == (p, c):
                continue
            place_general = p2 == "" or p == p2 or p.startswith(p2 + ".")
            if place_general and c2 in ancestors(c):
                general = True
                break
        if not general:
            out.append((p, c))
    return out


for eid in sample_ids(3000):
    keys, stored = entry_cells(eid)
    all_c.append(len(keys))
    stored_c.append(len(stored))
    frontier_c.append(len(frontier(keys, stored)))
results["A_cells_per_entry"] = {
    "sample": len(all_c),
    "all_mean": round(statistics.mean(all_c), 1),
    "all_p95": pct(all_c, 0.95),
    "all_max": max(all_c),
    "stored_mean": round(statistics.mean(stored_c), 1),
    "stored_p95": pct(stored_c, 0.95),
    "frontier_mean": round(statistics.mean(frontier_c), 1),
    "frontier_p95": pct(frontier_c, 0.95),
}
print("A", results["A_cells_per_entry"], flush=True)

# ------------------------------------------------------------------ B
conn.execute("DROP TABLE IF EXISTS rollup_naive")
conn.execute("CREATE TABLE rollup_naive (LIKE rollup_all INCLUDING ALL) WITH (fillfactor = 70)")
conn.execute("INSERT INTO rollup_naive SELECT * FROM rollup_all")
conn.execute("ANALYZE rollup_naive")


def naive_update(c, eid, sign):
    keys = [(r[0], r[1]) for r in c.execute(CELLS_SQL, (eid,)).fetchall()]
    keys.sort()
    with c.transaction():
        c.execute(
            "INSERT INTO rollup_naive (place_path, concept_id, total, published, verified) "
            "SELECT p, k, 0, %s, 0 FROM unnest(%s::text[], %s::int[]) AS t(p, k) ORDER BY 1, 2 "
            "ON CONFLICT (place_path, concept_id) DO UPDATE SET published = rollup_naive.published + %s",
            (sign, [k[0] for k in keys], [k[1] for k in keys], sign),
        )


def frontier_probe(c, p, cid):
    pf = "" if p == "" else f" AND (ec.place_path = '{p}' OR ec.place_path LIKE '{p}.%')"
    return c.execute(
        "SELECT count(*) FROM (SELECT DISTINCT ec.entry_id FROM concept_closure cl JOIN ec ON ec.concept_id = cl.descendant_id "
        f"WHERE cl.ancestor_id = {cid}{pf} LIMIT 26) q"
    ).fetchone()[0]


def design_update(c, eid, sign, hot_skip=False):
    t0 = time.perf_counter()
    rows = c.execute(CELLS_SQL, (eid,)).fetchall()
    keys = [(r[0], r[1]) for r in rows if not (hot_skip and (r[0].count(".") == 0 and r[2] <= 2))]
    keys.sort()
    t1 = time.perf_counter()
    with c.transaction():
        cur = c.execute(
            "WITH want AS (SELECT p, k FROM unnest(%s::text[], %s::int[]) AS t(p, k)), "
            "locked AS (SELECT r.place_path, r.concept_id FROM rollup_cell r JOIN want w ON r.place_path = w.p AND r.concept_id = w.k "
            "ORDER BY 1, 2 FOR UPDATE) "
            "UPDATE rollup_cell r SET published = r.published + %s FROM locked l WHERE r.place_path = l.place_path AND r.concept_id = l.concept_id",
            ([k[0] for k in keys], [k[1] for k in keys], sign),
        )
        updated = cur.rowcount
    t2 = time.perf_counter()
    stored = set()
    if keys:
        stored = {
            (r[0], r[1])
            for r in c.execute(
                "SELECT place_path, concept_id FROM rollup_cell WHERE (place_path, concept_id) IN (SELECT * FROM unnest(%s::text[], %s::int[]))",
                ([k[0] for k in keys], [k[1] for k in keys]),
            ).fetchall()
        }
    fr = frontier([(r[0], r[1]) for r in rows], stored)
    for (p, cid) in fr:
        frontier_probe(c, p, cid)
    t3 = time.perf_counter()
    return (t1 - t0, t2 - t1, t3 - t2, updated, len(fr))


def run_B(n=1500):
    ids = sample_ids(n)
    t = time.perf_counter()
    for i, eid in enumerate(ids):
        naive_update(conn, eid, 1 if i % 2 == 0 else -1)
    naive_s = time.perf_counter() - t
    parts = []
    t = time.perf_counter()
    for i, eid in enumerate(ids):
        parts.append(design_update(conn, eid, 1 if i % 2 == 0 else -1))
    design_s = time.perf_counter() - t
    return {
        "entries": n,
        "naive_ms_per_entry": round(1000 * naive_s / n, 2),
        "design_ms_per_entry": round(1000 * design_s / n, 2),
        "design_breakdown_ms": {
            "find_cells": round(1000 * statistics.mean(p[0] for p in parts), 2),
            "update_stored": round(1000 * statistics.mean(p[1] for p in parts), 2),
            "frontier_probes": round(1000 * statistics.mean(p[2] for p in parts), 2),
        },
        "stored_rows_updated_mean": round(statistics.mean(p[3] for p in parts), 1),
        "frontier_probes_mean": round(statistics.mean(p[4] for p in parts), 1),
    }


results["B_single_client"] = run_B()
print("B", results["B_single_client"], flush=True)

# ------------------------------------------------------------------ C
C = []
for K in (1, 100, 1000, 10000, 100000):
    ids = list(set(sample_ids(K)))
    t0 = time.perf_counter()
    conn.execute("DROP TABLE IF EXISTS changed")
    conn.execute("CREATE TEMP TABLE changed (id bigint PRIMARY KEY)")
    with conn.cursor().copy("COPY changed FROM STDIN") as cp:
        for i in ids:
            cp.write_row((i,))
    conn.execute(
        """
CREATE TEMP TABLE delta AS
SELECT p AS place_path, concept_id, count(*) AS d
FROM (SELECT DISTINCT ec.entry_id, pp AS p, cl.ancestor_id AS concept_id
      FROM changed ch JOIN ec ON ec.entry_id = ch.id JOIN concept_closure cl ON cl.descendant_id = ec.concept_id,
           LATERAL place_prefixes(ec.place_path) pp) x
GROUP BY 1, 2
"""
    )
    t1 = time.perf_counter()
    nd = conn.execute("SELECT count(*) FROM delta").fetchone()[0]
    cur = conn.execute(
        "UPDATE rollup_cell r SET published = r.published + d.d FROM delta d WHERE r.place_path = d.place_path AND r.concept_id = d.concept_id"
    )
    upd = cur.rowcount
    t2 = time.perf_counter()
    conn.execute("UPDATE rollup_cell r SET published = r.published - d.d FROM delta d WHERE r.place_path = d.place_path AND r.concept_id = d.concept_id")
    C.append(
        {
            "K": len(ids),
            "delta_cells": nd,
            "stored_cells_updated": upd,
            "find_ms_per_entry": round(1000 * (t1 - t0) / len(ids), 3),
            "apply_ms_per_entry": round(1000 * (t2 - t1) / len(ids), 3),
            "total_ms_per_entry": round(1000 * (t2 - t0) / len(ids), 3),
            "total_s": round(t2 - t0, 2),
        }
    )
    print("C", C[-1], flush=True)
results["C_batch"] = C


# ------------------------------------------------------------------ D
def worker(args):
    seed, seconds, hot_skip = args
    c = connect()
    r = random.Random(seed)
    n = 0
    t_end = time.perf_counter() + seconds
    lat = []
    while time.perf_counter() < t_end:
        eid = r.randint(1, N_ENTRIES)
        t = time.perf_counter()
        design_update(c, eid, 1 if n % 2 == 0 else -1, hot_skip=hot_skip)
        lat.append(time.perf_counter() - t)
        n += 1
    return n, lat


D = []
for hot_skip in (False, True):
    for clients in (1, 4):
        with mp.Pool(clients) as pool:
            t = time.perf_counter()
            out = pool.map(worker, [(100 + i, 20, hot_skip) for i in range(clients)])
            el = time.perf_counter() - t
        n = sum(o[0] for o in out)
        lat = [x for o in out for x in o[1]]
        D.append(
            {
                "hot_cells_in_online_path": not hot_skip,
                "clients": clients,
                "entries_per_s": round(n / el, 1),
                "p50_ms": round(1000 * pct(lat, 0.5), 2),
                "p95_ms": round(1000 * pct(lat, 0.95), 2),
                "max_ms": round(1000 * max(lat), 1),
            }
        )
        print("D", D[-1], flush=True)
results["D_concurrency"] = D

# ------------------------------------------------------------------ E
conn.execute("SET statement_timeout = 120000")
E = []
for eid in sample_ids(12):
    keys = [(r[0], r[1]) for r in conn.execute(CELLS_SQL, (eid,)).fetchall()]
    t = time.perf_counter()
    status = "ok"
    try:
        for (p, cid) in keys:
            pf = "" if p == "" else f" AND (ec.place_path = '{p}' OR ec.place_path LIKE '{p}.%')"
            conn.execute(
                "SELECT count(DISTINCT ec.entry_id), count(DISTINCT ec.entry_id) FILTER (WHERE ec.published) "
                f"FROM concept_closure cl JOIN ec ON ec.concept_id = cl.descendant_id WHERE cl.ancestor_id = {cid}{pf}"
            ).fetchone()
    except psycopg.errors.QueryCanceled:
        status = "timeout"
    E.append({"entry": eid, "cells": len(keys), "seconds": round(time.perf_counter() - t, 2), "status": status})
    print("E", E[-1], flush=True)
results["E_exact_recount_per_entry"] = E
results["E_summary"] = {
    "median_s": statistics.median(e["seconds"] for e in E),
    "max_s": max(e["seconds"] for e in E),
    "timeouts": sum(1 for e in E if e["status"] == "timeout"),
}
results['checksum_after'] = list(conn.execute(CHECK_SQL).fetchone())
results['checksum_equal'] = results['checksum_before'] == results['checksum_after']
json.dump(results, open(f"{OUT}/rollup_incremental.json", "w"), indent=1)
print(json.dumps(results["E_summary"]))
