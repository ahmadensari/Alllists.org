from analytics.models import RollupCell
from analytics.rollups import place_paths, recount_all, recount_cell, refresh_for_entry
from entries import services as es


def test_place_paths():
    assert place_paths("pk.punjab.sialkot") == ["", "pk", "pk.punjab", "pk.punjab.sialkot"]
    assert place_paths("") == [""]


def test_incremental_refresh_matches_recount(entry, tree, surgical, users):
    es.record_verification(
        entry, field_group="identity", level="surveyor", actor=users["surveyor"], method="call", evidence="Answered"
    )
    entry.refresh_from_db()
    refresh_for_entry(entry)
    cities = RollupCell.objects.get(place_path=tree["sialkot"].path, concept=surgical)
    assert cities.total == 1 and cities.published == 1 and cities.by_level["surveyor"] == 1
    assert cities.with_contact_pct == 100
    world = RollupCell.objects.get(place_path="", concept=surgical)
    assert world.total == 1
    before = {(c.place_path, c.concept_id): (c.total, c.published) for c in RollupCell.objects.all()}
    recount_all()
    after = {(c.place_path, c.concept_id): (c.total, c.published) for c in RollupCell.objects.all()}
    assert before == after


def test_drafts_count_in_total_but_not_published(entry, tree, surgical):
    refresh_for_entry(entry)
    cell = RollupCell.objects.get(place_path=tree["paris"].path, concept=surgical)
    assert cell.total == 1 and cell.published == 0


def test_merged_entries_leave_the_counts(entry, tree, surgical, users):
    other = es.create_entry(
        name="Dup Co",
        place=tree["paris"],
        primary_concept=surgical,
        addons={"business_type": "trader", "product_categories": ["x"]},
    )
    recount_all()
    assert RollupCell.objects.get(place_path=tree["paris"].path, concept=surgical).total == 2
    es.merge_entries(entry, other)
    recount_all()
    assert RollupCell.objects.get(place_path=tree["paris"].path, concept=surgical).total == 1


def test_empty_cell_is_removed(entry, tree, surgical):
    refresh_for_entry(entry)
    entry.deleted_at = entry.created_at
    entry.save()
    assert recount_cell(entry.country_code, tree["paris"].path, surgical.pk) is None
    assert not RollupCell.objects.filter(place_path=tree["paris"].path).exists()
