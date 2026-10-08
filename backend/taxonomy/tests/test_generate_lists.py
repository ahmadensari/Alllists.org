import pytest
from django.core.management import call_command

from places.models import Place
from taxonomy.models import Concept, PlaceList

pytestmark = pytest.mark.django_db


def test_generate_lists_creates_each_type_at_each_place_and_is_repeatable(tree):
    call_command("seed_taxonomy")
    types = Concept.objects.filter(kind="list_type", status="active").count()
    places = Place.objects.filter(status="active").count()
    call_command("generate_lists", "--all")
    assert PlaceList.objects.count() == types * places
    call_command("generate_lists", "--all")
    assert PlaceList.objects.count() == types * places


def test_levels_filter_and_dry_run(tree):
    call_command("seed_taxonomy")
    call_command("generate_lists", "--all", "--dry-run")
    assert PlaceList.objects.count() == 0
    call_command("generate_lists", "--all", "--levels=country")
    n = Place.objects.filter(status="active", level="country").count()
    assert PlaceList.objects.count() == n * Concept.objects.filter(kind="list_type", status="active").count()


def test_extended_set_loads_once_and_gates_individuals(tree):
    call_command("seed_taxonomy", "--extended")
    n = Concept.objects.filter(kind="list_type").count()
    assert n > 200
    call_command("seed_taxonomy", "--extended")
    assert Concept.objects.filter(kind="list_type").count() == n
    c = Concept.objects.get(kind="list_type", slug="electricians")
    assert c.settings.is_individual and c.settings.share_hidden
    q = Concept.objects.filter(kind="list_type", slug__contains="quran").first()
    assert q is None or q.settings.is_child_facing


def test_large_runs_need_confirmation(tree, monkeypatch):
    from core.management.commands import generate_lists as gl

    call_command("seed_taxonomy")
    monkeypatch.setattr(gl, "LARGE", 10)
    call_command("generate_lists", "--all")
    assert PlaceList.objects.count() == 0
    call_command("generate_lists", "--all", "--confirm-large")
    assert PlaceList.objects.count() > 10


def test_default_lists_exist_only_where_entries_live_and_above(tree, entry):
    from analytics.rollups import recount_all
    from places.services import create_place

    lahore = create_place(parent=tree["punjab"], level=Place.Level.CITY, name="Lahore")
    islamabad = create_place(parent=tree["pk"], level=Place.Level.ADMIN1, name="Islamabad Capital")
    recount_all()
    call_command("generate_lists")
    where = set(PlaceList.objects.filter(concept=entry.primary_concept).values_list("place__path", flat=True))
    # the entry's address decides: Paris Road, Sialkot, Punjab, Pakistan and the world; nowhere else
    assert where == {tree["paris"].path, tree["sialkot"].path, tree["punjab"].path, tree["pk"].path, tree["world"].path}
    assert lahore.path not in where and islamabad.path not in where
    n = PlaceList.objects.count()
    call_command("generate_lists")
    assert PlaceList.objects.count() == n


def test_prune_removes_lists_that_lost_their_entries(tree, entry):
    from analytics.rollups import recount_all

    recount_all()
    call_command("generate_lists")
    n = PlaceList.objects.count()
    assert n > 0
    entry.deleted_at = entry.created_at
    entry.save(update_fields=["deleted_at"])
    recount_all()
    call_command("generate_lists", "--prune")
    assert PlaceList.objects.count() == 0
