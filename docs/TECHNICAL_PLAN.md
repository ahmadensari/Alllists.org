# AllLists.org: Technical Plan for the Website Code (v1)

Prepared 2026-10-05. This is the build plan for the production website. It is written so that coding can start from it without reopening debates.

- It turns every decision in `docs/DECISIONS.md` and `docs/REQUIREMENTS.md` into something the code must do, and says where in the code that happens.
- It uses the research in `reports/` and `research_notes/`, the specifications in `docs/LIST_AND_ENTRY_COMPONENTS.md` and `docs/DESIGN_SYSTEM.md`, and the working prototype (`prototype/alllists-prototype.html`).
- It starts from the first software build in `backend/` (Django 5.2, 17 tests) and says what stays, what is replaced and what is added.
- It does **not** reopen anything marked Decided. Where an open decision blocks code, the plan names the default it assumes, so work is never stuck (section 21).

Evidence tags used for facts that came from research: **[M]** measured by running something, **[S]** from a source or a search result, **[I]** my estimate or judgement, **[U]** unverified recall. Anything without a tag is design (a proposal under the decisions, not a fact about the world).

## How to use this plan

1. Read sections 1 to 3 (rules, tools, architecture). They bind every other section.
2. Sections 4 to 17 are the specification by area. Each ends with the work packages (WP) that build it.
3. Section 19 is the delivery plan: phases P0 to P6, every work package with size and acceptance test, and the first 90 days.
4. Section 21 is the owner-decision register with the default each phase assumes.
5. Section 22 maps every requirement ID (A1 to V8, CP, S, P) to the section and work package that implements it, so nothing is missed.
6. Appendices hold the details a coder needs open next to the editor: URL map, template list, registry seeds, permission matrix, settings and environment variables, job list, event names, test list, CI pipeline, repository layout and coding conventions.

## Contents

1. Rules the code must enforce (from the decisions)
2. Stack and resources to use (build, reuse, buy)
3. Architecture
4. Data model
5. Places, list types and the add-on registry
6. Entries, verification, claims and stewardship
7. Getting data in: sources, import, cleaning, duplicates, AI agents
8. Public pages, templates and the design system in code
9. Access, plans, quotas and anti-copying
10. Search, location and roll-ups
11. Accounts, roles and permissions
12. Money: products, payments, the ledger and payouts
13. Outreach and enquiries
14. Contributors, volunteers and surveyors
15. Back office: moderation, takedown, erasure, audit
16. Later modules: reviews, personal lists, topic lists, commerce, government, API
17. Security and privacy controls
18. Operations: environments, deployment, monitoring, backups, costs, per-country switches
19. Delivery plan: phases, work packages, first 90 days
20. Testing, CI and definition of done
21. Owner-decision register and assumed defaults
22. Requirement traceability matrix
23. Risks and how the plan answers them
24. Current code: keep, replace, add

Appendices: A URL map. B Template and fragment list. C Registry seeds. D Permission matrix. E Settings and environment variables. F Background jobs. G Events and metrics. H Test list. I CI pipeline. J Repository layout. K Coding conventions. L Page-weight and performance gates. M Glossary.

---

## 1. Rules the code must enforce

These are the decisions turned into testable rules. Each has an ID (R01 to R40). Section 20 requires an automated test for every rule that can be tested. A change to a rule is a decision change and goes into `docs/DECISIONS.md` first.

| ID | Rule | Source | Where enforced |
|---|---|---|---|
| R01 | Text and numbers only. No image, video or file upload fields. Content-Security-Policy allows no remote images. Media is reserved in the model, not built | C29 | Models (no media fields), CSP, template lint |
| R02 | Phone, WhatsApp and email of any entry are never rendered to any visitor, buyer or subscriber. Only the relay uses them. Stored encrypted | E13, G1 | `entries.contact` model has no public serializer; test greps every rendered page for contact values |
| R03 | One line between free and subscriber, defined in one table (the plans-and-visibility registry). No per-template exceptions | Spec s11, C34 | `access.policy` registry; every view calls it |
| R04 | Wider than the viewer's own place, a free viewer sees names only (a capped preview); a subscriber sees the full list | CP3, CP4, C39 | `access.scope_rule` |
| R05 | The address of every list and entry page returns the same main content to everyone. Location and plan never change content at an address. Personalised parts arrive as separate fragments. No automatic redirect by location | C39, search hygiene | Cache design (section 3.4), tests that compare responses |
| R06 | Only the four decided check labels exist: Surveyor-verified, Owner-verified, AI-checked, Not verified yet. "Verified" never appears alone. An AI check is never called verified | D19, D20 | `check_label` registry, template lint test |
| R07 | Independence: a surveyor is never the contributor who added the entry; an AI check must use a different source or method from the AI draft; every check expires and is dropped by a scheduler | D20 | Verification state machine guards (section 6.4) |
| R08 | An entry at "Not verified yet" is hidden from the public list; list counts read "N published, M awaiting verification" (assumed default, Q-P6) | D18, P14, Q-P6 | `publish_state` and list queries |
| R09 | Imports, agent drafts and self-listed entries earn no contributor payout. Payout credit needs surveyor or owner level and a re-check | D5, D8, D20.8, CP1 | `credit_event.eligible` rules |
| R10 | Contributors are paid only when a list is sold. No cash up front | CP1 | Ledger design: credit accrues, pays on sale |
| R11 | Contributor rate steps 50, 40, 30 by phase; the phase is locked on each entry the day it is accepted | F2, F3 (assumed) | `rate_phase`, `entry.phase_id` |
| R12 | The contributor share is calculated on net revenue, buyer-side revenue first, with a cap on how long an entry earns its phase rate (default 36 months) | Q-S15 (assumed default) | `ledger.rules` |
| R13 | No download of list data. The only export is the heavy-price extract (about USD 1,000 minimum), made by staff, watermarked with planted trace entries | E13, E10 | No export endpoint for users; admin-only extract job |
| R14 | Paid ranking is labelled "Sponsored", sits in capped slots, and never changes check labels or verification order. A check cannot be bought | E15, C35 | `placement` table, template slot component |
| R15 | Company-provided sections are public, labelled "Provided by the company" with the update date. Certificates show "Company says" until checked | C35 | Company template sections |
| R16 | Free visitors see ads; subscribers see none | CP5 | Ad slot component |
| R17 | Removing or correcting your own personal data is free and available on every entry ("Something wrong?") | P17 | Moderation module; link in the legal footer |
| R18 | Individuals (doctors, lawyers, tradespeople, tutors, data scientists) appear only with consent, by area only, no home address, no ranking of people, no share button unless consent covers it; contact by relay only | C22, Q-S2 | `consent_record`, `entity_type=person` rules |
| R19 | Child-facing services (including Quran tutors) are not public until safeguarding and relay-only contact are built; schools and centres first | Q-S2 | Feature flag, publish gate |
| R20 | Prices are shown only with a price date. No "cheapest". Health prices wait for the health rules | C21, Q-S1 | `entry_service.price_date` required; flag per list type |
| R21 | Every record keeps source, licence, collection date, robots decision and consent status. A record whose source is blocked cannot be published | D17 | `source`, `entry_value_meta`, licence gate |
| R22 | Red sources (scraped Google Maps, Facebook, Baidu or Amap, logins, anti-bot bypass, bought lists) are never ingested | D15, Q-P4 (assumed) | `source.tier=red` blocks import and agent fetch |
| R23 | Thin or empty list pages are `noindex,follow` and not in sitemaps. A list page is indexable only with at least N verified entries (start N=10). Entry pages are indexable only when verified and rich. Filters and sorts are `noindex` with canonical to the plain list. `robots.txt` never blocks thin pages | J5, P6, A5 | SEO module (section 8.6) |
| R24 | Global structure from day one; selling, outreach, ads and indexing are switched on country by country | P11, S3 | `country_switch` table, feature flags |
| R25 | No hand-made pages. A template change reaches every page that uses it. Template versions are in cache keys | C34 | Template architecture (section 8.1) |
| R26 | System fonts only, no third-party scripts, page weight budgets enforced in CI | Design s9 | Build gate (Appendix L) |
| R27 | Right-to-left works from the start. Logical CSS only (start and end). Whole-sentence strings with placeholders. Western digits in all languages | N3, Design s7 | CSS lint, i18n tests |
| R28 | Rows with no value are left out. The page never says "Not stated". No position numbers on rows. People are never ranked | Design review | Template tests |
| R29 | Outreach is opt-in, platform-sent, with caps, quiet hours and one-tap opt-out. The official WhatsApp Business API only. No unofficial WhatsApp libraries. Off in a country until counsel clears it | G4, E13, Q-N5 | `outreach` module, country switch |
| R30 | Government and institutions get aggregate statistics only at first | E16, Q-N3 (assumed) | Statistics product only |
| R31 | No public API at launch | Service-provider round | No API routes; test asserts none |
| R32 | The ledger and audit log are append-only. The application database role has no update or delete right on them. Postings of each transaction sum to zero | F11, B5 | DB grants, trigger, property tests |
| R33 | Personal lists are private by default and are never sold, exported or used for recommendations without the owner's consent | I2, I8 | Later module, schema reserved |
| R34 | Secrets only in environment or a secret store, never in the repository. The previously exposed credentials are rotated before any deployment | M8, M9 | CI secret scan, deployment checklist |
| R35 | AI agents have no passwords and no production write access. They write only to staging. Every phone and address must be quoted verbatim from the fetched page. Hard cost caps and a kill switch. Fetched pages are data, never instructions | D14, B5 | `intake.agent` module |
| R36 | Map pin is stored as latitude and longitude (WGS-84) only. Map links are generated at display time. China coordinate conversion happens at link time only | Spec s8 | `maps.links` helper |
| R37 | Code is licensed Apache-2.0 (proposal, A3); list data is under separate terms | A3 | `LICENSE`, data terms page |
| R38 | Every new decision is recorded in `docs/DECISIONS.md` and `docs/REQUIREMENTS.md` before or with the code that depends on it | C24 | Pull-request checklist |
| R39 | Do not charge to remove personal data. Charge for visibility, rank, badge, extra fields and leads | P17 | Product catalogue |
| R40 | Every access or pricing rule is judged by two tests: better usage and returning clients, and revenue. Each such rule ships with the event that measures it | CP8 | Section 18 metrics |

---

## 2. Stack and resources to use

### 2.1 Chosen stack (defaults from Q-S9 and Q-S18; recorded in `docs/DECISIONS.md` as suggested, not yet signed off)

| Layer | Choice | Why | Licence | Status |
|---|---|---|---|---|
| Language | Python 3.12 (CI also 3.11 and 3.13) | Django 5.2 needs 3.10 or newer; 3.9 is out of support [U] | PSF | In use |
| Framework | Django 5.2 LTS | Admin, auth, migrations, forms, translation and security middleware ship with it; back office is the bulk of early work [S, analysis B12] | BSD | In use |
| Database | PostgreSQL 16 or newer with `pg_trgm` and `unaccent` now; PostGIS enabled at stage S1 | All timings in the analysis were measured on 16.14 [M]; PostGIS was not available on the test machine, so geo queries are untested | PostgreSQL licence; PostGIS GPL (used as a database extension) | SQLite in use for demo only; CI must move to Postgres (WP P0.04) |
| DB driver | psycopg 3 (`psycopg[binary]`) | Current Django support | LGPL | To add |
| Server rendering | Django templates | Search-engine readable, works without JavaScript (R05, R26) | BSD | In use |
| Interaction | HTMX 2 for fragment swaps; native `<details>`, `popover`, `dialog`; a tiny own script. Alpine.js only if a component needs client state | Keeps JavaScript under the 30 KB budget (HTMX is about 14 KB compressed and Alpine about 16 KB [U], so both together sit at the limit; measure before adding Alpine) | HTMX BSD-2, Alpine MIT | Own small script in use |
| Motion | CSS only: View Transitions, `@starting-style`, scroll-driven header shadow, transitions on opacity and position | Decided approach (C36, MODERN_UI_TOOLS) | n/a | In prototype; port to templates |
| Styling | Hand-written CSS with tokens (the prototype's block, already copied to `backend/lists/static/lists/app.css`); no Tailwind needed | Tokens are the source of truth; a build step adds nothing | n/a | In use |
| App server | Gunicorn behind a reverse proxy; WhiteNoise for static files behind the CDN | Simple, one deploy | MIT, MIT | In use |
| Job queue | Procrastinate (Postgres-backed) [U on features, check before adoption]. Fallback: Celery with a Postgres or Redis broker | No extra service; load is tiny at first (analysis 4.3) | MIT | To add |
| Auth extras | `django-allauth` (sign-in providers incl. ORCID later), `django-otp` (MFA), login throttling through `django-axes` or a small own table | MFA is required for admin, moderator, surveyor lead and payout roles | MIT, check django-otp, check axes | To add |
| Security headers | `django-csp` or a small own middleware; Django's `SecurityMiddleware` | CSP is required (the legacy `app.js` violated it) | BSD-style [U] | To add |
| Rate limiting | CDN rules plus an application counter table (`quota_counter`); `django-ratelimit` optional | Anti-scraping and brute-force defence | Apache-2.0 [U] | To add |
| Encryption | `cryptography` (Fernet or AES-GCM) with key versioning for contact values and sensitive person fields | Contacts stored encrypted, shown only to the relay | Apache-2.0/BSD | To add |
| Tests | pytest, pytest-django, Hypothesis (ledger property tests), coverage | Property tests for money | MIT, MPL-2.0 | pytest in use |
| Browser tests | Playwright with the Chromium already installed in cloud sessions; axe-core injected for accessibility checks | Real rendering, RTL, theme and keyboard checks | Apache-2.0; axe-core MPL-2.0 [U] | Scripts exist outside the repo |
| Linting and scans | flake8 now (add ruff if wanted), bandit, pip-audit, GitHub secret scanning with push protection (already blocked one push), Dependabot | Free checks in CI | Apache/MIT | flake8 in CI; rest to add |
| Load tests | k6 or Locust [U] | Before each stage | AGPL (k6) is used as a tool only, not linked; Locust MIT | To add at P6 |
| Monitoring | Sentry, UptimeRobot, Grafana Cloud (free tiers first) [S] | Small quotas are enough at S0 to S1 | Services | To add |
| CDN and bot rules | Cloudflare (free tier first). Location headers `CF-IPCountry` always; city headers need the "visitor location headers" setting [S] | Caching, bot rules, edge location | Service | Header reading in use |

### 2.2 Open code, data and tools to reuse (from `docs/REUSE_AND_TOOLS.md`, with the step where each is used)

| Need | Reuse | Licence (grade) | Used at | Caution |
|---|---|---|---|---|
| Place tree seed | GeoNames, Overture divisions | CC BY 4.0; Overture per-record | P1 (WP P1.06) | Avoid GADM (non-commercial) |
| Taxonomy seed | Overture categories, Foursquare categories, ISCO-08, ISIC, schema.org, own local layer | Overture CC BY 4.0 file; Foursquare Apache-2.0 | P1 (WP P1.07) | Confirm each file's licence before copying text |
| Open baseline places | Overture places, Foursquare Open Source Places, government registers, OSM (separate share-alike layer) | Per record; ODbL for OSM | P1 import, as `draft` | Licence gate on every batch |
| Duplicate detection | `pg_trgm` and `unaccent` first; Splink later | MIT (File) | P1 v1, Splink at S2 | Needs Urdu folding rules (section 7.3); trigram similarity of the same Urdu name with two yeh forms was only 0.54 and Urdu against Latin 0.00 [M] |
| Address parsing | libpostal later | MIT (Memory) | S2+ | Weak on informal addresses |
| Geocoding | Hosted service if terms allow; Pelias (MIT) or Photon (Apache-2.0) self-hosted later; Mimirsbrunn AGPL avoided | As listed | P2 or later | Check licence terms of any service used |
| Ledger design reference | Saleor payouts (BSD-3, File) for study; `django-ledger` for reference only | BSD-3; unknown | P3 design | Build a small Postgres double-entry ledger; Formance (MIT) only if volume demands |
| Inbox for replies | Chatwoot (MIT) as a separate service | MIT (Seen) | P4 | Needs official WhatsApp Business API |
| Email campaigns | listmonk (AGPL-3.0) as a separate service only | AGPL (Seen) | P4 optional | Never copy its code into ours |
| Search engine | Postgres first; Meilisearch Community Edition (MIT) or OpenSearch (Apache-2.0) later; Typesense is GPL-3 | As listed | P6 only if measured | Meilisearch Enterprise parts are BUSL |
| Maps | MapLibre GL JS with self-hosted Protomaps PMTiles | Open | Later (text-only scope now) | Read terms first |
| Design tool | Penpot (AGPL, self-hostable) or keep tokens in CSS | AGPL | Optional | Tokens in the repo stay the source of truth |
| Observability | Sentry, UptimeRobot, Grafana free tiers | Services | P3 | Quotas small |

### 2.3 Services to buy, not build

| Need | Approach | Open point |
|---|---|---|
| Payments in (Pakistan) | A licensed local gateway (PayFast and Safepay are reported to hold State Bank licences [S]); Stripe and PayPal do not onboard Pakistani businesses [S] | Which one (Q-S/F12); manual payment recording first |
| Payments in (foreign buyers) | A merchant-of-record provider or a gateway the founder's entity can open; decide at the bake-off | Not researched to a named product |
| Payouts | Local wallets and bank rails through a disbursement aggregator; manual first; limits per wallet apply [S] | Counsel on holding balances |
| WhatsApp, SMS, email | Official WhatsApp Business API through a provider; an SMS aggregator; a transactional email provider. Pakistan WhatsApp marketing rate reported at USD 0.0473 and utility USD 0.0100 per message from 1 April 2026 [S, third-party page, not checked at Meta] | Bake-off of two providers after counsel |
| CDN, DNS, bot rules | Cloudflare free first | |
| Counsel | Hours before any messaging test, named-individual list, health or child data, talent list, and before the first payout | Budget |

### 2.4 What the tools in this working environment do for the build

| Capability here | Use in the build |
|---|---|
| `security-review`, `code-review`, `simplify` skills | Run on every phase's pull request; security review before P3 (money) and P4 (outreach) |
| `session-start-hook` skill | Make cloud sessions install dependencies and run tests and linters at start (WP P0.09) |
| `run` skill and the installed Chromium with Playwright | Launch the app and take screenshots at 320, 390 and 1100 px in English and Urdu, light and dark |
| Subagents | Parallel test writing, labelled-pair building for duplicates, translation drafts, research on registers |
| Workflow tool | Only when the owner asks in their own words ("use a workflow") |
| GitHub tools | Pull requests, CI results, review threads, secret scanning |
| Scheduled routines | Re-check source terms, watch pull requests, run the quarterly restore-drill reminder |
| Docs and artifacts | Share plans and a decision dashboard privately |

---

## 3. Architecture

### 3.1 Principles

1. **One application, one database, background workers** (a modular monolith). Split only when a measurement demands it.
2. **Rows only for things that exist.** List-places (a list type at a place) are computed, never pre-created. Billions of possible list-places, a few thousand real pages [M].
3. **Events are append-only; current state is a projection.** Verification, consent, ledger, outreach, change history and audit.
4. **The server renders pages.** Plain HTML first; JavaScript only improves.
5. **Country is a key everywhere** (law, partitioning, switches).
6. **Registries, not special cases.** Share channels, social platforms, check labels, list types and add-ons, plans and visibility, listing plans, strings, feature flags (R25).
7. **Lists are views.** A list is a list type at a place; entries are stored once and roll up.

### 3.2 Modules (Django apps)

Each module owns its tables and exposes a small `services.py`. Modules call each other only through services, never by writing another module's tables. An import-boundary check in CI fails the build on a forbidden import.

| Module | Owns | Depends on |
|---|---|---|
| `core` | ULIDs, soft-delete base, audit log, change log, feature flags, country switches, settings loaders, encryption helpers, clock | none |
| `places` | Place tree, names, proposals, GeoNames import | `core` |
| `taxonomy` | Concepts (list types, specialities, services, products), labels, crosswalks, add-on registry, list-type settings | `core` |
| `entries` | Entries, child records, per-field meta, verification events and projection, claims, stewardship, merge map, credit events | `core`, `places`, `taxonomy` |
| `intake` | Sources, licence gate, import batches, normalisation, duplicate pipeline, agent jobs and draft staging, takedown intake | `core`, `places`, `taxonomy`, `entries` |
| `catalog` | Public pages: views, templates, fragments, share registry, SEO, sitemaps, roll-up reads, search, location | `core`, `places`, `taxonomy`, `entries`, `access` |
| `access` | Viewer plans, entitlements, quotas, scope rules, listing plans, placements (sponsored), ad slots | `core`, `accounts` |
| `accounts` | Users, profiles, roles, MFA, steward grants, sessions | `core` |
| `ledger` | Accounts, transactions, postings, phases, sales, allocations, payouts | `core`, `entries` (read), `accounts` |
| `billing` | Products, orders, payments, provider adapters, webhooks, invoices, tax | `core`, `access`, `ledger` |
| `outreach` | Opt-in, suppression, templates, campaigns, messages, provider adapters, inbox bridge, enquiry relay | `core`, `entries`, `access` |
| `moderation` | Reports, suggested edits, claims queue, takedowns, erasure, consent records | `core`, `entries`, `accounts` |
| `volunteers` | Tasks, levels, rewards, surveyor workflow, audit samples, canaries | `core`, `entries`, `accounts` |
| `analytics` | Events, funnels, data-quality and revenue dashboards, roll-up cells | `core` |
| `topics` (later) | Topic tree and topic lists (apps, websites, books) | `core`, `taxonomy` |
| `personal` (later) | Private and shared personal lists | `core`, `accounts` |
| `commerce` (later) | Product requests, test panels, offers, shipping partners | everything above |

### 3.3 Request flow

```
Visitor / search bot
   -> CDN: cache, bot rules, quotas by address, edge location header
   -> Gunicorn / Django
        middleware: security headers, language, theme, template version, location (guess), quota check
        view: resolves place path + list type -> reads rollup_cell + list query (scoped, indexed)
        renders the SHELL (same for everyone): free view of rows, names, areas, checks, counts
        -> HTML (cacheable)
   -> in the browser, HTMX loads FRAGMENTS (not cached, private, Vary by cookie):
        near-you strip, subscriber detail panel, "show more" rows within the viewer's limit,
        ad slot (free only), enquiry form state, quota notice
```

### 3.4 Caching rules (needed so one address gives everyone the same content, R05)

| Part | Cacheable | How |
|---|---|---|
| Shell HTML of list, place, entry, empty list, static pages | Yes, shared | Key = path + language + template version + data version (the page's `updated_at` stamp). `Cache-Control: public, s-maxage` and `stale-while-revalidate`; ETag from the same stamp |
| Near-you strip, plan panel, extra rows, ads, quota notice | No, private | HTMX fragment endpoints under `/_f/`, `Cache-Control: private, no-store`, `Vary: Cookie`, never indexed (`X-Robots-Tag: noindex`) |
| Roll-up counts | Yes, as part of the shell | Read from `rollup_cell`, shown with "as of" time |
| Template change | Version bump | `TEMPLATE_VERSION` is in the cache key and the ETag, so new pages replace old as requested; urgent purge by URL prefix or tag if the CDN supports it (check plan); rollback = previous version (R25) |
| Language | Separate URL | Urdu pages live under `/ur/…` with `hreflang` pairs; English is unprefixed (proposal; see Q-T1) |

The first software build renders per-viewer HTML in one response. That is incompatible with a shared cache. Section 24 lists this as a rebuild item (WP P2.05).

### 3.5 Stages and topology (from the analysis; no stage is skipped, none is bought early)

| Stage | Entries / views | Topology | Triggers to move on |
|---|---|---|---|
| S0 Proof | up to 5,000 / under 5,000 a month | One small server or free-tier Postgres, CDN | First buyer pays for a sample |
| S1 Pilot | 50,000 / 100,000 | One app server (web and worker together), managed Postgres with point-in-time recovery, staging, PostGIS on | 5 paying buyers |
| S2 Country | 1 million / 1 million | 2 web, 1 worker, Postgres primary with automatic backups, country partitions turned on, Splink for duplicates | A measured limit |
| S3 Multi-country | 10 million / 10 million | Read replica, search engine for scoped search, second worker pool | Search p95 over 500 ms or maintenance windows too long |
| S4 Global | 100 million / 100 million | Country groups on separate Postgres, search cluster, separate ledger database | Above 100 million entries or a country above about 50 million |

Current environment facts to respect (O1 to O8): the old Google Cloud VM `all-lists-server` runs Python 3.8 (out of support) with an ephemeral IP and a hand-assembled copy; the plan does not reuse it. A new Ubuntu 24.04 host (or managed platform) is built from the repository, with a reserved static IP, DNS for `alllists.org` through the CDN, HTTPS at the edge, and the deploy done by a script from a tagged commit, never by pasting files.

### 3.6 Deferred on purpose

Kubernetes, Redis, a separate search engine, read replicas, sharding beyond list partitions, a public API (R31), maps on pages (R01), reviews until rules exist, personal lists, ML recommendations, the commerce layer, China-specific handling, automated payouts, and any global AI-agent run.

---

## 4. Data model

### 4.1 Conventions

- **IDs.** Every public object has a `uid` (ULID, 26 characters, time-ordered, never reused) used in URLs and APIs. Internal joins use `bigint` keys. Foreign keys that matter for law or partitioning also carry `country_code`.
- **Country partition key.** `entry`, every child table, `entry_value_meta`, `verification_event` and `change_log` carry `country_code` (ISO 3166-1 alpha-2; `ZZ` for global lists with no country). At S0 to S1 they are plain tables with indexes that lead with `country_code`. At S2 they are converted to Postgres list partitions by country in a migration written then (declarative partitions need the partition key inside the primary key and foreign keys; Django 5.2 has composite primary keys but not composite foreign keys, so the conversion is a hand-written SQL migration). Designing the columns now makes that conversion mechanical. `ledger_*` and `audit_log` are partitioned by month instead, because money and audit must stay in one consistent store.
- **Soft delete.** No row disappears silently. `deleted_at`, `tombstone_reason`, `merged_into_id`. Erasure of personal data replaces fields with a tombstone and keeps hashed identifiers for the audit trail.
- **Money.** Integer minor units (`bigint`) plus ISO 4217 currency, always with a price date where shown.
- **Time.** UTC `timestamptz`; opening hours also carry the IANA time-zone name.
- **Language tags.** BCP 47 (`ur`, `en`, `ar`, `ur-Latn` for Roman Urdu).
- **Phones.** E.164. **Coordinates.** WGS-84 `numeric(9,6)` pair now; PostGIS `geography(Point)` added at S1 with the pair kept as the source value.
- **Append-only tables** (`verification_event`, `change_log`, `audit_log`, `ledger_txn`, `ledger_posting`, `consent_record`, `delivery_event`, `merge_map`): no update or delete grant for the application role; corrections are new rows.
- **Encrypted columns** (`*_enc`): contact values, owner name of individuals, payout details, KYC data. A lookup hash column (`*_hash`, keyed HMAC) allows de-duplication and suppression without decrypting.
- **Migrations.** Forward-only in production; each migration has a tested reverse in CI; destructive changes need two releases (add, then drop).

### 4.2 Table groups

Columns are shown as `name type (note)`. "R" required, "idx" index. This is the schema v1 to build; names may change in code but the content may not (section 1 rule R38).

#### 4.2.1 `core`

| Table | Columns | Notes |
|---|---|---|
| `audit_log` | id, ts, actor_id, actor_role, action, object_type, object_uid, country_code, ip_hash, payload jsonb, prev_hash, hash | Hash chain: `hash = H(prev_hash || row)`; written in the same transaction as the change; covers logins, role changes, verification, claims, exports, ledger and payout actions (analysis 6.3) |
| `change_log` | id, entry_id, country_code, field_key, old jsonb, new jsonb, actor_id, source_id, ts | One row per field change; feeds "last three changes" on the entry page and disputes |
| `feature_flag` | key, description, enabled_default, scope (country / group / user), rollout_percent | Risky template changes go to a small share first (R25) |
| `country_switch` | country_code, selling_on, outreach_on, outreach_channels[], ads_on, indexing_on, publish_cap_per_week, named_individuals_on, health_prices_on, child_services_on, legal_note, cleared_by, cleared_on | The per-country control for R24; everything defaults to off except browsing |
| `registry_version` | registry_key, version, changed_at, changed_by | Add-on and template registries are versioned (spec rule 3) |

#### 4.2.2 `places`

| Table | Columns | Notes |
|---|---|---|
| `place` | id, uid, parent_id, level (enum: world, region, country, admin1, admin2, admin3, city, area, society, street), local_level_label, iso_code, country_code, slug, path text (e.g. `pk.punjab.rawalpindi.adyala`), depth, centre_lat, centre_lon, bbox, population_band, status (active, proposed, rejected, merged), proposed_by, source_id, geonames_id, wikidata_id, created_at | `path` with a prefix index (`text_pattern_ops`) makes "everything under Rawalpindi" one range scan: 1.7 ms for a city, 50 ms country-wide at 1 million entries [M]. Levels are generic because countries differ (C14). Unique `(parent_id, slug)` |
| `place_name` | place_id, language, script, name, kind (preferred, alias, transliteration), name_fold | Both scripts; fold column feeds search |
| `place_proposal` | id, parent_id, proposed_name, language, proposer_id, state, duplicate_of_place_id, decided_by, reason | User-added areas (Adyala Road, Abraham Street) are proposed, matched against existing areas first, approved by a moderator or a duplicate check (Q-O2 default) |

#### 4.2.3 `taxonomy`

| Table | Columns | Notes |
|---|---|---|
| `concept` | id, uid, parent_id, kind (family, list_type, speciality, service, product), slug, entity_type_default (business, facility, person, institution), natural_scale (hyper_local, city, national, global), template_id, status, created_by, created_at | One concept per list type (C15). Browse depth about 3 levels. Ambiguous words map to a parent |
| `concept_label` | concept_id, language, region, kind (preferred, synonym, local, misspelling), text, text_fold | "Petrol pump", "gas station", "fuel station" are one concept; used by search and by list-page titles |
| `concept_crosswalk` | concept_id, system (isic, isco, overture, foursquare, osm, schema_org, hs), code, match_type (exact, broader, narrower) | Seed from Overture, Foursquare, ISCO-08, ISIC |
| `addon_template` | id, key, version, status, description | One per list-type family (doctors, hospitals, labs, trades, schools, tutors, manufacturers, contractors, agents, hotels, pharmacies and pumps, retail) |
| `addon_field` | template_id, key, label_key, type (text, number, enum, bool, date, concept_list, money), validation jsonb, required_for_publish, show (P, L, H, I), filterable, row_descriptor, version, deprecated_at | Add and deprecate, never change meaning |
| `list_type_settings` | concept_id, index_threshold (default 10), row_descriptor_field, word_for_thing_key, actions_allowed[], share_hidden_rule, is_individual, is_child_facing, is_health, price_required_date | Exceptions are rules here, not special pages (R25) |

#### 4.2.4 `entries` (the fixed core and everything repeating)

`entry` columns (the Tier 1 core of `docs/LIST_AND_ENTRY_COMPONENTS.md` section 4; every key there maps to a column or child table):

| Column | Type / note | Spec key |
|---|---|---|
| id, uid, country_code | keys | `entry_id` |
| entity_type | enum business, facility, person, institution | `entity_type` |
| primary_concept_id; secondary concepts in `entry_concept` | FK; M2M | `primary_category`, `secondary_categories` |
| name, name_lang, name_fold | text | `name` |
| description | text, 150 to 600 characters recommended | `description` |
| status, status_date | open, temporarily_closed, permanently_closed, moved | `status` |
| publish_state | draft, review, published, suppressed, tombstoned | supports R08 |
| address (jsonb structured), address_text_local, address_text_latin | | `address` |
| place_id, place_path | most specific place and its `path` copied for range scans | `place_ids` |
| lat, lon, precision_class (exact, building, street, area, city), coord_source, coord_date | | `location` |
| service_area jsonb | place ids or radius | `service_area` |
| website | URL | `website` |
| size_band | enum by type (employees, beds, rooms, fleet) | `size` |
| year_established | int | `year_established` |
| parent_entry_id | chain or branch link | `parent_entry` |
| languages[] | BCP 47 | `languages` |
| price_band | enum | `price_band` |
| payment_methods[] | enum list | `payment_methods` |
| addons jsonb, addon_template_version | validated by `addon_field` | Tier 2 |
| rating_score, rating_count | reserved; hidden until review rules exist (Q-P3) | `rating` |
| claim_state | unclaimed, pending, claimed | `claim` |
| listing_plan, plan_valid_until | basic or company | company page |
| visibility_flags | do_not_share, noindex, suppressed | `visibility_flags` |
| created_via | contributor, import, agent, register, self | R09 |
| created_by_id, phase_id | contributor and locked rate phase | `contributor_credit`, R11 |
| created_at, updated_at, last_verified_at, deleted_at, tombstone_reason, merged_into_id | | `timestamps` |

Indexes: `(country_code, place_path text_pattern_ops, primary_concept_id, publish_state)` for the list query; trigram GIN on `name_fold`; full-text `simple` configuration on folded name plus concept labels; `uid` unique; `(country_code, claim_state)`; partial index on `publish_state='published'`.

Sensitive person fields (owner name of an individual, personal mobile) live in `entry_sensitive` (encrypted, separate table and database role), not on `entry`.

Child tables, each keyed by `(country_code, entry_id)`:

| Table | Columns |
|---|---|
| `entry_name_variant` | text, language, kind (legal, trade, old, transliteration), text_fold |
| `entry_contact` | type (phone, mobile, whatsapp, email, fax), value_enc, value_hash, label (sales, support, emergency), preferred_hours, verified_at, relay_only (always true), optin_state |
| `entry_social` | platform (from the social registry), handle_or_url, owner_confirmed, last_link_check, link_status |
| `entry_hours` | day_from, day_to, open, close, split_shift, holiday_rule, appointment_only, confirmed_on, tz |
| `entry_service` | concept_id, name_text, description, price_minor, currency, price_type (fixed, from, hourly, per_visit), unit, price_date (required if price set), prep_notes |
| `entry_product` | concept_id or name, brand, unit, price_band, availability_note, price_date |
| `entry_speciality` | concept_id, qualification, own_hours (OPD timings) |
| `entry_identifier` | scheme (PMDC, PEC, NTN, SECP, GSTIN, ISO_13485, drug_licence, HS), value, issuer, valid_from, valid_to, last_checked, register_url. National ID numbers (CNIC) are never stored |
| `entry_area_served` | place_id or radius_km, notes |
| `entry_equipment` | type, make_model, quantity, modality, installed_year, services_supported |
| `entry_branch` | address, lat, lon, hours ref, contacts ref |
| `entry_concept` | secondary concept links |

Per-value metadata and verification:

| Table | Columns | Notes |
|---|---|---|
| `entry_value_meta` | entry_id, country_code, field_key, source_id, licence_id, retrieved_at, level (surveyor, owner, ai, none), verified_by, method, verified_at, expires_at, evidence_text, consent_ref, confidence | One row per field costs about 701 bytes per entry; store a row only where it differs from the entry-level default (halves it) [M, I] |
| `verification_event` | id, entry_id, country_code, field_group, level, state (pending, verified, expired, revoked), actor_id, method, evidence_text, ts, expires_at, supersedes_id | Append-only |
| `verification_current` | entry_id, field_group, level, state, verified_at, expires_at, method, actor_display | Projection the pages read; rebuilt from events |
| `claim` | id, entry_id, user_id, method (otp_phone, otp_email, documents), state, evidence_text, created_at, decided_by, decided_at | |
| `steward_grant` | id, user_id, place_id, concept_id (nullable), state, granted_at, last_active_at, expires_at (90-day inactivity default), dispute_state | Revocable stewardship (C20, Q-P2 default) |
| `consent_record` | id, subject_kind (entry, contact), subject_id, status, method, wording_version, evidence_text, at, takedown_state | Append-only |
| `merge_map` | id, from_entry_id, to_entry_id, score, decided_by, decided_at | Keeps the earliest credit |
| `credit_event` | id, entry_id (nullable after merge), user_id, kind (added, verified, area_added, claimed_assist), eligible, ineligible_reason, phase_id, created_at, merged_from_id | Credit lives here, not on the entry, so duplicates merge without losing first-adder credit (D6) |

#### 4.2.5 `intake`

| Table | Columns |
|---|---|
| `source` | id, name, tier (green, amber, red), licence_text, terms_url, robots_decision, allowed_uses, bulk_permission, personal_data_rules, attribution_text, reviewed_by, reviewed_on, status |
| `import_batch` | id, source_id, uploader_id, declared_rights (bool), file_ref, mapping jsonb, status, counts jsonb, started_at, finished_at |
| `import_row` | batch_id, raw jsonb, normalised jsonb, status (new, duplicate, error, held, published_as_draft), entry_id |
| `dedupe_candidate` | id, a_entry_id, b_entry_id, score, features jsonb, state (pending, auto_merged, rejected, merged), decided_by |
| `agent_job` | id, kind, source_id, budget_cap_minor, spent_minor, tokens, model, status, started_at |
| `draft_entry` | id, job_id, raw jsonb, evidence_quotes jsonb, source_urls[], confidence, cost_minor, state (staged, promoted, rejected) |
| `takedown` | id, requester_hash, entry_id, kind, state, log jsonb |

#### 4.2.6 `access`, `billing`, `ledger`

| Table | Columns / note |
|---|---|
| `plan` | key (free, subscriber_scope, listing_basic, listing_company, rank_city, download_extract), price_minor, currency, interval, features jsonb |
| `subscription` | user_id, plan_key, scope_path, scope_concept_id, state, period_start, period_end, provider_ref |
| `entitlement` | user_id, kind (list_access, subscription, extract), scope_path, concept_id, valid_from, valid_to, source (order or subscription) |
| `quota_counter` | subject (user id or address hash), key, day, count |
| `placement` | id, entry_id, scope_path, concept_id, level (area, city, country), slot, price_minor, starts_at, ends_at, state, label ("Sponsored") |
| `ad_campaign` / `ad_slot` | supplier ads in the relevant trade and place for free viewers; added with ads (P5); ad revenue sharing undecided (Q-R3) |
| `order` / `order_item` | buyer, items, amount, currency, state |
| `payment` | order_id, provider, provider_ref, amount, state, webhook_event_ids (idempotency) |
| `invoice` | order_id, number, tax lines |
| `ledger_account` | id, kind (platform, contributor, fees, tax, holding, refund_reserve), user_id, currency |
| `ledger_txn` | id, idempotency_key (unique), kind (sale, refund, payout, adjustment), ref, ts, memo |
| `ledger_posting` | txn_id, account_id, amount_minor (signed), currency. Constraint trigger: postings of a transaction sum to zero |
| `rate_phase` | id, name, starts_on, ends_on, rate_percent (50, 40, 30), cap_months |
| `sale` | id, order_id, kind (list, subscription, outreach, rank, extract, listing), scope, gross_minor, fees_minor, net_minor, ts, state |
| `sale_allocation` | sale_id, user_id, entry_count, share_percent, amount_minor |
| `payout` | id, user_id, amount_minor, method, state, ref, kyc_ok, hold_until |
| `kyc_record` | user_id, data_enc, state, checked_on |

#### 4.2.7 `outreach`, `moderation`, `volunteers`, `analytics`

| Table | Columns / note |
|---|---|
| `optin` | id, contact_id, channel, ts, method, wording_version, evidence_text, withdrawn_at |
| `suppression` | hash, channel, scope, ts. Global and survives re-imports |
| `message_template` | key, channel, language, body, provider_state (draft, submitted, approved), approved_by |
| `campaign` | id, buyer_id, scope_path, concept_id, template_key, channel, status, budget_minor, approved_by, country_code |
| `message` | id, campaign_id, entry_id, contact_id, channel, state (queued, sent, delivered, read, replied, failed, opted_out), provider_id, ts |
| `delivery_event` | message_id, event, payload, ts |
| `enquiry` | id, buyer_id, text, reply_to_enc, scope, created_at; `enquiry_recipient` (enquiry_id, entry_id, state) |
| `report` | id, entry_id, kind (closed, wrong, duplicate, fake, remove_my_data, suggest_edit, claim), text, reporter_hash, state, assigned_to, resolution, created_at |
| `suggested_edit` | id, entry_id, field_key, new_value, actor_id, state |
| `task` | id, kind (verify, survey, dedupe_review, area_review, translate), entry_id or place_id, assigned_to, state, due_at, result jsonb |
| `contributor_profile` | user_id, level, points, certificate_ids, display_name_public, reward_state |
| `reward` | user_id, kind (certificate, credit_visible, discount), granted_at |
| `audit_sample` | id, batch, entry_id, auditor_id, result, accuracy |
| `canary_entry` | entry_id, purpose (verifier test, scrape trace), planted_at |
| `rollup_cell` | country_code, place_path, concept_id, total, published, by_level jsonb, with_phone_pct, verified_12m, median_price_band, specialities_top jsonb, updated_at. Only non-empty cells |
| `event` | name, ts, subject_hash, props jsonb (privacy-respecting analytics) |

### 4.3 Sizing facts the schema relies on [M]

A realistic entry with per-field provenance, contacts, services and history cost about 1.7 KB (421 B entry, 701 B value meta, 151 B contacts, 125 B services, 345 B history). 10 million entries are about 17 GB, 100 million about 175 GB. List query 1.7 ms; country-wide category 50 ms; count of everything in a country 203 ms (so use `rollup_cell`); unscoped fuzzy name search 150 to 520 ms (so always scope). A free 500 MB database holds about 287,000 entries.

### 4.4 Roll-ups

`rollup_cell` rows exist only for non-empty cells. Each new or changed entry touches about 31 cells (7 place levels times about 4.5 concept levels) [I]; a worker updates them in batches every few minutes, with an exact nightly recount. Pages show an "as of" time. Place and list pages read counts from here, never `count(*)` over large sets.

### 4.5 Work packages for this section

| WP | Work | Size |
|---|---|---|
| P1.01 | Create modules and base models (`core`: ULID, soft delete, audit hash chain, change log, flags, country switch) | L |
| P1.02 | `places` and `taxonomy` tables and admin | M |
| P1.03 | `entries` core, child tables, value meta, verification tables | XL |
| P1.04 | Postgres grants (append-only roles), constraint triggers, migration tests up and down | M |
| P1.05 | `rollup_cell` and the refresher job | M |

---

## 5. Places, list types and the add-on registry

### 5.1 Place tree

- **Seed** the top levels from GeoNames and Overture divisions (about 194,000 places [U]: 250 countries, 3,900 first-level regions, 40,000 districts, 150,000 cities). Avoid GADM. Treat OSM-derived data as a share-alike layer kept apart. Country names in English and the local language; Urdu names for Pakistan down to city.
- **Generic levels** with a `local_level_label` ("province", "state", "division", "tehsil") so Pakistan, India, the UAE and others fit.
- **Areas below city** (road, street, neighbourhood, housing society) are contributor-proposed (C13). Rules: match the proposed name against existing areas in the same city using folded names and trigram similarity; a close match is shown as "Did you mean?"; moderators or an auto-rule approve; each approved area gets Urdu and English names; areas can be merged with a `merged` status and a redirect.
- **Path** is maintained by the service that creates a place; a check constraint verifies that `path` equals parent path plus slug.
- **Slugs** are unique per parent, ASCII (transliterated) for URLs; the Urdu name is a label. Slug collisions with list-type slugs are prevented by one reserved-slug table (section 8.2).
- **Pages** exist for every place with entries or children with entries. A place with nothing is reachable (C11) but is marked `noindex`.

### 5.2 List types and the creating rule

- Creating a list type in one place makes it exist (empty) everywhere (C11). In code this costs nothing: a list-place is a view (`concept` at `place_path`). Only `concept` is created.
- **Who may propose a list type** (Q-O3 default): any contributor proposes; moderators approve; synonyms are merged into labels of the existing concept; the creator of a new list type earns a small early-sales bonus (Q-O1 default, amount undecided, off until set).
- **Seed list types** come from `docs/DECISIONS.md` section 8 and `reports/Which lists pay.md` ranking: pilot types first (Sialkot surgical instrument makers, Sialkot football makers), then the owner's named list types (petrol pumps, schools, salons, bakeries, mobile stores, mobile repair, spare parts, furniture, medical stores, doctors, nurses, lawyers, bookshops, hardware, MRI, plumbers, Quran tutors [flag: not public, R19], fans and sanitaryware in Gujranwala, furniture in Faisalabad, hotels in Murree, eye doctors and hospitals, contractors, data scientists [consent, R18], factories and suppliers). The 113 proposed types from the platform catalogue stay out until the owner decides (Q-S8).
- **Natural scale** per list type (C25) sets the default level shown on place pages and the level at which the list is previewed and priced.
- **Topic lists** (apps, websites, books, tools) use a topic tree, built later (section 16).

### 5.3 Add-on registry (Tier 2)

- One `addon_template` per family with its `addon_field`s exactly as in `docs/LIST_AND_ENTRY_COMPONENTS.md` section 6: doctors, hospitals and clinics, labs and imaging, trades (plumbers, electricians, mobile repair), schools, tutors (including Quran), manufacturers and exporters, contractors, real estate agents, hotels, pharmacies and petrol pumps, retail and others.
- The registry validates add-on values on write (type, enum values, required for publish, price date rule) and drives: the entry form, the details block on the entry page, extra filters on the list page, the row descriptor, and the import mapper.
- Rules: fields can be added or deprecated, never changed in meaning; each change bumps the template version and is logged in `registry_version`.
- Fields flagged inference in the spec (section 10 item 9) are marked `provisional` and are checked against about five live listings per list type in a session with working page access (WP P2.12).

### 5.4 Work packages

| WP | Work | Size |
|---|---|---|
| P1.06 | GeoNames and Overture divisions loader; place path builder; Urdu names for Pakistan | L |
| P1.07 | Taxonomy loader (Overture, Foursquare, ISCO, own); labels and crosswalks; reserved slugs | L |
| P1.08 | Place proposal flow and approval screens | M |
| P1.09 | Add-on registry, validators, form generator, seeds for the 12 families | L |
| P1.10 | List-type proposal flow, `list_type_settings`, seed list types | M |

---

## 6. Entries, verification, claims and stewardship

### 6.1 Entry lifecycle

```
(created_via: contributor | import | agent | register | self)
     |
  [draft]  -- "Not verified yet": visible only to owner (once claimable) and moderators (R08)
     |   AI check (different source or method from the draft) passes, quality bar met
  [review] -- optional manual queue when the quality bar is borderline
     |
  [published] -- public, with level chips and dates
     |   report upheld / owner request / takedown
  [suppressed] -- hidden, reversible
     |
  [tombstoned] -- erased personal data, hashed identifiers kept
```

**Quality bar for publish** (default from Q-P6 and P14): two sources agree on name and place, or a register match; a working website or a phone that passed a lookup; business-level fields only; consent present for persons; list type allows publish (R18, R19, R20 flags). Counts on list pages read "N published, M awaiting verification".

### 6.2 What a draft may and may not do (P14 default)

| May | May not |
|---|---|
| Be seen and claimed by its owner; be seen by moderators and surveyors; be counted as "awaiting" | Be sold as verified; be counted as verified in paid statistics; be messaged (until opt-in); be indexed; earn payout; be exported |

### 6.3 Verification levels (D19, D20) as data

- Four labels as a registry (`check_label`): key, English and Urdu name, plain explanation, shape (solid thick, solid, dashed, dotted), whether it counts for payout, default validity in days. Defaults for validity are set in the pilot (Q-P7); until then: surveyor 12 months, owner 12 months, AI 6 months [I].
- An entry can hold several levels at once; they are independent chips, not a ladder. The list statistics show counts per level.
- Badge wording states what was checked, by whom and when ("Licence seen 2026-10"), never a bare "verified".

### 6.4 State machine and guards

States per field group: `none, pending, verified, expired, revoked`. Field groups: identity (name, register ID), location (address, pin), contact (reachable by relay), hours, services and prices, certificates.

| Transition | Guard (enforced in code and by constraint where possible) |
|---|---|
| AI check → verified at `ai` level | Check uses a source or method different from the draft's; records confidence; evidence text stored; cannot be called "verified" in any label |
| Surveyor → verified at `surveyor` level | Surveyor user is not `created_by` and not a steward-owner of that entry; method and evidence required; counted in an audit sample at the configured rate |
| Owner → verified at `owner` level | A successful claim exists (OTP to a stored contact, then optional documents) |
| any → expired | Scheduler drops it at `expires_at`; the chip falls back to the next level or "Not verified yet" |
| any → revoked | Moderator or an upheld report; reason stored |
| Payout eligibility | Only surveyor and owner events, with a re-check about 30 days later [S, analysis] |

Expired checks: when every check on a published entry has expired, the entry stays published for a grace period (default 90 days, queued for re-check) showing its past checks as dated and expired with the label "Not verified yet"; after the grace period it returns to draft (R08). Appendix C.3 repeats this rule.

Cheat controls: canary entries (fake shops only the platform knows) test verifiers; a quarterly audit of 385 records per batch [S, AI report]; weekly report of repeated contributor-verifier pairs; verifier accuracy under 80% suspends the verifier.

### 6.5 Claims

Flow: "Claim this business" → OTP to a stored phone or email (relay, value never shown) → optional documents (text description of what was seen, no photos at this stage) → owner-verified chip, claim state `claimed`, owner can edit allowed fields, add company page content if on the paid plan, and opt in to messaging. A claim dispute goes to the moderation queue. Self-listed entries earn nothing (R09).

### 6.6 Stewardship (C20, default from Q-P2)

A steward is a user holding a revocable grant on a place segment (and optionally one list type). Rights: verify and correct entries in the segment through the review queue (not unreviewed edits). No fee, no recruitment commission. The grant expires after 90 days of inactivity (`last_active_at`) and returns to the pool; disputes go to moderators. Stewards earn non-cash credit (levels, visible credit) and the same sale-time share as any contributor for entries they verified.

### 6.7 Duplicates and merging at the entry level

A merge writes `merge_map`, moves child records, re-points credit events (keeping the earliest `credit_event` as first-adder credit, D6), leaves a tombstone redirect at the old URL, and logs `change_log`. Un-merge is possible from the log.

### 6.8 Individuals, children and health (rules turned into behaviour)

| Case | Behaviour |
|---|---|
| `entity_type=person` | Consent record required before publish; area only (no street address); contact by relay only; no rank or position; share button hidden unless consent covers it; "Not you? Remove or correct" always visible |
| Child-facing list types (`is_child_facing`) | Not public until the feature flag opens it per country; relay-only variant: no personal name in shares, no share button, Report foregrounded |
| Health list types (`is_health`) | Prices only with a price date and only where `country_switch.health_prices_on`; no "cheapest"; no patient data |

### 6.9 Work packages

| WP | Work | Size |
|---|---|---|
| P1.11 | Publish state machine, quality bar, draft visibility rules | M |
| P1.12 | Verification events, projection, check-label registry, scheduler job for expiry | L |
| P1.13 | Claims (OTP via relay adapter stub), claim queue | L |
| P2.10 | Stewardship grants, inactivity expiry job, review queue | M |
| P1.14 | Merge service and redirects | M |
| P2.11 | Person, child and health rule gates | M |

---

## 7. Getting data in

### 7.1 Source register and licence gate (R21, R22)

Every import and every agent fetch references a `source` row. The gate rejects a batch or job when the source is `red`, when `allowed_uses` excludes the use, when personal-data rules are unmet, or when robots say no. Defaults: green = Overture (per-record licence), Foursquare Open Source Places (Apache-2.0), GeoNames (CC BY 4.0), owner submissions, FDA registration data (CC0 per the pilot research); amber = chamber lists, registers (SIMAP, SCCI, TDAP, DRAP and others; terms unverified, Q-S3), business websites; red = scraped Google Maps, Facebook, Baidu, Amap, logins, anti-bot bypass, bought lists. Attribution text is stored with the source and rendered in the entry provenance block and a sources page.

### 7.2 Importers (D1 to D5)

1. **Paste or CSV or Excel upload** (officer-pasted lists, association lists). Contributor declares the right to share (D11); that declaration is stored.
2. **Column mapper:** auto-guess from headers (English, Urdu, Roman Urdu), preview of 20 rows, saved mapping per source.
3. **Normalisation:** phones to E.164 (country from place), URLs canonicalised, names Unicode-normalised (NFC) with a separate fold (7.3), addresses split to structure where possible, place matched to the tree (proposal if unknown), concept matched through labels.
4. **Dedupe against existing data** (7.4); duplicates are held for review, not inserted twice.
5. **Result:** rows become `draft` entries with `created_via=import` and provenance; they earn nothing (R09) until verified.
6. **Bulk loaders** for Overture and Foursquare by region as background batches (about 5,000 rows per second realistic in production; 100 million entries would take about 83 hours as a batched job [I]).

### 7.3 Urdu, Arabic and Roman-Urdu folding (needed because Unicode normalisation does not unify these letters [M])

`fold(text)` is one tested function used for names, place names, concept labels and queries:

| Step | Rule |
|---|---|
| 1 | NFKC normalisation; lowercase Latin |
| 2 | Remove tatweel U+0640, ZWNJ U+200C, ZWJ U+200D (ZWNJ becomes a space where it separates words) |
| 3 | Remove harakat and other Arabic marks (U+064B to U+065F, U+0670) |
| 4 | Arabic yeh U+064A and alef maksura U+0649 → Farsi yeh U+06CC; Arabic kaf U+0643 → keheh U+06A9; heh U+0647 and heh goal U+06C1 → one form; heh doachashmee U+06BE handled as in the alias table |
| 5 | Alef variants U+0623, U+0625, U+0671 and madda U+0622 → alef U+0627 |
| 6 | Arabic-Indic and extended Arabic-Indic digits → ASCII digits |
| 7 | Collapse whitespace, strip punctuation |

Roman-Urdu and cross-script matching uses a curated alias table (concept labels and brand names) plus an ICU-transliteration key later [U]. A labelled set of 500 pairs from the pilot measures precision (target at least 95%).

### 7.4 Duplicate pipeline

1. **Block:** compare only entries sharing a place subtree and concept, or a phone hash, or a point within 100 m. At 1 million entries all-pairs would be 5e11; blocking to about 20 per block gives about 9.5 million comparisons [I]. Scoped lookup ran in 5 ms [M].
2. **Score:** phone match (strongest), proximity, folded-name similarity (trigram), alias table, address similarity.
3. **Decide:** auto-merge only above a high threshold; otherwise a review queue task (`dedupe_review`). Reviewer rejection of more than 10% of auto-merges triggers a threshold raise (early warning).
4. **Credit:** the earliest `credit_event` is kept (D6).
5. **Tooling path:** `pg_trgm` and `unaccent` at S0 to S1; Splink (MIT) when volume justifies; `dedupe` and `recordlinkage` only if easier at small scale.

### 7.5 Geocoding and pins

Addresses geocode through a hosted service only where its terms allow storing the result; otherwise the contributor or surveyor places the pin. Only latitude and longitude are stored with a precision class and source (R36). Map links (Google, Apple, OpenStreetMap; Baidu and Amap with GCJ-02 and BD-09 conversion at link time) are built at display time from the stored point. External place IDs are stored as identifiers only.

### 7.6 AI agent pipeline (D14, R35, T1 track)

| Element | Design |
|---|---|
| Jobs | Short, capped, one record each; kinds: draft from a permitted page, second-source check, freshness re-check |
| Isolation | No passwords, no production write access; writes only to `draft_entry` staging; promotion to `entry` is a separate service with the licence gate |
| Evidence | Every phone, address and name must be quoted verbatim from the fetched page or the draft is rejected; quotes and URLs stored |
| Fetching | Honest user-agent, per-site rate limits, robots respected, stop on first refusal, red sources blocked |
| Safety | Fetched pages are treated as data, never instructions (prompt-injection tests with planted instructions) |
| Cost | Per job, day and month caps; kill switch; every call logs tokens and cost with a job tag; alerts at 50% and 80% of the monthly cap; dashboard of cost per verified record (stop above USD 0.30 per verified record; accuracy under 90% on audit stops the job kind) [S, analysis] |
| Models | A provider-neutral wrapper; a cheap model for extraction, a mid-size one for hard cases; short capped jobs cost USD 0.03 to 0.10 all-in [S] |
| Output | `draft` only (R08). The second check must differ in source or method (R07) |

### 7.7 Data quality measurement

Audit samples per source and per verifier (385 records per batch); accuracy, freshness (expired chips share, early warning at 25%), coverage by place and concept, duplicate rate, zero-result search rate (early warning at 15%). All feed the analytics dashboards (section 18).

### 7.8 Work packages

| WP | Work | Size |
|---|---|---|
| P1.15 | Source register, licence gate, attribution | M |
| P1.16 | Import UI: paste/CSV/Excel, mapper, preview, normaliser | XL |
| P1.17 | `fold()` function, Urdu tests, query folding | M |
| P1.18 | Duplicate pipeline v1, review queue, merge integration | XL |
| P1.19 | Overture and Foursquare batch loaders by region | L |
| P2.13 | Geocoder adapter, pin entry UI (text fields), map-link helper including GCJ-02 and BD-09 | M |
| T1.01 | Agent job runner, staging, evidence-quote check, caps and kill switch | XL |
| T1.02 | Second-check job, injection tests, cost dashboard | L |
| T1.03 | Audit sampler and canary entries | M |

---

## 8. Public pages, templates and the design system in code

The prototype is the visual specification; `docs/DESIGN_SYSTEM.md` is the contract. This section says how they become server-rendered Django templates.

### 8.1 Template architecture (R25)

- **About a dozen base templates**, no hand-made pages: place, list (with the empty state), entry (basic and company sections), search results, topic list (later), static page, one form template, message form, and four or five dashboards. Full list with inputs and states in Appendix B.
- **Shared parts** as template includes (one file each): header, footer, breadcrumb, check label and key, share bar, action row, filter bar, result row, key facts, subscriber panel, notices, sponsored slot, ad slot, trust hero, area chips, view toggle, records list, "Something wrong?" section, empty state, quota notice.
- **Registries** read by the templates (Appendix C seeds): share channels, social platforms, check labels, list types and add-ons, plans and visibility, listing plans, strings, feature flags.
- **Template version** (`TEMPLATE_VERSION`, bumped by hand on a template change) is in cache keys and ETags (3.4). A change is tested on the fixed sample-page set (section 20.5) and rolled out to a small share first through a feature flag; rollback is the previous version.
- **Exceptions are rules.** "No share button for named individuals" is a field in `list_type_settings` and `entity_type` checks, not a different template.
- **Tokens.** The prototype's `:root` block (paper, surface, ink, ink-2, rule, control, accent, accent-ink, lock, ok, warn, bad, focus; type scale; 4 px space scale) is `app.css` and is the only place colour and size are defined. Dark theme: tokens redefined under `prefers-color-scheme` unless the user chose light, and under an explicit dark choice. Theme choice stored in a cookie and applied by an inline two-line snippet in `<head>` to avoid a flash.

### 8.2 URL scheme

Addresses follow the place tree and are the same for everyone (R05, C38). Full table in Appendix A.

| Page | Pattern | Example |
|---|---|---|
| World (home) | `/` | |
| Place at any level | `/{country}/{region}/…/` | `/pk/punjab/sialkot/` |
| List (list type at a place) | `/{place path}/{list-type-slug}/` | `/pk/punjab/sialkot/surgical-instrument-makers/` |
| Entry | `/e/{uid}/{slug}/` | |
| Search | `/search/?q=…&place=…` | |
| Urdu | `/ur/…` mirror of the above, with `hreflang` pairs | `/ur/pk/punjab/sialkot/` |
| Forms | `/add/`, `/claim/{uid}/`, `/wrong/{uid}/`, `/message/{uid}/`, `/enquiry/` | |
| Static | `/about/`, `/terms/`, `/privacy/`, `/plans/`, `/sources/`, `/how-checks-work/` | |
| Fragments | `/_f/…` (private, never indexed) | |
| Sitemaps | `/sitemap.xml`, `/sitemaps/{country}-{n}.xml` | |

Resolution rule for the last path segment: if a child place with that slug exists, it is a place; otherwise if a list type has that slug, it is a list. A **reserved-slug table** is checked whenever a place or list type is created so the two namespaces never collide. Country segment is the lowercase ISO code. The earlier `/p/…/l/…` scheme from the first build is replaced (WP P2.01).

Language: English unprefixed, Urdu under `/ur/`, so each language has a crawlable address (proposal Q-T1; the language cookie only chooses where the language switch sends you). Trailing slashes canonical.

### 8.3 Page specifications

#### 8.3.1 Place page (every level from world to area)

Order: breadcrumb (place only) → title (place name in page language) → scope line → roll-up trust line (counts from `rollup_cell`) → **places inside** (tiles with counts; at area level there are none) → **lists here** (list-type tiles with counts, grouped by family, ordered by natural scale then count) → near-you strip fragment (world and country pages) → widen steps (your place, region, country, world) → empty state when nothing exists → footer. A place with children but no entries shows children only. Titles: "{Place} – lists – AllLists".

#### 8.3.2 List page (list type at a place)

Order fixed by the design review (spec section 11 and design system 5):

1. Breadcrumb (place) and list-type tag.
2. Title "{List type} in {Place}" and one line of scope.
3. **Trust hero:** large count, trust bar (split by check type, patterned, with text legend), last-checked date, "N published, M awaiting verification", and the tap-to-open key explaining the four checks.
4. Primary action: "Send one enquiry to several" (subscribers; others see what it is and an upgrade line). Secondary: save or "Tell me when this list changes".
5. **Share bar** (registry driven): native Share, WhatsApp, Copy link; More: Facebook, email, LinkedIn, X. Copy link gives the clean address.
6. **Filters:** area chips (with counts), check type, extra filters from the add-on registry, sort (name, recently verified, ranked). Filters are links or HTMX swaps; focus stays; the new count is announced in one polite live region; "Clear filters" appears when any filter is on. Filter and sort URLs are `noindex` with canonical to the plain list.
7. **Results:** view toggle (list or cards, same fields). Each row: name and other-language name, type and area, up to three specialities and "+n more", check labels with date and age. Sponsored row (labelled, same checks and date) sits first within its slot; empty slot renders nothing. No position numbers, no lock boxes. First five rows, then "Show n more" within the stated free limit.
8. **Subscriber panel:** one panel naming what subscribers also see, built from fields that exist, one button.
9. **Ad slot** (free visitors only, labelled), below results.
10. **Add an entry, suggest an area, claim your business** (contributor funnel).
11. **Related lists:** same place other types, same type nearby, parent roll-up.
12. **Contributors and steward panel** (credit, CP9, C20).
13. **Provenance:** sources, licences, method, change-log link, as-of time.
14. **Something wrong?** One section: report, claim, suggest a correction, remove or correct my data.
15. Footer: "A check is a record, not a guarantee. Listings are not endorsements." Privacy and opt-out, report, terms.

Empty list: a designed page (what is missing, who can add, link to nearest filled list); `noindex,follow`; about 4 KB.

#### 8.3.3 Entry page (basic) and company page (paid)

Top to bottom (spec section 9 with design-review changes):

1. Breadcrumb: place, list, entry. 2. Name with other-language name, category, entity type, status. 3. Trust strip: check chips with level, who (display name), date; click for what was checked; claimed state; last updated. 4. Action row: **Message this business** (through AllLists; never a number), Request a quote (B2B types), Save, Share, Report. 5. Key facts (definition list, only rows with a value): area, hours with confirmed date, languages, year established, business type, OEM, how it was checked. 6. About: description, specialities, size. 7. Type-specific block from the registry. 8. Services and prices with price dates; products (stacked records, not wide tables). 9. Registrations and certifications with numbers and register links. 10. Ratings: hidden until real. 11. Rank in list, similar entries, other lists. 12. Provenance: source, licence, retrieval date, last three changes, contributor and steward credit. 13. **Something wrong?** (claim, suggest edit, report, remove my data). 14. Legal footer.

Subscriber-only (fragment, loaded after the shell): street address, exact pin, size, website, social pages, export markets, minimum order, prices with dates, certificate details. Free viewers see one subscriber-panel line instead (design system 5; spec section 11 table).

**Company page** is the same template with sections switched on by `listing_plan=company` (spec section 12): about the company, products and services with specifications and prices, certificates the company lists (each "Checked by AllLists" or "Company says"), capacity and facilities, terms and samples, questions buyers ask. Company-provided sections are labelled "Provided by the company" with the update date (R15). Row on the list carries a "Company page" tag. Individuals and children's services are not eligible (R18, R19). Updates and documents come later.

Entry states: closed (left-ruled notice, no message button, checks shown as past), moved, individual variant, child-facing variant, long names, many specialities, sponsored but unchecked (shows "Not verified yet" like any row).

#### 8.3.4 Search results, static pages, forms

- **Search:** section 10.1.
- **Static pages:** about, terms, privacy and opt-out, plans (what free and subscriber get, the one table), sources (attribution and licences), how checks work (the four labels), contributor rulebook (payout rules published as a trust asset, analysis 5.5).
- **One form template** driven by a form registry: add entry, add area, claim, suggest a correction, report, remove or correct my data. Same layout, labels above fields, errors in a summary at the top with links, no placeholder-only labels, 44 px targets, CSRF, rate limits, no CAPTCHA unless abuse appears.
- **Message form:** message to one business (and to many for subscribers), reply-to email, 2,000-character text, no phone numbers allowed in free text (pattern check), approved templates for outreach campaigns (section 13).

### 8.4 Interaction layer

| Behaviour | Implementation | Works without JS |
|---|---|---|
| Filters, sort, area chips, view toggle | Links and GET forms; HTMX swaps the results region; focus kept; live-region count | Yes (full page load) |
| Search as you type | HTMX `hx-trigger="input changed delay:150ms"` on the list-scoped search; keeps focus | Yes (submit) |
| Show n more | HTMX append of the next rows (within quota) | Yes (paged link) |
| Near-you strip, subscriber panel, ad slot, quota notice | HTMX `hx-trigger="load"` fragments under `/_f/` | Page works without them |
| Share | Native Share API where present; links otherwise; Copy link uses the clipboard API with a toast | Links work |
| Theme and language | Forms posting to a preference endpoint; cookie; no flash | Yes |
| Page transitions and row glide | View Transitions (CSS plus `view-transition-name` on rows); enhancement only | Instant change |
| Sticky header shadow | Scroll-driven animation, wide screens only | Static |
| Entrance and press effects | CSS only | None shown |
| Reduced motion | All motion off under `prefers-reduced-motion` | n/a |

JavaScript total (HTMX plus own script) stays under 30 KB compressed with no third-party scripts (R26). Only opacity and position animate, 150 to 220 ms.

### 8.5 Strings, language and right-to-left (R27)

- Use Django's gettext with `.po` files (replaces the first build's `strings.py` dictionary), because Urdu plural and grammar need whole-sentence strings with placeholders and plural forms. English is the source language.
- CI check: no string concatenation to build sentences; every user-visible template string goes through translation; missing Urdu falls back to English and is reported.
- Names appear in both scripts: the main name in the page language, the other below, each isolated (`<bdi>`) so punctuation stays put.
- Dates: "18 Sep 2026" with an age ("2 weeks ago"); Urdu month names in Urdu pages; Western digits everywhere (decided for consistency across Pakistan and the Gulf); locale grouping of large numbers decided with the first priced list (design open item 4).
- Urdu typography: body 18 px, line-height 1.95, titles 1.6, Naskh system fallback now; Nastaliq later if data cost allows (Q-S14). Native-speaker review of every Urdu string before launch.
- CSS uses logical properties only; a lint rule fails the build on `left`, `right`, `margin-left` and similar.
- Test every release at 320, 390 and 1100 px in English and Urdu, light and dark.

### 8.6 Search-engine rules in code (R23)

| Item | Rule |
|---|---|
| Titles | Unique: "{Name} – {List type} in {Place} – AllLists" for entries; "{List type} in {Place} – AllLists" for lists |
| Canonical | The plain address without tracking tags or filter parameters |
| Robots meta | `index,follow` only when the list has at least N verified entries (default 10, per-list-type override) and the country switch allows indexing; entries index only when verified and rich; everything else `noindex,follow`. Filters and sorts `noindex` |
| `robots.txt` | Does not block thin pages (a blocked page cannot show its `noindex`); blocks `/_f/`, `/admin/`, `/staff/`, search results |
| Sitemaps | Sharded at 50,000 URLs per file by country; only indexable pages; `lastmod` from the data stamp; sitemap index |
| Publishing throttle | New indexable pages per week capped by `country_switch.publish_cap_per_week` so a bug cannot publish a million pages overnight |
| Structured data | JSON-LD only for what is visible: list pages `ItemList` of names and areas; entry pages `LocalBusiness` or `Organization` with name and area (no locked fields, no contacts). Check how names-only pages qualify before relying on it (spec gap 4) |
| `hreflang` | English and Urdu pairs; `x-default` English |
| Same content to bots | No cloaking: bots get the same shell as visitors. Verify search-engine bots by reverse DNS for quota exemption only |
| Indexing watch | Track submitted versus indexed, impressions per page; early warning: under 20% indexed at day 90 |

### 8.7 Accessibility (design system section 8)

Contrast 4.5:1 text and 3:1 controls in both themes; 44 px targets; one `h1`, landmarks, skip link to results; every control keyboard reachable with visible 3 px focus ring; focus kept after filters; one polite live region; forced-colours keeps borders and pressed state; reduced motion honoured; patterns plus words, never colour alone. Automated checks (axe) in CI and manual screen-reader and low-end phone tests before launch.

### 8.8 Work packages

| WP | Work | Size |
|---|---|---|
| P2.01 | URL scheme, resolver, reserved slugs, redirects from the old scheme | M |
| P2.02 | Template system: base layout, shared includes, tokens, theme snippet, template version | L |
| P2.03 | Place page (all levels), world page, widen steps | L |
| P2.04 | List page (hero, key, filters, rows, cards, paging, subscriber panel, empty state) | XL |
| P2.05 | Shell and fragments split; cache headers; `/_f/` endpoints; ETag and template version | L |
| P2.06 | Entry page basic with all sections, states and registry-driven blocks | XL |
| P2.07 | Company page sections and moderation of provided content | L |
| P2.08 | Search results page and list-scoped live search | L |
| P2.09 | Forms: add, claim, correct, report, remove my data, message | L |
| P2.14 | gettext migration, Urdu strings, string lint, `<bdi>` handling, date and age formatting | L |
| P2.15 | SEO module: titles, canonical, robots meta, JSON-LD, hreflang, sitemaps, publish throttle | L |
| P2.16 | Static pages (about, terms, privacy, plans, sources, how checks work, contributor rulebook) | M |
| P2.17 | Accessibility, RTL and weight gates in CI; sample-page set | L |

---

## 9. Access, plans, quotas and anti-copying

### 9.1 Viewer plans (one table, R03)

Registry `plans_and_visibility`; the view layer calls `policy.visible(field, viewer, entry, scope)` and nothing else decides visibility.

| Field or feature | Free visitor | Subscriber |
|---|---|---|
| List row: names (both scripts), type, area, up to 3 specialities, check labels with date | Yes | Yes |
| Entry page: everything on the row plus area, hours, languages, year established, business type, OEM, how it was checked, message button | Yes | Yes |
| Street address, exact map pin, size, website, social pages, export markets, minimum order, prices with dates, certificate details | Locked (one panel names them) | Yes |
| One enquiry to many | No | Yes |
| List statistics: count, last checked, split by check type | Yes | Yes, plus with checkable certificate, verified in last 12 months |
| Phone, WhatsApp, email, individual's owner name | Never | Never |
| Advertisements | Shown | None |
| Download | No | No (only the heavy-price extract, R13) |

Website and social links are locked on the free view by default (Q-S13).

### 9.2 Scope rule (R04, C39)

Let `own` be the viewer's own place subtree (chosen place, else edge guess). For a list at place `P`:

- `P` inside `own` (or an ancestor chain of `own` that has the viewer's place as a descendant at the viewer's city level or below): free viewers see rows as in 9.1.
- `P` wider than `own` (region, country, world) or outside it: free viewers see a **names-only preview** (name, area, check label with date), capped at the preview limit; subscribers see the full list.
- Where the cutoff lies exactly (CP3, CP4, Q-S20): assumed default is "city and below free with limited fields; above city names only". Configurable per country and list type in `list_type_settings` and `country_switch`; the unit tests encode the default.
- Pricing of larger roll-ups follows decided direction: more for bigger lists (platform sets price, E2).

### 9.3 Quotas and anti-copying (P15)

| Control | Default [I; to calibrate in the pilot] |
|---|---|
| Free rows per list view | 5 at first, then "Show n more" up to the free limit |
| Free names per account per day | 100; anonymous per address 40 |
| Free list pages per address per day | alarm at 500 distinct list pages (early warning from the analysis); block above a hard cap |
| Pagination depth | Capped per account tier (L15) |
| Statistics instead of rows on free roll-ups | Yes |
| Planted canary entries | A set in each large list so copies are traceable (E10) |
| Terms of use | Forbid systematic copying; contract and trace entries are the protection since no database right is known in Pakistan [S] |
| CDN bot rules, reverse-DNS check for search bots | Yes |
| Price grows with list size | Yes (decided) |

Quota state is in `quota_counter`; the quota notice fragment says plainly how many free views remain and what subscription unlocks.

### 9.4 Listing plans and placements

- `listing_plan`: **basic** (free, every entry keeps a basic page for the claim funnel and to show checks, Q-S17 default) or **company** (paid; more sections). Charge for visibility, rank, badge, extra fields and leads, never for removing personal data (R39). Hidden versus lower-ranked for unpaid businesses is undecided; assumed default: everyone listed, decide on hiding only after traffic exists (Q-R1).
- **Placements** (paid rank, E15): sold per scope and level (assumed first product: city level, Q-O4), a small number of slots per list (default 2), fixed monthly price first (auction later), always labelled "Sponsored", with the same checks and date as any row, shown in a distinct slot, never altering the verification order. Revenue shares are undecided (Q-N2); default: platform revenue not in the contributor pool until decided. A "How this list is ordered" link is required once any placement is sold.
- **Ads** for free viewers: supplier ads in the relevant trade and place (assumed default), labelled, below results; none for subscribers; ad revenue sharing undecided (Q-R3).

### 9.5 Product catalogue (what can be bought)

| Product | Buyer | Notes |
|---|---|---|
| Subscription, by scope (place subtree and list type) | Buyers, researchers | Lower recurring fee for live, scope-based access (E7); optional platform-wide plan later (E8) |
| List purchase / time-limited full access | Buyers | View-only, no download (E6, E9) |
| Enquiry to many | Subscribers | Relay (section 13) |
| Outreach campaign | Buyers | Opt-in recipients, platform-sent, per country (P4) |
| Company page listing | Businesses | Per period |
| Paid rank placement | Businesses | Per scope and level |
| Extract (download) | Institutions, large buyers | About USD 1,000 minimum, scaled by size and freshness (Q-N1 default); staff-made, watermarked |
| Statistics report | Government and institutions | Aggregate only at first (R30) |

### 9.6 Work packages

| WP | Work | Size |
|---|---|---|
| P3.01 | Policy registry and `policy.visible()`; tests for the whole matrix | L |
| P3.02 | Scope rule and names-only previews; configurable cutoffs | M |
| P3.03 | Quotas, counters, notices, bot rules, canaries | L |
| P3.04 | Plans, subscriptions, entitlements (manual grant first) | L |
| P3.05 | Listing plans and company page gating | M |
| P5.01 | Placements, ad slots, labelled rendering | L |
| P5.02 | Statistics report product; extract job and watermarking | L |

---

## 10. Search, location and roll-ups

### 10.1 Search

**Pipeline:** fold the query (7.3) → look up concept labels (recall by synonym: "gas station" finds petrol pumps) and place names → scope to the current place subtree (or the whole country when the user asks) → trigram on folded names inside the scope for typos → rank by relevance and trust (published, higher check level, freshness); paid placements are inserted only in their labelled slot (R14).

| Item | Rule |
|---|---|
| Result groups | List types, places, entries (names-only for free viewers beyond their own place) |
| Zero results | The page says so and offers "Start this list" (every list exists but may be empty); logged for the zero-result rate |
| Scoped versus unscoped | Scoped about 5 ms; unscoped common-word search 150 to 520 ms at 1 million entries [M], so unscoped search is limited to concept and place name lookup until a search engine exists |
| Filters | Location, category, rating (when real), price band, verification level |
| Autocomplete | List-scoped live search on the list page; global suggestions of concepts and places in the header |
| Measurement | Zero-result rate (warning above 15% on a 200-query native-speaker test set), search p95 (scoped under 150 ms, unscoped under 500 ms) |
| Later | Meilisearch Community or OpenSearch when measured limits hit (S3) |

Collation: confirm the host's database collation handles Urdu text for trigram work before launch (analysis 5.1).

### 10.2 Automatic location (C39, Q-S20)

| Method | Implementation |
|---|---|
| Edge guess | Read `CF-IPCountry` always and city and region headers when the CDN setting is on; match to the place tree (city, else country). Used only for the near-you fragment and the widen steps; not stored; a guess is labelled as one |
| Browser location | A button "Use my exact location" (never an automatic prompt). The coordinates are sent once, matched to the nearest area using distance on stored centres (PostGIS at S1), and kept only in the session if the user chooses |
| Manual picker | Always available; a place search box with the tree; the fallback when the guess is wrong; the choice is saved in the session and, for signed-in users, the profile |
| Fallback chain | Chosen place → guessed city → guessed country → world, never an empty page |
| Rules | The page at an address is identical for everyone (R05); no redirect by location; the banner text is "We think you are in Sialkot. This is a guess from your connection and is not stored. Change place." (wording reviewed by counsel per country because an IP address can count as personal data) |
| Widen steps | Your place, region, country, world, each with its count; wider than the viewer's own place the scope rule (9.2) applies |
| MaxMind GeoLite2 | Alternative when no CDN: attribution required, not to be used to identify individuals [S] |

### 10.3 Roll-up reads

Place and list pages read `rollup_cell`. A page shows the "as of" time. Exact counts reconcile nightly. Where a cell is missing the page falls back to a limited live count with a bounded `LIMIT` and marks it approximate.

### 10.4 Work packages

| WP | Work | Size |
|---|---|---|
| P2.18 | Search service (fold, concepts, scope, trigram), result page, zero-result flow | L |
| P2.19 | Location service: edge guess, picker, exact-location button, widen steps, fragment | L |
| P2.20 | Roll-up reads on pages with as-of time | S |
| P6.01 | Search engine adapter behind the same service interface when measured | L |

---

## 11. Accounts, roles and permissions

### 11.1 Accounts

| Item | Design |
|---|---|
| Registration | Email and password with email verification (B6). Chosen public display name separate from the real name (shown on credit only if chosen). Google and Facebook sign-in later (B7) through `django-allauth`; ORCID for professionals later |
| Passwords | Argon2id through `argon2-cffi` [check licence and version], Django validators, breach-list check optional; legacy PBKDF2 accepted for migration only |
| Login protection | Throttle by account and address, lockout with timed release, generic error text; the first build measured 20 wrong logins in a row all answered with no limit [M], so this is a P3 gate |
| MFA | Mandatory (TOTP through `django-otp`) for admin, moderator, surveyor lead and payout roles; optional for others (B8 later for all) |
| Sessions | Secure, HttpOnly, SameSite=Lax cookies; rotation on login; idle timeout for staff roles; "sign out everywhere" |
| Profile | Language, theme, saved place, display name, contributor level, notification settings; theme and avatars beyond this are later (B9) |
| Account deletion | Free; personal fields removed; ledger and audit keep hashed ids |

### 11.2 Roles (resolves P3: names from both sources)

Roles are Django groups plus capability checks; many people hold several.

| Role | What they can do | MFA |
|---|---|---|
| Visitor | Browse free views | no |
| Registered user | Save, follow, suggest edits, report, add entries as draft, become a contributor | optional |
| Subscriber | Subscriber visibility and enquiry to many (through an entitlement, not a role flag) | optional |
| Buyer | Purchases, campaigns, dashboard | optional |
| Contributor (list maker or populator, B3) | Add entries and areas, import with declared rights, verification tasks | optional |
| Surveyor | Independent verification tasks (never on own entries); mobile task screens | optional; lead: required |
| Steward | Review queue for a segment | optional |
| Owner (claimed business) | Edit allowed fields, company page content if on the plan, opt in or out of messaging | optional |
| Moderator | Reports, claims, takedowns, area proposals, dedupe review, content moderation | required |
| Finance | Payout approval, reconciliation, rate phases (two-person rule) | required |
| Admin | Registries, switches, users, everything else except approving own payouts | required |

Appendix D is the full permission matrix. Rules: separation of duties (verifier is not adder; payout approver is not batch creator; admin cannot approve own payout); every staff action is audit-logged; per-object checks (an owner edits only their claimed entries).

### 11.3 Work packages

| WP | Work | Size |
|---|---|---|
| P3.06 | Registration, email verification, login throttling, lockout, reset, deletion | L |
| P3.07 | Roles, groups, capability checks, matrix tests (an authorisation test for every route) | L |
| P3.08 | MFA for staff roles, session policy | M |
| P6.02 | Social sign-in, optional MFA for all (later) | M |

---

## 12. Money: products, payments, the ledger and payouts

Nothing in this section is built until its gate (section 19). Manual payment recording is the first version; automatic payments and payouts come at P5. The step trigger (F4) must be decided before payouts are coded; the plan assumes date phases locked per entry.

### 12.1 Design rules

1. **Contributors are paid only when a list is sold** (R10). Credit accrues as `credit_event` rows with a locked phase; cash moves only at a sale.
2. **Double-entry ledger** in plain Postgres (R32): each sale is one transaction whose postings sum to zero across platform, contributors, fees, tax and the refund reserve. A constraint trigger rejects unbalanced transactions. The application role has no update or delete right on `ledger_*`.
3. **Integer minor units plus currency.** Rounding by largest remainder so cents are conserved.
4. **Idempotency** key on every sale and webhook; replays change nothing. Corrections are reversing transactions.
5. **One line per contributor per sale**, not per entry (32 million postings a month at 20,000 sales of 50,000-entry lists, versus about 1 billion per entry [I]).

### 12.2 Who earns what (decided steps, assumed mechanics)

| Rule | Value |
|---|---|
| Contributor rate | 50%, 40%, 30% by phase (F2). The phase is locked on the entry the day it is accepted (R11, F3 assumed) |
| Base | Net revenue = gross minus provider fees, tax collected, refunds and delivery pass-through, buyer-side first (R12, Q-S15 assumed) |
| Unit | Equal per verified entry (F5): a sold list's net amount is divided equally across its entries at surveyor or owner level and unexpired at sale time; each contributor receives that slice times the rate locked on the entry; the platform keeps the remainder. Imports, agent drafts and self-listed entries are not in the denominator and earn nothing (R09). Alternative bases are a configuration change, not code |
| Cap | After `cap_months` (default 36) an entry earns the lowest rate (30%) |
| Subscriptions (F8) | Net subscription revenue for the period is allocated across verified entries in the subscriber's scope, weighted 1.0 plus a freshness bonus (default 0.25) for entries re-verified in the last 90 days [I] |
| Outreach (F7) | A share applies at a lower rate than list sales; the figure is not decided; paid outreach billing cannot be switched on until `outreach_share_percent` is set |
| Paid rank and company pages | Outside the contributor pool until decided (Q-N2, P9 assumed) |
| Creator-of-list-type bonus | Small early-sales bonus (Q-O1); off until an amount is set |
| Refund hold | 14 days (F9): allocation lines are created as `held` and released after the hold; a refund exactly reverses them |
| Volunteers' early reality | Year-one pool is small (about USD 1,000 in the base case [I]); non-cash rewards carry the early period (section 14) |

### 12.3 Posting examples (to be turned into the first property tests)

List sale of USD 100 gross, provider fee USD 3, no tax, list has 10 verified entries from 2 contributors (6 and 4 entries), rates 50% and 40%:

- Net 97.00; slice per entry 9.70.
- Contributor A: 6 × 9.70 × 50% = 29.10; contributor B: 4 × 9.70 × 40% = 15.52; platform keeps 97.00 − 44.62 = 52.38.
- Postings: `+100.00` buyer clearing, `−3.00` fees, `−29.10` contributor A holding, `−15.52` contributor B holding, `−52.38` platform revenue; sum is zero. After the 14-day hold the holding lines move to each contributor's payable account.

### 12.4 Billing and payments

| Item | Design |
|---|---|
| Provider adapter | One interface: create checkout, verify webhook signature, fetch status, refund. First adapters: manual (staff records a bank or wallet receipt) and one local licensed gateway; a merchant-of-record or foreign-capable gateway for foreign buyers after the bake-off |
| Card data | Hosted payment pages only; no card data touches our servers |
| Webhooks | Signature verified, idempotent, stored raw, replay-safe |
| Orders | `order` → `payment` → `sale` → `ledger_txn`, each linked; entitlements granted by the sale, expiring with the period (E6) |
| Invoices and tax | Invoice numbers, currency, tax lines configurable per country (VAT, GST; the 2% digital-payments sales tax and a proposed 5% creator withholding in Pakistan are unverified and left as configuration) |
| Reconciliation | Daily ledger versus provider report; monthly full reconciliation; any difference is an alert (early warning for R08 ledger error) |
| Chargebacks | Recorded as reversing transactions; hold period absorbs most |
| Multi-currency | Store original currency; reporting currency conversion by dated rates |

### 12.5 Payouts

- Manual first: staff with MFA export an approved payout batch; a second finance user approves (two-person rule); the file goes to the wallet or bank rail; results are recorded back into the ledger.
- Automated disbursement through a local aggregator at P5; limits per wallet apply [S].
- KYC for contributors before first cash payout (F14); data encrypted; payout details in `kyc_record`.
- Minimum payout threshold and a published payout rulebook with notice periods (a trust asset).
- Counsel hour before any balance is held: whether holding contributor balances needs a payment licence and how worker status and withholding apply (open).

### 12.6 Property tests (Hypothesis) required before payouts

Postings sum to zero for every transaction; a replayed webhook changes nothing; a refund exactly reverses the sale and allocations; total payouts never exceed collections; the result is independent of entry order; rounding conserves every cent; locked phase is used even when phases change later; entries merged after crediting keep the earliest credit; ineligible entries never appear in allocations.

### 12.7 Work packages

| WP | Work | Size |
|---|---|---|
| P3.09 | Products, orders, payment adapter interface, manual payment recording, entitlement grant | L |
| P3.10 | Ledger tables, balance trigger, grants, idempotency, reversal | L |
| P3.11 | Rate phases, locked phase on entry, credit events, eligibility rules | M |
| P3.12 | Allocation engine for list sales with largest-remainder rounding and property tests | L |
| P5.03 | Subscription allocation with freshness weight | M |
| P5.04 | Local gateway adapter and webhooks; foreign adapter after bake-off | XL |
| P5.05 | Payout batches, two-person approval, KYC, reconciliation jobs | XL |
| P5.06 | Tax lines, invoices, multi-currency reporting | L |

---

## 13. Outreach and enquiries

### 13.1 Two products

1. **Enquiry to one or many** (subscribers, available from P3): the subscriber writes one message; the platform relays it to the entries that have an `optin` for relayed enquiries; the sender sees counts of delivered and answered, never contact data. Replies come back through the platform thread. Entries without an opt-in are counted as "not reachable yet" and prompt the claim funnel.
2. **Outreach campaign** (buyers, P4): a buyer chooses a list scope, an approved template and a channel; the platform sends; contacts stay hidden (R02, R29). This is the main revenue product but the riskiest (P8), so it launches after counsel and a measured test.

### 13.2 Rules

| Rule | Detail |
|---|---|
| Opt-in | Only entries with a recorded opt-in are messageable (D20.7). `optin` stores who, when, how (claim flow tick plus OTP), channel and wording version. Shops choose topics, channels and frequency (V7) |
| Country switch | Per country `outreach_on` and allowed channels, off until counsel clears it (R24, R29) |
| Channels | Buyer picks (G3): WhatsApp first through the official Business API via a provider; SMS and email through providers; in-app inbox; phone is not automated |
| Templates | Buyers choose approved templates; free text is limited and scanned for phone numbers, emails and URL shorteners to stop contact extraction (threat 4); supplier verified (V8) and message reviewed before the first send (G5) |
| Caps | Per shop (default 2 a week across all senders), per sender per day, quiet hours by recipient local time (UAE: 9am to 6pm and its do-not-call register [S]), global suppression list (hashed) surviving re-imports |
| Opt-out | One tap in every message; keyword STOP; effective immediately; suppression written first |
| Auto-pause | Opt-out above 2% or delivery failure above 10% pauses the sender and alerts staff |
| Tracking | Delivery, read, reply and order per campaign (G6) through provider callbacks into `delivery_event`; replies to the platform inbox (Chatwoot as a separate service, MIT) and relayed to the buyer in the thread |
| Costs | Provider cost passed through (Pakistan rates reported at USD 0.0473 marketing and 0.0100 utility per message [S, unverified at Meta]); price per reply or lead target decided with Q-N4 |
| Compliance | PECA spamming offence and PTA bulk SMS rules in Pakistan; UAE do-not-call; US TCPA and CAN-SPAM; EU and UK consent rules; counsel's written view per country and channel before any test (A7 table) |
| Never | Unofficial WhatsApp libraries; messaging agent-sourced numbers; messaging named individuals before consent and counsel |

### 13.3 Entry gate for P4 (from the delivery plan)

Counsel's written view for one country and channel; at least 100 opted-in shops; the test campaign delivered; opt-out works; reply rate measured against Google and Meta (Q-N4). If reply rate or cost fails, the module stays disabled.

### 13.4 Work packages

| WP | Work | Size |
|---|---|---|
| P3.13 | Enquiry relay v1: opt-in model, relay by email with masked reply-to, thread view, counts, anti-contact-extraction scan | L |
| P4.01 | Provider adapter interface; one WhatsApp provider and one SMS and email provider; sandbox mode | L |
| P4.02 | Opt-in capture in claim flow with OTP; suppression list; opt-out endpoints | L |
| P4.03 | Templates, supplier verification, campaign builder, caps and quiet hours, approval queue | XL |
| P4.04 | Callbacks, delivery tracking, inbox bridge, auto-pause, campaign report | L |
| P4.05 | Test-campaign measurement against Google and Meta (Q-N4) | M |

---

## 14. Contributors, volunteers and surveyors

### 14.1 Principles

Volunteers (students and others) contribute without upfront pay (CP1); the share arrives only when a list is sold, so motivation in year one is non-cash (CP9, agreed). Capacity is the real limit: at 1 to 3 minutes a record, 1 million records need 17,000 to 50,000 volunteer hours [I]; the pilot measures how many checks volunteers actually complete (P16, early warning under 30% of assigned checks done in two weeks).

### 14.2 Features

| Feature | Design |
|---|---|
| Onboarding | Guidelines, a short quiz, the declaration of right to share, the payout rulebook, the privacy rules for personal data |
| Contributor dashboard | Entries added, published, verified, awaiting; credit earned and pending share (shown only as accrued credit and a plain statement that cash arrives only when lists sell; never a promise); level; certificates |
| Task queue | Verification, survey, dedupe review, area review, translation tasks; mobile-friendly screens for surveyors (large targets, offline-tolerant form that saves a draft); each task logs minutes and outcome, which measures cost per record and completion rate |
| Surveyor workflow | Task shows what to confirm (phone reachable through the call tool, address visit, certificate seen), evidence text, outcome; never assigned to the contributor who added the entry (R07); canary tasks inserted to test accuracy |
| Levels and rewards (CP9) | Reputation levels by verified contributions and audit accuracy; certificates and CV letters; visible credit on entries and segments; free or discounted access in proportion to verified contributions ("give to get"), implemented as non-cash `access_credit` entries in the ledger separate from money; exact rewards are the owner's choice (Q-R5) |
| Segments | Stewards (section 6.6) |
| Social campaigns (C32) | Each contributor gets a `ref` code; pre-written share messages carry `utm_source`, `utm_medium=share`, `utm_campaign=list_share` or `entry_share` and `ref`; opt-in, chosen display name only. Rules from the campaign research: no rewards for sharing itself (platform rules), reward verified contributions, label any benefit #ad where required, never message people who did not opt in |
| Integrity | Collusion report (repeated contributor-verifier pairs), audit samples, canaries, verifier accuracy under 80% suspends |
| First-volunteer offer | Fee plus share versus share only is tested in the pilot (Q-S15); a small fixed fee per audited record can be switched on if volunteers do not finish checks |

### 14.3 Work packages

| WP | Work | Size |
|---|---|---|
| P2.21 | Contributor onboarding and dashboard | M |
| P2.22 | Task engine and surveyor mobile screens with time logging | XL |
| P2.23 | Levels, certificates, access credit, visible credit | L |
| P2.24 | `ref` codes, share messages, campaign stats | M |
| T1.03 | Audit sampler, canaries (shared with the agent track) | M |

---

## 15. Back office: moderation, takedown, erasure, audit

### 15.1 Staff console (`/staff/`) on top of Django admin

Django admin is used for raw data edits by admins. The staff console gives queue-based screens (the actual work):

| Queue | Contents | Who |
|---|---|---|
| Dedupe review | Candidates above the review threshold, side by side with folded names and phones | Moderator, steward |
| Area proposals | Proposed areas with nearest matches | Moderator |
| Claims | Pending claims, evidence text, decision | Moderator |
| Reports | Closed, wrong, duplicate, fake, remove my data, suggest edit | Moderator |
| Takedown and erasure | Requests with the legal basis, deadline, log | Moderator, admin |
| Verification audit | Sampled records, auditor result, accuracy per verifier and per source | Surveyor lead |
| Imports | Batches, row errors, held rows, source licence status | Moderator |
| Source register | Terms, tier, permissions, review date | Admin |
| Company-page content | Provided sections awaiting moderation; "Company says" certificates | Moderator |
| Payouts and reconciliation | Batches, approvals, differences | Finance |
| Switches and registries | Country switches, feature flags, registry editors with version bump | Admin |
| Users and roles | Grants, suspensions, MFA reset | Admin |

### 15.2 Moderation policy in code

Agents write facts, never opinions; a free report-and-correct flow exists on every entry (R17); takedown log kept; claims about certificates show "Company says" until checked; no claims about other businesses; suppression is reversible, tombstone is not.

### 15.3 Erasure and personal data

Deletion replaces personal fields with a tombstone, removes contacts, deletes sensitive store rows, suppresses re-import by hash, and keeps hashed identifiers in the audit trail. Subject-access requests export what we hold about a person. A written breach runbook (detect, contain, assess, notify within the legal window) is tested once before launch.

### 15.4 Audit log

Hash-chained; covers logins, role changes, verification, claims, exports, ledger and payout actions, registry and switch changes, staff views of sensitive data. A nightly job re-verifies the chain and alerts on a break.

### 15.5 Work packages

| WP | Work | Size |
|---|---|---|
| P1.20 | Staff console shell with queue framework; dedupe and area queues | L |
| P2.25 | Claims, reports, suggested edits queues and decisions | L |
| P3.14 | Takedown, erasure, subject-access flows; consent register UI | L |
| P3.15 | Audit-chain verifier job and alerts | S |
| P3.16 | Company-page moderation queue | M |

---

## 16. Later modules (schemas reserved now, built when their gate opens)

| Module | Plan | Gate |
|---|---|---|
| **Reviews and rankings** (C19, J8, Q-P3) | Verified users only, one per user per entry, owner reply, authenticity statement, fake-review detection, clearly separate from paid rank; compliance with the FTC rule and EU disclosure rules. Until built the entry page shows nothing for rankings and the rating columns stay empty | Rules decided (Q-P3) and counsel |
| **Personal lists** (I1 to I8) | Private by default; shared with chosen people or public; partially public (title visible); collaborative lists; templates; never sold, exported or used for recommendations without consent; health data excluded from any suggestion; suggestions need opt-in | After the public product is proven |
| **Topic lists** (C27, Q-S4) | A topic tree and topic list template for apps, websites, books, tools and public figures; monetised by sponsored placement, affiliate links and ads, not by list sales; same check labels where applicable | After the pilot, topics chosen by the owner |
| **Talent list** (data scientists, global) | Design now, launch after a pilot of about 50 consented people and counsel review (consent, area only, relay) | Counsel and pilot |
| **Commerce layer** (V1 to V8) | Stage 2: demand intelligence from aggregate events and roll-ups; product requests (request for quotation) tables; test panels. Stage 3: direct offers and shipping through partners for payments and logistics; verified factory and shop accounts (KYC). Each stage is gated on evidence (reply rates, repeat buyers, shops asking to order) | P4 results and P5 |
| **Government and institutions** (E16, Q-N3) | Aggregate statistics reports first; full lists only with a disclosed data-sharing policy | Policy decision |
| **API** (E11) | None at launch (R31); custom extracts case by case; a keyed read API later with quotas and watermarking | After P5 |
| **Maps** | Text areas table now; MapLibre with self-hosted PMTiles later; China conversion at link time only | After text-only scope |
| **Other later items** | Social sign-in (B7), MFA for all (B8), profile customisation (B9), activity logs (K4), gamification (K5), business view for suppliers (K6), product-level local search (J6), favourites (J7), offline service worker (N4), platform-wide subscription (E8), affiliate links (H4), notifications of similar lists (I7), real-time analytics (N12), distributed media storage (N7, not needed without media) | Each when its decision and evidence exist |

Schema reservations now: `entry.rating_*`, `entry_concept`, `topic` placeholder concept kind, `personal` namespace in the reserved-slug table, `event` table for demand intelligence, `media` documented as unused (R01).

---

## 17. Security and privacy controls

### 17.1 Controls by threat (analysis 6.2), with the module that carries each

| # | Threat | Control | Module or WP |
|---|---|---|---|
| 1 | Exposed database password and secret key still valid; public repository | **Rotate everything before any deployment** (database, app secret, `mysecretkey`, GitLab token, key passphrase, anything pasted in chats); secrets only in environment or secret store; GitHub secret scanning and push protection (already stopped one push); history rewrite does not undo copies | P0.01 |
| 2 | Account takeover | Argon2id, throttling, lockout, MFA for staff and payout roles | P3.06, P3.08 |
| 3 | Scraping of paid data | Section 9.3 controls; quota alarms | P3.03 |
| 4 | Buyer extracts contacts through outreach | Contacts never leave the server; replies relayed; approved templates; free-text scan | P3.13, P4.03 |
| 5 | Fake entries and shops to earn credit | Imports and self-listings earn nothing; payout needs independent verification and a re-check; canaries | P1.11, P3.11 |
| 6 | Contributor and verifier collusion | Verifier never the adder; audits; weekly pair report | P2.22 |
| 7 | Ledger tampering or error | Append-only, no update rights, balance trigger, hash-chained audit, two-person payout approval, monthly reconciliation | P3.10, P5.05 |
| 8 | Injection and cross-site scripting | ORM parameterised queries, template auto-escape (no `\|safe` without review), CSP, CI scan; the legacy `frontend/app.js` that wrote names with `innerHTML` is deleted | all |
| 9 | Prompt injection through fetched pages | Agents hold no credentials and no production write access; planted-instruction tests | T1.02 |
| 10 | Personal-data breach | Field encryption, separate sensitive store and database role, least privilege, no personal data in logs, restricted exports, breach runbook | P3.14 |
| 11 | Spam through outreach; number banned | Opt-in gate, caps, templates, suppression, country switch | P4 |
| 12 | Abuse of cheap-to-call heavy endpoints (the first build's `/recommend` took 169 ms per call unauthenticated [M]) | Remove or cache; rate limit by address; cap work per request; no such endpoint is carried over | P0.02 |
| 13 | Payment fraud and chargebacks | Hosted payment pages, manual confirmation first, refund hold | P3.09 |
| 14 | Takedown and defamation | Facts only; free correct-or-remove flow; moderation queue; takedown log | P2.25, P3.14 |
| 15 | Supply chain | Locked versions (lock file), Dependabot, `pip-audit` in CI, pinned GitHub Action versions (update `setup-python@v3`) | P0.05 |

### 17.2 Web security baseline

| Item | Setting |
|---|---|
| HTTPS | Everywhere; HSTS once stable; secure cookies; `SECURE_PROXY_SSL_HEADER` behind the proxy (already set) |
| Content-Security-Policy | `default-src 'self'; img-src 'self'; script-src 'self'; style-src 'self'` (inline CSS only through a hash or nonce while inline styles remain); no third-party origins; `frame-ancestors 'none'`; report-only first, then enforce |
| Other headers | `X-Content-Type-Options`, `Referrer-Policy: same-origin` (set), `Permissions-Policy` denying camera, microphone, and geolocation except on the exact-location button page, COOP |
| CSRF | Django middleware on all POST forms and HTMX requests (token header) |
| Output | Auto-escape on; names and addresses isolated with `<bdi>`; no raw HTML from users; no Markdown rendering at launch |
| Uploads | No file uploads except CSV import (size cap, parsed in a worker, row-level validation); CSV exports prefix formula characters |
| SSRF | Agent fetchers and link checkers use an allow-list, resolve and block private address ranges, cap response size and time |
| Webhooks | Signature, timestamp tolerance, idempotency, source address allow-list where the provider publishes one |
| Rate limits | Login, registration, search, list pages, enquiries, every unauthenticated endpoint |
| Database | Separate roles: app (no update or delete on append-only tables), migration, read-only reporting, sensitive-store role; connection over TLS; encryption at rest from the host plus field encryption; backups encrypted |
| Logging | Structured; a scrubber removes contact values, emails and tokens; no personal data in logs; IP stored only as a rotating-salt hash for quotas |
| Admin | Admin URL not guessable and behind MFA; staff network allow-list optional |

### 17.3 Privacy by design

Consent register for every messageable contact and every individual; data minimisation; separate storage for sensitive fields (personal mobiles, owner names of individuals, ID facts, child and health data); retention schedule (messages and delivery events 12 months, logs 90 days, audit log kept; proposal); deletion workflow with suppression; per-country rules through `country_switch`; cookie use limited to session, CSRF and preferences, analytics are server-side hashed events (counsel confirms that no consent banner is needed per country); Pakistan has no enacted general data-protection law in the 2026 reviews, which is a window and not a safe harbour [S]; the EU trader-traceability question (publishing trader contacts versus hidden contacts) is settled by counsel before any EU consumer launch (spec gap 5).

### 17.4 Required before launch (analysis 6.3, copied as gates)

Secret rotation done and old secrets confirmed dead; MFA mandatory for the roles above; rate limits everywhere; audit log hash-chained; consent register in place with per-country switch off by default; deletion and correction request form with a tested tombstone deletion that suppresses re-import; a restore performed and timed; terms, privacy notice and takedown route written, with counsel's view before any messaging test; `security-review` skill run plus a manual pass on authorisation and the ledger.

### 17.5 Work packages

| WP | Work | Size |
|---|---|---|
| P0.01 | Rotate all exposed secrets; verify old ones dead; push protection on | S |
| P0.02 | Remove legacy Flask app, legacy `frontend/`, unused schema files; fix README | S |
| P3.17 | CSP, headers, rate-limit middleware, log scrubber, encrypted fields and key versioning | L |
| P3.18 | Sensitive store and database roles; append-only grants | M |
| P3.19 | `security-review` run and fixes; authorisation tests for every route | M |

---

## 18. Operations: environments, deployment, monitoring, backups, costs

### 18.1 Environments

| Environment | Purpose | Notes |
|---|---|---|
| Development | Local and cloud sessions; Docker Compose with Postgres 16 and the same extensions; seed data from `seed_demo` | CI uses a real Postgres service, never SQLite for the checks that matter (the first build's tests ran on SQLite, which cannot test constraints, locking or extensions) |
| Staging | Production-like; synthetic and pilot data; used for release rehearsal, load tests and the sample-page set | Auth and payment sandboxes |
| Production | Real users | Country switches default off |

### 18.2 Deployment

- A tagged commit is built into an image or a release directory; deploy by one script (build, migrate with a pre-check, collect static files, restart web then worker, smoke test, roll back on failure). No file pasting.
- Process layout: reverse proxy (Caddy or Nginx) → Gunicorn → Django; a worker process for Procrastinate; a scheduler for periodic jobs (Appendix F). `systemd` units or a container platform.
- Migrations: forward-only in production; a migration that locks a large table is split into safe steps; a reverse is tested in CI.
- Static files by WhiteNoise behind the CDN with hashed names; no remote fonts or scripts.
- Feature flags and country switches control exposure; risky changes go to a small share first.

### 18.3 Monitoring and alerts

| Need | Tool and thresholds |
|---|---|
| Errors, uptime, metrics | Sentry, UptimeRobot, Grafana Cloud free tiers first [S] |
| Database | Slow-query log, connection count, replication lag, table and index growth, vacuum |
| Jobs | Queue depth, failure rate, age of oldest job |
| Data quality | Accuracy by source (audit), freshness (expired chips share, alert above 25%), coverage, duplicate rate (reviewer rejection above 10% of auto-merges) |
| Search | p95 latency, zero-result rate (alert above 15%) |
| AI spend | Every call logs tokens and cost with a job tag; daily cap; alerts at 50% and 80% of the monthly cap; cost per verified record |
| Outreach | Delivery failure above 10% and opt-out above 2% alerts and auto-pause |
| Money | Daily reconciliation; any difference alerts |
| Abuse | One address or account fetching over 500 distinct list pages a day |
| Indexing | Submitted versus indexed; alert under 20% indexed at day 90 |
| Verifier quality | Accuracy under 80% |

### 18.4 Backups and recovery

| Stage | Availability goal | Data loss at most | Restore within |
|---|---|---|---|
| S0 to S1 | 99% (about 7 h a month) | last nightly dump | 1 day |
| S2 | 99.5% (about 3.6 h) | 15 minutes (WAL archive) | 4 hours |
| S3 to S4 | 99.9% (about 43 min) | 5 minutes | 1 hour; replica failover |

Nightly logical dump plus continuous WAL archive in a different account or region; **restore drill every quarter** (a 2.4 GB database restored in 34 seconds with four jobs [M]); a drill that is skipped is an alert.

### 18.5 Performance budgets (also Appendix L)

List page of 25 rows about 11 KB compressed (hard ceiling 18 KB), entry page 7 KB (12 KB), empty list 4 KB (6 KB); inline CSS 2 KB (3 KB); no fonts or images; JavaScript under 30 KB compressed. Latency: cached page from the edge to a phone in Lahore, Karachi or Dubai under 200 ms [I]; uncached origin p95 under 300 ms; database query p95 under 50 ms. The build fails above the hard ceilings.

### 18.6 Cost guardrails (analysis 8.2)

Servers are not the cost; AI drafting and verification are. Infrastructure per month: S0 about USD 1 to 32, S1 37 to 157, S2 217 to 900, S3 1,775 to 6,110, S4 14,610 to 52,620 [I, with sourced anchors]. AI drafting at S2 could be USD 2,500 to 8,300 a month, so every stage has a spend cap set from measured cost per verified record. Zero-spend path: S0 and the early part of S1 at zero to under USD 50 a month; what cannot be zero is the domain, counsel, a payment collection route and a card that foreign hosts accept.

### 18.7 Per-country switches (R24)

`country_switch` is the control panel for law and rollout. For each country: browsing is on; indexing, selling, outreach (and which channels), ads, named individuals, health prices and child-facing services are each off until a person with the admin role records who cleared it, when, and a legal note. Pakistan is first; UAE, Saudi Arabia and others open only after counsel (analysis 7.1 table).

### 18.8 Runbooks to write before launch

Deploy and rollback; restore from backup; secret rotation; breach response; takedown request; payout cycle; reconciliation difference; sender banned or auto-paused; AI spend runaway; template rollback; indexing drop; scraper surge.

### 18.9 Work packages

| WP | Work | Size |
|---|---|---|
| P0.03 | Docker Compose dev stack with Postgres 16, extensions | S |
| P0.04 | CI on real Postgres; drop Python 3.9; update action versions; blocking lint; coverage floor | M |
| P0.05 | Lock file, Dependabot, `pip-audit`, `bandit`, secret scan in CI | S |
| P0.06 | Deploy script, systemd units, reverse proxy config, static IP, DNS and CDN setup, staging | L |
| P0.09 | `session-start-hook` so cloud sessions install and test | S |
| P3.20 | Monitoring, alerts, AI-cost and quota dashboards | M |
| P3.21 | Backup, WAL archive and a timed restore drill | M |
| P3.22 | Runbooks (18.8) | M |
| P6.03 | Load tests at 3 times peak; recovery drill; read replica; country partitions; Splink | XL |

---

## 19. Delivery plan: phases, work packages, first 90 days

### 19.1 How the work is run

- **Phase gates.** A phase starts only when the previous exit criteria are met (or the owner waives one in writing in the decision log). This is the "phased, evidence-gated" rule from the decisions: build only to P3 before a buyer pays for a sample; P4 only after counsel; P5 only after paying buyers.
- **Slices.** The plan is also cut by evidence need. **Cut M** work packages are the minimum to reach the first paid sample; **Cut L** can follow it. The **pilot slice** is smaller still: what the 200-firm pilot (gate 1) needs.
- **Sizes** are person-days of an experienced engineer directing AI coding agents with human review of anything touching security, money or data rules: S up to 2, M up to 5, L up to 10, XL up to 18 days [I]. Estimates are plus or minus 50%.
- **Pull-request flow.** One branch per work package or small group; every pull request runs CI and the `code-review` skill; security, money, consent and encryption code gets two human reviewers and the `security-review` skill; each pull request names the rules (R01 to R40) it touches and updates `docs/DECISIONS.md` if a decision changed (R38).
- **Definition of done** is in section 20.6.

### 19.2 Effort summary

| Phase | Work packages | Person-days (all) | Person-months (all) | Person-days (cut M) | Person-months (cut M) |
|---|---|---|---|---|---|
| P0 Foundations | 10 | 34 | 1.6 | 34 | 1.6 |
| P1 Data core | 20 | 179 | 8.5 | 159 | 7.6 |
| P2 Public site | 25 | 226 | 10.8 | 151 | 7.2 |
| P3 Accounts, access, money v1, safety | 22 | 162 | 7.7 | 150 | 7.1 |
| P4 Outreach | 5 | 53 | 2.5 | 0 | 0 |
| P5 Growth money | 6 | 71 | 3.4 | 0 | 0 |
| P6 Scale | 3 | 33 | 1.6 | 0 | 0 |
| T1 Agent track | 3 | 33 | 1.6 | 0 | 0 |
| **Total** | **94** | **791** | **37.7** | **494** | **23.5** |

Pilot slice (the 21 packages P0.01 to P0.05, P0.07, P0.08, P0.10, P1.01 to P1.04, P1.09 to P1.12, P1.15 to P1.18, P1.20): **146 person-days, about 7.0 person-months**.

How this compares with `reports/Project analysis.md` (20 to 40 person-months in total, 10 to 18 to the first revenue-capable system): the plan's total sits at the top of that range because it specifies more than the analysis costed (staff console, task engine, string tooling, security gates, runbooks). The sale-capable cut (23.5) is above the analysis' 10 to 18, so the analysis figure is optimistic or this plan carries scope that the first sale does not need. Two ways to close the gap if money or time is short: run gate 1 on the pilot slice and Django admin only (7.0 person-months, and the pilot needs only a spreadsheet-grade front end), and defer P2.14 to P2.17 polish items to after the first paid sample. Treat every number as plus or minus 50%.

### 19.3 Non-code work that gates the code

| Item | Gate it feeds | Owner |
|---|---|---|
| Rotate exposed secrets (database password, app secret, tokens, passphrase) | P0 and any deployment | Founder with engineer |
| Paper checks: open the TDAP brochure, SIMAP, SCCI, DRAP and Trade Portal pages; email each body for written terms; one counsel hour each for Pakistan and the UAE; trace 50 firms in DRAP, FDA, EUDAMED, IAF CertSearch | Gate 0, before P1 import of register data (Q-S3) | Founder |
| Choose one first trade in writing (Q-S16) | P1 seeds and P2 pilot pages | Founder |
| Pilot of 200 firms verified by evidence tier; log minutes and cost; show a 50-firm sample to 20 to 30 buyers; offer makers a paid badge | Gate 1 (weeks 2 to 8): at least 2 of 5 targeted buyers deposit at 3 times cost per entry; 5 payers or 5 foreign buyers send enquiries; cost at most USD 1.50; at least 90% correct at 30 days. Kill: no buyer pays after 10 conversations, or cost above one third of price | Founder and volunteers |
| Paid maker pilot: 20 to 30 makers offered a badge at USD 100 to 300 for 3 months | Gate 2 (months 3 to 6): at least 2 of 20 pay | Founder |
| Counsel's written view for one messaging country and channel | P4 entry | Founder |
| Payment route chosen (local gateway; foreign route) | P3.09 live and P5.04 | Founder |
| Step trigger F4 and contributor share definition decided | P3.11 and P5.05 | Founder |
| Native-speaker review of Urdu strings | P2.14 exit | Founder |
| Counsel hour on contributor balances and "verified" badge wording | P5.05 and launch | Founder |

### 19.4 Phases and work packages

### 19.5 Phase P0: Foundations

**Entry:** Owner go-ahead; stack confirmed (Q-S9, Q-S18). **Exit:** Secrets rotated; CI runs on Postgres; schema v1 migrates from an empty database; staging deploy works from a tag.

| WP | Work | Needs | Size | Cut | Acceptance test |
|---|---|---|---|---|---|
| P0.01 | Rotate every exposed secret; confirm old ones dead; secret scanning and push protection on | - | S | M | Old database password, app secret and tokens rejected by their services; GitHub reports no open secret alerts |
| P0.02 | Delete the legacy Flask draft remnants (`Data Schema`, `Deployment Script`, old schema files, unused endpoints); rewrite README current-state section | - | S | M | Repository has no unused or insecure legacy file; README matches reality |
| P0.03 | Docker Compose dev stack with Postgres 16, `pg_trgm`, `unaccent` | - | S | M | `docker compose up` then `manage.py migrate` works from empty |
| P0.04 | CI on a real Postgres service; Python 3.11, 3.12, 3.13; blocking lint; coverage floor; update action versions | P0.03 | M | M | CI green; a deliberately broken constraint test fails on Postgres but would pass on SQLite |
| P0.05 | Lock file, Dependabot, `pip-audit`, `bandit`, secret scan in CI | P0.04 | S | M | Each scan runs in CI and fails on a seeded finding |
| P0.06 | Deploy script, process units, reverse proxy, static IP, DNS and CDN, staging environment | P0.01 | L | M | A tagged commit deploys to staging and rolls back by script; HTTPS valid; no pasted files |
| P0.07 | Module skeletons, settings split (dev, staging, prod), import-boundary check | - | M | M | Forbidden import fails CI; each module has `services.py` |
| P0.08 | Decision sprint: stack, hosting, code licence, provider shortlist; book counsel; record in decision log | - | S | M | `docs/DECISIONS.md` updated; counsel booked |
| P0.09 | `session-start-hook` so cloud sessions install dependencies and run tests | P0.04 | S | M | A fresh cloud session can run `pytest` with no manual steps |
| P0.10 | `LICENSE` (Apache-2.0 proposal), data-terms placeholder, CONTRIBUTING, pull-request template with decision-log checklist | P0.08 | S | M | Template shows on new pull requests |

### 19.6 Phase P1: Data core

**Entry:** P0 done. **Exit:** 1,000-record pilot imported; duplicate precision at least 95% on 500 labelled pairs; provenance on every field; audit log works; backfill of Urdu fold tests green.

| WP | Work | Needs | Size | Cut | Acceptance test |
|---|---|---|---|---|---|
| P1.01 | `core` module: ULIDs, soft delete, audit hash chain, change log, feature flags, country switch, encryption helpers | P0.07 | L | M | Audit chain verifies; tamper test breaks it; flags and switches editable |
| P1.02 | `places` and `taxonomy` tables, admin, reserved-slug table | P1.01 | M | M | Create place and concept in admin; slug collision refused |
| P1.03 | `entries` core, child tables, value meta, verification tables | P1.02 | XL | M | Schema matches section 4; migration up and down in CI |
| P1.04 | Postgres roles and grants (append-only), constraint triggers, migration tests | P1.03 | M | M | App role cannot update or delete append-only tables; unbalanced ledger test fails as designed (when ledger lands) |
| P1.05 | `rollup_cell` and refresher job | P1.03 | M | M | Counts match a full recount within one refresh; nightly exact recount job |
| P1.06 | GeoNames and Overture divisions loader; place path builder; Urdu names for Pakistan | P1.02 | L | M | Pakistan to city loaded with both scripts; path constraint holds |
| P1.07 | Taxonomy loader (Overture, Foursquare, ISCO, own); labels and crosswalks | P1.02 | L | M | Synonym lookup finds one concept for petrol pump, gas station, fuel station |
| P1.08 | Place proposal flow and approval screens | P1.06 | M | M | Proposed area matched to existing; approve and reject paths tested |
| P1.09 | Add-on registry, validators, form generator, seeds for 12 families | P1.07 | L | M | Invalid add-on rejected; form renders from registry; deprecation tested |
| P1.10 | List-type proposal flow, `list_type_settings`, seed list types | P1.09 | M | M | Seed types present; new type appears empty in every place |
| P1.11 | Publish state machine, quality bar, draft visibility | P1.03 | M | M | Draft hidden from public; counts read published and awaiting |
| P1.12 | Verification events, projection, check-label registry, expiry scheduler | P1.03 | L | M | Guards (adder never surveyor; AI differs from draft) enforced; expiry drops chip |
| P1.13 | Claims with OTP via relay adapter stub; claim queue backend | P1.12 | L | L | Claim grants owner chip; dispute path tested |
| P1.14 | Merge service and redirects | P1.03 | M | M | Merge keeps earliest credit; old URL redirects; un-merge from log |
| P1.15 | Source register, licence gate, attribution | P1.03 | M | M | Red source blocked; attribution renders |
| P1.16 | Import UI: paste/CSV/Excel, mapper, preview, normaliser | P1.15, P1.17 | XL | M | Pasted 1,000-row list becomes draft entries with provenance |
| P1.17 | `fold()` and query folding with Urdu tests | P1.01 | M | M | Measured pairs in section 7.3 unify; unit tests for every rule |
| P1.18 | Duplicate pipeline v1, review queue, merge integration | P1.16, P1.14 | XL | M | Precision at least 95% on 500 labelled pairs |
| P1.19 | Overture and Foursquare batch loaders by region | P1.15 | L | L | One region loads as drafts with licences; resumable |
| P1.20 | Staff console shell with queue framework; dedupe and area queues | P1.18, P1.08 | L | M | Moderator resolves a candidate and an area proposal; audit rows written |

### 19.7 Phase P2: Public site

**Entry:** P1 done. **Exit:** 20 to 30 quality pages server-rendered with budgets enforced; empty pages noindex; design-review must-fix list closed; Urdu reviewed.

| WP | Work | Needs | Size | Cut | Acceptance test |
|---|---|---|---|---|---|
| P2.01 | URL scheme, resolver, reserved slugs, redirects from the old scheme | P1.02 | M | M | Every address in Appendix A resolves; old `/p/` addresses redirect |
| P2.02 | Template system: layout, shared includes, tokens, theme snippet, template version | P1.01 | L | M | Sample pages render in light and dark; version appears in headers |
| P2.03 | Place page (all levels), world page, widen steps | P2.02, P1.05 | L | M | World to area drill-down works; counts from rollups |
| P2.04 | List page: hero, key, filters, rows, cards, paging, subscriber panel, empty state | P2.02, P1.11 | XL | M | Matches section 8.3.2 order; 25-row page within budget |
| P2.05 | Shell and fragments split; cache headers; `/_f/` endpoints; ETag and template version | P2.04 | L | M | Two different viewers get byte-identical shell; fragments are private |
| P2.06 | Entry page with all sections, states and registry blocks | P2.02, P1.09 | XL | M | All states in section 8.3.3 covered by sample pages |
| P2.07 | Company page sections | P2.06, P3.05 | L | L | Company sections labelled and dated; basic page shows one prompt line |
| P2.08 | Search results page and list-scoped live search | P2.04, P1.17 | L | L | Scoped query under 150 ms on 1 million entries; zero-result flow |
| P2.09 | Forms: add, claim, correct, report, remove my data, message | P2.02, P1.13 | L | M | One form template; error summary links to fields |
| P2.10 | Stewardship grants, inactivity expiry, review queue | P1.20 | M | L | Grant expires after inactivity; edits go through review |
| P2.11 | Person, child and health rule gates | P1.11 | M | L | Individual page lacks share and street address; child-facing not public without flag |
| P2.12 | Check provisional add-on fields against about five live listings per list type | P1.09 | M | M | Provisional flags cleared or fields dropped; note in spec |
| P2.13 | Geocoder adapter, pin entry, map-link helper with GCJ-02 and BD-09 | P1.03 | M | L | Link built from stored point; China conversion unit tests |
| P2.14 | gettext migration, Urdu strings, string lint, `<bdi>`, date and age | P2.02 | L | M | No concatenated sentences; Urdu dates; RTL screenshots pass |
| P2.15 | SEO module: titles, canonical, robots meta, JSON-LD, hreflang, sitemaps, publish throttle | P2.04, P2.06 | L | M | Thin and empty pages noindex; sitemap shards at 50,000; throttle caps weekly publish |
| P2.16 | Static pages including plans, sources, how checks work, contributor rulebook | P2.02 | M | M | Pages exist and match decisions |
| P2.17 | Accessibility, RTL and weight gates in CI; sample-page set | P2.04, P2.06 | L | M | axe clean; no left or right CSS; weight ceilings enforced |
| P2.18 | Search service (fold, concepts, scope, trigram), result page, zero-result flow | P1.17, P1.07 | L | L | Gas station finds petrol pump lists; typo tolerated |
| P2.19 | Location service: edge guess, picker, exact-location button, fragment | P2.05 | L | L | Guess labelled; picker overrides; no redirects |
| P2.20 | Roll-up reads with as-of time on pages | P1.05 | S | M | As-of text shown; fallback bounded |
| P2.21 | Contributor onboarding and dashboard | P1.13 | M | L | New contributor completes onboarding and sees dashboard |
| P2.22 | Task engine and surveyor mobile screens with time logging | P1.12 | XL | M | Surveyor completes a task on a phone; minutes logged; canary task works |
| P2.23 | Levels, certificates, access credit, visible credit | P2.22 | L | L | Level rises with verified work; credit visible on entries |
| P2.24 | `ref` codes, share messages, campaign stats | P2.04 | M | L | Share link carries tags and ref; stats count visits |
| P2.25 | Claims, reports and suggested-edits queues and decisions | P1.20 | L | M | Each queue resolves items with audit rows |

### 19.8 Phase P3: Accounts, access, money v1, safety

**Entry:** P2 done; one buyer agreed to look at a sample. **Exit:** Manual payment recorded; ledger property tests green; restore drill done; security review passed; first paid sample sold.

| WP | Work | Needs | Size | Cut | Acceptance test |
|---|---|---|---|---|---|
| P3.01 | Policy registry and `policy.visible()`; tests for the whole visibility matrix | P2.04 | L | M | Every cell of Appendix C plans table has a test |
| P3.02 | Scope rule and names-only previews; configurable cutoffs | P3.01 | M | M | Own place full, wider names only; cutoffs configurable |
| P3.03 | Quotas, counters, notices, bot rules, canaries | P3.01 | L | M | Quota exhausted message; canary seeded; alarm at 500 pages a day |
| P3.04 | Plans, subscriptions, entitlements (manual grant first) | P3.06 | L | M | Staff grants a subscription; viewer sees subscriber fields and no ads |
| P3.05 | Listing plans and company-page gating | P3.04 | M | L | Company sections only for paid plan |
| P3.06 | Registration, email verification, throttling, lockout, reset, deletion | P0.07 | L | M | 20 wrong logins lock the account; reset and delete work |
| P3.07 | Roles, groups, capability checks; authorisation test per route | P3.06 | L | M | Matrix in Appendix D tested; route inventory test fails on an unprotected route |
| P3.08 | MFA for staff roles; session policy | P3.06 | M | M | Staff cannot reach console without MFA |
| P3.09 | Products, orders, payment adapter interface, manual payment recording, entitlement grant | P3.04 | L | M | Staff records a receipt; order paid; entitlement active |
| P3.10 | Ledger tables, balance trigger, grants, idempotency, reversal | P1.04 | L | M | Unbalanced transaction rejected; update and delete refused |
| P3.11 | Rate phases, locked phase on entry, credit events, eligibility | P3.10, P1.12 | M | M | Later phase change does not alter locked entries; ineligible entries earn nothing |
| P3.12 | Allocation engine with largest-remainder rounding; property tests | P3.11 | L | M | All properties in section 12.6 green |
| P3.13 | Enquiry relay v1 with opt-in, masked reply-to, thread, anti-extraction scan | P3.04, P1.13 | L | M | Sender sees counts only; phone numbers in text blocked |
| P3.14 | Takedown, erasure, subject-access flows; consent register UI | P2.25 | L | M | Erased person leaves tombstone, suppressed on re-import |
| P3.15 | Audit-chain verifier job and alerts | P1.01 | S | L | Break detected and alerted |
| P3.16 | Company-page moderation queue | P2.07 | M | L | Provided content reviewed before showing |
| P3.17 | CSP, headers, rate-limit middleware, log scrubber, encrypted fields and key versioning | P0.07 | L | M | CSP enforced; log scrub test; contact values encrypted at rest |
| P3.18 | Sensitive store and database roles; append-only grants in staging and production | P1.04 | M | M | Separate role cannot read other store; verified on staging |
| P3.19 | `security-review` skill run and fixes; authorisation tests | P3.07 | M | M | Findings fixed or recorded with owner sign-off |
| P3.20 | Monitoring, alerts, AI-cost and quota dashboards | P0.06 | M | M | Alerts fire in a drill |
| P3.21 | Backups, WAL archive, timed restore drill | P0.06 | M | M | Restore performed and timed; result in runbook |
| P3.22 | Runbooks (section 18.8) | P3.21 | M | M | Each runbook exists and a dry run was done for deploy, restore and rotation |

### 19.9 Phase P4: Outreach

**Entry:** P3 done; counsel's written view for one country and channel; at least 100 opted-in shops. **Exit:** Test campaign delivered; opt-out works; reply rate measured against Google and Meta (Q-N4); go or no-go.

| WP | Work | Needs | Size | Cut | Acceptance test |
|---|---|---|---|---|---|
| P4.01 | Provider adapter interface; one WhatsApp provider and one SMS and email provider; sandbox | P3.13 | L | L | Sandbox send and callback round-trip |
| P4.02 | Opt-in capture in claim flow with OTP; suppression list; opt-out endpoints | P3.13 | L | L | Opt-out suppresses globally and survives re-import |
| P4.03 | Templates, supplier verification, campaign builder, caps, quiet hours, approval queue | P4.01, P4.02 | XL | L | Caps and quiet hours enforced by tests |
| P4.04 | Callbacks, delivery tracking, inbox bridge, auto-pause, campaign report | P4.03 | L | L | Auto-pause at 2% opt-out and 10% failure |
| P4.05 | Test-campaign measurement versus Google and Meta | P4.04 | M | L | Report with cost per reply for each channel |

### 19.10 Phase P5: Growth money

**Entry:** At least 5 paying buyers; step trigger (F4) decided. **Exit:** Automated payments; payouts reconcile to the cent for two cycles.

| WP | Work | Needs | Size | Cut | Acceptance test |
|---|---|---|---|---|---|
| P5.01 | Placements, ad slots, labelled rendering | P3.05 | L | L | Sponsored rows labelled and capped; ads only for free viewers |
| P5.02 | Statistics report product; extract job and watermarking | P3.09 | L | L | Extract has planted trace entries; no user download route |
| P5.03 | Subscription allocation with freshness weight | P3.12 | M | L | Property tests extended |
| P5.04 | Local gateway adapter and webhooks; foreign adapter after bake-off | P3.09 | XL | L | Webhook replay safe; sandbox payment reconciles |
| P5.05 | Payout batches, two-person approval, KYC, reconciliation jobs | P3.12 | XL | L | Two payout cycles reconcile to the cent |
| P5.06 | Tax lines, invoices, multi-currency reporting | P5.04 | L | L | Invoices numbered; tax config per country |

### 19.11 Phase P6: Scale

**Entry:** A measured limit (latency, size or cost). **Exit:** Load test at 3 times peak passes; recovery drill meets targets.

| WP | Work | Needs | Size | Cut | Acceptance test |
|---|---|---|---|---|---|
| P6.01 | Search engine adapter behind the same service interface | P2.18 | L | L | Same tests pass on both backends |
| P6.02 | Social sign-in; optional MFA for all | P3.08 | M | L | ORCID and Google sign-in work |
| P6.03 | Load tests at 3 times peak; recovery drill; read replica; country partitions; Splink | P3.21 | XL | L | Targets in section 18.4 met |

### 19.12 Phase T1: Agent track (parallel to P1 to P3)

**Entry:** P1.15 licence gate and P1.03 schema exist. **Exit:** Audit accuracy at least 90% on a 385-record sample; cost per verified record under USD 0.30.

| WP | Work | Needs | Size | Cut | Acceptance test |
|---|---|---|---|---|---|
| T1.01 | Agent job runner, staging, evidence-quote check, caps, kill switch | P1.15 | XL | L | Draft without verbatim evidence rejected; cap stops a runaway job |
| T1.02 | Second-check job, injection tests, cost dashboard | T1.01 | L | L | Planted instruction ignored; cost per verified record shown |
| T1.03 | Audit sampler and canary entries | T1.01 | M | L | 385-record sample produced; canaries seeded |

### 19.13 First 90 days (after the owner's go-ahead)

| Weeks | Block | Work packages |
|---|---|---|
| 1 | Rotate secrets; README; decision sprint (stack, hosting, licence, providers); book counsel; Django and Postgres in CI | P0.01 to P0.05, P0.08, P0.10 |
| 2 to 3 | Place tree and taxonomy import; schema v1; entry core with provenance and audit log; CSV import; Urdu folding with tests; experiment 1 (gap check) | P0.07, P1.01 to P1.04, P1.06, P1.07, P1.09, P1.15, P1.17 |
| 4 | Duplicate detection v1 and review queue; experiment 2 (385-record audit) | P1.14, P1.16, P1.18, P1.20 |
| 5 to 6 | Server-rendered list, entry and place pages; noindex rules; sharded sitemaps; page-weight gate; scoped search; English and Urdu strings with plural rules; fix design-review items | P2.01 to P2.06, P2.14, P2.15, P2.17 |
| 7 | Verification events and claim flow; load the 1,000-record pilot (one trade, one city) | P1.11 to P1.13, P2.22 |
| 8 to 9 | Accounts, roles, staff MFA; rate limits; consent register; deletion workflow; names-only tiers, quotas, canaries; staging; first load test | P3.01 to P3.03, P3.06 to P3.08, P3.14, P3.17, P3.18 |
| 10 | Ledger v1 with property tests; manual payments; payment route chosen | P3.09 to P3.12 |
| 11 | Backup and restore drill; monitoring and AI cost caps; security review | P3.19 to P3.22 |
| 12 | Soft launch of 20 to 30 indexable pages; start the 90-day indexing watch; show a buyer the sample | P2.16, sample set |
| 13 | Review against exit criteria; go or no-go for P4 | gate review |

This calendar is the analysis' 90-day plan re-mapped to work packages. It fits a one-to-two engineer team only on the pilot slice plus the first half of the cut; the whole cut M takes longer (section 19.2). If the calendar and the effort disagree, the effort wins and the calendar stretches.

### 19.14 Critical path and parallel tracks

Critical path to the first paid sample: P0.04 (CI on Postgres) → P1.03 (schema) → P1.12 (verification) and P1.16 to P1.18 (import and duplicates) → P2.04 and P2.06 (list and entry pages) → P3.01 (policy) → P3.09 to P3.12 (orders and ledger) → P3.21 restore drill. Parallel tracks: the agent track T1 (needs only P1.15 and P1.03); Urdu review and string work (P2.14) alongside page work; surveyor screens (P2.22) alongside pages; counsel and register paper checks alongside P0 and P1; payment route selection alongside P3.

### 19.15 Rules for changing the plan

A change to a rule (section 1) or to a phase exit criterion is recorded in `docs/DECISIONS.md` first. A work package may be split but not dropped without a note. New work packages take the next free number in their phase. Sizes are re-estimated at each phase entry from measured velocity.

---

## 20. Testing, CI and definition of done

### 20.1 Layers

| Layer | What | Tools |
|---|---|---|
| Unit | Folding, rate-phase maths, state-machine guards, policy table, share registry, map-link conversions, string lint | pytest |
| Integration | Real Postgres 16 with `pg_trgm`, `unaccent` (not SQLite); migrations up and down; grants; triggers | pytest-django, CI service container |
| Rule tests | One test per testable rule R01 to R40 (20.2) | pytest |
| Data quality | Labelled duplicate pairs (500), audit accuracy per source, noindex rules, page-weight ceilings, Urdu query set (200) | pytest and scripts |
| Ledger | Property tests (12.6) plus monthly reconciliation job tests | Hypothesis |
| Security | `pip-audit`, `bandit`, secret scan, CSP check, authorisation test for every route (a route-inventory test fails if a route has no declared access level), `security-review` skill | CI |
| Browser | Playwright: sample-page set at 320, 390, 1100 px, English and Urdu, light and dark, keyboard path, axe | Chromium |
| Load | List page, search and import at 3 times expected peak before each stage | k6 or Locust |
| Restore | Quarterly drill, timed | script |

### 20.2 Rule-to-test map

| Rule | Test (name pattern) |
|---|---|
| R01 | `test_no_media_fields`, CSP header test (`img-src 'self'`), no `<img>` or `<video>` in rendered pages |
| R02 | `test_contacts_never_rendered`: seed contacts, crawl every page type as every viewer, assert no value or hash appears; assert no serializer exposes them |
| R03 | `test_visibility_matrix`: every cell of the plans table |
| R04 | `test_scope_rule_own_vs_wider` for each level |
| R05 | `test_shell_identical_for_all_viewers` (byte comparison of the cacheable shell for free, subscriber, different guessed places) and `test_no_location_redirect` |
| R06 | `test_labels_only_four`; template lint rejects bare "verified" and "AI verified" |
| R07 | `test_surveyor_not_adder`, `test_ai_check_needs_different_source`, `test_check_expires` |
| R08 | `test_draft_hidden_and_counts_published_awaiting` |
| R09 | `test_ineligible_entries_earn_nothing` (import, agent, self-listed) |
| R10 | `test_no_cash_before_sale` |
| R11 | `test_phase_locked_on_entry` |
| R12 | `test_net_revenue_base_and_36_month_cap` |
| R13 | `test_no_user_export_route`; extract job test for watermarks |
| R14 | `test_sponsored_labelled_capped_and_checks_unchanged` |
| R15 | `test_company_sections_labelled_dated`; certificate shows "Company says" until checked |
| R16 | `test_ads_free_only` |
| R17 | `test_something_wrong_on_every_page_and_free` |
| R18 | `test_person_rules`: consent required, area only, no share, no rank |
| R19 | `test_child_facing_not_public_without_flag` |
| R20 | `test_price_requires_date`; health prices off by default |
| R21 | `test_record_needs_source_licence_date_consent`; blocked-source record cannot publish |
| R22 | `test_red_source_rejected` for import and agent |
| R23 | `test_robots_meta_rules`, `test_sitemap_only_indexable`, `test_filters_noindex_canonical`, `test_robots_txt_allows_thin_pages` |
| R24 | `test_country_switch_defaults_off`; selling, outreach, indexing respect switches |
| R25 | `test_template_version_in_cache_key`; test adds a share channel as one registry row and sees it on list, entry and closed entry |
| R26 | Weight gate (Appendix L); no third-party origin in any page |
| R27 | CSS lint for physical properties; Urdu screenshot test; string-concatenation lint; digits test |
| R28 | `test_no_not_stated_and_no_position_numbers` |
| R29 | `test_outreach_requires_optin_and_switch`; caps, quiet hours, opt-out, auto-pause tests |
| R30 | `test_government_gets_aggregates_only` |
| R31 | `test_no_public_api_routes` |
| R32 | `test_ledger_append_only_and_balanced` against Postgres grants and trigger |
| R33 | Schema test: personal lists default private (when built) |
| R34 | CI secret scan; `test_settings_refuse_start_without_secret` |
| R35 | `test_agent_rejects_unquoted_values`, `test_agent_cannot_write_production`, `test_agent_cap_stops_job` |
| R36 | `test_only_lat_lon_stored`; map-link tests including GCJ-02 and BD-09 |
| R37 | `LICENSE` present check |
| R38 | Pull-request template check (manual review) |
| R39 | `test_removal_flow_free` |
| R40 | Each pricing or access rule has an emitted event (event-name test) |

### 20.3 CI pipeline (Appendix I has the steps)

On every pull request: lint (blocking flake8 and a physical-CSS check), type check where annotated, tests on Postgres for Python 3.11, 3.12 and 3.13, coverage floor on new code, migration up and down, dependency and secret scans, import-boundary check, page-weight gate on the sample-page set, string lint, and the accessibility run. Releases additionally run the browser suite, the load smoke test and the security scan.

### 20.4 Test data

`seed_demo` stays as a small human-readable dataset; a generator builds synthetic data at 1 million entries (Zipf-skewed, Urdu, Latin and Roman-Urdu names, 5 countries) for performance tests, as in the analysis; a labelled set of 500 duplicate pairs and a 200-query Urdu search set are built in the pilot and kept in the repository (names only, no personal data).

### 20.5 Sample-page set (every template change is checked on it)

One list page and one entry page for each of: every launch list type, empty, one result, many results, closed entry, moved entry, individual, child-facing, health with prices, sponsored and unchecked, company page, very long names, many specialities, Urdu, dark theme, free viewer, subscriber, over-quota viewer, wider-than-own-place list. Plus place pages at world, country, city and area levels, search with zero results, the forms, and the static pages.

### 20.6 Definition of done

A work package is done when: automated gates pass; a human reviewed it (two reviewers for ledger, authorisation, consent and encryption); the migration runs forward and back; logs contain no personal data; the audit log covers any new staff or money action; the rule tests for rules it touches exist and pass; the page-weight and accessibility gates pass for pages it touches; the Urdu strings exist or are listed as pending review; `docs/DECISIONS.md` and `docs/REQUIREMENTS.md` reflect any decision; and the build log records it.

---

## 21. Owner-decision register and assumed defaults

Coding starts without waiting for these. For each, the plan assumes the default shown, built so that changing it is configuration or a small change, not a rewrite. "Needed by" is the first work package that cannot be finished without the answer.

### 21.1 From the decision log (open items)

| Open item | Needed by | Assumed default in this plan | Ref |
|---|---|---|---|
| Backend stack, hosting, front-end approach | P0 | Django 5.2, PostgreSQL, server-rendered, HTMX; hosting with managed Postgres accepting the founder's payment method | Q-S9, Q-S18 |
| Domain and name | P0.06 | AllLists; confirm alllists.org ownership; price alllists.com; fallback ListAtlas | Q-S19 |
| First country, city and trade | P1.10 (seeds), pilot | Pakistan, Sialkot, surgical instrument makers as a verified-supplier register | Q-S16, Q-N6, Q-P1 |
| How the 50, 40, 30 steps work | P3.11 | Date phases, locked on each entry at acceptance | F3, F4 |
| Contributor share definition | P3.12 | Net revenue, buyer-side first, 36-month cap then lowest rate | Q-S15 |
| What a "not verified yet" entry may do | P1.11 | Hidden from the public; visible to owner and moderators; public with badge from AI-checked up, above the quality bar | Q-P6 |
| Requirements and duration of each verification level; who pays surveyors | P1.12 | Validity surveyor 12 months, owner 12, AI 6; measured in the pilot; volunteers unpaid, fixed fee per audited record switchable | Q-P7, P16 |
| Download price basis | P5.02 | Scaled by size and freshness, USD 1,000 minimum | Q-N1 |
| Paid ranking: how sold, which level, who earns | P5.01 | City level first, fixed monthly price, two slots, outside the contributor pool | Q-N2, Q-O4 |
| Which ads free users see; ad revenue sharing | P5.01 | Supplier ads in the relevant trade and place; sharing decided later | Q-R3 |
| Hidden or lower-ranked for unpaid businesses | P3.05 | All listed; free basic page; decide after traffic exists | Q-R1 |
| Government policy | P5.02 | Aggregate statistics only | Q-N3 |
| First outreach channels | P4.01 | Opt-in, platform-sent, WhatsApp first, after counsel | Q-N5 |
| Which agent sources are used and excluded | P1.15, T1.01 | Chambers, associations, owner submissions, registries and open data in; scraping Google Maps, Facebook and Baidu Maps out until counsel advises | Q-P4 |
| Segment ownership | P2.10 | Revocable stewardship, review queue, 90-day inactivity expiry, no fee, no recruitment commission | Q-P2 |
| Who writes reviewer rankings | Module in section 16 | Verified users, one per user, owner reply, separate from paid rank; hidden until built | Q-P3 |
| New list type or area earnings | P3.11 | Platform prices; creator of a list type earns a small early-sales bonus (off until an amount is set) | Q-O1 |
| Code versus data licence | P0.10 | Apache-2.0 for code; data under terms | A3 |
| Register terms and bulk access | Gate 0, P1.19 | Email each body for written terms; start with facility and school registers, not individuals | Q-S3 |
| Pilot city and first source pack | P1.19 | One city: eye hospitals and eye doctors first, then schools, then contractors (service-provider pack; the Sialkot trade pilot is the cluster pack) | Q-P1 |
| Named individuals | P2.11 | Consent only, area only, relay contact | Q-S2 |
| Housing-society partnership | later | One-society pilot; opt-in link; no fee | Q-P2 |
| Child-facing and Quran tutors | P2.11 | Not public until safeguarding designed; schools and centres first | Q-S2 |
| Talent list timing | section 16 | Design now; launch after about 50 consented people and counsel | |
| API | section 16 | None at launch | |
| Per-listing fees for individuals | none | None at launch | |
| Health-sector rules | P2.11 | Adopt the report's health rules before collecting any price | Q-S1 |
| Counsel | P3 and P4 gates | Book before any messaging test, list of individuals, health or child data, talent list | |
| Which platform-catalogue list types join the seed | P1.10 | The report's top ranked group; delay children's services, health data, named individuals | Q-S8 |
| Sign-off of component spec | P1.03 | Approve `docs/LIST_AND_ENTRY_COMPONENTS.md` after reading its section 10; core frozen for version 1 | Q-S12 |
| Website and social links public or locked | P3.01 | Locked on the free view | Q-S13 |
| Design system sign-off, Urdu style, number format | P2.14 | Naskh fallback, Western digits, grouping with first priced list | Q-S14 |
| Company page scope and price | P3.05, P2.07 | Unpaid keep a basic page; sections per spec section 12; price tested in the pilot | Q-S17 |
| Automatic location wording and where free ends | P2.19, P3.02 | Edge guess plus optional exact location; city and below free with limited fields, above names only | Q-S20, CP3, CP4 |
| Zero-spend snowball costs | P0.06 | Founder time as the real budget; managed Postgres at S1 | Q-S5 |
| Scale plan | P1.03 | Country column from day one; one managed Postgres until a measured limit | Q-S6 |
| Cluster pilot success test | Gate 1 | Verify 200 firms; 5 pay or 5 foreign buyers enquire in 6 to 8 weeks | Q-S7 |
| Topic lists | section 16 | Later; monetised by sponsorship, affiliate and ads | Q-S4 |
| Reuse plan and counsel view on GPL or AGPL code | P0.08 | Never copy GPL or AGPL code; run such tools as separate services only | Q-S10 |
| Prototype scope | resolved | Production code authorised by the founder's request of 2026-10-05 ("Than code the software for it"); this plan is the build plan | Q-S11 |
| Rewards for volunteers | P2.23 | Levels, certificates, visible credit, access credit | Q-R5 |
| Which revenue streams switch on first | P3 and P5 | Order: paid sample and subscriptions, badges and company pages, enquiry relay, paid rank, outreach last | Q-R4 |
| Share of messaging revenue to contributors | P4 billing | Lower than list sales; must be set before paid outreach billing | F7 |
| Payment provider and payout method | P3.09, P5.04 | Manual first; a local licensed gateway; foreign route after bake-off | F12 |
| First 2 to 3 categories and first city | pilot | As above | R.13 |
| Languages at launch | P2.14 | English and Urdu | N3 |
| Personal lists, ratings, ads in version 1 | section 16 | Later | I, J8, H |

### 21.2 Added by this plan (new questions; defaults assumed)

| ID | Question | Needed by | Assumed default |
|---|---|---|---|
| Q-T1 | Language addresses: Urdu under `/ur/` with hreflang, or one address with a language cookie | P2.01 | `/ur/` prefix, English unprefixed |
| Q-T2 | Free quotas in numbers (rows, names per day, pages per address) | P3.03 | 5 rows first; 100 names per account per day; 40 per anonymous address; alarm at 500 pages per address per day; calibrated in the pilot |
| Q-T3 | Index threshold N for list pages and what makes an entry "rich" | P2.15 | N = 10 verified entries; entry indexable when verified at surveyor or owner level with at least hours or services and a certificate or identifier |
| Q-T4 | Validity days per check level | P1.12 | 365, 365, 180 |
| Q-T5 | Retention schedule | P3.14 | Messages and delivery events 12 months; logs 90 days; audit log kept |
| Q-T6 | Job queue product | P0.07 | Procrastinate; fallback Celery |
| Q-T7 | Password hasher and MFA package licences | P3.06 | Argon2id; `django-otp`; licences checked before adoption |
| Q-T8 | Sponsored slot count and placement price unit | P5.01 | Two slots per list; fixed monthly price |
| Q-T9 | Payout minimum and cap months after which lowest rate applies | P5.05 | Minimum set by the payout rail; cap 36 months |
| Q-T10 | Whether first-page rows number is 5 (design) while the first build showed more | P2.04 | 5 then "Show n more" (design system) |
| Q-T11 | Whether Python 3.12 or 3.13 is the production runtime | P0.06 | 3.12 |

---

## 22. Requirement traceability matrix

Every requirement, decision and open question in `docs/REQUIREMENTS.md`, with the plan section and work packages that deliver it. "Defer" means a schema reservation or a later module (section 16), not forgotten.

### 22.1 A to D (vision, users, lists, data intake)

| ID | Requirement (short) | Where in the plan |
|---|---|---|
| A1 | Anyone creates a list and sells at own price | §5.2, §9.5; P1.10, P3.09; conflict with P12 open: platform prices (E2) |
| A2 | Platform takes a share; contributors earn the rest | §12.2; P3.11, P3.12 |
| A3 | Open-source website | R37; P0.10 |
| A4 | One page per list | §8.2, §8.3.2; P2.01, P2.04 |
| A5 | Scale to very large number of list pages | §4.4, §8.6 (publish only worthy pages); P1.05, P2.15 |
| A6 | Platform runs marketplace; people build and sell | §3 overall; §14 |
| A7 | Example list types in scope | §5.2 seeds; P1.10 |
| B1 | Roles admin, creator, subscriber | §11.2 |
| B2 | Roles admin, moderator, user | §11.2 (union) |
| B3 | List maker and populator | §11.2, §14; P2.21 |
| B4 | Businesses add themselves and claim | §6.5; P1.13, P2.09 |
| B5 | Buyer types | §9.5, §11.2 |
| B6 | Email and password | §11.1; P3.06 |
| B7 | Google and Facebook login | §16; P6.02 |
| B8 | MFA | §11.1; P3.08 (staff), P6.02 (all) |
| B9 | Profile customisation | §16 defer |
| C1 | Bottom-up merge (superseded) | superseded by C10 |
| C2 | Hierarchy works for topics too | §16 topic lists; `concept` kinds |
| C3 | Drill down and zoom out | §8.3.1, §8.3.2 breadcrumbs; P2.03 |
| C4 | Categories and subcategories | §5.2, §4.2.3 |
| C5 | Lists have different fields | §5.3; P1.09 |
| C6 | Entries carry contact, location, description (superseded) | C17 |
| C7 | Entry in several parent lists | `entry_concept` secondary concepts; §4.2.4; answers "yes" by design (assumption, owner to confirm) |
| C8 | Merge performed by platform | §4.4 roll-ups; §6.7 |
| C9 | `parent_list_id` hierarchy (superseded) | C10 |
| C10 | Global top-down place hierarchy | §5.1; P1.06 |
| C11 | Creating a list type opens it everywhere | §5.2; P1.10 |
| C12 | List is a category at a place; roll-ups | §4.4, §3.1; P1.05 |
| C13 | Contributors add entries and areas | §5.1; P1.08 |
| C14 | Seed place tree from open data | §5.1; P1.06 |
| C15 | Shared multilingual taxonomy with synonyms | §4.2.3, §5.2; P1.07 |
| C16 | Thin lists not indexed; invite first contributor | R23, §8.3.2 empty state; P2.15 |
| C17 | Entry fields: name, address, owner, phone, WhatsApp, social, rankings, size, goods, services | §4.2.4; P1.03 |
| C18 | Owner and personal phone are personal data | R18, §6.8; P2.11 |
| C19 | Rankings by reviewers need rules | §16 reviews |
| C20 | Segment ownership | §6.6; P2.10 |
| C21 | Equipment and priced services | `entry_equipment`, `entry_service`; R20 |
| C22 | Skill-based lists of individuals | §6.8, R18; P2.11 |
| C23 | Mobile repair, Quran tutors | §5.2 seeds; R19 |
| C24 | Record every decision | R38; P0.10 |
| C25 | Natural scale per list type | `concept.natural_scale`; §5.2 |
| C26 | Entry template per list type | §5.3; P1.09 |
| C27 | Lists not about places (apps, websites) | §16 topic lists |
| C28 | Launch globally with no spending | §18.6 zero-spend path |
| C29 | Text and numbers only | R01 |
| C30 | Pakistani cluster and tourism lists | §5.2 seeds; pilot |
| C31 | Catalogue of list types from 53 platforms | §5.2 (held until Q-S8) |
| C32 | List and entry components, social buttons, campaigns | §8, §14.2; P2.24 |
| C33 | Components finalised | §4.2.4, `docs/LIST_AND_ENTRY_COMPONENTS.md`; Q-S12 |
| C34 | Few templates; change once | §8.1; R25 |
| C35 | Paid companies get a full page | §8.3.3; P2.07, P3.05 |
| C36 | Modern, dynamic, moving page | §8.4; P2.02, P2.05 |
| C37 | The name | §21.1 Q-S19; P0.06 |
| C38 | World to list navigation | §8.2, §8.3.1; P2.01, P2.03 |
| C39 | Automatic location | §10.2; P2.19 |
| D1 | People who hold lists paste them | §7.2; P1.16 |
| D2 | Bulk import with column mapping | §7.2; P1.16 |
| D3 | Duplicate detection on import | §7.4; P1.18 |
| D4 | Validation of list data | §7.2 normaliser; §5.3 validators |
| D5 | Imported entries earn nothing until verified | R09 |
| D6 | First adder gets credit | `credit_event`, §6.7 |
| D7 | Businesses claim their entry | §6.5 |
| D8 | Self-listed entries earn no payout | R09 |
| D9 | Entries record source, contributor, verification, last-verified | `entry_value_meta`, `credit_event` |
| D10 | Community quality checks | later: stewards, §6.6 |
| D11 | Contributors declare right to share; takedown | §7.2, §15; P1.16, P3.14 |
| D12 | No copying from sources forbidding it | R22 |
| D13 | Report-an-error flow | §8.3.4; P2.09, P2.25 |
| D14 | AI agents draft lists | §7.6; T1.01 to T1.03 |
| D15 | Agent source list; red sources out | §7.1; R22 |
| D16 | Open baseline data licensed in | §7.1, §2.2; P1.19 |
| D17 | Every record stores source, licence, date, robots, consent | R21; `source`, `entry_value_meta` |
| D18 | Draft-first collection | §6.1; P1.11 |
| D19 | Verification levels | §6.3, §6.4; P1.12 |
| D20 | Design notes for levels | §6.4 guards |
| D21 | Service providers from established sources first | §7.1; gate 0; P1.19 |

### 22.2 E to H (products, money, outreach, advertising)

| ID | Requirement (short) | Where |
|---|---|---|
| E1 | Creators set price | §9.5, conflict P12; default platform prices |
| E2 | Platform sets price of merged lists | §9.2 (priced by scope), §9.5 |
| E3 | First few listings free to signed-up viewers | §9.1, §9.3 |
| E4 | Free public preview of each page | §8.3.2, R05; P2.04 |
| E5 | Buyers receive data (superseded) | E13 |
| E6 | View-only time-limited access, renewals | §9.5, §12.4; P3.04 |
| E7 | Subscriptions by scope | §9.5; P3.04, P5.03 |
| E8 | Platform-wide subscription | §16 defer |
| E9 | Pay-per-view | §9.5 (list purchase) |
| E10 | Exports rate-limited and watermarked | R13; P5.02, P3.03 canaries |
| E11 | API access | §16 defer; R31 |
| E12 | Pricing ladder | §9.1, §9.5 |
| E13 | No download except about USD 1,000; outreach default | R13, R02; P5.02, §13 |
| E14 | First entries plus statistics of whole list | §8.3.2 hero; §4.4; P2.04 |
| E15 | Businesses pay to rank | §9.4; R14; P5.01 |
| E16 | Government and institutions buy | R30; P5.02 |
| E17 | Cheaper, more targeted than Google and Meta | §13.3; P4.05 |
| E18 | Research how platforms earn | done in `reports/`; informs §9.5 |
| F1 | Contributors share funds from sold lists | §12.2 |
| F2 | 50, 40, 30 step-down | `rate_phase`; P3.11 |
| F3 | Rate locked per entry | R11 |
| F4 | What triggers each step | §21.1; assumed date phases |
| F5 | Equal share per verified entry | §12.2 |
| F6 | Ad revenue sharing | §21.1 Q-R3 |
| F7 | Messaging share lower than list sales | §12.2; P4 billing |
| F8 | Subscription allocation by scope plus freshness | §12.2; P5.03 |
| F9 | Payout held for refund window | §12.2; P3.12 |
| F10 | Admin configures percentages; payout reports | `rate_phase`, §15.1; P3.11, P5.05 |
| F11 | Payout ledger, one line per person per sale | §12.1; P3.10 |
| F12 | Payment gateway and payout method | §12.4, §12.5; P3.09, P5.04, P5.05 |
| F13 | Multi-currency, VAT/GST | §12.4; P5.06 |
| F14 | Seller identity checks for payouts | §12.5; P5.05 |
| G1 | Platform sends suppliers' messages; contacts hidden | §13; R02 |
| G2 | Email outreach tools (resolved by E13) | §13 |
| G3 | Buyer chooses channel | §13.2; P4.01 |
| G4 | Shops opt in; caps; opt-out | §13.2; P4.02, P4.03 |
| G5 | Supplier verification and message review | §13.2; P4.03 |
| G6 | Delivery, read, reply, order tracking | §13.2; P4.04 |
| G7 | Anti-spam compliance | §13.2; counsel gate |
| G8 | Notifications including expiry reminders | event jobs (Appendix F); P3.04 |
| H1 | Ads on list pages | §9.4; P5.01 |
| H2 | Share of ad revenue to creators | §21.1 Q-R3 |
| H3 | Featured placement (superseded by E15) | E15 |
| H4 | Affiliate links | §16 defer |

### 22.3 I to O (personal lists, search, dashboards, admin, security, platform, operations)

| ID | Requirement (short) | Where |
|---|---|---|
| I1 to I8 | Personal lists, private by default, sharing, templates, no recommendation without consent | §16 personal lists; R33; schema namespace reserved |
| J1 | Search with filters | §10.1; P2.08, P2.18 |
| J2 | Full-text search and autocomplete | §10.1; P2.08 |
| J3 | Recommendation engine | §16 defer (first build's TF-IDF endpoint removed, threat 12) |
| J4 | SEO-friendly URLs mirroring hierarchy | §8.2; P2.01 |
| J5 | Thin pages not indexed | R23; P2.15 |
| J6 | Product-level local search | §16 defer |
| J7 | Favorites | §16 defer; "Save" action in §8.3.3 |
| J8 | Ratings and reviews | §16 reviews (hidden until rules) |
| K1 | Creator dashboard | §14.2; P2.21 |
| K2 | Buyer dashboard | §11.2, Appendix B; P3.04 |
| K3 | List performance analytics | §18.3, Appendix G; P3.20 |
| K4 | Activity logs for collaborative edits | `change_log` now; UI later |
| K5 | Gamification | §14.2 levels (limited); rest later |
| K6 | Business view for suppliers | §16 defer |
| L1 | Review reported lists and entries | §15.1; P2.25 |
| L2 | Ban or suspend accounts; manage roles | §15.1; P3.07 |
| L3 | Analytics: API usage, active users, traffic | §18.3; P3.20 |
| L4 | Audit log | §15.4; P1.01, P3.15 |
| L5 | Dispute handling and refunds | §12.4, §15.1; P3.09 |
| M1 | Passwords hashed; token auth | §11.1 (sessions, no bearer tokens needed) |
| M2 | Encryption in transit and at rest | §17.2 |
| M3 | Role-based access control | §11.2; P3.07 |
| M4 | Anti-scraping, CAPTCHA | §9.3 (CAPTCHA only if abuse appears) |
| M5 | GDPR and CCPA | §17.3; P3.14 |
| M6 | WCAG 2.1 accessibility | §8.7; P2.17 |
| M7 | Rate limiting | §17.2; P3.03, P3.17 |
| M8 | Secrets only in environment | R34 |
| M9 | Credentials already exposed: rotate | P0.01 |
| M10 | Local law for Pakistan and other launch countries | §18.7; counsel gate |
| N1 | Python backend with PostgreSQL | §2.1 |
| N2 | React SPA (conflict; server-rendered chosen) | §2.1, §8 |
| N3 | Multilingual, real-time language switching | §8.5; P2.14 |
| N4 | Offline and service worker | §16 defer |
| N5 | Kubernetes, Prometheus, Terraform | §3.6 deferred |
| N6 | Redis, Celery, replication, CDN, autoscale | §3.5 stages; P6.03 |
| N7 | Distributed storage for media | §16 (no media) |
| N8 | DB optimised for hierarchical data | `place.path`; §4.2.2 |
| N9 | CI/CD through GitHub Actions | §20.3, P0.04 |
| N10 | Daily database backups | §18.4; P3.21 |
| N11 | Local dev with Docker Compose | §18.1; P0.03 |
| N12 | Real-time analytics | §16 defer |
| O1 to O8 | Current deployment facts | §3.5 (new host from repository, static IP, DNS, HTTPS); P0.06 |

### 22.4 V, P, CP, S and the question lists

| ID | Where |
|---|---|
| V1 demand intelligence | §16 commerce stage 2; aggregate events and rollups |
| V2 product requests | §16 commerce stage 2 |
| V3 product testing | §16 commerce stage 2 |
| V4 direct sell offers | §13 outreach is step 1; §16 stage 3 |
| V5 direct shipping | §16 stage 3, partners |
| V6 targeted audience | §13; E17 test P4.05 |
| V7 shop-side controls (topics, channels, frequency) | §13.2 opt-in settings; P4.02 |
| V8 verified factory and shop accounts | §13.2 supplier verification; P4.03 |
| P1, P2 (resolved) | R02, R13, §13 |
| P3 role names | §11.2 |
| P4 SPA versus server-rendered | §2.1 |
| P5 anti-scraping versus indexable | §9.3 (same content to bots) |
| P6 billion pages versus thin-page penalty | §8.6, §4.4 |
| P7 heavy infrastructure | §3.5 |
| P8 outreach riskiest, now main product | §13.3 gate |
| P9 paid rank versus contributor pay | §12.2 default |
| P10 government as buyer | R30 |
| P11 global versus one trade | R24; country switches |
| P12 top-down lists versus creators price lists | §21.1 default platform prices |
| P13 paid ranking level | §9.4; city first |
| P14 draft-first versus unverified at scale | §6.1, §6.2 |
| P15 free segments versus paid roll-ups | §9.2, §9.3 |
| P16 no cash versus verifier capacity | §14.1; pilot measurement |
| P17 charging versus free removal | R17, R39 |
| CP1 paid only when list sells | R10; §12 |
| CP2 businesses pay to be on list | §9.4; hidden versus lower open |
| CP3 access by level | §9.2 |
| CP4 names only in free preview | R04; §9.2 |
| CP5 free users see ads | R16 |
| CP6 governments buy | R30 |
| CP7 revenue streams | §9.5 |
| CP8 two tests | R40 |
| CP9 non-cash rewards | §14.2; P2.23 |
| S1 refine before coding | resolved by the founder's instruction; this plan |
| S2 top to bottom coding order | §19: P1 place tree and taxonomy first, then lists and entries |
| S3 all countries in structure; lighter-rule countries first | R24; §18.7 |
| S4 high-end product over time | §6, §7.7 (accuracy and compliance records) |
| S5 which lists pay | `reports/Which lists pay.md`; seeds §5.2 |
| Q-N1 to Q-N6 | §21.1 |
| Q-O1 to Q-O5 | §21.1; Q-O2 §5.1; Q-O3 §5.2; Q-O4 §9.4; Q-O5 §18.7 |
| Q-P1 to Q-P7 | §21.1 |
| Q-R1 to Q-R5 | §21.1 |
| Q-S1 to Q-S20 | §21.1 |

---

## 23. Risks and how the plan answers them

Top risks from `reports/Project analysis.md` B11 with the plan's answer (L likelihood and I impact, 1 to 5).

| Risk | L×I | Plan answer | Early warning built into the plan |
|---|---|---|---|
| R01 Nobody pays; build wasted | 20 | Phase gates; pilot slice first; sample sold before P3 spending; manual payments first | No paying buyer 8 weeks into the pilot |
| R02 Thin pages not indexed | 16 | R23 threshold; throttle; indexing watch | Under 20% indexed at day 90 |
| R05 Volunteers do not complete verification | 16 | Task engine measures completion; non-cash rewards; owner claims; fee switch | Under 30% of assigned checks done in 2 weeks |
| R06 Exposed secrets still live | 16 | P0.01 first; push protection | Logins from unknown addresses |
| R07 Cross-script duplicates | 16 | §7.3, §7.4; credit events; merge map | Reviewers reject over 10% of auto-merges |
| R09 Scrapers rebuild paid lists | 16 | §9.3 controls; canaries | One address over 500 pages a day |
| R14 Scope creep | 16 | Phase gates; deferred list §3.6; section 19.15 | Work started with no exit criterion met |
| R03 Outreach law and bans | 15 | §13.2; per-country switch; counsel gate | Opt-out over 2%; delivery failure over 10% |
| R21 Data decay | 15 | Expiry on every check; re-check scheduler | Expired chips over 25% |
| R04 AI drafts inaccurate | 12 | R35; audit samples; draft-only | Audit accuracy under 90% |
| R13 Key-person and AI-code debt | 12 | Two reviewers on sensitive code; rule tests; decision log | One reviewer on sensitive merges |
| R15 No payment route from Pakistan | 12 | Manual first; local gateways; bake-off | No provider onboarded by week 8 |
| R17 Urdu search poor | 12 | Folding, alias table, 200-query set | Zero-result rate over 15% |
| R20 Fake or colluding verifiers | 12 | Separation of duties; canaries; audits | Verifier accuracy under 80% |
| R22 AI summaries cut traffic | 12 | Statistics and dates on pages; owner claims | Impressions flat as pages grow |
| R08 Ledger error | 10 | Property tests; two-person approval; reconciliation | Any reconciliation difference |
| R10 Personal-data breach | 10 | Encryption; separate store; runbook | Unusual exports |
| R24 Backups not restorable | 10 | Quarterly timed drill | Drill skipped |
| R11 AI spend overruns | 9 | Caps, kill switch, alerts | 80% of cap before month end |
| R12 Prompt injection | 9 | No credentials; staging only; injection tests | Unexpected fields in agent output |
| R18 Postgres hot spots at 10 million | 9 | Roll-ups; scoped search; engine when measured | Search p95 over 500 ms |
| R26 Registers' terms forbid bulk use | 9 | Written terms per body; start with facility and school registers | A refusal or letter |

Additional plan risks: the first build's per-viewer rendering blocks shared caching (fixed by P2.05); effort above the analysis' estimate (section 19.2 explains and offers a smaller slice); decisions still open (section 21 defaults); reliance on third-party price and rate figures that are unverified at source (marked [S] and [U]).

---

## 24. Current code: keep, replace, add

State at the time of writing: `backend/` holds Django 5.2 with one app `lists`, 17 passing tests, SQLite by default, 14 models, nine views, templates and CSS from the prototype, a demo seed, and CI on Python 3.11 to 3.13 (without Postgres).

| Item | Verdict | Action |
|---|---|---|
| `config/settings.py` secure-by-default pattern (refuses to start without a secret, cookie and header settings, WhiteNoise) | Keep and extend | Split into dev, staging and prod; add CSP, Postgres, queue, Argon2id |
| `lists/static/lists/app.css` (prototype tokens) | Keep | Becomes the design-token source; add logical-property lint |
| `lists/templates/lists/*` | Rework | Split into shared includes; shell versus fragments (P2.02, P2.05) |
| `lists/share.py` | Keep the idea | Becomes the registry (Appendix C); add `hide` rule per entry |
| `lists/visibility.py` | Replace | Becomes `access.policy` registry (P3.01); current per-viewer HTML is not cacheable |
| `lists/middleware.py` | Rework | Location becomes a fragment, preferences stay; add quota and template-version middleware |
| `lists/models.py` | Replace | Place, ListType, Entry, Check, Contact etc. are flat; replace with section 4 tables in modules; keep concepts |
| Views and URL scheme `/p/…/l/…` | Replace | Section 8.2 scheme with redirects (P2.01) |
| `lists/strings.py` | Replace | gettext `.po` files (P2.14) |
| `Contribution`, `Sale`, `LedgerLine` | Replace | Mutable and per-entry; replace with the append-only ledger (P3.10 to P3.12) |
| Enquiry and Report models | Rework | Relay with opt-in and thread (P3.13); moderation queues (P2.25) |
| `seed_demo` | Keep and extend | Human-readable dataset; add Urdu names, more list types, claimed and company entries |
| Tests (17) | Keep as seeds of rule tests | Move to Postgres; add rule tests (20.2) |
| `scripts/build_master_document.py`, `docs/MASTER_DOCUMENT.md` | Keep | Regenerate after each phase |
| `prototype/` | Keep | Remains the visual specification; update when design changes |
| Root files `Data Schema`, `Deployment Script`; `docs/DEPLOYMENT.md` | Delete or rewrite | P0.02, P0.06 |
| CI workflow | Rework | Postgres service, blocking lint, scans, coverage, page-weight gate (P0.04, P0.05) |

Migration note: there is no production data, so the replacement is a fresh start with the demo seed re-created from the new model; no data migration is needed. From the first deployed release on, migrations are forward-only.

---

# Appendices

## Appendix A. URL map

Access: **P** public, **S** signed in, **R** role needed, **F** fragment (private, `noindex`, `no-store`). All paths exist with an `/ur/` mirror for page routes. Trailing slash canonical.

| Path | Method | Access | Purpose | Cache |
|---|---|---|---|---|
| `/` | GET | P | World page | Shared |
| `/{country}/…/` | GET | P | Place page at any level | Shared |
| `/{place path}/{list-type}/` | GET | P | List page | Shared |
| `/e/{uid}/{slug}/` | GET | P | Entry page (basic or company) | Shared |
| `/search/` | GET | P | Search results (`noindex`) | Short |
| `/add/` | GET, POST | S | Add an entry (draft) | No |
| `/add/area/` | GET, POST | S | Propose an area | No |
| `/claim/{uid}/` | GET, POST | S | Claim a business (OTP) | No |
| `/wrong/{uid}/` | GET, POST | P | Something wrong: report, correct, remove my data | No |
| `/message/{uid}/` | GET, POST | S | Message a business | No |
| `/enquiry/` | GET, POST | R subscriber | Enquiry to many | No |
| `/about/`, `/terms/`, `/privacy/`, `/plans/`, `/sources/`, `/how-checks-work/`, `/contributors/rules/` | GET | P | Static pages | Shared |
| `/account/signup/`, `/login/`, `/logout/`, `/password/…`, `/delete/` | GET, POST | P or S | Accounts | No |
| `/account/` | GET | S | Dashboard (contributor, owner, buyer by role) | No |
| `/account/owner/{uid}/` | GET, POST | R owner | Edit claimed entry, company page content, opt-ins | No |
| `/account/tasks/` | GET, POST | R surveyor, steward | Task queue | No |
| `/account/subscription/` | GET, POST | S | Subscription and orders | No |
| `/staff/…` | GET, POST | R staff + MFA | Queues, registries, switches, payouts | No |
| `/admin/` | GET, POST | R admin + MFA | Django admin | No |
| `/_f/near-you/` | GET | F | Near-you strip | Private |
| `/_f/panel/{uid}/` | GET | F | Subscriber detail panel for an entry | Private |
| `/_f/rows/…` | GET | F | More rows within quota | Private |
| `/_f/ad/{slot}/` | GET | F | Ad slot (free viewers) | Private |
| `/_f/quota/` | GET | F | Quota notice | Private |
| `/prefs/` | POST | P | Language, theme, view, place choice | No |
| `/webhooks/payments/{provider}/` | POST | signed | Payment webhooks | No |
| `/webhooks/messaging/{provider}/` | POST | signed | Delivery callbacks and replies | No |
| `/optout/{token}/` | GET, POST | P | One-tap opt-out | No |
| `/sitemap.xml`, `/sitemaps/{country}-{n}.xml`, `/robots.txt` | GET | P | Search engines | Shared |
| `/healthz` | GET | P | Health check (no data) | No |

Not present by decision: any public data API (R31), any user export or download (R13), any image or file upload route (R01).

## Appendix B. Templates and fragments

| Template | Inputs | States it must render | Notes |
|---|---|---|---|
| `base` | language, direction, theme, version | all | Header with search, language and theme; skip link; footer |
| `place` | place, children with counts, list types with counts | empty, children only, entries | Widen steps on world and country |
| `list` | place, list type, rows, trust split, filters | empty, one result, many, over-quota, names-only, sponsored | Section 8.3.2 order |
| `entry` | entry, viewer plan, checks, add-on block | closed, moved, individual, child-facing, health, company, long names | Subscriber details as a fragment |
| `search` | query, scope, groups | zero results | `noindex` |
| `topic_list` (later) | topic node, items | empty | |
| `static` | page key | | |
| `form` | form key, fields | errors, success | One template, form registry |
| `message_form` | entry or scope | blocked content, sent | |
| `dashboard_*` | role data | empty | Contributor, owner, buyer, moderator, admin |
| Includes | header, footer, breadcrumb, check_label, check_key, share_bar, action_row, filter_bar, result_row, result_card, key_facts, subscriber_panel, notice, sponsored_slot, ad_slot, trust_hero, area_chips, view_toggle, records, something_wrong, empty_state, quota_notice, near_you | | One file each |
| Fragments | near_you, subscriber_panel, more_rows, ad_slot, quota_notice | | Under `/_f/` |

## Appendix C. Registry seeds

### C.1 Share channels (one row each; template reads this list)

| id | label | group | kind | link format | Hidden for |
|---|---|---|---|---|---|
| native | Share | main | native Share API button | n/a | named individuals without consent, child-facing, `do_not_share` |
| whatsapp | WhatsApp | main | link | `https://wa.me/?text={title}. {line} {url}` | same |
| copy | Copy link | main | copy | clean address, no tracking tags | none |
| facebook | Facebook | more | link | sharer URL | same |
| email | Email | more | mailto | subject and body | same |
| linkedin | LinkedIn | more | link | share-offsite URL | same |
| x | X | more | link | intent URL | same |
| later | Telegram, SMS, QR, embed | | | | |

Tracking tags on shared links: `utm_source={channel}`, `utm_medium=share`, `utm_campaign=list_share` or `entry_share`, `ref={contributor code}`. No third-party scripts, plain links.

### C.2 Social platforms (entry form and page read this)

Businesses: facebook, instagram, linkedin, x, youtube, tiktok, telegram, snapchat, pinterest, threads, whatsapp_channel, wechat, weibo, douyin, xiaohongshu, line, kakaotalk, vk, other. Professionals (people entries): github, kaggle, orcid, behance, dribbble, google_scholar. WhatsApp number is a contact, not a social page. Outbound links carry `rel="nofollow noopener noreferrer"`.

### C.3 Check labels

| key | English | Plain explanation (draft; native Urdu review pending) | Shape | Counts for payout |
|---|---|---|---|---|
| surveyor | Surveyor-verified | An independent AllLists surveyor checked this by call or visit. | Solid thick outline | Yes |
| owner | Owner-verified | The owner or manager of the business confirmed this. | Solid outline | Yes |
| ai | AI-checked | A computer program compared this with other sources. A person has not checked it. | Dashed outline | No |
| none | Not verified yet | Nobody has checked this yet. | Dotted outline | No |

Rule for expired checks: when every check on a published entry expires, it stays published for a grace period (default 90 days, queued for re-check) with the past checks shown dated and expired and the label "Not verified yet"; after the grace period it returns to draft (R08). Each check shows "Checked {date} · {age}".

### C.4 Plans and visibility (the table `policy.visible()` reads)

| Field key | Free in own place | Free wider than own place | Subscriber | Notes |
|---|---|---|---|---|
| name, name_variants | P | P | P | |
| entity_type, primary_category | P | P | P | |
| area (place name) | P | P | P | |
| specialities | first 3 | none | all | |
| check labels with date | P | P | P | |
| status | P | P | P | |
| hours, languages, year_established, business type, OEM flag, how checked | P (entry page) | none | P | |
| address | area only | none | full street | Individuals: area only for everyone |
| location | area precision | none | exact pin | |
| website, social links | locked | none | P | Q-S13 |
| size, markets, minimum order | locked | none | P | |
| services and prices with dates, products | names only | none | full | Health prices off by default |
| certificates | list of names | none | details with register links | |
| company-provided sections | P (public, labelled) | none | P | Company page |
| enquiry button | one message to one business | none | to many | |
| contacts, owner name of individual | never | never | never | R02 |
| ads | shown | shown | none | R16 |
| statistics | count, last checked, split by type | count only | adds "with checkable certificate", "verified 12 months" | |

### C.5 Listing plans

| Plan | Price | Switches on |
|---|---|---|
| basic | free | Basic entry page, claim funnel, checks, one-line prompt to add a company page |
| company | paid per period (price tested in the pilot) | About, products and services with specifications, certificates listed, capacity, terms, questions; "Company page" tag on rows; not for individuals or child-facing services |

### C.6 Feature flags (initial)

`company_pages`, `placements`, `ads`, `outreach`, `enquiry_relay`, `reviews` (off), `personal_lists` (off), `topic_lists` (off), `child_services` (off), `named_individuals` (off), `health_prices` (off), `urdu_pages`, `template_canary` (small rollout of a new template version).

### C.7 Country switches (initial)

| Country | Browsing | Indexing | Selling | Outreach | Ads | Individuals | Health prices | Child services |
|---|---|---|---|---|---|---|---|---|
| Pakistan | on | on after the pilot pages pass quality | on at P3 | off until counsel | off | off | off | off |
| All other countries | on | off | off | off | off | off | off | off |

### C.8 Add-on example: manufacturers and exporters (the pilot template)

| Key | Type | Show | Filter | Required to publish |
|---|---|---|---|---|
| business_type (manufacturer, trader, wholesaler, exporter) | enum | P | yes | yes |
| product_categories with hs_code | concept list | P names, L codes | yes | yes |
| tax_ids (NTN, SECP) with per-ID verified flag | identifier list | P number, register link | no | no |
| registered_address, factory_address | address | L | no | no |
| year_established, years_exporting | number | P | no | no |
| export_markets | place list | L | yes | no |
| certifications (ISO 13485, CE, FDA) with body, id, expiry | identifier list | names P, details L | yes (has checkable certificate) | no |
| verification_tier (none, documents, on-site, third-party) | enum | P | yes | derived |
| capacity_band, workforce_band | enum | L | no | no |
| oem | bool | P | yes | no |
| moq | text | L | no | no |

## Appendix D. Permission matrix

✓ allowed, o own items only, q through a review queue, – not allowed. MFA required for Mod, Fin, Adm and Surveyor lead.

| Capability | Visitor | User | Subscriber | Contributor | Surveyor | Steward | Owner | Mod | Fin | Adm |
|---|---|---|---|---|---|---|---|---|---|---|
| Browse free views | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Subscriber fields and enquiry to many | – | – | ✓ | – | – | – | – | ✓ | – | ✓ |
| Report, suggest edit, remove my data | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Add entry (draft) | – | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓ | – | ✓ |
| Propose area or list type | – | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓ | – | ✓ |
| Import list with declared rights | – | – | – | ✓ | – | ✓ | – | ✓ | – | ✓ |
| Verification tasks | – | – | – | – | ✓ (not own adds) | q | – | ✓ | – | ✓ |
| Edit entries in a segment | – | – | – | – | – | q | – | ✓ | – | ✓ |
| Claim and edit own business | – | ✓ claim | – | – | – | – | o | ✓ | – | ✓ |
| Company page content | – | – | – | – | – | – | o (paid) | q | – | ✓ |
| Approve claims, reports, area proposals, dedupe | – | – | – | – | – | – | – | ✓ | – | ✓ |
| Takedown and erasure | – | – | – | – | – | – | – | ✓ | – | ✓ |
| Edit registries, switches, flags | – | – | – | – | – | – | – | – | – | ✓ |
| Manage rate phases | – | – | – | – | – | – | – | – | ✓ (two-person) | ✓ |
| Create payout batch | – | – | – | – | – | – | – | – | ✓ | – |
| Approve payout batch | – | – | – | – | – | – | – | – | ✓ (not creator) | – |
| Record manual payment | – | – | – | – | – | – | – | – | ✓ | ✓ |
| View audit log | – | – | – | – | – | – | – | ✓ own area | ✓ money | ✓ |
| Manage users and roles | – | – | – | – | – | – | – | – | – | ✓ |
| Run extract (download) | – | – | – | – | – | – | – | – | – | ✓ with Fin approval |

## Appendix E. Settings and environment variables

| Name | Purpose | Default | Notes |
|---|---|---|---|
| `DJANGO_SECRET_KEY` | Signing | none (refuses to start) | Rotated; never in the repository |
| `DJANGO_DEBUG` | Debug | off | `1` only locally |
| `DJANGO_ALLOWED_HOSTS` | Hosts | localhost list | |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | CSRF origins | empty | |
| `DJANGO_HSTS_SECONDS` | HSTS | 0 | Raise after stable HTTPS |
| `DJANGO_INSECURE_COOKIES` | Allow non-secure cookies | off | Local only |
| `ALLLISTS_DEMO` | Show the plan preview switch | off outside debug | Never on in production |
| `POSTGRES_DB`, `_USER`, `_PASSWORD`, `_HOST`, `_PORT` | Database | SQLite for local demo only | TLS required in production |
| `FIELD_ENCRYPTION_KEYS` | Versioned keys for encrypted columns | none | Key ids stored with ciphertext |
| `CONTACT_HASH_PEPPER` | Keyed hash for contact lookup and suppression | none | |
| `IP_HASH_SALT` | Rotating salt for quota keys | none | Rotated daily |
| `SENTRY_DSN` | Error tracking | empty | |
| `PAYMENT_<PROVIDER>_KEY`, `_WEBHOOK_SECRET` | Payment adapters | empty | |
| `MESSAGING_<PROVIDER>_KEY`, `_WEBHOOK_SECRET` | Messaging adapters | empty | |
| `AI_PROVIDER_KEY`, `AI_DAILY_CAP_MINOR`, `AI_MONTHLY_CAP_MINOR`, `AI_KILL_SWITCH` | Agent track | empty, caps required to start | |
| `EMAIL_*` | Transactional email | console in dev | |
| `CDN_PURGE_TOKEN` | Cache purge | empty | |
| `BACKUP_*` | Backup target and keys | empty | |
| Settings constants | `TEMPLATE_VERSION`, `FREE_INITIAL_ROWS` (5), `FREE_PREVIEW_NAMES`, `FREE_MAX_SPECIALITIES` (3), `INDEX_THRESHOLD` (10), `PUBLISH_CAP_PER_WEEK`, `CAP_MONTHS` (36), `REFUND_HOLD_DAYS` (14), `GRACE_DAYS` (90), `STEWARD_INACTIVITY_DAYS` (90) | | Read from DB where an admin changes them |
| Retired | `ALLLISTS_PHASE` | | Replaced by the `rate_phase` table |

## Appendix F. Background jobs

| Job | Schedule | Purpose |
|---|---|---|
| rollup_refresh | every 5 minutes | Incremental `rollup_cell` updates |
| rollup_recount | nightly | Exact recount and drift report |
| expiry_sweeper | hourly | Drop expired checks; start grace periods |
| recheck_scheduler | daily | Queue re-check tasks by age and risk |
| steward_inactivity | daily | Expire stewardship grants |
| audit_chain_verify | nightly | Re-verify the audit hash chain |
| sitemap_build | daily | Sharded sitemaps from indexable pages |
| indexing_watch | weekly | Submitted versus indexed |
| link_checker | weekly | Website and social link liveness (SSRF-safe) |
| quota_cleanup | daily | Drop old counters |
| import_runner, dedupe_runner | on demand | Batch imports and candidate scoring |
| agent_jobs | on demand within caps | Draft and second-check jobs |
| ai_spend_monitor | hourly | Cap and alert checks |
| canary_seeder | on demand | Plant and monitor canaries |
| outreach_sender | continuous | Queue to provider, caps and quiet hours |
| callback_processor | continuous | Delivery events, replies, opt-outs |
| subscription_reminders | daily | Expiry reminders |
| allocation_runner | per sale | Contributor allocations |
| hold_release | daily | Release holding after the refund hold |
| payout_batch_builder | per cycle | Prepare batch for approval |
| reconciliation | daily and monthly | Ledger versus provider reports |
| backup_dump, wal_archive | nightly, continuous | Backups |
| restore_drill_reminder | quarterly | Alert if no drill logged |
| data_quality_metrics | daily | Accuracy, freshness, coverage, duplicate rate |
| retention_purge | weekly | Remove data past retention |
| erasure_executor | on demand | Tombstone and suppress |

## Appendix G. Events and metrics

Server-side, privacy-respecting, keyed by a hashed subject; no contact values.

| Event | Why |
|---|---|
| `list_view`, `entry_view`, `place_view` | Usage and returning clients (CP8 test 1) |
| `search`, `search_zero_result` | Search quality; "Start this list" funnel |
| `filter_change`, `view_toggle` | Interface use |
| `share_click` (channel), `copy_link` | Social campaigns |
| `upgrade_panel_view`, `subscribe_click`, `subscription_started` | Conversion (CP8 test 2) |
| `quota_hit` | Calibrate free limits |
| `enquiry_sent`, `enquiry_answered` | Core value of the relay |
| `claim_started`, `claim_completed`, `optin_recorded` | Supply funnel |
| `report_submitted`, `removal_requested` | Quality and law |
| `contributor_signup`, `entry_added`, `task_completed`, `verification_recorded` | Volunteer capacity |
| `campaign_sent`, `message_delivered`, `message_replied`, `optout` | Outreach test against Google and Meta |
| `sale_recorded`, `allocation_created`, `payout_paid` | Money |

Metrics tracked from these: weekly returning-user rate by place and list type; share of views from search, share and direct; conversion free to subscriber; revenue per list; cost per verified record; verification completion rate; accuracy by source and verifier; expired-check share; zero-result rate; indexed share.

## Appendix H. Named tests beyond the rule tests

Place path constraint; slug collision with list-type slug; folding rules one by one; query folding finds Urdu variants; concept synonym lookup; import mapper header guesses (English, Urdu, Roman Urdu); phone normalisation to E.164 by country; duplicate scoring examples (same shop two spellings; different shops same road); merge keeps earliest credit; claim OTP flow; verification guard matrix; expiry and grace; rollup refresher against recount; list query plan uses the place-prefix index; query budget (a list page's query count does not grow with the rows (no N+1)); entry page query budget; pagination caps; quota counters; canary seeding; URL resolver for place versus list; redirects from old scheme; ETag changes only when data or template version changes; fragments are `private, no-store`; JSON-LD matches visible content; sitemap shard size; publish throttle; ledger balance trigger rejects unbalanced; idempotent webhook replay; refund reversal; largest-remainder conservation; phase lock under changed phases; cap-months rule; hold release; payout two-person rule; MFA required for staff routes; every-route authorisation inventory; CSP header; log scrubber removes contacts; encrypted column round-trip with key rotation; erasure tombstone and suppression on re-import; opt-out suppression global; caps and quiet hours; auto-pause thresholds; agent evidence-quote check; agent isolation; agent cap and kill switch; map-link conversions; date and age formatting in English and Urdu; plural forms in Urdu; RTL screenshot comparisons at three widths.

## Appendix I. CI pipeline outline

```
on: pull_request, push to main
jobs:
  lint:      flake8 (blocking), physical-CSS lint, string-concatenation lint, import-boundary check
  test:      matrix python 3.11, 3.12, 3.13; services: postgres 16 with pg_trgm and unaccent
             steps: install from lock file; migrate up; migrate down (reverse test); pytest with coverage floor
  security:  pip-audit, bandit, secret scan, CSP check
  pages:     build sample-page set; page-weight gate (Appendix L); axe accessibility; RTL check
  browser:   (release only) Playwright suite at 320, 390, 1100 px, English and Urdu, light and dark
  load:      (release only) smoke load test against staging
release: tag -> deploy script to staging -> smoke test -> manual promote -> production -> smoke test; rollback script
```

## Appendix J. Repository layout (target)

```
backend/
  manage.py
  config/            settings/{base,dev,staging,prod}.py, urls.py, wsgi.py
  core/ places/ taxonomy/ entries/ intake/ catalog/ access/ accounts/
  ledger/ billing/ outreach/ moderation/ volunteers/ analytics/
  (later) topics/ personal/ commerce/
  each module: models.py, services.py, views.py (if public), admin.py, migrations/, tests/, templates/<module>/
  locale/            en and ur .po files
  static/            css (tokens), js (own small script, htmx)
docs/                decisions, requirements, specs, this plan, runbooks/
reports/ research_notes/ prototype/ scripts/
.github/workflows/   CI and release
```

## Appendix K. Coding conventions

- Python 3.12, flake8 at 127 characters, type hints on every `services.py` function; docstrings say why.
- Modules interact through services only; views contain no business rules; templates contain no business rules.
- Every list query is scoped by country and place path and uses the indexes; no unbounded counts on large sets; query-count tests on pages.
- All writes that change entry data go through one service that writes `change_log` and the audit log in the same transaction.
- Money is integer minor units; time comes from one clock function so tests can set it; no raw SQL outside migrations and documented performance queries.
- No `|safe`, no `innerHTML`, no inline event handlers; user text goes through escaping and `<bdi>` where names appear.
- CSS uses logical properties and tokens only; no hard-coded colours or sizes outside the token block.
- Every user-visible string is translated whole; no concatenated sentences.
- Feature flags and country switches wrap anything not for everyone.
- Commit messages say what and why; pull requests list the rules (R01 to R40) touched and link the decision-log change if any.
- Secrets never in code, tests, logs or comments; tests use fake values.

## Appendix L. Page-weight and performance gates

| Page | Target (compressed) | Hard ceiling (build fails) |
|---|---|---|
| List page, 25 rows | 11 KB | 18 KB |
| Entry page | 7 KB | 12 KB |
| Empty list | 4 KB | 6 KB |
| Inline CSS | 2 KB | 3 KB |
| JavaScript (HTMX plus own script) | under 30 KB total, never blocking | 30 KB |
| Fonts and images | none | none |
| Requests for the shell | 1 HTML plus 1 cached CSS file (or inline) and 1 deferred script | |

Latency goals in section 18.5. A list page's database query count must not grow with the number of rows (tested: the same count at 2 rows and at 25; currently 23). CSS is served once and cached for a year with hashed names.

## Appendix M. Glossary

| Term | Meaning |
|---|---|
| Entry | One business, facility, person or institution, stored once |
| List | A list type at a place; a view, not a copy |
| List type | A kind of thing (concept), such as eye hospitals |
| Place tree | World, region, country, state, district, city, area, society or street |
| Roll-up | Counts and previews for a place that include everything below it |
| Shell | The cacheable HTML of a page, identical for everyone |
| Fragment | A small private piece loaded after the shell |
| Check label | One of the four decided verification names |
| Draft | An entry marked "Not verified yet", hidden from public lists |
| Claim | The owner proves they run a business |
| Steward | A volunteer with a revocable right to correct a segment |
| Relay | The platform passes a message on without revealing contacts |
| Opt-in | A recorded agreement to be messaged |
| Phase (rate) | A period with a contributor rate of 50, 40 or 30 percent |
| Credit event | A record that a person added or verified an entry |
| Ledger | The append-only double-entry record of money |
| Canary | A planted fake entry used to catch copying or poor verification |
| Country switch | The per-country on-off control for selling, outreach and similar |
| Cut M | Work needed for the first paid sample |
| Pilot slice | Work needed for the 200-firm pilot only |
