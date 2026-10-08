# AllLists.org: technical capabilities needed

Purely technical view, for the coding phase. No code is written yet. Recommendations here are mine, not owner decisions; the owner's decisions are in `docs/DECISIONS.md`. Scope rule C29: text and numbers only for now, no pictures or videos.

Last updated: 2026-10-05.

## Core idea in one paragraph

A list is a view (category at a place), not a copy. The data that grows is entries, each with a source, a verification level and a history. Everything below follows from that: store entries once, derive lists and roll-ups, and treat trust, freshness and money as first-class data.

## 1. Data management (the heart of the system)

| Capability | Plain meaning | Notes |
|---|---|---|
| Relational database with map support | One main database that also understands places and distances | PostgreSQL with PostGIS (my recommendation) |
| Place tree | World, region, country, state, district, city, area, street | Store the tree so that "everything under Lahore" is one fast query (materialised path or closure table) |
| Category taxonomy | One concept per list type, with local names and crosswalks | Concept table, alias table (language, region), crosswalk table to ISIC, ISCO, Overture, Foursquare, OSM, schema.org |
| Entries with typed core fields plus flexible per-type fields | Name, address, phone are fixed; MRI make, tutor subjects, MOQ vary by list type | Typed columns for the core; JSONB for add-ons; a field registry that validates add-ons per list type |
| Field-level provenance and verification | Every value knows its source, licence, date, who checked it and how | Needed for the verification levels (D19), licence compliance (D17) and buyer filters |
| History and audit | Never overwrite silently | Append-only change log; supports disputes, rollback and payout audits |
| Partitioning by country | Split data by country from day one | Matches the place tree and makes later scaling easy |
| Roll-up engine | Counts and previews for every place level | Precomputed aggregates updated incrementally; counts by verification level feed the list-page statistics (E14) |
| Retention and erasure | Delete personal data on request while keeping the audit trail | Tombstones plus separate store for sensitive fields |
| Backups and restore tests | Point-in-time recovery, tested | Untested backups do not count |

## 2. Intake and data quality

| Capability | Plain meaning |
|---|---|
| Importers | CSV, Excel and pasted lists with column mapping; open datasets such as Overture and Foursquare |
| Cleaning | Normalise names, phone numbers (international format), addresses, and spelling variants across Urdu, Arabic and Latin script |
| Duplicate detection and merging | The hardest data problem: blocking, similarity scoring, review queue, rules for which value wins |
| Geocoding | Turn addresses into coordinates; check licence terms of any service used |
| AI agent pipeline | Draft entries from many sources with structured output, saved evidence, second-source checks, cost caps and human review; never a source of truth (D14) |
| Licence and robots gate | Block any record whose source licence or terms forbid use; log the decision (D17) |
| Quality measurement | Sampling and audit sets to measure accuracy per source and per verifier |

## 3. Search

| Capability | Notes |
|---|---|
| Text, category and map search | Postgres full-text and trigram search is enough for millions of entries; add a dedicated search engine only after a measured limit |
| Multilingual search | Urdu, Arabic, transliteration, synonyms ("petrol pump" and "gas station"), common misspellings |
| Distance and area queries | PostGIS indexes |
| Ranking logic | Relevance and trust first; paid ranking (E15) kept separate, labelled and auditable |

## 4. Business logic (rules the system must enforce exactly)

| Capability | Notes |
|---|---|
| Verification state machine | Levels, expiry, re-check scheduling, evidence, who may move an entry up or down |
| Access and entitlement engine | What each user type sees: names-only preview, first few entries, paid roll-ups, subscriber without ads, usage limits |
| Revenue ledger | Immutable, double-entry, one line per person per sale; step-down rates locked per entry (50, 40, 30); refund windows |
| Payouts | Only when a list is sold (CP1); provider choice depends on country; KYC and AML for cash payouts; non-cash rewards first (CP9) |
| Outreach engine | Opt-in register, frequency caps, one-tap opt-out, templates, delivery through providers, delivery status callbacks, contacts never exposed to buyers (E13) |
| Segment stewardship | Claim, lease, 90-day inactivity expiry, dispute queue (C20) |
| Paid ranking and ads | Slots or auction, labelling, reporting |
| Moderation and takedown | Review queues, abuse reports, personal-data removal |

## 5. Web, design and experience

| Capability | Notes |
|---|---|
| Server-rendered pages | List, entry, place and category pages must be readable by search engines |
| Search-engine hygiene | Clean URLs by place and category, structured data (schema.org), sharded sitemaps, noindex for thin or empty pages, canonical tags |
| Right-to-left and Urdu typography | Proper fonts and layout, not an afterthought |
| Low-bandwidth, mobile-first | Pages light by design; text-only helps |
| Design system | Consistent components; visible trust badges for verification levels |
| Role dashboards | Contributor, surveyor (mobile-friendly task screens), business owner (claim and update), buyer, admin and moderator back office |
| Forms and wizards | Import, claim, verify, submit evidence |
| Accessibility | Keyboard and screen-reader basics |

## 6. Security and privacy

| Capability | Notes |
|---|---|
| Authentication | Strong password hashing, multi-factor for admins and payouts, optional sign-in with ORCID or similar for professionals |
| Authorisation | Role-based plus per-record checks; separation of duties for payouts and verification |
| Secrets management | Rotate the credentials already exposed in the prototype; keep secrets outside the code |
| Web attack protection | Input validation, SQL injection and cross-site scripting defences, CSRF, content security policy, secure cookies |
| Anti-scraping | Rate limits, bot detection, account checks, seeded fake entries (watermarks), traps for bulk copying (P15) |
| Fraud controls | Fake listings, fake reviews, fake contributors, payout fraud, spam through outreach |
| Privacy by design | Consent register, data minimisation, separate storage for sensitive fields (personal mobiles, ID numbers, child and health data), deletion workflow, per-country rules |
| Payment safety | Use hosted payment pages so card data never touches our servers |
| Encryption and logging | Encryption in transit and at rest; tamper-evident audit logs |
| Supply-chain safety | Dependency scanning, secret scanning, locked versions |
| Incident readiness | Written response plan and a practised restore |

## 7. Engineering practice and operations

| Capability | Notes |
|---|---|
| Architecture | One well-organised application (a "modular monolith") plus background workers; split into services only when measurements demand it |
| Background jobs and scheduler | Imports, re-verification reminders, roll-up refresh, outreach sends, payouts |
| Automated tests | Unit, integration, data-quality and ledger tests; migration tests. The repository has none today, which is why CI is red |
| Continuous integration and delivery | Tests, linting, security scans on every change; staged releases; safe database migrations |
| Environments | Development, staging, production |
| Observability | Logs, metrics, error tracking, uptime and cost alerts (AI spend especially) |
| Caching and delivery | Page and query caching, a content delivery network |
| Performance and load testing | Before each stage, not after |
| Infrastructure as code | Later, once more than one server exists |
| Feature flags | Switch features on by country or user group |

## 8. Measurement

Event tracking that respects privacy; funnels and returning-user cohorts (design test 1, CP8); revenue analytics (design test 2); data-quality dashboards (accuracy, freshness, coverage by place and category).

## 9. Payments and finance engineering

Payment providers differ by country and collection from Pakistan needs checking; multi-currency; tax and VAT; invoices; refunds and chargebacks; reconciliation against the ledger; payout provider and tax forms for contributors.

## 10. The six hardest technical problems

1. Duplicate detection and merging at scale across scripts and spellings.
2. Multilingual search that finds what people mean.
3. A correct, auditable money ledger with locked step-down rates.
4. Keeping verification honest (fake verifiers, stale data).
5. Resisting scraping while staying visible to search engines.
6. Publishing only pages that deserve to exist, at scale.

## 11. Build order (technical)

1. Data model, place tree, taxonomy, entries with provenance, import, duplicate detection, tests and CI.
2. Public pages with free preview, search, verification levels, claim flow.
3. Accounts, access tiers, ads, manual payment recording, revenue ledger.
4. Outreach through a provider, after legal advice.
5. Roll-ups, paid ranking, subscriptions, automated payments and payouts.
6. Search engine, read replicas and country sharding only when measured need appears.

## 12. Open technical decisions (suggested defaults)

| Decision | Suggested default |
|---|---|
| Backend language and framework | Python; Django for the admin and moderation back office, or the Flask or FastAPI draft already prepared. Decide at coding time. |
| Database | PostgreSQL with PostGIS |
| Hosting | One managed host and managed Postgres at first |
| Front end | Server-rendered; English and Urdu from the start |
| Job queue | A Postgres-backed or Redis-backed queue, whichever the framework supports best |
| Search | Postgres first |
