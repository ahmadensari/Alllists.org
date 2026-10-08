from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import Client

from accounts.roles import grant_role
from volunteers import services as vs
from volunteers.models import AuditSample, CanaryEntry, Task


def surveyor(name):
    u = User.objects.create_user(name, f"{name}@x.org", "x")
    grant_role(u, "surveyor")
    return u


def test_audit_sample_picks_published_entries_once_and_never_the_original_verifier(
    db, tree, surgical, make_published, users
):
    for i in range(6):
        make_published(f"Audit {i} Works", tree["paris"], phone=f"0305 000 000{i}", refresh=False)
    assert vs.queue_audit_sample(4, seed=1) == 4
    assert vs.queue_audit_sample(10, seed=2) == 2  # only unsampled entries are queued again
    assert vs.queue_audit_sample(10, seed=3) == 0
    original = users["surveyor"]  # verified every entry
    grant_role(original, "surveyor")
    assert vs.take_next_task(original) is None  # audits never go to the person who verified
    other = surveyor("auditor")
    t = vs.take_next_task(other)
    assert t and t.field_group == "audit"


def test_audit_results_measure_accuracy_and_record_no_new_check(db, tree, surgical, make_published, users):
    e1 = make_published("Right Works", tree["paris"], phone="0305 111 0001", refresh=False)
    e2 = make_published("Wrong Works", tree["paris"], phone="0305 111 0002", refresh=False)
    vs.queue_audit_sample(5, seed=1)
    a = surveyor("auditor2")
    before = {e.pk: e.verification_events.count() for e in (e1, e2)}
    for _ in range(2):
        t = vs.take_next_task(a)
        outcome = "confirmed" if t.entry_id == e1.pk else "wrong"
        vs.complete_task(t, user=a, outcome=outcome, evidence="rechecked" if outcome == "confirmed" else "", minutes=2)
    assert {e.pk: e.verification_events.count() for e in (e1, e2)} == before
    acc = vs.accuracy_by_verifier()
    assert acc[users["surveyor"].pk][:2] == (2, 1) and acc[users["surveyor"].pk][2] == 0.5
    assert (
        AuditSample.objects.filter(correct=True).count() == 1 and AuditSample.objects.filter(correct=False).count() == 1
    )


def test_audit_closed_outcome_closes_the_entry(db, tree, surgical, make_published):
    e = make_published("Shut Works", tree["paris"], phone="0305 222 0001")
    vs.queue_audit_sample(1, seed=1)
    a = surveyor("auditor3")
    t = vs.take_next_task(a)
    vs.complete_task(t, user=a, outcome="closed", evidence="Shop shuttered", minutes=3)
    e.refresh_from_db()
    assert e.status == "permanently_closed"


def test_canaries_are_hidden_fake_drafts_and_never_audited(db, tree, surgical, make_published):
    made = vs.plant_canaries(tree["paris"], surgical, 3)
    assert len(made) == 3 and all(e.publish_state == "draft" for e in made)
    assert CanaryEntry.objects.count() == 3 and Task.objects.filter(canary=True).count() == 3
    make_published("Real Works", tree["paris"], phone="0305 333 0001")
    assert vs.queue_audit_sample(10, seed=1) == 1  # canaries are not in the sample (they are not published)
    trace = vs.plant_canaries(tree["paris"], surgical, 1, purpose="trace")
    assert CanaryEntry.objects.get(entry=trace[0]).purpose == "trace" and Task.objects.filter(canary=True).count() == 3


def test_staff_command_queues_samples_and_canaries(db, tree, surgical, make_published, capsys):
    make_published("Real Works", tree["paris"], phone="0305 444 0001")
    call_command(
        "seed_audit_sample",
        "--size",
        "5",
        "--canaries",
        "2",
        "--place",
        "pk.punjab.sialkot",
        "--type",
        "surgical-instrument-makers",
    )
    out = capsys.readouterr().out
    assert "1 audit tasks queued" in out and "2 canaries planted" in out


def test_agents_staff_page_shows_caps_and_accuracy(db, settings):
    settings.AI_DAILY_CAP_MINOR, settings.AI_MONTHLY_CAP_MINOR = 100, 1000
    u = User.objects.create_user("modag", "m@x.org", "x")
    grant_role(u, "moderator")
    c = Client()
    c.force_login(u)
    s = c.session
    s["mfa_ok"] = True
    s.save()
    html = c.get("/staff/agents/").content.decode()
    assert "Kill switch: off" in html and "Today 0/100" in html and "no audits yet" in html
