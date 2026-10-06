#!/usr/bin/env python3
"""Two small experiments on the 2M-entry scratch data. Needs taxonomy_05_rollup_build.py (rollup_cell) first.

R  Resolving a (place, node) page under the store rule: stored cell lookup, else a live probe (LIMIT 26), else the
   nearest populated cells for an empty page. 100 random pairs per node level (1 to 5), places drawn from all home places
   at country, region, city and area level. Timed with and without the place-major index on ec.
F  Facet filters inside a list page: entry_facet(entry, facet, value) with 3 values per entry, 4 filterable facets with
   skewed value use. List page with 0, 1 and 2 facet filters, and the sidebar counts for the cell.

  sudo -u postgres env PYTHONPATH=/var/tmp/benchlibs python3 taxonomy_09_resolve_and_facets.py DBNAME OUTDIR
"""
import json
import random
import re
import statistics
import sys
import time

import psycopg

DB, OUT = sys.argv[1], sys.argv[2]
assert re.fullmatch(r"bench_taxonomy_[a-z0-9_]+", DB)
conn = psycopg.connect(dbname=DB, user="postgres", autocommit=True)
conn.execute("SET work_mem = '64MB'")
conn.execute("SET statement_timeout = 30000")
rng = random.Random(21)
out = {}


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(len(xs) * p))]


def stats(xs):
    return {"n": len(xs), "p50_ms": round(pct(xs, 0.5), 2), "p95_ms": round(pct(xs, 0.95), 2), "max_ms": round(max(xs), 1)}


# ------------------------------------------------------------------ R
places = {
    1: [r[0] for r in conn.execute("SELECT DISTINCT split_part(place_path, '.', 1) FROM entry").fetchall()],
}
all_places = [r[0] for r in conn.execute("SELECT place_path FROM place_total WHERE place_path <> '' ORDER BY random() LIMIT 20000").fetchall()]
levels = {r[0]: (r[1], r[2]) for r in conn.execute("SELECT level, first_id, n FROM lv").fetchall()}


def combos():
    out_ = []
    for lvl in range(1, 6):
        f, n = levels[lvl]
        for _ in range(100):
            out_.append((lvl, f + rng.randrange(n), rng.choice(all_places)))
    return out_


COMBOS = combos()


def probe_sql(cid, p):
    pf = "" if p == "" else f" AND (ec.place_path = '{p}' OR ec.place_path LIKE '{p}.%')"
    return (
        "SELECT count(*) FROM (SELECT DISTINCT ec.entry_id FROM concept_closure cl JOIN ec ON ec.concept_id = cl.descendant_id "
        f"AND ec.published WHERE cl.ancestor_id = {cid}{pf} LIMIT 26) q"
    )


def nearest_sql(cid, p):
    parts = p.split(".")
    ancestors = [".".join(parts[:i]) for i in range(len(parts) - 1, 0, -1)] + [""]
    arr = "ARRAY[" + ",".join(f"'{a}'" for a in ancestors) + "]::text[]"
    return (
        f"SELECT place_path, published FROM rollup_cell WHERE concept_id = {cid} AND place_path = ANY({arr}) AND published > 0 "
        "ORDER BY length(place_path) DESC LIMIT 1"
    )


def run_resolve(label):
    rows = []
    modes = {"stored": 0, "live": 0, "virtual_empty": 0}
    per_mode = {"stored": [], "live": [], "virtual_empty": []}
    by_level = {l: [] for l in range(1, 6)}
    for (lvl, cid, p) in COMBOS:
        t = time.perf_counter()
        hit = conn.execute("SELECT published FROM rollup_cell WHERE place_path = %s AND concept_id = %s", (p, cid)).fetchone()
        if hit:
            mode = "stored"
        else:
            n = conn.execute(probe_sql(cid, p)).fetchone()[0]
            mode = "virtual_empty" if n == 0 else "live"
            conn.execute(nearest_sql(cid, p)).fetchall()
        ms = (time.perf_counter() - t) * 1000
        modes[mode] += 1
        per_mode[mode].append(ms)
        by_level[lvl].append(ms)
    return {
        "label": label,
        "modes": modes,
        "all": stats([x for v in per_mode.values() for x in v]),
        "by_mode": {k: stats(v) for k, v in per_mode.items() if v},
        "by_node_level": {k: stats(v) for k, v in by_level.items()},
    }


out["R_resolve_no_place_index"] = run_resolve("resolve, concept-major index only")
print(out["R_resolve_no_place_index"], flush=True)
conn.execute("CREATE INDEX ec_place_concept ON ec (place_path text_pattern_ops, concept_id) INCLUDE (entry_id, sort_key) WHERE published")
conn.execute("ANALYZE ec")
out["R_resolve_with_place_index"] = run_resolve("resolve, with place-major index")
print(out["R_resolve_with_place_index"], flush=True)
conn.execute("DROP INDEX ec_place_concept")

# ------------------------------------------------------------------ F
conn.execute("DROP TABLE IF EXISTS entry_facet")
t = time.perf_counter()
conn.execute(
    """
CREATE TABLE entry_facet AS
SELECT e.id AS entry_id, f.facet_id, (CASE f.facet_id WHEN 1 THEN 40 WHEN 2 THEN 30 WHEN 3 THEN 60 ELSE 5 END * power(random(), 2.2))::int + 1 AS value_id
FROM entry e
CROSS JOIN LATERAL (
    SELECT DISTINCT 1 + floor(random() * 4)::int + (g - g) AS facet_id FROM generate_series(1, 3) g
) f
"""
)
conn.execute("ALTER TABLE entry_facet ADD COLUMN concept_id int")  # company scope in this experiment (null)
conn.execute("CREATE UNIQUE INDEX entry_facet_uq ON entry_facet (entry_id, facet_id, value_id)") if False else None
conn.execute("CREATE INDEX entryfacet_filter ON entry_facet (facet_id, value_id, entry_id)")
conn.execute("CREATE INDEX entryfacet_entry ON entry_facet (entry_id)")
conn.execute("ANALYZE entry_facet")
out["F_build_s"] = round(time.perf_counter() - t, 1)
out["F_rows"] = conn.execute("SELECT count(*) FROM entry_facet").fetchone()[0]
out["F_bytes"] = conn.execute("SELECT pg_total_relation_size('entry_facet')").fetchone()[0]
out["F_index_bytes"] = {
    "entryfacet_filter": conn.execute("SELECT pg_relation_size('entryfacet_filter')").fetchone()[0],
    "entryfacet_entry": conn.execute("SELECT pg_relation_size('entryfacet_entry')").fetchone()[0],
}

pairs = conn.execute("SELECT id, concept_id, place_path, n_members FROM bench_pairs WHERE n_members >= 100 ORDER BY id").fetchall()


def page(cid, p, extra=""):
    pf = "" if p == "" else f" AND (ec.place_path = '{p}' OR ec.place_path LIKE '{p}.%')"
    return (
        "SELECT ec.entry_id, min(ec.sort_key) sk FROM concept_closure cl JOIN ec ON ec.concept_id = cl.descendant_id AND ec.published "
        f"WHERE cl.ancestor_id = {cid}{pf} {extra} GROUP BY ec.entry_id ORDER BY sk, ec.entry_id LIMIT 25"
    )


def facet_exists(fid, vid):
    return f" AND EXISTS (SELECT 1 FROM entry_facet f WHERE f.entry_id = ec.entry_id AND f.facet_id = {fid} AND f.value_id = {vid})"


def counts_sql(cid, p):
    pf = "" if p == "" else f" AND (ec.place_path = '{p}' OR ec.place_path LIKE '{p}.%')"
    return (
        "WITH m AS (SELECT DISTINCT ec.entry_id FROM concept_closure cl JOIN ec ON ec.concept_id = cl.descendant_id AND ec.published "
        f"WHERE cl.ancestor_id = {cid}{pf}) SELECT f.facet_id, f.value_id, count(*) FROM m JOIN entry_facet f ON f.entry_id = m.entry_id GROUP BY 1, 2"
    )


def timed(sql):
    t = time.perf_counter()
    try:
        conn.execute(sql).fetchall()
        return (time.perf_counter() - t) * 1000
    except psycopg.errors.QueryCanceled:
        return 30000.0


buckets = {"100-999": (100, 1000), "1k-9.9k": (1000, 10000), "10k-99k": (10000, 100000), ">=100k": (100000, 10**9)}
F = {}
for name, (lo, hi) in buckets.items():
    sel = [p for p in pairs if lo <= p[3] < hi]
    if not sel:
        continue
    res = {"pairs": len(sel), "no_filter": [], "one_facet": [], "two_facets": [], "sidebar_counts": []}
    for (pid, cid, p, nm) in sel:
        f1 = (rng.randint(1, 4), 1)  # a common value (value 1 is the most used)
        f2 = (rng.randint(1, 4), 2)
        res["no_filter"].append(timed(page(cid, p)))
        res["one_facet"].append(timed(page(cid, p, facet_exists(*f1))))
        res["two_facets"].append(timed(page(cid, p, facet_exists(*f1) + facet_exists(*f2))))
        res["sidebar_counts"].append(timed(counts_sql(cid, p)))
    F[name] = {"pairs": res["pairs"], **{k: stats(v) for k, v in res.items() if k != "pairs"}}
    print(name, F[name], flush=True)
out["F_list_with_facets"] = F
conn.execute("DROP TABLE IF EXISTS entry_facet")
json.dump(out, open(f"{OUT}/resolve_and_facets.json", "w"), indent=1)
