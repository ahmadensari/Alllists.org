"""B02b: repeat the headline writer comparison 3 times, interleaved (round robin) so machine noise hits every variant equally.
Reports median and range of rows/s over the rounds. Uses the functions of b02_audit_alternatives.py.

Run: .venv/bin/python "research_notes/Scale research/benchmarks/b02b_audit_repeat.py" [seconds] [rounds]
"""

import multiprocessing as mp
import statistics
import sys
import time

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import b02_audit_alternatives as b  # noqa: E402
from common import connect, drop_db, make_db, pctl  # noqa: E402


def one(variant, workers, duration, hold):
    b.reset()
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    start_at = time.time() + 2
    ps = [ctx.Process(target=b.worker, args=(variant, i, duration, hold, q, start_at)) for i in range(workers)]
    [p.start() for p in ps]
    res = [q.get() for _ in ps]
    [p.join() for p in ps]
    lat = [x for r in res for x in r[0]]
    rows = sum(r[1] for r in res)
    return rows / duration, pctl(lat, 50) * 1000, pctl(lat, 99) * 1000


def main():
    duration = float(sys.argv[1]) if len(sys.argv) > 1 else 6
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    make_db(b.DB)
    with connect(b.DB) as c:
        c.execute(b.SCHEMA)
    variants = ["current", "chain16", "chain256", "chainC_skew", "unchained", "batch500_chain", "batch500_unchained"]
    cases = [(v, w, 0) for v in variants for w in (1, 8)] + [(v, w, 5) for v in ("current", "chain16", "unchained") for w in (1, 8)]
    results = {c: [] for c in cases}
    for r in range(rounds):
        for case in cases:
            results[case].append(one(case[0], case[1], duration, case[2]))
        print(f"round {r + 1} done", flush=True)
    print("variant | writers | hold ms | rows/s median (min-max over rounds) | p50 ms | p99 ms")
    for case, vals in results.items():
        rates = [v[0] for v in vals]
        print(f"{case[0]} | {case[1]} | {case[2]} | {statistics.median(rates):,.0f} ({min(rates):,.0f}-{max(rates):,.0f}) | "
              f"{statistics.median(v[1] for v in vals):.2f} | {statistics.median(v[2] for v in vals):.1f}")
    drop_db(b.DB)


if __name__ == "__main__":
    main()
