# Hosting and cost model: Django + PostgreSQL 16 for alllists.com at 10 thousand, 1 million and 100 million entries

Research date: 2026-10-06. English only. This note models infrastructure, not people, counsel, domain or entity set-up.

How to read the flags used in this note:

- `[R]` read from this repository (file and line named).
- `[D]` derived by arithmetic from `[R]` facts and stated assumptions. Not measured (see section 11).
- `[EST]` my estimate or extrapolation with the assumption stated.
- `UNVERIFIED-V` a price seen only as a search-result summary of a vendor page.
- `UNVERIFIED-A` a price seen only on an aggregator or blog.
- **Price date for every price in this note: retrieved by WebSearch on 2026-10-06.** The pages' own effective dates are given where the snippet stated one. Direct fetches of vendor pages (hetzner.com, aws.amazon.com) were blocked by the network egress proxy, so **no price here was confirmed on a primary page**. Treat every dollar figure as a planning input to re-check before a purchase.

Assumed exchange rates (not looked up; change them in one place if wrong): 1 EUR = 1.15 USD, 1 USD = 280 PKR, 1 USD = 88 INR, 1 USD = 3.6725 AED (peg).

---

## 1. What the repository already says

Read: `docs/DEPLOYMENT.md`, `docs/TECHNICAL_PLAN.md` sections 2.1, 3.1, 3.5, 4.1 to 4.4, 5.2, 18.3 to 18.6, `docs/DECISIONS.md` (build log of 2026-10-06), `deploy/`, `scripts/`, `backend/entries/models.py`, `backend/taxonomy/models.py`, `backend/core/models.py`, `backend/analytics/models.py`, `backend/intake/models.py`, `backend/agents/models_ai.py`.

| Fact | Where | Why it matters here |
|---|---|---|
| Shape: Caddy or Nginx, Gunicorn (3 workers per unit), PostgreSQL 16, five-minute scheduler timer, nightly backup timer. No Redis, Celery or search engine until measured. | DEPLOYMENT.md section 1; `deploy/systemd/alllists-web.service` | S0 and S1 need one box and nothing else. |
| Starting server in the plan: Ubuntu 24.04, 2 vCPU, 4 GB RAM, 80 GB disk. | DEPLOYMENT.md section 2 | Used as the 10 thousand entry baseline. |
| Stages: S0 up to 5,000 entries; S1 50,000; S2 1 million (2 web, 1 worker, primary with automatic backups, country partitions, Splink); S3 10 million (read replica, search engine, second worker pool); S4 100 million (country groups on separate Postgres, search cluster, separate ledger DB). Views follow entries: under 5,000 a month at S0, 100,000 at S1, 1 million at S2, 10 million at S3, 100 million at S4. | TECHNICAL_PLAN.md 3.5 | The three scales asked for are S0 to S1, S2 and S4. |
| Measured sizing: about 1.7 KB per realistic entry (421 B entry, 701 B value meta, 151 B contacts, 125 B services, 345 B history), 100 million about 175 GB; list query 1.7 ms; country-wide category 50 ms; unscoped fuzzy name search 150 to 520 ms; 2.4 GB restored in 34 s with four jobs. | TECHNICAL_PLAN.md 4.3, 18.4 | The plan's number is a lower bound (section 2.3). The restore rate is used for recovery times. |
| Plan's own infrastructure estimates per month: S0 USD 1 to 32, S1 37 to 157, S2 217 to 900, S3 1,775 to 6,110, S4 14,610 to 52,620. AI drafting at S2 USD 2,500 to 8,300 a month. | TECHNICAL_PLAN.md 18.6 | Compared with this model in section 8. |
| Recovery goals: S0 to S1 loss up to last nightly dump, restore in 1 day; S2 15 minutes (WAL), 4 hours; S3 to S4 5 minutes, 1 hour with replica failover. | TECHNICAL_PLAN.md 18.4 | Logical dumps cannot meet the S4 goal (section 3). |
| Backup script: `pg_dump -Fc -Z6` nightly, keeps 14 daily and 8 weekly. | `scripts/backup.sh` | Sizing of backup storage at S0 to S2. |
| Search: Postgres trigram first; engine adapter behind `catalog/search_backend.py`; GIN trigram indexes already exist on `entries_entry.name_fold`, `entries_namevariant.text_fold`, places names and concept labels. | `backend/*/migrations/0002_*`, `core/pg.py` | GIN index size is included in the entry size. |
| Build log of 2026-10-06 decision **E27: lists are stored rows**, one `PlaceList` per list type per place, created by `manage.py generate_lists`; the log itself warns "hundreds of millions of rows". | DECISIONS.md build log; `backend/taxonomy/models.py:143`; `backend/core/management/commands/generate_lists.py` | **TECHNICAL_PLAN.md rule 3.1.2 and section 5.2 still say list-places are "computed, never pre-created".** The plan text is stale on this point. Section 2.2 sizes the new table. |
| 235 list types in the seed file (236 lines with header). | `backend/taxonomy/data/list_types.csv` | The 235 multiplier for `PlaceList`. |
| Place tree seed about 194,000 places (250 countries, 3,900 regions, 40,000 districts, 150,000 cities), marked uncertain. | TECHNICAL_PLAN.md 5.1 | The place multiplier for `PlaceList`. |
| Every audited write takes one global advisory lock (`pg_advisory_xact_lock(727001)`) and extends one hash chain. | `backend/core/models.py` `audit()` | Caps write throughput and blocks splitting the audit chain by country (section 10). |
| AI draft pipeline: hosted adapter uses Claude Haiku 4.5, page text capped at 20,000 characters, 400 output tokens; caps `AI_DAILY_CAP_MINOR`, `AI_MONTHLY_CAP_MINOR`, kill switch. | `backend/agents/models_ai.py`; `deploy/env.example`; `docs/runbooks/ai-spend-runaway.md` | Section 7. |

---

## 2. Database size

### 2.1 Row-size method

PostgreSQL 16 heap tuple = 24 bytes header (23 rounded up to 8) + data (each column aligned) + 4 bytes line pointer. Variable text under 127 bytes carries a 1-byte header, longer text a 4-byte header (no TOAST compression below about 2 KB). B-tree leaf entry = 8-byte header + key (rounded to 8) + 4-byte line pointer, divided by 0.9 for fillfactor; deduplicated non-unique indexes on repeated keys cost about 7 bytes per row (PostgreSQL 13 and later). Django on PostgreSQL also creates a second `_like` (varchar_pattern_ops) index for every `CharField` with `db_index=True` or `unique=True`; this is counted.

Assumed content of one **average published Pakistani business entry** (assumption, change if the real mix differs): name 28 characters, description 300 characters, address JSON 150 B, address text 70 B, place path 36 B, website 28 B, add-on JSON 220 B, payment methods JSON 26 B.

### 2.2 Per-entry arithmetic `[D]`

`Entry` row, data bytes (aligned sum): id 8, uid 27, country 3, entity_type 9, concept_id 8, name 29, name_lang 3, name_fold 29, description 304, status 5, publish_state 10, address JSON 151, address_text 71, place_id 8, place_path 37, lat and lon 12 each, precision 9, coord_source 8, coord_date 4, service_area `{}` 9, website 29, size_band 8, year 2, languages 15, price_band 3, payment_methods 27, addons 221, template version 4, claim_state 10, listing_plan 6, flags 8, created_via 8, created_by 8, source 8, three timestamps 24, nulls 0 = **1,145 B**. Heap tuple = 24 + 1,145 + 6 (null bitmap) rounded to 8 = 1,176, plus 4 = **1,180 B**.

`Entry` indexes (bytes per row): primary key 22; uid unique 49; uid `_like` 49; country_code 7 (dedup); country_code `_like` 7; name_fold btree 49; name_fold `_like` 49; place FK 7; primary concept FK 7; parent FK 7; created_by FK 7; source FK 7; merged_into FK 7; `entry_list_query` (country, place_path, concept, publish_state) 84; `entry_claim_idx` 31; GIN trigram on name_fold about 100 (`[EST]`: about 30 trigrams per 28-character name at 2 to 3 bytes each plus keys) = **about 490 B**.

Child and event rows (rows per entry are assumptions; tuple bytes include the line pointer, index bytes include FK indexes):

| Table | Rows per entry | Tuple B | Index B per row | Bytes per entry |
|---|---|---|---|---|
| `Entry` (heap 1,180 + indexes 490) | 1 | 1,180 | 490 | 1,670 |
| NameVariant | 0.5 | 108 | 203 (btree, `_like`, GIN, FKs) | 156 |
| Contact (encrypted value 60 B plus 16 B overhead; 64-char hash with btree and `_like`) | 1.6 | 220 | 216 | 698 |
| Social | 0.5 | 116 | 29 | 73 |
| Hours | 1.5 | 84 | 29 | 170 |
| Service | 1.0 | 228 | 36 | 264 |
| Product | 0.5 | 148 | 36 | 92 |
| Speciality | 0.8 | 124 | 36 | 128 |
| Identifier | 0.5 | 140 | 29 | 85 |
| AreaServed, Equipment, Branch | 0.3, 0.1, 0.1 | 84, 132, 148 | 36, 29, 29 | 70 |
| ValueMeta (one per field with provenance) | 5.0 | 180 | 76 | 1,281 |
| VerificationEvent (append-only) | 1.5 | 156 | 43 | 299 |
| VerificationCurrent | 2.0 | 108 | 69 | 354 |
| CreditEvent | 1.0 | 84 | 36 | 120 |
| ChangeLog (`core`, one row per field change) | 3.0 | 148 | 29 | 532 |
| Claim, consent, merge, company section, steward (blended) | 0.1 | 124 | 29 | 15 |
| **Subtotal, heap plus indexes** | | | | **6,011** |
| AuditLog, 1.0 row per create (about 300 B tuple; hash unique index 93; pk 22) | 1.0 | 300 | 115 | 415 |
| `intake.ExternalRecord` for imported entries (unique source+external id) | 1.0 | 100 | 90 | 190 |
| **Total** | | | | **6,616 B** |

Heap-only share (tuples without indexes): 4,185 + 300 + 100 = 4,585 B. Indexes are about 31% of the total.

Add 15% for dead tuples, free space and visibility maps: 6,616 x 1.15 = **7,608 B**. **Planning figure: 7.5 KB per entry.** For comparison the plan's measured 1.7 KB (`TECHNICAL_PLAN.md` 4.3) is 4.4 times smaller. The plan's `Entry` row was 421 B against my 1,180 B; the likely reasons are synthetic short strings in the measurement, no `_like`, GIN or FK indexes counted, and no audit or import rows. I keep both as a bracket: **low 1.7 KB, planning 7.5 KB**. A paid company page can add up to five sections of 4,000 characters (about 20 KB) per paying entry (`CompanySection.body`), negligible at under 1% of entries.

Not included: PostGIS `geography(Point)` plus GiST index at S1 (about 100 B per entry `[EST]`, adds 1.3%), full-text or translation columns, and anything for Urdu (frozen by the English-only rule).

### 2.3 `PlaceList` and the other tables that scale with places, not entries `[D]`

`PlaceList` columns: id (bigint), place_id, concept_id, created_at (8 bytes each). Heap tuple = 24 + 32 + 4 = **60 B**. Indexes: primary key 22; unique (place, concept) 31; (concept, place) 31 = **84 B**. **144 B per row**, 58% of it indexes.

Rows = places x list types. Scenarios (235 list types today):

| Scenario | Places | Rows | Heap | Indexes | Total |
|---|---|---|---|---|---|
| Pilot: Pakistan only, `--levels world,country,admin1,admin2,city` (600 places `[EST]`) | 600 | 141,000 | 0.01 GB | 0.01 GB | **0.02 GB** |
| Global GeoNames and Overture tree to city, unscoped run | 194,000 | 45.6 million | 2.7 GB | 3.8 GB | **6.6 GB** |
| Global tree plus 100,000 launch-country areas (1 million entry scale) | 294,000 | 69.1 million | 4.1 GB | 5.8 GB | **10.0 GB** |
| 100 million entry scale, 1.5 million places (areas, societies, streets from Overture and contributors) | 1.5 million | 352.5 million | 21.2 GB | 29.6 GB | **50.8 GB** |
| High case: 3.2 million places and 300 list types | 3.2 million | 960 million | 57.6 GB | 80.6 GB | **138 GB** |

The "hundreds of millions of rows" warning in the build log is correct from 1.5 million places upward. Two consequences:

1. **At the 10 thousand entry scale an unscoped `generate_lists` makes the database 6.6 GB, about 90 times larger than the entries it describes.** Use `--country PK --levels ...` (0.02 GB) until a measurement says otherwise.
2. One run of 352.5 million rows writes about 130 GB of WAL (rows plus three indexes, assuming WAL of about 2.5 times stored size `[EST]`) and takes roughly 1 to 4 hours on NVMe `[EST]`; it must not run on a primary with a replica lag budget without throttling by `--levels` or `--country`.

Most stored lists are empty by definition. Non-empty (place, concept) cells are what `analytics.RollupCell` holds; that table is the real index of lists that exist.

`RollupCell`: tuple about 148 B (country 3, place_path 37, concept 8, three counters 12, by_level JSON 41, percent 2, timestamp 8, id 8), indexes 154 B (pk 22, unique 67, place index 58, concept FK 7) = **302 B per non-empty cell**. Non-empty cells `[EST]`: 25,000 at 10 thousand entries, 1.2 million at 1 million, 60 million at 100 million (upper place levels collapse many entries into few cells). Sizes: 0.01 GB, 0.36 GB, **18 GB**. It is rewritten every five minutes, so expect heavy update churn and set a lower `fillfactor`.

`Place`: tuple 196 B plus seven indexes 241 B plus two `PlaceName` rows (100 B each plus trigram GIN about 150 B each) = about 940 B per place. 194,000 places = 0.18 GB; 3 million places = 2.8 GB. Note `Place.path` has `db_index=True` and also an explicit `varchar_pattern_ops` index, so it carries redundant indexes (small).

`analytics.Event` `[EST]`: one event per 20 page views, 250 B with indexes: 100 million views a month = 5 million events = 1.25 GB a month; keep 90 days.

Ledger, billing, accounts, outreach, moderation and volunteers: under 1 GB at all three scales, except `outreach.message` and `delivery_event` which grow with campaigns (pass-through cost, section 7).

### 2.4 Database size at the three scales

| Component | 10 thousand entries | 1 million entries | 100 million entries |
|---|---|---|---|
| Entries and children, low (1.7 KB) | 0.017 GB | 1.7 GB | 170 GB |
| **Entries and children, planning (7.5 KB)** | **0.075 GB** | **7.5 GB** | **750 GB** |
| `PlaceList` (scoped pilot / 294k places / 1.5M places) | 0.02 GB | 10.0 GB | 50.8 GB |
| `RollupCell` | 0.01 GB | 0.36 GB | 18 GB |
| Places and names | 0.002 GB | 0.3 GB | 2.8 GB |
| Events (90 days), ledger, accounts, other | 0.05 GB | 0.5 GB | 15 GB |
| **Total, planning** | **about 0.16 GB** | **about 18.7 GB** | **about 837 GB (0.84 TB)** |
| Total, low (plan 1.7 KB) | about 0.1 GB | about 12.9 GB | about 257 GB |

Plan check: 100 million x 1.7 KB = 170 GB against the plan's 175 GB; the planning figure of 750 GB is the one to budget storage with.

---

## 3. Sizing by scale (what to run)

Traffic assumptions `[EST]`: monthly human page views follow the plan's stage table (50,000 at 10 thousand entries, between S0 and S1; 1 million; 100 million). Crawler and scraper traffic is assumed to be 3 times human traffic (so 4 times the requests in total). Average page: 60% entry pages at 7 KB, 40% list pages at 11 KB (plan 18.5 budgets) = 8.6 KB compressed. Bytes served = views x 8.6 KB x 4.

| Item | 10 thousand entries | 1 million entries | 100 million entries |
|---|---|---|---|
| Monthly human views / total requests | 50,000 / 200,000 | 1 million / 4 million | 100 million / 400 million |
| Bytes served by CDN | 50,000 x 8.6 KB x 4 = 1.7 GB | 1 million x 8.6 KB x 4 = 34 GB | 100 million x 8.6 KB x 4 = 3.4 TB |
| Origin requests (CDN hit ratio 60% to 90% at 1M and 70% to 90% at 100M, plus uncached `/_f/` fragments at 0.3 per human view) | under 0.1 million | 0.7 to 2 million (0.3 to 0.8 requests a second average) | 40 to 120 million (15 to 45 a second average, peak about 5 times) |
| Database queries at peak (peak = 5 times the average origin rate; 23 queries per list page is the figure in the plan's performance notes, `TECHNICAL_PLAN.md` near line 2279) | negligible | 0.8 requests a second average, 4 at peak, x 23 = about 90 queries a second | 46 requests a second average, 230 at peak, x 23 = about 5,300 queries a second |
| **App servers** | the one box (web and worker together) | 2 web (2 vCPU, 4 GB each, 3 Gunicorn workers) + 1 worker (2 vCPU, 4 GB) | 4 to 6 web (4 vCPU, 8 GB) + 2 to 3 workers (4 vCPU, 8 GB); CPU is not the limit, the database is |
| **Database CPU and RAM** | 2 vCPU, 4 GB (plan). Whole database 0.16 GB fits in memory | 4 vCPU, 16 to 32 GB. Hot set: entry heap and indexes 7.5 GB + rollup 0.4 GB + the part of `PlaceList` that is read; 16 GB keeps it cached with `shared_buffers` at 4 GB | Total 0.84 TB. Assumed hot set 15% = 125 GB. Either one primary of 32 to 64 vCPU and 256 GB, or (plan S4) **4 country-group clusters of about 0.21 TB each**, each 16 vCPU and 128 GB (cheaper per GB of RAM in every provider below) plus a small separate ledger database |
| **Storage (database)** | 80 GB disk (plan) is ample | 100 GB NVMe or gp3 (18.7 GB data x 2.5 for growth, WAL and vacuum headroom = 47 GB; rounded) | 4 clusters x 500 GB NVMe (data 0.21 TB x 2.4 for bloat, WAL and rebuild room); total 2 TB, 4 TB with replicas |
| **Read replicas** | none | none for load (plan defers to S3); one streaming **standby** for high availability is the choice at S2 | 1 replica per cluster for failover plus reads (plan S3 to S4); 2 for the busiest country group |
| **Backups** | Nightly `pg_dump -Fc -Z6` about 10 to 15 MB (heap 4.6 KB x 85% = 3.9 KB, 3 to 4 times compression, about 1 to 1.5 KB per entry); 22 kept = under 0.5 GB; copy to a different provider | Dumps about 1.5 to 2 GB each (1 to 1.5 GB entries + 0.6 GB `PlaceList` rows at about 8 B compressed); 22 kept = about 44 GB. Add WAL archive and pgBackRest from S2 (plan: 15 minute loss). Restore by extrapolating the plan's measured 70.6 MB/s: 18.7 GB / 70.6 MB/s = about 4.4 minutes | **Logical dumps stop being viable.** Restore at the measured rate: 837 GB / 70.6 MB/s = 11,860 s = **3.3 hours**, plus index rebuilds for GIN and the 352-million-row `PlaceList`, against a plan goal of 1 hour. Use physical backups (pgBackRest, zstd, full weekly, incremental daily, 14 days): 2 fulls at about 0.45 x 837 GB = 750 GB + 12 incrementals at about 2% churn (17 GB each, 200 GB) + WAL about 20 GB a day compressed x 14 = 280 GB = **about 1.2 to 1.5 TB** in object storage, plus a standby that can be promoted (the only way to meet 1 hour) |
| **CDN and caching** | Cloudflare Free; shared HTML cached (`s-maxage`, plan 3.4); 1.7 GB is nothing | Cloudflare Free or Pro; origin egress = (1 - hit ratio) x 34 GB = 3 to 14 GB. The long tail of 1 million rarely visited pages keeps the hit ratio low; set long `s-maxage` plus `stale-while-revalidate` | Cloudflare Business for bot management, or CloudFront flat plan. Origin egress = 10% to 30% of 3.4 TB = 340 GB to 1 TB. Cache key includes `TEMPLATE_VERSION` and page `updated_at` (plan 3.4), so no mass purge |
| **Email** | 2,000 a month (sign-up codes, enquiry relay, alerts) | 200,000 a month `[EST]` | 10 million a month `[EST]` (0.1 per entry per month: claims, enquiry relay, digests, alerts). Outreach campaigns are WhatsApp and SMS led and charged to buyers (section 7) |
| **Search backend** | Postgres `pg_trgm` (existing GIN indexes); no engine | Postgres, always scoped by place (unscoped fuzzy search 150 to 520 ms at 1M, plan 4.3). No engine until search p95 exceeds 500 ms (plan S3 trigger) | Dedicated engine behind `catalog/search_backend.py`. 100 million documents x about 300 B (name, labels, place path, concept) = 30 GB raw, 90 to 150 GB indexed `[EST]`, 3 data nodes of 64 GB RAM. Self-host Meilisearch or OpenSearch (Meilisearch Cloud overage of USD 0.20 per 1,000 documents would be USD 20,000 a month at 100 million documents, section 4) |
| **Object storage** | under 1 GB (backups 0.5 GB, claim documents 0.2 GB) | about 75 GB: dumps 44 GB + WAL 10 GB + claim documents (1% of entries claim with 2 MB evidence = 20 GB) + extracts 1 GB | about 4 TB: backups 1.5 TB + claim documents (1% x 100 million x 2 MB = 2 TB) + extracts and log archive 0.4 TB |
| **Monitoring** | Sentry free, UptimeRobot free, Grafana Cloud free (plan 2.1); `/staff/metrics/` and `/healthz` already exist | Sentry Team, one uptime tool, Grafana Cloud, `pg_stat_statements` | Metrics and logs for about 20 hosts: Sentry Business plus volume, Grafana Cloud Pro or self-hosted Prometheus and Loki, Postgres exporter per cluster, pager |

---

## 4. Provider price inputs

All prices below: WebSearch, 2026-10-06. Source flag in the last column. Nothing confirmed on a primary page.

### 4.1 Option A: single VPS provider (Hetzner Cloud and Dedicated)

| Item | Price (excluding VAT) | Note | Flag |
|---|---|---|---|
| CPX22 shared AMD | EUR 19.49 a month | Effective 15 June 2026 (was 7.99); applies to new orders | UNVERIFIED-A (several blogs agree) |
| CPX52 | EUR 100.49 | June 2026 | UNVERIFIED-A |
| CPX62 | EUR 171.99 | June 2026 | UNVERIFIED-A |
| CCX13 / CCX23 / CCX33 / CCX53 (dedicated vCPU) | EUR 42.99 / 85.99 / 138.49 / 533.49 | June 2026; up 113% to 173% | UNVERIFIED-A |
| CX and CAX cost-optimised lines | "currently not available" on Hetzner's cloud page per two blogs; increases 30% to 38% | Do not plan on them | UNVERIFIED-A |
| Dedicated AX52 (8 cores, 64 GB, 2 x 1 TB NVMe) | EUR 89.60 | possibly stale | UNVERIFIED-A |
| Dedicated AX102 (16 cores, 128 GB, 2 x 1.92 TB NVMe) | EUR 257.30 plus setup EUR 129 or 269 (sources conflict) | | UNVERIFIED-A |
| Volumes | EUR 0.044 per GB a month | one source says a rise to USD 0.12 from April 2026; conflict | UNVERIFIED-A |
| Object Storage | EUR 6.49 a month including 1 TB stored and 1 TB egress; EUR 8.70 per extra TB; EUR 1 per extra TB egress (July 2026) | | UNVERIFIED-A |
| Storage Box BX41 (20 TB) | EUR 40.60 | | UNVERIFIED-A |
| Singapore location | 1 TB traffic included (20 TB in EU); USD 8.49 per extra TB; smaller June increase | | UNVERIFIED-A |
| Managed PostgreSQL | none offered | self-managed only | n/a |
| Locations | Germany, Finland, Singapore, US; none in the Gulf or South Asia | | n/a |

### 4.2 Option B: hyperscale managed stack (AWS, regions Mumbai ap-south-1 and UAE me-central-1)

| Item | Price | Note | Flag |
|---|---|---|---|
| RDS PostgreSQL db.r6g.xlarge (4 vCPU, 32 GB) on demand | USD 374 a month Mumbai; USD 404 UAE; USD 379.60 US East ($0.52 an hour) | Multi-AZ doubles the instance price | UNVERIFIED-A (bytebase dbcost) |
| RDS 1-year and 3-year reserved, UAE | USD 250 and USD 170 a month | cuts by 38% and 58% | UNVERIFIED-A |
| RDS gp3 storage | USD 0.115 per GB a month (US East) | I use USD 0.138 for Mumbai and UAE `[EST]` (+20%) | UNVERIFIED-A, EST |
| Larger RDS sizes | I price the 4xlarge at four times the xlarge (AWS prices scale linearly by size within a family) | | EST |
| EC2 m7g.large | USD 0.0583 an hour Mumbai (USD 42.6 a month); USD 0.100 an hour in me-central-1 (USD 73) | one snippet labelled me-central-1 "Bahrain"; me-central-1 is UAE. Label conflict | UNVERIFIED-A |
| EC2 m7g.xlarge | USD 0.200 an hour me-central-1 (USD 146); m7g.2xlarge by doubling USD 292 | | UNVERIFIED-A, EST |
| Aurora PostgreSQL db.t4g.xlarge, UAE | from USD 251 a month | not used | UNVERIFIED-A |
| CloudFront flat-rate plans (launched Nov 2025) | Free USD 0 (1M requests, 100 GB); Pro USD 15 (10M requests, 50 TB); Business USD 200 (125M requests); Premium USD 1,000 (500M requests) | one distribution, one apex domain | UNVERIFIED-A |
| CloudFront pay as you go | 1 TB and 10 million requests free; India USD 0.109 per GB; Middle East USD 0.110 then 0.085 then 0.080; HTTPS requests USD 0.012 per 10,000 India, USD 0.016 Middle East | | UNVERIFIED-A |
| S3 Standard Mumbai | INR 2.10 per GB a month (about USD 0.024); internet egress about INR 8 to 9 per GB after the first 100 GB | | UNVERIFIED-A |
| OpenSearch r7g.xlarge.search | USD 0.388 an hour US East (USD 283 a month); r6g.xlarge.search USD 0.335; gp3 USD 0.08 per GB | | UNVERIFIED-A |
| Amazon SES | USD 0.10 per 1,000 emails | | UNVERIFIED-A |
| ALB, NAT gateway, CloudWatch | about USD 25, 35 and 30 a month at 1M scale | not searched | EST |

### 4.3 Option C: regional provider close to South Asia (Vultr, Mumbai and Delhi)

| Item | Price | Flag |
|---|---|---|
| Regular Cloud Compute 2 vCPU, 4 GB, 80 GB, 3 TB | USD 20 a month | UNVERIFIED-A |
| Regular 4 vCPU, 8 GB, 160 GB, 4 TB | USD 40 | UNVERIFIED-A |
| Optimized Cloud Compute 2 dedicated vCPU, 4 GB, 100 GB NVMe, 3 TB | USD 28 | UNVERIFIED-A |
| Egress above included | USD 0.01 per GB | UNVERIFIED-A |
| Managed PostgreSQL, general purpose optimised 4 vCPU, 16 GB, 80 GB with 2 replica nodes | USD 840 a month for three nodes, so about USD 280 a node (derived) | UNVERIFIED-A, derived |
| Managed PostgreSQL premium AMD node 4 vCPU, 16 GB, 384 GB | USD 0.92 an hour = USD 672 a month | UNVERIFIED-A |
| Regions listed for managed databases | Bangalore, Mumbai, Delhi | UNVERIFIED-A |
| Object storage, load balancer, bare metal | not found in this search | not priced |
| (alternative) DigitalOcean managed PostgreSQL | single node USD 15 (1 GiB) to USD 243 (16 GiB); high availability from USD 60 (primary plus standby at USD 30 each); Bangalore availability not confirmed | UNVERIFIED-A |

### 4.4 Option D: regional Gulf (Oracle Cloud Dubai and Jeddah; Azure UAE North as the managed swap-in; Pakistan-local note)

| Item | Price | Flag |
|---|---|---|
| OCI VM.Standard.E4.Flex | USD 0.025 per OCPU hour (1 OCPU = 2 vCPU) | UNVERIFIED-A |
| OCI memory | USD 0.0015 per GB hour from my recollection of the OCI list; **not found in this search** | EST |
| OCI Block Volume | USD 0.0255 per GB a month | UNVERIFIED-A |
| OCI outbound data transfer | one source says all outbound charges were removed in 48 regions in February 2026; surprising, confirm | UNVERIFIED-A |
| OCI Database with PostgreSQL | priced as compute plus a service fee plus storage; rate not retrieved | not priced; self-managed PostgreSQL on VMs is modelled |
| Regions | Dubai (me-dubai-1) and Jeddah (me-jeddah-1) exist | UNVERIFIED-A |
| Azure Database for PostgreSQL flexible server, UAE North, Standard_D4ds_v5 (4 vCPU, 16 GB) | USD 317 a month (USD 0.868 an hour) | UNVERIFIED-A |
| Nayatel Cloud (Pakistan, hosted in Pakistan) | packages from PKR 2,999 a month (about USD 11); configurations not retrieved | UNVERIFIED-A; use only if Pakistani data residency is required |

OCI compute arithmetic: price = (vCPU / 2) x 0.025 x 730 + GB x 0.0015 x 730. 4 vCPU and 32 GB = 36.5 + 35.0 = USD 71.5. 16 vCPU and 128 GB = 146.0 + 140.2 = USD 286. 8 vCPU and 64 GB = USD 143. 2 vCPU and 8 GB = USD 27. 4 vCPU and 16 GB = USD 54.

### 4.5 Shared services

| Service | Price | Flag |
|---|---|---|
| Cloudflare Free | USD 0, unlimited bandwidth, basic bot fight mode | UNVERIFIED-A |
| Cloudflare Pro / Business | USD 20 a month annual or 25 monthly / USD 200 annual or 250 monthly, per domain | UNVERIFIED-A (older pages say 20 and 200; conflict resolved by a June 2026 source) |
| Cloudflare R2 | USD 0.015 per GB a month, zero egress; USD 4.50 per million writes, USD 0.36 per million reads | UNVERIFIED-A |
| Backblaze B2 | USD 0.00695 per GB (USD 6.95 per TB) a month; egress free up to 3 times stored | UNVERIFIED-A |
| Postmark | USD 15 a month for 10,000 emails, overage USD 1.80 down to USD 1.20 per 1,000 | UNVERIFIED-A |
| Resend | Free 3,000 a month (100 a day); Pro USD 20 for 50,000, USD 35 for 100,000 | UNVERIFIED-A |
| Brevo | free 300 a day; paid from about USD 9 | UNVERIFIED-A |
| Meilisearch Cloud | Build USD 30 a month (50,000 searches, 100,000 documents; extra searches USD 0.40 per 1,000, extra documents USD 0.30 per 1,000); Pro 250,000 searches and 1 million documents (overage USD 0.30 and 0.20 per 1,000; base price not retrieved) | UNVERIFIED-A |
| Typesense Cloud | hourly by RAM and CPU; about USD 21.60 a month at 0.5 GB; high-availability 3 nodes about USD 86 at the smallest | UNVERIFIED-A |
| Sentry | Developer free (5,000 errors); Team USD 26 a month annual; Business USD 80 | UNVERIFIED-A |
| Better Stack | free plan; paid from USD 24 | UNVERIFIED-A |
| Grafana Cloud | free plan; Pro from USD 19 plus usage | UNVERIFIED-A |
| UptimeRobot | free tier (plan 2.1); paid price not retrieved | not priced |
| Claude API | Haiku 4.5 USD 1 / 5 per million tokens in and out; Sonnet 4.6 USD 3 / 15; batch 50% off; cache reads 0.1 times. The repo's own research note (2026-10-05, primary page fetched then) lists Sonnet 5.5 at USD 2 / 10 | UNVERIFIED-A this session; V in repo note |

---

## 5. Monthly infrastructure cost by option and scale

Each line shows the arithmetic. "Core" = compute, database, storage, load balancer, search and object storage. Wrapper costs (CDN, email, monitoring) are added in section 5.5 so options compare on equal terms. Excluded everywhere: staff time, domain, counsel, legal entity, payment fees (section 6), AI (section 7), one-off dedicated-server set-up fees.

### 5.1 Scale 1: 10 thousand entries

| Option | Build | Arithmetic | Monthly (USD) |
|---|---|---|---|
| A Hetzner | One CPX22 (2 vCPU, 4 GB, 80 GB) running everything; Hetzner backup option (20% of server) and Object Storage for off-box copies | 19.49 + 3.90 + 6.49 = EUR 29.9 = USD 34 | **USD 25 to 45** |
| B AWS | Self-managed on one EC2 m7g.large in Mumbai; or managed (RDS db.t4g.medium class, price not found, about USD 50 to 70 `[EST]`, plus a small EC2 about USD 15 and storage) | EC2 42.6 + 30 GB EBS 3 + S3 and misc 5 = USD 51 self-managed; managed about USD 90 to 200 `[EST]` | **USD 50 (self-managed) to 200 (managed, Multi-AZ)** |
| C Vultr Mumbai or Delhi | One Regular 2 vCPU, 4 GB, plus 20% backups | 20 + 4 = USD 24 | **USD 20 to 35** |
| D Oracle Dubai | One 1 OCPU (2 vCPU), 8 GB VM plus 100 GB volume; Nayatel from about USD 11 if Pakistani hosting is wanted | 18.25 + 8.76 + 2.55 = USD 29.6 | **USD 30 to 40** |

### 5.2 Scale 2: 1 million entries (plan S2)

| Option | Build | Arithmetic | Monthly (USD) |
|---|---|---|---|
| A Hetzner | AX52 dedicated primary (8 cores, 64 GB NVMe); 2 x CPX22 web; 1 x CPX22 worker; Object Storage; load balancer about EUR 7 `[EST]`. Optional second AX52 as streaming standby | no standby: 89.60 + 2 x 19.49 + 19.49 + 6.49 + 7 = EUR 161.6 = USD 186. With standby: + 89.60 = EUR 251.2 = USD 289 | **USD 186 (single DB) to 289 (with standby)** |
| B AWS | RDS db.r6g.xlarge, 100 GB gp3; 2 web and 1 worker m7g.large; ALB, S3, SES, Sentry, NAT, CloudWatch. CloudFront inside its free quota (34 GB, 4 million requests) | Mumbai single AZ: 374 + 14 + 3 x 43 + 138 = **USD 655**. UAE Multi-AZ: 808 + 28 + 3 x 73 + 138 = **USD 1,193** | **USD 655 to 1,193** |
| C Vultr | Managed PostgreSQL 4 vCPU, 16 GB (about USD 280 a node); 2 web 4 vCPU, 8 GB (USD 40 each); 1 worker (USD 40); object storage about USD 18 and load balancer about USD 10 `[EST]` | Single node: 280 + 80 + 40 + 18 + 10 = USD 428. With standby node: + 280 = USD 708 | **USD 428 to 708** |
| D Oracle Dubai | Self-managed primary and standby 4 vCPU, 32 GB (USD 71.5 each); 2 web and 1 worker 2 vCPU, 8 GB (USD 27); 500 GB volumes; load balancer about USD 15 `[EST]` | 2 x 71.5 + 3 x 27 + 500 x 0.0255 + 15 = USD 252. Managed swap-in: Azure UAE North D4ds_v5 x 2 for HA = USD 634 for the database alone, about USD 880 in total | **USD 252 (self-managed) to 880 (Azure managed)** |

### 5.3 Scale 3: 100 million entries (plan S4)

Design for A, C and D: 4 country-group clusters, each a primary plus one streaming replica, 16 vCPU and 128 GB where the provider offers it (the 4 x 0.21 TB split from section 3); a separate small ledger database; 4 to 6 web servers; 2 to 3 workers; 3 search nodes of 64 GB RAM; physical backups to object storage.

| Option | Arithmetic | Monthly (USD) |
|---|---|---|
| A Hetzner dedicated | 8 x AX102 (4 primaries + 4 replicas) = 8 x 257.30 = 2,058; ledger 2 x AX52 = 179; web 4 x CPX52 = 402; workers 2 x CPX52 = 201; search 3 x AX52 = 269; Storage Box BX41 40.60 + Object Storage (6.49 + 3 x 8.70 = 32.6) = 73; 2 load balancers 14; monitoring host 19.5. Sum EUR 3,216 = **USD 3,700** (core). One-off setup EUR 129 to 269 each x 8 = EUR 1,032 to 2,152 | **USD 3,000 to 5,000** (fewer replicas / six clusters) |
| B AWS | 4 clusters x (db.r6g.4xlarge Multi-AZ primary 2 x 1,616 + one read replica 1,616) = 4 x 4,848 = 19,392; storage 3 copies x 760 GB x 0.138 = 315; provisioned IOPS 1,000 `[EST]`; 6 web m7g.2xlarge 6 x 292 = 1,752; 3 workers 876; OpenSearch 3 x r7g.xlarge.search plus masters and storage 1,100 `[EST]`; CloudFront Premium flat plan 1,000 (pay as you go: 3,440 GB - 1,000 free = 2,440 x 0.11 = 268 + 390 million x 0.016 / 10,000 = 624, = 892); S3 4 TB 102; SES 10 million x 0.10 / 1,000 = 1,000; monitoring 1,000; inter-AZ and NAT transfer 2,000 `[EST]`; ALB 200. Sum **USD 29,700**. With 1-year reserved database instances (UAE xlarge 250 against 404 = 62%): database 19,392 x 0.62 = 12,000, total **USD 22,400** | **USD 22,000 to 38,000** (upper end for a support plan and more provisioned IOPS) |
| C Vultr (weakest data) | No source for a 16 vCPU managed node or 760 GB storage. Extrapolating the 4 vCPU node linearly at USD 70 a vCPU (USD 1,120 per 16 vCPU node): 8 nodes = 8,960; web 6 x 80 = 480; workers 3 x 80 = 240; search 3 x 160 = 480; object storage 130; load balancers 50; monitoring host 200. Sum **USD 10,500** | **USD 9,000 to 13,000, `[EST]`, do not rely on it** |
| D Oracle Dubai self-managed | 8 x (16 vCPU, 128 GB at 286) = 2,290; storage 3 copies x 760 GB x 0.0255 = 58 (a higher performance tier would cost more, not retrieved); web 6 x (4 vCPU, 16 GB at 54) = 324; workers 3 x 54 = 162; search 3 x (8 vCPU, 64 GB at 143) = 429; object storage 4 TB 130 `[EST]`; load balancers 50. Sum **USD 3,440** | **USD 3,400 to 6,000** |

### 5.4 Cost per entry, planning point

AWS at 100 million: USD 29,700 / 100 million = USD 0.0003 per entry a month. Hetzner: USD 3,700 / 100 million = USD 0.00004. The AI fill cost per record (USD 0.04 to 0.20) is 130 to 5,000 times the monthly infrastructure per entry.

### 5.5 Wrapper costs added to every option (CDN, email, monitoring)

| Scale | CDN | Email (assumed volume x price) | Monitoring | Wrapper total |
|---|---|---|---|---|
| 10 thousand | Cloudflare Free USD 0 | 2,000 x 0.10 / 1,000 = USD 0.20 (SES) or free tiers | free tiers USD 0 | **USD 0 to 1** |
| 1 million | Free USD 0 to Pro USD 25 | SES 200,000 x 0.10 / 1,000 = USD 20; Postmark USD 15 + 190 x 1.80 = USD 357; Resend and Brevo in between | Sentry Team 26 + Grafana or Better Stack 0 to 70 | **USD 50 to 100** typical (USD 20 + 25 + 26 + 0 to 30); up to about 450 with Postmark |
| 100 million | Cloudflare Business USD 250 (bot management), or CloudFront USD 892 to 1,000 | SES 10 million x 0.10 / 1,000 = USD 1,000 (Postmark at 10 million would be about USD 12,000, so SES) | Sentry Business plus volume and Grafana Pro: USD 500 to 2,000 `[EST]` | **USD 1,750 to 3,250** |

AWS rows in section 5 already contain their own CDN, email and monitoring lines; do not add the wrapper to AWS twice.

---

## 6. Payment provider fees by market

The ledger and billing modules have a generic signed webhook and manual order recording; no gateway adapter exists yet (`research_notes/Platform requirements/01_monetisation.md` M-23). Fees are per successful payment unless stated.

| Provider and route | Fee found | Who can use it | Flag |
|---|---|---|---|
| **Stripe, Pakistan** | Not available: Pakistan is not a Stripe-supported country; Stripe Atlas is not offered to businesses operating from Pakistan | needs a UAE or US entity (cost of entity not researched) | UNVERIFIED-A; matches TECHNICAL_PLAN.md 2.3 |
| **Stripe, UAE entity** | 2.9% + AED 1 (about USD 0.27); +1% for international cards; +1% more if currency conversion applies. USD 100 domestic card: 2.9 + 0.27 = USD 3.17; international card USD 4.17; with conversion USD 5.17 | UAE-registered business, AED settlement | UNVERIFIED-A |
| **Stripe, US entity** | 2.9% + USD 0.30 (USD 3.20 on USD 100); Atlas USD 500 one time; Delaware fee USD 109 from 1 August 2026 | foreign route, but Atlas excludes Pakistan-operated businesses | UNVERIFIED-A |
| **JazzCash (Mobilink Microfinance Bank schedule of charges, Q1 2026)** | Online gateway (mobile account, voucher, card) 2.32%; QR or till 1.25%; incoming interbank transfer 2%; funds from a JazzCash account 2%; pay-by-link 3% plus tax; tap on phone 2% plus tax. PKR 5,000 ticket at 2.32% = PKR 116 | Pakistani company merchant account | UNVERIFIED-V (bank PDF snippet) |
| **Easypaisa (merchant online charges)** | Mobile account 1% including taxes; over-the-counter token 2% including taxes; no setup or annual fee. PKR 5,000 at 1% = PKR 50 | Pakistani company merchant account | UNVERIFIED-V (card fee not found) |
| **Raast P2M (QR, alias, request to pay)** | Merchant discount rate 0%; participating banks may charge up to 0.25% for onboarding and servicing; government subsidy of 0.5% or PKR 100 per transaction to banks ran 1 September 2025 to 30 June 2026 (status after that date not checked) | Pakistani merchants; bank account needed | UNVERIFIED-A |
| **Safepay (SBP-licensed gateway, reported)** | Cards 2.9% + PKR 30 domestic, 3.2% + PKR 30 international, excluding tax. PKR 5,000 domestic = 145 + 30 = PKR 175 (3.5%) | Pakistani company | UNVERIFIED-V (help page snippet) |
| **PayFast Pakistan** | fee set per merchant; no figure found | Pakistani company | not priced |
| **Razorpay (India)** | 2% domestic (cards, UPI, netbanking, wallets) plus 18% GST on the fee = 2.36%; international cards 3% plus GST = 3.54%; international bank transfer 1% plus GST; no setup or annual charge. INR 8,800 (about USD 100): domestic INR 208, international INR 312 | Indian entity | UNVERIFIED-V (Razorpay blog snippet) |
| **Paddle or Lemon Squeezy (merchant of record)** | 5% + USD 0.50 per transaction (USD 5.50 on USD 100); Lemon Squeezy adds 1.5% international, 1.5% PayPal, 0.5% subscriptions; Pakistani Lemon Squeezy sellers are paid out by PayPal only at a 3% fee (cap USD 30). Paddle reported to onboard sellers from any non-sanctioned country and to handle VAT, GST and US sales tax | foreign buyers without a foreign entity; answers the plan's open "foreign route" | UNVERIFIED-A |
| **Bank transfer, domestic (IBFT, Raast)** | no merchant fee found; the cost is staff time to match references in `/staff/orders/` | any Pakistani buyer | UNVERIFIED-A |
| **Bank transfer, international (SWIFT)** | incoming fee about USD 10 to 15 at Pakistani banks, up to USD 35; plus 2% to 5% exchange margin. USD 100 order: 12% to 20%; USD 1,000 order: 1.2% to 2% | invoice buyers of large lists (more than about USD 500) | UNVERIFIED-A |
| **Payoneer** | 1% receiving from marketplaces, 3% for a client card payment request; about USD 1.50 per USD withdrawal; up to 2% over mid-market for PKR | alternative to a foreign entity | UNVERIFIED-A |
| **Wise** | not opening new accounts for Pakistani residents since January 2026 | | UNVERIFIED-A |

Per USD 10,000 of monthly sales, fee cost by market (simple blends of the figures above):

| Market and route | Effective rate | Fee on USD 10,000 |
|---|---|---|
| Pakistan, wallet and Raast heavy (Easypaisa 1%, JazzCash 1.25% to 2.32%, Raast 0%) | 0.5% to 2.3% | USD 50 to 230 |
| Pakistan, cards through Safepay on PKR 5,000 tickets | 3.5% (3.1% at PKR 20,000) | USD 310 to 350 |
| UAE and Gulf cards, Stripe through a UAE entity, USD 100 tickets | 3.2% domestic, 4.2% to 5.2% international | USD 320 to 520 |
| India, Razorpay | 2.36% to 3.54% | USD 236 to 354 |
| Foreign buyers through a merchant of record, USD 100 tickets | 5.5% | USD 550 |
| SWIFT invoices of USD 1,000 | 1.2% to 3.5% | USD 120 to 350 |

Implication for the cost model: infrastructure at 1 million entries (USD 250 to 1,200 a month) is smaller than one month of fees on USD 10,000 of sales through a card route (USD 300 to 550). Fees only matter once the sales exist, and the cheapest route (Raast and wallets for Pakistan) is also the one the Pakistan notes already recommend.

---

## 7. AI agent costs at USD 0.04 to 0.20 per record

Per-record cost band given by the owner: USD 0.04 to 0.20. Cross-checks:

- The repo's research note (`research_notes/AI agent populated lists/agent_data_collection.md`, 2026-10-05) estimates search plus fetch plus extract at USD 0.03 to 0.06 per record with a Haiku-class model and USD 0.10 to 0.25 with Sonnet-class on heavier pages, plus USD 0.01 to 0.035 automated verification. The owner's band sits inside that.
- The shipped adapter calls Haiku 4.5 with up to 20,000 characters (about 5,000 tokens) and 400 output tokens: 5,000 x 1 / 1,000,000 + 400 x 5 / 1,000,000 = USD 0.007 a call. So USD 0.04 to 0.20 is 6 to 29 model calls per record at list price, or fewer calls plus search, proxy and verification fees. Batch (50% off) and cache reads (0.1 times) lower the model part.

One-time cost to fill all entries by AI (upper bound; no imports from Overture, Foursquare or registers):

| Scale | Low USD 0.04 | High USD 0.20 | If only 30% of records need AI (the rest imported free from open datasets, `[EST]`) |
|---|---|---|---|
| 10 thousand | USD 400 | USD 2,000 | USD 120 to 600 |
| 1 million | USD 40,000 | USD 200,000 | USD 12,000 to 60,000 |
| 100 million | USD 4 million | USD 20 million | USD 1.2 to 6 million |

Run rate if filling is spread out: 1 million over 12 months = 83,333 records a month = USD 3,333 to 16,667 a month; 100 million over 36 months = 2.78 million a month = USD 111,000 to 556,000 a month. The plan's S2 allowance (USD 2,500 to 8,300 a month, section 18.6) buys 12,500 to 207,500 records a month at this band.

Refresh multiplies this: the repo's research note says refresh cost per cycle is about the verification-only cost, so two cycles a year add roughly USD 0.01 to 0.035 x 2 per record a year plus any re-extraction. Human audit of a 5% sample adds USD 0.003 to 0.04 per record (research note, 1 to 3 minutes at USD 3 to 15 an hour).

Reading: **AI cost dominates infrastructure at every scale.** At 1 million entries the fill is USD 12,000 to 200,000 once against USD 300 to 1,200 a month of servers, which is 10 months to 55 years of server bills. Per entry, the AI fill (USD 0.04 to 0.20) is 130 to 5,000 times the monthly infrastructure share at 100 million (USD 0.0003 on AWS, USD 0.00004 on Hetzner). The caps (`AI_DAILY_CAP_MINOR`, `AI_MONTHLY_CAP_MINOR`) and cost per verified record are the budget control, not server size.

Pass-through messaging cost (not infrastructure): WhatsApp Pakistan marketing USD 0.0473 and utility USD 0.0100 per message from 1 April 2026 (TECHNICAL_PLAN.md 2.3, third-party page, not checked at Meta). A 100,000-message campaign is USD 1,000 to 4,730, charged to the buyer.

---

## 8. Totals and comparison with the plan

Monthly infrastructure, USD, price date 2026-10-06, core plus wrapper, no labour, no AI, no payments:

| Scale | A Hetzner (Germany or Finland; Singapore alternative) | B AWS managed (Mumbai or UAE) | C Vultr Mumbai or Delhi | D Oracle Dubai self-managed | Plan 18.6 estimate |
|---|---|---|---|---|---|
| 10 thousand entries | **25 to 45** | **50 to 200** | **20 to 35** | **30 to 40** (Nayatel from about 11) | S0 1 to 32; S1 37 to 157 |
| 1 million entries | core 186 to 289 + wrapper 50 to 100 = **240 to 390** | **655 to 1,193** (wrapper inside) | core 428 to 708 + wrapper 50 to 100 = **480 to 810** | core 252 + wrapper 50 to 100 = **300 to 350** (Azure managed swap: about **880 to 980**) | S2 217 to 900 |
| 100 million entries | core 3,700 + wrapper 1,750 to 3,250 = **5,500 to 7,000** | **22,000 to 38,000** (wrapper inside) | **10,500 + 1,750 to 3,250 = about 12,000 to 14,000, `[EST]`, weakest data** | core 3,440 + wrapper 1,750 to 3,250 = **5,200 to 6,700** | S4 14,610 to 52,620 |

Notes on the comparison:

- At 10 thousand and 1 million entries every option falls inside or below the plan's own estimate; the plan is conservative at the low end. At 100 million the AWS figure is inside the plan's range (low half); the dedicated-hardware options (Hetzner, Oracle) are below the plan's low end, about a quarter to a fifth of AWS. The difference (about USD 16,000 to 30,000 a month) is what buys managed failover, managed backups, support and no database administrator; it is roughly the monthly cost of a few engineers, so it is a staffing decision, not a hardware one.
- Hetzner's June 2026 reprice (CPX22 EUR 7.99 to 19.49, CCX13 EUR 15.99 to 42.99) removed its price lead at the VPS size: CPX22 at about USD 22 now sits level with Vultr Mumbai at USD 20 and Oracle at about USD 30, and the Asian options are 100 ms or more closer to Lahore and Karachi (typical round-trip times, not measured here). Hetzner's value now is in dedicated servers (AX52, AX102) and in bulk storage.
- Hetzner and Oracle numbers carry no managed database, no managed failover and no support contract. Vultr's managed PostgreSQL covers S1 to S2 only on the evidence found.
- Currency and tax: VAT, GST and Pakistani withholding are not included.

---

## 9. Recommended path

1. **Now (up to about 10,000 entries, S0 to S1).** One VM with 2 vCPU, 4 to 8 GB, in Mumbai, Delhi or Dubai (Vultr Mumbai about USD 24 including backups, or Oracle Dubai about USD 30), Cloudflare Free, the plan's own Caddy, Gunicorn and PostgreSQL 16 layout, the nightly `scripts/backup.sh` dump copied to a **different provider** (Backblaze B2 about USD 7 per TB, or Hetzner Object Storage EUR 6.49), Sentry free and UptimeRobot, SES or Resend free for email. Reason for Asia or Gulf over Germany: uncached `/_f/` fragments and the staff console go to the origin, and a European origin adds a few hundred milliseconds from Lahore. Cost USD 25 to 45 a month. **Run `generate_lists` only with `--country` and `--levels` (0.02 GB); an unscoped run adds 6.6 GB and 45.6 million rows.**
2. **Before the first payment gateway.** Raast and wallets (Easypaisa 1%, JazzCash 1.25% to 2.32%) for Pakistan and manual bank transfer through `/staff/orders/`; a merchant of record (Paddle at 5% + USD 0.50) or a UAE entity with Stripe for foreign cards; Safepay if cards are needed locally (3.5% on small tickets). Decide which one by what a counsel-cleared entity can open (open question Q-S/F12).
3. **At the plan's S1 trigger (5 paying buyers, about 50,000 entries).** Move PostgreSQL to a managed instance with point-in-time recovery or to a primary plus standby with pgBackRest: Vultr managed about USD 280 a node, DigitalOcean from USD 60 for primary plus standby (availability near South Asia unconfirmed), RDS Mumbai about USD 374 single-AZ plus storage. Keep one app server. Cost USD 100 to 500 a month.
4. **At 1 million entries (S2).** 2 web, 1 worker, 4 vCPU and 16 to 32 GB database with a standby, WAL archive (15 minute loss), country partitions on `Entry` and children. Budget USD 300 to 1,200 a month depending on provider; the cheaper end is self-managed on Oracle Dubai or Hetzner dedicated, the upper end is RDS Multi-AZ. Choose by who is on call, not by price. Keep search on PostgreSQL.
5. **Before 10 million entries (S3).** Add a read replica; test the search engine against the plan's 500 ms p95 trigger; self-host Meilisearch or OpenSearch (do not use Meilisearch Cloud at this size: USD 0.20 per 1,000 documents over 1 million).
6. **At 100 million (S4).** Four country-group clusters with replicas on dedicated hardware or reserved managed instances. Budget USD 5,000 to 7,000 a month (dedicated) or USD 22,000 to 38,000 (managed). Before getting there decide the two code-level questions in section 10 (audit chain and `PlaceList` shape); both are cheaper to settle at 1 million than at 100 million.
7. **Spend order.** Fix AI caps and cost per verified record before buying servers: the AI fill of the first 1 million entries (USD 12,000 to 200,000) equals 10 months to 55 years of S2 server bills.

---

## 10. What to monitor before upgrading

Thresholds come from the plan (18.3, 18.5, 3.5) unless marked `[mine]`.

| Signal | Measure from | Upgrade or act when |
|---|---|---|
| Origin latency | `scripts/loadtest.py`, access log | Uncached p95 over 300 ms (plan); shared pages from cache over 200 ms; private parts over 400 ms |
| Database query time | `log_min_duration_statement = 500`, `pg_stat_statements` | Query p95 over 50 ms (plan); any list query over 100 ms; query count per list page rising above the tested 23 |
| Memory fit | `pg_stat_database` cache hit ratio, `pg_buffercache` | Buffer cache hit under 99% [mine]; hot set above 70% of RAM [mine]; then move to the next RAM tier before adding CPU |
| Disk | volume usage, WAL growth, table and index growth (plan 18.3) | Data disk above 70% [mine]; WAL archive lag; `PlaceList` or `RollupCell` growth outpacing entries |
| CPU and connections | host metrics, `pg_stat_activity` | Sustained CPU above 60% on the primary [mine]; connections near `max_connections` (add pgbouncer first) |
| Vacuum | autovacuum lag, dead tuples on `analytics_rollupcell`, `core_auditlog`, `entries_entry` | Dead tuple share above 20% [mine]; `RollupCell` updates every five minutes are the usual cause |
| Replication | replication lag, replica promotion drill | Lag over 5 seconds, or before turning on read routing; failover drill passes |
| Search | search p95 and zero-result rate (plan) | p95 over 500 ms (plan S3 trigger) or zero-result rate over 15% |
| Restore | `scripts/restore_drill.sh` time, quarterly | Restore time over half the recovery goal [mine]. Extrapolated 3.3 hours at 0.84 TB against a 1 hour goal means physical backups and a standby are needed before about 150 GB of data [mine] |
| Backups | `record_ops backup` size and age | Nightly dump over 4 hours or 100 GB [mine]; a skipped drill alerts (plan) |
| CDN | cache hit ratio, share of origin requests from bots | Hit ratio under 60% [mine]; any address fetching over 500 distinct list pages a day (plan abuse rule); then rate rules, then Cloudflare Business |
| Audit write rate | wait time on advisory lock 727001, `pg_stat_activity` | Lock waits above 50 ms [mine]. Each `create_entry` takes the lock once; at an assumed 3 ms hold, 100 million audited creates is 100 million / 333 per second = 300,000 s, 3.5 days of pure lock time |
| Job queue and roll-ups | `/staff/jobs/`, age of the oldest `rollup_refresh` | Roll-up older than 15 minutes or a nightly recount mismatch (plan 4.4) |
| Email | bounce and complaint rate, SES reputation | Bounce above 5% or complaints above 0.1% [mine]; delivery failure above 10% pauses outreach (plan) |
| Payments | webhook failures, daily reconciliation | Any ledger difference (plan: alerts); webhook failure rate above 1% [mine] |
| AI spend | `/staff/agents/`, daily and monthly caps | Alert at 50% and 80% of the monthly cap (plan); cost per verified record above the planned band |
| Entry growth | entries per country | A country above about 50 million entries gets its own cluster (plan S4 trigger) |

---

## 11. Repo findings that change the cost, and limits of this note

Findings for the owner (no code was edited):

1. **Plan text and decision log disagree on stored lists.** TECHNICAL_PLAN.md 3.1.2 and 5.2 ("computed, never pre-created") against DECISIONS.md E27 (stored rows). The table is 144 B a row, 58% of it indexes; 235 types times 1.5 million places is 352.5 million rows and 51 GB.
2. **`PlaceList` has no `country_code`**, so it cannot be partitioned by country like the entry tables (plan 4.1) and would sit on one cluster when the entries are split into country groups at S4. It also keeps a surrogate `id` primary key; a composite primary key (supported by Django 5.2) would drop about 30 B a row (21%).
3. **One global audit chain** (`core/models.py audit()`): all audited writes serialise on one advisory lock and one hash chain. That limits bulk creation (3.5 days of lock time for 100 million creates at 3 ms a hold, section 10) and conflicts with plan 4.1, which says `audit_log` is partitioned by month and entries by country. Decide before S4 whether each country-group cluster keeps its own chain.
4. **The backup script is a logical dump with 22 retained copies**; correct at S0 to S2, wrong at S4 (section 3).
5. Django `_like` indexes and the GIN trigram index make indexes 31% of the entry footprint; the plan's measured 1.7 KB does not include them.
6. `Place.path` carries redundant indexes.

Limits:

- **Sizes are arithmetic, not measurements.** No PostgreSQL server is installed in this environment (only the `psql` client), so I could not load the schema and run `pg_total_relation_size`. The first staging rehearsal (DEPLOYMENT.md section 9) should load 100,000 entries and 1 million `PlaceList` rows and compare against section 2; the largest uncertainties are description length, rows per entry for children, GIN size and the 15% bloat allowance.
- **No price was confirmed on a primary vendor page** (fetch blocked). Aggregator figures can lag a vendor's own page by a few weeks, and Hetzner and several others repriced in 2026.
- Not priced for lack of data: Vultr object storage, load balancer, bare metal and large managed nodes; OCI PostgreSQL service fee and memory price; PayFast; UptimeRobot paid; Meilisearch Pro base price; Cloudflare Enterprise; AWS support plans.
- Traffic, crawler share, claim rate, email volume and the AI-filled share are assumptions; the owner's price band for AI (USD 0.04 to 0.20) is used as given.
- The Pakistani and Gulf latency comparisons are typical figures, not measurements from this project.
- Entity set-up for a UAE or US entity, Pakistani withholding and sales tax on gateway fees, and counsel are outside this model.

Sources (all retrieved by WebSearch on 2026-10-06; none opened on a primary page):

- Hetzner June 2026 repricing: wz-it.com, northflank.com, findstack.com, privatedevops.com, agentdeals.dev; Hetzner Object Storage and Storage Box: sliplane.io, whtop.com; Singapore: hetzner.com press and docs snippets; dedicated: websnp.com, lowendtalk.com.
- AWS: bytebase.com dbcost (RDS), aws-pricing.com and cloudprice.net (me-central-1), doit.com (EC2 Mumbai), egresscost.com and costbench.com (CloudFront), filebase.com and precisiontech.in (S3), cloudburn.io and coralogix.com (OpenSearch).
- Vultr: costbench.com, sparecores.com; DigitalOcean: infratally.com; Oracle: oracle.com price list snippets, holori.com, vpsranking.com; Azure: sparecores.com and bytebase.com; Nayatel: propakistani.pk, cloud.nayatel.com.
- Payments: Mobilink Bank schedule of charges Q1 2026 (mobilinkbank.com PDF), Easypaisa schedule of charges and merchant documentation, Raast notices (profit.pakistantoday.com.pk, bankalfalah.com, sbp.org.pk), Safepay help centre, Razorpay blog, learnwithhasan.com, dodopayments.com (Paddle and Lemon Squeezy), globalfeecalculator.com and ziina.com (Stripe UAE), jobbers.io and vaultleap.com (Pakistan receiving).
- Other services: Cloudflare (blazingcdn.com, costbench.com, toolradar.com), Backblaze (costbench.com), email (dupple.com, agentdeals.dev, brevo.com), Meilisearch (meilisearch.com docs, costbench.com), Typesense (markaicode.com), Sentry and Grafana (toolradar.com, costbench.com), Claude pricing (puter.com tutorial, docs.anthropic.com snippet), Neon and Supabase (not used).
