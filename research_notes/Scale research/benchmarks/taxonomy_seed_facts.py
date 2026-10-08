#!/usr/bin/env python3
"""Facts about 01_manufacturing_seed.csv that the schema design relies on (read-only, no database).
  python3 taxonomy_seed_facts.py > results/taxonomy_seed_facts.txt"""
import collections
import csv
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, "..", "01_manufacturing_seed.csv"), encoding="utf-8")))
ids = {r["id"]: r for r in rows}
slugs = {r["slug"]: r for r in rows}
order = {"sector": 1, "industry": 2, "family": 3, "product": 4, "variant": 5}
kids = collections.Counter(r["parent_id"] for r in rows if r["parent_id"])
print("rows", len(rows))
print("by level", dict(collections.Counter(r["level"] for r in rows)))
print("duplicate slugs", len(rows) - len(slugs))
print("max listable children under one parent", kids.most_common(3), "mean", round(sum(kids.values()) / len(kids), 2), "parents with children", len(kids))
print("primary parent not exactly one level above", sum(1 for r in rows if r["parent_id"] and order[r["level"]] != order[ids[r["parent_id"]]["level"]] + 1))
also = []
for r in rows:
    m = re.search(r"also_under=([^;]+)", r["facets"] or "")
    if m:
        also += [(r["slug"], s) for s in m.group(1).split("|")]
perchild = collections.Counter(c for c, _ in also)
print("secondary parent links", len(also), "| missing parent slug", sum(1 for _, p in also if p not in slugs),
      "| parent not one level above child", sum(1 for c, p in also if p in slugs and order[slugs[p]["level"]] + 1 != order[slugs[c]["level"]]),
      "| max secondary parents on one node", max(perchild.values()))
facet_keys, vals, withf = collections.Counter(), set(), 0
for r in rows:
    parts = [x for x in (r["facets"] or "").split(";") if "=" in x and not x.startswith("also_under=")]
    withf += bool(parts)
    for x in parts:
        k, v = x.split("=", 1)
        facet_keys[k] += 1
        vals.update((k, vv) for vv in v.split("|"))
print("rows that declare facet groups", withf, "| facet keys", len(facet_keys), "| distinct (key, value) pairs", len(vals))
print("catch-all names (other, n.e.c., miscellaneous, etc, various)", sum(1 for r in rows if re.search(r"\b(other|n\.e\.c|miscellaneous|etc|various)\b", r["name"], re.I)))
print("longest slug", max(len(r["slug"]) for r in rows), "| longest name", max(len(r["name"]) for r in rows), "chars,", max(len(r["name"].split()) for r in rows), "words")
print("leaf nodes", sum(1 for r in rows if r["id"] not in kids), "| sectors", sum(1 for r in rows if r["level"] == "sector"))
print("rows with an HS code", sum(1 for r in rows if r["hs_code"]), "| with an ISIC code", sum(1 for r in rows if r["isic_code"]))
