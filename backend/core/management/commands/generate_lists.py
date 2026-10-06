"""Create the stored lists in one command. Default: only where entries exist (decision E28), so a list appears at a place
and at every place above it when an entry lives below it, and never at a place with no entries. `--all` creates every
list type at every place (small seeds only). Safe to re-run: existing lists are skipped."""

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
        parser.add_argument("--all", action="store_true", help="every list type at every place (small seeds only)")
        parser.add_argument("--prune", action="store_true", help="remove stored lists that no longer have entries")
        parser.add_argument("--levels", default="", help="comma list, e.g. world,country,admin1,city; default all")
        parser.add_argument("--country", default="", help="two-letter code, e.g. US")
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--confirm-large", action="store_true", help=f"required above {LARGE:,} lists")

    def handle(self, *args, **opts):
        if not opts["all"]:
            return self.from_entries(opts)
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

    def from_entries(self, opts):
        """Stored lists mirror the non-empty roll-up cells: an entry sits at one place (its address) and counts for that
        place and every place above it, and for its list type and every type above it."""
        from analytics.models import RollupCell
        from places.models import Place

        if opts["country"]:
            cells = RollupCell.objects.filter(country_code=opts["country"].upper())
        else:
            cells = RollupCell.objects.all()
        cells = cells.filter(total__gt=0, concept__kind="list_type", concept__status="active")
        if opts["levels"]:
            levels = [x for x in opts["levels"].split(",") if x]
            allowed = set(Place.objects.filter(level__in=levels).values_list("path", flat=True))
            cells = cells.filter(place_path__in=allowed)
        wanted = cells.count()
        self.stdout.write(f"{wanted} non-empty lists, {PlaceList.objects.count()} already stored")
        if opts["dry_run"]:
            return
        made = 0
        for path, concept_id in cells.values_list("place_path", "concept_id").iterator(chunk_size=5000):
            place_id = Place.objects.filter(path=path, status="active").values_list("pk", flat=True).first()
            if place_id and PlaceList.objects.get_or_create(place_id=place_id, concept_id=concept_id)[1]:
                made += 1
        self.stdout.write(f"{made} lists created")
        if opts["prune"]:
            live = {(p, c) for p, c in RollupCell.objects.filter(total__gt=0).values_list("place_path", "concept_id")}
            gone = [
                pl.pk
                for pl in PlaceList.objects.select_related("place")
                if (pl.place.path, pl.concept_id) not in live
            ]
            PlaceList.objects.filter(pk__in=gone).delete()
            self.stdout.write(f"{len(gone)} empty lists removed")
