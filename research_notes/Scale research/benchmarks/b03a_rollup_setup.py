"""B03a: load a synthetic catalogue into bench_django (the real Django schema, made by `manage.py migrate`).

Shape: 1 root list type, 4 mid concepts, 20 leaf concepts; 10 countries. PK has exactly 100,000 entries (the "cell of 100k"),
the other 9 countries 100,000 each, so the table holds 1,000,000 entries. Places: 4 provinces x 5 cities per country.
Per entry: 70% published, 20% draft, 10% review; 1% soft-deleted; 30% verified in the last 12 months; 35% have a
verification row (surveyor / owner / ai; 80% unexpired); 50% have a contact row.

Run: .venv/bin/python "research_notes/Scale research/benchmarks/b03a_rollup_setup.py" [entries_per_country]
"""

import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import Timer, connect  # noqa: E402

DB = "bench_django"
COUNTRIES = ["PK", "IN", "BD", "LK", "NP", "AE", "SA", "TR", "EG", "NG"]


def main():
    per = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000
    c = connect(DB)
    with Timer() as t0:
        c.execute(
            "TRUNCATE entries_contact, entries_verificationcurrent, entries_entry, analytics_rollupcell, "
            "taxonomy_listtypesettings, taxonomy_placelist, places_place, taxonomy_concept RESTART IDENTITY CASCADE"
        )
        # concepts: 1 root, 4 mid, 20 leaves
        c.execute(
            "INSERT INTO taxonomy_concept (id, uid, kind, slug, entity_type_default, natural_scale, status, created_at, parent_id) "
            "VALUES (1000, 'C000000000000000000000ROOT', 'list_type', 'manufacturing', 'business', 'global', 'active', now(), NULL)"
        )
        c.execute(
            "INSERT INTO taxonomy_concept (id, uid, kind, slug, entity_type_default, natural_scale, status, created_at, parent_id) "
            "SELECT 1000 + m, 'C0000000000000000000MID' || lpad(m::text, 3, '0'), 'list_type', 'mid-' || m, 'business', 'country', 'active', now(), 1000 "
            "FROM generate_series(1, 4) m"
        )
        c.execute(
            "INSERT INTO taxonomy_concept (id, uid, kind, slug, entity_type_default, natural_scale, status, created_at, parent_id) "
            "SELECT 1100 + l, 'C000000000000000000LEAF' || lpad(l::text, 3, '0'), 'list_type', 'leaf-' || l, 'business', 'city', 'active', now(), 1000 + 1 + ((l - 1) / 5) "
            "FROM generate_series(1, 20) l"
        )
        c.execute("INSERT INTO taxonomy_listtypesettings (concept_id, index_threshold, row_descriptor_field, actions_allowed, share_hidden, is_individual, is_child_facing, is_health, price_required_date) "
                  "SELECT id, 10, '', '[]', false, false, false, false, true FROM taxonomy_concept")
        # places: world, 10 countries, 4 provinces, 5 cities each
        c.execute("INSERT INTO places_place (id, uid, level, local_level_label, iso_code, country_code, slug, path, depth, population_band, status, wikidata_id, created_at) "
                  "VALUES (1, 'P000000000000000000000WORLD', 'world', '', '', '', 'world', '', 0, '', 'active', '', now())")
        for ci, cc in enumerate(COUNTRIES):
            slug = cc.lower()
            base = 100 + ci * 100
            c.execute("INSERT INTO places_place (id, uid, level, local_level_label, iso_code, country_code, slug, path, depth, population_band, status, wikidata_id, created_at, parent_id) "
                      "VALUES (%s, %s, 'country', '', %s, %s, %s, %s, 1, '', 'active', '', now(), 1)",
                      (base, f"P{ci:02d}" + "0" * 20 + "CTRY", cc, cc, slug, slug))
            for p in range(1, 5):
                c.execute("INSERT INTO places_place (id, uid, level, local_level_label, iso_code, country_code, slug, path, depth, population_band, status, wikidata_id, created_at, parent_id) "
                          "VALUES (%s, %s, 'region', '', '', %s, %s, %s, 2, '', 'active', '', now(), %s)",
                          (base + p * 10, f"P{ci:02d}R{p}" + "0" * 18 + "REG", cc, f"p{p}", f"{slug}.p{p}", base))
                for k in range(1, 6):
                    c.execute("INSERT INTO places_place (id, uid, level, local_level_label, iso_code, country_code, slug, path, depth, population_band, status, wikidata_id, created_at, parent_id) "
                              "VALUES (%s, %s, 'city', '', '', %s, %s, %s, 3, '', 'active', '', now(), %s)",
                              (base + p * 10 + k, f"P{ci:02d}R{p}C{k}" + "0" * 16 + "CIT", cc, f"c{k}", f"{slug}.p{p}.c{k}", base + p * 10))
    print(f"concepts and places: {t0.s:.1f}s", flush=True)

    with Timer() as t:
        for ci, cc in enumerate(COUNTRIES):
            base = 100 + ci * 100
            c.execute(
                """
INSERT INTO entries_entry (uid, deleted_at, tombstone_reason, country_code, entity_type, name, name_lang, name_fold, description,
  status, publish_state, address, address_text, place_path, precision_class, coord_source, service_area, website, size_band,
  languages, price_band, payment_methods, addons, claim_state, listing_plan, visibility_flags, created_via, created_at, updated_at,
  last_verified_at, place_id, primary_concept_id)
SELECT 'E' || lpad(%(ci)s::text, 2, '0') || lpad(n::text, 23, '0'),
       CASE WHEN n % 100 = 0 THEN now() ELSE NULL END, '', %(cc)s, 'business',
       'Entry ' || %(cc)s || ' ' || n, 'en', 'entry ' || lower(%(cc)s) || ' ' || n, '',
       'open', CASE WHEN n % 10 < 7 THEN 'published' WHEN n % 10 < 9 THEN 'draft' ELSE 'review' END,
       '{}', '', lower(%(cc)s) || '.p' || (1 + n % 4) || '.c' || (1 + (n / 4) % 5), '', '', '{}', '', '',
       '[]', '', '[]', '{}', 'unclaimed', 'basic', '[]', 'import', now() - (n % 700 || ' days')::interval, now(),
       CASE WHEN n % 10 < 3 THEN now() - ((n % 300) || ' days')::interval ELSE NULL END,
       %(base)s + (1 + n % 4) * 10 + (1 + (n / 4) % 5),
       1100 + 1 + n % 20
FROM generate_series(1, %(per)s) n
""",
                {"ci": ci, "cc": cc, "base": base, "per": per},
            )
        print(f"entries inserted: {t.s:.1f}s", flush=True)
    with Timer() as t:
        c.execute(
            """
INSERT INTO entries_verificationcurrent (field_group, level, state, verified_at, expires_at, method, actor_display, entry_id)
SELECT 'basics', (ARRAY['surveyor','owner','ai'])[1 + id % 3], 'verified', now() - interval '30 days',
       CASE WHEN id % 5 = 0 THEN now() - interval '1 day' ELSE now() + ((id % 300) + 5 || ' days')::interval END, 'visit', '', id
FROM entries_entry WHERE id % 20 < 7""")
        c.execute(
            """
INSERT INTO entries_contact (country_code, kind, value_enc, value_hash, label, preferred_hours, relay_only, optin_state, entry_id)
SELECT country_code, 'phone', 'enc', md5(id::text), '', '', true, 'none', id FROM entries_entry WHERE id % 2 = 0""")
    print(f"verification + contacts: {t.s:.1f}s", flush=True)
    with Timer() as t:
        c.execute("ANALYZE")
    n = c.execute("SELECT count(*) FROM entries_entry").fetchone()[0]
    pk = c.execute("SELECT count(*) FROM entries_entry WHERE country_code='PK' AND deleted_at IS NULL").fetchone()[0]
    sizes = c.execute("SELECT pg_size_pretty(pg_total_relation_size('entries_entry')), pg_size_pretty(pg_total_relation_size('entries_verificationcurrent')), pg_size_pretty(pg_total_relation_size('entries_contact'))").fetchone()
    print(f"entries={n:,} PK live={pk:,} sizes entry/verif/contact = {sizes} analyze={t.s:.1f}s")


if __name__ == "__main__":
    main()
