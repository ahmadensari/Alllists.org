#!/usr/bin/env bash
# One-command deploy (plan 18.2): build a release directory, install, migrate with a pre-check, collect static files,
# switch the symlink, restart, smoke test, and roll back automatically if the smoke test fails.
#   scripts/deploy.sh <git-tag-or-commit>
set -euo pipefail
REF="${1:?usage: deploy.sh <tag-or-commit>}"
ROOT="${ALLLISTS_ROOT:-/srv/alllists}"
REPO="${ALLLISTS_REPO:-$ROOT/repo.git}"          # a bare mirror kept up to date by `git fetch`
SMOKE_URL="${SMOKE_URL:-http://127.0.0.1:8000/healthz}"
STAMP="$(date +%Y%m%d%H%M%S)"
REL="$ROOT/releases/$STAMP"
PREV="$(readlink -f "$ROOT/current" || true)"

echo "== fetch and unpack $REF into $REL"
git --git-dir="$REPO" fetch --tags --quiet
mkdir -p "$REL"
git --git-dir="$REPO" archive "$REF" | tar -x -C "$REL"

echo "== install dependencies"
"$ROOT/venv/bin/pip" install --quiet -r "$REL/backend/requirements.txt"

set -a; . /etc/alllists/alllists.env; set +a
cd "$REL/backend"
PY="$ROOT/venv/bin/python"

echo "== pre-checks (settings, pending migrations, take a dump first)"
"$PY" manage.py check --deploy --fail-level ERROR
"$REL/scripts/backup.sh"
"$PY" manage.py migrate --plan | tail -n 20
echo "== migrate"
"$PY" manage.py migrate --noinput
echo "== static files"
"$PY" manage.py collectstatic --noinput --verbosity 0
echo "== re-apply database grants"
if [ -n "${DB_OWNER_URL:-}" ]; then "$PY" manage.py db_roles --apply; fi

echo "== switch and restart"
ln -sfn "$REL" "$ROOT/current"
sudo systemctl restart alllists-web

echo "== smoke test"
ok=0
for i in 1 2 3 4 5 6 7 8 9 10; do
  if curl -fsS --max-time 5 "$SMOKE_URL" >/dev/null; then ok=1; break; fi
  sleep 2
done
if [ "$ok" != 1 ]; then
  echo "SMOKE TEST FAILED: rolling back to $PREV" >&2
  if [ -n "$PREV" ]; then ln -sfn "$PREV" "$ROOT/current"; sudo systemctl restart alllists-web; fi
  exit 1
fi
echo "== done: $REF is live ($STAMP). Previous release kept at $PREV"
ls -1dt "$ROOT"/releases/* | tail -n +6 | xargs -r rm -rf   # keep the five newest releases
