import pytest

from core.models import RegistryVersion
from taxonomy.models import AddonField
from taxonomy.services import TaxonomyError, bump_template, create_concept, find_concepts, validate_addons


def test_synonyms_find_one_concept(db):
    c = create_concept(
        kind="list_type", name="Petrol pumps", synonyms=["gas station", "fuel station", "filling station"]
    )
    for q in ("Gas Station", "FUEL  station", "petrol pumps"):
        assert list(find_concepts(q)) == [c]
    assert not find_concepts("hotel").exists()


def test_list_type_slug_cannot_shadow_system_or_place(db, tree):
    with pytest.raises(TaxonomyError):
        create_concept(kind="list_type", name="Search")
    with pytest.raises(TaxonomyError):
        create_concept(kind="list_type", name="Sialkot")


def test_same_name_other_kind_is_fine(db):
    create_concept(kind="list_type", name="Plumbing")
    assert create_concept(kind="service", name="Plumbing").pk


def test_addon_validation(surgical):
    tpl = surgical.template
    assert validate_addons(tpl, {"business_type": "manufacturer", "product_categories": ["x"]}, for_publish=True) == []
    probs = dict(validate_addons(tpl, {"business_type": "pirate", "oem": "yes", "year_established": 1700, "zzz": 1}))
    assert probs["business_type"] == "not an allowed choice" and probs["oem"] == "must be true or false"
    assert probs["year_established"] == "below minimum" and probs["zzz"] == "unknown field"
    missing = dict(validate_addons(tpl, {}, for_publish=True))
    assert set(missing) == {"business_type", "product_categories"}


def test_deprecated_field_rejected_and_version_bumped(surgical):
    tpl = surgical.template
    AddonField.objects.filter(template=tpl, key="moq").update(deprecated_at="2026-01-01T00:00:00Z")
    assert dict(validate_addons(tpl, {"moq": "100"}))["moq"] == "unknown field"
    assert bump_template(tpl, "tester") == 2
    assert RegistryVersion.objects.filter(registry_key="addon:manufacturers", version=2).exists()
