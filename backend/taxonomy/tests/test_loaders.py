from taxonomy.loaders import (
    concept_for_code,
    load_foursquare_categories,
    load_isco,
    load_overture_categories,
    load_own_csv,
)
from taxonomy.models import Concept
from taxonomy.services import find_concepts


def test_overture_categories_build_a_tree_and_crosswalk(db):
    text = (
        "category_code;Overture Taxonomy\n"
        "restaurant;[eat_and_drink,restaurant]\n"
        "italian_restaurant;[eat_and_drink,restaurant,italian_restaurant]\n"
        "gas_station;[energy_and_utility,gas_station]\n"
    )
    out = load_overture_categories(text)
    assert out["created"] == 5
    italian = concept_for_code("overture", "italian_restaurant")
    assert italian.parent == concept_for_code("overture", "restaurant") and italian.kind == "list_type"
    assert concept_for_code("overture", "eat_and_drink").kind == "family"
    assert load_overture_categories(text)["created"] == 0  # repeat load changes nothing


def test_foursquare_categories_use_the_label_path(db):
    text = "category_id\tcategory_label\n4bf58dd8\tDining and Drinking > Restaurant\n4bf58dd9\tDining and Drinking > Restaurant > Italian Restaurant\n"
    load_foursquare_categories(text)
    leaf = concept_for_code("foursquare", "4bf58dd9")
    assert leaf.parent == concept_for_code("foursquare", "4bf58dd8") and leaf.parent.parent.kind == "family"


def test_isco_groups_by_prefix(db):
    load_isco(
        "2,Professionals\n21,Science professionals\n212,Mathematicians and statisticians\n2120,Mathematicians, actuaries\n"
    )
    assert concept_for_code("isco", "2120").parent == concept_for_code("isco", "212")


def test_own_csv_adds_synonyms_in_both_scripts_and_never_renames(db):
    text = "kind,slug,name,language,parent_slug,synonyms\nlist_type,petrol-pumps,Petrol pumps,en,,gas station|fuel station|پیٹرول پمپ@ur\n"
    load_own_csv(text)
    assert find_concepts("gas station").first().slug == "petrol-pumps"
    assert find_concepts("پیٹرول پمپ").first().slug == "petrol-pumps"
    load_own_csv(text.replace("Petrol pumps", "Renamed"))
    assert Concept.objects.get(slug="petrol-pumps").label("en") == "Petrol pumps"
