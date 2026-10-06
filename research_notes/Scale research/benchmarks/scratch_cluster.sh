#!/usr/bin/env bash
# Throw-away PostgreSQL 16 primary (port 55432) and streaming replica (port 55433) in /var/tmp/bench_pg, owned by the
# postgres OS user, trust auth on 127.0.0.1. It never touches the main cluster. Used for replica-lag throttling (B06)
# and for connection-limit tests with a small max_connections (B08).
#   scratch_cluster.sh up      create and start primary + replica
#   scratch_cluster.sh down    stop both and delete /var/tmp/bench_pg
set -euo pipefail
BIN=/usr/lib/postgresql/16/bin
ROOT=/var/tmp/bench_pg
as_pg() { runuser -u postgres -- "$@"; }
case "${1:-}" in
up)
  rm -rf "$ROOT"; mkdir -p "$ROOT"; chown postgres:postgres "$ROOT"
  as_pg $BIN/initdb -D "$ROOT/primary" -A trust -E UTF8 --locale=C.UTF-8 >/dev/null
  cat >> "$ROOT/primary/postgresql.conf" <<EOF
port = 55432
listen_addresses = '127.0.0.1'
unix_socket_directories = '$ROOT'
max_connections = 40
shared_buffers = 512MB
wal_level = replica
max_wal_senders = 5
hot_standby = on
max_wal_size = 4GB
checkpoint_timeout = 5min
EOF
  as_pg $BIN/pg_ctl -D "$ROOT/primary" -l "$ROOT/primary.log" -w start >/dev/null
  as_pg $BIN/pg_basebackup -h 127.0.0.1 -p 55432 -D "$ROOT/replica" -R -X stream >/dev/null
  cat >> "$ROOT/replica/postgresql.conf" <<EOF
port = 55433
EOF
  as_pg $BIN/pg_ctl -D "$ROOT/replica" -l "$ROOT/replica.log" -w start >/dev/null
  echo "primary 127.0.0.1:55432 (max_connections=40), replica 127.0.0.1:55433"
  ;;
down)
  as_pg $BIN/pg_ctl -D "$ROOT/replica" -m fast stop >/dev/null 2>&1 || true
  as_pg $BIN/pg_ctl -D "$ROOT/primary" -m fast stop >/dev/null 2>&1 || true
  rm -rf "$ROOT"
  echo "scratch cluster removed"
  ;;
*) echo "usage: $0 up|down"; exit 1 ;;
esac
