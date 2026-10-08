import pytest
from django.db import connection
from django.db.utils import ProgrammingError

from core import dbroles

pytestmark = pytest.mark.django_db(transaction=True)


def _superuser():
    with connection.cursor() as cur:
        cur.execute("select rolsuper or rolcreaterole from pg_roles where rolname = current_user")
        return cur.fetchone()[0]


def _drop(cur):
    for r in ("al_test_app", "al_test_ro"):
        cur.execute(f"drop owned by {r}")
        cur.execute(f"drop role if exists {r}")


@pytest.fixture
def roles(pg):
    if not _superuser():
        pytest.skip("needs a database user that can create roles")
    with connection.cursor() as cur:
        for r in ("al_test_app", "al_test_ro"):
            cur.execute("select 1 from pg_roles where rolname = %s", [r])
            if cur.fetchone():
                _drop(cur)
        cur.execute("create role al_test_app")
        cur.execute("create role al_test_ro")
        for s in dbroles.grants_sql("al_test_app", "al_test_ro"):
            cur.execute(s)
    yield
    with connection.cursor() as cur:
        cur.execute("reset role")
        _drop(cur)


def test_app_role_cannot_change_append_only_tables_and_readonly_cannot_read_sensitive(roles):
    rep = dbroles.privilege_report("al_test_app")
    for t in dbroles.APPEND_ONLY:
        if t in rep:
            assert rep[t]["SELECT"] and rep[t]["INSERT"], t
            assert not (rep[t]["UPDATE"] or rep[t]["DELETE"] or rep[t]["TRUNCATE"]), t
    ro = dbroles.privilege_report("al_test_ro")
    for t in dbroles.SENSITIVE:
        if t in ro:
            assert not ro[t]["SELECT"], t
    assert ro["core_auditlog"]["SELECT"] and not ro["core_auditlog"]["INSERT"]


def test_a_real_update_is_refused_by_the_database(roles):
    with connection.cursor() as cur:
        cur.execute("set role al_test_app")
        with pytest.raises(ProgrammingError):
            cur.execute("update core_auditlog set action = 'x'")
        cur.execute("reset role")
