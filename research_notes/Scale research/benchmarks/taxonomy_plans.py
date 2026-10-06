#!/usr/bin/env python3
"""Saves EXPLAIN (ANALYZE, BUFFERS) output of the list-page query for four representative pages and every variant.
  sudo -u postgres env PYTHONPATH=/var/tmp/benchlibs python3 taxonomy_plans.py DBNAME OUTDIR"""
import sys

sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], "none"]
import taxonomy_bench_queries as q  # noqa: E402  (module code connects; the main guard keeps it from running the benchmark)

picks = {}
for (pid, cl, pl, x, y, nm, nd) in q.pairs:
    key = (cl, pl)
    picks.setdefault(key, []).append((nm, pid, x, y))
want = [("small cell: product variant in one region", (5, 2)), ("medium cell: family in one country", (3, 1)), ("large cell: sector in one country", (1, 1)), ("huge cell: sector in the world", (1, 0))]
out = []
for label, key in want:
    nm, pid, x, y = sorted(picks[key])[len(picks[key]) // 2]
    out.append(f"\n==== {label}: pair {pid}, node {x}, place {y!r}, {nm} members ====\n")
    for v in ["closure", "rcte", "ltree_resolver", "ltree_denorm", "closure_ltplace"]:
        sql = q.build(v, "page", x, y)
        out.append(f"\n--- variant {v}\n")
        try:
            rows = q.conn.execute("EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, SUMMARY ON) " + sql).fetchall()
            out.append("\n".join(r[0] for r in rows))
        except Exception as e:  # noqa: BLE001
            out.append(f"ERROR {e}")
open(f"{sys.argv[2]}/plans.txt", "w").write("\n".join(out))
print("saved")
