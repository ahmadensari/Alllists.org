#!/bin/bash
# Closure and ltree sizes for three secondary-parent mixes. Creates and drops two scratch databases named bench_taxonomy_*.
# usage: sudo -u postgres ./taxonomy_realistic_trees.sh OUTDIR   (run from this directory)
set -euo pipefail
OUT=$1
for mix in "moderate:0,0,0,0,0,0,0,0,0,1" "seedlike:0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1"; do
  name=${mix%%:*}; arr=${mix#*:}
  db="bench_taxonomy_20261006_${name}"
  case "$db" in bench_taxonomy_*) ;; *) echo "refusing"; exit 1;; esac
  createdb "$db"
  psql -X -d "$db" -v sec_array="$arr" -f taxonomy_01_generate_concepts.sql 2>&1 | grep -v "^Time:\|^$\|NOTICE" > "$OUT/tree_stats_${name}.txt" || true
  dropdb "$db"
done
