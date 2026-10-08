"""B06: batched, resumable, throttled backfill versus one big UPDATE, on the scratch primary + streaming replica
(benchmarks/scratch_cluster.sh up; run with POSTGRES_PORT=55432 POSTGRES_USER=postgres).

Table t(5,000,000 rows, ~230 B/row). Backfill: set t.depth_fold = lower(country) || ':' || (id % 100) for every row.
A foreground probe (one connection doing point reads and writes every ~3 ms) measures what users feel.

Variants:
  big      one UPDATE statement over all rows
  fixed    keyset batches of 5,000 rows, no pause, no throttle
  throttled keyset batches, adaptive size (target 150 ms per batch), 50% duty cycle, pause while replica replay lag > 2 MB or 1 s
Then: resume after a kill (checkpoint row updated in the same transaction as the batch) and OFFSET versus keyset cost.

Run: POSTGRES_PORT=55432 POSTGRES_USER=postgres .venv/bin/python "research_notes/Scale research/benchmarks/b06_backfill.py" [rows]
"""

import random
import statistics
import sys
import threading
import time

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import Timer, connect, drop_db, make_db, pctl  # noqa: E402

import psycopg  # noqa: E402

DB = "bench_backfill"
REPLICA_PORT = 55433


def setup(n):
    make_db(DB)
    c = connect(DB)
    c.execute("""CREATE TABLE t (id bigserial PRIMARY KEY, country varchar(2) NOT NULL, name varchar(80) NOT NULL,
                 payload text NOT NULL, touched timestamptz, depth_fold text)""")
    with Timer() as tl:
        c.execute("""INSERT INTO t (country, name, payload) SELECT (ARRAY['PK','IN','BD','LK','NP'])[1 + g %% 5], 'name ' || g, repeat('p', 120) || g
                     FROM generate_series(1, %s) g""", (n,))
    c.execute("CREATE INDEX t_country ON t (country)")
    c.execute("CREATE INDEX t_name ON t (name)")
    c.execute("ANALYZE t")
    c.execute("CREATE TABLE backfill_job (name text PRIMARY KEY, last_id bigint NOT NULL, done bigint NOT NULL, status text NOT NULL, updated_at timestamptz NOT NULL DEFAULT now())")
    print(f"loaded {n:,} rows in {tl.s:.0f}s", flush=True)
    return c


def lag_sample(c):
    r = c.execute("SELECT pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn), extract(epoch FROM replay_lag) FROM pg_stat_replication").fetchone()
    if not r:
        return 0, 0.0
    return int(r[0] or 0), float(r[1] or 0.0)


class Monitor(threading.Thread):
    """Samples replica lag every 100 ms and the foreground probe latency."""

    def __init__(self, nrows):
        super().__init__(daemon=True)
        self.stop = False
        self.max_lag_bytes = 0
        self.max_lag_s = 0.0
        self.probe = []
        self.nrows = nrows

    def run(self):
        c = connect(DB)
        p = connect(DB)
        rng = random.Random(3)
        last = 0
        while not self.stop:
            now = time.perf_counter()
            if now - last > 0.1:
                b, s = lag_sample(c)
                self.max_lag_bytes, self.max_lag_s = max(self.max_lag_bytes, b), max(self.max_lag_s, s)
                last = now
            i = rng.randint(1, self.nrows)
            t = time.perf_counter()
            p.execute("UPDATE t SET touched = now() WHERE id = %s", (i,))
            p.execute("SELECT name FROM t WHERE id = %s", (i,)).fetchone()
            self.probe.append(time.perf_counter() - t)
            time.sleep(0.003)
        c.close()
        p.close()


def measure(label, fn, n):
    c = connect(DB)
    w0 = c.execute("SELECT pg_current_wal_lsn()").fetchone()[0]
    s0 = c.execute("SELECT pg_relation_size('t') + pg_indexes_size('t')").fetchone()[0]
    c.execute("DELETE FROM backfill_job")
    m = Monitor(n)
    m.start()
    time.sleep(1)
    base = len(m.probe)
    with Timer() as t:
        extra = fn()
    time.sleep(0.5)
    m.stop = True
    m.join()
    w1 = c.execute("SELECT pg_current_wal_lsn()").fetchone()[0]
    wal = c.execute("SELECT pg_wal_lsn_diff(%s, %s)", (w1, w0)).fetchone()[0]
    s1 = c.execute("SELECT pg_relation_size('t') + pg_indexes_size('t')").fetchone()[0]
    probe = m.probe[base:]
    print(f"{label}: {t.s:.1f}s, WAL {float(wal) / 1e6:,.0f} MB, table+index growth {(s1 - s0) / 1e6:,.0f} MB, "
          f"probe (read+write) p50={pctl(probe, 50) * 1000:.1f}ms p99={pctl(probe, 99) * 1000:.1f}ms max={max(probe) * 1000:.0f}ms (n={len(probe)}), "
          f"max replica lag {m.max_lag_bytes / 1e6:.1f} MB / {m.max_lag_s:.2f}s {extra or ''}", flush=True)
    c.close()


def reset_col(c):
    c.execute("UPDATE t SET depth_fold = NULL")
    c.execute("VACUUM (ANALYZE) t")
    # let the replica catch up before the next variant
    while lag_sample(c)[0] > 1_000_000:
        time.sleep(0.5)


def big():
    c = connect(DB)
    c.execute("UPDATE t SET depth_fold = lower(country) || ':' || (id % 100)")
    c.close()


SLICE = "SELECT max(id), count(*) FROM (SELECT id FROM t WHERE id > %s ORDER BY id LIMIT %s) b"
UPD = "UPDATE t SET depth_fold = lower(country) || ':' || (id %% 100) WHERE id > %s AND id <= %s AND depth_fold IS NULL"


def batch(c, name, last, n):
    """One transaction: update a keyset slice and move the checkpoint. Returns (new_last, rows_in_slice)."""
    with c.transaction():
        hi, cnt = c.execute(SLICE, (last, n)).fetchone()
        if hi is None:
            return last, 0
        c.execute(UPD, (last, hi))
        c.execute("INSERT INTO backfill_job (name, last_id, done, status) VALUES (%s, %s, %s, 'running') "
                  "ON CONFLICT (name) DO UPDATE SET last_id = EXCLUDED.last_id, done = backfill_job.done + EXCLUDED.done, updated_at = now()", (name, hi, cnt))
    return hi, cnt


def run_batches(name, n, mode, kill_after=None, replica=None):
    c = connect(DB)
    r = c.execute("SELECT last_id FROM backfill_job WHERE name = %s", (name,)).fetchone()
    last = r[0] if r else 0
    batches = 0
    size = n
    paused = 0.0
    lc = connect(DB)
    while True:
        if mode == "throttled":
            while True:
                b, s = lag_sample(lc)
                if b <= 2_000_000 and s <= 1.0:
                    break
                time.sleep(0.2)
                paused += 0.2
        t = time.perf_counter()
        last, cnt = batch(c, name, last, size)
        dt = time.perf_counter() - t
        if not cnt:
            break
        batches += 1
        if mode == "throttled":
            size = max(1000, min(50_000, int(size * (0.15 / max(dt, 0.001)) ** 0.5)))
            time.sleep(dt)  # 50% duty cycle
        if kill_after and batches >= kill_after:
            c.close()
            return "killed", batches, last
    c.execute("UPDATE backfill_job SET status = 'done' WHERE name = %s", (name,))
    return "done", batches, last, round(paused, 1)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
    c = setup(n)
    # wait for replica to be in sync
    while lag_sample(c)[0] > 1_000_000:
        time.sleep(0.5)
    print("== backfill variants (foreground probe running throughout) ==", flush=True)
    measure("big single UPDATE", big, n)
    reset_col(c)
    measure("fixed 5,000-row batches, no pause", lambda: run_batches("fixed", 5000, "fixed"), n)
    reset_col(c)
    measure("throttled adaptive batches + replica lag guard", lambda: run_batches("thr", 5000, "throttled"), n)
    ok = c.execute("SELECT count(*) FROM t WHERE depth_fold IS NULL").fetchone()[0]
    wrong = c.execute("SELECT count(*) FROM t WHERE depth_fold <> lower(country) || ':' || (id % 100)").fetchone()[0]
    print(f"after throttled run: rows still NULL={ok}, rows with wrong value={wrong}")

    print("== resume after kill ==", flush=True)
    reset_col(c)
    c.execute("DELETE FROM backfill_job")
    kill = max(1, n // 5000 // 2)  # kill half way
    st = run_batches("res", 5000, "fixed", kill_after=kill)
    mid = c.execute("SELECT last_id, done, status FROM backfill_job WHERE name='res'").fetchone()
    nulls_mid = c.execute("SELECT count(*) FROM t WHERE depth_fold IS NULL").fetchone()[0]
    print(f"killed after {kill} batches: {st}; checkpoint {mid}; NULL rows left {nulls_mid:,}")
    with Timer() as t:
        st = run_batches("res", 5000, "fixed")
    fin = c.execute("SELECT last_id, done, status FROM backfill_job WHERE name='res'").fetchone()
    print(f"resumed: {st} in {t.s:.1f}s; checkpoint {fin}; NULL left {c.execute('SELECT count(*) FROM t WHERE depth_fold IS NULL').fetchone()[0]}, "
          f"rows touched exactly once: done={fin[1]:,} vs table {n:,} (live inserts by probe excluded)")

    print("== OFFSET versus keyset at depth ==")
    for off in (0, n // 2, n - 10_000):
        with Timer() as t1:
            c.execute("SELECT id FROM t ORDER BY id OFFSET %s LIMIT 5000", (off,)).fetchall()
        with Timer() as t2:
            c.execute("SELECT id FROM t WHERE id > %s ORDER BY id LIMIT 5000", (off,)).fetchall()
        print(f"position {off:>9,}: OFFSET {t1.s * 1000:7.1f} ms   keyset {t2.s * 1000:5.1f} ms")
    c.close()
    drop_db(DB)


if __name__ == "__main__":
    main()
