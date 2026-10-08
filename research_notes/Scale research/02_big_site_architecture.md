# How very large catalogue sites run, and what AllLists should do at 10 thousand, 1 million and 100 million entries

Research date: 2026-10-06. English only. Scope: data, search, browse, SEO and operations at the scale of Amazon and Alibaba. Nothing in this note was built, deployed or priced for purchase. No code was edited.

## How to read the flags

| Flag | Meaning |
|---|---|
| `R-gh` | Read today from the GitHub API through the GitHub tool (licence, stars, last push, issue count). This is primary metadata. |
| `R-web` | Read in a WebSearch result summary on 2026-10-06. **No primary web page was opened in this session**, so every `R-web` figure is also UNVERIFIED by the house rule. Re-check before relying on it. |
| `S` | Secondary source (a blog or aggregator) seen in a search result. |
| `R-repo` | Read in this repository (file named). |
| `I` | Inference or arithmetic from stated inputs. Not measured. |
| `H` | Hypothesis. A bet to test. |
| `UNVERIFIED-M` | From my memory only. I saw no source for it this session. Treat as a question, not a fact. |

Assumed rates are the ones in `research_notes/Backend research/03_hosting_and_costs.md` (called "the hosting note" below): 7.5 KB per entry planning figure, 1.7 KB measured lower bound, restore speed 70.6 MB/s, 23 queries per list page.

Read before writing: `docs/TECHNICAL_PLAN.md` (sections 3, 4.3, 4.4, 8.6, 9.3, 10, 18), `docs/DEPLOYMENT.md`, the hosting note, `docs/REQUIREMENTS_DEPTH_AND_SCALE.md` (D-01 to D-14), and the code named in section 2.

---

## 1. Bottom line

1. **The database design is not the first thing that breaks. Four pieces of application code are.** All four can be fixed while the data is still small (section 2): the roll-up recount loads every entry of a cell into Python; the audit lock is held to the end of each transaction; the sitemap is recomputed on every request; and the stored-list table cannot hold a deep tree.
2. **A list is a saved filter, not a stored object.** One search document per entry with ancestor paths for place and for list type turns every list at every depth (Hotels-Global down to one district) into a filtered query. Store a list row or roll-up cell only where it is big enough to be worth it. This answers requirement D-06 and the "150 billion rows" conflict.
3. **Stay on one PostgreSQL primary with a standby until the biggest table is larger than about half the server's RAM** (about 10 million entries on the hosting note's sizes). Partition then, by country group. Do not adopt Citus, Kafka or ClickHouse before their triggers in section 5.
4. **Search: Postgres trigram and scoped queries to about 1 million entries (as planned). Pick the engine by a bake-off at the S3 gate. Default candidate: OpenSearch** (Apache-2.0, sharded, mature facets and geo). Typesense and Meilisearch are simpler but hold the whole index on one node's RAM or disk (section 3.2). The hosting note's plan to self-host Meilisearch at 100 million documents needs a re-check: Meilisearch sharding is an Enterprise (BUSL) feature `R-web`.
5. **Events: use a transactional outbox table and a Postgres-backed worker first.** Event volume at 100 million entries is small (a few per second on average). Kafka is justified by replay, fan-out and several clusters feeding one global read model, not by throughput (section 3.5).
6. **SEO is a publishing-control problem, not a sitemap-size problem.** At 100 million entries the sitemap files fit easily (about 120 to 280 files). The risk is publishing millions of near-identical programmatic pages. The plan's indexing rules are sound; the field that caps weekly publishing (`publish_cap_per_week`) exists but nothing enforces it.
7. **Near-duplicate parent and child lists are the hidden SEO cost of the Hotels logic.** In a data-poor market, Sialkot, Punjab and Pakistan can hold the same 300 manufacturers. Index the list at its natural scale; index other levels only when they differ enough (section 3.8).
8. **Learn from open source, but take patterns, not code,** from most commerce platforms. Real reuse candidates: Splink (entity resolution), pgBackRest and Patroni (backup and failover), Superset (internal dashboards), OpenSearch or Typesense (search), PeerDB or Debezium (change capture), Overture tools (data). Section 4 gives licence and risk for each.
9. **Two data-licence conflicts need a founder decision:** Overture's divisions theme is ODbL (OpenStreetMap-derived) `R-web`, but the repository rule says share-alike sources are left out; and Elasticsearch, Typesense, Nominatim, Citus and ParadeDB carry GPL or AGPL terms (section 4.3).
10. **Cost is dominated by AI filling, not by servers** (hosting note section 7). Scale work should follow the order in section 5, each step gated by a metric.

---

## 2. What the repository does today (read from the code)

Facts already in the plan and the hosting note are not repeated. The findings below come from reading the code in this session. None was measured; the sizes are arithmetic.

| ID | Finding | Where | Why it matters at scale | Grade |
|---|---|---|---|---|
| F1 | `recount_cell` loads **every entry in a cell into Python**, then runs one `contact_set.exists()` query per published entry. `refresh_for_entry` calls it for every ancestor place and every ancestor concept of the changed entry. A change to one entry in Pakistan recounts the whole country cell. | `backend/analytics/rollups.py` lines 33 to 110 | Cost per write grows with cell size. A cell of 1 million entries means 1 million rows and up to 1 million extra queries for one edit. Breaks long before 1 million entries per cell; `recount_all` is worse. | I (code read) |
| F2 | The audit lock `pg_advisory_xact_lock(727001)` is a **transaction-level lock: it is held until the whole transaction ends,** not for the 3 ms the hosting note assumed. In `bulk.publish`, each row runs `create_entry` (which calls `audit`) and then `settle_duplicate` (a trigram search) inside one `transaction.atomic()`. The lock is held through the duplicate search and the commit. | `core/models.py` `audit()`; `intake/bulk.py` lines 172 to 188 | Throughput is 1 divided by hold time. At 20 ms: 50 audited writes a second, 100 million creates take 23 days; at 50 ms: 58 days (section 3.7). Any bulk run also queues every user edit behind it. | I (code read; hold time not measured) |
| F3 | Sitemaps are built **on every request**. `indexable_list_cells` loads all roll-up cells of a country into memory and runs one `ListTypeSettings` query per cell. `sitemap_shard` repeats the full scan for each of the shard files. Only list pages are listed; entry pages are not. | `catalog/views.py` lines 636 to 690 | N+1 queries over cells, repeated per shard. Fine for thousands of cells; fails at hundreds of thousands. A crawler fetching 280 shards would trigger 280 full scans. | I (code read) |
| F4 | `PlaceList` stores one row per (place, list type), 144 bytes a row with indexes (hosting note 2.3). 235 types times 1.5 million places is 50.8 GB. D-02 and D-06 expect thousands to 100,000 types. | `taxonomy/models.py` line 143 | 100,000 types times 1.5 million places is 150 billion rows, 21.6 TB. Cannot be stored (arithmetic in section 3.1). | I |
| F5 | `Concept` is an **adjacency list** (`parent` foreign key). `descendant_concept_ids` walks it with one query per level, per cell. No stored path or closure table. | `taxonomy/models.py`, `analytics/rollups.py` | A deep manufacturing tree (D-01, D-02) makes every roll-up and every "all surgical goods" query a multi-query walk. | I |
| F6 | `Entry` has `secondary_concepts` (many to many), but roll-ups and the list index `entry_list_query` use `primary_concept` only. | `entries/models.py` lines 46 and 96 to 100; `rollups.py` | D-04 (one entry on many lists) is stored but not rolled up or listed. | I |
| F7 | `CountrySwitch.publish_cap_per_week` exists as a field and a migration. **Nothing reads it.** Plan 8.6 says a bug must not publish a million pages overnight. | `core/models.py` line 147 | The control that protects against scaled-content penalties is not enforced. | I (grep: no other reference) |
| F8 | No partitioning, no outbox, no PgBouncer, no `CONN_MAX_AGE`, no cache backend setting in the repo. `entries.Entry.uid` is globally unique. | grep over `backend/`, `deploy/`, `scripts/` | A partitioned table needs the partition key inside every unique key `UNVERIFIED-M` (PostgreSQL documentation, not opened). A global unique `uid` must be redesigned before partitioning. | I; M for the PostgreSQL rule |
| F9 | `QuotaCounter` increments are three queries inside a transaction on one row per (address, key, day). | `access/quotas.py` | Fine to about S2. A hot address row bloats and serialises. Move to Redis or the edge at S3. | I |
| F10 | Good and already in place: filters and sorts are `noindex`; `/_f/` and `/search/` are disallowed; indexable pages need at least 10 verified entries (`INDEX_THRESHOLD`) and a switch that allows indexing; shared pages carry `s-maxage=300, stale-while-revalidate=600`; the search interface is a three-method contract with two backends and contract tests; `generate_lists` refuses very large runs without `--confirm-large`; runbooks `scraper-surge.md` and `indexing-drop.md` exist. | `catalog/seo.py`, `catalog/views.py`, `catalog/search_backend.py`, `core/management/commands/generate_lists.py`, `docs/runbooks/` | These are the right foundations. | R-repo |

---

## 3. Challenge catalogue

Each challenge has an ID, what large sites do, the options, and what AllLists should do with the trigger. Triggers are collected in section 5.

### 3.1 Storage, partitioning and sharding

**What large sites do.** Wikidata (about 122 million content pages `R-web`) ran a single Blazegraph store until it was "nearing its capacity", then split the graph into two services in May 2025 and is looking at replacing the engine `R-web`. The lesson: a single store has a hard ceiling, and the split key (there: scholarly articles versus the rest) was chosen late and under pressure. AllLists already has the natural key: country. Amazon lists about 600 million products `S` (marketplacepulse); Alibaba's Havenask serves Taobao and Tmall with "hundreds of billions" of records `R-web` (vendor documentation). Those are separate systems for catalogue, search and orders; none is "one Postgres".

| ID | Option | Fits AllLists when | Risk or cost | Verdict |
|---|---|---|---|---|
| BS-01 | **Single primary plus streaming standby, vertical growth** | Up to about 10 million entries (75 GB planning size, hosting note) | One failure domain; restore time grows (3.3 hours for 837 GB by dump) | Default through S2 |
| BS-02 | **Declarative partitioning by country group** inside one cluster | Largest table exceeds about half of RAM. PostgreSQL documentation gives "exceeds the memory of the server" as the rule of thumb `UNVERIFIED-M` | Planner cost rises with partitions left unpruned; "a few thousand partitions" is fine when queries prune `R-web` (PostgreSQL mailing list summaries). Keys must include the partition column (F8) | Design the key now; turn on at S3, not S2. This changes plan 3.5, which says "country partitions turned on" at S2 |
| BS-03 | **Per-country-group clusters** (plan S4) | A country passes about 50 million entries, or data-residency rules need isolation | Cross-country reads (global lists) need a global read model (below) | Default at S4 |
| BS-04 | **Citus** (distributed PostgreSQL extension) | Transparent horizontal scale across many nodes; one logical database | AGPL-3.0 `R-gh`; 12.8 thousand stars, active (last push 2026-10-06); Citus 14 supports PostgreSQL 18 `R-web`. You must pick the distribution column and co-locate child tables; the coordinator needs its own high availability `UNVERIFIED-M` | Evaluate only at S4 in a bake-off against BS-03 on 100 million synthetic rows |
| BS-05 | Separate ledger database | Plan S4 | Cross-database money reporting | Already in plan |

**How global lists work with per-country clusters (H).** The clusters are the system of record for writes. Two global read models are fed by events: the search index (all countries, one alias) and the roll-up store. Hotels-Global and Hotels-Asia are served from those, never by scatter-gather across clusters. This also keeps requirement D-10 (no global write lock) intact.

**Stored lists versus virtual lists (D-06), with arithmetic `I`.**

| Design | Rows at 100 million entries, 100,000 types, 1.5 million places | Size | Verdict |
|---|---|---|---|
| Stored `PlaceList` for every (place, type) | 150,000,000,000 | 21.6 TB at 144 B a row | Impossible |
| Stored for 235 types only (today's seed) | 352,500,000 | 50.8 GB | Possible, but dead weight: most are empty |
| Roll-up cell for every non-empty (place, type) | 0.5 to 1.5 billion (H: 100 million entries times 3 memberships times about 1 to 3 distinct lowest-level cells, plus shared upper levels) | 150 to 450 GB at 302 B a row | Too heavy to rewrite every five minutes |
| **Roll-up cell only where the cell holds at least 25 memberships** | At most 300 million memberships times 6 place levels divided by 25 = 72 million cells; double it for ancestor types = 144 million | 43 GB at 302 B a row | **Recommended.** Below 25 members, answer live: one page of 25 rows is one index range scan (1.7 ms measured, plan 4.3) |

Rule: a cell is stored when it has at least 25 members or when it is an indexable page (at least 10 verified entries, plan 8.6) or when a person created it. Everything else is a filtered query. Run `generate_lists` only with `--country` and `--levels` (already guarded).

**Deep tree storage (F5).** Add a stored path to `Concept` (materialised path, or PostgreSQL `ltree`) so "all descendants" is one prefix query and the search document can carry the ancestor list. A closure table is the alternative; a path is simpler. Needed before the manufacturing tree (D-02) is loaded.

### 3.2 Search: engines, faceting, ranking, autocomplete, geo

**One document per entry, many paths (H).** Each search document carries: folded names and aliases, `concept_ancestors` (every ancestor of the primary and secondary concepts), `place_ancestors` (every ancestor path), `country`, check level, freshness, completeness, coordinates, and facet fields (process, material, certification, capacity band, minimum order band, export markets, per D-03). A list page is then `concept_ancestors = X AND place_ancestors = Y`, sorted by rank. Facet counts are aggregations over the same filter. Entries are stored once; membership is many to many (D-04).

**Engine comparison.** Counts are from GitHub today. "Faceting and geo" are listed in each project's GitHub topics `R-gh` or are well known; deeper claims are marked.

| ID | Engine | Licence | Maturity | Facets and geo | Scale model | Fit and risk for AllLists |
|---|---|---|---|---|---|---|
| BS-10 | **PostgreSQL trigram + scoped queries** (built) | PostgreSQL licence | Core | Trigram typo match; no BM25; no native facet counts | One node (plus replicas) | Right to about 1 million entries when always scoped. Unscoped fuzzy name search 150 to 520 ms at 1 million (plan 4.3) |
| BS-11 | **PostgreSQL full text (tsvector)** | PostgreSQL licence | Core | `ts_rank` has no inverse document frequency and no efficient top-k, and slows on large tables `R-web` | One node | Do not use for ranking at scale |
| BS-12 | **ParadeDB `pg_search`** (BM25 inside Postgres, Tantivy) | AGPL-3.0 `R-gh`; 9.4 thousand stars; active | Young; vendor claims 20 times faster ranking than tsvector at 1 million rows `R-web` | BM25 index can push filters and facet aggregations into one scan `R-web` | One node, plus its own distributed mode `R-web` | Attractive middle step at 1 to 10 million, if the host lets us install extensions (managed services often do not `UNVERIFIED-M`). AGPL needs counsel. Test it before choosing an engine |
| BS-13 | **OpenSearch** | Apache-2.0 `R-gh`; 13.8 thousand stars; 3,213 open issues; active | Mature; fork of Elasticsearch | Facets as aggregations; geo points and shapes `UNVERIFIED-M` | Sharded and replicated. Guidance: 10 to 50 GB per shard and under 200 million documents per shard; avoid thousands of tiny shards `R-web` (Elastic documentation, same engine family) | **Default candidate at 10 to 100 million.** 100 million documents at 300 B is 30 GB raw (hosting note), 90 to 150 GB indexed `[EST]`: 3 to 10 primary shards |
| BS-14 | **Elasticsearch** | `R-gh` reports "other" because the repository is multi-licensed. Elastic added AGPL-3.0 beside SSPL and Elastic License 2.0 in 2024 `R-web`. 78 thousand stars | Most mature | Same as OpenSearch | Same | Technically equal. Licence is more complex. Use OpenSearch unless a feature is missing |
| BS-15 | **Typesense** | GPL-3.0 `R-gh`; 26.6 thousand stars; 913 open issues; active | Mature for site search | Faceting, geosearch, search-as-you-type, synonyms (GitHub topics `R-gh`) | **Whole index in RAM**: plan 2 to 3 times the searchable data size `R-web`. 100 million documents with 30 GB of searchable fields is about 60 to 90 GB of RAM per node `I`. High-availability clusters replicate, not shard `UNVERIFIED-M` | Excellent developer experience, typo tolerance and speed up to what fits on one node. Hosting note's "3 nodes of 64 GB" is too small if that estimate holds. GPL-3.0 applies to the server; calling it over HTTP from our code does not make our code GPL (our judgement; counsel to confirm) |
| BS-16 | **Meilisearch** | Community Edition MIT; Enterprise Edition BUSL `R-web`. GitHub reports "other" `R-gh`. 59.5 thousand stars | Mature for site search | Facets, geosearch, typo tolerance (topics `R-gh`) | **Sharding is Enterprise only** `R-web`. Community is one node. Cloud overage USD 0.20 per 1,000 documents makes 100 million documents about USD 20,000 a month (hosting note) | Good to about 10 million on one node. **Conflict with the hosting note, which names self-hosted Meilisearch for 100 million documents.** Re-check before S3 |
| BS-17 | **Vespa** | Apache-2.0 `R-gh`; 7.1 thousand stars; active | Mature; Vinted moved to it from Elasticsearch for scale and cost (Vespa's own blog) `S` | Ranking expressions, tensors, structured and vector search | Distributed by design | Strongest for custom ranking at very large scale; heavier to run. Revisit only if ranking becomes the bottleneck |
| BS-18 | **Solr** | Apache-2.0 `R-gh`; 1.7 thousand stars (mirror) | Old, stable | Facets and geo | Sharded (SolrCloud) | No advantage over OpenSearch for a team starting now |
| BS-19 | django-haystack | `R-gh` reports "other" (believed BSD-3 `UNVERIFIED-M`) | 3.7 thousand stars; 582 open issues | n/a | n/a | Not needed: our three-method contract (`catalog/search_backend.py`) is smaller and already tested |

**How others went.** Yelp built its own Lucene-based engine, nrtSearch, after Elasticsearch showed bottlenecks in replication, resource use and operations at its scale `R-web`. Alibaba built Havenask for its own scale `R-web`. These are hundreds-of-millions-of-queries stories. The lesson for us is small: **keep the engine behind the adapter** so it can be replaced, and measure before choosing.

**Decision method.** At the S3 gate (search p95 over 500 ms or zero-result rate over 15%, plan 3.5 and 10.1) run a bake-off of OpenSearch, Typesense and Meilisearch Community, and `pg_search` if installable. Load 10 million synthetic documents with the real field shapes. Use the existing contract tests (`catalog/tests/test_search_backends.py`) plus: p95 for a list filter with 5 facets; index build time; RAM and disk; cost per month; behaviour during a reindex. Pick the cheapest that passes at 3 times the expected 100 million size projection.

**Ranking and relevance (H).** Start with fixed weights, not learning. Features: text match on folded name and aliases; concept synonym expansion (built in `ConceptLabel`); place scope or distance; check level (Surveyor-verified and Owner-verified above AI-checked above Not verified yet); verification freshness; completeness; later popularity from enquiries. **Paid placement is a separate labelled slot and never a ranking feature** (rule 4, plan R14). Build the judgement set first: the plan's 200-query native-speaker test set (plan 10.1) scored with NDCG@10, mean reciprocal rank and zero-result rate. Learning-to-rank only after there are judgements and enquiry data; do not buy it early.

**Autocomplete.**

| Level | Source | Notes |
|---|---|---|
| Header: list types and places | A small in-memory or Postgres trigram table (a few hundred thousand labels) | Already in the plan; cheap to about S3 |
| Inside one list: entry names | Scope filter plus prefix or n-gram match | In the engine at S3; in Postgres with the scoped trigram index before that |
| Edge cache | CDN key = scope plus prefix, 60 second lifetime | Popular prefixes repeat; the long tail does not matter |
| Privacy | Do not store full queries with identifiers | Plan 17.3 |

**Geo search.** The place tree does most "near me" work: list pages are by place, so a radius query is a feature on top, not the base. Use PostGIS (plan S1) for distance sort and `ST_DWithin` through S2. In the engine use its geo-point field at S3. For geocoding addresses to coordinates see section 4 (Photon, Pelias, Nominatim) and the licence warning there. Maps are not shown on pages (plan R01), so tile and map-rendering cost is out of scope.

**Embeddings and semantic search.** Not early. 100 million names at 768 dimensions of 32-bit floats is 307 GB of index before overhead (`I`: 100 million times 768 times 4 bytes); 8-bit quantisation brings it to about 77 GB. Synonym recall already comes from `ConceptLabel`. Revisit when the zero-result rate stays above 15% after synonym work.

### 3.3 Browse and facets

- **Facets are filters, not list types** (D-03). A facet value is a field in the search document. It never creates a page by itself.
- **Counts.** Big cells: from the roll-up store ("as of" time shown). Small cells: aggregated live from the engine or the index.
- **Facet count caps.** Show the top 20 values per facet with counts; allow "more" through the engine. Do not pre-compute the cross product of facets.
- **Page weight.** List page budget is 11 KB (plan 18.5). Facets render as plain links or a form, not as a script-driven widget.
- **URL shape.** Filters live in query parameters, sorted and canonical, and are `noindex` (built, `seo.py`). Parameters blocked from crawling by `robots.txt` (section 3.8).

### 3.4 Caching and CDN

**Today.** Shared pages: `s-maxage=300, stale-while-revalidate=600`. Crawler files: `max-age=3600`. Private fragments: never cached. All `R-repo`.

**The long-tail problem `I`.** The hosting note assumes a 70 to 90% CDN hit ratio at 100 million entries. A page that is fetched once a month never hits a 5-minute cache. Crawlers touch exactly those pages. Suppose 300 million of the 400 million monthly requests are bots (hosting note ratio) and 60% of bot requests hit an uncached page; with 10% of the 100 million human requests missing:

- origin requests = 0.6 x 300 million + 0.1 x 100 million = 190 million a month = 73 a second average, about 370 a second at 5 times peak;
- queries at 23 per page = about 8,400 a second at peak, against the hosting note's 5,300.

Three remedies, in order:

1. **Tiered lifetimes by page class.** Entry pages: 1 day plus 7 days stale. List pages: 1 hour plus 1 day stale. Counts carry an "as of" time, so staleness is already disclosed.
2. **A per-page snapshot.** Store the rendered rows for page 1 of each stored cell (and each indexable entry) in one table or key-value store, so a cold hit is one read, not 23 queries. Refresh on events from the outbox.
3. **Static snapshots of indexable pages in object storage** (S4 option). 14 million indexable pages at 11 KB is about 154 GB, about USD 4 a month at S3 prices in the hosting note; rendering 5% a day is about 8 pages a second `I`. This removes crawler load from the origin completely.

**Versioned cache keys.** Plan 3.4 puts the page's `updated_at` stamp in the cache key. A CDN cannot see that stamp before fetching, so in practice the key is the URL plus a short lifetime plus revalidation by `ETag`. Say so in the plan. Tag-based purge is a higher-tier CDN feature `UNVERIFIED-M`; do not design around it.

**Do not add Redis for page caching early.** Redis is justified at S3 for rate-limit counters and sessions (section 3.11), not as a second page cache in front of a CDN.

### 3.5 Event-driven pipelines

**What is needed.** When an entry changes: update roll-up deltas, refresh the search document, upsert the sitemap row, rebuild the page snapshot, and (later) stream to analytics.

**Volume `I`.** Assume 100 million entries built over 18 months by bulk load and agents: 185,000 new entries a day, about 2 a second. Edits and verifications: assume 50% of entries change once a year: 137,000 a day, 1.6 a second. Even 10 times that is 20 a second. **Throughput is not the reason to adopt Kafka.**

| ID | Option | Licence and maturity | Use when | Verdict |
|---|---|---|---|---|
| BS-20 | **Transactional outbox table + worker using `SELECT ... FOR UPDATE SKIP LOCKED`** | Postgres features | From S2. One table written in the same transaction as the change; workers claim rows; consumers are idempotent | **Introduce at 1 million entries** |
| BS-21 | Postgres logical decoding read by **PeerDB** to ClickHouse | PeerDB is now part of ClickHouse `R-web`; replicates through a logical slot with about 10 seconds freshness, no Kafka needed `R-web` | When analytics moves to ClickHouse | Preferred for the analytics path |
| BS-22 | **Debezium** | Apache-2.0 `R-gh`; 13.2 thousand stars; active | Needs Kafka, Kafka Connect and monitoring `R-web` | Use only if Kafka exists for other reasons |
| BS-23 | **Apache Kafka** | Apache-2.0 `R-gh`; 33.9 thousand stars; active | More than 3 independent consumers that need replay; several clusters feeding one global read model; sustained over about 5,000 events a second | Introduce at S4, probably as a managed service |
| BS-24 | Celery or RQ with Redis | Common | Background jobs that are not "events" | The plan defers Celery and Redis; keep the 5-minute scheduler until queue depth or latency says otherwise |

Rules for every consumer: idempotent by event ID; ordered per entry; a dead-letter table with an alert; a replay command. Keep the audit rows and the outbox separate (the outbox is deletable after processing; the audit log is not).

### 3.6 Analytics (ClickHouse)

`analytics.Event` is estimated at 5 million rows a month at 100 million views (hosting note); that is small for Postgres. **ClickHouse earns its place on crawl and access logs**, not on product events: 400 million requests a month at about 250 B is about 100 GB of raw log a month `I`. Questions that need it: which URLs does Googlebot fetch, how much of the crawl hits `noindex` or thin pages, hit ratio by page class, scraper detection by distinct pages per address.

- ClickHouse: Apache-2.0 `R-gh`; 50 thousand stars; very active (last push today); 8,077 open issues.
- Introduce when: Postgres `analytics_event` exceeds about 100 million rows, or crawl-log queries take over a minute, or the CDN's own analytics cannot answer the crawl questions. Until then: CDN logs to object storage, and `/staff/metrics/`.
- dbt for models in the warehouse: introduce only after ClickHouse exists. Before that, plain SQL views. (The GitHub tool did not return `dbt-labs/dbt-core`; its licence and activity are `UNVERIFIED-M`.)
- Apache Superset (section 4) as the dashboard layer for staff.

### 3.7 Write hot spots

| ID | Hot spot | Evidence | Fix | When |
|---|---|---|---|---|
| WH-1 | **Global audit lock and single hash chain** (`audit()`, lock 727001) | F2. Throughput table below | Replace the single chain: see options | P1; decide before S2 bulk loads |
| WH-2 | **Roll-up recount per write** | F1 | Delta counters: the outbox consumer adds or subtracts from the affected cells (batched, grouped by cell, one `UPDATE ... SET total = total + n` per cell per batch). Nightly exact recount as one SQL `GROUP BY`, never a Python loop. Skip cells under the 25-member threshold | P0 before 100,000 entries per country |
| WH-3 | `RollupCell` updates every five minutes | Hosting note 2.3 (heavy churn) | Same fix; set `fillfactor` 70 to 80 so updates stay in-page | S2 |
| WH-4 | `QuotaCounter` row per address per day | F9 | Redis `INCR` with expiry, or edge counters | S3 |
| WH-5 | Sequence and unique-key contention on very hot tables | General | Time-ordered IDs (ULIDs already used for `uid`); batch inserts | Watch only |
| WH-6 | Bulk import in one transaction per row | F2 | Batch commits (hundreds of rows) with the audit written per batch | With WH-1 |

**Audit throughput `I`** (100 million audited creates, lock held for the stated time):

| Hold time | Writes a second | Days for 100 million | Note |
|---|---|---|---|
| 3 ms (hosting note's assumption) | 333 | 3.5 | Best case; lock released immediately |
| 20 ms (create plus duplicate search inside the transaction, guess) | 50 | 23 | Plausible for F2 |
| 50 ms | 20 | 58 | Slow disk or a long duplicate search |

**Options for the chain.**

1. **One chain per country group** (lock key = a number per country group). Keeps the per-chain proof; parallelism equals the number of groups; skewed if one country dominates.
2. **N chains by hash of `object_uid`** (for example 256). Even load; verification walks each chain; a row records its chain number.
3. **No lock on the hot path.** Write audit rows unchained (append-only roles already prevent edits, `deploy/db_roles.sql`). A **sealing job** every minute hashes the new rows (a Merkle root over the batch) and chains the seals. Tamper evidence moves from per-row to per-batch granularity; writes never wait. This is the usual pattern for transparency logs: Merklemap reports 100 billion rows with a Merkle design `R-web`. Contention on a single chain is described in the transparency-log literature as a database bottleneck `R-web`.

Suggested default: option 3, with option 2 as an interim step if the founder wants per-row proof. Decision belongs to the founder (section 9).

### 3.8 Sitemaps, URL scale, crawl budget, canonical and noindex rules, thin pages

**Facts.** One sitemap file holds up to 50,000 URLs and 50 MB uncompressed; a sitemap index holds up to 50,000 files `S` (third-party summaries of the sitemap protocol; Google's page not opened). Google's guide on faceted navigation says: blocking filter URLs in `robots.txt` is the most effective way to cut crawling of them; `rel=canonical` may reduce it over time; both are "less effective in the long term" for `canonical` and `nofollow` `R-web` (Google Search Central summary). Google's crawl-budget document applies to sites above roughly 1 million pages that change weekly, or 10,000 pages that change daily `UNVERIFIED-M`.

**URL arithmetic `I`.**

| Class | Count at 100 million entries | Basis |
|---|---|---|
| Potential list URLs | 100,000 types x 1.5 million places = 150 billion | Why lists are never enumerated |
| Potential facet URLs | Multiply the above by the facet combinations | Unbounded. Never index by default |
| Indexable entry pages | About 5 million | H: 5% verified by a person and rich (plan Q-T3 default) |
| Indexable list pages | At most 5 million verified x 3 memberships x 6 place levels / 10 = 9 million | Upper bound; real number is lower |
| Sitemap files | (5 million + 9 million) / 50,000 = 280 | Well inside 50,000 files |
| Curated facet pages | Cap at 100,000 | A whitelist chosen by demand |

So the sitemap size is not the constraint. The constraint is how many of the 14 million are worth a crawl and unique enough to survive.

**Near-duplicate parent and child lists `I`.** The Hotels logic puts the same entry on Global, Country, Region, City and District. In a young market the child may equal the parent. Rule: a list is indexable if it has at least 10 verified entries **and** it is at the list type's natural scale (`Concept.natural_scale` already exists), **or** it holds at most 80% of its parent's verified entries (so it adds something). Otherwise `noindex,follow` with a canonical to the parent. The 80% figure is a starting hypothesis; calibrate it with the indexing watch.

**What to change from the current rules.**

| ID | Change | Why |
|---|---|---|
| SEO-1 | **Materialise the sitemap**: a table `sitemap_url(country_group, loc, lastmod, shard)` maintained by the outbox consumer; a nightly job writes the shard files to object storage; the CDN serves them. | F3 |
| SEO-2 | Add **entry pages** to the sitemap when indexable | F3 |
| SEO-3 | Robots disallow **parameter patterns** (`Disallow: /*?*sort=`, filter keys, `page=` beyond a depth), while thin **path** pages stay crawlable so their `noindex` can be read | Google's guidance above; plan 8.6 only blocks `/_f/` and `/search/` |
| SEO-4 | **Do not link to empty or thin lists** from other pages. Show the text without a link, or `rel=nofollow` | `noindex,follow` still costs a fetch per link; the "every list exists" rule (plan 5.2) is a crawl trap at 150 billion potential pages |
| SEO-5 | **Enforce `publish_cap_per_week`** (F7) and alert when a country passes it | A bug must not publish a million pages overnight |
| SEO-6 | **Indexing watch**: submitted versus indexed per sitemap shard, from Search Console, and the plan's alert under 20% indexed at day 90 | Plan 8.6, 18.3. Not found in code |
| SEO-7 | **Return 404 or 410 for lists with no entries and no creator**, not 200 | Fewer soft-404 signals. Conflicts with plan C11 ("reachable but empty"); offer "Start this list" from search and from a place page instead |
| SEO-8 | Keep structured data limited to visible content (plan 8.6) | Unchanged |

**Risk: scaled content abuse.** Google's spam policy treats many pages made mainly to rank as abuse, whether written by people or AI; manual actions cluster on templated pages with thin per-page value `R-web` (third-party summaries; an August 2026 spam update is reported `S`). AllLists list pages are programmatic by nature. The defence is the existing rule (enough verified entries, real data, no filler text) plus SEO-3 to SEO-5. Do not generate descriptive paragraphs with AI to "thicken" pages.

### 3.9 Image-free text pages

This is an advantage. A list page is 11 KB and an entry page 7 KB (plan 18.5), so 3.4 TB a month at 100 million views with 4 times bot traffic (hosting note) and no image pipeline, no resizing service, no image CDN. Keep the build gate on page weight. The cost to watch is requests, not bytes.

### 3.10 Multilingual later

The English-only rule stands. Design now so that adding languages is a data task:

- Labels already live in rows: `ConceptLabel`, `PlaceName` (per language). Keep all new display text in label tables, never in code.
- **URL multiplication `I`:** L languages multiply indexable URLs by L. 14 million becomes 140 million at L = 10; sitemap files 2,800.
- **hreflang weight `I`:** the current code puts alternates in each page. At L = 10 the link tags add about 1.2 KB (10 tags of about 120 B), 11% of the 11 KB list-page budget. Move to hreflang in the sitemap files once L is above 3.
- **Search:** one analyser set per language (tokenisation, folding, transliteration; the plan's Urdu, Arabic and Roman-Urdu folding is in 7.3). A bake-off must include a non-English test set before the engine is chosen.
- **Index only languages with content.** A translated page with an untranslated body is thin.

### 3.11 Rate limiting and anti-scraping at scale

**Layers, cheapest first.**

| Layer | Control | Status |
|---|---|---|
| CDN | Edge rate rules by path and address. Cloudflare Free allows 1 rule, Pro 10, Business 15 `R-web` (a third-party summary of plan limits) | Plan: Free first |
| CDN | Bot scoring. The hosting note says Business has bot management; Cloudflare's machine-learning Bot Management is an Enterprise product `UNVERIFIED-M`. **Possible conflict with the hosting note; verify.** | Check before budgeting USD 250 a month |
| Origin | Quotas by address and account (`QuotaCounter`, built) | Postgres to S2; Redis at S3 (WH-4) |
| Data | Contacts never shown (rule 2); names-only previews; pagination cap per tier; canary entries; terms of use (plan 9.3) | Built or planned |
| Search bots | Reverse DNS check for quota exemption (plan 8.6) | Planned |
| Response to a surge | `docs/runbooks/scraper-surge.md` | Exists |

**Arithmetic `I`.** To copy 100 million entries at 25 rows a page needs at least 4 million list-page fetches. At the plan's alarm of 500 pages a day per address, that is 8,000 address-days, trivial with a rented proxy pool (cost not researched). **Per-address limits alone do not stop a determined copier.** What protects the business is that the valuable fields are not on public pages (contacts are relayed, never shown), plus canaries, plus a legal route. Accept some copying of names and areas; spend effort on detection (distinct list pages per account per day, new-account bursts, canary hits) and on speed of response, not on a perfect block.

**Open data option (judgement).** Open Food Facts publishes full dumps in several formats `R-web`, which lowers the incentive to scrape. That fits a free public database; it conflicts with a model that sells larger lists. Not recommended for AllLists, listed for completeness.

### 3.12 Observability and cost control

- **Golden signals per page class** (entry, list, search, fragment, sitemap): request rate, error rate, p50/p95/p99, cache hit ratio, origin share, bot share.
- **Database:** `pg_stat_statements`, `log_min_duration_statement = 500` (already in DEPLOYMENT.md 4), cache hit ratio, replication lag, vacuum lag on `analytics_rollupcell`, `core_auditlog`, `entries_entry`; the hosting note section 10 holds the thresholds.
- **New signals** for this note: wait time on lock 727001; outbox age and dead-letter count; search p95 and zero-result rate; sitemap build age; crawl share on `noindex` pages; indexed-over-submitted per shard.
- **Tools:** Sentry, Grafana (Cloud free tier first, plan 18.3), Prometheus and Loki when about 20 hosts, `postgres_exporter` per cluster.
- **Cost control.** Unit costs on one dashboard: infrastructure per entry per month (hosting note: USD 0.0003 on AWS, 0.00004 on Hetzner at 100 million); CDN cost per million pages served; search cost per million queries; AI cost per verified record (cap USD 0.30, rule 6). AI filling stays the largest line, so its caps stay the main control. Budget alerts at 50% and 80% (plan 18.3). Each new component carries an owner, a monthly budget and a trigger to remove it.
- **Protect the origin from crawlers.** Search engines accept a temporary 503 or 429 with `Retry-After` as a request to slow down `UNVERIFIED-M`. Add this as a switch in the scraper-surge runbook, never as a default.

---

## 4. What to learn from open source

Counts are from the GitHub API on 2026-10-06 (`R-gh`). "Last push" is the date of the latest push to the default branch. Maturity is my judgement (`I`) from stars, activity and open issues. Licence text was not read; the GitHub field is shown, and where GitHub shows "other" (NOASSERTION) the real licence is `UNVERIFIED` and must be read from the LICENSE file before any reuse.

### 4.1 Commerce and marketplace platforms (patterns, not code)

| Repository | Licence | Stars, last push | Maturity | Take this | AllLists problem it solves | Do not take |
|---|---|---|---|---|---|---|
| **saleor/saleor** | BSD-3-Clause | 23.4 thousand; 2026-10-06 | High; Python and Django, active | Typed attribute model per product type (our add-on registry is the same idea); translation tables; webhook and event payload design; background-task patterns; how a Django catalogue handles search vectors with a "dirty" flag refreshed in batches `UNVERIFIED-M` | Attribute and facet design (D-03); Django scale practice; event payloads for the outbox | Checkout, orders, payments, GraphQL API (public API is deferred, plan R31) |
| **medusajs/medusa** | GitHub shows "other"; believed MIT `UNVERIFIED` | 36.6 thousand; 2026-10-06 | High; TypeScript | Module isolation and workflow steps with compensation (saga) for multi-step money flows | Ideas for the ledger and payout workflows later | Any code (different stack) |
| **spree/spree** | BSD-3-Clause | 15.7 thousand; 2026-10-06 | High; Ruby; has multi-vendor and multi-tenant topics | Taxonomy and classification: product linked to many nodes of a tree (our D-04); option types and variants | Many-to-many membership and tree modelling | Storefront |
| **solidusio/solidus** | BSD-3-Clause | 5.3 thousand; 2026-10-01 | Medium; Ruby; Spree fork | Same as Spree; nothing extra | None beyond Spree | Everything else |
| **vendurehq/vendure** | GitHub shows "other" `UNVERIFIED` (licence history unclear to me) | 8.5 thousand; 2026-10-06 | High; TypeScript | Collections that fill themselves from filter rules over facet values `UNVERIFIED-M`. This is the same idea as "a list is a saved filter" | The list-as-filter model (3.2) | Any code |
| **sharetribe/sharetribe** (Sharetribe Go) | GitHub shows "other"; the repository calls itself "source-available" and **no longer maintained** | 2.4 thousand; 2026-05-11 | Low; frozen | Marketplace flow ideas only (listing, enquiry, transaction states) | Reference for enquiry relay flow | **Do not copy code**: a source-available licence can forbid use for a competing marketplace `UNVERIFIED-M`. Not maintained |
| **sharetribe/web-template** | "other" | 67 stars; 2026-10-06 | Small; tied to a hosted product | None | None | Tied to the vendor's paid platform `UNVERIFIED-M` |

### 4.2 Data, geography and knowledge tools

| Repository | Licence | Stars, last push | Maturity | Take this | AllLists problem it solves | Risk |
|---|---|---|---|---|---|---|
| **openfoodfacts/openfoodfacts-server** | AGPL-3.0 | 1.2 thousand; 2026-10-06; 1,854 open issues; Perl | High as a product, heavy codebase | Governance of a crowd-filled catalogue; multilingual taxonomies with synonyms and parents (`taxonomies/`) `UNVERIFIED-M`; the Robotoff machine-learning suggestion service and the taxonomy editor named in its description `R-gh`; open bulk dumps in several formats `R-web` | Contributor-led data quality and taxonomy governance (D-01, D-05) | AGPL on the server code: do not copy it into a closed product. Perl stack |
| **wikimedia/wikidata-query-rdf** (GitHub mirror) | GitHub shows no licence | 158; 2026-08-08 | Mirror of a Gerrit project | The scaling story, not the code: single store hit a ceiling, graph split May 2025, replacement search under way `R-web` | Evidence for choosing the split key early (BS-03) | Not a tool we run |
| **Wikidata dumps and tools** (WikibaseIntegrator, pywikibot) | Not read | The GitHub tool returned no result for the Wikidata toolkit; I could not check them | n/a | Use **dumps** to build crosswalks to Wikidata IDs (D-05) offline; licence of the data (believed CC0) is `UNVERIFIED-M` | Stable identifiers and crosswalks | Do not query the live SPARQL service from production |
| **osm-search/Nominatim** | GPL-3.0 | 4.5 thousand; 2026-09-30; Python | High | A full address geocoder and reverse geocoder run as a separate service | Turning addresses into coordinates and places | Data is OpenStreetMap (ODbL, share-alike). The repository's rule leaves share-alike sources out. A planet import is hardware heavy `UNVERIFIED-M`. Storing results from ODbL data may raise share-alike questions: counsel |
| **komoot/photon** | Apache-2.0 | 3.1 thousand; 2026-09-24; Java | High | Search-as-you-type geocoding on OpenSearch or Elasticsearch | Autocomplete of places and addresses | Same ODbL data question |
| **pelias/pelias** | MIT | 3.6 thousand; 2026-07-24 (umbrella repository; sub-repositories not checked) | High, modular | Importer, Elasticsearch, admin-hierarchy lookup layers; can load sources other than OSM (WhosOnFirst, GeoNames, OpenAddresses) `UNVERIFIED-M` | Place hierarchy and geocoding without OSM | Operating cost of several services |
| **OvertureMaps/overturemaps-py** | MIT | 275; 2026-10-06 | Small, official CLI | Download Overture themes by area as GeoParquet | Loading places and the place tree in S1 to S2 | **Data licences differ by theme:** Places are CDLA-Permissive-2.0 with more than 64 million points; Divisions, Buildings, Base and Transportation are ODbL `R-web` (Overture documentation summary). **The place tree (divisions) built from "GeoNames + Overture" would carry ODbL.** Conflicts with the share-alike rule. Decide (section 9) |
| **OvertureMaps/overture-tiles** | MIT | 173; 2026-09-22 | Small | Not needed (no maps on pages) | None | n/a |

### 4.3 Search engines (see section 3.2 for the comparison)

| Repository | Licence (`R-gh`) | Stars, last push | What to take |
|---|---|---|---|
| **opensearch-project/OpenSearch** | Apache-2.0 | 13.8 thousand; 2026-10-06 | Default engine candidate |
| **elastic/elasticsearch** | "other" (multi-licence; AGPL option added 2024 `R-web`) | 78.2 thousand; 2026-10-06 | Documentation on shard sizing applies to OpenSearch too |
| **typesense/typesense** | GPL-3.0 | 26.6 thousand; 2026-10-06 | Fast typo-tolerant search up to one node's RAM |
| **meilisearch/meilisearch** | "other" (Community MIT, Enterprise BUSL `R-web`) | 59.5 thousand; 2026-10-06 | Single-node site search to about 10 million |
| **vespa-engine/vespa** | Apache-2.0 | 7.1 thousand; 2026-10-06 | Ranking-heavy later option |
| **apache/solr** | Apache-2.0 | 1.7 thousand; 2026-10-06 | None; no advantage today |
| **paradedb/paradedb** | AGPL-3.0 | 9.4 thousand; 2026-10-06 | BM25 inside Postgres; test at 1 to 10 million; AGPL needs counsel |

**Licence note (our judgement, not legal advice).** GPL and AGPL obligations attach to distributing the software, and for AGPL to offering a **modified** version to users over a network. Running unmodified Typesense, ParadeDB, Citus or Nominatim as a service we call over a network does not, by that reading, make our Django code subject to them. Any patch we make to them would. Counsel should confirm before S3. Prefer Apache-2.0 and MIT components when quality is equal.

### 4.4 Entity resolution, analytics, backup and availability

| Repository | Licence | Stars, last push | Maturity | Take this | AllLists problem it solves | Risk |
|---|---|---|---|---|---|---|
| **moj-analytical-services/splink** | MIT | 2.5 thousand; 2026-10-06 | High, active; DuckDB and Spark back ends; Spark for 100 million and more `R-web` | Probabilistic scoring with blocking rules and an explainable match weight | Batch duplicate detection (D-09); already in plan S2 | Needs good blocking keys: country, folded name token, geo cell, hashed phone (the contact hash exists) |
| **dedupeio/dedupe** | MIT | 4.5 thousand; **2025-07-29** (14 months quiet) | Medium; slowing | Active-learning ideas for training pairs | Labelling duplicates efficiently | Maintenance risk |
| **J535D165/recordlinkage** | BSD-3-Clause | 1.1 thousand; **2024-02-21** (31 months quiet) | Low | Ideas for comparison functions only | None | Stale: do not adopt |
| **apache/superset** | Apache-2.0 | 75.1 thousand; 2026-10-06 | Very high | Staff dashboards for data quality, revenue and crawl on the read replica or ClickHouse (the `alllists_readonly` role already hides contacts) | Internal analytics (replaces hand-built staff pages as questions grow) | Separate Python service to run; keep it internal; never expose entry contacts |
| **dbt-labs/dbt-core** | Not returned by the GitHub tool; Apache-2.0 `UNVERIFIED-M` | not checked | Not checked | SQL models and tests in the warehouse | Analytics modelling after ClickHouse exists | Not needed earlier |
| **ClickHouse/ClickHouse** | Apache-2.0 | 50.3 thousand; 2026-10-06 | Very high | Crawl and access-log analytics | Section 3.6 | Operating a second database; trigger first |
| **citusdata/citus** | AGPL-3.0 | 12.8 thousand; 2026-10-06 | High; PostgreSQL 18 support in Citus 14 `R-web` | Distributed tables with co-located children, reference tables for places and concepts | BS-04 at S4 only | AGPL; operating a coordinator and workers |
| **pgbackrest/pgbackrest** | GitHub shows "other"; believed MIT `UNVERIFIED` | 4.4 thousand; 2026-10-06 | High | Physical backups, incremental, parallel, zstd, restore to a point in time | The S4 recovery goal (logical dumps take 3.3 hours at 837 GB, hosting note) | None known |
| **patroni/patroni** | MIT | 8.8 thousand; 2026-10-06 | High | Automatic failover with etcd, Consul or Kubernetes | Standby promotion in minutes without a managed service | Needs a consensus store; skip if a managed database is used |
| **cloudnative-pg/cloudnative-pg** | Apache-2.0 | 9.4 thousand; 2026-10-06 | High | PostgreSQL operator for Kubernetes | Only if the team runs Kubernetes | The plan defers Kubernetes (3.6) |
| **wal-g/wal-g** | GitHub shows "other" `UNVERIFIED` | 4.3 thousand; 2026-10-06 | Medium to high | Alternative to pgBackRest | None extra | Pick one backup tool, not two |
| **pgbouncer/pgbouncer** | GitHub shows "other"; believed ISC `UNVERIFIED-M` | 4.4 thousand; 2026-09-23 | High | Connection pooling in front of Postgres | Many web workers exhausting `max_connections` (hosting note 10 says add it first) | Transaction pooling breaks session features and advisory locks held across statements: check with `audit()` |
| **debezium/debezium** | Apache-2.0 | 13.2 thousand; 2026-10-06 | High | Change capture to Kafka | BS-22 | Needs Kafka |
| **apache/kafka** | Apache-2.0 | 33.9 thousand; 2026-10-06 | Very high | Replayable event log | BS-23 at S4 | Heavy to run; buy managed |

Not found or not checked: Wikidata Toolkit and `dbt-labs/dbt-core` (the tool returned nothing), PeerDB (seen only in web results), QLever, Search-a-licious (Open Food Facts), the Typesense and Meilisearch showcase repositories.

---

## 5. Architecture by stage

Stage names follow plan 3.5. The three sizes asked for are S0 to S1 (10 thousand), S2 (1 million) and S4 (100 million); the 10 million gate (S3) is shown because the changes between S2 and S4 happen there. Sizes, costs and restore times for the 10 thousand, 1 million and 100 million columns come from the hosting note; other numbers are `I`.

### 5.1 Component by stage

| Component | 10 thousand (S0 to S1) | 1 million (S2) | 10 million (S3 gate) | 100 million (S4) |
|---|---|---|---|---|
| Database size (planning) | 0.16 GB | 18.7 GB | about 100 to 150 GB `I` (75 GB of entries at 7.5 KB, plus roll-ups, places, events; not in the hosting note) | about 837 GB total |
| Database topology | One server, nightly dump | Primary plus standby, WAL archive, 4 to 16 vCPU, 16 to 32 GB | Primary plus standby plus read replica; PostgreSQL 17 or 18 upgrade `I` | Country-group clusters (4 of about 0.21 TB), separate ledger database |
| Partitioning | None. **Design keys now** (country inside primary and unique keys; decide `uid` uniqueness) | None. Partition only audit, events and change log by month if they pass 50 GB | Partition `Entry` and children by country group | Per cluster; evaluate Citus (BS-04) |
| Connection pooling | None | PgBouncer when connections near `max_connections` | Yes | Per cluster |
| Backup and recovery | Nightly dump to another provider; drill quarterly | pgBackRest, WAL, 15-minute loss, 4-hour restore | Physical backups; drill under 1 hour for a replica promote | Physical backups plus standby; restore of one cluster about 0.21 TB |
| Lists | Scoped `generate_lists` (0.02 GB) or none | **Hybrid rule**: stored cell at 25 members or an indexable page; live below | Same; closure or path on `Concept` loaded | Same: bounded at about 144 million cells, 43 GB |
| Roll-ups | Existing recount is acceptable | **Delta counters through the outbox** (WH-2); nightly SQL recount | Cells under threshold dropped | Per cluster, merged into a global store |
| Search | Postgres trigram, always scoped | Same; test `pg_search` | **Engine bake-off, then adopt** (default OpenSearch) | Engine cluster, one index per country group plus a global alias; 90 to 150 GB indexed |
| Autocomplete | Header table in Postgres | Same plus CDN prefix cache | Engine | Engine |
| Geo | PostGIS | PostGIS | Engine geo field | Engine geo field |
| Cache and CDN | Cloudflare Free; 300 s plus 600 s stale | Tiered lifetimes by page class | Page snapshot table | Static snapshots in object storage for indexable pages (optional) |
| Sitemaps | Computed on request (acceptable under 10,000 URLs) | **Materialised table and files** (SEO-1, SEO-2) | Same | About 280 files |
| Events | Five-minute scheduler | **Outbox plus worker** | Outbox; PeerDB to ClickHouse if analytics moves | Kafka, managed, if the triggers hold |
| Analytics | `/staff/metrics/`, Postgres events | Superset on read replica if asked | ClickHouse for crawl and access logs | ClickHouse cluster, dbt |
| Entity resolution | Trigram plus geo at ingest (built) | Splink batch (plan S2) | Splink plus engine candidate search | Splink on Spark or DuckDB per country group |
| Bot defence | CDN free rules, `QuotaCounter`, canaries | Pro rules, scraper-surge runbook | Redis counters | Business or Enterprise rules after the Bot Management check |
| Multilingual | English only; label tables | Same | Decide on first language | hreflang in sitemaps |
| Observability | Sentry, uptime, Grafana free | Plus `pg_stat_statements`, outbox and lock metrics | Prometheus per cluster | About 20 hosts: Loki or Grafana Pro, pager |
| Infrastructure cost a month (hosting note, USD) | 25 to 45 | 240 to 390 (dedicated) to 655 to 1,193 (AWS managed) | Plan S3: 1,775 to 6,110 | 5,200 to 7,000 (dedicated) to 22,000 to 38,000 (AWS managed) |
| Restore time | Under 1 minute | About 4.4 minutes by dump | Physical restore, target under 1 hour | 3.3 hours by dump (not acceptable); use standby |

### 5.2 Triggers: the metric that introduces each component

| ID | Component | Metric and threshold | Source of threshold |
|---|---|---|---|
| TR-1 | Fix roll-up recount (WH-2) | Any cell with over 10,000 entries, or recount of one entry taking over 200 ms | `I`; before 100,000 entries per country |
| TR-2 | Enforce publish cap, materialise sitemap | Before the first bulk publish over 10,000 pages | `I` |
| TR-3 | Outbox and worker | Roll-up age over 15 minutes, or a second consumer (search, sitemap) is added | Plan 18.3, hosting note 10 |
| TR-4 | Replace single audit chain (WH-1) | Lock wait over 50 ms, or planned bulk load over 1 million audited writes | Hosting note 10; `I` |
| TR-5 | PgBouncer | Connections above 70% of `max_connections` | `I`; hosting note 10 |
| TR-6 | Physical backups (pgBackRest) | Data over 150 GB, or restore time over half the recovery goal | Hosting note 10 |
| TR-7 | Read replica | Sustained primary CPU over 60%, or list queries over 100 ms | Hosting note 10 |
| TR-8 | Search engine | Search p95 over 500 ms, or zero-result rate over 15% | Plan 3.5, 10.1 |
| TR-9 | Partition `Entry` | Largest table over half of server RAM, or index build or vacuum windows too long | PostgreSQL rule of thumb `UNVERIFIED-M`; plan S3 |
| TR-10 | Country-group clusters | A country above 50 million entries, or total above 100 million | Plan 3.5 |
| TR-11 | Redis for counters and sessions | `QuotaCounter` writes above 50 a second, or lock waits on hot rows | `I` |
| TR-12 | ClickHouse | Postgres events above 100 million rows, or crawl-log questions unanswerable by CDN analytics | `I` |
| TR-13 | Kafka | More than 3 independent consumers needing replay, or over 5,000 events a second, or several clusters feeding one read model | `I` |
| TR-14 | Static page snapshots | Origin share of crawler traffic keeps database queries above 5,000 a second at peak | Section 3.4 arithmetic |
| TR-15 | Citus bake-off | Cross-country transactional queries appear, or cluster management cost exceeds the Citus cost | `I` |
| TR-16 | Cloudflare Business or Enterprise | CDN hit ratio under 60%, or any address fetching over 500 distinct list pages a day despite rules | Plan 18.3, hosting note 10 |

---

## 6. What not to do early

| # | Do not | Why | Revisit when |
|---|---|---|---|
| 1 | Build Kubernetes, microservices or a service mesh | Plan 3.6; one modular monolith until measured | S4, and only if the team can run it |
| 2 | Adopt Kafka for volume | Event rate is a few a second at 100 million entries (section 3.5) | TR-13 |
| 3 | Adopt Citus or shard at 1 million entries | 7.5 GB of entries fits in one server's memory | TR-10, TR-15 |
| 4 | Turn on partitioning at S2 | No benefit under half of RAM; adds planner and key constraints | TR-9; but fix keys now |
| 5 | Buy a search engine before the trigger | Trigram scoped search is under 150 ms (plan) | TR-8; keep the adapter and the contract tests current |
| 6 | Store a list row for every (place, type) | 150 billion rows, 21.6 TB | Never; use the hybrid rule |
| 7 | Run `generate_lists` unscoped, or with `--confirm-large` | 6.6 GB at 10 thousand entries (hosting note) | Never at S0 to S2 |
| 8 | Recount cells by loading entries in Python | F1 | Replace now |
| 9 | Show `count(*)` over large sets on a page | Plan 4.3: 203 ms for one country | Never |
| 10 | Index every facet page, every empty list, every child list | Crawl waste and scaled-content risk | Only whitelisted, distinct pages |
| 11 | Let `noindex,follow` thin pages be linked everywhere | Each link costs a crawl | SEO-4 |
| 12 | Publish pages in a bulk run with no weekly cap | F7 | SEO-5 before the first bulk run |
| 13 | Learning-to-rank, click models or embeddings | No judgement set; 307 GB of vectors at 100 million | After the judged query set and enquiry data exist |
| 14 | Use Meilisearch Cloud at scale | About USD 20,000 a month at 100 million documents (hosting note) | Never at that size |
| 15 | Plan on Meilisearch Community alone for 100 million | No sharding without Enterprise `R-web` | After a bake-off |
| 16 | Assume Typesense fits 100 million on 64 GB nodes | 60 to 90 GB RAM per node by the 2 to 3 times rule | After a bake-off |
| 17 | Add a second page cache (Redis) in front of the CDN | Complexity without a measured gain | Only for counters and sessions (TR-11) |
| 18 | Build ClickHouse before crawl logs exist | Postgres handles product events to 100 million rows | TR-12 |
| 19 | Build your own geocoder, search engine or record-linkage library | Mature open-source options exist (section 4) | Never |
| 20 | Use OpenStreetMap-derived data (Nominatim, Overture divisions) without a decision | Conflicts with the share-alike rule | Founder decision, section 9 |
| 21 | Put a single global lock or hash chain on every write | WH-1 | Replace before S2 bulk loads |
| 22 | Use thousands of tiny partitions or search shards | Planner and cluster overhead `R-web` | Keep partitions to country groups and months |
| 23 | Translate or add languages | English-only rule | When the founder lifts it; design label tables now |
| 24 | Run a big AI fill before caps and the audited-accuracy gate | Rule 6; fill cost dominates (hosting note 7) | Existing caps |
| 25 | Depend on an AGPL database extension on a managed service without counsel | Licence and hosting limits | Counsel review |

---

## 7. Requirements for the repository

Priority P0 (before real data at volume), P1 (before 1 million entries), P2 (later). Status checked against the repository on 2026-10-06.

| ID | Requirement | Pri | Status | Evidence |
|---|---|---|---|---|
| SC-01 | Roll-ups update by deltas and recount in SQL, never by loading entries | P0 | Not built | F1 |
| SC-02 | Enforce `publish_cap_per_week` and alert on breach | P0 | Not built | F7 |
| SC-03 | Materialised sitemap table and files, served from storage | P0 | Partly (sharded at 50,000 by country; built per request; lists only) | F3 |
| SC-04 | Entry pages in the sitemap when indexable | P1 | Not built | F3 |
| SC-05 | Hybrid list storage rule (25 members or indexable) and tests | P0 | Partly (`generate_lists` guard exists; no threshold rule; stored table for all types) | F4; D-06 |
| SC-06 | Audit without a global lock (sealed batches or many chains) | P1 | Not built | F2 |
| SC-07 | Stored path on `Concept` for deep trees | P1 | Not built | F5 |
| SC-08 | Roll-ups and lists include secondary memberships | P1 | Partly (field exists, roll-ups use primary only) | F6; D-04 |
| SC-09 | Outbox table, worker, dead-letter and replay | P1 | Not built | F8 |
| SC-10 | Search engine adapter passing the contract tests | P1 | Partly (interface and two backends; no engine adapter) | `search_backend.py` |
| SC-11 | Robots rules for filter and sort parameters | P1 | Partly (`noindex` in page; `/search/` and `/_f/` blocked; parameters not blocked) | `views.py` robots |
| SC-12 | Near-duplicate parent and child rule using `natural_scale` | P1 | Not built | `seo.py` |
| SC-13 | PgBouncer settings and a check that `audit()` works through it | P1 | Not built | F8 |
| SC-14 | Partition-ready keys (country in unique keys; `uid` plan) | P1 | Not built | F8 |
| SC-15 | Tiered cache lifetimes by page class | P1 | Partly (one shared lifetime) | `views.py` line 38 |
| SC-16 | Page snapshot store for cold reads | P2 | Not built | Section 3.4 |
| SC-17 | Quota counters on Redis or the edge | P2 | Not built (Postgres works to S2) | F9 |
| SC-18 | Crawl and access-log analytics | P1 | Not built | Section 3.6 |
| SC-19 | Indexing watch (submitted versus indexed) and the 20% day-90 alert | P1 | Not built (runbook `indexing-drop.md` exists) | Plan 8.6 |
| SC-20 | Load test with a long-tail bot mix, not only a hot-page mix | P1 | Partly (`scripts/loadtest.py` replays a realistic mix; long-tail share not checked) | `scripts/loadtest.py` |
| SC-21 | Bake-off harness for 10 million synthetic documents | P1 | Not built | Section 3.2 |

---

## 8. Gaps, conflicts and unverified claims

**Conflicts with existing documents.**

1. **Hosting note versus Meilisearch limits.** It names self-hosted Meilisearch for 100 million documents; sharding is Enterprise (BUSL) `R-web`.
2. **Hosting note versus Typesense memory.** Three nodes of 64 GB RAM vs 60 to 90 GB per node needed `I`, and clusters replicate `UNVERIFIED-M`.
3. **Hosting note versus Cloudflare.** It places bot management at the Business plan (USD 250); the ML product may be Enterprise `UNVERIFIED-M`.
4. **Plan 3.5 versus this note.** Plan turns on country partitions at S2; this note says S3 and fixes keys now.
5. **Plan 5.2 ("every list exists, reachable but empty") versus SEO-4 and SEO-7.** Needs a decision.
6. **Plan 3.4 (data stamp in the cache key) versus how a CDN works.** The key cannot include a stamp the CDN does not yet know.
7. **Repository rule (no share-alike sources) versus Overture divisions (ODbL) and OSM-based geocoders.**
8. **Hosting note's 3 ms audit hold time versus the transaction-level lock** (F2).

**Not verified in this session.** Every `R-web` figure (no primary page opened). All `UNVERIFIED-M` items: the PostgreSQL "exceeds memory" partitioning rule and the partition-key rule for unique indexes; Google's crawl-budget thresholds; Typesense replicating rather than sharding; Cloudflare Bot Management tier; the real licences of Medusa, Vendure, pgBackRest, WAL-G, PgBouncer, django-haystack and dbt-core; Saleor's search vector pattern; Vendure collections; Nominatim hardware; geocoding results and ODbL; Wikidata data licence; 503 and 429 handling by crawlers; Search-a-licious. Our licence reading of GPL and AGPL is not legal advice.

**Not measured.** Every size, rate and time marked `I` or `H`. The biggest unknowns: lock hold time in real bulk runs; true number of non-empty cells with a deep tree; share of bot traffic that hits cold pages; share of entries that become indexable; search engine RAM and disk at 100 million documents. Section 7 SC-21 and SC-20 are the tests that turn them into measurements.

**Not covered.** Payments at scale, legal review, and the people and tooling for data operations (see the other Scale research notes). I did not read `01_manufacturing_depth_taxonomy.md` or `03_capabilities_and_skills_matrix.md` because they did not exist when I started.

---

## 9. Open decisions for the founder, with suggested defaults

| # | Decision | Suggested default |
|---|---|---|
| 1 | Replace the single audit hash chain (WH-1) | Sealed batches (option 3); per-country-group chains as the fallback. Fix before any bulk load over 1 million rows |
| 2 | Hybrid list storage rule for D-06 | Store a cell at 25 members or when indexable or created by a person; live below. Never enumerate all (place, type) pairs |
| 3 | Overture divisions (ODbL) and OSM-based geocoders | Use GeoNames for the place tree and Overture Places (CDLA-Permissive) only; no OSM-derived data until counsel decides |
| 4 | When to partition | S3 (largest table over half of RAM), not S2; make keys partition-ready now |
| 5 | Search engine | OpenSearch by default, chosen by bake-off at the S3 trigger; keep adapter and contract tests green |
| 6 | Empty and thin list URLs | Return 404 or 410 for empty lists with no creator; do not link to thin lists; offer "Start this list" from search |
| 7 | Near-duplicate parent and child pages | Index at the natural scale; others only if they hold 80% or less of the parent's verified entries |
| 8 | Publishing speed | Enforce a weekly cap per country (start at 5,000 pages a week) and raise it as indexing watch passes |
| 9 | GPL and AGPL components (Typesense, ParadeDB, Citus, Nominatim) | Allowed as unmodified services behind our API after counsel confirms |
| 10 | Kafka | Not before TR-13; outbox first |
| 11 | Bot-management spend | Re-check the Cloudflare tier before budgeting USD 250 a month |

Suggested entry for `docs/DECISIONS.md` (build log), not yet added because the task allowed one file only:

> 2026-10-06, scale architecture research (`research_notes/Scale research/02_big_site_architecture.md`): four code risks logged (roll-up recount loads whole cells; audit lock held to transaction end; sitemap built per request; stored-list table cannot hold a deep tree); proposed defaults: hybrid list rule at 25 members, outbox before Kafka, partition at S3, OpenSearch by bake-off, sealed-batch audit, enforce `publish_cap_per_week`; two licence questions for counsel (ODbL data, GPL and AGPL services). Nothing built.

---

## 10. Sources

Read in this repository: `docs/TECHNICAL_PLAN.md` (3, 4, 5, 8, 9, 10, 18, 19), `docs/DEPLOYMENT.md`, `docs/REQUIREMENTS_DEPTH_AND_SCALE.md`, `research_notes/Backend research/03_hosting_and_costs.md`, `backend/core/models.py`, `backend/intake/bulk.py`, `backend/intake/importer.py`, `backend/entries/services.py`, `backend/entries/models.py`, `backend/taxonomy/models.py`, `backend/analytics/rollups.py`, `backend/analytics/models.py`, `backend/access/quotas.py`, `backend/access/models.py`, `backend/catalog/views.py`, `backend/catalog/seo.py`, `backend/catalog/search_backend.py`, `backend/config/settings/base.py`, `backend/core/management/commands/generate_lists.py`, `docs/runbooks/` (file list).

GitHub API through the GitHub tool, 2026-10-06 (licence, stars, last push): saleor/saleor, medusajs/medusa, spree/spree, solidusio/solidus, vendurehq/vendure, sharetribe/sharetribe, sharetribe/web-template, openfoodfacts/openfoodfacts-server, wikimedia/wikidata-query-rdf, osm-search/Nominatim, komoot/photon, pelias/pelias, OvertureMaps/overturemaps-py, OvertureMaps/overture-tiles, typesense/typesense, meilisearch/meilisearch, opensearch-project/OpenSearch, elastic/elasticsearch, apache/solr, vespa-engine/vespa, paradedb/paradedb, django-haystack/django-haystack, moj-analytical-services/splink, J535D165/recordlinkage, dedupeio/dedupe, apache/superset, pgbackrest/pgbackrest, patroni/patroni, citusdata/citus, ClickHouse/ClickHouse, debezium/debezium, apache/kafka, cloudnative-pg/cloudnative-pg, pgbouncer/pgbouncer, wal-g/wal-g. Not returned: dbt-labs/dbt-core, Wikidata Toolkit.

WebSearch summaries, 2026-10-06 (no page opened):

- Google Search Central, faceted navigation: developers.google.com/crawling/docs/faceted-navigation
- Sitemap limits: library.linkbot.com, seo-day.de, gautamkhorana.com (third party)
- PostgreSQL partitioning overhead: postgresql.org mailing list threads, hackorum.dev, oneuptime.com
- Elastic shard sizing: elastic.co/docs/deploy-manage/production-guidance/optimize-performance/size-shards
- Typesense system requirements: typesense.org/docs/guide/system-requirements.html; valebyte.com
- Meilisearch sharding and licence: meilisearch.com/docs (enterprise edition, sharding), meilisearch.com/blog/enterprise-license
- Wikidata graph split and Blazegraph: wikidata.org WDQS backend update pages, meta.wikimedia.org WikiCite graph split, ceur-ws.org Vol-4108 paper 3
- Elasticsearch licence: itbrief.co.uk and bigdatawire.com reports on the AGPL option
- Scaled content abuse: gsqi.com, seojuice.com, techwyse.com, alexcloudstar.com (third party)
- Yelp nrtSearch: engineeringblog.yelp.com, arpitbhayani.me; Vinted and Vespa: blog.vespa.ai
- Havenask and Alibaba OpenSearch: help.aliyun.com, sourcepulse.org; Amazon catalogue: marketplacepulse.com, sellerengine.com
- Audit chains and Merkle logs: blog.transparency.dev (Merklemap), dev.to, appmaster.io
- Overture data: docs.overturemaps.org/guides/places, overturemaps.org/about/faq, tech.marksblogg.com
- Open Food Facts exports: openfoodfacts.org/data pages
- Citus 14 and PostgreSQL 18: citusdata.com/blog/2026/02/17/distribute-postgresql-18-with-citus-14
- PeerDB and Debezium: blog.peerdb.io, clickhouse.com/blog, risingwave.com, streams.dbconvert.com
- Cloudflare rate limiting: developers.cloudflare.com/waf/rate-limiting-rules, eastondev.com
- PostgreSQL full text and BM25: paradedb.com/blog, tigerdata.com, hackernoon.com, ramnode.com
- Splink scale: pypi.org/project/splink, realworlddatascience.net
