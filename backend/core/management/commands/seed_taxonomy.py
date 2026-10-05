"""Seed the full list-type set and the twelve add-on families. Safe to run twice."""

from django.core.management.base import BaseCommand

from taxonomy.seeds import seed_list_types


class Command(BaseCommand):
    def handle(self, *args, **opts):
        n = seed_list_types()
        self.stdout.write(f"{n} list types created")
