import json
import re

import pytest
from django.test import Client

from accounts.roles import grant_role
from entries import services as es
from moderation import privacy
from outreach.models import Suppression


@pytest.fixture
def person(tree, surgical, users, pk_open):
    from taxonomy.models import ListTypeSettings

    ListTypeSettings.objects.filter(concept=surgical).update(is_individual=True)
    e = es.create_entry(
        name="Dr Test Person",
        place=tree["paris"],
        primary_concept=surgical,
        created_by=users["adder"],
        entity_type="person",
        website="https://doc.example",
        contacts=[("phone", "0300 555 1212")],
        addons={"business_type": "trader", "product_categories": ["x"]},
    )
    es.record_consent(e, status="consented", method="web_form", wording_version="v1")
    es.record_verification(
        e, field_group="identity", level="surveyor", actor=users["surveyor"], method="call", evidence="ok"
    )
    es.try_publish(e)
    e.refresh_from_db()
    return e


def _staff(user, role="moderator"):
    grant_role(user, role)
    c = Client()
    c.force_login(user)
    s = c.session
    s["mfa_ok"] = True
    s.save()
    return c


def test_subject_access_names_what_we_hold_but_never_the_value(person):
    rep = privacy.subject_access_report("phone", "+92 300 555 1212", "PK")
    assert len(rep["entries"]) == 1
    row = rep["entries"][0]
    assert row["code"] == person.uid and row["consent"][0]["status"] == "consented"
    text = privacy.subject_access_json(rep)
    # timestamps are digits too and can contain "0300" by chance, so remove them before looking for the number
    text = re.sub(r"\d{4}-\d\d-\d\dT[\d:.+-]+", "", text)
    assert "5551212" not in text and "0300" not in text
    assert privacy.subject_access_report("phone", "+92 300 000 0000", "PK")["entries"] == []


def test_withdrawal_records_takes_down_and_blocks_a_return(person):
    mod = person.created_by  # any user; the rule is the same
    privacy.withdraw_consent(person, actor=mod)
    person.refresh_from_db()
    assert person.publish_state == "suppressed"
    assert person.consents.order_by("-id").first().status == "withdrawn"
    assert Suppression.objects.filter(reason="consent_withdrawn").exists()
    with pytest.raises(es.EntryError):
        es.create_entry(
            name="Again",
            place=person.place,
            primary_concept=person.primary_concept,
            contacts=[("phone", "0300 555 1212")],
        )
    assert es.try_publish(person) == []  # not a draft any more: stays down


def test_staff_pages_and_register(person, users):
    c = _staff(users["mod"])
    assert "Dr Test Person" in c.get("/staff/consent/").content.decode()
    r = c.post("/staff/subject-access/", {"kind": "phone", "value": "03005551212", "country": "PK", "format": "json"})
    assert r.status_code == 200 and json.loads(r.content)["entries"][0]["code"] == person.uid
    c.post(f"/staff/consent/{person.consents.first().pk}/withdraw/")
    person.refresh_from_db()
    assert person.publish_state == "suppressed"
    plain = Client()
    plain.force_login(users["adder"])
    assert plain.get("/staff/subject-access/").status_code in (302, 403)


def test_account_holder_gets_own_data_only(users, entry):
    c = Client()
    c.force_login(users["adder"])
    data = json.loads(c.get("/account/my-data/").content)
    assert data["account"]["username"] == "adder" and data["entries_added"][0]["code"] == entry.uid
    assert "0300" not in json.dumps(data) and "3001234567" not in json.dumps(data)
    assert Client().get("/account/my-data/").status_code == 302
