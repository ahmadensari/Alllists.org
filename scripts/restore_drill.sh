#!/usr/bin/env bash
# Quarterly restore drill (plan 18.4): restore the newest dump into a scratch database, time it, check that the audit
# chain and the ledger still verify, record the result, and drop the scratch database. A skipped drill is an alert.
set -euo pipefail
BACKUP_DIR="${BACKUP_DIR:-/var/backups/alllists}"
SCRATCH="${SCRATCH_DB:-alllists_restore_drill}"
LATEST="$(ls -1t "$BACKUP_DIR"/daily/*.dump | head -n 1)"
[ -n "$LATEST" ] || { echo "no dump found in $BACKUP_DIR" >&2; exit 1; }
export PGPASSWORD="${POSTGRES_PASSWORD:-}"
H="${POSTGRES_HOST:-127.0.0.1}"; P="${POSTGRES_PORT:-5432}"; U="${POSTGRES_USER}"
dropdb -h "$H" -p "$P" -U "$U" --if-exists "$SCRATCH"
createdb -h "$H" -p "$P" -U "$U" "$SCRATCH"
START="$(date +%s)"
pg_restore -h "$H" -p "$P" -U "$U" -d "$SCRATCH" -j 4 --no-owner "$LATEST"
SECS=$(( $(date +%s) - START ))
cd "${ALLLISTS_ROOT:-/srv/alllists}/current/backend"
PY="${ALLLISTS_ROOT:-/srv/alllists}/venv/bin/python"
POSTGRES_DB="$SCRATCH" "$PY" manage.py shell -c "
from core.models import verify_audit_chain
from billing.reconcile import reconcile, all_ok
assert verify_audit_chain() is None, 'audit chain broken in the restored copy'
assert all_ok(reconcile()), 'ledger does not reconcile in the restored copy'
print('restored copy verifies')
"
dropdb -h "$H" -p "$P" -U "$U" "$SCRATCH"
"$PY" manage.py record_ops restore_drill "restored $(basename "$LATEST") in ${SECS}s"
echo "restore drill passed: ${SECS}s"
