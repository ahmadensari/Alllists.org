"""The paywall rule, tested against a plain-language reference and at every boundary (found weak by the mutation check):
what a subscription covers, what a free viewer's own place covers, and what each field shows to each kind of viewer."""

import itertools

import pytest
from hypothesis import given, settings as hs, strategies as st

from access.policy import FIELDS, FREE_OWN, FREE_WIDER, SUBSCRIBER, Viewer, list_mode, scope_of, subscribes_to, visible

SEG = ["pk", "punjab", "punjabi", "sialkot", "sialkot2", "paris-road", "lahore"]
paths = st.lists(st.sampled_from(SEG), min_size=0, max_size=4).map(lambda p: ".".join(p))
concepts = st.one_of(st.none(), st.integers(1, 3))


def reference_covers(scope_path, scope_cid, place_path, concept_id):
    """In words: the scope's place is the world, or the same place, or an ancestor of the entry's place (a whole segment,
    never a longer name that merely starts the same); and the list type matches, or either side names no list type."""
    parts_s = scope_path.split(".") if scope_path else []
    parts_p = place_path.split(".") if place_path else []
    place_ok = parts_p[: len(parts_s)] == parts_s
    type_ok = scope_cid is None or concept_id is None or scope_cid == concept_id
    return place_ok and type_ok


@given(st.lists(st.tuples(paths, concepts), max_size=3), paths, concepts)
@hs(max_examples=600, deadline=None)
def test_subscription_cover_matches_the_reference_for_any_scopes(scopes, place_path, concept_id):
    viewer = Viewer(scopes=tuple(scopes))
    expected = any(reference_covers(p, c, place_path, concept_id) for p, c in scopes)
    assert subscribes_to(viewer, place_path, concept_id) is expected


@given(paths, paths)
@hs(max_examples=400, deadline=None)
def test_own_place_is_exactly_the_subtree(own, place_path):
    expected = "own" if own and reference_covers(own, None, place_path, None) else "wider"
    assert scope_of(Viewer(own_path=own or None), place_path) == (expected if own else "wider")


@pytest.mark.parametrize(
    "scope,cid,place,concept,covers",
    [
        ("pk.punjab.sialkot", 1, "pk.punjab.sialkot", 1, True),  # the very place
        ("pk.punjab.sialkot", 1, "pk.punjab.sialkot.paris-road", 1, True),  # below it
        ("pk.punjab.sialkot", 1, "pk.punjab", 1, False),  # above it
        ("pk.punjab.sialkot", 1, "pk.punjab.sialkot2", 1, False),  # a different place whose name starts the same
        ("pk.punjab.sialkot", 1, "pk.punjab.lahore", 1, False),  # a sibling
        ("pk.punjab", 1, "pk.punjabi.sialkot", 1, False),  # prefix without the dot
        ("pk.punjab.sialkot", 1, "pk.punjab.sialkot", 2, False),  # right place, other list type
        ("pk.punjab.sialkot", None, "pk.punjab.sialkot", 2, True),  # subscription to every type there
        ("pk.punjab.sialkot", 1, "pk.punjab.sialkot", None, True),  # a place page names no type
        ("", 1, "pk.punjab.sialkot", 1, True),  # whole world, one type
        ("", 1, "pk.punjab.sialkot", 2, False),
        ("", None, "anything.at.all", 3, True),
        ("pk.punjab.sialkot", None, "pk", None, False),
    ],
)
def test_subscription_boundaries(scope, cid, place, concept, covers):
    assert subscribes_to(Viewer(scopes=((scope, cid),)), place, concept) is covers


def test_no_subscription_covers_nothing_and_the_flag_covers_everything():
    assert not subscribes_to(Viewer(), "pk", 1) and not subscribes_to(Viewer(scopes=()), "", None)
    assert subscribes_to(Viewer(subscriber=True), "any.place", 99)


def test_several_scopes_any_one_is_enough_and_a_wrong_one_adds_nothing():
    v = Viewer(scopes=(("pk.punjab.lahore", 1), ("pk.punjab.sialkot", 2)))
    assert subscribes_to(v, "pk.punjab.sialkot.paris-road", 2)
    assert not subscribes_to(v, "pk.punjab.sialkot.paris-road", 1)
    assert subscribes_to(v, "pk.punjab.lahore", 1) and not subscribes_to(v, "pk.punjab.lahore", 2)


# ---- what each kind of viewer sees ----------------------------------------------------------------------------------------------

SUB = Viewer(scopes=(("pk.punjab.sialkot", None),))
OWN = Viewer(own_path="pk.punjab.sialkot")
WIDE = Viewer(own_path="pk.punjab.lahore")
NOWHERE = Viewer()
PLACE = "pk.punjab.sialkot.paris-road"


def test_each_viewer_gets_the_column_of_the_table_meant_for_them():
    for field, row in FIELDS.items():
        assert visible(field, SUB, PLACE) == row[SUBSCRIBER], field
        assert visible(field, OWN, PLACE) == row[FREE_OWN], field
        assert visible(field, WIDE, PLACE) == row[FREE_WIDER], field
        assert visible(field, NOWHERE, PLACE) == row[FREE_WIDER], field  # unknown own place counts as wider
    assert visible("not_a_field", SUB, PLACE) == "none" and visible("contact", SUB, PLACE) == "none"


def test_a_subscription_elsewhere_does_not_unlock_here():
    far = Viewer(own_path="pk.punjab.lahore", scopes=(("pk.punjab.lahore", None),))
    assert list_mode(far, PLACE) == "names" and visible("website", far, PLACE) == FIELDS["website"][FREE_WIDER]
    assert list_mode(far, "pk.punjab.lahore.model-town") == "full"


@pytest.mark.parametrize("viewer,mode", [(SUB, "full"), (OWN, "free"), (WIDE, "names"), (NOWHERE, "names")])
def test_list_modes(viewer, mode):
    assert list_mode(viewer, PLACE) == mode


def test_table_rules_that_must_never_change():
    assert not [f for f in FIELDS if "contact" in f or "phone" in f or "email" in f]  # contacts are not a field (R02)
    for f in ("name", "checks", "status", "category", "area"):
        assert set(FIELDS[f]) == {"full"}, f  # the basics and the check labels are free for everyone (R03)
    assert FIELDS["ads"][SUBSCRIBER] == "none" and FIELDS["ads"][FREE_OWN] == "full"
    assert FIELDS["enquiry_many"][FREE_OWN] == "none" and FIELDS["enquiry_many"][FREE_WIDER] == "none"
    for f, row in FIELDS.items():
        if f != "ads":
            assert row[SUBSCRIBER] == "full", f  # a subscriber sees everything, except the ads they are spared


def test_a_free_viewer_never_sees_more_in_a_wider_place_than_in_their_own():
    rank = {"none": 0, "locked": 1, "area": 2, "list": 2, "first3": 3, "names": 1, "full": 4}
    for f, row in FIELDS.items():
        if f in ("ads",):
            continue
        assert rank[row[FREE_WIDER]] <= rank[row[FREE_OWN]], f
    assert itertools.count
