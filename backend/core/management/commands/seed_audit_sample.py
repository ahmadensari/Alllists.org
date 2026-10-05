"""Queue the 385-record audit sample, and optionally plant canaries."""

from django.core.management.base import BaseCommand, CommandError

from places.models import Place
from taxonomy.models import Concept
from volunteers import services as vs


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--size", type=int, default=vs.AUDIT_SAMPLE_SIZE)
        parser.add_argument("--canaries", type=int, default=0)
        parser.add_argument("--place", default="")
        parser.add_argument("--type", default="")

    def handle(self, *args, **o):
        self.stdout.write(f"{vs.queue_audit_sample(o['size'])} audit tasks queued")
        if o["canaries"]:
            place = Place.objects.filter(path=o["place"]).first()
            concept = Concept.objects.filter(kind="list_type", slug=o["type"]).first()
            if not (place and concept):
                raise CommandError("--place and --type are needed to plant canaries")
            self.stdout.write(f"{len(vs.plant_canaries(place, concept, o['canaries']))} canaries planted")
