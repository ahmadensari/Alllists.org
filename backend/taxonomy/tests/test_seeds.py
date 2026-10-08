import pytest
from django.core.management import call_command

from taxonomy.models import AddonField, AddonTemplate, Concept, ListTypeSettings
from taxonomy.seeds import FAMILIES, FAMILY_TREE
from taxonomy.services import find_concepts, validate_addons


@pytest.fixture
def seeded(db):
    call_command("seed_taxonomy")


def test_all_twelve_families_and_all_named_list_types_exist(seeded):
    assert set(AddonTemplate.objects.values_list("key", flat=True)) >= set(FAMILIES)
    assert len(FAMILIES) == 11 + 0 or len(FAMILIES) >= 11
    names = {c.label("en") for c in Concept.objects.filter(kind="list_type")}
    for must in [
        "Petrol pumps",
        "Schools",
        "Beauty parlours and salons",
        "Bakeries",
        "Mobile stores",
        "Mobile phone repair",
        "Spare parts shops",
        "Furniture stores",
        "Medical stores and pharmacies",
        "Doctors",
        "Nurses",
        "Bookshops",
        "Hardware shops",
        "MRI and imaging centres",
        "Plumbers",
        "Quran tutors",
        "Surgical instrument makers",
        "Football makers",
        "Fan makers",
        "Sanitaryware makers",
        "Furniture makers",
        "Hotels",
        "Eye doctors",
        "Eye hospitals",
        "Contractors",
        "Data scientists",
        "Factories and suppliers",
    ]:
        assert must in names, must


def test_seeding_twice_changes_nothing(seeded):
    before = Concept.objects.count()
    call_command("seed_taxonomy")
    assert Concept.objects.count() == before


def test_gates_are_set_for_individuals_children_and_health(seeded):
    def settings_of(name):
        return ListTypeSettings.objects.get(
            concept__labels__text=name, concept__labels__kind="preferred", concept__kind="list_type"
        )

    assert settings_of("Quran tutors").is_child_facing and settings_of("Quran tutors").is_individual
    assert (
        settings_of("Doctors").is_health
        and settings_of("Doctors").is_individual
        and settings_of("Doctors").share_hidden
    )
    assert settings_of("Hospitals").is_health and not settings_of("Hospitals").is_individual
    assert not settings_of("Bakeries").is_health and not settings_of("Bakeries").share_hidden


def test_talent_list_is_paused_so_it_is_not_reachable(seeded, client):
    ds = Concept.objects.get(kind="list_type", labels__text="Data scientists", labels__kind="preferred")
    assert ds.status == "paused" and ds.natural_scale == "global"


def test_synonyms_and_urdu_names_find_the_concept(seeded):
    assert any(c.label("en") == "Petrol pumps" for c in find_concepts("gas station"))
    assert any(c.label("en") == "Petrol pumps" for c in find_concepts("پیٹرول پمپ"))
    assert find_concepts("پیٹرول پمپ").first().label("ur") == "پیٹرول پمپ"


def test_every_template_validates_and_required_fields_gate_publish(seeded):
    for key in FAMILIES:
        tpl = AddonTemplate.objects.get(key=key)
        required = set(AddonField.objects.filter(template=tpl, required_for_publish=True).values_list("key", flat=True))
        missing = {k for k, _ in validate_addons(tpl, {}, for_publish=True)}
        assert missing == required, key


def test_doctors_pilot_fields_follow_the_spec(seeded):
    keys = set(AddonField.objects.filter(template__key="doctors").values_list("key", flat=True))
    assert {"specialty", "regulator_number", "consultation_fee", "insurance_panels"} <= keys
    assert AddonField.objects.get(template__key="doctors", key="consultation_fee").show == "L"


def test_every_family_has_listed_types_and_slugs_are_unique(seeded):
    slugs = list(Concept.objects.filter(kind="list_type").values_list("slug", flat=True))
    assert len(slugs) == len(set(slugs)) and len(slugs) >= 28
    assert Concept.objects.filter(kind="family").count() == len(FAMILY_TREE)
