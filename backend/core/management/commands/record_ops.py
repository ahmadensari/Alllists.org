"""Record an operational fact from a script: `record_ops backup "nightly dump 2.4 GB"` or `record_ops restore_drill ...`.
The monitor alerts when these go stale (plan 18.4)."""

from django.core.management.base import BaseCommand

from core.models import OpsRecord


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("kind", choices=["backup", "restore_drill"])
        parser.add_argument("detail", nargs="?", default="")

    def handle(self, *args, **o):
        OpsRecord.objects.create(kind=o["kind"], detail=o["detail"][:300])
        self.stdout.write(f"recorded {o['kind']}")
