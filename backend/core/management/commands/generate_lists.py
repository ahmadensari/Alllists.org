"""Create every list type at every place in one command (decision E27). Safe to re-run: existing lists are skipped."""

from django.core.management.base import BaseCommand
from django.db import connection
from psycopg import sql

from places.models import Place
from taxonomy.models import PlaceList

LARGE = 5_000_000  # about 0.7 GB at 144 bytes a row; hosting note 03
LEVELS = [lv for lv, _ in Place.Level.choices]


class Command(BaseCommand):
    help = "Create a stored list for every active list type at every active place (optionally limited by level or country)."

    def add_arguments(self, parser):
        parser.add_argument("--levels", default="", help="comma list, e.g. world,country,admin1,city; default all")
        parser.add_argument("--country", default="", help="two-letter code, e.g. US")
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--confirm-large", action="store_true", help=f"required above {LARGE:,} lists")

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
        clause = sql.SQL(" AND ").join(sql.SQL(w) for w in where)
        with connection.cursor() as cur:
            cur.execute(
                sql.SQL("SELECT count(*) FROM places_place p CROSS JOIN taxonomy_concept c WHERE {}").format(clause),
                params,
            )
            wanted = cur.fetchone()[0]
        have = PlaceList.objects.count()
        self.stdout.write(f"{wanted} lists wanted, {have} already stored")
        if opts["dry_run"]:
            return
        if wanted - have > LARGE and not opts["confirm_large"]:
            self.stderr.write(f"{wanted - have:,} new lists is large; use --levels or --country, or add --confirm-large")
            return
        before = have
        with connection.cursor() as cur:
            cur.execute(
                sql.SQL(
                    "INSERT INTO taxonomy_placelist (place_id, concept_id, created_at) "
                    "SELECT p.id, c.id, now() FROM places_place p CROSS JOIN taxonomy_concept c WHERE {} "
                    "ON CONFLICT (place_id, concept_id) DO NOTHING"
                ).format(clause),
                params,
            )
        self.stdout.write(f"{PlaceList.objects.count() - before} lists created")
