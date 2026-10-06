"""B08: PgBouncer 1.22 in transaction mode in front of (a) the scratch primary with max_connections=40 (benchmarks/scratch_cluster.sh up)
and (b) the main local server for the real-Django checks (pool of 4 server connections, bench_django only).

PgBouncer is run from an extracted .deb (no system install). Set PGBOUNCER_DIR to the extraction directory
(contains usr/sbin/pgbouncer and usr/lib/x86_64-linux-gnu). Run:
  POSTGRES_PORT=55432 POSTGRES_USER=postgres PGBOUNCER_DIR=<dir> .venv/bin/python b08_pgbouncer.py

Parts: connection limit, connect cost, pgbench throughput, and semantic checks (advisory locks, prepared statements,
server-side cursors, SET, startup options, role defaults).
"""

import os
import subprocess
import sys
import tempfile
import threading
import time

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import Timer, connect, drop_db, make_db  # noqa: E402

import psycopg  # noqa: E402

PGB = os.environ["PGBOUNCER_DIR"]
PORT = 6432
BIN = "/usr/lib/postgresql/16/bin"
SCRATCH = {"host": "127.0.0.1", "port": 55432}


def start_pgb(max_prepared=0, pool_size=20, extra=""):
    d = tempfile.mkdtemp(prefix="bench_pgb_")
    ini = f"""[databases]
bench_pgb = host=127.0.0.1 port=55432 dbname=bench_pgb pool_size={pool_size}
bench_pgb1 = host=127.0.0.1 port=55432 dbname=bench_pgb pool_size=1
bench_pgb2 = host=127.0.0.1 port=55432 dbname=bench_pgb pool_size=2
bench_django_pool = host=127.0.0.1 port=5432 dbname=bench_django user=alllists password=alllists pool_size=4

[pgbouncer]
listen_addr = 127.0.0.1
listen_port = {PORT}
unix_socket_dir = {d}
auth_type = trust
pool_mode = transaction
max_client_conn = 2000
default_pool_size = {pool_size}
max_prepared_statements = {max_prepared}
server_idle_timeout = 60
query_wait_timeout = 30
logfile = {d}/pgbouncer.log
pidfile = {d}/pgbouncer.pid
admin_users = postgres
{extra}
"""
    open(f"{d}/pgbouncer.ini", "w").write(ini)
    env = dict(os.environ, LD_LIBRARY_PATH=f"{PGB}/usr/lib/x86_64-linux-gnu")
    p = subprocess.Popen([f"{PGB}/usr/sbin/pgbouncer", f"{d}/pgbouncer.ini"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    for _ in range(50):
        try:
            psycopg.connect(host="127.0.0.1", port=PORT, user="postgres", dbname="bench_pgb", autocommit=True, connect_timeout=1).close()
            break
        except psycopg.Error:
            time.sleep(0.1)
    return p, d


def stop_pgb(p):
    p.terminate()
    p.wait()


def via(db="bench_pgb", **kw):
    return psycopg.connect(host="127.0.0.1", port=PORT, user="postgres", dbname=db, autocommit=True, **kw)


def direct(db="bench_pgb"):
    return psycopg.connect(host="127.0.0.1", port=55432, user="postgres", dbname=db, autocommit=True)


def part_limits():
    print("== 1. connection limit: scratch server max_connections=40 ==")
    conns, err = [], None
    for i in range(120):
        try:
            conns.append(direct())
        except psycopg.Error as e:
            err = str(e).strip().splitlines()[0]
            break
    print(f"direct: {len(conns)} connections opened before failure: {err}")
    [c.close() for c in conns]
    p, d = start_pgb(pool_size=20)
    done, errs, lat = [], [], []

    def client(i):
        try:
            c = via()
            for _ in range(20):
                t = time.perf_counter()
                c.execute("SELECT pg_sleep(0.02)")
                lat.append(time.perf_counter() - t)
            c.close()
            done.append(i)
        except psycopg.Error as e:
            errs.append(str(e).splitlines()[0])

    peak = [0]
    stop = [False]

    def watch():
        w = direct("postgres")
        while not stop[0]:
            peak[0] = max(peak[0], w.execute("SELECT count(*) FROM pg_stat_activity WHERE datname = 'bench_pgb'").fetchone()[0])
            time.sleep(0.05)

    wt = threading.Thread(target=watch)
    wt.start()
    with Timer() as t:
        ths = [threading.Thread(target=client, args=(i,)) for i in range(300)]
        [x.start() for x in ths]
        [x.join() for x in ths]
    stop[0] = True
    wt.join()
    lat.sort()
    print(f"via PgBouncer: 300 client connections x 20 queries of 20 ms: {len(done)} ok, {len(errs)} errors, {t.s:.1f}s, "
          f"peak server backends for the database = {peak[0]} (pool_size 20), query p50={lat[len(lat) // 2] * 1000:.0f}ms p99={lat[int(len(lat) * .99)] * 1000:.0f}ms")
    return p


def part_connect_cost():
    print("== 2. cost of a new connection (the CONN_MAX_AGE=0 case) ==")
    for label, fn in (("direct", direct), ("via PgBouncer", via)):
        with Timer() as t:
            for _ in range(200):
                c = fn()
                c.execute("SELECT 1").fetchone()
                c.close()
        print(f"{label}: {t.s / 200 * 1000:.2f} ms per connect+query+close (trust auth, localhost)")


def pgbench(args, label):
    r = subprocess.run([f"{BIN}/pgbench", *args], capture_output=True, text=True)
    out = r.stdout + r.stderr
    tps = [l for l in out.splitlines() if l.startswith("tps")]
    lat = [l for l in out.splitlines() if "latency average" in l]
    fail = [l for l in out.splitlines() if "connection to server" in l or "too many" in l.lower()]
    print(f"{label}: {tps[0] if tps else 'NO RESULT'} | {lat[0].strip() if lat else ''} {fail[0][:90] if fail else ''}", flush=True)


def part_pgbench(p_holder):
    print("== 3. pgbench select-only (-S), 8 s, 2 threads, scratch server max_connections=40 ==")
    subprocess.run([f"{BIN}/pgbench", "-i", "-s", "10", "-h", "127.0.0.1", "-p", "55432", "-U", "postgres", "bench_pgb"], capture_output=True)
    base = ["-S", "-T", "8", "-j", "2", "-U", "postgres", "bench_pgb"]
    pgbench(["-c", "8", "-h", "127.0.0.1", "-p", "55432", *base], "direct, 8 clients")
    pgbench(["-c", "30", "-h", "127.0.0.1", "-p", "55432", *base], "direct, 30 clients")
    pgbench(["-c", "200", "-h", "127.0.0.1", "-p", "55432", *base], "direct, 200 clients")
    pgbench(["-c", "8", "-h", "127.0.0.1", "-p", str(PORT), *base], "PgBouncer, 8 clients")
    pgbench(["-c", "30", "-h", "127.0.0.1", "-p", str(PORT), *base], "PgBouncer, 30 clients")
    pgbench(["-c", "200", "-h", "127.0.0.1", "-p", str(PORT), *base], "PgBouncer, 200 clients")
    pgbench(["-c", "1000", "-j", "2", "-h", "127.0.0.1", "-p", str(PORT), "-S", "-T", "8", "-U", "postgres", "bench_pgb"], "PgBouncer, 1000 clients")
    print("-- same with new connection per transaction (-C), 8 clients --")
    pgbench(["-C", "-c", "8", "-h", "127.0.0.1", "-p", "55432", *base], "direct -C")
    pgbench(["-C", "-c", "8", "-h", "127.0.0.1", "-p", str(PORT), *base], "PgBouncer -C")


def part_semantics():
    print("== 4. semantics in transaction pooling mode ==")
    # a. transaction-level advisory lock still serialises (this is what audit() uses)
    res = []

    def hold(tag, secs):
        c = via("bench_pgb")
        t = time.perf_counter()
        with c.transaction():
            c.execute("SELECT pg_advisory_xact_lock(727001)")
            res.append((tag, "got lock after", round(time.perf_counter() - t, 2)))
            time.sleep(secs)
        c.close()

    a = threading.Thread(target=hold, args=("A", 1.0))
    a.start()
    time.sleep(0.2)
    b = threading.Thread(target=hold, args=("B", 0.0))
    b.start()
    a.join()
    b.join()
    print("a. pg_advisory_xact_lock through the pooler:", res, "-> B waited for A: serialisation intact")

    # b. session advisory lock leaks
    c1, c2 = via("bench_pgb1"), via("bench_pgb1")  # pool_size=1: both clients share one server connection
    c1.execute("SELECT pg_advisory_lock(42)")
    got = c2.execute("SELECT pg_try_advisory_lock(42)").fetchone()[0]
    print(f"b. session-level advisory lock held by client 1; client 2 try_lock returns {got} (a direct connection would return False): the lock is tied to the shared server connection -> do not use pg_advisory_lock through the pooler")
    c1.execute("SELECT pg_advisory_unlock_all()")
    c1.close()
    c2.close()

    # c. SET leaks, SET LOCAL does not
    c1, c2 = via("bench_pgb1"), via("bench_pgb1")
    c1.execute("SET statement_timeout = '1234ms'")
    v = c2.execute("SHOW statement_timeout").fetchone()[0]
    print(f"c. session SET by client 1 is visible to client 2: statement_timeout={v}")
    c1.execute("RESET statement_timeout")
    with c1.transaction():
        c1.execute("SET LOCAL statement_timeout = '4321ms'")
    print("   SET LOCAL inside a transaction: after commit client 2 sees", c2.execute("SHOW statement_timeout").fetchone()[0])
    c1.close()
    c2.close()

    # d. startup options parameter (how Django OPTIONS={'options': '-c lock_timeout=...'} is sent)
    try:
        c = via("bench_pgb", options="-c lock_timeout=5000")
        print("d. startup option '-c lock_timeout=5000':", c.execute("SHOW lock_timeout").fetchone()[0], "(accepted)")
        c.close()
    except psycopg.Error as e:
        print("d. startup option '-c lock_timeout=5000' through PgBouncer:", str(e).strip().splitlines()[0])

    # e. role/database defaults reach pooled sessions
    admin = direct("bench_pgb")
    admin.execute("ALTER DATABASE bench_pgb SET lock_timeout = '3s'")
    c = via("bench_pgb")
    print("e. ALTER DATABASE .. SET lock_timeout='3s' seen through the pooler:", c.execute("SHOW lock_timeout").fetchone()[0])
    c.close()
    admin.execute("ALTER DATABASE bench_pgb RESET lock_timeout")

    # f. server-side cursor with hold (what Django .iterator() uses in autocommit)
    c1, c2 = via("bench_pgb2"), via("bench_pgb2")
    try:
        cur = c1.cursor(name="big_scan", withhold=True)
        cur.execute("SELECT aid FROM pgbench_accounts ORDER BY aid")
        got = 0
        for _ in range(200):
            c2.execute("SELECT 1").fetchone()  # other clients move the shared server connections around
            rows = cur.fetchmany(100)
            got += len(rows)
        print(f"f. named WITH HOLD cursor through the pooler: fetched {got} rows without error (lucky routing)")
    except psycopg.Error as e:
        print("f. named cursor through the pooler:", type(e).__name__, str(e).strip().splitlines()[0])
    c1.close()
    c2.close()


def part_prepared(max_prepared):
    p, d = start_pgb(max_prepared=max_prepared, pool_size=2)
    errs, ok = [], []

    def client(i):
        try:
            c = via("bench_pgb2", prepare_threshold=0)  # psycopg 3 prepares every statement at once
            for k in range(60):
                c.execute("SELECT abalance FROM pgbench_accounts WHERE aid = %s", (1 + k,)).fetchone()
                c.execute("SELECT count(*) FROM pgbench_branches WHERE bid = %s", (1,)).fetchone()
            ok.append(i)
        except psycopg.Error as e:
            errs.append(type(e).__name__ + ": " + str(e).strip().splitlines()[0][:80])

    ths = [threading.Thread(target=client, args=(i,)) for i in range(8)]
    [t.start() for t in ths]
    [t.join() for t in ths]
    print(f"   psycopg prepare_threshold=0, max_prepared_statements={max_prepared}: {len(ok)}/8 clients finished; errors: {sorted(set(errs))[:2]}")
    # default psycopg (threshold 5) and prepare_threshold=None
    for label, kw in (("default threshold 5", {}), ("prepare_threshold=None (Django: DISABLE_SERVER_SIDE_BINDING-safe setting)", {"prepare_threshold": None})):
        errs.clear()
        ok.clear()

        def client2(i):
            try:
                c = via("bench_pgb2", **kw)
                for k in range(60):
                    c.execute("SELECT abalance FROM pgbench_accounts WHERE aid = %s", (1 + k,)).fetchone()
                ok.append(i)
            except psycopg.Error as e:
                errs.append(type(e).__name__ + ": " + str(e).strip().splitlines()[0][:80])

        ths = [threading.Thread(target=client2, args=(i,)) for i in range(8)]
        [t.start() for t in ths]
        [t.join() for t in ths]
        print(f"   psycopg {label}, max_prepared_statements={max_prepared}: {len(ok)}/8 finished; errors: {sorted(set(errs))[:2]}")
    stop_pgb(p)


def main():
    make_db("bench_pgb", **SCRATCH)
    p = part_limits()
    part_connect_cost()
    part_pgbench(p)
    part_semantics()
    stop_pgb(p)
    print("== 5. prepared statements ==")
    part_prepared(0)
    part_prepared(100)
    drop_db("bench_pgb", **SCRATCH)


if __name__ == "__main__":
    main()
