---
name: steward
description: How to drive the AllLists.com pull request to green. Use when CI fails, a review arrives, or the base branch changes.
---

# Steward guide

- Work on branch `claude/zen-wright-fudnux`; the PR is a draft. Subscribe to its activity and act on every event.
- Run locally before every push: `.venv/bin/flake8 backend`, `.venv/bin/bandit -q -r backend -x backend/lists,"*/tests/*","*/migrations/*" -ll`, `.venv/bin/pip-audit -r backend/requirements.txt`, `python manage.py makemigrations --check --dry-run`, and the tests (`cd backend && ../.venv/bin/pytest -q`, about 3 minutes; never run two test runs at once, they share a database).
- Bandit B608 on SQL: compose with `psycopg.sql`, do not use f-strings.
- Read the actual check results (`pull_request_read get_check_runs`); a "no failed suite" notice is not proof of success.
- Never skip or quarantine a test to get green. Fix the cause.
- Commit messages end with the attribution lines required by the session; push with `git push -u origin claude/zen-wright-fudnux`.
