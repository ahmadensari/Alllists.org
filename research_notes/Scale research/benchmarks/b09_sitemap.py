"""B09: sitemap generation. The REAL catalog.views.sitemap_index / sitemap_shard / indexable_list_cells on bench_django with
160,000 roll-up cells for one country, versus a precomputed table + file writer. Then the file writer at 5,000,000 URLs.

Setup done here (bench_django only): 8,000 extra PK city places, CountrySwitch(PK, indexing_on), 200,000 RollupCell rows
(8,000 places x 20 leaf concepts; about two thirds have >= 10 verified entries so they are indexable).

Run: PYTHONDONTWRITEBYTECODE=1 DJANGO_ALLOW_TEST_KEY=1 POSTGRES_DB=bench_django .venv/bin/python b09_sitemap.py [out_dir]
"""

import glob
import gzip
import os
import sys
import time

BACKEND = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend"))
sys.path.insert(0, BACKEND)
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(BACKEND)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django  # noqa: E402

django.setup()

from django.db import connection  # noqa: E402
from django.test import RequestFactory  # noqa: E402
from django.test.utils import CaptureQueriesContext  # noqa: E402

from catalog import views  # noqa: E402
from common import Timer, connect  # noqa: E402

SIZE = 50_000
HEAD = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'


def setup():
    c = connect("bench_django")
    c.execute("TRUNCATE analytics_rollupcell")
    c.execute("DELETE FROM places_place WHERE path LIKE 'pk.r%'")
    c.execute(
        """INSERT INTO places_place (id, uid, level, local_level_label, iso_code, country_code, slug, path, depth, population_band, status, wikidata_id, created_at, parent_id)
           SELECT 50000 + g, 'PX' || lpad(g::text, 24, '0'), 'city', '', '', 'PK', 'c' || g, 'pk.r' || (g % 80) || '.c' || g, 3, '', 'active', '', now(),
                  (SELECT id FROM places_place WHERE path = 'pk')
             FROM generate_series(1, 8000) g""")
    c.execute("INSERT INTO core_countryswitch (country_code, browsing_on, indexing_on, selling_on, outreach_on, outreach_channels, ads_on, named_individuals_on, health_prices_on, child_services_on, publish_cap_per_week, legal_note, cleared_by) "
              "VALUES ('PK', true, true, false, false, '[]', false, false, false, false, 0, '', '') ON CONFLICT (country_code) DO UPDATE SET indexing_on = true")
    c.execute(
        """INSERT INTO analytics_rollupcell (country_code, place_path, concept_id, total, published, by_level, verified_12m, with_contact_pct, updated_at)
           SELECT 'PK', p.path, k.id, 20, 15,
                  jsonb_build_object('surveyor', (p.id + k.id) % 9 + 2, 'owner', (p.id * 3 + k.id) % 7 + 2, 'ai', 5, 'none', 3), 4, 50, now() - ((p.id + k.id) % 30 || ' days')::interval
             FROM places_place p CROSS JOIN taxonomy_concept k
            WHERE p.path LIKE 'pk.r%' AND k.kind = 'list_type' AND k.id >= 1100""")
    c.execute("ANALYZE analytics_rollupcell")
    n = c.execute("SELECT count(*) FROM analytics_rollupcell").fetchone()[0]
    print(f"setup: {n:,} roll-up cells for PK", flush=True)
    return c


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/bench_sitemap_out"
    os.makedirs(out, exist_ok=True)
    c = setup()
    rf = RequestFactory()
    print("== real code, on request ==")
    with CaptureQueriesContext(connection) as q:
        with Timer() as t:
            cells = views.indexable_list_cells("PK")
    print(f"indexable_list_cells('PK'): {t.s:.1f}s, {len(q):,} queries, {len(cells):,} indexable cells")
    with CaptureQueriesContext(connection) as q:
        with Timer() as t:
            r = views.sitemap_shard(rf.get("/sitemaps/pk-1.xml"), "pk", 1)
    print(f"sitemap_shard pk-1 (one crawler request): {t.s:.1f}s, {len(q):,} queries, {len(r.content) / 1e6:.1f} MB")
    with Timer() as t:
        views.sitemap_index(rf.get("/sitemap.xml"))
    print(f"sitemap_index: {t.s:.1f}s")
    shards = -(-len(cells) // SIZE)
    print(f"a crawler fetching the index and all {shards} shards triggers about {(shards + 1)} full scans = {t.s * (shards + 1):.0f}s of database time (index {t.s:.1f}s each)")

    print("== precomputed table ==")
    c.execute("DROP TABLE IF EXISTS sitemap_url")
    c.execute("""CREATE TABLE sitemap_url (id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, country_code varchar(2) NOT NULL, loc text NOT NULL,
                 lastmod date NOT NULL, shard int NOT NULL DEFAULT 0, changed_at timestamptz NOT NULL DEFAULT now(), UNIQUE (country_code, loc))""")
    with Timer() as t:
        c.execute(
            """INSERT INTO sitemap_url (country_code, loc, lastmod)
               SELECT rc.country_code, 'https://alllists.com/' || replace(rc.place_path, '.', '/') || '/' || k.slug || '/', rc.updated_at::date
                 FROM analytics_rollupcell rc
                 JOIN taxonomy_concept k ON k.id = rc.concept_id AND k.kind = 'list_type'
                 LEFT JOIN taxonomy_listtypesettings s ON s.concept_id = k.id
                WHERE rc.place_path > '' AND (rc.by_level->>'surveyor')::int + (rc.by_level->>'owner')::int >= COALESCE(s.index_threshold, 10)
                ORDER BY rc.place_path, rc.concept_id""")
        c.execute("UPDATE sitemap_url SET shard = (id - 1) / %s", (SIZE,))
    n = c.execute("SELECT count(*) FROM sitemap_url").fetchone()[0]
    print(f"one SQL statement builds sitemap_url: {t.s:.1f}s for {n:,} URLs (same count as real code: {n == len(cells)})")

    def write_shard(cur_conn, cc, shard, path):
        with gzip.open(path, "wt", compresslevel=6) as f:
            f.write(HEAD)
            cur = cur_conn.cursor(name=f"s{shard}")
            cur.itersize = 10000
            with cur_conn.transaction():
                cur.execute("SELECT loc, lastmod FROM sitemap_url WHERE country_code = %s AND shard = %s ORDER BY id", (cc, shard))
                for loc, lm in cur:
                    f.write(f"<url><loc>{loc}</loc><lastmod>{lm.isoformat()}</lastmod></url>\n")
            f.write("</urlset>\n")

    with Timer() as t:
        for s in range(shards):
            write_shard(c, "PK", s, f"{out}/pk-{s + 1}.xml.gz")
    print(f"write {shards} gzip shard files for {n:,} URLs: {t.s:.1f}s; total size {sum(os.path.getsize(p) for p in glob.glob(out + '/pk-*.xml.gz')) / 1e6:.1f} MB")

    print("== 5,000,000 URLs ==")
    c.execute("TRUNCATE sitemap_url RESTART IDENTITY")
    with Timer() as t:
        c.execute(
            """INSERT INTO sitemap_url (country_code, loc, lastmod, shard)
               SELECT (ARRAY['PK','IN','BD','LK','NP'])[1 + g % 5], 'https://alllists.com/' || 'x' || (g % 80) || '/y' || g || '/leaf-' || (g % 25) || '/', current_date - (g % 300), (g - 1) / %s
                 FROM generate_series(1, 5000000) g""", (SIZE,))
    print(f"table filled: {t.s:.0f}s")
    c.execute("CREATE INDEX sitemap_url_shard ON sitemap_url (shard, id)")
    c.execute("ANALYZE sitemap_url")
    nshard = c.execute("SELECT max(shard) + 1 FROM sitemap_url").fetchone()[0]
    big = os.path.join(out, "big")
    os.makedirs(big, exist_ok=True)

    def write_shard_all(cur_conn, shard, path):
        with gzip.open(path, "wt", compresslevel=6) as f:
            f.write(HEAD)
            cur = cur_conn.cursor(name=f"b{shard}")
            cur.itersize = 10000
            with cur_conn.transaction():
                cur.execute("SELECT loc, lastmod FROM sitemap_url WHERE shard = %s ORDER BY id", (shard,))
                for loc, lm in cur:
                    f.write(f"<url><loc>{loc}</loc><lastmod>{lm.isoformat()}</lastmod></url>\n")
            f.write("</urlset>\n")

    with Timer() as t:
        for s in range(nshard):
            write_shard_all(c, s, f"{big}/s-{s + 1}.xml.gz")
    size = sum(os.path.getsize(p) for p in glob.glob(big + "/*.gz"))
    print(f"full rebuild: {nshard} shard files, 5,000,000 URLs: {t.s:.0f}s ({5_000_000 / t.s:,.0f} URLs/s), {size / 1e6:.0f} MB gzip, single process")

    # SQL-side XML (string_agg) for one shard
    with Timer() as t:
        xml = c.execute("SELECT string_agg('<url><loc>' || loc || '</loc><lastmod>' || lastmod || '</lastmod></url>', E'\\n' ORDER BY id) FROM sitemap_url WHERE shard = 7").fetchone()[0]
    print(f"one shard built entirely in SQL (string_agg): {t.s * 1000:.0f} ms ({len(xml) / 1e6:.1f} MB raw)")

    # the usual case: new URLs append to the last shard
    c.execute("UPDATE sitemap_url SET changed_at = now() - interval '1 day'")
    c.execute("INSERT INTO sitemap_url (country_code, loc, lastmod, shard) SELECT 'PK', 'https://alllists.com/new/' || g, current_date, (SELECT max(id) FROM sitemap_url) / %s FROM generate_series(1, 2000) g", (SIZE,))
    dirty = [r[0] for r in c.execute("SELECT DISTINCT shard FROM sitemap_url WHERE changed_at > now() - interval '5 minutes' ORDER BY 1").fetchall()]
    with Timer() as t:
        for s in dirty:
            write_shard_all(c, s, f"{big}/s-{s + 1}.xml.gz")
    print(f"2,000 new URLs appended -> {len(dirty)} shard file rewritten ({t.s:.1f}s) instead of {nshard}; stable shard = (identity id - 1) / 50000")
    c.close()


if __name__ == "__main__":
    main()
