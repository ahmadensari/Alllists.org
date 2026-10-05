# Contributing

The build plan is `docs/TECHNICAL_PLAN.md`. Work is done in work packages (WP) named there; each pull request says which.

1. Read section 1 of the plan (rules R01 to R40) and the rule tests in section 20.2.
2. Run the stack: `docker compose up -d db`, then
   `cd backend && pip install -r requirements.txt && export POSTGRES_DB=alllists POSTGRES_USER=alllists POSTGRES_PASSWORD=alllists POSTGRES_HOST=localhost DJANGO_DEBUG=1 && python manage.py migrate`.
3. Check your work from the repository root: `flake8 backend` and `pytest`.
4. Modules talk to each other through `services.py` only. Migrations are forward-only in production.
5. Decisions go in `docs/DECISIONS.md` before the code that depends on them.
6. Never commit secrets. Tests use fake values.
