# AllLists backend (Django 5.2)

Server-rendered Django app that implements the design in `docs/` and `prototype/`:
place tree, lists as views, entries stored once, per-field checks (four labels), free vs subscriber
visibility, company pages, enquiry relay (contacts never shown), report/claim, share registry,
English/Urdu with right-to-left, automatic location (Cloudflare edge headers, never a redirect),
contributor ledger with the 50/40/30 phase rate locked per entry.

Run locally:

    cd backend
    pip install -r requirements.txt
    export DJANGO_DEBUG=1
    python manage.py migrate && python manage.py seed_demo && python manage.py runserver

Tests (from the repository root): `pytest`.

Production needs `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`, and for
PostgreSQL `POSTGRES_DB/USER/PASSWORD/HOST` plus `psycopg[binary]`. `ALLLISTS_DEMO=1` shows the plan
preview switch and must stay off in production. Payments, real email relay, subscriptions and
moderation queues are not built yet; see `docs/DECISIONS.md` open items.
