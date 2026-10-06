#!/usr/bin/env python3
"""Turns query_raw.csv (from taxonomy_bench_queries.py) into the markdown tables of the note.
  python3 taxonomy_report_query_tables.py results/taxonomy_query_raw.csv pairs.csv"""
import csv
import statistics
import sys
from collections import defaultdict

raw = list(csv.DictReader(open(sys.argv[1])))
pairs = {int(r["id"]): r for r in csv.DictReader(open(sys.argv[2]))}


def bucket(n):
    n = int(n)
    return "a <100" if n < 100 else "b 100-999" if n < 1000 else "c 1k-9.9k" if n < 10000 else "d 10k-99k" if n < 100000 else "e >=100k"


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(len(xs) * p))]


def table(kind, key):
    cells = defaultdict(list)
    cold = defaultdict(list)
    timeouts = defaultdict(int)
    for r in raw:
        if r["kind"] != kind:
            continue
        p = pairs[int(r["pair_id"])]
        k = (r["label"], key(p))
        ms = float(r["ms"])
        if int(r["rep"]) == 1:
            cold[k].append(ms)
        else:
            cells[k].append(ms)
        if r["status"] == "timeout":
            timeouts[k] += 1
    labels = sorted({k[0] for k in cells})
    keys = sorted({k[1] for k in cells})
    print(f"\n{kind}: median / p95 ms of warm repetitions (reps 2 and 3); timeouts at 30 s counted at 30,000\n")
    print("| " + key.__name__ + " | pairs | " + " | ".join(labels) + " |")
    print("|---|---|" + "---|" * len(labels))
    for kk in keys:
        n = len({int(r["pair_id"]) for r in raw if r["kind"] == kind and key(pairs[int(r["pair_id"])]) == kk and r["label"] == labels[0]})
        row = [f"{statistics.median(cells[(l, kk)]):.1f} / {pct(cells[(l, kk)], 0.95):.0f}" + (f" ({timeouts[(l, kk)]} t/o)" if timeouts[(l, kk)] else "") if cells.get((l, kk)) else "-" for l in labels]
        print(f"| {kk} | {n} | " + " | ".join(row) + " |")
    # all pairs
    print("| all | " + str(len(pairs)) + " | " + " | ".join(f"{statistics.median([v for (l2, _), vs in cells.items() if l2 == l for v in vs]):.1f} / {pct([v for (l2, _), vs in cells.items() if l2 == l for v in vs], 0.95):.0f}" for l in labels) + " |")
    print("| first run, all | | " + " | ".join(f"{statistics.median([v for (l2, _), vs in cold.items() if l2 == l for v in vs]):.1f}" for l in labels) + " |")


for kind in ("page", "count"):
    def size_bucket(p):
        return bucket(p["n_members"])

    size_bucket.__name__ = "members in the cell"
    table(kind, size_bucket)

    def node_level(p):
        return "L" + p["concept_level"]

    node_level.__name__ = "node level"
    table(kind, node_level)

    def place_level(p):
        return ["world", "country", "region", "city", "area"][int(p["place_level"])]

    place_level.__name__ = "place level"
    table(kind, place_level)
