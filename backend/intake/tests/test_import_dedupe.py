import pytest

from entries import services as es
from entries.models import Contact, CreditEvent, Entry
from intake import dedupe
from intake.importer import ImportError_, guess_mapping, normalise_row, parse_table, run_import
from intake.models import DedupeCandidate, ImportBatch, Source
from intake.gate import SourceBlocked

CSV = """Business Name,Mobile,Address,Products
Crescent Surgical Works,0300-111-2222,Paris Road,"scissors, forceps"
Falcon Medical Instruments,0301 333 4444 / 0302 555 6666,Kashmir Road,dental
,0300 999 9999,Nowhere,
"""


def batch(tree, surgical, users, source, text=CSV, rights=True):
    return ImportBatch.objects.create(
        source=source,
        uploader=users["adder"],
        declared_rights=rights,
        place=tree["sialkot"],
        concept=surgical,
        raw_text=text,
    )


def run(b, addons=True):
    return run_import(b, addons={"business_type": "manufacturer", "product_categories": ["x"]} if addons else None)


def test_parse_detects_delimiters():
    h, rows = parse_table("name\tphone\nA\t0300 1\nB\t0300 2")
    assert h == ["name", "phone"] and len(rows) == 2
    h, rows = parse_table("name;phone\nA;1")
    assert h == ["name", "phone"]
    with pytest.raises(ImportError_):
        parse_table("  ")


def test_header_guess_english_urdu_roman_urdu():
    assert guess_mapping(["Business Name", "Mobile", "Address", "Products"]) == {
        "Business Name": "name",
        "Mobile": "phone",
        "Address": "address",
        "Products": "specialities",
    }
    assert guess_mapping(["نام", "موبائل", "پتہ"]) == {"نام": "name", "موبائل": "phone", "پتہ": "address"}
    assert guess_mapping(["Naam", "Raabta", "Pata"]) == {"Naam": "name", "Raabta": "phone", "Pata": "address"}
    assert guess_mapping(["foo", "bar"]) == {}


def test_normalise_row_phones_and_website():
    m = {"N": "name", "P": "phone", "W": "website"}
    out = normalise_row({"N": "  A   B ", "P": "0300-111-2222 / 042 111 222", "W": "a.example.org"}, m, "PK")
    assert out["name"] == "A B" and out["phones"][0] == "+923001112222" and out["website"] == "https://a.example.org"


def test_import_creates_drafts_with_provenance_and_no_earnings(tree, surgical, users, green):
    counts = run(batch(tree, surgical, users, green))
    assert counts["rows"] == 3 and counts["drafted"] == 2 and counts["error"] == 1
    entries = Entry.objects.filter(created_via="import")
    assert entries.count() == 2 and set(entries.values_list("publish_state", flat=True)) == {"draft"}
    assert all(e.source_id == green.pk for e in entries)
    assert Contact.objects.filter(entry__name="Falcon Medical Instruments").count() == 2
    assert not CreditEvent.objects.filter(entry__in=entries, eligible=True).exists()


def test_import_requires_rights_and_a_green_or_reviewed_source(tree, surgical, users, green):
    with pytest.raises(ImportError_):
        run(batch(tree, surgical, users, green, rights=False))
    red = Source.objects.create(name="Scraped", tier="red", allowed_uses=["import"])
    with pytest.raises(SourceBlocked):
        run(batch(tree, surgical, users, red))
    amber = Source.objects.create(name="Chamber list", tier="amber", allowed_uses=["import"])
    with pytest.raises(SourceBlocked):
        run(batch(tree, surgical, users, amber))


def test_missing_name_column_fails_clearly(tree, surgical, users, green):
    b = batch(tree, surgical, users, green, text="foo,bar\n1,2")
    with pytest.raises(ImportError_):
        run(b)


def test_same_phone_similar_spelling_auto_merges_and_keeps_first_credit(tree, surgical, users, green):
    first = es.create_entry(
        name="Crescent Surgical Works",
        place=tree["sialkot"],
        primary_concept=surgical,
        created_by=users["mod"],
        contacts=[("phone", "0300 111 2222")],
        addons={"business_type": "manufacturer", "product_categories": ["x"]},
    )
    counts = run(batch(tree, surgical, users, green, text="Name,Phone\nCrescent Surgical Work,+92 300 111 2222"))
    assert counts["duplicate"] == 1 and Entry.objects.filter(merged_into=first).count() == 1
    dropped = Entry.objects.get(merged_into=first)
    assert dropped.publish_state == "suppressed"
    adds = CreditEvent.objects.filter(entry=first, kind="added").order_by("created_at", "id")
    assert adds.count() == 2 and adds[0].user == users["mod"]
    assert adds[1].ineligible_reason == "duplicate" and not adds[1].eligible
    assert Contact.objects.filter(entry=first).count() == 2


def test_similar_name_without_phone_goes_to_review_not_merge(tree, surgical, users, green):
    es.create_entry(
        name="Royal Steel Instruments",
        place=tree["sialkot"],
        primary_concept=surgical,
        created_by=users["mod"],
        addons={"business_type": "trader", "product_categories": ["x"]},
    )
    counts = run(batch(tree, surgical, users, green, text="Name,Address\nRoyal Steel Instrument,Paris Road"))
    assert counts["possible_duplicate"] == 1 and counts["duplicate"] == 0
    cand = DedupeCandidate.objects.get()
    assert dedupe.REVIEW <= cand.score < dedupe.AUTO_MERGE and cand.state == "pending"


def test_different_shops_same_road_are_not_candidates(tree, surgical, users, green):
    es.create_entry(
        name="Crescent Surgical Works",
        place=tree["sialkot"],
        primary_concept=surgical,
        created_by=users["mod"],
        addons={"business_type": "trader", "product_categories": ["x"]},
    )
    counts = run(batch(tree, surgical, users, green, text="Name,Address\nUnity Medical Traders,Paris Road"))
    assert counts["possible_duplicate"] == 0 and not DedupeCandidate.objects.exists()


def test_urdu_spelling_variants_match_after_fold(tree, surgical, users, green):
    a = "كريسنت سرجيكل"  # Arabic yeh and kaf
    b = "کریسنت سرجیکل"  # Farsi yeh and keheh
    assert dedupe.similarity(a, b) == 1.0
    es.create_entry(
        name=a,
        place=tree["sialkot"],
        primary_concept=surgical,
        created_by=users["mod"],
        contacts=[("phone", "0300 000 1111")],
        addons={"business_type": "trader", "product_categories": ["x"]},
    )
    counts = run(batch(tree, surgical, users, green, text=f"Name,Phone\n{b},0300 000 1111"))
    assert counts["duplicate"] == 1


def test_distance_feature(tree, surgical, users):
    from decimal import Decimal

    addons = {"business_type": "trader", "product_categories": ["x"]}
    a = es.create_entry(
        name="A Shop",
        place=tree["sialkot"],
        primary_concept=surgical,
        addons=addons,
        lat=Decimal("32.5"),
        lon=Decimal("74.5"),
    )
    b = es.create_entry(
        name="B Shop",
        place=tree["sialkot"],
        primary_concept=surgical,
        addons=addons,
        lat=Decimal("32.5003"),
        lon=Decimal("74.5"),
    )
    assert dedupe.features(a, b)["distance"] == 1.0 and dedupe.features(a, b)["distance_m"] < 100


def test_merge_guards(tree, surgical, entry, users):
    with pytest.raises(es.EntryError):
        es.merge_entries(entry, entry)
    other = es.create_entry(
        name="Other",
        place=tree["sialkot"],
        primary_concept=surgical,
        addons={"business_type": "trader", "product_categories": ["x"]},
    )
    es.merge_entries(entry, other, actor=users["mod"])
    with pytest.raises(es.EntryError):
        es.merge_entries(entry, other)


def test_scan_all_stores_candidates_once(tree, surgical, users):
    for nm in ("Royal Steel Instruments", "Royal Steel Instrument"):
        es.create_entry(
            name=nm,
            place=tree["sialkot"],
            primary_concept=surgical,
            created_by=users["mod"],
            addons={"business_type": "trader", "product_categories": ["x"]},
        )
    assert dedupe.scan_all() == 1 and dedupe.scan_all() == 0
