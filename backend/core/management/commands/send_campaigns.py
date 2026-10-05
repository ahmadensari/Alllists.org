"""Send what is due for every approved, funded campaign (run from cron). Uses the sandbox provider for now."""

from django.core.management.base import BaseCommand

from outreach import campaigns
from outreach.models import Campaign
from outreach.providers import get_provider


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--provider", default="sandbox")

    def handle(self, *args, **o):
        provider = get_provider(o["provider"])
        for c in Campaign.objects.filter(status__in=["approved", "sending"], funded=True):
            self.stdout.write(f"campaign {c.pk}: {campaigns.send_batch(c, provider)}")
