import pytest

from access.policy import FIELDS, Viewer, list_mode, scope_of, visible

OWN = "pk.punjab.sialkot"


@pytest.mark.parametrize(
    "own,place,expected",
    [
        (OWN, "pk.punjab.sialkot", "own"),
        (OWN, "pk.punjab.sialkot.paris-road", "own"),
        (OWN, "pk.punjab", "wider"),
        (OWN, "pk", "wider"),
        (OWN, "", "wider"),
        (OWN, "pk.punjab.sialkotx", "wider"),
        (OWN, "ae.dubai", "wider"),
        (None, "pk.punjab.sialkot", "wider"),
    ],
)
def test_scope(own, place, expected):
    assert scope_of(Viewer(own_path=own), place) == expected


def test_list_mode():
    assert list_mode(Viewer(subscriber=True), "pk") == "full"
    assert list_mode(Viewer(own_path=OWN), "pk.punjab.sialkot.x") == "free"
    assert list_mode(Viewer(own_path=OWN), "pk") == "names"
    assert list_mode(Viewer(), "pk.punjab.sialkot") == "names"


EXPECTED = {  # the plans-and-visibility table of the technical plan, appendix C.4, as an independent copy
    "name": ("full", "full", "full"),
    "name_variants": ("full", "full", "full"),
    "category": ("full", "full", "full"),
    "area": ("full", "full", "full"),
    "checks": ("full", "full", "full"),
    "status": ("full", "full", "full"),
    "specialities": ("first3", "none", "full"),
    "free_details": ("full", "none", "full"),
    "address": ("area", "none", "full"),
    "location": ("area", "none", "full"),
    "website": ("locked", "none", "full"),
    "social_links": ("locked", "none", "full"),
    "size": ("locked", "none", "full"),
    "markets": ("locked", "none", "full"),
    "min_order": ("locked", "none", "full"),
    "services": ("list", "none", "full"),
    "certificates": ("list", "none", "full"),
    "products": ("locked", "none", "full"),
    "enquiry_one": ("full", "full", "full"),
    "enquiry_many": ("none", "none", "full"),
    "ads": ("full", "full", "none"),
}


def test_visibility_matrix_every_cell():
    own, wider, sub = Viewer(own_path=OWN), Viewer(own_path=OWN), Viewer(subscriber=True, own_path=OWN)
    for field, (a, b, c) in EXPECTED.items():
        assert visible(field, own, OWN + ".x") == a, field
        assert visible(field, wider, "pk") == b, field
        assert visible(field, sub, "pk") == c, field
    assert set(EXPECTED) <= set(FIELDS)


def test_contacts_have_no_visibility_row_so_they_never_show():
    for field in ("phone", "whatsapp", "email", "contacts", "owner_name"):
        for v in (Viewer(), Viewer(subscriber=True, own_path=OWN)):
            assert visible(field, v, OWN) == "none"
    assert not {"phone", "whatsapp", "email", "contacts"} & set(FIELDS)


def test_ads_only_for_free():
    assert visible("ads", Viewer(), "pk") != "none" and visible("ads", Viewer(subscriber=True), "pk") == "none"
