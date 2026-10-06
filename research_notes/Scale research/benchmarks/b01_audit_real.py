"""B01: throughput of the REAL core.models.audit() (not a copy) on a scratch database.

Runs the project code unchanged through Django against bench_django (made by `manage.py migrate` with
POSTGRES_DB=bench_django). Variants:
  plain   one audit() per transaction (autocommit caller)
  hold=H  audit() followed by H ms of other work in the SAME transaction (pg_sleep), the shape of intake.bulk.publish
          where create_entry (audit inside) is followed by settle_duplicate and the commit
Writers: 1 process, 8 processes (4 vCPU machine, so 8 writers also compete for CPU).

Run: PYTHONDONTWRITEBYTECODE=1 DJANGO_ALLOW_TEST_KEY=1 POSTGRES_DB=bench_django \
     .venv/bin/python "research_notes/Scale research/benchmarks/b01_audit_real.py"
"""

import multiprocessing as mp
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
BACKEND = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend"))


def worker(idx, duration, hold_ms, q, start_at):
    sys.path.insert(0, BACKEND)
    os.chdir(BACKEND)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    import django

    django.setup()
    from django.db import connection, transaction

    from core.models import audit

    # warm the connection and the code path
    audit("bench.warm", object_type="bench", object_uid=f"w{idx}")
    while time.time() < start_at:
        time.sleep(0.001)
    lat, end = [], time.time() + duration
    i = 0
    while time.time() < end:
        t = time.perf_counter()
        with transaction.atomic():
            audit("bench.write", actor_role="system", object_type="entry", object_uid=f"{idx}-{i}", country_code="PK",
                  payload={"i": i})
            if hold_ms:
                with connection.cursor() as cur:
                    cur.execute("select pg_sleep(%s)", [hold_ms / 1000.0])
        lat.append(time.perf_counter() - t)
        i += 1
    q.put(lat)


def run(n_workers, duration, hold_ms):
    from common import connect, summary

    with connect("bench_django") as c:
        c.execute("ALTER TABLE core_auditlog DISABLE TRIGGER core_auditlog_append_only")
        c.execute("TRUNCATE core_auditlog RESTART IDENTITY")
        c.execute("ALTER TABLE core_auditlog ENABLE TRIGGER core_auditlog_append_only")
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    start_at = time.time() + 6  # let every worker finish django.setup()
    ps = [ctx.Process(target=worker, args=(i, duration, hold_ms, q, start_at)) for i in range(n_workers)]
    [p.start() for p in ps]
    lats = [q.get() for _ in ps]
    [p.join() for p in ps]
    flat = [x for l in lats for x in l]
    with connect("bench_django") as c:
        rows = c.execute("select count(*) from core_auditlog").fetchone()[0]
    print(summary(f"audit() writers={n_workers} hold={hold_ms}ms", flat, duration), f"rows={rows}", flush=True)


if __name__ == "__main__":
    duration = float(sys.argv[1]) if len(sys.argv) > 1 else 15
    for workers, hold in [(1, 0), (8, 0), (1, 5), (8, 5), (1, 20), (8, 20)]:
        run(workers, duration, hold)
