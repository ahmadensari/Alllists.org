"""B08b: the real Django project through PgBouncer (transaction mode): audit() under concurrency, verify_audit_chain(),
and QuerySet.iterator() with and without DISABLE_SERVER_SIDE_CURSORS.

Start PgBouncer first (b08 helper start_pgb, or by hand) so that database `bench_django_pool` -> main server bench_django,
port 6432. Run:
  PYTHONDONTWRITEBYTECODE=1 DJANGO_ALLOW_TEST_KEY=1 POSTGRES_DB=bench_django_pool POSTGRES_HOST=127.0.0.1 POSTGRES_PORT=6432 \
  POSTGRES_USER=alllists POSTGRES_PASSWORD=alllists PGBOUNCER_DIR=<dir> .venv/bin/python b08b_django_via_pgbouncer.py
"""

import multiprocessing as mp
import os
import sys
import time

BACKEND = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend"))
sys.path.insert(0, os.path.dirname(__file__))


def setup_django():
    sys.path.insert(0, BACKEND)
    os.chdir(BACKEND)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    import django

    django.setup()


def worker(idx, duration, q):
    setup_django()
    from core.models import audit

    n, end = 0, time.time() + duration
    while time.time() < end:
        audit("bench.pooled", actor_role="system", object_type="entry", object_uid=f"{idx}-{n}", country_code="PK", payload={"i": n})
        n += 1
    q.put(n)


def main():
    from b08_pgbouncer import start_pgb, stop_pgb

    p, d = start_pgb(max_prepared=100, pool_size=4)
    try:
        import psycopg

        c = psycopg.connect(host="127.0.0.1", port=5432, user="alllists", password="alllists", dbname="bench_django", autocommit=True)
        c.execute("ALTER TABLE core_auditlog DISABLE TRIGGER core_auditlog_append_only")
        c.execute("TRUNCATE core_auditlog RESTART IDENTITY")
        c.execute("ALTER TABLE core_auditlog ENABLE TRIGGER core_auditlog_append_only")
        ctx = mp.get_context("spawn")
        q = ctx.Queue()
        ps = [ctx.Process(target=worker, args=(i, 8, q)) for i in range(6)]
        [x.start() for x in ps]
        counts = [q.get() for _ in ps]
        [x.join() for x in ps]
        print(f"real audit() through PgBouncer (pool of 4 server connections), 6 client processes, 8 s: {sum(counts)} writes = {sum(counts) / 8:.0f}/s")
        setup_django()
        from django.db import connection

        from core.models import AuditLog, verify_audit_chain

        print("rows:", AuditLog.objects.count(), " verify_audit_chain() ->", verify_audit_chain(), "(None means intact: advisory xact lock held correctly through the pooler)")
        # server side cursors
        from entries.models import Entry

        for disable in (False, True):
            connection.settings_dict["DISABLE_SERVER_SIDE_CURSORS"] = disable
            connection.close()
            try:
                n = 0
                for e in Entry.objects.only("id").iterator(chunk_size=2000):
                    n += 1
                    if n % 2000 == 0:
                        # other activity on the same pooled connection, as a real request mix would do
                        Entry.objects.filter(pk=e.pk).exists()
                    if n >= 60000:
                        break
                print(f"QuerySet.iterator() with DISABLE_SERVER_SIDE_CURSORS={disable}: iterated {n} rows without error")
            except Exception as ex:  # noqa: BLE001
                print(f"QuerySet.iterator() with DISABLE_SERVER_SIDE_CURSORS={disable}: {type(ex).__name__}: {str(ex).splitlines()[0]}")
    finally:
        stop_pgb(p)


if __name__ == "__main__":
    main()
