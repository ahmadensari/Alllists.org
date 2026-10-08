import json

import pytest

from entries.models import CreditEvent, Entry
from intake import loaders
from intake.gate import SourceBlocked
from intake.models import ExternalRecord, Source


@pytest.fixture
def open_source(db):
    return Source.objects.create(
        name="Overture places", tier="green", allowed_uses=["import", "display"], licence_text="CC BY 4.0"
    )


def _setup(tree, surgical):
    from places.models import Place
    from taxonomy.models import ConceptCrosswalk

    Place.objects.filter(pk=tree["sialkot"].pk).update(centre_lat="32.50", centre_lon="74.53")
    Place.objects.filter(pk=tree["paris"].pk).update(centre_lat="32.51", centre_lon="74.54")
    ConceptCrosswalk.objects.create(concept=surgical, system="overture", code="surgical_supply")


def _line(i, name="Crescent Works", lat=32.511, lon=74.541, cat="surgical_supply", phone="+92 52 1234567"):
    return json.dumps(
        {
            "id": f"ov{i}",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {
                "names": {"primary": name, "common": {"ur": "کریسنٹ ورکس"}},
                "categories": {"primary": cat},
                "phones": [phone],
                "websites": ["https://crescent.example"],
                "addresses": [{"freeform": "Paris Road", "locality": "Sialkot"}],
            },
        }
    )


def test_places_become_drafts_without_credit_and_unmapped_ones_are_skipped(tree, surgical, open_source):
    _setup(tree, surgical)
    lines = [
        _line(1),
        _line(2, name="Far Away", lat=40.0, lon=10.0),
        _line(3, name="Cafe", cat="cafe"),
        _line(4, name=""),
    ]
    counts = loaders.load_places(open_source, loaders.read_overture_places(lines), country="PK")
    assert counts["drafted"] == 1 and counts["no_place"] == 1 and counts["no_category"] == 1 and counts["no_name"] == 1
    e = Entry.objects.get()
    assert e.publish_state == "draft" and e.created_via == "import" and e.place_id == tree["paris"].pk  # deepest near
    assert not CreditEvent.objects.filter(entry=e, eligible=True).exists()
    assert e.namevariant_set.filter(language="ur").exists()


def test_rerun_skips_loaded_records_and_a_limit_stops_early(tree, surgical, open_source):
    _setup(tree, surgical)
    lines = [_line(i, name=f"Distinct Maker {i} Ltd", phone=f"+92300000000{i}") for i in range(1, 5)]
    first = loaders.load_places(open_source, loaders.read_overture_places(lines), country="PK", limit=2)
    assert Entry.objects.count() == 2 and ExternalRecord.objects.count() == 2
    loaders.load_places(open_source, loaders.read_overture_places(lines), country="PK")
    assert Entry.objects.count() == 4 and first["drafted"] == 2


def test_duplicate_goes_through_the_pipeline(tree, surgical, open_source):
    _setup(tree, surgical)
    lines = [_line(1), _line(2)]  # same name, phone and place
    counts = loaders.load_places(open_source, loaders.read_overture_places(lines), country="PK")
    assert counts["merged"] == 1 and Entry.objects.filter(merged_into__isnull=True).count() == 1


def test_gate_blocks_a_source_that_may_not_be_imported(tree, surgical, db):
    _setup(tree, surgical)
    red = Source.objects.create(name="Do not use", tier="red", allowed_uses=[])
    with pytest.raises(SourceBlocked):
        loaders.load_places(red, loaders.read_overture_places([_line(1)]), country="PK")
    assert Entry.objects.count() == 0 and ExternalRecord.objects.count() == 0


def test_foursquare_reader_and_generic_csv(tree, surgical, open_source):
    _setup(tree, surgical)
    from taxonomy.models import ConceptCrosswalk

    ConceptCrosswalk.objects.create(concept=surgical, system="foursquare", code="fsq123")
    tsv = "fsq_place_id\tname\tlatitude\tlongitude\taddress\tlocality\ttel\twebsite\tfsq_category_ids\nF1\tAtlas Surgical\t32.511\t74.541\tParis Rd\tSialkot\t+923001112233\thttps://atlas.example\t['fsq123']\n"
    assert loaders.load_places(open_source, loaders.read_foursquare_places(tsv), country="PK")["drafted"] == 1
    csv_text = "id,name,lat,lon,category,phone\nc1,Zed Instruments,32.511,74.541,surgical_supply,+923009998877\n"
    n = loaders.load_places(open_source, loaders.read_generic_csv(csv_text, system="overture"), country="PK")
    assert n["drafted"] == 1
