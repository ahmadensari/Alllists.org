import json


from places.loaders import load_geonames, load_overture_divisions
from places.models import Place

COUNTRY_INFO = "#ISO\tISO3\tISON\tfips\tCountry\tCapital\tArea\tPop\n" + "\t".join(
    [
        "PK",
        "PAK",
        "586",
        "PK",
        "Pakistan",
        "Islamabad",
        "796095",
        "240000000",
        "AS",
        ".pk",
        "PKR",
        "Rupee",
        "92",
        "",
        "",
        "ur,en-PK",
        "1168579",
    ]
)
ADMIN1 = "PK.04\tPunjab\tPunjab\t1168883\n"


def _city(gid, name, adm1, pop, lat="32.5", lon="74.5", fclass="P"):
    cols = [
        gid,
        name,
        name,
        "",
        lat,
        lon,
        fclass,
        "PPL",
        "PK",
        "",
        adm1,
        "",
        "",
        "",
        str(pop),
        "",
        "",
        "Asia/Karachi",
        "",
    ]
    return "\t".join(cols)


PLACES = "\n".join(
    [
        _city("1176639", "Sialkot", "04", 655852),
        _city("1167528", "Lahore", "04", 5143495),
        _city("999", "Hamlet", "04", 300),
        _city("1000", "A Hill", "04", 900000, fclass="T"),
    ]
)
ALT = "1\t1176639\tur\tسیالکوٹ\t1\n2\t1176639\ten\tSialkot\t\n3\t1168579\tur\tپاکستان\t\n"


def test_geonames_loads_country_regions_cities_with_urdu_names_and_is_repeatable(db):
    first = load_geonames(country_info=COUNTRY_INFO, admin1=ADMIN1, places=PLACES, alternate_names=ALT, country="PK")
    assert first["countries"] == 1 and first["regions"] == 1 and first["cities"] == 2
    sialkot = Place.objects.get(path="pk.punjab.sialkot")
    assert sialkot.level == "city" and sialkot.depth == 3 and sialkot.name_for("ur") == "سیالکوٹ"
    assert Place.objects.get(path="pk").name_for("ur") == "پاکستان"
    assert not Place.objects.filter(slug__in=["hamlet", "a-hill"]).exists()  # too small, or not a populated place
    again = load_geonames(country_info=COUNTRY_INFO, admin1=ADMIN1, places=PLACES, alternate_names=ALT, country="PK")
    assert again["cities"] == 0 and again["countries"] == 0 and Place.objects.count() == 5


def test_geonames_name_collision_keeps_both_places(db):
    twin = PLACES + "\n" + _city("555", "Sialkot", "04", 90000)
    load_geonames(country_info=COUNTRY_INFO, admin1=ADMIN1, places=twin, country="PK")
    slugs = set(Place.objects.filter(level="city").values_list("slug", flat=True))
    assert "sialkot" in slugs and "sialkot-555" in slugs


def test_overture_divisions_any_order_with_parents_first_resolution(db):
    recs = [
        {
            "id": "loc1",
            "subtype": "locality",
            "country": "PK",
            "parent_division_id": "reg1",
            "names": {"primary": "Daska", "common": {"ur": "ڈسکہ"}},
        },
        {
            "id": "reg1",
            "subtype": "region",
            "country": "PK",
            "parent_division_id": "ctry",
            "names": {"primary": "Punjab"},
        },
        {"id": "ctry", "subtype": "country", "country": "PK", "names": {"primary": "Pakistan"}},
        {
            "id": "orph",
            "subtype": "locality",
            "country": "PK",
            "parent_division_id": "missing",
            "names": {"primary": "Lost"},
        },
        {"id": "x", "subtype": "planet", "country": "PK", "names": {"primary": "Mars"}},
    ]
    counts = load_overture_divisions([json.dumps(r) for r in recs], country="PK")
    assert counts["created"] == 3 and counts["skipped_no_parent"] == 1
    daska = Place.objects.get(path="pk.punjab.daska")
    assert daska.name_for("ur") == "ڈسکہ"
    assert load_overture_divisions([json.dumps(r) for r in recs], country="PK")["created"] == 0
