# AllLists backend (Django 5.2, PostgreSQL 16)

A modular monolith. Each folder is one module with its own models, services, tests and migrations:

| Module | Responsibility |
|---|---|
| `core` | ULIDs, audit log (hash chain), change log, field encryption, flags, country switches, scheduled jobs, monitoring, database roles |
| `places`, `taxonomy` | Place tree and list types with synonyms, add-on templates, loaders for GeoNames, Overture, Foursquare, ISCO |
| `entries` | Entries, the verification state machine, claims, consent, credit rules, merging, company pages |
| `intake` | Source register and gate, paste and CSV import, duplicate pipeline, bulk place loaders |
| `access` | Visibility policy, plans, subscriptions, quotas, placements and ads |
| `accounts` | Sign-up, sign-in, two-step sign-in, roles, Google and ORCID sign-in |
| `moderation` | Reports, suggestions, takedown and erasure, consent withdrawal, subject access |
| `outreach` | Enquiry relay, opt-in, claim codes, campaigns, delivery callbacks |
| `volunteers` | Surveyor tasks, canaries, audit samples, onboarding, levels, certificates |
| `agents` | Page fetcher with address checks, model clients, draft jobs with verbatim evidence, caps and kill switch |
| `ledger`, `billing` | Double-entry ledger, rate phases, allocation, holds, payouts and batches, KYC, orders, payments, invoices, reconciliation, revenue report |
| `analytics` | Roll-up cells, events, statistics reports, extracts with planted trace entries |
| `catalog` | The public site: pages, fragments, forms, staff console, search, SEO, share registry, strings (English and Urdu) |

Rules that shape the code (see `docs/TECHNICAL_PLAN.md`): shared pages are identical for every visitor and carry no
personal data (R05); personal parts arrive through private `/_f/` fragments; contacts are never shown, only relayed
(R02); a check cannot be bought (R14); there is no list download, only a staff-made, traced extract (R13).

## Run it locally

    docker compose up -d db          # PostgreSQL 16 on localhost:5432 (throwaway credentials)
    cd backend
    pip install -r requirements.txt
    export DJANGO_DEBUG=1 POSTGRES_DB=alllists POSTGRES_USER=alllists POSTGRES_PASSWORD=alllists POSTGRES_HOST=localhost
    python manage.py migrate
    python manage.py seed_pilot && python manage.py seed_taxonomy && python manage.py seed_demo_entries
    python manage.py runserver

`python manage.py run_scheduled` runs whatever scheduled job is due (roll-ups, expiry, holds, reconciliation, alerts).

## Checks

    pytest                                   # about 400 tests on PostgreSQL, random order
    flake8 backend scripts                   # blocking in CI
    bandit -r backend -x "*/tests/*","*/migrations/*" -ll
    python scripts/mutation_check.py backend/ledger/services.py backend/ledger billing --max 30   # do the tests notice a broken rule?
    python scripts/loadtest.py http://localhost:8000 --users 20 --seconds 60

## Production

Read `docs/DEPLOYMENT.md`. It needs `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `DJANGO_CSRF_TRUSTED_ORIGINS`,
PostgreSQL settings, `FIELD_ENCRYPTION_KEYS`, `FIELD_ENCRYPTION_ACTIVE_KEY` and `CONTACT_HASH_PEPPER` (production refuses
to start without them; `deploy/env.example` lists everything). `ALLLISTS_DEMO` must stay off.
