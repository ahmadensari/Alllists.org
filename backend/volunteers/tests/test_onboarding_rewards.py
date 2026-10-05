from datetime import timedelta

from django.contrib.auth.models import User
from django.test import Client

from access import services as acs
from accounts.models import Profile
from accounts.roles import grant_role
from analytics.models import Event
from core import clock
from volunteers import onboarding, rewards, services as vs
from volunteers.models import ContributorProfile, Reward

RIGHT = {"contacts": "b", "rights": "a", "independence": "b", "evidence": "a", "people": "a"}


def test_quiz_scores_and_pass_mark(users):
    u = users["surveyor"]
    assert onboarding.score(RIGHT) == 5
    s, passed = onboarding.submit(u, {**RIGHT, "contacts": "a", "people": "b"}, declared_rights=True)
    assert s == 3 and not passed and vs.ensure_profile(u).onboarded_at is None
    s, passed = onboarding.submit(u, {**RIGHT, "people": "b"}, declared_rights=False)
    assert s == 4 and not passed  # the rights box is required even with a good score
    s, passed = onboarding.submit(u, {**RIGHT, "people": "b"}, declared_rights=True)
    assert passed and vs.ensure_profile(u).onboarded_at and vs.ensure_profile(u).declared_rights_at


def test_surveyor_screens_send_the_unprepared_to_onboarding(users):
    grant_role(users["surveyor"], "surveyor")
    c = Client()
    c.force_login(users["surveyor"])
    r = c.get("/account/tasks/")
    assert r.status_code == 302 and r["Location"].endswith("/account/contributor/onboarding/")
    page = c.get("/account/contributor/onboarding/")
    assert page.status_code == 200 and "Before you start" in page.content.decode()
    post = c.post("/account/contributor/onboarding/", {**{f"q_{k}": v for k, v in RIGHT.items()}, "rights": "on"})
    assert post.status_code == 302 and c.get("/account/tasks/").status_code == 200


def test_levels_grant_certificates_once_and_access_credit_from_level_two(entry, users):
    u = users["surveyor"]
    rewards.on_level_change(u, 1, place_path=entry.place_path)
    rewards.on_level_change(u, 1, place_path=entry.place_path)  # repeating changes nothing
    assert Reward.objects.filter(user=u, kind="certificate").count() == 1
    made = rewards.on_level_change(u, 2, place_path=entry.place_path)
    assert {r.kind for r in made} == {"certificate", "access_credit"}
    assert acs.active_scopes(u) and any(s[0] == "pk.punjab.sialkot" for s in acs.active_scopes(u))
    rewards.on_level_change(u, 3, place_path=entry.place_path)
    assert Reward.objects.filter(user=u, kind="access_credit").count() == 1  # only once


def test_completing_tasks_raises_level_and_grants_a_certificate(entry, users):
    u = users["surveyor"]
    prof = vs.ensure_profile(u)
    prof.points = 4
    prof.save()
    t = vs.queue_verification(entry)
    vs_task = vs.take_next_task(u)
    vs.complete_task(vs_task, user=u, outcome="confirmed", evidence="phone answered")
    assert vs.ensure_profile(u).level == 1 and Reward.objects.filter(user=u, kind="certificate").count() == 1
    assert t


def test_certificate_page_is_private_but_verification_is_public(users):
    u = users["surveyor"]
    rewards.on_level_change(u, 1)
    r = Reward.objects.get(user=u, kind="certificate")
    owner, other = Client(), Client()
    owner.force_login(u)
    other.force_login(users["adder"])
    assert owner.get(f"/account/certificates/{r.pk}/").status_code == 200
    assert other.get(f"/account/certificates/{r.pk}/").status_code == 404
    anon = Client().get(f"/certificate/{r.code}/")
    assert anon.status_code == 200 and "A contributor" in anon.content.decode()
    assert Client().get("/certificate/NOPE/").status_code == 404
    vs.ensure_profile(u)
    ContributorProfile.objects.filter(user=u).update(show_credit=True)
    Profile.objects.update_or_create(user=u, defaults={"display_name": "Sana K"})
    assert "Sana K" in Client().get(f"/certificate/{r.code}/").content.decode()


def test_visible_credit_only_when_opted_in_checked_and_not_a_person(entry, users):
    adder = users["adder"]
    assert rewards.credit_line(entry) is None  # unchecked draft: credit not eligible
    from entries import services as es
    from entries.models import CreditEvent

    es.record_verification(
        entry, field_group="identity", level="surveyor", actor=users["surveyor"], method="call", evidence="ok"
    )
    CreditEvent.objects.filter(entry=entry, kind="added").update(eligible=True)
    assert rewards.credit_line(entry) is None  # contributor has not opted in
    vs.ensure_profile(adder)
    ContributorProfile.objects.filter(user=adder).update(show_credit=True)
    Profile.objects.update_or_create(user=adder, defaults={"display_name": "Adeel R"})
    assert rewards.credit_line(entry) == "Adeel R"
    entry.entity_type = "person"
    assert rewards.credit_line(entry) is None


def test_ref_visits_are_counted_once_a_day_per_visitor_and_only_for_real_codes(users):
    prof = vs.ensure_profile(users["adder"])
    c = Client()
    for _ in range(3):
        assert c.get(f"/_f/ref/?ref={prof.ref_code}&path=/pk/").status_code == 204
    assert Event.objects.filter(name="ref_visit", props__ref=prof.ref_code).count() == 1
    Client().get(f"/_f/ref/?ref={prof.ref_code}&path=/pk/")  # a different visitor address counts again
    c.get("/_f/ref/?ref=deadbeef&path=/")
    c.get("/_f/ref/?ref=<script>&path=/")
    assert (
        Event.objects.filter(name="ref_visit").count() >= 1 and not Event.objects.filter(props__ref="deadbeef").exists()
    )
    me = Client()
    me.force_login(users["adder"])
    assert "Visits that arrived through your link" in me.get("/account/contributor/").content.decode()
    assert timedelta and clock and User
