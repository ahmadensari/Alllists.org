"""Print (default) or apply the grants for the application and read-only roles. Run as the database owner:
`python manage.py db_roles --print > grants.sql` then review, or `--apply`. The roles themselves are created by
deploy/db_roles.sql with passwords from the secret store."""

from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from core import dbroles


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--app-role", default="alllists_app")
        parser.add_argument("--readonly-role", default="alllists_readonly")
        parser.add_argument("--apply", action="store_true")
        parser.add_argument("--check", action="store_true", help="fail if the app role can change an append-only table")

    def handle(self, *a, **o):
        if connection.vendor != "postgresql":
            raise CommandError("PostgreSQL only")
        if o["check"]:
            with connection.cursor() as cur:
                for role in (o["app_role"], o["readonly_role"]):
                    cur.execute("select 1 from pg_roles where rolname = %s", [role])
                    if not cur.fetchone():
                        raise CommandError(f"role {role!r} does not exist; create it with deploy/db_roles.sql first")
            rep = dbroles.privilege_report(o["app_role"])
            bad = [
                t for t in dbroles.APPEND_ONLY if t in rep and any(rep[t][p] for p in ("UPDATE", "DELETE", "TRUNCATE"))
            ]
            leak = [
                t
                for t in dbroles.SENSITIVE
                if t in dbroles.privilege_report(o["readonly_role"])
                and dbroles.privilege_report(o["readonly_role"])[t]["SELECT"]
            ]
            if bad or leak:
                raise CommandError(
                    f"append-only tables the app can change: {bad}; sensitive tables the read-only role can read: {leak}"
                )
            self.stdout.write("grants are as designed")
            return
        stmts = dbroles.grants_sql(o["app_role"], o["readonly_role"])
        if not o["apply"]:
            self.stdout.write(";\n".join(stmts) + ";")
            return
        with connection.cursor() as cur:
            for s in stmts:
                cur.execute(s)
        self.stdout.write(f"applied {len(stmts)} statements")
