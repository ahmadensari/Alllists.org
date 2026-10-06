#!/usr/bin/env python3
"""Roll-up benchmark, part 1: set-based full build of every (place, node) cell, then the store rule.

Algorithm (tree-reduced, requirement R6 of 01_manufacturing_depth_taxonomy.md section 4.6):
  step 1  per country: GROUP BY (home place, ancestor node) with count(DISTINCT entry). Distinctness is needed only on the
          node axis, because an entry sits in several nodes under the same ancestor.
  step 2  place axis is additive (an entry has exactly one home place), so every place prefix is a plain SUM of step 1.
  step 3  world cells = sum of the country cells.
  rule    keep a cell when published >= 25 or verified >= 10 (pinned cells are not simulated). "Members" means published
          entries, the ones a visitor can see on the page.

  sudo -u postgres env PYTHONPATH=/var/tmp/benchlibs python3 taxonomy_05_rollup_build.py DBNAME OUTDIR
"""
import json
import re
import sys
import time

import psycopg

DB, OUT = sys.argv[1], sys.argv[2]
assert re.fullmatch(r"bench_taxonomy_[a-z0-9_]+", DB)
conn = psycopg.connect(dbname=DB, user="postgres", autocommit=True)
conn.execute("SET work_mem = '256MB'")
conn.execute("SET maintenance_work_mem = '1GB'")

conn.execute("DROP TABLE IF EXISTS rollup_all, rollup_cell, place_total")
conn.execute(
    """
CREATE OR REPLACE FUNCTION place_prefixes(p text) RETURNS SETOF text LANGUAGE sql IMMUTABLE AS $$
  SELECT '' UNION ALL
  SELECT array_to_string((string_to_array(p, '.'))[1:i], '.') FROM generate_series(1, array_length(string_to_array(p, '.'), 1)) i
$$
"""
)
conn.execute(
    "CREATE UNLOGGED TABLE rollup_all (place_path text NOT NULL, concept_id int NOT NULL, total int NOT NULL, published int NOT NULL, verified int NOT NULL)"
)
countries = [r[0] for r in conn.execute("SELECT country_code FROM entry GROUP BY 1 ORDER BY count(*) DESC").fetchall()]
t_all = time.perf_counter()
per_country = []
for cc in countries:
    t0 = time.perf_counter()
    conn.execute("DROP TABLE IF EXISTS leaf")
    # verified = published and best level surveyor or owner (sort_key / 1000 is the trust rank in this synthetic data)
    conn.execute(
        f"""
CREATE TEMP TABLE leaf AS
SELECT ec.place_path, cl.ancestor_id AS concept_id,
       count(DISTINCT ec.entry_id) AS total,
       count(DISTINCT ec.entry_id) FILTER (WHERE ec.published) AS published,
       count(DISTINCT ec.entry_id) FILTER (WHERE ec.published AND ec.sort_key < 2000) AS verified
FROM ec JOIN concept_closure cl ON cl.descendant_id = ec.concept_id
WHERE ec.place_path LIKE '{cc}.%'
GROUP BY 1, 2
"""
    )
    t1 = time.perf_counter()
    leaf_rows = conn.execute("SELECT count(*) FROM leaf").fetchone()[0]
    conn.execute(
        """
INSERT INTO rollup_all
SELECT pp, concept_id, sum(total), sum(published), sum(verified)
FROM leaf, LATERAL place_prefixes(leaf.place_path) pp
WHERE pp <> ''
GROUP BY pp, concept_id
"""
    )
    t2 = time.perf_counter()
    n = conn.execute("SELECT count(*) FROM entry WHERE country_code = %s", (cc,)).fetchone()[0]
    per_country.append((cc, n, leaf_rows, round(t1 - t0, 2), round(t2 - t1, 2)))
t3 = time.perf_counter()
conn.execute(
    "INSERT INTO rollup_all SELECT '', concept_id, sum(total), sum(published), sum(verified) FROM rollup_all WHERE place_path NOT LIKE '%.%' GROUP BY concept_id"
)
t4 = time.perf_counter()
conn.execute("CREATE UNIQUE INDEX rollup_all_pk ON rollup_all (place_path, concept_id)")
conn.execute("ANALYZE rollup_all")
total_build_s = time.perf_counter() - t_all
cells_all = conn.execute("SELECT count(*) FROM rollup_all").fetchone()[0]

# store rule
conn.execute(
    """
CREATE TABLE rollup_cell (
    place_path text NOT NULL, concept_id int NOT NULL, total int NOT NULL, published int NOT NULL, verified int NOT NULL,
    PRIMARY KEY (place_path, concept_id)
) WITH (fillfactor = 70)
"""
)
conn.execute("INSERT INTO rollup_cell SELECT * FROM rollup_all WHERE published >= 25 OR verified >= 10")
conn.execute("ANALYZE rollup_cell")
conn.execute(
    "CREATE TABLE place_total AS SELECT place_path, sum(total) AS total, sum(published) AS published FROM (SELECT p AS place_path, count(*) AS total, count(*) FILTER (WHERE publish_state = 1) AS published FROM entry, LATERAL place_prefixes(entry.place_path) p GROUP BY 1) x GROUP BY 1"
)
conn.execute("ALTER TABLE place_total ADD PRIMARY KEY (place_path)")

stats = {}
stats["countries"] = len(countries)
stats["build_seconds_total"] = round(total_build_s, 1)
stats["world_step_seconds"] = round(t4 - t3, 2)
stats["cells_all"] = cells_all
stats["cells_published_ge25"] = conn.execute("SELECT count(*) FROM rollup_all WHERE published >= 25").fetchone()[0]
stats["cells_verified_ge10"] = conn.execute("SELECT count(*) FROM rollup_all WHERE verified >= 10").fetchone()[0]
stats["cells_stored"] = conn.execute("SELECT count(*) FROM rollup_cell").fetchone()[0]
stats["cells_published_ge10"] = conn.execute("SELECT count(*) FROM rollup_all WHERE published >= 10").fetchone()[0]
stats["cells_published_eq1"] = conn.execute("SELECT count(*) FROM rollup_all WHERE published = 1").fetchone()[0]
stats["cells_published_ge1"] = conn.execute("SELECT count(*) FROM rollup_all WHERE published >= 1").fetchone()[0]
stats["rollup_all_bytes"] = conn.execute("SELECT pg_total_relation_size('rollup_all')").fetchone()[0]
stats["rollup_cell_bytes"] = conn.execute("SELECT pg_total_relation_size('rollup_cell')").fetchone()[0]
stats["place_total_rows"] = conn.execute("SELECT count(*) FROM place_total").fetchone()[0]
stats["memberships"] = conn.execute("SELECT count(*) FROM ec").fetchone()[0]
stats["entries"] = conn.execute("SELECT count(*) FROM entry").fetchone()[0]
by_level = conn.execute(
    """
SELECT array_length(string_to_array(NULLIF(place_path, ''), '.'), 1) AS place_level,
       count(*) AS cells_all, count(*) FILTER (WHERE published >= 25 OR verified >= 10) AS cells_stored
FROM rollup_all GROUP BY 1 ORDER BY 1 NULLS FIRST
"""
).fetchall()
stats["by_place_level"] = [list(r) for r in by_level]
stats["per_country_first5"] = per_country[:5]
stats["per_country_seconds_largest"] = per_country[0]
json.dump(stats, open(f"{OUT}/rollup_build.json", "w"), indent=1, default=str)
print(json.dumps(stats, indent=1, default=str))
