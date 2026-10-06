"""Create every list type at every place in one command (decision E27). Safe to re-run: existing lists are skipped."""

from django.core.management.base import BaseCommand
from django.db import connection

from places.models import Place
from taxonomy.models import PlaceList

LEVELS = [lv for lv, _ in Place.Level.choices]


class Command(BaseCommand):
    help = "Create a stored list for every active list type at every active place (optionally limited by level or country)."

    def add_arguments(self, parser):
        parser.add_argument("--levels", default="", help="comma list, e.g. world,country,admin1,city; default all")
        parser.add_argument("--country", default="", help="two-letter code, e.g. US")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **opts):
        levels = [x for x in opts["levels"].split(",") if x]
        bad = [x for x in levels if x not in LEVELS]
        if bad:
            self.stderr.write(f"unknown levels: {', '.join(bad)}")
            return
        where, params = ["p.status = 'active'", "c.kind = 'list_type'", "c.status = 'active'"], []
        if levels:
            where.append("p.level = ANY(%s)")
            params.append(levels)
        if opts["country"]:
            where.append("(p.country_code = %s OR p.level = 'world')")
            params.append(opts["country"].upper())
        clause = " AND ".join(where)
        with connection.cursor() as cur:
            cur.execute(
                f"SELECT count(*) FROM places_place p CROSS JOIN taxonomy_concept c WHERE {clause}", params
            )
            wanted = cur.fetchone()[0]
        have = PlaceList.objects.count()
        self.stdout.write(f"{wanted} lists wanted, {have} already stored")
        if opts["dry_run"]:
            return
        before = have
        with connection.cursor() as cur:
            cur.execute(
                f"INSERT INTO taxonomy_placelist (place_id, concept_id, created_at) "
                f"SELECT p.id, c.id, now() FROM places_place p CROSS JOIN taxonomy_concept c WHERE {clause} "
                f"ON CONFLICT (place_id, concept_id) DO NOTHING",
                params,
            )
        self.stdout.write(f"{PlaceList.objects.count() - before} lists created")
