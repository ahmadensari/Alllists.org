"""Seed the pilot structure: Pakistan to Sialkot, the surgical-instrument list type, and a starter source register.
Safe to run twice. Entries are not created here; they come from imports and verification."""

import datetime

from django.core.management.base import BaseCommand

from core.models import CountrySwitch
from intake.models import Source
from places.models import Place
from places.services import create_place
from taxonomy.models import Concept
from taxonomy.services import create_concept, seed_manufacturer_template

CENTRES = {
    "sialkot": (32.4945, 74.5229),
    "paris-road": (32.4990, 74.5300),
    "kashmir-road": (32.5040, 74.5150),
    "wazirabad-road": (32.5200, 74.5400),
}


def get_or_create_place(parent, **kw):
    slug = kw.get("slug") or kw["name"].lower().replace(" ", "-")
    place = Place.objects.filter(parent=parent, slug=slug).first() or create_place(parent=parent, **kw)
    if slug in CENTRES and place.centre_lat is None:
        place.centre_lat, place.centre_lon = CENTRES[slug]
        place.save(update_fields=["centre_lat", "centre_lon"])
    return place


class Command(BaseCommand):
    def handle(self, *args, **opts):
        world = Place.objects.filter(level="world").first() or create_place(
            parent=None, level=Place.Level.WORLD, name="World", slug="world"
        )
        pk = Place.objects.filter(country_code="PK", level="country").first() or create_place(
            parent=world, level=Place.Level.COUNTRY, name="Pakistan", country_code="PK", names=[("ur", "پاکستان")]
        )
        punjab = get_or_create_place(pk, level=Place.Level.ADMIN1, name="Punjab", names=[("ur", "پنجاب")])
        city = get_or_create_place(punjab, level=Place.Level.CITY, name="Sialkot", names=[("ur", "سیالکوٹ")])
        for area, ur in (("Paris Road", "پیرس روڈ"), ("Kashmir Road", "کشمیر روڈ"), ("Wazirabad Road", "وزیرآباد روڈ")):
            get_or_create_place(city, level=Place.Level.AREA, name=area, names=[("ur", ur)])
        tpl = seed_manufacturer_template()
        if not Concept.objects.filter(kind="list_type", slug="surgical-instrument-makers").exists():
            create_concept(
                kind=Concept.Kind.LIST_TYPE,
                name="Surgical instrument makers",
                template=tpl,
                natural_scale="national",
                synonyms=[("surgical instruments manufacturers", "en"), ("جراحی آلات بنانے والے", "ur")],
            )
        Source.objects.get_or_create(
            name="Owner and contributor submissions",
            defaults=dict(
                tier="green", allowed_uses=["import", "display"], attribution_text="Provided by contributors"
            ),
        )
        Source.objects.get_or_create(
            name="Open web page check",
            defaults=dict(
                tier="amber",
                allowed_uses=["agent_fetch", "display"],
                reviewed_on=datetime.date.today(),
                personal_data_rules="Business facts only; no personal data",
            ),
        )
        CountrySwitch.objects.get_or_create(country_code="PK")  # everything off except browsing until counsel clears it
        self.stdout.write("pilot structure ready")
