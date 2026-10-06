#!/usr/bin/env python3
"""Cost of changing the concept graph: closure table against ltree paths against the ltree copy on membership rows.

Every edit runs inside a transaction that is rolled back, so the data stays as generated.
  add    a secondary edge parent -> child (the child keeps its own subtree)
  remove the same edge again (rebuild what depended on it)

  closure        rows inserted into concept_closure (ancestor x descendant cross product, minus pairs that exist)
  ltree          rows inserted into concept_path (every path of the new parent x every relative path below the child)
  ltree_on_ec    memberships in the child subtree whose ec_lt.cpaths array must be rewritten (counted, and timed for
                 the smaller cases)

  sudo -u postgres env PYTHONPATH=/var/tmp/benchlibs python3 taxonomy_07_graph_edits.py DBNAME OUTDIR
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
conn.execute("SET work_mem = '128MB'")
rng = random.Random(11)

levels = {r[0]: (r[1], r[2]) for r in conn.execute("SELECT level, first_id, n FROM lv").fetchall()}


def pick_edge(child_level):
    while True:
        f, n = levels[child_level]
        child = f + rng.randrange(n)
        pf, pn = levels[child_level - 1]
        parent = pf + rng.randrange(pn)
        if conn.execute("SELECT 1 FROM concept_edge WHERE parent_id = %s AND child_id = %s", (parent, child)).fetchone() is None:
            return parent, child


CLOSURE_ADD = """
INSERT INTO concept_closure (ancestor_id, descendant_id, depth)
SELECT a.ancestor_id, d.descendant_id, a.depth + d.depth + 1
FROM concept_closure a JOIN concept_closure d ON d.ancestor_id = %(c)s
WHERE a.descendant_id = %(p)s
ON CONFLICT (ancestor_id, descendant_id) DO UPDATE SET depth = LEAST(EXCLUDED.depth, concept_closure.depth)
"""

LTREE_ADD = """
INSERT INTO concept_path (concept_id, path)
SELECT sub.concept_id, pp.path || sub.suffix
FROM concept_path pp
CROSS JOIN LATERAL (
    SELECT cp.concept_id, subpath(cp.path, nlevel(src.path) - 1) AS suffix
    FROM (SELECT path FROM concept_path WHERE concept_id = %(c)s LIMIT 1) src
    JOIN concept_path cp ON cp.path <@ src.path
) sub
WHERE pp.concept_id = %(p)s
"""

# rebuild after removing the edge: closure rows of the child subtree that came from outside, recomputed level by level
CLOSURE_REBUILD = """
DROP TABLE IF EXISTS _sub;
CREATE TEMP TABLE _sub AS SELECT descendant_id AS id FROM concept_closure WHERE ancestor_id = %(c)s;
DELETE FROM concept_closure WHERE descendant_id IN (SELECT id FROM _sub) AND ancestor_id NOT IN (SELECT id FROM _sub);
"""
CLOSURE_REBUILD_LEVEL = """
INSERT INTO concept_closure (ancestor_id, descendant_id, depth)
SELECT cl.ancestor_id, e.child_id, cl.depth + 1
FROM concept_edge e
JOIN concept c ON c.id = e.child_id AND c.level = %(lvl)s AND c.id IN (SELECT id FROM _sub)
JOIN concept_closure cl ON cl.descendant_id = e.parent_id
ON CONFLICT (ancestor_id, descendant_id) DO UPDATE SET depth = LEAST(EXCLUDED.depth, concept_closure.depth)
"""
LTREE_REMOVE = "DELETE FROM concept_path cp USING concept_path src WHERE src.concept_id = %(p)s AND cp.path <@ src.path || ('n' || %(c)s)::ltree"


def timed(fn):
    t = time.perf_counter()
    r = fn()
    return (time.perf_counter() - t) * 1000, r


results = []
for child_level in (2, 3, 4, 5):
    rows = []
    for _ in range(12):
        p, c = pick_edge(child_level)
        n_desc = conn.execute("SELECT count(*) FROM concept_closure WHERE ancestor_id = %s", (c,)).fetchone()[0]
        n_anc = conn.execute("SELECT count(*) FROM concept_closure WHERE descendant_id = %s", (p,)).fetchone()[0]
        n_members = conn.execute(
            "SELECT count(*) FROM ec JOIN concept_closure cl ON cl.descendant_id = ec.concept_id WHERE cl.ancestor_id = %s", (c,)
        ).fetchone()[0]
        rec = {"child_level": child_level, "parent": p, "child": c, "desc_nodes": n_desc, "parent_ancestors": n_anc, "members_in_subtree": n_members}
        # --- closure: add
        conn.execute("BEGIN")
        conn.execute("INSERT INTO concept_edge (parent_id, child_id, is_primary) VALUES (%s, %s, false)", (p, c))
        ms, cur = timed(lambda: conn.execute(CLOSURE_ADD, {"c": c, "p": p}))
        rec["closure_add_ms"], rec["closure_rows_written"] = round(ms, 2), cur.rowcount
        # --- closure: remove (rebuild subtree), still inside the same transaction
        conn.execute("DELETE FROM concept_edge WHERE parent_id = %s AND child_id = %s", (p, c))
        t = time.perf_counter()
        conn.execute(CLOSURE_REBUILD, {"c": c})
        for lvl in range(child_level, 6):
            conn.execute(CLOSURE_REBUILD_LEVEL, {"lvl": lvl})
        rec["closure_remove_ms"] = round((time.perf_counter() - t) * 1000, 2)
        conn.execute("ROLLBACK")
        # --- ltree: add
        conn.execute("BEGIN")
        conn.execute("INSERT INTO concept_edge (parent_id, child_id, is_primary) VALUES (%s, %s, false)", (p, c))
        ms, cur = timed(lambda: conn.execute(LTREE_ADD, {"c": c, "p": p}))
        rec["ltree_add_ms"], rec["ltree_rows_written"] = round(ms, 2), cur.rowcount
        conn.execute("ROLLBACK")
        # --- ltree: remove one parent's paths under the child (rows deleted)
        conn.execute("BEGIN")
        ms, cur = timed(lambda: conn.execute(LTREE_REMOVE, {"p": rng.choice([r[0] for r in conn.execute("SELECT parent_id FROM concept_edge WHERE child_id = %s", (c,)).fetchall()]), "c": c}))
        rec["ltree_remove_ms"], rec["ltree_rows_deleted"] = round(ms, 2), cur.rowcount
        conn.execute("ROLLBACK")
        # --- ltree copy on membership rows: how many ec_lt rows are in the child subtree (they all change)
        rec["ltree_on_ec_rows_to_rewrite"] = n_members
        if n_members <= 150000:
            conn.execute("BEGIN")
            ms, cur = timed(
                lambda: conn.execute(
                    "UPDATE ec_lt SET cpaths = cpaths || (SELECT array_agg(path) FROM concept_path WHERE concept_id = %s) "
                    "WHERE concept_id IN (SELECT descendant_id FROM concept_closure WHERE ancestor_id = %s)",
                    (p, c),
                )
            )
            rec["ltree_on_ec_update_ms"], rec["ltree_on_ec_rows_updated"] = round(ms, 1), cur.rowcount
            conn.execute("ROLLBACK")
        rows.append(rec)
    results += rows


def med(rows, key):
    xs = [r[key] for r in rows if key in r]
    return round(statistics.median(xs), 2) if xs else None


def p95(rows, key):
    xs = sorted(r[key] for r in rows if key in r)
    return xs[min(len(xs) - 1, int(0.95 * len(xs)))] if xs else None


summary = []
for lvl in (2, 3, 4, 5):
    rs = [r for r in results if r["child_level"] == lvl]
    summary.append(
        {
            "child_level": lvl,
            "median_desc_nodes": med(rs, "desc_nodes"),
            "median_members_in_subtree": med(rs, "members_in_subtree"),
            "closure_add_ms_median": med(rs, "closure_add_ms"),
            "closure_add_ms_p95": p95(rs, "closure_add_ms"),
            "closure_rows_written_median": med(rs, "closure_rows_written"),
            "closure_remove_ms_median": med(rs, "closure_remove_ms"),
            "closure_remove_ms_p95": p95(rs, "closure_remove_ms"),
            "ltree_add_ms_median": med(rs, "ltree_add_ms"),
            "ltree_add_ms_p95": p95(rs, "ltree_add_ms"),
            "ltree_rows_written_median": med(rs, "ltree_rows_written"),
            "ltree_remove_ms_median": med(rs, "ltree_remove_ms"),
            "ltree_on_ec_rows_median": med(rs, "ltree_on_ec_rows_to_rewrite"),
            "ltree_on_ec_rows_max": max(r["ltree_on_ec_rows_to_rewrite"] for r in rs),
            "ltree_on_ec_update_ms_median": med(rs, "ltree_on_ec_update_ms"),
        }
    )
json.dump({"summary": summary, "rows": results}, open(f"{OUT}/graph_edits.json", "w"), indent=1)
for s in summary:
    print(s)
