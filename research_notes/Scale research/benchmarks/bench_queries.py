#!/usr/bin/env python3
"""List-page query benchmark: "published entries under node X at place Y", page of 25, ordered by sort_key.

Variants (all return the same entries; checked by --verify):
  closure        concept_closure join, membership table ec with text place_path (text_pattern_ops)
  ltree_resolver concept_path (ltree, GiST) resolves the descendant nodes, then the same ec join
  rcte           recursive CTE over concept_edge resolves the descendant nodes, then the same ec join
  ltree_denorm   every root-to-node path copied onto the membership row (ec_lt.cpaths ltree[] with GiST)
  closure_ltplace closure + place path stored as ltree with GiST (ec_pl)
  closure_placeidx closure + an extra place-major index on ec (place_path, concept_id)

Run as the postgres OS user against a scratch database whose name starts with bench_taxonomy_:
  sudo -u postgres env PYTHONPATH=/var/tmp/benchlibs python3 bench_queries.py DBNAME OUTDIR
"""
import csv
import re
import statistics
import sys
import time

import psycopg

DB = sys.argv[1]
OUT = sys.argv[2]
assert re.fullmatch(r"bench_taxonomy_[a-z0-9_]+", DB), "scratch database names only"
TIMEOUT_MS = 30000
REPS = 3
SAFE = re.compile(r"[a-z0-9_.]*")

conn = psycopg.connect(dbname=DB, user="postgres", autocommit=True)
conn.execute("SET work_mem = '64MB'")  # per session; the server default is 4MB
conn.execute(f"SET statement_timeout = {TIMEOUT_MS}")


def place_filter(alias, y):
    if y == "":
        return ""
    assert SAFE.fullmatch(y)
    return f" AND ({alias}.place_path = '{y}' OR {alias}.place_path LIKE '{y}.%')"


def tail(hit_select):
    return (
        f"WITH hit AS ({hit_select}) "
        "SELECT e.id, e.name FROM hit JOIN entry e ON e.id = hit.entry_id ORDER BY hit.sk, hit.entry_id"
    )


def page_select(frm, where):
    return (
        f"SELECT ec.entry_id, min(ec.sort_key) AS sk FROM {frm} WHERE ec.published {where} "
        "GROUP BY ec.entry_id ORDER BY min(ec.sort_key), ec.entry_id LIMIT 25"
    )


def count_sql(frm, where):
    return f"SELECT count(DISTINCT ec.entry_id) FROM {frm} WHERE ec.published {where}"


def parts(variant, x, y):
    """Return (from_clause, where_clause, with_prefix) for the variant."""
    pf = place_filter("ec", y)
    if variant in ("closure", "closure_placeidx"):
        return "concept_closure cl JOIN ec ON ec.concept_id = cl.descendant_id", f"AND cl.ancestor_id = {x}{pf}", ""
    if variant == "ltree_resolver":
        frm = (
            "(SELECT DISTINCT cp.concept_id FROM concept_path xp JOIN concept_path cp ON cp.path <@ xp.path "
            f"WHERE xp.concept_id = {x}) d JOIN ec ON ec.concept_id = d.concept_id"
        )
        return frm, pf, ""
    if variant == "rcte":
        pre = (
            f"WITH RECURSIVE d(id) AS (SELECT {x}::int UNION SELECT e.child_id FROM concept_edge e JOIN d ON e.parent_id = d.id) "
        )
        return "d JOIN ec ON ec.concept_id = d.id", pf, pre
    if variant == "ltree_denorm":
        cur = conn.execute("SELECT path::text FROM concept_path WHERE concept_id = %s", (x,))
        paths = [r[0] for r in cur.fetchall()]
        cond = " OR ".join(f"ec.cpaths <@ '{p}'::ltree" for p in paths)
        return "ec_lt ec", f"AND ({cond}){pf}", ""
    if variant == "closure_ltplace":
        lp = "" if y == "" else f" AND ec.place_l <@ '{y}'::ltree"
        return "concept_closure cl JOIN ec_pl ec ON ec.concept_id = cl.descendant_id", f"AND cl.ancestor_id = {x}{lp}", ""
    raise ValueError(variant)


def build(variant, kind, x, y):
    frm, where, pre = parts(variant, x, y)
    if kind == "page":
        sel = page_select(frm, where)
        if pre:  # the recursive CTE must come first; merge it with the hit CTE
            return pre.rstrip() + ", hit AS (" + sel + ") SELECT e.id, e.name FROM hit JOIN entry e ON e.id = hit.entry_id ORDER BY hit.sk, hit.entry_id"
        return tail(sel)
    sel = count_sql(frm, where)
    return pre + sel


def timed(sql):
    t0 = time.perf_counter()
    try:
        cur = conn.execute(sql)
        rows = cur.fetchall()
        return (time.perf_counter() - t0) * 1000, "ok", rows
    except psycopg.errors.QueryCanceled:
        return float(TIMEOUT_MS), "timeout", []


pairs = conn.execute(
    "SELECT id, concept_level, place_level, concept_id, place_path, n_members, n_desc FROM bench_pairs ORDER BY id"
).fetchall()


def run(label, variant, kind):
    rows_out = []
    for (pid, cl, pl, x, y, nm, nd) in pairs:
        sql = build(variant, kind, x, y)
        for rep in range(1, REPS + 1):
            ms, status, _ = timed(sql)
            rows_out.append((label, kind, pid, rep, round(ms, 3), status))
    return rows_out


def verify(variants, sample=40):
    """All variants must return the same first page and the same count."""
    bad = 0
    for (pid, cl, pl, x, y, nm, nd) in pairs[:: max(1, len(pairs) // sample)]:
        ref = None
        for v in variants:
            _, st, rows = timed(build(v, "page", x, y))
            if st != "ok":
                continue
            if ref is None:
                ref = rows
            elif rows != ref:
                bad += 1
                print("MISMATCH", v, pid, x, y)
    print("verify: mismatches =", bad)


if __name__ == "__main__":
    mode = sys.argv[3] if len(sys.argv) > 3 else "all"
    results = []
    if mode in ("verify", "all"):
        verify(["closure", "ltree_resolver", "rcte", "ltree_denorm", "closure_ltplace"])
    if mode in ("all",):
        for v in ["closure", "ltree_resolver", "rcte", "ltree_denorm", "closure_ltplace"]:
            results += run(v, v, "page")
            print("done page", v, flush=True)
        for v in ["closure", "ltree_resolver", "rcte"]:
            results += run(v, v, "count")
            print("done count", v, flush=True)
        # extra place-major index, then repeat the closure page query
        conn.execute("CREATE INDEX ec_place_concept ON ec (place_path text_pattern_ops, concept_id) INCLUDE (entry_id, sort_key) WHERE published")
        conn.execute("ANALYZE ec")
        sz = conn.execute("SELECT pg_relation_size('ec_place_concept')").fetchone()[0]
        print("ec_place_concept size bytes", sz)
        results += run("closure_placeidx", "closure_placeidx", "page")
        results += run("closure_placeidx", "closure_placeidx", "count")
        conn.execute("DROP INDEX ec_place_concept")
        with open(f"{OUT}/query_raw.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["label", "kind", "pair_id", "rep", "ms", "status"])
            w.writerows(results)
        print("wrote", len(results), "rows")
