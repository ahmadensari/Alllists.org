"""Load a small demo register (Sialkot surgical instruments and footballs). Safe to run twice."""
import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from lists.models import Check, Contact, Contribution, Entry, ListType, Place, Profile, Service, SocialLink

AREAS = [("Paris Road", "پیرس روڈ"), ("Kashmir Road", "کشمیر روڈ"), ("Wazirabad Road", "وزیرآباد روڈ")]
DEMO = [
    ("Crescent Surgical Works", "Manufacturer", 0, ["Scissors", "Forceps", "Needle holders", "Retractors"], "company", "surveyor"),
    ("Falcon Medical Instruments", "Manufacturer", 1, ["Dental", "Forceps"], "company", "owner"),
    ("Royal Steel Instruments", "Exporter", 0, ["Scissors"], "basic", "ai"),
    ("Sialkot Precision Tools", "Manufacturer", 2, ["Needle holders", "Clamps"], "basic", "owner"),
    ("Unity Surgical Co", "Trader", 1, ["Retractors", "Speculums"], "basic", "none"),
    ("Pioneer Instruments", "Manufacturer", 0, ["Forceps"], "basic", "surveyor"),
]


class Command(BaseCommand):
    def handle(self, *args, **opts):
        world, _ = Place.objects.get_or_create(kind="world", parent=None, defaults={"name": "World", "slug": "world"})
        pk, _ = Place.objects.get_or_create(parent=world, slug="pakistan", defaults={"kind": "country", "name": "Pakistan", "name_ur": "پاکستان", "country_code": "PK"})
        pb, _ = Place.objects.get_or_create(parent=pk, slug="punjab", defaults={"kind": "region", "name": "Punjab", "name_ur": "پنجاب", "country_code": "PK"})
        city, _ = Place.objects.get_or_create(parent=pb, slug="sialkot", defaults={"kind": "city", "name": "Sialkot", "name_ur": "سیالکوٹ", "country_code": "PK"})
        areas = [Place.objects.get_or_create(parent=city, slug=n.lower().replace(" ", "-"), defaults={"kind": "area", "name": n, "name_ur": u, "country_code": "PK"})[0] for n, u in AREAS]
        lt, _ = ListType.objects.get_or_create(slug="surgical-instrument-makers", defaults={"name": "Surgical instrument makers", "name_ur": "جراحی آلات بنانے والے", "group": "Manufacturing"})
        ListType.objects.get_or_create(slug="football-makers", defaults={"name": "Football makers", "name_ur": "فٹ بال بنانے والے", "group": "Manufacturing"})
        user, _ = User.objects.get_or_create(username="contributor1")
        Profile.objects.get_or_create(user=user, defaults={"contributor": True})
        today = datetime.date.today()
        for i, (name, kind, a, specs, plan, level) in enumerate(DEMO):
            e, created = Entry.objects.get_or_create(name=name, defaults={
                "place": areas[a], "entry_type": kind, "specialities": specs, "plan": plan,
                "address": f"Plot {10 + i}, {areas[a].name}, Sialkot", "website": f"https://example.org/{i}",
                "markets": "EU, USA", "moq": "100 pieces", "certificates": "ISO 13485",
                "company_profile": "Family firm making instruments since 1980." if plan == "company" else "",
                "sponsored": i == 0})
            if not created:
                continue
            e.list_types.add(lt)
            if level != "none":
                Check.objects.create(entry=e, level=level, checked_on=today - datetime.timedelta(days=i * 9))
            Contact.objects.create(entry=e, kind="phone", value="+92 300 0000000")
            SocialLink.objects.create(entry=e, channel="facebook", url="https://facebook.com/example")
            Service.objects.create(entry=e, text="OEM and private label")
            Contribution.lock(e, user)
        self.stdout.write("demo data ready")
