"""Management commands and production settings, run the way an operator would run them."""

import os
import subprocess
import sys
from io import StringIO
from pathlib import Path

import pytest
from cryptography.fernet import Fernet
from django.core.management import call_command
from django.core.management.base import CommandError
from django.db import connection

from core.models import OpsRecord

BACKEND = Path(__file__).resolve().parents[2]


def run(*args, **kw):
    out = StringIO()
    call_command(*args, stdout=out, **kw)
    return out.getvalue()


def test_record_ops_writes_a_row(db):
    assert "recorded backup" in run("record_ops", "backup", "nightly 1 MB")
    assert OpsRecord.objects.get(kind="backup").detail == "nightly 1 MB"
    with pytest.raises(CommandError):
        run("record_ops", "nonsense")


def test_run_scheduled_runs_due_jobs_and_records_them(db):
    first = run("run_scheduled", "--only", "quota_cleanup", "placement_expiry")
    assert "quota_cleanup:" in first and "placement_expiry:" in first
    assert run("run_scheduled", "--only", "quota_cleanup") == ""  # not due again straight away


def test_send_campaigns_with_nothing_to_send_is_quiet(db):
    assert run("send_campaigns") == ""


def test_seed_commands_are_repeatable(db, settings):
    settings.DEBUG = True
    run("seed_pilot")
    run("seed_taxonomy")
    assert "list types created" in run("seed_taxonomy")
    run("seed_demo_entries")
    from entries.models import Entry

    n = Entry.objects.count()
    assert n >= 6
    run("seed_demo_entries")  # a second run does not duplicate the demo entries
    assert Entry.objects.count() == n


def test_seed_demo_entries_refuses_outside_debug(db, settings):
    settings.DEBUG = False
    with pytest.raises(CommandError):
        run("seed_demo_entries")


def test_audit_sample_command_needs_place_and_type_for_canaries(db, tree, surgical):
    assert "0 audit tasks queued" in run("seed_audit_sample")
    with pytest.raises(CommandError):
        run("seed_audit_sample", "--canaries", "2")
    out = run("seed_audit_sample", "--canaries", "2", "--place", tree["paris"].path, "--type", surgical.slug)
    assert "2 canaries planted" in out


def test_load_data_all_modes(db, tmp_path):
    ci = tmp_path / "countryInfo.txt"
    ci.write_text(
        "\t".join(
            [
                "PK",
                "PAK",
                "586",
                "PK",
                "Pakistan",
                "Islamabad",
                "796095",
                "240000000",
                "AS",
                ".pk",
                "PKR",
                "Rupee",
                "92",
                "",
                "",
                "ur",
                "1168579",
            ]
        )
    )
    a1 = tmp_path / "admin1.txt"
    a1.write_text("PK.04\tPunjab\tPunjab\t1168883\n")
    places = tmp_path / "PK.txt"
    cols = [
        "1176639",
        "Sialkot",
        "Sialkot",
        "",
        "32.5",
        "74.5",
        "P",
        "PPL",
        "PK",
        "",
        "04",
        "",
        "",
        "",
        "655852",
        "",
        "",
        "Asia/Karachi",
        "",
    ]
    places.write_text("\t".join(cols))
    out = run(
        "load_data",
        "geonames",
        "--country",
        "PK",
        "--country-info",
        str(ci),
        "--admin1",
        str(a1),
        "--places",
        str(places),
    )
    assert "'cities': 1" in out
    tax = tmp_path / "cats.csv"
    tax.write_text(
        "kind,slug,name,language,parent_slug,synonyms\nlist_type,petrol-pumps,Petrol pumps,en,,gas station\n"
    )
    assert "'created': 1" in run("load_data", "taxonomy", "--scheme", "own", "--file", str(tax))
    div = tmp_path / "div.jsonl"
    div.write_text('{"id":"c1","subtype":"country","country":"PK","names":{"primary":"Pakistan"}}\n')
    assert "created" in run("load_data", "overture-divisions", "--country", "PK", "--file", str(div))
    with pytest.raises(CommandError, match="file not found"):
        run("load_data", "taxonomy", "--scheme", "own", "--file", str(tmp_path / "missing.csv"))
    with pytest.raises(CommandError):
        run("load_data", "taxonomy", "--file", str(tax))  # scheme missing
    with pytest.raises(CommandError):
        run("load_data", "geonames")  # files missing
    with pytest.raises(CommandError):
        run(
            "load_data",
            "places",
            "--file",
            str(tax),
            "--source",
            "No such source",
            "--country",
            "PK",
            "--scheme",
            "own",
        )


def test_load_data_places_refuses_a_source_that_may_not_be_imported(db, tmp_path, tree):
    from intake.models import Source

    Source.objects.create(name="Blocked", tier="red", allowed_uses=[])
    f = tmp_path / "p.csv"
    f.write_text("id,name,lat,lon,category\n1,X,32.5,74.5,cafe\n")
    with pytest.raises(CommandError, match="gate refused"):
        run("load_data", "places", "--file", str(f), "--source", "Blocked", "--country", "PK", "--scheme", "own")


def test_db_roles_command_prints_and_checks(pg):
    out = run("db_roles")
    assert 'GRANT SELECT, INSERT ON "core_auditlog"' in out and 'REVOKE ALL ON "entries_contact"' in out
    assert "UPDATE" not in "".join(ln for ln in out.splitlines() if "core_auditlog" in ln and ln.startswith("GRANT"))
    with connection.cursor() as cur:
        cur.execute("select rolsuper or rolcreaterole from pg_roles where rolname = current_user")
        can = cur.fetchone()[0]
    with pytest.raises(CommandError, match="does not exist"):
        run("db_roles", "--check", "--app-role", "no_such_role_here")
    if can:
        with connection.cursor() as cur:
            for r in ("al_chk_app", "al_chk_ro"):
                cur.execute(f"drop role if exists {r}")
                cur.execute(f"create role {r}")
        try:
            with connection.cursor() as cur:
                cur.execute("grant all on core_auditlog to al_chk_app")  # too much on purpose
            with pytest.raises(CommandError, match="append-only"):
                run("db_roles", "--check", "--app-role", "al_chk_app", "--readonly-role", "al_chk_ro")
            run("db_roles", "--apply", "--app-role", "al_chk_app", "--readonly-role", "al_chk_ro")
            assert "as designed" in run(
                "db_roles", "--check", "--app-role", "al_chk_app", "--readonly-role", "al_chk_ro"
            )
        finally:
            with connection.cursor() as cur:
                for r in ("al_chk_app", "al_chk_ro"):
                    cur.execute(f"drop owned by {r}")
                    cur.execute(f"drop role if exists {r}")


# ---- production settings, in a fresh process (settings are read once at start) ------------------------------------------------


def prod_env(**extra):
    env = {
        "PATH": os.environ["PATH"],
        "HOME": os.environ.get("HOME", "/tmp"),
        "DJANGO_SETTINGS_MODULE": "config.settings.prod",
    }
    env.update(extra)
    return env


def run_prod(code, **env):
    return subprocess.run(
        [sys.executable, "-c", code], cwd=BACKEND, env=prod_env(**env), capture_output=True, text=True, timeout=120
    )


GOOD = {
    "DJANGO_SECRET_KEY": "Zq7!vK2#mP9xRt4$Lw8&Ye3^Nc6*Bd1@Hf5%Gs0(Ju2)Ia9-Oo7_Ty4+Xr6=",
    "DJANGO_ALLOWED_HOSTS": "alllists.org",
    "CONTACT_HASH_PEPPER": "p" * 32,
    "FIELD_ENCRYPTION_ACTIVE_KEY": "k1",
}


def good_env():
    return {**GOOD, "FIELD_ENCRYPTION_KEYS": "k1:" + Fernet.generate_key().decode()}


def test_production_refuses_to_start_without_its_secrets():
    for missing in ("DJANGO_SECRET_KEY", "CONTACT_HASH_PEPPER", "FIELD_ENCRYPTION_ACTIVE_KEY"):
        env = good_env()
        env.pop(missing)
        r = run_prod("import django; django.setup()", **env)
        assert r.returncode != 0 and "ImproperlyConfigured" in r.stderr, missing
    env = good_env()
    del env["FIELD_ENCRYPTION_KEYS"]
    assert run_prod("import django; django.setup()", **env).returncode != 0


def test_production_refuses_debug_mode():
    r = run_prod("import django; django.setup()", DJANGO_DEBUG="1", **good_env())
    assert r.returncode != 0 and "DEBUG" in r.stderr


def test_production_deploy_check_is_clean_and_https_is_enforced():
    code = (
        "import django; django.setup();"
        "from django.core import checks;"
        "ids = {m.id for m in checks.run_checks(include_deployment_checks=True)};"
        "assert ids <= {'security.W005', 'security.W021'}, ids;"  # include-subdomains and preload are left off on purpose
        "from django.conf import settings as s;"
        "assert s.SECURE_SSL_REDIRECT and s.SESSION_COOKIE_SECURE and s.CSRF_COOKIE_SECURE and s.SECURE_HSTS_SECONDS >= 86400;"
        "assert not s.DEBUG and not s.DEMO_MODE;"
        "print('ok')"
    )
    r = run_prod(code, **good_env())
    assert r.returncode == 0 and "ok" in r.stdout, r.stderr[-800:]


def test_production_redirects_http_to_https_but_serves_health_check():
    code = (
        "import django; django.setup();"
        "from django.test import Client;"
        "c = Client(HTTP_HOST='alllists.org');"
        "r = c.get('/about/'); assert r.status_code == 301 and r['Location'].startswith('https://'), r.status_code;"
        "r = c.get('/about/', HTTP_X_FORWARDED_PROTO='https'); assert r.status_code in (200, 500), r.status_code;"
        "r = c.get('/healthz'); assert r.status_code in (200, 503), r.status_code;"
        "print('ok')"
    )
    r = run_prod(
        code,
        POSTGRES_DB="alllists_nonexistent_for_test",
        POSTGRES_USER="x",
        POSTGRES_PASSWORD="x",
        POSTGRES_HOST="127.0.0.1",
        **good_env(),
    )
    assert "ok" in r.stdout, r.stdout + r.stderr[-800:]


def test_production_requires_the_active_key_to_be_one_of_the_keys():
    env = good_env()
    env["FIELD_ENCRYPTION_ACTIVE_KEY"] = "k9"
    r = run_prod("import django; django.setup()", **env)
    assert r.returncode != 0 and "ACTIVE_KEY" in r.stderr


def test_production_pages_work_even_if_collectstatic_was_never_run(tmp_path):
    code = (
        "import django; django.setup();"
        "from django.conf import settings; settings.STATIC_ROOT = %r;"
        "from django.templatetags.static import static;"
        "print(static('catalog/app.css'))"
    ) % str(tmp_path / "empty")
    r = run_prod(code, **good_env())
    assert r.returncode == 0 and r.stdout.strip() == "/static/catalog/app.css", r.stderr[-600:]
