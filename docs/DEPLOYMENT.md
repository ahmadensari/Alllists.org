# Deployment guide

How AllLists runs in production, written for the founder and whoever the founder hires. Every file named here is in the repository: `deploy/`, `scripts/`, `docs/runbooks/`. Nothing in this guide has been run on a real server yet; the first run is the staging rehearsal (section 9).

## 1. Shape of the system

Reverse proxy (Caddy, or Nginx) → Gunicorn (Django) → PostgreSQL 16. A scheduler runs every five minutes and does whatever is due (roll-ups, expiry, holds, reconciliation, alerts). A second timer sends approved outreach campaigns. A nightly timer takes the backup. No Redis, no Celery, no search engine at the start (the plan's stage S1); each is added only when a measurement says so.

Stages (plan 3.5): S0 one small server; S1 managed PostgreSQL plus one app server behind a CDN; S2 a read replica and a worker server; later stages in the plan.

## 2. What you need to decide or buy first (the founder)

1. **Domain and name.** Confirm the owner of `alllists.org`; consider `alllists.com` and `.pk`.
2. **Hosting.** One server in a region close to most users plus managed backups, or a managed platform. The plan assumes Ubuntu 24.04, 2 vCPU, 4 GB RAM, 80 GB disk to start.
3. **CDN and DNS** (Cloudflare free plan is enough at the start). It also supplies the visitor's country header the app reads.
4. **Email sender** (a transactional email service) for sign-up codes, enquiry relay and alerts.
5. **Payment provider** for the local currency and a foreign route. Until chosen, payments are recorded by hand in `/staff/orders/`.
6. **Counsel** before any messaging campaign, any list of named people, or any child-facing list.
7. **Rotate the secrets that were pasted into chat** (`docs/runbooks/secret-rotation.md`). Do this before anything goes on a real server.

## 3. Prepare the server

```
sudo apt update && sudo apt install -y python3.12 python3.12-venv postgresql-16 postgresql-client-16 caddy git
sudo useradd --system --create-home --shell /usr/sbin/nologin alllists
sudo mkdir -p /srv/alllists/releases /var/lib/alllists/extracts /var/backups/alllists /var/log/alllists /etc/alllists
sudo chown -R alllists:alllists /srv/alllists /var/lib/alllists /var/backups/alllists /var/log/alllists
sudo ufw allow OpenSSH && sudo ufw allow 80,443/tcp && sudo ufw enable
python3.12 -m venv /srv/alllists/venv
git clone --mirror <repository-url> /srv/alllists/repo.git
```

Only ports 22, 80 and 443 are open; the app port is bound to 127.0.0.1.

## 4. Database

```
sudo -u postgres createdb alllists
sudo -u postgres psql -v app_pw="'<long random>'" -v ro_pw="'<long random>'" -f deploy/db_roles.sql alllists
```

The application connects as `alllists_app`, which can insert into the append-only tables (audit log, change log, verification events, consent records, ledger) but cannot update, delete or truncate them. `alllists_readonly` is for analysts and replicas and cannot read the sensitive tables (contacts, payout details, sessions, users). Migrations run as the owner; after each migrating deploy run `python manage.py db_roles --apply` as the owner, and `python manage.py db_roles --check` to confirm the grants are as designed.

PostgreSQL settings worth setting at once: `shared_buffers` 25% of RAM, `log_min_duration_statement = 500`, `wal_level = replica`, and WAL archiving to a different account or region (`archive_mode = on`, `archive_command` pointing at your object store with a tool such as `pgBackRest` or `wal-g`). The nightly dump in `scripts/backup.sh` is the floor; WAL archiving is what gets the loss window down to minutes at stage S2.

## 5. Configuration

Copy `deploy/env.example` to `/etc/alllists/alllists.env` (mode 600, owner `alllists`). Generate:

```
python3 -c "import secrets; print(secrets.token_urlsafe(64))"                           # DJANGO_SECRET_KEY
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"  # one field-encryption key
python3 -c "import secrets; print(secrets.token_hex(32))"                                # CONTACT_HASH_PEPPER
```

`FIELD_ENCRYPTION_KEYS` is written as `k1:<key>` (more keys separated by commas) and `FIELD_ENCRYPTION_ACTIVE_KEY=k1`. Keep an offline copy of these in a password manager: **losing the keys makes every contact and payout detail unreadable, and losing the pepper breaks the do-not-contact list.** Production refuses to start without them.

## 6. First release

```
scripts/deploy.sh <tag-or-commit>        # builds the release, migrates, collects static files, restarts, smoke tests
cd /srv/alllists/current/backend && set -a && . /etc/alllists/alllists.env && set +a
../../venv/bin/python manage.py seed_pilot          # Sialkot structure, first list type, sources, country switch (everything off but browsing)
../../venv/bin/python manage.py seed_taxonomy       # all list types and the add-on families
../../venv/bin/python manage.py createsuperuser     # the first admin; then turn on two-step sign-in at /account/security/
```

Install the units and timers and the proxy configuration:

```
sudo cp deploy/systemd/* /etc/systemd/system/ && sudo systemctl daemon-reload
sudo systemctl enable --now alllists-web alllists-scheduler.timer alllists-backup.timer
sudo systemctl enable alllists-campaigns.timer         # start it only when counsel has cleared a country
sudo cp deploy/Caddyfile /etc/caddy/Caddyfile && sudo systemctl reload caddy
```

Caddy obtains HTTPS certificates by itself once the DNS name points at the server. With Nginx use `deploy/nginx.conf` and certbot.

## 7. Everyday operation

| Task | How |
|---|---|
| Deploy | `scripts/deploy.sh <tag>` (`docs/runbooks/deploy-rollback.md`) |
| Roll back | `scripts/rollback.sh` |
| Health | `/staff/metrics/` (red rows are also emailed to `ALERT_EMAILS`, once a day each) and `/healthz` for an uptime monitor |
| Scheduled jobs | `/staff/jobs/` shows each job, its last run and last error |
| Backup | nightly by timer; copy `/var/backups/alllists` to another account or region |
| Restore drill | quarterly, `scripts/restore_drill.sh` |
| Money | `/staff/ledger/` reconciliation; `docs/runbooks/payout-cycle.md` |
| Incidents | `docs/runbooks/README.md` |

## 8. Container option

`deploy/Dockerfile` builds the same app as an image (`docker build -f deploy/Dockerfile -t alllists:TAG .`). Run one container for the web process and the same image with the command `python manage.py run_scheduled` on a five-minute schedule. Pass the environment from the platform's secret store. The database is a managed PostgreSQL instance.

## 9. Staging rehearsal (before the first real release)

1. Build a second small server the same way with `staging` hosts and payment sandboxes.
2. Deploy a tag, load the pilot data and the demo entries (`seed_demo_entries`), click through the sample pages in light and dark, English and Urdu.
3. Run the load script (`scripts/loadtest.py`, section 10) at three times the expected peak.
4. Run `scripts/restore_drill.sh`, time it and record it in `docs/runbooks/restore.md`.
5. Practise one rollback and one secret rotation.
6. Only then point the real domain at production.

## 10. Load tests and scale-up

`scripts/loadtest.py` replays a realistic mix (list pages, entry pages, search, fragments) against a base URL and reports p50/p95/p99 and error rate; the targets are in plan section 18.5 (shared pages from cache in under 200 ms, p95 of the private parts under 400 ms). When the targets are missed the order of remedies is: CDN cache rules, indexes, a read replica for list queries (`DATABASES["replica"]` and a router), partitioning the entry tables by country (the schema keeps `country_code` on every row for this), then a search engine behind the search service interface (`catalog/search_backend.py`).

## 11. What stays manual on purpose

Approving payout batches, approving message templates, turning a country on, and rotating secrets. Each needs a person, and the system will not do them by itself.
