"""Load open data from local files: `load_data geonames|overture-divisions|taxonomy|places ...` (plan P1.06, P1.07, P1.19).
Nothing is downloaded. Every load is repeatable and writes an audit row."""

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from intake import loaders
from intake.gate import SourceBlocked
from intake.models import Source
from places import loaders as place_loaders
from taxonomy import loaders as tax_loaders


def _read(path):
    p = Path(path)
    if not p.is_file():
        raise CommandError(f"file not found: {path}")
    return p.read_text(encoding="utf-8")


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument("what", choices=["geonames", "overture-divisions", "taxonomy", "places"])
        parser.add_argument("--country", help="two-letter country code")
        parser.add_argument("--country-info")
        parser.add_argument("--admin1")
        parser.add_argument("--places", help="GeoNames place dump, or the places file for the places loader")
        parser.add_argument("--alternate-names", default="")
        parser.add_argument("--min-population", type=int, default=15000)
        parser.add_argument("--file", help="input file for overture-divisions, taxonomy and places")
        parser.add_argument(
            "--scheme", choices=["overture", "foursquare", "isco", "own"], help="taxonomy or places format"
        )
        parser.add_argument("--source", help="name of a registered source (places)")
        parser.add_argument("--limit", type=int)

    def handle(self, *args, **o):
        what = o["what"]
        if what == "geonames":
            if not (o["country_info"] and o["admin1"] and o["places"]):
                raise CommandError("--country-info, --admin1 and --places are required")
            out = place_loaders.load_geonames(
                country_info=_read(o["country_info"]),
                admin1=_read(o["admin1"]),
                places=_read(o["places"]),
                alternate_names=_read(o["alternate_names"]) if o["alternate_names"] else "",
                country=o["country"],
                min_population=o["min_population"],
            )
        elif what == "overture-divisions":
            out = place_loaders.load_overture_divisions(_read(o["file"]).splitlines(), country=o["country"])
        elif what == "taxonomy":
            fn = {
                "overture": tax_loaders.load_overture_categories,
                "foursquare": tax_loaders.load_foursquare_categories,
                "isco": tax_loaders.load_isco,
                "own": tax_loaders.load_own_csv,
            }.get(o["scheme"])
            if fn is None:
                raise CommandError("--scheme is required")
            out = fn(_read(o["file"]))
        else:
            src = Source.objects.filter(name=o["source"]).first()
            if src is None or not o["country"] or not o["scheme"]:
                raise CommandError("--source (a registered source), --country and --scheme are required")
            text = _read(o["file"])
            records = {
                "overture": lambda: loaders.read_overture_places(text.splitlines()),
                "foursquare": lambda: loaders.read_foursquare_places(text),
                "own": lambda: loaders.read_generic_csv(text),
            }[o["scheme"]]()
            try:
                out = loaders.load_places(src, records, country=o["country"], limit=o["limit"])
            except SourceBlocked as exc:
                raise CommandError(f"the source gate refused this load: {exc}") from exc
        self.stdout.write(str(out))
