"""Write the SQL of every migration in the project (Django `sqlmigrate`, read-only; needs a database connection but changes
nothing) to lint_out/<app>__<name>.sql so squawk can read it.
Run: PYTHONDONTWRITEBYTECODE=1 DJANGO_ALLOW_TEST_KEY=1 POSTGRES_DB=bench_django .venv/bin/python lint_real_migrations.py [out_dir]
"""
import io
import os
import sys

BACKEND = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend"))
sys.path.insert(0, BACKEND)
os.chdir(BACKEND)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django  # noqa: E402

django.setup()
from django.core.management import call_command  # noqa: E402
from django.db import connection  # noqa: E402
from django.db.migrations.loader import MigrationLoader  # noqa: E402

out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/bench_lint_out"
os.makedirs(out, exist_ok=True)
loader = MigrationLoader(connection)
n = 0
for (app, name), _ in sorted(loader.graph.nodes.items()):
    if app in ("admin", "auth", "contenttypes", "sessions"):
        continue
    buf = io.StringIO()
    try:
        call_command("sqlmigrate", app, name, stdout=buf)
    except Exception as e:  # noqa: BLE001
        buf.write(f"-- sqlmigrate failed: {e}\n")
    with open(f"{out}/{app}__{name}.sql", "w") as f:
        f.write(buf.getvalue())
    n += 1
print(f"{n} migrations written to {out}")
