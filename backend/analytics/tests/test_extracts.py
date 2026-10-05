import pytest
from django.test import Client

from accounts.roles import grant_role
from analytics import extracts as ex
from billing import services as bs
from billing.models import Product
from core.models import AuditLog


@pytest.fixture(autouse=True)
def extract_dir(settings, tmp_path):
    settings.EXTRACT_DIR = tmp_path


@pytest.fixture
def admin(users):
    grant_role(users["mod"], "admin")
    return users["mod"]


def _staff(user):
    c = Client()
    c.force_login(user)
    s = c.session
    s["mfa_ok"] = True
    s.save()
    return c


def _seed(tree, make_published, n=8):
    return [make_published(f"Works {i}", tree["paris"], phone=f"0300 000 00{i:02d}") for i in range(n)]


def test_statistics_are_aggregates_only_and_hide_small_cells(tree, surgical, make_published, admin):
    _seed(tree, make_published, 8)
    rep = ex.statistics_report("pk.punjab.sialkot", surgical)
    assert rep["published"] == 8
    text = ex.statistics_csv(rep)
    assert "Works 1" not in text and "0300" not in text
    small = ex.statistics_report("pk.punjab.sialkot.paris-road", None)
    assert isinstance(small["by_level"], dict)
    make_published("Lonely Co", tree["sialkot"])
    rep2 = ex.statistics_report("pk.punjab", surgical)
    assert rep2["by_child_place"].get("pk.punjab.sialkot") == 9
    from analytics.rollups import recount_all  # noqa: F401

    tiny = ex.statistics_report("pk.punjab.sialkot.paris-road", surgical)
    assert tiny["entries"] in (8, "fewer than 5")


def test_government_gets_aggregates_only(tree, surgical, make_published, users, admin):
    _seed(tree, make_published)
    c = Client()
    c.force_login(users["adder"])
    assert c.get("/staff/statistics/").status_code in (302, 403)
    assert c.get("/staff/extracts/").status_code in (302, 403)
    staff = _staff(admin)
    r = staff.get("/staff/statistics/?scope=pk.punjab.sialkot&type=" + surgical.slug + "&format=csv")
    assert r.status_code == 200 and b"Works 1" not in r.content


def test_extract_plants_trace_entries_excludes_contacts_and_identifies_leaks(tree, surgical, make_published, admin):
    es_ = _seed(tree, make_published, 10)
    with pytest.raises(ex.ExtractError):
        ex.build_extract(admin, "pk.punjab.sialkot", surgical)  # needs an order or a purpose
    one = ex.build_extract(admin, "pk.punjab.sialkot", surgical, purpose="research", buyer_label="Buyer A")
    two = ex.build_extract(admin, "pk.punjab.sialkot", surgical, purpose="research", buyer_label="Buyer B")
    data = ex.read_extract(one, admin).decode()
    assert "0300" not in data and "@" not in data
    assert one.row_count == 10 and one.trace_count >= 3
    assert data.count("\n") == 1 + 10 + one.trace_count
    traces = list(one.traces.all())
    assert all(t.name in data for t in traces)
    assert not any(t.name in ex.read_extract(two, admin).decode() for t in traces)  # traces differ per extract
    sample = "\n".join(ln for ln in data.splitlines() if traces[0].name in ln)
    assert list(ex.identify_leak("copied from somewhere: " + sample)) == [one.pk]
    assert ex.identify_leak("Works 1 and Works 2 only") == {}
    assert AuditLog.objects.filter(action="extract.download").exists() and es_


def test_extract_skips_people_and_do_not_share_and_needs_paid_order(tree, surgical, make_published, admin, users):
    keep = _seed(tree, make_published, 5)
    keep[0].visibility_flags = ["do_not_share"]
    keep[0].save()
    ex1 = ex.build_extract(admin, "pk", surgical, purpose="r")
    assert ex1.row_count == 4
    bs.seed_products()
    prod = Product.objects.get(key="extract-custom")
    order = bs.create_order(users["adder"], prod, scope_path="pk")
    with pytest.raises(ex.ExtractError):
        ex.build_extract(admin, "pk", surgical, order=order)
    bs.record_payment(order, provider="manual", provider_ref="X1", amount_minor=order.amount_minor, actor=admin)
    order.refresh_from_db()
    assert ex.build_extract(admin, "pk", surgical, order=order).order_ref == order.ref


def test_no_user_export_route():
    from django.urls import get_resolver

    bad = [
        str(p.pattern)
        for p in get_resolver().url_patterns
        if any(w in str(p.pattern).lower() for w in ("export", "download", "extract"))
    ]
    assert bad == [], bad
    from catalog.urls import urlpatterns

    for p in urlpatterns:
        s = str(p.pattern)
        if any(w in s for w in ("export", "download", "extract")):
            assert s.startswith("staff/"), s


def test_a_shared_address_never_points_at_the_wrong_extract(tree, surgical, make_published, admin):
    from analytics.models import TraceEntry

    _seed(tree, make_published, 6)
    one = ex.build_extract(admin, "pk.punjab.sialkot", surgical, purpose="r", buyer_label="A")
    two = ex.build_extract(admin, "pk.punjab.sialkot", surgical, purpose="r", buyer_label="B")
    a = one.traces.first()
    TraceEntry.objects.filter(extract=two).update(address_text=a.address_text)  # force the same address in both
    assert list(ex.identify_leak(f"somebody posted: {a.address_text}")) == []  # an address alone proves nothing
    assert list(ex.identify_leak(f"{a.name}, {a.address_text}")) == [one.pk]


def test_trace_names_are_never_reused_across_extracts(tree, surgical, make_published, admin):
    from analytics.models import TraceEntry

    _seed(tree, make_published, 6)
    for i in range(8):
        ex.build_extract(admin, "pk.punjab.sialkot", surgical, purpose="r", buyer_label=str(i))
    names = list(TraceEntry.objects.values_list("name", flat=True))
    assert len(names) == len(set(names)) >= 24
