import pytest
from django.core.management import call_command

from places.models import Place
from taxonomy.models import Concept, PlaceList

pytestmark = pytest.mark.django_db


def test_generate_lists_creates_each_type_at_each_place_and_is_repeatable(tree):
    call_command("seed_taxonomy")
    types = Concept.objects.filter(kind="list_type", status="active").count()
    places = Place.objects.filter(status="active").count()
    call_command("generate_lists")
    assert PlaceList.objects.count() == types * places
    call_command("generate_lists")
    assert PlaceList.objects.count() == types * places


def test_levels_filter_and_dry_run(tree):
    call_command("seed_taxonomy")
    call_command("generate_lists", "--dry-run")
    assert PlaceList.objects.count() == 0
    call_command("generate_lists", "--levels=country")
    n = Place.objects.filter(status="active", level="country").count()
    assert PlaceList.objects.count() == n * Concept.objects.filter(kind="list_type", status="active").count()
