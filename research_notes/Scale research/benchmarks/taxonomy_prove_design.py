#!/usr/bin/env python3
"""Proof run for the designs in 05_taxonomy_schema_designs.md. Plain assertions, not pytest: pytest-django would create a
database named test_*, and this work may only touch databases whose names start with bench_.

What it does
  1. applies the repository migrations plus the design migrations to an empty scratch database (bench_alllists_design_*),
  2. builds a small world with the repository's own services (places, concepts, entries),
  3. runs one check per acceptance test named below. Each check carries the pytest name proposed in the note.

It needs a COPY of backend/ that contains the design models (made by the note's patch). It never writes under backend/.

  sudo -u postgres env PYTHONPATH=/var/tmp/benchlibs DJANGO_SETTINGS_MODULE=config.settings POSTGRES_DB=bench_alllists_design_20261006 \
       POSTGRES_USER=postgres POSTGRES_HOST=/var/run/postgresql DJANGO_DEBUG=1 python3 taxonomy_prove_design.py /var/tmp/benchdj/backend
"""
import csv
import os
import random
import sys
import traceback

backend = sys.argv[1]
sys.path.insert(0, backend)
os.chdir(backend)
assert os.environ["POSTGRES_DB"].startswith("bench_alllists_design_"), "scratch database only"
import django  # noqa: E402

django.setup()
from django.conf import settings  # noqa: E402

assert settings.DATABASES["default"]["NAME"].startswith("bench_alllists_design_")
from django.core.management import call_command  # noqa: E402
from django.db import IntegrityError, connection, transaction  # noqa: E402
from django.test.utils import CaptureQueriesContext  # noqa: E402
from django.utils import timezone  # noqa: E402

from analytics import recount  # noqa: E402
from analytics.models import PlaceTotal, RollupCell  # noqa: E402
from analytics.storerule import should_store  # noqa: E402
from catalog import lists  # noqa: E402
from datetime import timedelta  # noqa: E402

from entries import lifecycle as lc  # noqa: E402
from entries import membership as mb  # noqa: E402
from entries.merge import merge_with_undo, unmerge  # noqa: E402
from entries.models import Brand, ClosureSignal, CreditEvent, Entry, EntryConcept, EntryFacet, EntryStatusEvent, MergeEvent  # noqa: E402
from intake.branchrule import classify_pair  # noqa: E402
from places.models import Place  # noqa: E402
from places.services import create_place  # noqa: E402
from taxonomy import closure, crosswalk, facets, slugs  # noqa: E402
from taxonomy.models import (  # noqa: E402
    ClassificationScheme,
    Concept,
    ConceptClosure,
    ConceptCrosswalk,
    ConceptEdge,
    ConceptSlug,
    CrosswalkReview,
    FacetApplicability,
    FacetDef,
    FacetRule,
    FacetValue,
    PlaceList,
)
from taxonomy.services import TaxonomyError, create_concept  # noqa: E402

RESULTS = []


def check(name):
    def deco(fn):
        try:
            fn()
            RESULTS.append((name, "PASS", ""))
        except Exception as e:  # noqa: BLE001
            RESULTS.append((name, "FAIL", f"{type(e).__name__}: {e}\n{traceback.format_exc(limit=3)}"))
        return fn

    return deco


def raises(exc, fn):
    try:
        with transaction.atomic():
            fn()
    except exc:
        return True
    raise AssertionError(f"expected {exc.__name__}")


# --------------------------------------------------------------------------- database
call_command("migrate", verbosity=0)

# --------------------------------------------------------------------------- fixtures
world = create_place(parent=None, level=Place.Level.WORLD, name="World", slug="world")
pk = create_place(parent=world, level=Place.Level.COUNTRY, name="Pakistan", country_code="PK")
punjab = create_place(parent=pk, level=Place.Level.ADMIN1, name="Punjab")
sialkot = create_place(parent=punjab, level=Place.Level.CITY, name="Sialkot")
lahore = create_place(parent=punjab, level=Place.Level.CITY, name="Lahore")
paris = create_place(parent=sialkot, level=Place.Level.AREA, name="Paris Road")
sindh = create_place(parent=pk, level=Place.Level.ADMIN1, name="Sindh")
karachi = create_place(parent=sindh, level=Place.Level.CITY, name="Karachi")

_n = [0]


def mk(name, level, parents=(), kind=Concept.Kind.LIST_TYPE):
    """Create a concept at a level with edges to its parents (first one primary). Registers its slug."""
    c = create_concept(kind=kind, name=name, slug=None)
    Concept.objects.filter(pk=c.pk).update(level=level)
    c.refresh_from_db()
    closure.ensure_self_row(c)
    for i, p in enumerate(parents):
        closure.add_edge(p, c, primary=(i == 0), reason="primary" if i == 0 else "use")
    slugs.register_slug(c, c.slug)
    c.refresh_from_db()
    return c


root = mk("Manufacturing", 0)
leather = mk("Leather goods", 1, [root])
sports = mk("Sports goods", 1, [root])
gloves = mk("Leather gloves", 2, [leather])
prot = mk("Protective sports gear", 2, [sports])
cricket_gloves = mk("Cricket batting gloves", 3, [gloves, prot])  # two routes to the root
sports_gloves = mk("Sports leather gloves", 3, [gloves])
football_gloves = mk("Football goalkeeper gloves", 3, [gloves])
wk_gloves = mk("Wicketkeeping gloves", 4, [cricket_gloves])  # a deeper node under the two-route node


def make_entry(name, place, concept, published=True, **kw):
    e = Entry.objects.create(
        name=name, name_fold=name.lower(), country_code=place.country_code or "PK", primary_concept=concept,
        place=place, place_path=place.path,
        publish_state=Entry.PublishState.PUBLISHED if published else Entry.PublishState.DRAFT, **kw,
    )
    mb.set_primary(e, concept)
    return e


# --------------------------------------------------------------------------- D1 multi-parent concepts
@check("test_closure_matches_edges_after_random_graph")
def _():
    rnd = random.Random(1)
    lv = {0: [mk("rg root", 0)]}
    for level in range(1, 5):
        lv[level] = []
        for i in range(25 if level > 1 else 6):
            ps = rnd.sample(lv[level - 1], min(len(lv[level - 1]), rnd.choice([1, 1, 2, 3])))
            lv[level].append(mk(f"rg l{level} n{i}", level, ps))
    r = closure.check_consistency()
    assert r == {"parent_mismatch": 0, "closure_missing": 0, "closure_extra": 0}, r


@check("test_add_secondary_edge_adds_ancestors_to_all_descendants")
def _():
    # wk_gloves sits under cricket_gloves, which has two routes: leather > gloves and sports > protective
    anc = set(closure.ancestor_ids(wk_gloves.pk))
    assert {leather.pk, sports.pk, gloves.pk, prot.pk, root.pk, cricket_gloves.pk} <= anc
    extra = mk("Boxing hand protection", 2, [sports])
    closure.add_edge(extra, cricket_gloves, reason="use")
    assert extra.pk in closure.ancestor_ids(wk_gloves.pk)
    assert closure.check_consistency()["closure_missing"] == 0


@check("test_cycle_is_rejected")
def _():
    raises(closure.GraphError, lambda: closure.add_edge(wk_gloves, cricket_gloves))
    raises(closure.GraphError, lambda: closure.add_edge(cricket_gloves, cricket_gloves))


@check("test_parent_must_be_one_level_above")
def _():
    raises(closure.GraphError, lambda: closure.add_edge(leather, wk_gloves))  # level 1 to level 4


@check("test_fourth_secondary_parent_rejected")
def _():
    c = mk("cap test child", 3, [gloves])
    for i in range(3):
        closure.add_edge(mk(f"cap parent {i}", 2, [sports]), c)
    raises(closure.GraphError, lambda: closure.add_edge(mk("cap parent 4", 2, [sports]), c))


@check("test_second_primary_edge_rejected_by_database")
def _():
    other = mk("another family", 2, [sports])
    raises(IntegrityError, lambda: ConceptEdge.objects.create(parent=other, child=cricket_gloves, is_primary=True, reason="primary"))


@check("test_remove_secondary_edge_keeps_ancestors_reachable_by_other_path")
def _():
    a, b = mk("two-route A", 2, [leather]), mk("two-route B", 2, [sports])
    d = mk("two-route D", 3, [a, b])
    assert {leather.pk, sports.pk} <= set(closure.ancestor_ids(d.pk))
    closure.remove_edge(b, d)
    anc = set(closure.ancestor_ids(d.pk))
    assert leather.pk in anc and sports.pk not in anc and root.pk in anc
    assert closure.check_consistency()["closure_extra"] == 0


@check("test_set_primary_parent_moves_subtree_and_updates_parent_column")
def _():
    f = mk("movable family", 2, [leather])
    p = mk("movable product", 3, [f])
    v = mk("movable variant", 4, [p])
    closure.set_primary_parent(f, sports)
    f.refresh_from_db()
    assert f.parent_id == sports.pk
    anc = set(closure.ancestor_ids(v.pk))
    assert sports.pk in anc and leather.pk not in anc
    assert closure.check_consistency() == {"parent_mismatch": 0, "closure_missing": 0, "closure_extra": 0}


@check("test_descendants_one_query")
def _():
    with CaptureQueriesContext(connection) as q:
        ids = closure.descendant_ids(root.pk)
    assert len(q) == 1 and wk_gloves.pk in ids


@check("test_parent_column_equals_primary_edge")
def _():
    Concept.objects.filter(pk=sports_gloves.pk).update(parent=prot)  # simulate drift
    assert closure.check_consistency()["parent_mismatch"] == 1
    Concept.objects.filter(pk=sports_gloves.pk).update(parent=gloves)
    assert closure.check_consistency()["parent_mismatch"] == 0


# --------------------------------------------------------------------------- D5 entry_concept (and list pages)
e1 = make_entry("Sialkot Gloves Ltd", sialkot, sports_gloves)
e2 = make_entry("Lahore Cricket Works", lahore, wk_gloves)
e3 = make_entry("Karachi Keepers", karachi, football_gloves)
e4 = make_entry("Draft Maker", sialkot, wk_gloves, published=False)
e5 = make_entry("Paris Road Gloves", paris, cricket_gloves)


@check("test_one_primary_per_entry_db_constraint")
def _():
    raises(IntegrityError, lambda: EntryConcept.objects.create(entry=e1, concept=football_gloves, role=1, state=2))


@check("test_set_primary_demotes_old_primary_to_secondary")
def _():
    e = make_entry("Switcher", sialkot, sports_gloves)
    mb.set_primary(e, football_gloves)
    rows = {m.concept_id: m.role for m in EntryConcept.objects.filter(entry=e)}
    assert rows == {football_gloves.pk: 1, sports_gloves.pk: 2}
    e.refresh_from_db()
    assert e.primary_concept_id == football_gloves.pk  # denormalised copy in step


@check("test_unevidenced_secondary_not_on_list_page")
def _():
    mb.add_secondary(e1, football_gloves, source=EntryConcept.Source.CONTRIBUTOR)  # no evidence
    ids = {e.pk for e in lists.first_page(world, football_gloves)}
    assert e1.pk not in ids and e3.pk in ids


@check("test_secondary_membership_appears_on_list_page")
def _():
    mb.add_secondary(e1, prot, source=EntryConcept.Source.OWNER, evidence_ref=1)
    assert e1.pk in {e.pk for e in lists.first_page(world, prot)}


@check("test_agent_secondary_stays_proposed")
def _():
    row = mb.add_secondary(e2, football_gloves, source=EntryConcept.Source.AGENT, evidence_ref=5, confidence=0.9)
    assert row.state == EntryConcept.State.PROPOSED and not row.listable


@check("test_secondary_cap_enforced_service_and_trigger")
def _():
    e = make_entry("Cap Test", lahore, sports_gloves)
    cs = [mk(f"capnode {i}", 3, [gloves]) for i in range(25)]
    for c in cs[:24]:
        mb.add_secondary(e, c, source=EntryConcept.Source.OWNER, evidence_ref=1)
    raises(mb.MembershipError, lambda: mb.add_secondary(e, cs[24], source=EntryConcept.Source.OWNER, evidence_ref=1))
    # the database trigger is the backstop for code that skips the service
    raises(Exception, lambda: EntryConcept.objects.create(entry=e, concept=cs[24], role=2, state=2, country_code="PK", place_path=e.place_path))


@check("test_entry_counted_once_at_ancestor_with_two_routes")
def _():
    # e5 is primary in cricket_gloves (two routes to the root); add it also under a sibling below gloves
    mb.add_secondary(e5, sports_gloves, source=EntryConcept.Source.OWNER, evidence_ref=1)
    page = [e.pk for e in lists.first_page(world, gloves)]
    assert page.count(e5.pk) == 1
    page2 = [e.pk for e in lists.first_page(world, leather)]
    assert page2.count(e5.pk) == 1


@check("test_list_page_under_node_includes_secondary_parent_route")
def _():
    # wk_gloves is under cricket_gloves, which is under both gloves and prot: e2 must show in both lists
    assert e2.pk in {e.pk for e in lists.first_page(world, gloves)}
    assert e2.pk in {e.pk for e in lists.first_page(world, prot)}
    assert e2.pk not in {e.pk for e in lists.first_page(world, football_gloves)}  # proposed membership only


@check("test_place_filter_includes_places_below_and_excludes_siblings")
def _():
    assert e1.pk in {e.pk for e in lists.first_page(punjab, sports_gloves)}
    assert e3.pk not in {e.pk for e in lists.first_page(punjab, football_gloves)}  # Karachi is in Sindh
    assert e5.pk in {e.pk for e in lists.first_page(sialkot, cricket_gloves)}  # area below the city


@check("test_unpublished_entry_not_listable")
def _():
    assert e4.pk not in {e.pk for e in lists.first_page(world, wk_gloves)}
    Entry.objects.filter(pk=e4.pk).update(publish_state="published")
    e4.refresh_from_db()
    mb.sync_entry_concepts(e4)
    assert e4.pk in {e.pk for e in lists.first_page(world, wk_gloves)}


@check("test_merged_or_deleted_entry_not_listable")
def _():
    e = make_entry("To merge", lahore, sports_gloves)
    Entry.objects.filter(pk=e.pk).update(merged_into=e1)
    e.refresh_from_db()
    mb.sync_entry_concepts(e)
    assert e.pk not in {x.pk for x in lists.first_page(world, sports_gloves)}


@check("test_entry_move_updates_place_path_of_all_memberships")
def _():
    e = make_entry("Mover", lahore, sports_gloves)
    mb.add_secondary(e, prot, source=EntryConcept.Source.OWNER, evidence_ref=1)
    Entry.objects.filter(pk=e.pk).update(place=karachi, place_path=karachi.path)
    e.refresh_from_db()
    mb.sync_entry_concepts(e)
    paths = set(EntryConcept.objects.filter(entry=e).values_list("place_path", flat=True))
    assert paths == {karachi.path}


@check("test_reconcile_fixes_drift")
def _():
    EntryConcept.objects.filter(entry=e1).update(place_path="zz.wrong")
    assert mb.reconcile() >= 1
    assert set(EntryConcept.objects.filter(entry=e1).values_list("place_path", flat=True)) == {e1.place_path}


@check("test_backfill_copies_primary_and_secondary")
def _():
    # legacy shape: an entry with a primary_concept and rows in the old secondary_concepts table, no EntryConcept rows
    e = Entry.objects.create(
        name="Legacy", name_fold="legacy", country_code="PK", primary_concept=sports_gloves, place=lahore,
        place_path=lahore.path, publish_state="published",
    )
    e.secondary_concepts.add(prot, football_gloves)
    from entries.backfill import backfill_entry_concept

    n = backfill_entry_concept(batch=100)
    got = {m.concept_id: m.role for m in EntryConcept.objects.filter(entry=e)}
    assert got == {sports_gloves.pk: 1, prot.pk: 2, football_gloves.pk: 2}, got
    assert backfill_entry_concept(batch=100) == 0  # idempotent


# --------------------------------------------------------------------------- D2 slug history and redirects
@check("test_rename_writes_history_and_old_slug_301")
def _():
    c = mk("Slug test node", 3, [gloves])
    old = c.slug
    slugs.rename(c, "slug-test-renamed")
    r = slugs.resolve_slug(old)
    assert (r.status, r.redirect_slug, r.concept.pk) == (301, "slug-test-renamed", c.pk)
    assert slugs.resolve_slug("slug-test-renamed").status == 200
    assert ConceptSlug.objects.filter(concept=c).count() == 2
    assert ConceptSlug.objects.filter(concept=c, is_current=True).count() == 1


@check("test_old_slug_cannot_be_taken_by_other_concept")
def _():
    c = mk("Slug owner", 3, [gloves])
    old = c.slug
    slugs.rename(c, "slug-owner-new")
    other = mk("Slug taker", 3, [gloves])
    raises(TaxonomyError, lambda: slugs.rename(other, old))


@check("test_rename_back_to_old_slug_reuses_row")
def _():
    c = mk("Slug back", 3, [gloves])
    old = c.slug
    slugs.rename(c, "slug-back-2")
    slugs.rename(c, old)
    assert slugs.resolve_slug(old).status == 200 and slugs.resolve_slug("slug-back-2").status == 301
    assert ConceptSlug.objects.filter(concept=c).count() == 2


@check("test_merge_old_slugs_redirect_to_winner")
def _():
    loser, winner = mk("Merge loser", 3, [gloves]), mk("Merge winner", 3, [gloves])
    slugs.merge(loser, winner)
    r = slugs.resolve_slug(loser.slug)
    assert (r.status, r.concept.pk, r.redirect_slug) == (301, winner.pk, winner.slug)


@check("test_merge_chain_flattened_single_hop")
def _():
    a, b, c = (mk(f"Chain {x}", 3, [gloves]) for x in "abc")
    slugs.merge(a, b)
    slugs.merge(b, c)
    a.refresh_from_db()
    assert a.merged_into_id == c.pk  # flattened, not a -> b -> c
    assert slugs.resolve_slug(a.slug).redirect_slug == c.slug


@check("test_merge_into_self_or_loop_rejected")
def _():
    a, b = mk("Loop a", 3, [gloves]), mk("Loop b", 3, [gloves])
    slugs.merge(a, b)
    raises(TaxonomyError, lambda: slugs.merge(b, a))
    raises(TaxonomyError, lambda: slugs.merge(b, b))


@check("test_retired_slug_returns_410")
def _():
    c = mk("Retire me", 3, [gloves])
    Concept.objects.filter(pk=c.pk).update(status="retired", retired_at=timezone.now())
    assert slugs.resolve_slug(c.slug).status == 410
    assert slugs.resolve_slug("never-existed").status == 404


@check("test_slug_colliding_with_place_rejected")
def _():
    c = mk("Place collision", 3, [gloves])
    raises(TaxonomyError, lambda: slugs.rename(c, "sialkot"))
    raises(TaxonomyError, lambda: slugs.rename(c, "search"))


@check("test_entries_untouched_by_rename")
def _():
    c = mk("Untouched", 3, [gloves])
    e = make_entry("Untouched Ltd", lahore, c)
    before = Entry.objects.filter(pk=e.pk).values_list("updated_at", "primary_concept_id").get()
    slugs.rename(c, "untouched-renamed")
    after = Entry.objects.filter(pk=e.pk).values_list("updated_at", "primary_concept_id").get()
    assert before == after


@check("test_changes_logged_and_release_assigns_version")
def _():
    from taxonomy import changes
    from taxonomy.models import TaxonomyChange

    c = mk("Change log node", 3, [gloves])
    slugs.rename(c, "change-log-renamed")
    v, n = changes.release(changed_by="proof")
    assert n >= 2 and not TaxonomyChange.objects.filter(release__isnull=True).exists()
    d = changes.diff_for_review(v)
    assert "rename" in d and "edge_add" in d
    v2, n2 = changes.release()
    assert v2 == v + 1 and n2 == 0


@check("test_db_check_slug_current_xor_retired")
def _():
    c = mk("Xor", 3, [gloves])
    raises(IntegrityError, lambda: ConceptSlug.objects.create(slug="xor-bad", concept=c, is_current=False, retired_at=None))


# --------------------------------------------------------------------------- D3 crosswalk
hs = ClassificationScheme.objects.create(key="hs2022", name="HS", edition="2022", licence_class="restricted", publish_codes=False)
wd = ClassificationScheme.objects.create(key="wikidata", name="Wikidata", licence_class="open", publish_codes=True)


@check("test_exact_match_unique_per_concept_and_scheme")
def _():
    c = mk("XW node", 3, [gloves])
    now = timezone.now()
    ConceptCrosswalk.objects.create(concept=c, scheme=wd, code="Q1", relation="exact", state="approved", approved_by_id=1, approved_at=now)
    raises(IntegrityError, lambda: ConceptCrosswalk.objects.create(concept=c, scheme=wd, code="Q2", relation="exact", state="approved", approved_by_id=1, approved_at=now))
    ConceptCrosswalk.objects.create(concept=c, scheme=wd, code="Q3", relation="broad", state="approved", approved_by_id=1, approved_at=now)  # allowed
    ConceptCrosswalk.objects.create(concept=c, scheme=wd, code="Q4", relation="exact", state="proposed")  # proposals may compete


@check("test_exact_code_belongs_to_one_concept")
def _():
    a, b = mk("XW a", 3, [gloves]), mk("XW b", 3, [gloves])
    now = timezone.now()
    ConceptCrosswalk.objects.create(concept=a, scheme=wd, code="Q10", relation="exact", state="approved", approved_by_id=1, approved_at=now)
    raises(IntegrityError, lambda: ConceptCrosswalk.objects.create(concept=b, scheme=wd, code="Q10", relation="exact", state="approved", approved_by_id=1, approved_at=now))
    ConceptCrosswalk.objects.create(concept=b, scheme=wd, code="Q10", relation="narrow", state="approved", approved_by_id=1, approved_at=now)


@check("test_approved_requires_approver_db_check")
def _():
    c = mk("XW approver", 3, [gloves])
    raises(IntegrityError, lambda: ConceptCrosswalk.objects.create(concept=c, scheme=wd, code="Q20", relation="close", state="approved"))


@check("test_confidence_range_db_check")
def _():
    c = mk("XW conf", 3, [gloves])
    raises(IntegrityError, lambda: ConceptCrosswalk.objects.create(concept=c, scheme=wd, code="Q30", relation="close", confidence=1.5))


@check("test_scheme_without_publish_flag_hides_codes")
def _():
    c = mk("XW publish", 3, [gloves])
    now = timezone.now()
    ConceptCrosswalk.objects.create(concept=c, scheme=hs, code="420321", relation="broad", state="approved", approved_by_id=1, approved_at=now)
    ConceptCrosswalk.objects.create(concept=c, scheme=wd, code="Q40", relation="exact", state="approved", approved_by_id=1, approved_at=now)
    ConceptCrosswalk.objects.create(concept=c, scheme=wd, code="Q41", relation="close", state="proposed")
    shown = {(x.scheme.key, x.code) for x in crosswalk.published_codes(c)}
    assert shown == {("wikidata", "Q40")}


@check("test_unmapped_review_row_is_unique_and_cleared_by_approval")
def _():
    c = mk("XW review", 3, [gloves])
    CrosswalkReview.objects.create(concept=c, scheme=hs, outcome="none_exists")
    raises(IntegrityError, lambda: CrosswalkReview.objects.create(concept=c, scheme=hs, outcome="deferred"))
    cw = crosswalk.propose(c, hs, "999999", "narrow", confidence=0.4)
    crosswalk.approve(cw, by_id=7)
    assert not CrosswalkReview.objects.filter(concept=c, scheme=hs).exists()


@check("test_backfill_maps_old_system_to_scheme")
def _():
    # rows written the old way: system and match_type only; the data migration has a function we can call again
    c = mk("XW legacy", 3, [gloves])
    old = ConceptCrosswalk.objects.create(concept=c, system="foursquare", code="13065", match_type="exact", scheme=None, state="proposed")
    import importlib

    from django.apps import apps as django_apps

    importlib.import_module("taxonomy.migrations.0005_backfill_graph").backfill_schemes(django_apps)
    old.refresh_from_db()
    assert old.scheme.key == "foursquare" and old.relation == "exact" and old.state == "approved"


# --------------------------------------------------------------------------- D4 facets
material = FacetDef.objects.create(key="material", label_key="f.material", kind="multi_enum", scope="product", max_values_per_entry=3)
process = FacetDef.objects.create(key="process", label_key="f.process", kind="multi_enum", scope="product")
tannage = FacetDef.objects.create(key="tannage", label_key="f.tannage", kind="enum", scope="product")
for f, node in ((material, root), (process, root), (tannage, leather)):
    FacetApplicability.objects.create(facet=f, concept=node)
v = {}
for f, slugs_ in ((material, ["goatskin", "cowhide", "synthetic-leather"]), (process, ["hand-stitched", "thermally-bonded"]), (tannage, ["chrome", "vegetable"])):
    for s in slugs_:
        v[s] = FacetValue.objects.create(facet=f, slug=s, label_key=f"v.{s}")
v["fifa-pro"] = FacetValue.objects.create(facet=FacetDef.objects.create(key="cert", label_key="f.cert", kind="multi_enum"), slug="fifa-quality-pro", label_key="v.fifa", only_under=football_gloves)
FacetApplicability.objects.create(facet=v["fifa-pro"].facet, concept=root)
FacetRule.objects.create(kind="forbid", value_a=v["thermally-bonded"], value_b=v["goatskin"])
FacetRule.objects.create(kind="require", value_a=v["chrome"], value_b=v["cowhide"])


@check("test_facet_not_applicable_outside_subtree")
def _():
    assert facets.validate_facet_values(cricket_gloves, {"tannage": ["chrome"], "material": ["cowhide"]}) == []  # leather subtree
    pr = facets.validate_facet_values(prot, {"tannage": ["vegetable"]})  # sports subtree, not leather
    assert pr and "does not apply" in pr[0][1]


@check("test_value_only_under_node")
def _():
    assert facets.validate_facet_values(football_gloves, {"cert": ["fifa-quality-pro"]}) == []
    assert facets.validate_facet_values(sports_gloves, {"cert": ["fifa-quality-pro"]})


@check("test_forbid_rule_blocks_combination")
def _():
    assert facets.validate_facet_values(sports_gloves, {"process": ["thermally-bonded"], "material": ["goatskin"]})
    assert facets.validate_facet_values(sports_gloves, {"process": ["thermally-bonded"], "material": ["cowhide"]}) == []


@check("test_require_rule_demands_other_facet")
def _():
    assert facets.validate_facet_values(sports_gloves, {"tannage": ["chrome"]})  # chrome needs a material value (cowhide)
    assert facets.validate_facet_values(sports_gloves, {"tannage": ["chrome"], "material": ["cowhide"]}) == []


@check("test_enum_single_value")
def _():
    assert facets.validate_facet_values(sports_gloves, {"tannage": ["chrome", "vegetable"], "material": ["cowhide"]})


@check("test_child_cap_blocks_81st_listable_child")
def _():
    parent = mk("Cap parent", 2, [leather])
    for i in range(facets.MAX_LISTABLE_CHILDREN):
        mk(f"cap child {i}", 3, [parent])
    raises(facets.FacetError, lambda: facets.check_child_cap(parent))


@check("test_facet_values_filter_list_page")
def _():
    EntryFacet.objects.create(entry=e1, concept=None, facet=material, value=v["goatskin"])
    EntryFacet.objects.create(entry=e5, concept=None, facet=material, value=v["cowhide"])
    raises(IntegrityError, lambda: EntryFacet.objects.create(entry=e1, concept=None, facet=material, value=v["goatskin"]))  # nulls not distinct
    ids = lists.member_rows(world, gloves).filter(entry__facet_values__value=v["goatskin"]).values_list("entry_id", flat=True)
    assert set(ids) == {e1.pk}


@check("test_seed_has_no_node_over_cap")
def _():
    seed = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "01_manufacturing_seed.csv")
    rows = list(csv.DictReader(open(seed, encoding="utf-8")))
    kids = {}
    for r in rows:
        if r["parent_id"]:
            kids[r["parent_id"]] = kids.get(r["parent_id"], 0) + 1
    assert max(kids.values()) <= facets.WARN_LISTABLE_CHILDREN, max(kids.values())


# --------------------------------------------------------------------------- D6 store rule and virtual empty pages
@check("test_should_store_rule_table")
def _():
    assert should_store(25, 0, False, False) and not should_store(24, 9, False, False)
    assert should_store(0, 10, False, False)
    assert should_store(1, 0, True, False)  # pinned
    assert should_store(22, 0, False, True) and not should_store(19, 7, False, True)  # hysteresis
    assert not should_store(22, 0, False, False)


def _bulk(place, concept, n, verified=0):
    for i in range(n):
        e = make_entry(f"bulk {place.slug} {concept.slug} {i}", place, concept)
        if i < verified:
            Entry.objects.filter(pk=e.pk).update(last_verified_at=timezone.now())
            EntryConcept.objects.filter(entry=e).update(best_level=1)


tiny = mk("Store tiny", 3, [sports_gloves.parent or gloves])  # 24 members
mid = mk("Store mid", 3, [gloves])  # 25 members
ver = mk("Store verified", 3, [gloves])  # 10 verified, 12 members
pin = mk("Store pinned", 3, [gloves])  # 1 member, pinned
empty = mk("Store empty", 3, [gloves])
_bulk(lahore, tiny, 24)
_bulk(lahore, mid, 25)
_bulk(lahore, ver, 12, verified=10)
_bulk(lahore, pin, 1)
PlaceList.objects.create(place=lahore, concept=pin, reason="sponsored")
recount.recount_country("PK")


def cell(place, concept):
    return RollupCell.objects.filter(country_code="PK", place_path=place.path, concept=concept).first()


@check("test_recount_stores_cell_at_25_and_not_at_24")
def _():
    assert cell(lahore, mid) and cell(lahore, mid).published == 25
    assert cell(lahore, tiny) is None


@check("test_recount_stores_cell_at_10_verified")
def _():
    c = cell(lahore, ver)
    assert c and c.verified == 10 and c.published == 12


@check("test_pinned_cell_stored_when_small")
def _():
    c = cell(lahore, pin)
    assert c and c.pinned and c.published == 1


@check("test_recount_rolls_up_to_every_place_and_node_above")
def _():
    for p in (punjab, pk, world):
        c = cell(p, mid)
        assert c and c.published == 25, (p.path, c)
    assert cell(world, gloves).published >= 25 + 12 + 1 + 24 - 24  # tiny is below the rule at node level but counts toward gloves


@check("test_recount_equals_bruteforce")
def _():
    # recount the stored cells again by brute force from Entry rows and compare
    for c in RollupCell.objects.filter(country_code="PK"):
        nodes = set(closure.descendant_ids(c.concept_id))
        ids = set()
        for m in EntryConcept.objects.filter(concept_id__in=nodes, state=2, listable=True):
            if not c.place_path or m.place_path == c.place_path or m.place_path.startswith(c.place_path + "."):
                ids.add(m.entry_id)
        assert len(ids) == c.published, (c.place_path, c.concept_id, len(ids), c.published)


@check("test_hysteresis_keeps_cell_at_22_drops_at_19")
def _():
    drop = mk("Store hyst", 3, [gloves])
    _bulk(karachi, drop, 25)
    recount.recount_country("PK")
    assert cell(karachi, drop)
    for e in Entry.objects.filter(name__startswith=f"bulk {karachi.slug} {drop.slug}")[:3]:
        Entry.objects.filter(pk=e.pk).update(publish_state="draft")
        e.refresh_from_db()
        mb.sync_entry_concepts(e)
    recount.recount_country("PK")
    assert cell(karachi, drop) and cell(karachi, drop).published == 22  # kept in the 20 to 24 band
    for e in Entry.objects.filter(name__startswith=f"bulk {karachi.slug} {drop.slug}", publish_state="published")[:3]:
        Entry.objects.filter(pk=e.pk).update(publish_state="draft")
        e.refresh_from_db()
        mb.sync_entry_concepts(e)
    recount.recount_country("PK")
    assert cell(karachi, drop) is None  # 19 < 20


@check("test_database_check_rejects_cell_below_drop_rule")
def _():
    raises(IntegrityError, lambda: RollupCell.objects.create(country_code="PK", place_path="pk.x", concept=empty, total=3, published=3, verified=0))


@check("test_virtual_empty_returns_200_noindex_with_nearest_links")
def _():
    r = lists.resolve_list(karachi, mid)  # mid has members at Lahore, none in Karachi
    assert (r.mode, r.http_status, r.robots, r.in_sitemap) == ("virtual_empty", 200, "noindex,follow", False)
    assert r.nearest["parent_place"] is not None and r.nearest["parent_place"].place_path == "pk"  # same node, higher place
    r2 = lists.resolve_list(lahore, empty)
    assert r2.mode == "virtual_empty" and r2.nearest["parent_nodes"]  # the parent node has members here


@check("test_live_page_for_substore_cell")
def _():
    r = lists.resolve_list(lahore, tiny)
    assert r.mode == "live" and r.count_hint == 24 and r.robots == "noindex,follow" and not r.in_sitemap


@check("test_stored_cell_indexable_only_with_verified_or_pinned")
def _():
    assert lists.resolve_list(lahore, mid).robots == "noindex,follow"  # 25 members but 0 verified
    assert lists.resolve_list(lahore, ver).robots == "index,follow"
    assert lists.resolve_list(lahore, pin).robots == "index,follow"


@check("test_place_total_independent_of_store_rule")
def _():
    recount.recount_place_totals("PK")
    pt = PlaceTotal.objects.get(country_code="PK", place_path=lahore.path)
    n = Entry.objects.filter(place_path__startswith=lahore.path, deleted_at__isnull=True, merged_into__isnull=True).count()
    assert pt.total == n and n > 0
    assert PlaceTotal.objects.get(country_code="PK", place_path="").total >= pt.total
    assert cell(lahore, tiny) is None  # the thin list has no cell, yet the place total counts its entries


@check("test_unknown_slug_or_place_is_404_not_virtual")
def _():
    assert slugs.resolve_slug("no-such-list-type").status == 404



# --------------------------------------------------------------------------- C05 merge and unmerge
@check("test_merge_unions_memberships_into_survivor")
def _():
    a, b = make_entry("Merge A", lahore, sports_gloves), make_entry("Merge B", lahore, football_gloves)
    mb.add_secondary(b, prot, source=EntryConcept.Source.OWNER, evidence_ref=1)
    ev = merge_with_undo(a, b)
    got = {m.concept_id: m.role for m in EntryConcept.objects.filter(entry=a)}
    assert got == {sports_gloves.pk: 1, football_gloves.pk: 2, prot.pk: 2}, got  # the absorbed primary became a secondary
    assert sorted(ev.moved["memberships_added"]) == sorted([football_gloves.pk, prot.pk])


@check("test_merged_entry_leaves_list_pages_and_survivor_appears_once")
def _():
    a, b = make_entry("Merge C", lahore, sports_gloves), make_entry("Merge D", lahore, sports_gloves)
    merge_with_undo(a, b)
    page = [e.pk for e in lists.first_page(lahore, sports_gloves, limit=500)]
    assert a.pk in page and b.pk not in page and page.count(a.pk) == 1


@check("test_unmerge_restores_children_credit_and_memberships")
def _():
    from entries.models import Contact
    from outreach.services import normalized_hash

    a, b = make_entry("Merge E", lahore, sports_gloves), make_entry("Merge F", lahore, football_gloves)
    Contact.objects.create(entry=b, country_code="PK", kind="phone", value_enc="x", value_hash=normalized_hash("phone", "0300111", "PK"))
    ev = merge_with_undo(a, b)
    assert Contact.objects.filter(entry=a).count() == 1 and Contact.objects.filter(entry=b).count() == 0
    unmerge(ev)
    assert Contact.objects.filter(entry=b).count() == 1 and Contact.objects.filter(entry=a).count() == 0
    assert {m.concept_id for m in EntryConcept.objects.filter(entry=a)} == {sports_gloves.pk}
    b.refresh_from_db()
    assert b.merged_into_id is None


@check("test_unmerge_absorbed_returns_to_draft_not_published")
def _():
    a, b = make_entry("Merge G", lahore, sports_gloves), make_entry("Merge H", lahore, sports_gloves)
    ev = merge_with_undo(a, b)
    unmerge(ev)
    b.refresh_from_db()
    assert b.publish_state == "draft" and not EntryConcept.objects.filter(entry=b, listable=True).exists()
    raises(Exception, lambda: unmerge(MergeEvent.objects.get(pk=ev.pk)))  # second undo refused


@check("test_second_applied_merge_of_same_absorbed_rejected_by_database")
def _():
    a, b, c = (make_entry(f"Merge dup {x}", lahore, sports_gloves) for x in "abc")
    merge_with_undo(a, b)
    raises(IntegrityError, lambda: MergeEvent.objects.create(survivor=c, absorbed=b))


# --------------------------------------------------------------------------- C13 closed, moved, renamed
@check("test_agent_signals_never_close_alone")
def _():
    e = make_entry("Signal Ltd", lahore, sports_gloves)
    for k in ("call_unanswered", "website_dead", "source_says_closed"):
        lc.record_signal(e, k)
    lc.recompute_closure_scores()
    e.refresh_from_db()
    assert e.closure_score == 4
    assert lc.suspect_from_scores() >= 1
    e.refresh_from_db()
    assert e.status == "suspected_closed"
    raises(lc.StatusError, lambda: lc.record_status(e, "permanently_closed", "web"))
    lc.record_status(e, "permanently_closed", "surveyor", actor_id=1, evidence="phoned, shop shuttered")
    e.refresh_from_db()
    assert e.status == "permanently_closed"


@check("test_signals_expire_and_score_recomputed")
def _():
    e = make_entry("Old signal", lahore, sports_gloves)
    old = timezone.now() - timedelta(days=lc.SIGNAL_LIFE_DAYS + 5)
    lc.record_signal(e, "source_says_closed", observed_at=old)
    lc.record_signal(e, "call_unanswered")
    lc.recompute_closure_scores()
    e.refresh_from_db()
    assert e.closure_score == 1


@check("test_suspected_status_ranks_below_open_on_list")
def _():
    o, s_ = make_entry("Rank open", karachi, tiny), make_entry("Rank suspect", karachi, tiny)
    lc.record_status(s_, "suspected_closed", "web", evidence="site down")
    page = [e.pk for e in lists.first_page(karachi, tiny)]
    assert page.index(o.pk) < page.index(s_.pk)


@check("test_closed_entry_listed_last_in_grace_then_delisted")
def _():
    o, c = make_entry("Grace open", karachi, football_gloves), make_entry("Grace closed", karachi, football_gloves)
    lc.record_status(c, "permanently_closed", "owner", actor_id=2, observed_at=timezone.now() - timedelta(days=30))
    page = [e.pk for e in lists.first_page(karachi, football_gloves)]
    assert page.index(o.pk) < page.index(c.pk)  # still shown, tagged on the page, ranked last
    Entry.objects.filter(pk=c.pk).update(status_date=(timezone.now() - timedelta(days=95)).date())
    assert lc.sweep_grace() >= 1
    assert c.pk not in [e.pk for e in lists.first_page(karachi, football_gloves)]


@check("test_reopen_needs_human_and_clears_signals")
def _():
    e = make_entry("Reopen", lahore, sports_gloves)
    lc.record_status(e, "permanently_closed", "owner", actor_id=3)
    raises(lc.StatusError, lambda: lc.record_status(e, "open", "web"))
    lc.record_status(e, "open", "owner", actor_id=3)
    e.refresh_from_db()
    assert e.status == "open" and e.closure_score == 0
    assert EntryStatusEvent.objects.filter(entry=e).count() == 2


@check("test_moved_entry_changes_place_lists_and_keeps_history")
def _():
    e = make_entry("Mover 2", lahore, sports_gloves)
    succ = make_entry("Mover 2 new", karachi, sports_gloves)
    lc.record_status(e, "moved", "owner", actor_id=4, successor=succ)
    e.refresh_from_db()
    assert e.moved_to_id == succ.pk and EntryStatusEvent.objects.filter(entry=e, successor_entry_id=succ.pk).exists()


# --------------------------------------------------------------------------- C03 chain versus branch
@check("test_branch_rule_table")
def _():
    cases = [
        # name_sim, same_phone, distance_m, same_address_text, same_brand -> verdict
        (0.98, True, 10, True, False, "duplicate"),
        (0.95, False, 30, False, False, "duplicate"),
        (0.95, True, 4200, False, False, "branch"),
        (0.92, False, 900, False, False, "branch"),
        (0.50, True, 3000, False, False, "shared_phone"),
        (0.40, True, 15, False, False, "different"),
        (0.30, False, 100, False, False, "different"),
        (0.97, False, None, False, False, "review"),
        (0.50, False, 1000, False, True, "branch"),
        (0.75, True, 20, False, False, "duplicate"),
        (0.95, False, 120, False, False, "review"),
    ]
    for ns, ph, d, addr, br, want in cases:
        got = classify_pair(name_sim=ns, same_phone=ph, distance_m=d, same_address_text=addr, same_brand=br)
        assert got == want, (ns, ph, d, addr, br, got, want)
    assert classify_pair(name_sim=0.5, same_phone=True, distance_m=3000, same_address_text=False) != "duplicate"  # the 0.5 + shared phone defect


@check("test_brand_unique_wikidata")
def _():
    Brand.objects.create(name="Chain A", name_fold="chain a", wikidata_id="Q42")
    Brand.objects.create(name="Chain B", name_fold="chain b", wikidata_id="")
    Brand.objects.create(name="Chain C", name_fold="chain c", wikidata_id="")  # blank ids may repeat
    raises(IntegrityError, lambda: Brand.objects.create(name="Chain A2", name_fold="chain a2", wikidata_id="Q42"))


@check("test_branch_counts_once_at_own_place")
def _():
    br = Brand.objects.create(name="Chain Z", name_fold="chain z")
    head = make_entry("Chain Z head", lahore, football_gloves, brand=br)
    b1 = make_entry("Chain Z Karachi", karachi, football_gloves, brand=br, parent_entry=head)
    ids_l = {e.pk for e in lists.first_page(lahore, football_gloves, limit=500)}
    ids_k = {e.pk for e in lists.first_page(karachi, football_gloves, limit=500)}
    assert head.pk in ids_l and head.pk not in ids_k and b1.pk in ids_k and b1.pk not in ids_l
    assert Entry.objects.filter(brand=br).count() == 2

# --------------------------------------------------------------------------- report
width = max(len(n) for n, _, _ in RESULTS)
for name, status, msg in RESULTS:
    print(f"{status}  {name}")
    if status == "FAIL":
        print("      " + msg.replace("\n", "\n      "))
fails = [r for r in RESULTS if r[1] == "FAIL"]
print(f"\n{len(RESULTS) - len(fails)} passed, {len(fails)} failed")
sys.exit(1 if fails else 0)
