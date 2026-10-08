"""Run every scheduled job that is due. Intended for cron, for example every five minutes."""

from django.core.management.base import BaseCommand

from core.jobs import run_due


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--only", nargs="*", default=None)

    def handle(self, *args, **opts):
        for name, result in run_due(only=opts["only"]).items():
            self.stdout.write(f"{name}: {result}")
