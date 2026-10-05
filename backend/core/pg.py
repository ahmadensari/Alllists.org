"""Helpers for PostgreSQL-only parts of migrations. SQLite (local demo) skips them."""
from django.db import migrations


def only_postgres(forward_sql, reverse_sql=""):
    def forward(apps, schema_editor):
        if schema_editor.connection.vendor == "postgresql":
            schema_editor.execute(forward_sql, params=None)

    def reverse(apps, schema_editor):
        if reverse_sql and schema_editor.connection.vendor == "postgresql":
            schema_editor.execute(reverse_sql, params=None)

    return migrations.RunPython(forward, reverse)


FORBID_FN = """
CREATE OR REPLACE FUNCTION forbid_mutation() RETURNS trigger AS $$
BEGIN
  RAISE EXCEPTION 'table % is append-only: % is not allowed', TG_TABLE_NAME, TG_OP
    USING ERRCODE = 'integrity_constraint_violation';
END;
$$ LANGUAGE plpgsql;
"""
DROP_FORBID_FN = "DROP FUNCTION IF EXISTS forbid_mutation();"


def append_only(table):
    return only_postgres(
        f"CREATE TRIGGER {table}_append_only BEFORE UPDATE OR DELETE ON {table} "
        "FOR EACH ROW EXECUTE FUNCTION forbid_mutation();",
        f"DROP TRIGGER IF EXISTS {table}_append_only ON {table};")


def trigram_index(table, column, name):
    return only_postgres(
        f"CREATE INDEX {name} ON {table} USING gin ({column} gin_trgm_ops);",
        f"DROP INDEX IF EXISTS {name};")
