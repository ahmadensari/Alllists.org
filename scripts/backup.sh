#!/usr/bin/env bash
# Nightly logical dump (plan 18.4). Keeps 14 daily and 8 weekly dumps, records the run so the monitor can alert when it stops.
# Copy $BACKUP_DIR to a different account or region as well (rclone, rsync); a backup next to the database is not a backup.
set -euo pipefail
BACKUP_DIR="${BACKUP_DIR:-/var/backups/alllists}"
mkdir -p "$BACKUP_DIR/daily" "$BACKUP_DIR/weekly"
STAMP="$(date +%Y%m%d-%H%M%S)"
FILE="$BACKUP_DIR/daily/alllists-$STAMP.dump"
PGPASSWORD="${POSTGRES_PASSWORD:-}" pg_dump -h "${POSTGRES_HOST:-127.0.0.1}" -p "${POSTGRES_PORT:-5432}" \
  -U "${POSTGRES_USER}" -Fc -Z 6 -f "$FILE" "${POSTGRES_DB}"
SIZE="$(du -h "$FILE" | cut -f1)"
[ "$(date +%u)" = 7 ] && cp "$FILE" "$BACKUP_DIR/weekly/"
ls -1t "$BACKUP_DIR"/daily/*.dump | tail -n +15 | xargs -r rm -f
ls -1t "$BACKUP_DIR"/weekly/*.dump 2>/dev/null | tail -n +9 | xargs -r rm -f
if [ -n "${ALLLISTS_ROOT:-}" ] || [ -d /srv/alllists/current/backend ]; then
  (cd "${ALLLISTS_ROOT:-/srv/alllists}/current/backend" && "${ALLLISTS_ROOT:-/srv/alllists}/venv/bin/python" manage.py record_ops backup "$STAMP $SIZE") || true
fi
echo "backup written: $FILE ($SIZE)"
