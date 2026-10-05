"""Database roles and grants (plan P3.18). The application role may insert into the append-only tables but never update,
delete or truncate them; the read-only role (analysts, replicas, reports) cannot read the sensitive tables at all.

`grants_sql()` builds the statements from the live catalogue so a new table is covered the next time it runs."""

from django.db import connection

APPEND_ONLY = [
    "core_auditlog",
    "core_changelog",
    "entries_verificationevent",
    "entries_consentrecord",
    "entries_mergemap",
    "entries_creditevent",
    "ledger_ledgertxn",
    "ledger_ledgerposting",
    "billing_payment",
    "billing_invoice",
]
# Tables holding encrypted or secret values. Nobody but the application role can read them.
SENSITIVE = [
    "entries_contact",
    "outreach_claimotp",
    "outreach_enquiry",
    "outreach_optin",
    "outreach_outboxmessage",
    "outreach_message",
    "ledger_payoutprofile",
    "accounts_totpdevice",
    "accounts_recoverycode",
    "accounts_emailtoken",
    "accounts_loginattempt",
    "moderation_report",
    "auth_user",
    "django_session",
]


def _q(name):
    return '"' + name.replace('"', '""') + '"'


def existing_tables():
    with connection.cursor() as cur:
        cur.execute("select tablename from pg_tables where schemaname = 'public' order by tablename")
        return [r[0] for r in cur.fetchall()]


def grants_sql(app_role="alllists_app", readonly_role="alllists_readonly"):
    """Return the list of SQL statements. Roles must already exist (the script creates them with passwords)."""
    tables = existing_tables()
    out = [
        f"GRANT USAGE ON SCHEMA public TO {_q(app_role)}, {_q(readonly_role)}",
        f"GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO {_q(app_role)}",
    ]
    for t in tables:
        if t in APPEND_ONLY:
            out.append(f"REVOKE ALL ON {_q(t)} FROM {_q(app_role)}")
            out.append(f"GRANT SELECT, INSERT ON {_q(t)} TO {_q(app_role)}")
        else:
            out.append(f"GRANT SELECT, INSERT, UPDATE, DELETE ON {_q(t)} TO {_q(app_role)}")
        if t in SENSITIVE:
            out.append(f"REVOKE ALL ON {_q(t)} FROM {_q(readonly_role)}")
        else:
            out.append(f"GRANT SELECT ON {_q(t)} TO {_q(readonly_role)}")
    return out


def privilege_report(role):
    """{table: {privilege: bool}} for the append-only and sensitive tables, as the database sees it."""
    out = {}
    with connection.cursor() as cur:
        for t in APPEND_ONLY + SENSITIVE:
            if t not in existing_tables():
                continue
            row = {}
            for priv in ("SELECT", "INSERT", "UPDATE", "DELETE", "TRUNCATE"):
                cur.execute("select has_table_privilege(%s, %s, %s)", [role, t, priv])
                row[priv] = cur.fetchone()[0]
            out[t] = row
    return out
