#!/usr/bin/env bash
# Point `current` at the previous release and restart. Migrations are forward-only: if the bad release migrated,
# restore from the dump taken by deploy.sh instead (docs/runbooks/restore.md).
set -euo pipefail
ROOT="${ALLLISTS_ROOT:-/srv/alllists}"
CUR="$(readlink -f "$ROOT/current")"
PREV="$(ls -1dt "$ROOT"/releases/* | grep -v "^$CUR$" | head -n 1)"
[ -n "$PREV" ] || { echo "no previous release" >&2; exit 1; }
ln -sfn "$PREV" "$ROOT/current"
sudo systemctl restart alllists-web
echo "rolled back to $PREV"
