"""B03b: the REAL analytics.rollups.recount_cell / refresh_for_entry versus a SQL aggregate, on bench_django
(loaded by b03a). Compares results field by field.

Run: PYTHONDONTWRITEBYTECODE=1 DJANGO_ALLOW_TEST_KEY=1 POSTGRES_DB=bench_django \
     .venv/bin/python "research_notes/Scale research/benchmarks/b03b_rollup_real.py" [real_refresh_for_entry: 0|1]
"""

import os
import sys
import time
from datetime import timedelta

BACKEND = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend"))
sys.path.insert(0, BACKEND)
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(BACKEND)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django  # noqa: E402

django.setup()

from django.db import connection  # noqa: E402
from django.test.utils import CaptureQueriesContext  # noqa: E402

from analytics.models import RollupCell  # noqa: E402
from analytics.rollups import concept_chain, descendant_concept_ids, place_paths, recount_cell, refresh_for_entry  # noqa: E402
from core import clock  # noqa: E402
from entries.models import Entry  # noqa: E402

SQL_CELL = """
WITH ents AS (
  SELECT e.id, e.publish_state, e.last_verified_at,
         (SELECT min(CASE v.level WHEN 'surveyor' THEN 1 WHEN 'owner' THEN 2 WHEN 'ai' THEN 3 END)
            FROM entries_verificationcurrent v
           WHERE v.entry_id = e.id AND v.state = 'verified' AND v.expires_at > %(now)s) AS lv,
         EXISTS (SELECT 1 FROM entries_contact c WHERE c.entry_id = e.id) AS has_contact
    FROM entries_entry e
   WHERE e.primary_concept_id = ANY(%(cids)s) AND e.deleted_at IS NULL AND e.merged_into_id IS NULL
     AND e.country_code = %(cc)s
     AND (%(path)s = '' OR e.place_path = %(path)s OR starts_with(e.place_path, %(path)s || '.'))
)
SELECT count(*) AS total,
       count(*) FILTER (WHERE publish_state = 'published') AS published,
       count(*) FILTER (WHERE publish_state = 'published' AND lv = 1) AS surveyor,
       count(*) FILTER (WHERE publish_state = 'published' AND lv = 2) AS owner,
       count(*) FILTER (WHERE publish_state = 'published' AND lv = 3) AS ai,
       count(*) FILTER (WHERE publish_state = 'published' AND lv IS NULL) AS none,
       count(*) FILTER (WHERE publish_state = 'published' AND last_verified_at > %(now)s - interval '365 days') AS v12,
       count(*) FILTER (WHERE publish_state = 'published' AND has_contact) AS with_contact
  FROM ents
"""


def sql_cell(country, path, concept_id, now):
    with connection.cursor() as cur:
        cur.execute(SQL_CELL, {"now": now, "cids": descendant_concept_ids(concept_id), "cc": country, "path": path})
        t, p, s, o, a, n, v12, wc = cur.fetchone()
    return {
        "total": t, "published": p, "by_level": {"surveyor": s, "owner": o, "ai": a, "none": n},
        "verified_12m": v12, "with_contact_pct": round(100 * wc / p) if p else 0,
    }


def same(cell, d):
    return (cell.total == d["total"] and cell.published == d["published"] and cell.by_level == d["by_level"]
            and cell.verified_12m == d["verified_12m"] and cell.with_contact_pct == d["with_contact_pct"])


def main():
    do_refresh = len(sys.argv) > 1 and sys.argv[1] == "1"
    now = clock.now()
    root = 1000
    print("-- recount_cell (real code) vs SQL aggregate: same cell, same instant --")
    for label, cc, path, cid in [
        ("1k entries  (PK, city pk.p1.c1, leaf)", "PK", "pk.p1.c1", 1101),
        ("5k entries  (PK, province pk.p1, mid)", "PK", "pk.p1", 1001),
        ("20k entries (PK, province, root)", "PK", "pk.p1", 1000),
        ("100k entries (PK, country, root)", "PK", "pk", 1000),
    ]:
        with CaptureQueriesContext(connection) as q:
            t = time.perf_counter()
            cell = recount_cell(cc, path, cid, now)
            real = time.perf_counter() - t
        nq = len(q)
        t = time.perf_counter()
        d = sql_cell(cc, path, cid, now)
        sql = time.perf_counter() - t
        t = time.perf_counter()
        for _ in range(3):
            sql_cell(cc, path, cid, now)
        sql3 = (time.perf_counter() - t) / 3
        print(f"{label}: total={cell.total} published={cell.published}  real={real:.2f}s ({nq:,} queries)  "
              f"sql={sql * 1000:.0f}ms (warm {sql3 * 1000:.0f}ms)  speedup={real / sql3:,.0f}x  identical={same(cell, d)}", flush=True)

    # one edit: refresh_for_entry touches (place ancestors x concept ancestors) cells
    e = Entry.objects.filter(country_code="PK", place_path="pk.p1.c1", primary_concept_id=1101, deleted_at__isnull=True).first()
    cells = len(place_paths(e.place_path)) * len(concept_chain(e.primary_concept))
    sizes = []
    for path in place_paths(e.place_path):
        for cid in concept_chain(e.primary_concept):
            sizes.append((path, cid, sql_cell("PK", path, cid, now)["total"]))
    print(f"one entry edit touches {cells} cells; entries scanned by the real code = {sum(s[2] for s in sizes):,}")
    t = time.perf_counter()
    for path, cid, _ in sizes:
        sql_cell("PK", path, cid, now)
    print(f"same {cells} cells with the SQL aggregate: {(time.perf_counter() - t) * 1000:.0f}ms")
    if do_refresh:
        with CaptureQueriesContext(connection) as q:
            t = time.perf_counter()
            refresh_for_entry(e, now)
            real = time.perf_counter() - t
        print(f"REAL refresh_for_entry for ONE edited entry: {real:.1f}s, {len(q):,} queries", flush=True)


if __name__ == "__main__":
    main()
