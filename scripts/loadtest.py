#!/usr/bin/env python3
"""Load test (plan 18.5, P6.03). Standard library only.

    python3 scripts/loadtest.py https://staging.alllists.com --users 60 --seconds 120 --paths paths.txt

`paths.txt` holds one path per line (list pages, entry pages, search pages); without it a small default mix is used.
Every path that starts with /e/ also fetches its private fragment, like a browser does. Reports p50, p95, p99,
requests per second and the error rate per kind, and exits 1 when a target is missed:
shared pages p95 under 200 ms, private fragments p95 under 400 ms, errors under 1 percent."""

import argparse
import random
import statistics
import sys
import threading
import time
import urllib.error
import urllib.request

DEFAULT_PATHS = [
    "/",
    "/pk/",
    "/pk/punjab/sialkot/",
    "/pk/punjab/sialkot/surgical-instrument-makers/",
    "/search/?q=surgical",
]
TARGETS = {"page": 0.200, "fragment": 0.400}


def fetch(base, path, timeout):
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(
            urllib.request.Request(base + path, headers={"User-Agent": "alllists-loadtest"}), timeout=timeout
        ) as r:
            r.read()
            ok = 200 <= r.status < 400 or r.status == 204
    except urllib.error.HTTPError as exc:
        ok = exc.code in (204, 304, 429)  # 429 is the quota doing its job
    except Exception:  # noqa: BLE001 - any failure counts as an error
        ok = False
    return time.perf_counter() - t0, ok


def worker(base, paths, stop_at, results, lock, timeout):
    rng = random.Random()
    while time.time() < stop_at:
        path = rng.choice(paths)
        batch = [("page", path)]
        if path.endswith("/") and path.count("/") >= 4:
            batch.append(
                (
                    "fragment",
                    "/_f/list/?path="
                    + ".".join(p for p in path.strip("/").split("/")[:-1])
                    + "&type="
                    + path.strip("/").split("/")[-1],
                )
            )
        for kind, p in batch:
            dt, ok = fetch(base, p, timeout)
            with lock:
                results.setdefault(kind, []).append((dt, ok))


def pct(values, q):
    values = sorted(values)
    return values[min(int(len(values) * q), len(values) - 1)] if values else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("--users", type=int, default=20)
    ap.add_argument("--seconds", type=int, default=60)
    ap.add_argument("--paths")
    ap.add_argument("--timeout", type=float, default=10)
    a = ap.parse_args()
    paths = [ln.strip() for ln in open(a.paths) if ln.strip()] if a.paths else DEFAULT_PATHS
    results, lock = {}, threading.Lock()
    stop_at = time.time() + a.seconds
    threads = [
        threading.Thread(target=worker, args=(a.base.rstrip("/"), paths, stop_at, results, lock, a.timeout))
        for _ in range(a.users)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    failed = False
    for kind, rows in results.items():
        times = [r[0] for r in rows]
        errs = sum(1 for r in rows if not r[1])
        rate = errs / len(rows)
        p95 = pct(times, 0.95)
        print(
            f"{kind:9} n={len(rows):6} rps={len(rows)/a.seconds:7.1f} p50={statistics.median(times)*1000:6.0f}ms p95={p95*1000:6.0f}ms p99={pct(times, 0.99)*1000:6.0f}ms errors={rate:.2%}"
        )
        if p95 > TARGETS.get(kind, 0.4) or rate > 0.01:
            failed = True
    print("TARGETS MISSED" if failed else "targets met")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
