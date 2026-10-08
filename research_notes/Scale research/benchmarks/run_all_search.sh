#!/bin/sh
# Runs the search latency benchmark for 1M then 5M. PY is the venv python with psycopg and numpy.
PY=${PY:-python3}
cd "$(dirname "$0")"
$PY run_bench.py --db bench_search --scale 1m > results/search_1m.log 2>&1
$PY run_bench.py --db bench_search --scale 5m > results/search_5m.log 2>&1
