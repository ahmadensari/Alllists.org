import pytest

from places.models import Place, PlaceProposal
from places.services import PlaceError, approve_proposal, create_place, descendants, propose_area
from taxonomy.services import create_concept


def test_path_depth_and_country(tree):
    assert tree["pk"].path == "pk" and tree["pk"].country_code == "PK"
    assert tree["sialkot"].path == "pk.punjab.sialkot" and tree["sialkot"].depth == 3
    assert tree["paris"].country_code == "PK" and tree["paris"].path == "pk.punjab.sialkot.paris-road"
    assert tree["world"].path == ""


def test_descendants_is_a_prefix_scan(tree):
    ids = set(descendants(tree["punjab"]).values_list("slug", flat=True))
    assert ids == {"sialkot", "paris-road"}
    assert descendants(tree["world"]).count() == 4


def test_names_in_both_scripts(tree):
    assert tree["pk"].name_for("ur") == "پاکستان" and tree["pk"].name_for("en") == "Pakistan"


def test_country_needs_code(db, tree):
    with pytest.raises(PlaceError):
        create_place(parent=tree["world"], level=Place.Level.COUNTRY, name="Nowhere")


def test_slug_collision_with_list_type_refused(tree, db):
    create_concept(kind="list_type", name="Hotels")
    with pytest.raises(PlaceError):
        create_place(parent=tree["pk"], level=Place.Level.ADMIN1, name="Hotels")


def test_duplicate_proposal_is_flagged_and_pending_one_can_be_approved(tree):
    dup = propose_area(parent=tree["sialkot"], name="PARIS  road")
    assert dup.state == PlaceProposal.State.DUPLICATE and dup.duplicate_of == tree["paris"]
    new = propose_area(parent=tree["sialkot"], name="Kashmir Road")
    assert new.state == PlaceProposal.State.PENDING
    place = approve_proposal(new, actor=None)
    new.refresh_from_db()
    assert new.state == PlaceProposal.State.APPROVED and place.path.endswith("kashmir-road")
    with pytest.raises(PlaceError):
        approve_proposal(new, actor=None)
