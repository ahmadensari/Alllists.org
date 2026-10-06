"""Seed the full list-type set and the twelve add-on families. Safe to run twice."""

from django.core.management.base import BaseCommand

from taxonomy.seeds import seed_extended_list_types, seed_list_types


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--extended", action="store_true", help="also load the merged research set (about 235 types)")

    def handle(self, *args, **opts):
        n = seed_list_types()
        self.stdout.write(f"{n} list types created")
        if opts["extended"]:
            made, skipped, collisions = seed_extended_list_types()
            self.stdout.write(f"{made} extended list types created, {skipped} already present")
            if collisions:
                self.stdout.write(f"skipped, address collides with a place or system name: {', '.join(collisions)}")
