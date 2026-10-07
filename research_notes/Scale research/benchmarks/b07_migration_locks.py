"""B07: what a schema change does to live traffic, and what the safe pattern costs. Scratch database bench_mig on the main
local server (5,000,000-row table). A writer thread inserts or updates a row every ~2 ms and a reader thread reads a row
every ~2 ms; the stall is the longest gap either of them saw while the DDL ran.

Cases
  A  lock queue: an old transaction holds a lock, ALTER TABLE waits behind it, every new reader queues behind the ALTER.
     Without lock_timeout the readers stall until the old transaction ends; with lock_timeout=1s the ALTER gives up.
  B  ADD COLUMN: nullable, constant default (PG11+ catalog only), volatile default (rewrite).
  C  CREATE INDEX versus CREATE INDEX CONCURRENTLY.
  D  SET NOT NULL directly versus CHECK ... NOT VALID, VALIDATE, SET NOT NULL.
  E  ADD FOREIGN KEY directly versus NOT VALID + VALIDATE.
  F  ALTER COLUMN TYPE int -> bigint (table rewrite) versus expand and contract (new column, batched copy).

Run: .venv/bin/python "research_notes/Scale research/benchmarks/b07_migration_locks.py" [rows]
"""

import random
import sys
import threading
import time

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import Timer, connect, drop_db, make_db  # noqa: E402

import psycopg  # noqa: E402

DB = "bench_mig"


class Traffic:
    def __init__(self, n):
        self.n = n
        self.stop = False
        self.max_gap = {"writer": 0.0, "reader": 0.0}
        self.count = {"writer": 0, "reader": 0}
        self.errors = 0
        self.th = [threading.Thread(target=self.run, args=(k,), daemon=True) for k in ("writer", "reader")]

    def run(self, kind):
        c = connect(DB)
        c.execute("SET lock_timeout = '30s'")
        rng = random.Random(kind)
        last = time.perf_counter()
        while not self.stop:
            i = rng.randint(1, self.n)
            try:
                if kind == "writer":
                    c.execute("UPDATE t SET touched = now() WHERE id = %s", (i,))
                else:
                    c.execute("SELECT name FROM t WHERE id = %s", (i,)).fetchone()
            except psycopg.Error:
                self.errors += 1
            now = time.perf_counter()
            self.max_gap[kind] = max(self.max_gap[kind], now - last)
            self.count[kind] += 1
            last = now
            time.sleep(0.002)
        c.close()

    def __enter__(self):
        [t.start() for t in self.th]
        time.sleep(1.0)
        self.max_gap = {"writer": 0.0, "reader": 0.0}
        return self

    def __exit__(self, *a):
        time.sleep(0.3)
        self.stop = True
        [t.join() for t in self.th]


def timed_ddl(label, sql, n, setup=None, teardown=None):
    c = connect(DB)
    if setup:
        c.execute(setup)
    with Traffic(n) as tr:
        with Timer() as t:
            try:
                c.execute(sql)
                res = "ok"
            except psycopg.Error as e:
                res = f"FAILED {type(e).__name__}"
    print(f"{label}: DDL {t.s:.2f}s  longest stall writer={tr.max_gap['writer'] * 1000:,.0f}ms reader={tr.max_gap['reader'] * 1000:,.0f}ms  [{res}]", flush=True)
    if teardown:
        c.execute(teardown)
    c.close()


def case_a(n):
    print("== A. lock queue behind an old transaction ==")
    for lt in (None, "1s"):
        old = connect(DB, autocommit=False)
        old.execute("SELECT count(*) FROM t WHERE id < 10")  # ACCESS SHARE held until we end the transaction
        started = threading.Event()

        def alter():
            c = connect(DB)
            if lt:
                c.execute(f"SET lock_timeout = '{lt}'")
            started.set()
            t = time.perf_counter()
            try:
                c.execute("ALTER TABLE t ADD COLUMN IF NOT EXISTS probe_a int")
                r = "ok"
            except psycopg.Error as e:
                r = type(e).__name__
            self_res.append((time.perf_counter() - t, r))
            c.close()

        self_res = []
        with Traffic(n) as tr:
            th = threading.Thread(target=alter)
            th.start()
            started.wait()
            time.sleep(6.0)  # the old transaction (a slow report, an idle-in-transaction web request) lasts 6 s
            old.rollback()
            old.close()
            th.join()
        print(f"lock_timeout={lt or 'none'}: ALTER took {self_res[0][0]:.1f}s -> {self_res[0][1]}; longest stall writer={tr.max_gap['writer'] * 1000:,.0f}ms reader={tr.max_gap['reader'] * 1000:,.0f}ms", flush=True)
        c = connect(DB)
        c.execute("ALTER TABLE t DROP COLUMN IF EXISTS probe_a")
        c.close()


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5_000_000
    make_db(DB)
    c = connect(DB)
    with Timer() as tl:
        c.execute("CREATE TABLE t (id bigserial PRIMARY KEY, country varchar(2) NOT NULL, name varchar(80) NOT NULL, payload text NOT NULL, touched timestamptz, small_id int)")
        c.execute("INSERT INTO t (country, name, payload, small_id) SELECT (ARRAY['PK','IN','BD','LK','NP'])[1 + g %% 5], 'name ' || g, repeat('p', 120) || g, g FROM generate_series(1, %s) g", (n,))
        c.execute("CREATE TABLE ref (code varchar(2) PRIMARY KEY)")
        c.execute("INSERT INTO ref VALUES ('PK'),('IN'),('BD'),('LK'),('NP')")
        c.execute("ANALYZE")
    print(f"loaded {n:,} rows in {tl.s:.0f}s", flush=True)
    case_a(n)
    print("== B. ADD COLUMN ==")
    timed_ddl("ADD COLUMN nullable, no default", "ALTER TABLE t ADD COLUMN b1 int", n)
    timed_ddl("ADD COLUMN with constant default", "ALTER TABLE t ADD COLUMN b2 int NOT NULL DEFAULT 7", n)
    timed_ddl("ADD COLUMN with volatile default (random()) = rewrite", "ALTER TABLE t ADD COLUMN b3 double precision NOT NULL DEFAULT random()", n)
    print("== C. indexes ==")
    timed_ddl("CREATE INDEX (plain)", "CREATE INDEX t_name_plain ON t (name)", n)
    timed_ddl("CREATE INDEX CONCURRENTLY", "CREATE INDEX CONCURRENTLY t_name_conc ON t (payload)", n)
    print("== D. NOT NULL ==")
    c.execute("UPDATE t SET b1 = 1")
    timed_ddl("SET NOT NULL directly (scan under ACCESS EXCLUSIVE)", "ALTER TABLE t ALTER COLUMN b1 SET NOT NULL", n)
    c.execute("ALTER TABLE t ADD COLUMN d1 int")
    c.execute("UPDATE t SET d1 = 1")
    timed_ddl("CHECK NOT VALID (instant)", "ALTER TABLE t ADD CONSTRAINT d1_nn CHECK (d1 IS NOT NULL) NOT VALID", n)
    timed_ddl("VALIDATE CONSTRAINT (SHARE UPDATE EXCLUSIVE, reads and writes continue)", "ALTER TABLE t VALIDATE CONSTRAINT d1_nn", n)
    timed_ddl("SET NOT NULL after validated CHECK (no scan, PG12+)", "ALTER TABLE t ALTER COLUMN d1 SET NOT NULL", n, teardown="ALTER TABLE t DROP CONSTRAINT d1_nn")
    print("== E. foreign key ==")
    timed_ddl("ADD FOREIGN KEY directly", "ALTER TABLE t ADD CONSTRAINT fk_direct FOREIGN KEY (country) REFERENCES ref (code)", n, teardown="ALTER TABLE t DROP CONSTRAINT fk_direct")
    timed_ddl("ADD FOREIGN KEY NOT VALID", "ALTER TABLE t ADD CONSTRAINT fk_nv FOREIGN KEY (country) REFERENCES ref (code) NOT VALID", n)
    timed_ddl("VALIDATE CONSTRAINT fk_nv", "ALTER TABLE t VALIDATE CONSTRAINT fk_nv", n)
    print("== F. int -> bigint ==")
    timed_ddl("ALTER COLUMN TYPE int -> bigint (rewrite, ACCESS EXCLUSIVE)", "ALTER TABLE t ALTER COLUMN small_id TYPE bigint", n)
    c.execute("ALTER TABLE t ADD COLUMN big_id bigint")
    with Traffic(n) as tr:
        with Timer() as t:
            last = 0
            while True:
                hi = c.execute("SELECT max(id) FROM (SELECT id FROM t WHERE id > %s ORDER BY id LIMIT 20000) b", (last,)).fetchone()[0]
                if hi is None:
                    break
                c.execute("UPDATE t SET big_id = small_id WHERE id > %s AND id <= %s AND big_id IS NULL", (last, hi))
                last = hi
    print(f"expand/contract: batched copy of 5M values in 20,000-row batches: {t.s:.1f}s, longest stall writer={tr.max_gap['writer'] * 1000:,.0f}ms reader={tr.max_gap['reader'] * 1000:,.0f}ms", flush=True)
    c.close()
    drop_db(DB)


if __name__ == "__main__":
    main()
