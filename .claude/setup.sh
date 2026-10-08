#!/bin/bash
# Session start hook: install dependencies and start a local PostgreSQL so tests run (plan P0.09).
set -e
cd "$CLAUDE_PROJECT_DIR" 2>/dev/null || cd "$(dirname "$0")/.."
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then exit 0; fi
python3 -m venv .venv >/dev/null 2>&1 || true
.venv/bin/pip install -q -r backend/requirements.txt flake8 bandit pip-audit >/dev/null 2>&1 || true
if command -v pg_ctlcluster >/dev/null 2>&1; then
  pg_ctlcluster 16 main start >/dev/null 2>&1 || true
  sleep 2
  su postgres -c "psql -tc \"select 1 from pg_roles where rolname='alllists'\" | grep -q 1 || psql -c \"create user alllists with superuser password 'alllists'\"" >/dev/null 2>&1 || true
  su postgres -c "psql -tc \"select 1 from pg_database where datname='alllists'\" | grep -q 1 || psql -c \"create database alllists owner alllists\"" >/dev/null 2>&1 || true
fi
{
  echo 'export POSTGRES_DB=alllists POSTGRES_USER=alllists POSTGRES_PASSWORD=alllists POSTGRES_HOST=localhost DJANGO_DEBUG=1'
  echo 'export PATH="$CLAUDE_PROJECT_DIR/.venv/bin:$PATH"'
} >> "${CLAUDE_ENV_FILE:-/dev/null}"
