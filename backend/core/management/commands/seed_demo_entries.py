"""Development only: fictional published entries so pages can be looked at. Refuses to run unless DEBUG is on."""

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from analytics.rollups import recount_all
from entries import services as es
from entries.models import Entry, Service, Social
from intake.models import Source
from places.models import Place
from taxonomy.models import Concept

DEMO = [
    (
        "Demo Crescent Surgical Works",
        "ڈیمو کریسنٹ سرجیکل ورکس",
        "paris-road",
        "surveyor",
        ["scissors", "forceps", "needle holders", "retractors"],
        "company",
    ),
    ("Demo Falcon Medical Instruments", "", "kashmir-road", "owner", ["dental", "forceps"], "company"),
    ("Demo Royal Steel Instruments", "", "paris-road", "ai", ["scissors"], "basic"),
    ("Demo Sialkot Precision Tools", "", "wazirabad-road", "surveyor", ["needle holders", "clamps"], "basic"),
    ("Demo Unity Surgical Co", "", "kashmir-road", "surveyor", ["retractors", "speculums"], "basic"),
    ("Demo Pioneer Instruments", "", "paris-road", "owner", ["forceps"], "basic"),
]


class Command(BaseCommand):
    def handle(self, *args, **opts):
        if not settings.DEBUG:
            raise CommandError("demo entries are for development only (set DJANGO_DEBUG=1)")
        call_command("seed_pilot")
        adder, _ = User.objects.get_or_create(username="demo_adder")
        surveyor, _ = User.objects.get_or_create(username="demo_surveyor")
        owner, _ = User.objects.get_or_create(username="demo_owner")
        web = Source.objects.get(name="Open web page check")
        concept = Concept.objects.get(slug="surgical-instrument-makers")
        for i, (name, alt, area, level, specs, plan) in enumerate(DEMO):
            if Entry.objects.filter(name=name).exists():
                continue
            place = Place.objects.get(slug=area)
            e = es.create_entry(
                name=name,
                place=place,
                primary_concept=concept,
                created_by=adder,
                listing_plan=plan,
                website=f"https://example.org/demo-{i}",
                address_text=f"Plot {10 + i}, {place.slug}, Sialkot",
                contacts=[("phone", f"0300 555 00{i:02d}")],
                name_variants=[(alt, "ur", "trade")] if alt else [],
                year_established=1980 + i,
                addons={
                    "business_type": "manufacturer",
                    "product_categories": specs,
                    "oem": i % 2 == 0,
                    "moq": "100 pieces",
                },
            )
            Social.objects.create(
                entry=e, country_code="PK", platform="facebook", handle_or_url="https://facebook.com/example"
            )
            Service.objects.create(entry=e, country_code="PK", name_text="OEM and private label")
            if level == "ai":
                es.record_verification(
                    e, field_group="identity", level="ai", source=web, evidence="Page lists same address", method="web"
                )
            elif level == "owner":
                claim = es.start_claim(e, owner, "otp_phone", "OTP matched")
                es.decide_claim(claim, actor=surveyor, approve=True)
                owner = User.objects.get(username="demo_owner")
            else:
                es.record_verification(
                    e, field_group="identity", level="surveyor", actor=surveyor, method="call", evidence="Answered"
                )
        recount_all()
        self.stdout.write(f"{Entry.objects.filter(publish_state='published').count()} published demo entries")
