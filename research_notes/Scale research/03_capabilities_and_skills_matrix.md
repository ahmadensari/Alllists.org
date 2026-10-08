# Capabilities and skills matrix, challenge register, Claude-skills plan and learning loop

Research date: 2026-10-06. Scope: English only. Design and planning document; no code was changed. Requirement D-12 (`docs/REQUIREMENTS_DEPTH_AND_SCALE.md`) names this file as the one that is reviewed every month.

**Matrix version:** 1 (2026-10-06). **Next review due:** 2026-11-06. **Owner of the review:** Claude prepares, founder signs off the open decisions in section 6.

Evidence tags (house style, `.claude/skills/research-note`):

- **[R]** read in this repository this session.
- **[S]** from a web search summary. I did not open the page. Every [S] item is UNVERIFIED until a person or a later session opens the source.
- **[K]** from my background knowledge (tools, books, licences, repositories). Not checked this session. UNVERIFIED. Check the licence file of any repository before use (plan section 2.2 rule).
- **[I]** inference or arithmetic (inputs stated).
- **[H]** proposal or hypothesis: a design choice or threshold that has not been tested.

---

## 0. Summary

1. **What this is.** AllLists wants to handle, search and keep tidy hundreds of millions of entries and to be run like a very large marketplace. That needs sixteen capability areas (section 2), not one. Today the repository is strong on rules, money, consent, audit and agent safety, and thin on the scale side: no search engine, no real entity-resolution engine, no zero-downtime migration practice, no SEO measurement, no geospatial stack, no analytics warehouse. Those are the gaps the matrix ranks.
2. **Where the work is.** Of the 16 areas, 6 are needed at working level already at 10k entries (data engineering, taxonomy, entity resolution, legal and privacy, security, agent evaluation) and the rest ramp up by 1M. At 100M entries nearly every area needs a hired specialist or a vendor; the founder and Claude cannot cover it alone (section 2.18).
3. **Challenge register.** 62 specific challenges at Amazon and Alibaba scale (section 3), each with a solution and a tool or source, ranked by when it first bites (S0 to S4, using the plan's stage table). 36 are marked N (needed now) because they decide schema or process before the first million rows; 15 of those change schema most (listed under the register).
4. **Biggest scale risks that are already visible in this repository** [R]: one global audit hash chain and advisory lock (`core/models.py`, lock 727001: 3.5 days of pure lock time for 100M creates at 3 ms a hold, `03_hosting_and_costs.md` section 10); `PlaceList` without a country key and 150 billion possible rows once manufacturing depth is added (D-06); logical dumps that take 3.3 hours to restore at 0.84 TB against a 1 hour goal; roll-up cells updated every five minutes (bloat); unscoped search at 150 to 520 ms at 1M; no duplicate engine beyond `pg_trgm` and guessed thresholds (0.90 and 0.60).
5. **Skills plan.** Section 4 lists 17 new project skills in three waves. Wave 1 (5 skills) should exist before the founder asks to go beyond the prototype: `taxonomy-depth`, `entity-resolution`, `scale-migrations`, `large-scale-data`, `open-source-check`. Existing `depth-and-scale` stays as the thin umbrella and points at the narrow skills.
6. **Learning loop.** Section 5 fixes file locations: a weekly research log, the existing decision log, a challenge-register file that this matrix feeds, evals with a sealed gold set (not in git), post-incident notes under `docs/incidents/`, and a monthly matrix review. A skill that is never updated after an incident is treated as a defect.
7. **What I could and could not verify.** Twelve web searches were run (standard mode, summaries only, no pages opened) and are cited in section 7. GitHub API access to third-party repositories was refused in this session ("GitHub access to this repository is not enabled for this session"); one repository search returned only unrelated results. So **no repository star count, licence or last-commit date in this file has been checked**. Treat every repository named here as a [K] candidate to verify with `add_repo` plus a read of its LICENSE file before adoption.

---

## 1. Starting position (what the repository already has) [R]

| Fact | Source |
|---|---|
| Modular monolith: Django 5.2, PostgreSQL 16, Gunicorn, WhiteNoise, Cloudflare in front; server-rendered pages with HTMX fragments; Procrastinate planned for jobs | `docs/TECHNICAL_PLAN.md` 2.1, 3.2 |
| Stage table: S0 proof (5k entries), S1 pilot (50k), S2 country (1M), S3 multi-country (10M), S4 global (100M) with named triggers | plan 3.5 |
| Planning size at 100M entries: 750 GB entries and children, 837 GB total; peak about 5,300 queries a second; storage 4 country-group clusters of about 0.21 TB | `Backend research/03_hosting_and_costs.md` sections 2.4 and 3 |
| 235 list types seeded; stored lists as rows (E27) but depth rules (D-06) change this to hybrid | `DECISIONS.md`, `REQUIREMENTS_DEPTH_AND_SCALE.md` |
| Duplicate pipeline v1 (block, score, decide) on `pg_trgm`; thresholds auto-merge 0.90, review 0.60 are first guesses | `DECISIONS.md` build log, `backend/intake/dedupe.py` |
| Bulk upload pipeline: stage, 385-row audit sample, 90% pass, resumable publish, rollback | `backend/intake/bulk.py` |
| Agent track with caps defaulting to zero, kill switch, verbatim-evidence rule, verifier canaries; AI auditor designed but not built (18 work packages T1.04 to T1.21) | `Backend research/04_agent_training_and_ai_auditor.md` |
| Append-only ledger, double-entry balance trigger, two-person payout rule, daily reconciliation, idempotent webhooks | `DECISIONS.md` fifth and seventh coding steps |
| Search behind an interface with two implementations; Postgres only today | `backend/catalog/search_backend.py`, build log eighth step |
| Twelve runbooks, restore drill script, load-test script, mutation check script | `docs/runbooks/`, `scripts/` |
| Not in `requirements.txt`: Splink, python-phonenumbers, pgbouncer, any migration linter, any analytics warehouse, any search engine client | `backend/requirements.txt` |
| Existing project skills: `alllists-rules`, `ai-auditor`, `list-filing`, `research-note`, `steward`, `depth-and-scale` | `.claude/skills/` |

### 1.1 What the giants teach (all [S], UNVERIFIED)

| Lesson | Source |
|---|---|
| Amazon-style catalogues match duplicate listings on GTIN, brand, model and manufacturer part number, plus specifications and image checks; identifiers let the platform reconcile many sellers to one record | search summary of seller-help pages; see section 7, S3 |
| Amazon's AutoKnow reports a product knowledge graph run for over 11,000 product types, with taxonomy construction, attribute discovery, extraction, anomaly detection and synonym discovery done mostly automatically | KDD 2020 paper, section 7, S5 |
| Alibaba's AliCoCo (SIGMOD 2020 industry track) models shopper needs as concept nodes on top of the product taxonomy, built semi-automatically | section 7, S4 |
| Amazon released the Shopping Queries Dataset (about 130,000 queries and 2.6 million labelled query and product pairs, labels Exact, Substitute, Complement, Irrelevant) | section 7, S6 |
| The EU Digital Services Act article 30 requires marketplaces to collect and check trader identity, registration and payment details, from 17 February 2024 | section 7, S7 |
| EU VAT e-commerce rules (from 1 July 2021) make marketplaces deemed suppliers for some sales and require 10 years of records | section 7, S10 |
| Google's spam policies (March 2024 onward) target scaled content abuse: many pages made mainly to rank, whether written by a model, freelancers or a template | section 7, S8 |
| One report puts automated traffic above 57% of HTML requests in mid-2026 and says Cloudflare verifies AI crawlers and offers pay-per-crawl. Single, weak source | section 7, S11 |

---

## 2. Capability areas

### 2.0 How to read the matrix

**Level scale** (used for the 10k, 1M and 100M columns): L0 not needed; L1 aware, can follow a guide; L2 working, does it with documentation under review; L3 strong, designs and debugs alone; L4 expert, has run it at this scale before.

**Who:** F = founder; C = Claude (agent sessions, subagents, scheduled routines); H = hired role (employee or contractor); V = vendor or service.

**Status in repo** (what exists now, checked against the repository [R]): Built, Partly, Not built.

### 2.1 Overview table (priority and who)

| # | Area | 10k | 1M | 100M | Status in repo | F | C | H | V | First hire trigger |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Data engineering | L2 | L3 | L4 | Partly (loaders, bulk staging; no warehouse, no pipeline scheduler, no data tests) | decides sources | builds | data engineer | cloud storage | S2: 10M-row batches |
| 2 | Taxonomy and ontology | L2 | L3 | L4 | Partly (235 types, concept tables, synonyms; no crosswalks, no depth tooling) | approves tree | drafts and maintains | taxonomist (contract) | none | S2: leaves above 5,000 types |
| 3 | Entity resolution | L2 | L3 | L4 | Partly (pg_trgm v1) | sets merge policy | builds, calibrates | data scientist | none | S2: Splink at scale |
| 4 | Search relevance | L1 | L2 | L4 | Partly (Postgres, interface only) | accepts ranking rules | builds, evaluates | search engineer | managed engine optional | S3: p95 over 500 ms |
| 5 | Geospatial | L1 | L2 | L3 | Not built (PostGIS not tested, text-only scope) | decides map scope | builds | GIS engineer (contract) | geocoder | S1 to S2 |
| 6 | Database internals and scaling | L2 | L3 | L4 | Partly (indexes, triggers, partition plan, backup script) | none | designs, tests | Postgres DBA | managed Postgres | S2: standby, partitions |
| 7 | SRE and cost control | L2 | L3 | L4 | Partly (health page, alerts, runbooks, drills) | accepts budgets | writes runbooks | SRE | monitoring, CDN | S2: on-call |
| 8 | SEO at scale | L2 | L3 | L4 | Partly (rules in `seo.py`, sharded sitemaps) | none | builds, watches | SEO lead | Search Console | S2: 1M indexable pages |
| 9 | Trust and safety | L2 | L3 | L4 | Partly (reports, takedown, canaries, source gate) | policy | builds | T&S lead | KYB provider | S1: first paid listing |
| 10 | Payments and billing | L2 | L3 | L4 | Partly (ledger, orders, webhooks, invoices; no real provider) | decides provider | builds, tests | payments engineer, finance | gateway, tax engine | before first real payment |
| 11 | Legal and privacy | L2 | L3 | L4 | Partly (consent, erasure, suppression, gates) | decides risk | prepares questions | privacy counsel, DPO | counsel | before first messaging or individuals list |
| 12 | Data annotation operations | L1 | L3 | L4 | Partly (surveyor tasks, canaries, audit samples) | owns volunteer model | builds tools | annotation ops lead | label tool, panels | S1: volunteers at volume |
| 13 | Agent engineering and evaluation | L2 | L3 | L4 | Partly (agents safe; no gold set, no prompt versions, no auditor) | caps spend | builds | ML engineer | model provider | S1: first real hosted run |
| 14 | Product analytics | L1 | L2 | L3 | Partly (events catalogue, roll-ups) | picks metrics | builds | analyst | analytics tool | S2 |
| 15 | Security | L2 | L3 | L4 | Partly (headers, MFA, encryption, scans) | rotates secrets | reviews code | security engineer | pentest firm | before launch; S2 |
| 16 | Logic, correctness and systems design | L3 | L3 | L4 | Partly (property tests, state machines, mutation check) | none | applies | staff engineer | none | S3 |

### 2.2 Area 1: Data engineering

| Item | Detail |
|---|---|
| Covers | Ingest, clean, validate, load and re-load tens of millions of rows; batch pipelines; checkpoints and resume; data tests; lineage; storage formats; scheduling; backfills. |
| Why AllLists needs it | Open baselines (Overture, Foursquare, GeoNames) are tens to hundreds of millions of rows [R: `REUSE_AND_TOOLS.md`]; the bulk path is capped at 1M rows per batch without counsel. Every record keeps source, licence, date, consent (D17). |
| 10k | L2: CSV and loader scripts, `COPY`, simple checks. |
| 1M | L3: staged loads with row-level reject files, idempotent re-runs, data tests on every load, one scheduler. |
| 100M | L4: partitioned bulk loads, Parquet staging, columnar analytics beside Postgres, lineage, cost per row tracked, backfills measured in days not weeks. |
| Tools and repositories to learn from [K] | PostgreSQL `COPY` and unlogged staging tables; DuckDB (reads Parquet, fast profiling); Polars; Apache Parquet; `overturemaps-py` (official Overture client); dbt-core (SQL transformations and tests); Dagster or Apache Airflow (scheduling, only if Procrastinate is outgrown); Great Expectations, Soda Core or pandera (data tests); Debezium (change capture); OpenLineage (lineage); Apache Iceberg or Delta Lake (only at 100M with an analytics lake); pg_partman. |
| Learning resources [K] | Kleppmann, "Designing Data-Intensive Applications"; Kimball, "The Data Warehouse Toolkit"; PostgreSQL manual chapters on `COPY`, partitioning, and bulk loading ("Populating a Database"); dbt Learn; Overture documentation and release notes (release notes are published per release, [S] S9). |
| Who | F: chooses which sources and countries. C: writes loaders, tests, profiling. H: data engineer at S2. V: object storage. |
| Test of competence [H] | (a) Load 1M synthetic rows twice: second run adds 0 rows. (b) Kill the load at 50%: restart resumes within one chunk and the final count equals the source. (c) Inject 1% bad rows: all 1% land in the reject file with a reason, none in `entry`. (d) Load throughput stated in rows per second, with the arithmetic for 100M. |

### 2.3 Area 2: Taxonomy and ontology

| Item | Detail |
|---|---|
| Covers | Trees of list types (sector to variant), synonyms, stable IDs, crosswalks to external codes, facets versus types, multi-parent membership, versioning, redirects, concept relations. |
| Why AllLists needs it | The product is the taxonomy: 235 types today, tens of thousands at manufacturing depth (D-01, D-02), with capabilities as facets (D-03) and many-to-many membership (D-04). A wrong tree multiplies into rows, URLs and search cost. |
| 10k | L2: a clean tree of about 235 types, synonyms, reserved slugs. |
| 1M | L3: crosswalk tables to Overture, Foursquare, ISIC, ISCO, UNSPSC, HS; a facet registry; change process with redirects; coverage dashboard. |
| 100M | L4: tens of thousands of leaves maintained semi-automatically; concept layer for needs and use cases (the AliCoCo idea, [S] S4); anomaly detection on attributes (the AutoKnow idea, [S] S5); taxonomy versions with diffs. |
| Tools and repositories [K] | Overture categories and taxonomy (CC BY 4.0 file per `REUSE_AND_TOOLS.md`); Foursquare categories (Apache-2.0); GS1 Global Product Classification; UNSPSC; Harmonized System (customs); ISIC and ISCO-08; schema.org; Wikidata; W3C SKOS (mapping relations exactMatch, closeMatch, broadMatch, narrowMatch); Protégé; ETIM and ECLASS (technical product classification; licences UNVERIFIED, ECLASS is believed to be paid). Papers: AliCoCo (arXiv 2003.13230), AutoKnow (arXiv 2006.13473). |
| Learning resources [K] | Rosenfeld, Morville, Arango "Information Architecture"; Hedden "The Accidental Taxonomist"; W3C "SKOS Primer"; Noy and McGuinness "Ontology Development 101"; the two papers above. |
| Who | F: approves top levels and which sectors go deepest. C: drafts subtrees, proposes crosswalks, runs checks. H: taxonomist on contract at S2. V: none. |
| Test of competence [H] | (a) Take 200 random Overture categories: at least 95% map to one of our leaves or are flagged unmapped (never forced). (b) Rename and merge three nodes: old URLs 301 to new, no entry loses membership. (c) 50 manufacturers described in free text land on correct leaves, 90% agreement with two human labelers. (d) No leaf has more than the agreed number of child facets (default 15) as list types. |

### 2.4 Area 3: Entity resolution

| Item | Detail |
|---|---|
| Covers | Deciding that two records are the same real business or person; blocking; scoring; thresholds; clusters; merge and unmerge; transliteration; chain versus branch; keeping credit and URLs after merges. |
| Why AllLists needs it | Entries are stored once (rule 3). Every source (Overture, Foursquare, registers, owner uploads, agents) repeats the same business. At 1M entries all-pairs would be 5e11 comparisons; blocking to about 20 per block gives about 9.5 million [R: plan 7.4]. A false merge destroys a business's page; a missed duplicate splits its reputation. |
| 10k | L2: trigram and phone-hash rules, human review. |
| 1M | L3: Splink or similar with calibrated thresholds, labelled pairs, script folding, unmerge, review queue sizing. |
| 100M | L4: blocking rules per country, active learning on reviewer decisions, cluster stability checks, incremental linking (only new records versus existing), per-country models. |
| Tools and repositories [K] | Splink (MIT per `REUSE_AND_TOOLS.md` read from file; version 4 released, DuckDB, Spark and Athena backends, claims a million records in about a minute on a laptop and 100M+ on big-data backends, [S] S1); `dedupe`; `recordlinkage`; Zingg (Spark based); libpostal (address parsing); rapidfuzz (string distances); python-phonenumbers; pg_trgm and unaccent; Overture conflation notes ([S] S9). Benchmarks: Abt-Buy, Amazon-Google, WDC Products (entity matching benchmarks). Transformer matchers (DeepMatcher, Ditto) only for hard text-heavy cases. |
| Learning resources [K] | Christen, "Data Matching"; Fellegi and Sunter (1969) model behind Splink; Papadakis et al. surveys on blocking; Splink documentation tutorials and the MoJ blog ([S] S1). |
| Who | F: sets the cost of a wrong merge versus a missed one. C: builds, labels sample pairs for review, calibrates. H: data scientist at S2. V: none. |
| Test of competence [H] | On the 500 labelled pilot pairs (already planned in `DECISIONS.md`): auto-merge precision at least 0.99 at the chosen threshold, recall reported, review-queue size per 10,000 new records stated. Transliteration pairs (the plan found trigram similarity 0.54 for two spellings of one Urdu name and 0.00 for Urdu against Latin [R: plan 2.2]) scored separately; at least 0.9 recall after folding and alias table. Unmerge round trip: merge then unmerge returns both entries, credit and URLs unchanged. Monthly: if reviewers reject more than 10% of auto-merges, thresholds go up (plan 7.4). |

### 2.5 Area 4: Search relevance

| Item | Detail |
|---|---|
| Covers | Query understanding (folding, synonyms, typos, transliteration), retrieval, ranking, facets and counts, autocomplete, evaluation (judgement lists, NDCG), click models, paid-placement separation, index sync, zero-result handling. |
| Why AllLists needs it | Browse is the main path, but search decides conversion. Scoped search is about 5 ms but unscoped fuzzy name search is 150 to 520 ms at 1M [R: plan 10.1]; the trigger for a dedicated engine is p95 over 500 ms (S3). Paid ranking is a revenue line and a fairness risk (R14). |
| 10k | L1: Postgres plus trigram, a 200-query test set. |
| 1M | L2: judgement lists, NDCG@10 tracked, synonym curation, zero-result rate under 15% (plan). |
| 100M | L4: dedicated engine with 90 to 150 GB of index [I: `03_hosting_and_costs.md` section 3], learning to rank, query logs, position-bias correction, A/B or interleaving, per-country analyzers. |
| Tools and repositories [K] | Postgres full-text and `pg_trgm`; Meilisearch (MIT community edition, some BUSL parts per `REUSE_AND_TOOLS.md`); OpenSearch (Apache-2.0); Typesense (GPL-3, avoid copying); Elasticsearch (licence changed more than once, UNVERIFIED current terms); Vespa (Apache-2.0); Tantivy and Quickwit (Rust search library, logs); pgvector for embeddings; ParadeDB `pg_search` (licence UNVERIFIED, believed AGPL); Quepid and Splainer (open relevance-tuning tools from OpenSource Connections); `ranx` and `ir_measures` (evaluation libraries); XGBoost or LightGBM (LambdaMART ranking); SymSpell (typo correction, MIT). Public data: Amazon Shopping Queries Dataset ([S] S6) for method practice. |
| Learning resources [K] | Turnbull and Berryman, "Relevant Search"; Manning, Raghavan, Schütze, "Introduction to Information Retrieval" (free online); Grainger et al., "AI-Powered Search"; Joachims on unbiased learning to rank; the faceted-search guides for OpenSearch and Elasticsearch ([S] S12). |
| Who | F: signs off ranking rules and the "How this list is ordered" page. C: builds, runs evaluations. H: search engineer from S3. V: managed search only if hosting cost beats self-run (Meilisearch Cloud overage was computed at USD 20,000 a month at 100M documents, `03_hosting_and_costs.md` section 3). |
| Test of competence [H] | (a) 200-query test set built by native speakers: NDCG@10 and zero-result rate reported per country; no release if NDCG falls more than 2 points. (b) Same test suite passes on Postgres and the engine adapter (P6.01 acceptance). (c) Index rebuild into a new alias and swap with zero errors. (d) Paid slot never alters the organic order of other results (property test). |

### 2.6 Area 5: Geospatial

| Item | Detail |
|---|---|
| Covers | Place tree, geocoding, reverse geocoding, address parsing, pins and precision classes, distance and nearest queries, polygons, hex or tile indexes, coordinate systems, map tiles. |
| Why AllLists needs it | Every list is "a type at a place". "Near you" needs location. Informal addresses ("near X") are normal in the first markets. Rule R36 stores only point, precision class and source. |
| 10k | L1: GeoNames tree, manual pins. |
| 1M | L2: PostGIS on (plan S1), nearest-area matching, geocoder with permissive terms, pin QA by surveyors. |
| 100M | L3: area polygons, H3 or S2 cell keys for roll-ups, tile service (Protomaps) if maps are added, per-country geocoding quality dashboards. |
| Tools and repositories [K] | PostGIS (GPL, used as extension); H3 (Uber, Apache-2.0); S2 geometry (Google); GeoNames (CC BY 4.0); Overture divisions and addresses; OpenStreetMap (ODbL, kept as separate layer per decisions); Nominatim (GPL), Pelias (MIT), Photon (Apache-2.0), Mimirsbrunn (AGPL, avoided) per `REUSE_AND_TOOLS.md`; libpostal; Who's On First (admin boundaries); Protomaps PMTiles and MapLibre GL JS; `shapely` and `pyproj`. |
| Learning resources [K] | "PostGIS in Action"; PostGIS documentation workshops; H3 documentation; Overture documentation ([S] S9); OSM wiki on address and place tags. |
| Who | F: decides when maps enter scope. C: builds, tests PostGIS (not tested in this environment, plan 2.1). H: GIS contractor at S1 to S2. V: geocoder if its terms allow storing results. |
| Test of competence [H] | (a) 1,000 pilot addresses: share geocoded within 100 m of surveyor pin, reported per source. (b) "Nearest area" query p95 under 50 ms at 1M places. (c) Place merges and renames keep stable IDs and redirects. (d) Coordinates from Chinese sources converted correctly (GCJ-02, BD-09) at link time (plan 7.5). |

### 2.7 Area 6: Database internals and scaling

| Item | Detail |
|---|---|
| Covers | Query planning, indexes (b-tree, GIN, GiST, BRIN), vacuum and bloat, locks, WAL, replication, partitioning, connection pooling, backups and restore, online schema change, backfills, capacity arithmetic. |
| Why AllLists needs it | The database, not CPU, is the limit at 100M [R: `03_hosting_and_costs.md` section 3]. Planning size 837 GB; 5,300 queries a second at peak; PlaceList 352 million rows at 235 types. |
| 10k | L2: sound indexes, `pg_stat_statements`, tested backups. |
| 1M | L3: standby, point-in-time recovery, pgBouncer, country partitions (hand-written migration, because Django has no composite foreign keys), vacuum tuning. |
| 100M | L4: country-group clusters, physical backups, failover drills, partition maintenance automation, per-cluster audit chains, bloat control on hot tables. |
| Tools and repositories [K] | PostgreSQL; `pg_stat_statements`; pgBadger; pganalyze (service); HypoPG; pgBouncer; Patroni; pgBackRest; pg_partman; pg_repack and pg_squeeze (bloat); Citus (sharding extension); pgroll (Xata) and Reshape for zero-downtime migrations ([S] S2); `squawk` (migration linter); GitLab's public database guidelines (batched background migrations, migration style guide); Stripe's "Online migrations at scale" blog; Instagram's sharding and ID blog posts. |
| Learning resources [K] | Rogov, "PostgreSQL 14 Internals" (free); Suzuki, "The Internals of PostgreSQL"; "Use The Index, Luke"; Crunchy Data and Percona blogs; Citus article on partitioning versus sharding ([S] S13); Kleppmann chapters on replication and partitioning. |
| Who | F: none. C: designs, writes migrations, runs the load tests and drills. H: Postgres DBA (contract at S2, employee at S4). V: managed Postgres with PITR at S1. |
| Test of competence [H] | (a) Restore drill: time to restore the current dataset is recorded and projected to 0.84 TB (target: physical restore plus standby promotion under 1 hour). (b) A 100M-row backfill rehearsed on a copy with replication lag never above 5 s and p95 of live queries unchanged. (c) `EXPLAIN` review of the 10 slowest queries each month. (d) Add and drop a column and an index on a 100M-row copy with no lock wait over 1 s. |

### 2.8 Area 7: SRE and cost control

| Item | Detail |
|---|---|
| Covers | Monitoring, alerting, SLOs and error budgets, incident response, runbooks, capacity and load tests, deployment and rollback, backup and restore drills, FinOps (cost per entry, per page, per verified record), vendor spend caps. |
| Why AllLists needs it | A tiny team runs a big estate. Spend caps default to zero and the agent budget has hard stops (rule 6). The hosting model shows costs scale with bots as well as people (bots assumed 3 times humans) [R]. |
| 10k | L2: health page, hourly alert email, restore drill (exists). |
| 1M | L3: SLOs, on-call, dashboards, load tests at 3 times peak, cost per entry reported monthly. |
| 100M | L4: multi-cluster operations, chaos and failover drills, capacity forecasts, vendor negotiations, cost attribution per feature. |
| Tools and repositories [K] | Prometheus, Grafana, Loki, OpenTelemetry, Sentry, UptimeRobot, k6 (AGPL, run as a tool) and Locust (MIT); OpenTofu or Terraform; Ansible; Alertmanager; postgres_exporter; Cloudflare analytics; cost tools (cloud provider cost explorers, OpenCost for Kubernetes if ever used). |
| Learning resources [K] | Google "Site Reliability Engineering" and "The Site Reliability Workbook" (free online); Nygard, "Release It!"; Majors et al., "Observability Engineering"; FinOps Foundation framework; Dan Luu's postmortem collection. |
| Who | F: accepts budgets and risk. C: runbooks, scripts, drills. H: SRE at S2. V: monitoring SaaS, CDN. |
| Test of competence [H] | (a) Game-day each quarter: pick a runbook (restore, scraper surge, indexing drop), run it on staging, record time to detect and recover. (b) Load test at 3 times peak passes (P6.03). (c) Cost per 1,000 pages and cost per verified record tracked and within plan band. (d) Every alert has a runbook link; every incident gets a note under `docs/incidents/`. |

### 2.9 Area 8: SEO at scale

| Item | Detail |
|---|---|
| Covers | Indexable-URL policy, canonicals, faceted navigation control, sitemaps, internal linking, structured data, crawl-budget management, log analysis, thin-page handling, spam-policy compliance, indexing watch, AI-search visibility. |
| Why AllLists needs it | Traffic is the growth engine (Google and AI search). Millions of list pages are exactly what Google's scaled-content policy targets ([S] S8). D-08 requires sharded sitemaps, canonicalised facets and unpublished empty pages. |
| 10k | L2: noindex unless switch on and 10 verified entries (built per `DECISIONS.md`). |
| 1M | L3: sitemap shards by country and level, Search Console API monitoring, log-file analysis, indexation rate by template. |
| 100M | L4: crawl-budget engineering, per-template quality gates, experiments on page templates, structured-data validation at scale, defence against scraped clones. |
| Tools and repositories [K] | Google Search Central documentation (spam policies, large-site crawl budget, sitemaps); Search Console and its API; sitemap protocol (50,000 URLs or 50 MB per file); Lighthouse and CrUX; schema.org LocalBusiness and ItemList; IndexNow; GoAccess or an ELK stack for logs; Screaming Frog (commercial) or the open-source `advertools` Python package for crawling and log analysis. |
| Learning resources [K] | Google's documentation on large sites and faceted navigation; Search Engine Land and Search Engine Journal archives on programmatic SEO; post-mortems of directories and marketplaces (UNVERIFIED, not collected yet). |
| Who | F: none beyond content policy. C: builds, watches the day-90 indexing report. H: SEO lead at S2. V: none (Search Console is free). |
| Test of competence [H] | (a) Indexation: share of submitted URLs indexed after 90 days per template, target stated before launch. (b) No facet URL appears in a sitemap; canonical and noindex tests run on the sample-page set. (c) Every published page has at least N verified entries and a unique statistic block (default N = 5, plan R23 uses 10 verified for index). (d) Log analysis shows crawl share by template and bot, monthly. |

### 2.10 Area 9: Trust and safety

| Item | Detail |
|---|---|
| Covers | Fake supplier and fake business detection, seller and contributor onboarding checks (KYB), sanctions screening, fake reviews, account farms, abuse reports, takedown handling, child and individual safeguards, policy writing, enforcement tooling, appeals. |
| Why AllLists needs it | The checks (four labels) are the product's trust claim. Sialkot-type buyers abroad will use lists to find suppliers; one fake listing damages the register. DSA-style trader traceability is a legal pattern for marketplaces ([S] S7). |
| 10k | L2: report form, takedown, canaries, source gate (built). |
| 1M | L3: risk scoring per entry and per account, document checks, registry cross-checks, review queues with SLAs, appeals. |
| 100M | L4: graph-based fraud detection, automated enforcement with human appeal, regional policy teams, transparency reporting. |
| Tools and repositories [K] | Cloudflare Turnstile or hCaptcha; open sanctions data (OFAC lists are free; OpenSanctions data licence for commercial use UNVERIFIED); company registers (OpenCorporates is share-alike and excluded per `DECISIONS.md`); python-stdnum (tax and company number validation); networkx or Postgres recursive queries for shared-attribute graphs; commercial KYB and fraud services (Sumsub, Persona, Sift, Stripe Radar; named from [K], not evaluated); Tech Coalition and Trust and Safety Professional Association material for policy practice. |
| Learning resources [K] | TSPA curriculum; Stanford Trust and Safety research materials; DSA articles on marketplaces ([S] S7); FTC and EU guidance on fake reviews (UNVERIFIED, need to be opened). |
| Who | F: sets policy on enforcement (default: remove when in doubt for individuals and children). C: builds queues and detectors. H: T&S lead at S1. V: KYB and sanctions provider. Counsel for law. |
| Test of competence [H] | (a) Planted fake suppliers (canary entries) detected: at least 90% flagged before publication. (b) Median time from report to action per report type, tracked. (c) Appeal outcomes: share overturned under 10%. (d) Sanctions screening: 100 known listed names (public lists) are all caught, 100 common names produce under 2% false hits. |

### 2.11 Area 10: Payments and billing

| Item | Detail |
|---|---|
| Covers | Gateways, payouts, ledger design, refunds and chargebacks, reconciliation, currencies, invoicing, tax (VAT, GST, sales tax), marketplace deemed-supplier rules, subscription lifecycle, revenue sharing with contributors (50, 40, 30 percent steps), compliance for holding balances. |
| Why AllLists needs it | Revenue is subscriptions, ads, placements, extracts and list sales, with contributor shares. Pakistan, Gulf and foreign buyers each need different rails; Stripe and PayPal do not onboard Pakistani businesses ([S] in plan 2.3). |
| 10k | L2: manual payment recording, ledger tests (built). |
| 1M | L3: live gateway, webhooks with idempotency, reconciliation against provider reports, tax engine or merchant of record, payouts with KYC. |
| 100M | L4: multi-currency treasury, provider routing, dispute operations, audit-ready finance, ledger on its own database (plan S4). |
| Tools and repositories [K] | Saleor (BSD-3, payouts design study); Formance Ledger (MIT); TigerBeetle (only if volume demands); Hyperswitch by Juspay (open-source payments router, Apache-2.0 believed); Hypothesis (already in requirements); python-stdnum and the EU VIES service for VAT number checks; tax engines (Avalara, Stripe Tax; merchant of record such as Paddle; all [K]); Modern Treasury "Accounting for Developers" series. |
| Learning resources [K] | "Accounting for Developers" (Modern Treasury, free); Stripe engineering blog on idempotency and online migrations; Square engineering blog on ledgers; Pat Helland "Accountants Don't Use Erasers"; EU VAT e-commerce rules summary ([S] S10). |
| Who | F: picks provider after bake-off (Q-S/F12). C: ledger, adapters, property tests. H: payments engineer plus finance lead (accountant) before first real payment. V: gateway, tax engine, counsel on payout licensing. |
| Test of competence [H] | (a) Property tests: sum of postings is zero; allocations sum to net revenue; rounding by largest remainder; refunds exact (built; keep green). (b) Replay every webhook twice: no double fulfilment. (c) Daily reconciliation shows zero unexplained difference for 30 days on staging with provider sandbox. (d) Tax lines for five sample jurisdictions agree with an accountant's worked examples. |

### 2.12 Area 11: Legal and privacy

| Item | Detail |
|---|---|
| Covers | Data protection (GDPR and local laws), lawful basis and consent, data subject rights, erasure through derived copies, scraping and database rights, licences of open data (ODbL share-alike), terms of service, marketplace liability, advertising and messaging rules (WhatsApp, SMS, email), health and child rules, records retention. |
| Why AllLists needs it | Individuals, health, children and messaging are gated (rule 5). Each country has its own switch (R24). Source licences gate every batch (R21, R22). |
| 10k | L2: gates and consent register (built). |
| 1M | L3: per-country legal packs, DPIAs, processor agreements, retention schedules, takedown SLAs. |
| 100M | L4: privacy engineering with automated erasure across all copies, data-residency options, regulator relationships, transparency reports. |
| Tools and repositories [K] | ICO DPIA templates; the Data Privacy Vocabulary (W3C community group); Fides by Ethyca (open-source privacy engineering, Apache-2.0 believed); OneTrust and similar (commercial); licence texts (ODbL, CC BY 4.0, Apache-2.0). |
| Learning resources [K] | GDPR articles and EDPB guidelines; ICO guidance on lawful basis; the DSA marketplace articles ([S] S7); legal commentary on scraping cases (hiQ v LinkedIn in the US, Ryanair v PR Aviation in the EU; both [K], UNVERIFIED, counsel to confirm). |
| Who | F: decides risk appetite and signs. C: prepares question lists, reads licences, keeps the source register. H: privacy counsel or DPO. V: counsel hours (budgeted per plan 2.3). |
| Test of competence [H] | (a) Erasure drill: erase one test person; confirm gone from entries, search index, caches, extracts (tracer names), backups after retention window. (b) Every source in the gate has licence text and review date (Backend research default). (c) Counsel sign-off recorded before: any messaging test, individuals list, health or child data, talent list, first payout. |

### 2.13 Area 12: Data annotation operations

| Item | Detail |
|---|---|
| Covers | Labelling guidelines, labeller recruitment and training, task design, gold questions and canaries, inter-annotator agreement, adjudication, quality dashboards, throughput and cost, volunteer motivation, surveyor field verification. |
| Why AllLists needs it | The founder's model uses volunteers and surveyors; verification levels need evidence; agents are trained by audited labels. Quality of human labels caps quality of the whole system. |
| 10k | L1: a few surveyors, canaries (built). |
| 1M | L3: guidelines per list family, agreement measured, adjudication, labeller scorecards, paid panels if needed. |
| 100M | L4: tiered workforce, vendor panels, automated pre-labelling with audit, active learning to choose what humans see. |
| Tools and repositories [K] | Label Studio (Apache-2.0), Argilla (Apache-2.0), doccano (MIT), Prodigy (commercial); Krippendorff alpha and Cohen kappa (statsmodels, `krippendorff` package); Cleanlab (label-noise finding; open-source licence believed AGPL, check); vendor panels (Toloka, Scale, Surge, Appen; named from [K], not evaluated). |
| Learning resources [K] | Monarch, "Human-in-the-Loop Machine Learning"; Google PAIR guidebook; crowdsourcing quality literature (Dawid and Skene model); the project's own note `Backend research/04_agent_training_and_ai_auditor.md` sections 3 and 4. |
| Who | F: owns volunteer relations and rewards. C: builds task tools, computes agreement. H: annotation ops lead at S1 to S2. V: label tool hosting, panels. |
| Test of competence [H] | (a) Krippendorff alpha at least 0.8 on core fields for two independent surveyors on 100 shared entries. (b) Canary detection: planted wrong entries caught by at least 90% of surveyors, otherwise retrain or suspend (exists as rule). (c) Cost per verified record and time per task, weekly. (d) 385-record audit sample accuracy per surveyor (95% interval ±5 points). |

### 2.14 Area 13: Agent engineering and evaluation

| Item | Detail |
|---|---|
| Covers | Tool-using agents, structured output, prompt versioning, evaluation sets (frozen pages and world truth), regression tests on model change, cost caps, prompt-injection defence, auditing by an independent agent, drift detection, fallback to humans. |
| Why AllLists needs it | Agents draft entries at the cost of USD 0.04 to 0.20 a record [S in `03_hosting_and_costs.md` section 7]. The stop rules (90% accuracy, USD 0.30 per verified record) are written but not yet measured by a gold set (`04_agent_training_and_ai_auditor.md` section 0). |
| 10k | L2: capped agents on fake model (built), first gold set. |
| 1M | L3: versioned prompts, sealed gold set, shadow and canary stages, auditor service, per-country controls. |
| 100M | L4: multi-model routing, batch APIs and caching for cost, automatic demotion, large-scale audits, agent memory kept out of scope (stateless jobs). |
| Tools and repositories [K] | Anthropic API documentation (tool use, batch, prompt caching), the `claude-api` skill in this environment; promptfoo (MIT) and Inspect AI (UK AISI, MIT) for evaluation harnesses; Langfuse (MIT core) for tracing; Arize Phoenix; LiteLLM (provider routing); Hypothesis for adversarial test generation; OWASP Top 10 for LLM Applications; Anthropic's "Building effective agents" essay. |
| Learning resources [K] | The two docs above; the research note `04_agent_training_and_ai_auditor.md` (the project's own authority); Simon Willison's writing on prompt injection; eval blogs listed in note 04 section 2 (UNVERIFIED there). |
| Who | F: sets caps. C: builds the loop, runs evaluations under human approval. H: ML engineer by S1 to S2. V: model provider; check retention and training terms before sealed-test runs (note 04 section 3.6, UNVERIFIED). |
| Test of competence [H] | (a) Gold set per stratum with sealed test split; the evaluation runner reports record accuracy with a 95% lower bound. (b) Prompt-injection test pages: 0 of 50 planted instructions obeyed. (c) A model-id change forces the full ladder (note 04 section 5.1). (d) Auditor independence tests pass (import-boundary test, note 04 section 6.2). |

### 2.15 Area 14: Product analytics

| Item | Detail |
|---|---|
| Covers | Event design, funnels, retention, cohort and revenue analytics, search analytics (zero-result and click rates), experiments, data-quality dashboards, privacy-safe measurement, metric definitions. |
| Why AllLists needs it | Pricing and access rules are judged on two tests: better usage and returning clients, and revenue (CP8). Search relevance and SEO both need measured outcomes. |
| 10k | L1: events catalogue (built), a handful of counts. |
| 1M | L2: warehouse tables, weekly metrics review, experiment framework with minimum sample sizes. |
| 100M | L3: self-serve analytics, sequential testing, causal methods, forecasting. |
| Tools and repositories [K] | PostHog (MIT core, self-hostable), Umami (MIT), Plausible (AGPL), Matomo (GPL); Metabase (AGPL) or Apache Superset (Apache-2.0); GrowthBook (MIT core, experiments); DuckDB and dbt; statsmodels. |
| Learning resources [K] | Kohavi, Tang, Xu, "Trustworthy Online Controlled Experiments"; Croll and Yoskovitz, "Lean Analytics"; Evan Miller's A/B testing articles. |
| Who | F: picks the few metrics that matter. C: builds the pipeline and weekly report. H: analyst at S2. V: analytics SaaS optional. |
| Test of competence [H] | (a) Each metric has a written definition and a test that recomputes it from raw events. (b) An A/A test shows no false winner at the chosen alpha. (c) Cookie-light measurement still works when consent is declined (counted once a day per visitor via the private fragment is already built). |

### 2.16 Area 15: Security

| Item | Detail |
|---|---|
| Covers | Application security (OWASP), secrets, access control, encryption and key rotation, supply-chain security, abuse and bot defence, SSRF and fetcher safety, infrastructure hardening, logging and detection, incident response, third-party penetration tests, threat modelling. |
| Why AllLists needs it | Contacts are encrypted and never shown; a leak is the most damaging event (breach runbook exists). The agent fetcher touches arbitrary web pages; payments and payouts add attack surface. |
| 10k | L2: headers, CSP, MFA for staff, Argon2id, bandit, pip-audit (built). |
| 1M | L3: external penetration test, WAF rules, key rotation drills, SBOM, dependency policy. |
| 100M | L4: security engineering team, detection and response, bug bounty, red-team exercises, compliance audits. |
| Tools and repositories [K] | OWASP ASVS and Cheat Sheet Series; OWASP ZAP (Apache-2.0); Semgrep (LGPL); bandit; pip-audit; Trivy; gitleaks and trufflehog (secret scanning); ModSecurity with OWASP Core Rule Set; CrowdSec (MIT); GitHub secret scanning (already blocked one push, plan 2.1); OWASP Automated Threats handbook for scraping and abuse ([S] S14). |
| Learning resources [K] | PortSwigger Web Security Academy (free); OWASP Web Security Testing Guide; Shostack, "Threat Modeling"; Django security documentation. |
| Who | F: only the founder can rotate secrets (`secret-rotation.md`). C: code review, `security-review` skill on each phase. H: security engineer at S2. V: penetration test firm before launch. |
| Test of competence [H] | (a) Penetration test with no high findings open at launch. (b) Secrets drill: rotate one key in staging in under 30 minutes. (c) SSRF and DNS-rebinding tests on the fetcher stay in CI (exist). (d) Dependency alerts fixed within 7 days for high severity. |

### 2.17 Area 16: Logic, correctness and systems design

| Item | Detail |
|---|---|
| Covers | Invariants and state machines, property-based and mutation testing, formal specs for the few critical protocols (ledger, merge, consent), idempotency, ordering and concurrency, failure-mode analysis, decision records, simplicity versus scale trade-offs, back-of-envelope arithmetic before design (rule 4 of `depth-and-scale`). |
| Why AllLists needs it | The founder wants strong logic. Ledger, verification states, consent and merges are rule-heavy; the rigorous testing round already found eight concurrency and parsing defects [R: `DECISIONS.md`]. At scale, small logic flaws are replicated millions of times. |
| 10k | L3: rules in code, property tests, state machine guards (built). |
| 1M | L3: model-based tests for merge and ledger; chaos on retries and duplicates. |
| 100M | L4: formal models for cross-cluster operations, consistency design per data class, architecture reviews. |
| Tools and repositories [K] | Hypothesis (in use), `hypothesis.stateful` rule-based state machine tests; the mutation check script (`scripts/mutation_check.py`); TLA+ and Apache-licensed TLC tooling; Alloy; `transitions` state machine library; ADR templates (MADR); Jepsen reports for failure patterns. |
| Learning resources [K] | Kleppmann; Helland, "Life Beyond Distributed Transactions" and "Data on the Outside versus Data on the Inside"; Lamport's TLA+ video course; Nygard, "Release It!"; Hillel Wayne, "Practical TLA+". |
| Who | F: none. C: applies it, writes the model-based tests. H: staff engineer by S3. V: none. |
| Test of competence [H] | (a) Every new rule gets a test that fails when the rule is broken (mutation check, no surviving mutants in money, consent, merge code). (b) Each design note starts with scale arithmetic (rows, bytes, cost, restore time, lock time). (c) Two-run property: every import, merge and payout operation is safe to run twice. |

### 2.18 Team shape by stage [H]

| Stage | People | Why |
|---|---|---|
| S0 to S1 (to 50k entries) | Founder; Claude; counsel hours; pilot surveyors (volunteers); one part-time contractor reviewing Postgres and security | Plan says no stage is bought early; hire only against a trigger |
| S2 (1M) | + Postgres or SRE contractor (part-time), annotation operations lead, taxonomist (contract), T and S lead, accountant | Standby, partitions, Splink, KYB, finance close |
| S3 (10M) | + data engineer, search engineer, SEO lead, security engineer, analyst | Search engine trigger; multiple countries |
| S4 (100M) | Platform team with on-call, data science, privacy officer, payments engineer, regional operations leads | Country-group clusters; legal and fraud scale |

---

## 3. Challenge register (62 challenges)

Columns: **ID**; **Challenge** (and why it bites at scale); **Concrete solution**; **Tool, repository or source**; **Area** (number from section 2.1); **First needed** (stage); **Status** [R] (built, partly, not built).

Priority marker in the last column: **N** = needed now, because it decides schema or process; **P** = plan ahead; **L** = later.

Arithmetic anchors from the repository [R]: 1.7 KB per realistic entry (7.5 KB planning); 100M entries is 750 GB planning; roll-up touches about 31 cells per change; `count(*)` over a country 203 ms; list query 1.7 ms; `PlaceList` 144 B a row.

### 3.1 Catalogue, duplicates and taxonomy

| ID | Challenge | Concrete solution | Tool or source | Area | First | Status | Pri |
|---|---|---|---|---|---|---|---|
| C01 | Duplicate entities across contributors and sources (the same shop from Overture, Foursquare, an owner upload and an agent) | Block by place subtree plus concept, phone hash, and a 100 m point; score phone, proximity, folded name, alias table, address; auto-merge only above a calibrated threshold; otherwise a review task; keep the earliest credit | Splink, pg_trgm, rapidfuzz; plan 7.4 | 3 | S1 | Partly (pg_trgm v1, thresholds guessed) | N |
| C02 | Duplicate products or goods across sellers (the Amazon case): the same surgical instrument listed by 300 makers with different titles | Treat as a product-entity layer later: identify by brand, model, MPN and GTIN where present; cluster by attributes; show one product node with many supplier offers; do not merge suppliers | Amazon matching approach ([S] S3); AutoKnow ([S] S5); Splink on product attributes | 3 | S3 | Not built (commerce is a later module) | L |
| C03 | Chain or branch versus separate business (same phone, different address; same name, two branches) | Parent entity and branch entity; never auto-merge on phone alone when addresses differ beyond a distance; brand link to Wikidata where known | Overture `brand` field, Wikidata ([R] `REUSE_AND_TOOLS.md` 2b) | 3 | S1 | Not in build log | N |
| C04 | Same business in different scripts (Urdu, Roman Urdu, English) | Folding rules, alias table, transliteration keys, separate scoring for script pairs | Plan 7.3 folding; ICU; custom alias table | 3 | S1 | Built (folding), calibration open | N |
| C05 | Merge and unmerge with stable URLs and credit | Merge map, tombstones, 301 redirects, reversible merge events, credit events preserved | Plan 6.7, `merge service` (built) | 3 | S1 | Built (merge), unmerge not seen | N |
| C06 | Deep category mapping across Overture, Foursquare, ISIC, UNSPSC, HS and GPC (many-to-many, different depths, different meanings) | Crosswalk table with relation type (exact, close, broader, narrower) and confidence; unmapped is a valid state; LLM proposes, person approves; never force a mapping | W3C SKOS mapping properties; Overture and Foursquare categories | 2 | S1 | Not built | N |
| C07 | Taxonomy depth explosion: capabilities modelled as types (process, material, certification) multiply leaves | Capabilities are facets not types (D-03); facet registry with values and allowed combinations; cap on list types per parent | `depth-and-scale` skill; D-03 | 2 | S1 | Rule recorded, not enforced in code | N |
| C08 | Stored-list explosion: a row per type per place (100,000 types by 1.5 million places = 150 billion rows) | Hybrid rule (D-06): store above a depth threshold or when an entry exists; resolve the rest virtually; row arithmetic in `01_manufacturing_depth_taxonomy.md` (when written) | D-06; `generate_lists --levels`; `--confirm-large` | 2 | S1 | Partly (flag exists, hybrid not coded) | N |
| C09 | Taxonomy drift: renames, merges and splits over years | Permanent node IDs and slugs, deprecation not deletion, redirect map, versioned release notes, monthly diff review | SKOS style deprecation; D-05 | 2 | S2 | Rule only | P |
| C10 | Faceted-search explosion: facet combinations create millions of crawlable URLs and heavy aggregations | Facets never indexed (rule exists); allowlist for a few indexable combos; precomputed counts for top facets; engine aggregations with eager global ordinals; cache facet queries | Google faceted navigation guidance; OpenSearch aggregation guidance ([S] S12) | 4, 8 | S2 | Built (never indexed); counts partly | P |
| C11 | Attribute normalisation: phones, units, currencies, addresses, opening hours | Normalise at write, keep raw; one library per type; reject when unparseable | python-phonenumbers, pint, ISO 4217, OSM `opening_hours` grammar, libpostal | 1 | S1 | Partly (not in requirements) | N |
| C12 | Informal addresses ("near X, Adyala Road") | Landmark and area records, surveyor pins with precision class, H3 cell as key, geocode only where terms allow | Pelias, Photon, H3; plan 7.5 | 5 | S1 | Not built | P |
| C13 | Closed, moved or renamed businesses stay on the list | Operating-status field with source and date; closure signals from sources and calls; "permanently closed" workflow with grace period; freshness bonus in ranking | Overture operating status; plan expiry and grace (built) | 1, 9 | S1 | Partly (expiry and grace built) | P |

### 3.2 Data freshness, quality and bulk operations

| ID | Challenge | Concrete solution | Tool or source | Area | First | Status | Pri |
|---|---|---|---|---|---|---|---|
| C14 | Stale data at scale: 100M entries cannot all be re-verified | Freshness score per field with half-life by type; re-check queue ordered by (traffic x staleness x risk); change detection by content hash and ETag; honest `lastmod` | Plan 7.7 (expired chips, early warning at 25%); Bayesian staleness model [H] | 1, 13 | S1 | Partly (expiry built, queue not) | N |
| C15 | Catalogue quality scoring | Score = completeness x validity x freshness x verification level, stored per entry and per list; publish bar and ranking prior use it; dashboard by source | Great Expectations, Soda Core or pandera for field checks; plan 7.7 | 1, 3 | S1 | Partly (publish bar built, score not) | N |
| C16 | Backfill of 100M rows | Keyset-paginated batches (e.g. 5,000 rows), throttle on replica lag and p95, checkpoints, resumable, run as background job, dry run on a copy, progress dashboard | GitLab batched background migrations (pattern, [K]); pgroll batch settings ([S] S2); Procrastinate | 6 | S2 | Not built | N |
| C17 | Schema migrations with no downtime | Expand then contract; add columns nullable; `CREATE INDEX CONCURRENTLY`; constraints `NOT VALID` then `VALIDATE`; `lock_timeout` on every migration; linter in CI; two-release rule for renames | pgroll, Reshape, squawk, Django migration checks ([S] S2) | 6 | S1 | CI has migrations check only | N |
| C18 | Partitioning key and Django limits (no composite foreign keys) | Hand-written SQL migration to country list partitions; keys carry `country_code`; test restore and detach | Plan 4.1; pg_partman | 6 | S2 | Not built | N |
| C19 | Global write hot spot: one audit hash chain and one advisory lock (727001) | Per-partition or per-country chains; periodic anchor hashes; batch audit inserts for bulk paths | `core/models.py`; D-10 | 6, 16 | S2 | Not built | N |
| C20 | Hot-table bloat from roll-up updates every five minutes | Fillfactor and HOT updates; append delta rows and merge; partition and swap; autovacuum tuned per table; `pg_repack` | PostgreSQL docs; pg_repack | 6 | S2 | Not built | P |
| C21 | Counting at scale (`count(*)` over a country 203 ms) | Roll-up cells for pages; "as of" time; HyperLogLog for distinct counts; bounded live count fallback | Plan 4.4 and 10.3; postgresql-hll [K] | 6 | S1 | Built (roll-ups) | N |
| C22 | Restore time: 3.3 hours at 0.84 TB against a goal of 1 hour | Physical backups with pgBackRest, standby that can be promoted, WAL archive, drills quarterly | `03_hosting_and_costs.md` section 3; pgBackRest, Patroni | 6, 7 | S2 | Logical dump only | P |
| C23 | Connection exhaustion with many web workers | pgBouncer in transaction mode; check Django server-side cursors and prepared statements; pool sizes per role | pgBouncer docs | 6 | S2 | Not built | P |
| C24 | Read-after-write with replicas (user adds entry, then sees old page) | Router with sticky primary for N seconds after a write; lag guard; shared pages tolerate staleness | Django routers; replica router (built) | 6 | S3 | Partly | L |
| C25 | Large imports from uploaders (millions of rows, malformed, fraudulent) | Staging with reject files, sample audit, uploader reputation, lawful-basis record, resumable publish; DuckDB for profiling before staging | `intake/bulk.py` (built); DuckDB, Polars | 1, 9 | S1 | Partly (UI, worker, fraud checks not built) | N |
| C26 | Source licence tracking per record (ODbL share-alike contamination) | Licence on every record and field; gate blocks share-alike layers from merged lists; separate layer if ever used | Plan R21 and R22; Overture per-record licence | 11 | S1 | Built (gate) | N |
| C27 | Index sync between Postgres and the search engine | Outbox table plus change capture; versioned index and alias swap; nightly count and checksum compare | Debezium or logical decoding; OpenSearch or Meilisearch | 4, 1 | S3 | Not built | L |

### 3.3 Search and ranking

| ID | Challenge | Concrete solution | Tool or source | Area | First | Status | Pri |
|---|---|---|---|---|---|---|---|
| C28 | Search ranking fairness: paid placement versus trust | Labelled paid slots only (built); organic order independent of payment; "How this list is ordered" page; exposure audit by seller size, country and new versus old | Plan R14; `access/placements.py` (built); fairness-of-exposure metrics [H] | 4 | S1 | Built (slots) | N |
| C29 | Cold start: new entries have no clicks | Quality-score prior; small exploration share; time-boxed boost for verified new entries | Bayesian priors, bandit exploration [K] | 4 | S2 | Not built | P |
| C30 | Position bias in click data | Randomised bucket, inverse propensity weighting, interleaving for tests | Joachims unbiased learning to rank [K]; Quepid | 4 | S3 | Not built | L |
| C31 | Relevance evaluation without a clickstream | Judgement lists with Exact, Substitute, Complement, Irrelevant labels; NDCG@10; LLM judge calibrated to human labels | Amazon ESCI method ([S] S6); `ranx`; Quepid | 4 | S1 | Not built | N |
| C32 | Zero-result queries, synonyms, typos and Roman Urdu | Query log review weekly; synonym table; trigram fallback; SymSpell; "Start this list" flow (built) | Plan 10.1; SymSpell | 4 | S1 | Built (flow); curation open | P |
| C33 | Unscoped search cost (150 to 520 ms at 1M) | Scope first; concept and place lookup unscoped; engine at S3 trigger; cache popular queries | Plan 10.1; Meilisearch or OpenSearch | 4 | S3 | Built (scoping) | P |
| C34 | Multi-type search results (list types, places, entries) blended well | Grouped results with caps per group; type-specific scorers; one blended score only after evaluation | Vespa or OpenSearch multi-index [K] | 4 | S3 | Partly | L |
| C35 | Autocomplete latency at 100M | Separate small index of concepts and places; prefix structures; per-list live search | Meilisearch or OpenSearch suggesters | 4 | S3 | Partly | L |

### 3.4 SEO, traffic and scraping

| ID | Challenge | Concrete solution | Tool or source | Area | First | Status | Pri |
|---|---|---|---|---|---|---|---|
| C36 | Sitemaps at millions of URLs (50,000 URL and 50 MB per file limits) | Shard by country, level and type; sitemap index; only published, indexable pages; accurate `lastmod` | Sitemap protocol [K]; plan 8.6 | 8 | S1 | Built (sharded) | N |
| C37 | Crawl budget wasted on thin and empty pages | Unpublish empty lists; noindex below the bar (10 verified, built); internal links to strong pages; log analysis | Google large-site documentation [K]; GoAccess | 8 | S2 | Partly | P |
| C38 | Programmatic SEO read as scaled content abuse | Each indexed page carries unique verified data and statistics; no boilerplate-only pages; sample human review; watch indexation at day 90 | Google spam policies ([S] S8); `indexing-drop.md` runbook | 8 | S1 | Partly | N |
| C39 | Scraper pressure rebuilding paid lists from free pages | Names-only free view; quotas per address and account (built); alarm at 500, stop at 2,000 fragment requests a day (built); Cloudflare bot rules; planted canary entries; terms | OWASP OAT-011 ([S] S14); `scraper-surge.md` | 15, 9 | S1 | Built | N |
| C40 | AI crawlers and search crawlers: who may read what | Written crawler policy: search engines allowed, unknown bots challenged, AI crawlers decided by founder (allow for discovery versus pay or block) | Cloudflare bot management and verification ([S] S11, weak source) | 8, 15 | S2 | Not decided | P |
| C41 | Leak tracing when a bulk copy appears elsewhere | Planted unique made-up businesses per extract (built); watermark patterns; takedown letters via counsel | `analytics/extracts.py` (built) | 15 | S1 | Built | N |
| C42 | Long-tail cache hit ratio (1M rarely visited pages) | Long `s-maxage` plus stale-while-revalidate; cache key with template version and page stamp; pre-render the head; tiered cache | Plan 3.4; Cloudflare | 7 | S2 | Built (keys) | P |

### 3.5 Trust, safety and onboarding

| ID | Challenge | Concrete solution | Tool or source | Area | First | Status | Pri |
|---|---|---|---|---|---|---|---|
| C43 | Fake supplier listings | Registry cross-check (company and tax numbers), domain age, phone and email reuse graph, document check, surveyor visit for top tier; fake canaries in tests | python-stdnum; registers; plan 6.3 | 9 | S1 | Partly | N |
| C44 | Seller or business onboarding KYC and KYB | Tiered levels: self-declared, registry-matched, document-verified, visited; store encrypted; trader details shown as DSA article 30 requires where it applies | DSA article 30 ([S] S7); KYB vendor (Sumsub, Persona; [K]) | 9, 11 | S1 | Partly (claims built) | N |
| C45 | Sanctions and PEP screening before payouts or paid listings | Screen names and company names against public lists with fuzzy match; manual review for near matches; log decisions | OFAC lists; OpenSanctions (check licence); rapidfuzz or Splink | 9, 10 | before first payout | Not built | P |
| C46 | Fake reviews | Verified users only, one review per user (decision), owner reply, burst and similarity detection, separate from paid rank | `DECISIONS.md` Q-P3; regulators' rules (UNVERIFIED) | 9 | S2 | Rules only | P |
| C47 | Account farms and sybil accounts | Velocity limits, phone or email verification, shared-attribute graph (device, IP block, payout details), Turnstile on forms | Cloudflare Turnstile; Postgres recursive queries; networkx | 9, 15 | S1 | Partly (throttle, honeypot) | P |
| C48 | Contributor credit gaming | Credit payable only after independent verification (built); per-contributor accuracy; collusion detection; credit caps | Plan 6 and 14; ledger rules (built) | 9, 12 | S1 | Built | N |
| C49 | Individuals and child-facing data | Consent only, no public contact, counsel first; held rows in bulk path (built) | Plan 6.8; `bulk.py` | 11 | S1 | Built | N |
| C50 | Appeals and enforcement fairness | Written policy, reason codes, appeal queue with SLA, transparency counts | DSA-style statement of reasons [K] | 9 | S2 | Not built | P |

### 3.6 Money, tax and law

| ID | Challenge | Concrete solution | Tool or source | Area | First | Status | Pri |
|---|---|---|---|---|---|---|---|
| C51 | Cross-border tax on subscriptions and list sales | Merchant of record or tax engine; place-of-supply rules per country; tax lines from configuration (built); keep records 10 years where EU marketplace rules apply | EU VAT rules ([S] S10); accountant; Stripe Tax or Avalara or Paddle [K] | 10, 11 | before first real sale | Partly (config tax lines) | N |
| C52 | Multi-currency and FX | Integer minor units with currency; rate fixed at order; revenue per currency; indicative USD only where rates configured (built) | Plan 12; ISO 4217 | 10 | S1 | Built | N |
| C53 | Payout compliance, chargebacks and refunds after payout | Holds (built); clawback entries; KYC at first payout; two-person approval (built); velocity checks | Plan 12.5 | 10 | S2 | Built (holds, two-person) | P |
| C54 | Ledger correctness under replay and concurrency | Idempotency keys, advisory locks per order (built), balance trigger, daily reconciliation, property tests | Hypothesis; Formance or TigerBeetle only if volume demands | 10, 16 | S1 | Built | N |
| C55 | Right to erasure across derived copies (search index, caches, extracts, backups) | Tombstones and suppression list (built); reindex on erasure; backup retention window stated; extract tracing | Plan 15.3; `takedown-request.md` | 11 | S1 | Partly (index and backups not covered) | N |

### 3.7 Agents, annotation and operations

| ID | Challenge | Concrete solution | Tool or source | Area | First | Status | Pri |
|---|---|---|---|---|---|---|---|
| C56 | Agent hallucination and prompt injection from fetched pages | Verbatim-evidence rule (built); pages as data; planted-instruction tests; isolation; auditor independent | OWASP Top 10 for LLM Applications [K]; note 04 sections 4 and 6 | 13 | S1 | Partly | N |
| C57 | Agent regressions after a model or prompt change | Versioned prompt bundle; frozen-page regression set; sealed test set; shadow then canary; automatic rollback | Note 04 sections 3 and 5; promptfoo or Inspect AI [K] | 13 | S1 | Not built | N |
| C58 | Agent cost drift | Per-job, day, month caps (built, default zero); cost per verified record; batch API and caching; model routing | Note 04 5.4; `ai-spend-runaway.md` | 13, 7 | S1 | Built (caps) | N |
| C59 | Gold-set label noise and inter-annotator disagreement | Two labelers plus adjudicator; agreement metric; cleanlab-style review of suspicious labels; freeze versions with hash | Krippendorff alpha; Cleanlab (check licence); note 04 3.6 | 12 | S1 | Not built | N |
| C60 | Surveyor drift and fatigue | Rotating canaries (built), accuracy scorecards, suspension, retraining | Plan 14; `volunteers` app (built) | 12 | S1 | Built | P |
| C61 | Observability cost and cardinality at scale | Metric label limits, sampling, tiered log retention, per-host budgets | Prometheus, Loki, OpenTelemetry | 7 | S3 | Not built | L |
| C62 | Incidents with a tiny team | Severity levels, runbooks (12 exist), blameless notes in `docs/incidents/`, quarterly game days, error budgets | Google SRE book [K] | 7 | S1 | Partly (runbooks, no incident notes) | N |

**Count:** 62 challenges. "N" (needed now): 36; "P" (plan ahead): 19; "L" (later): 7. The 15 that most change schema or process before the first million rows: C01, C03, C04, C05, C06, C07, C08, C16, C17, C18, C19, C21, C25, C26, C55.

---

## 4. Claude-skills plan (`.claude/skills/<name>/SKILL.md`)

### 4.1 Current skills [R]

`alllists-rules` (standing rules), `ai-auditor`, `list-filing`, `research-note`, `steward`, `depth-and-scale` (the umbrella: Hotels logic, depth, facets, arithmetic, hybrid storage, no hot spots, URLs, open source first, keep learning).

**Gap:** `depth-and-scale` is one page of nine rules. It tells Claude *what* to respect but not *how* to do taxonomy mapping, entity resolution, migrations or search tuning. Narrow skills fix that. The umbrella should keep a table of links to them.

### 4.2 Authoring rules for every new skill [H]

1. File: `.claude/skills/<name>/SKILL.md` with front matter `name` and `description`. The description is the trigger: say what it is and finish with "Use when ...". Keep it one or two sentences.
2. Keep SKILL.md under about 60 lines. Put long material in a sibling `reference.md` or in `research_notes/` and link it.
3. Each skill lists the challenge IDs (C01 to C62) it covers and the research note it rests on.
4. Each skill ends with a "Done when" check (a test, a number or a file) and an "Escalate to founder" line (what is genuinely their decision).
5. Test each skill with the `skill-creator` evaluation flow (should trigger on 5 sample tasks, should not trigger on 5 unrelated tasks) before it is relied on.
6. Never put secrets, real contact values or non-public data in a skill.
7. Update the skill in the same pull request as any incident fix that taught something (see section 5).

### 4.3 Wave 1: before the founder asks to go beyond the prototype

| Skill | One-line purpose | Trigger (the `description` should say) | Covers | Rests on |
|---|---|---|---|---|
| `taxonomy-depth` | Build and change list-type trees to full depth with stable IDs, facets and crosswalks | Use when adding or changing list types, product trees, categories, synonyms, crosswalks to Overture, Foursquare, ISIC, UNSPSC, HS or GPC, or manufacturing subtrees | C06, C07, C08, C09 | `01_manufacturing_depth_taxonomy.md`, D-01 to D-05 |
| `entity-resolution` | Decide, calibrate, merge and unmerge duplicate entries safely | Use when touching duplicate detection, merge or unmerge, blocking keys, thresholds, transliteration folding, branch versus chain, or the labelled pair set | C01 to C05 | `intake/dedupe.py`, plan 7.3 and 7.4 |
| `scale-migrations` | Change schema and backfill 100M rows without downtime | Use when writing a migration, adding an index or constraint, backfilling, partitioning, or changing a large table | C16 to C20, C22, C23 | `03_hosting_and_costs.md`, section 3.2 here |
| `large-scale-data` | Do the arithmetic and choose the pattern before any large load, query or table | Use when a task involves more than about 1 million rows, a new table, a bulk load, a report over many rows, or a cost, restore-time or lock-time question | C11, C14, C15, C21, C25, C26 | `03_hosting_and_costs.md`, `depth-and-scale` rule 4 |
| `open-source-check` | Check licence, maintenance and fit before building or adding a dependency | Use before adding a package, copying code, choosing a tool, or building something that a maintained project may already do | all | `REUSE_AND_TOOLS.md`, D-13 |

### 4.4 Wave 2: with the first real audience and agents

| Skill | One-line purpose | Trigger | Covers | Rests on |
|---|---|---|---|---|
| `search-relevance` | Tune and evaluate search with judgement lists and metrics | Use when changing search code, synonyms, ranking, paid slots, facets, the search engine adapter, or when search quality or latency is discussed | C28 to C35, C27 | plan 10.1, section 2.5 |
| `seo-at-scale` | Keep millions of pages indexable, useful and not spam | Use when touching URLs, sitemaps, canonicals, noindex rules, templates for indexable pages, structured data, or indexing reports | C10, C36 to C38, C42 | plan 8.6, Google spam policies ([S] S8) |
| `trust-and-safety` | Design checks, risk scoring and policies against fake listings and abuse | Use when working on claims, verification, fake supplier detection, reviews, reports, takedowns, KYB, sanctions, account abuse or contributor credit | C43 to C50, C13 | plan 6, 15 |
| `agent-evals` | Run the gold-set, versioning, shadow and canary loop for agents | Use when changing an agent prompt, model id, few-shot examples, parser, or when asked about agent accuracy or cost | C56 to C59 | note 04 sections 3 to 5 |
| `annotation-ops` | Run surveyors, volunteers and gold questions with measured agreement | Use when designing tasks, guidelines, canaries, scorecards, or measuring human label quality | C59, C60, C48 | note 04, plan 14 |

### 4.5 Wave 3: before money, messaging and scale

| Skill | One-line purpose | Trigger | Covers | Rests on |
|---|---|---|---|---|
| `payments-and-tax` | Keep the ledger exact and tax correct across countries | Use when touching orders, ledger, payouts, invoices, tax lines, currencies, refunds, provider adapters | C51 to C54 | plan 12 |
| `legal-privacy-gate` | Stop work that needs counsel and keep the source and consent records straight | Use before importing a new source, handling people, children or health data, messaging, erasure, or a new country switch | C26, C49, C55 | plan 17, `DECISIONS.md` section 9 |
| `geo-and-addresses` | Handle places, pins, geocoding and informal addresses | Use when touching the place tree, geocoding, nearest-place, pins, polygons, address parsing | C12 | plan 5, 7.5 |
| `incident-response` | Run an incident and write the note that updates the skills | Use when something is down, leaking, wrong at scale, or a runbook is used | C62, C22 | `docs/runbooks/`, section 5 here |
| `product-analytics` | Define metrics, events and experiments that answer the two tests (usage and revenue) | Use when adding events, dashboards, metrics, or experiments | C29, C30 | plan 10, `analytics/events.py` |
| `security-baseline` | Apply the web, secrets and fetcher security checklist at every phase | Use when touching auth, fetcher, forms, headers, secrets, dependencies, or before a phase pull request | C39, C41, C47 | plan 17, `steward` |
| `logic-and-invariants` | Write the rule, the property test and the mutation check together | Use when adding a rule-heavy feature (state machine, consent, money, merge) or when a defect shows a missing invariant | C54, C19 | `scripts/mutation_check.py`, section 2.17 |

### 4.6 Build order and effort [H]

| Order | Skills | Effort | Gate |
|---|---|---|---|
| 1 | `taxonomy-depth`, `scale-migrations`, `large-scale-data` | one session each, about 1 hour of drafting plus eval | Write before the next schema change |
| 2 | `entity-resolution`, `open-source-check` | one session each | Write before Splink is evaluated |
| 3 | `agent-evals`, `search-relevance`, `trust-and-safety` | one session each | Before first real hosted agent run; before engine decision |
| 4 | `seo-at-scale`, `annotation-ops` | one session each | Before indexing 10,000 pages |
| 5 | Wave 3 | one session each | Each before its gate in section 2.1 |

Founder decision implied: none, unless the founder wants fewer skills. Default is all 17 in this order.

---

## 5. Learning loop

### 5.1 Principle

Every week the project asks "what did we learn that would have changed a decision?" and writes it where the next session will read it. Skills are the memory; the logs are the evidence.

### 5.2 Files and locations

| Purpose | File or folder (existing or proposed) | Cadence | Owner | Notes |
|---|---|---|---|---|
| Capabilities matrix (this file) | `research_notes/Scale research/03_capabilities_and_skills_matrix.md` | Monthly review (first Monday); update version header | Claude prepares, founder signs off section 6 | D-12 |
| Challenge register | Section 3 of this file; split to `research_notes/Scale research/04_challenge_register.md` when it passes 100 rows [H] | Update after every incident, audit or research round | Claude | Keep IDs stable; never reuse |
| Research log | `research_notes/Scale research/research_log.md` (proposed, append-only) | Weekly | Claude | One entry per source opened: date, question, source and what was opened, finding, grade (R, S, K, I, H), action, challenge IDs |
| Decision log | `docs/DECISIONS.md` (build log sections) | At every decision | Claude, founder | Rule 8 of `alllists-rules`; record open-source choices and licences here (D-13) |
| Evals: specs and synthetic fixtures | `backend/agents/tests/` and a proposed `backend/evals/` package (loader, scorer, synthetic fixture) | Every prompt, model, threshold or ranking change | Claude | Per note 04 section 3.6 the **gold set itself is not in git**; it lives in a separate `gold` schema with its own role |
| Search relevance judgements | proposed `backend/evals/search/` (queries and labels, no personal data) | Quarterly refresh | Claude plus native-speaker labelers | NDCG@10 and zero-result rate recorded |
| Entity-resolution labelled pairs | proposed `backend/evals/dedupe/` (500 pairs from pilot) | After each threshold change | Claude plus reviewer | Precision and recall written to the decision log |
| Daily and weekly audit reports | AI auditor output (design in note 04 section 6.7); weekly roll-up copied into `reports/` or `research_notes/Scale research/audits/` [H] | Daily and weekly | AI auditor, human reads | Drift versus last week |
| Post-incident notes | `docs/incidents/YYYY-MM-DD-short-title.md` (proposed) | Within 3 working days of any incident or near miss | Whoever ran the incident, Claude drafts | Template below |
| Runbooks | `docs/runbooks/` (12 exist) | Update on every incident that used one | Claude | Each alert links its runbook |
| Skills | `.claude/skills/` | Update in the same pull request as the lesson | Claude | Skill file has "Last lesson: date and link" line [H] |
| Competence log | `research_notes/Scale research/competence_log.md` (proposed) | Monthly, with the review | Claude | Date, area, test from section 2, result, next test date |
| Open questions | `research_notes/Scale research/open_questions.md` or section 6 below | Weekly | Claude | Things marked UNVERIFIED that need opening |

### 5.3 Entry templates

**Research log entry** [H]

```
## 2026-MM-DD  <short question>
- Question: ...
- Opened: <URL or repo and which file>   (say "search summary only" if not opened)
- Finding: ... (grade R / S / K / I / H)
- Changes: <challenge IDs touched, skills to update, decision to log>
- Next: <what to verify, by whom>
```

**Post-incident note** [H]

```
# <date> <title>   Severity: S1..S4   Duration: ...
- What happened (facts, times)
- Detection: how, how long
- Impact: records, money, people (no personal data in the note)
- Cause and contributing factors (no blame)
- What worked
- Fix now / fix later (with owner and date)
- Challenge IDs added or changed; skills and runbooks updated; tests added
```

### 5.4 Weekly and monthly rhythm [H]

| When | What | Output |
|---|---|---|
| Weekly (any day) | Research round of 1 to 3 questions from the open-questions list; open each source; update log | `research_log.md` entries |
| Weekly | Audit and eval digest: accuracy, cost per verified record, zero-result rate, NDCG, indexation, incidents | Short block in `reports/` or log |
| After any incident | Post-incident note within 3 working days; update runbook, skill, challenge register | `docs/incidents/` |
| Monthly (first Monday) | Review this matrix: re-rank gaps, mark competence tests run, add or retire challenges, check skills against lessons | Version bump and a line in `docs/DECISIONS.md` |
| Quarterly | Game day (restore, scraper surge, indexing drop), re-sealed gold set refresh, source terms re-check, pen-test or review plan | Notes in `docs/incidents/` or log |
| Each stage gate (S1 to S4) | Re-run capacity arithmetic against measurements; confirm hire triggers | Update `03_hosting_and_costs.md` or successor |

A scheduled routine (monthly, plus a weekly nudge) can open the review session automatically. Creating it is a founder-approved action because it fires without a person present; see section 6, item 6.

---

## 6. Gaps, conflicts and open decisions (with suggested defaults)

**Gaps and conflicts I found [R unless noted]**

1. Stored lists conflict: founder choice E27 versus D-06 hybrid. Default hybrid is already adopted; the code still creates rows for all types (`generate_lists`), guarded by `--confirm-large`.
2. The plan (3.1.2, 5.2) says lists are "computed, never pre-created" while the decision log says stored rows. Documents disagree; the founder's later decision wins.
3. `PlaceList` has no `country_code` and cannot be partitioned like entries (`03_hosting_and_costs.md` section 11, item 2).
4. The plan's Splink adoption is at S2; calibration data (500 labelled pairs) does not exist yet.
5. No competence tests have ever been run; all test descriptions in section 2 are proposals [H].
6. External facts (Splink version 4, AutoKnow, AliCoCo, DSA article 30, EU VAT, Google spam policies, Overture sources) are from search summaries only. The crawler and bot-traffic claims came from weak, partly promotional sources.
7. Repository facts (licences, activity) could not be checked in this session because GitHub access to those repositories was refused.

**Open decisions for the founder**

| # | Decision | Suggested default |
|---|---|---|
| 1 | Approve the 16-area matrix and the monthly review as a standing process (D-12) | Yes; first review 2026-11-06 |
| 2 | Approve writing the 17 new skills in the order of section 4.6 | Yes, Wave 1 next |
| 3 | First hire or contractor | A part-time Postgres and security reviewer at the S1 to S2 boundary; no full-time hire before a trigger |
| 4 | Annotation model beyond volunteers | Volunteers plus paid panel only for gold-set labelling; decide after the 1,000-record pilot |
| 5 | AI crawler policy | Allow search crawlers; challenge unverified bots; decide AI-crawler licensing after traffic exists |
| 6 | Scheduled routine for monthly review and weekly research nudge | Yes; Claude creates it when the founder says so |
| 7 | Allow Claude to attach third-party repositories read-only (via `add_repo`) to verify licences before adoption | Yes, read-only |
| 8 | Evaluation harness | Own thin runner for gold sets plus promptfoo or Inspect AI for ad hoc comparisons; licences checked first |
| 9 | KYB and sanctions provider | Decide at the bake-off with the payment provider; manual checks until then |
| 10 | Counsel budget | Book hours before the first messaging test, individuals list or payout (already in the decision log) |

**First 30 days learning plan [H]**

| Week | Focus | Output |
|---|---|---|
| 1 | Verify repository licences for Splink, pgroll, Meilisearch, OpenSearch, Label Studio, promptfoo, Inspect AI; write the three Wave 1 skills (`taxonomy-depth`, `scale-migrations`, `large-scale-data`) | Research log entries; three skills |
| 2 | Build the 500-pair labelled set plan; write `entity-resolution` and `open-source-check` | Pairs plan; two skills |
| 3 | Rehearse a 1M-row backfill and a no-downtime column change on a copy; record timings | Competence log entries |
| 4 | Judgement-list pilot (200 queries); first monthly review of this matrix | Version 2 of this file |

---

## 7. Sources

Web searches (standard mode, 2026-10-06). **Summaries only; no page was opened; all UNVERIFIED.**

| ID | Topic | Result pages named in the summary |
|---|---|---|
| S1 | Splink record linkage (version 4, scale claims) | [Splink: fast, accurate and scalable record linkage (UK government blog)](https://dataingovernment.blog.gov.uk/2022/09/23/splink-fast-accurate-and-scalable-record-linkage/); [Splink: latest developments (IJPDS)](https://ijpds.org/index.php/ijpds/article/view/2245); [Deduplicating and linking large datasets using Splink](https://realworlddatascience.net/case-studies/posts/2023/11/22/splink.html) |
| S2 | Zero-downtime Postgres migrations (pgroll, expand and contract) | [Introducing pgroll (Xata)](https://xata.io/blog/pgroll-schema-migrations-postgres); [pgroll 0.7.0 update](https://xata.io/blog/pgroll-0-7-0-update) |
| S3 | Amazon duplicate and ASIN matching | [Amazon Seller Central: potential duplicates and split variations](https://sellercentral.amazon.com/gp/help/external/G202105450); [How to fix duplicate Amazon ASIN](https://www.4seller.com/blog/en/article/433-How-to-Fix-Duplicate-Amazon-ASIN) (third-party summaries) |
| S4 | AliCoCo | [arXiv 2003.13230](https://arxiv.org/pdf/2003.13230) |
| S5 | AutoKnow | [Amazon Science page](https://www.amazon.science/publications/autoknow-self-driving-knowledge-collection-for-products-of-thousands-of-types); [arXiv 2006.13473 via alphaxiv](https://alphaxiv.org/abs/2006.13473) |
| S6 | Amazon Shopping Queries Dataset (ESCI) | [arXiv 2206.06588](https://arxiv.org/abs/2206.06588v1); [Amazon Science blog on KDD Cup](https://www.amazon.science/blog/amazon-product-query-competition-draws-more-than-9-200-submissions) |
| S7 | EU Digital Services Act article 30 (trader traceability) | [DSA article 30 text (SpringLex)](https://www.springlex.eu/en/packages/dsa/dsa-regulation/article-30/); [CCPC overview](https://www.ccpc.ie/enforcement-and-regulation/digital/the-digital-services-act) |
| S8 | Google spam policies (scaled content abuse, site reputation abuse) | [Search Engine Journal on spam policy updates](https://searchenginejournal.com/in-depth-look-at-google-spam-policies-updates/511005); [ppc.land: scaled content abuse](https://ppc.land/scaled-content-abuse/) |
| S9 | Overture Maps places, Foursquare data, schema changes | [Overture Places guide](https://docs.overturemaps.org/guides/places); [release notes 2025-09-24](https://docs.overturemaps.org/blog/2025/09/24/release-notes/); [release notes 2026-08-19](https://docs.overturemaps.org/blog/2026/08/19/release-notes/) |
| S10 | EU VAT e-commerce package (marketplace deemed supplier, IOSS, record keeping) | [WCO summary](https://www.wcoomd.org/es-es/media/newsroom/2021/june/the-european-union-introduces-new-value-added-tax-rules-for-e-commerce-from-1-july-202.aspx); [VATCalc summary](https://www.vatcalc.com/eu/eu-e-commerce-vat-package-1-july-2021/); [Avalara summary](https://www.avalara.com/blog/en/europe/2021/01/2021-eu-marketplaces-vat-deemed-supplier.html) |
| S11 | Cloudflare AI crawler verification and pay-per-crawl; bot share of traffic | [Cloudflare AI Crawl Control docs](https://developers.cloudflare.com/ai-crawl-control/features/pay-per-crawl/use-pay-per-crawl-as-ai-owner/verify-ai-crawler/); [Search Engine World](https://www.searchengineworld.com/cloudflare-for-seo-a-deep-dive-into-bot-management-ai-crawler-control-and-pay-per-crawl); several blogs (weak) |
| S12 | Faceted search at scale with OpenSearch and Elasticsearch | [AWS re:Post facet navigation series](https://www.repost.aws/articles/AR-Im-_iK0RduCvMTqUwPPZg/thank-goodness-it-s-search-building-faceted-navigation-final-part-5-opensearch-aggregation-best-practices); [Pulse faceted search guide](https://pulse.support/kb/faceted-search-implementation-guide) |
| S13 | Postgres partitioning versus sharding, pg_partman, Citus | [Citus: understanding partitioning and sharding](https://www.citusdata.com/blog/2023/08/04/understanding-partitioning-and-sharding-in-postgres-and-citus/); [Heroku on partitioning large tables](https://www.heroku.com/blog/handling-very-large-tables-in-postgres-using-partitioning) |
| S14 | OWASP Automated Threats, OAT-011 scraping | [OWASP OAT-011](https://owasp.org/www-project-automated-threats-to-web-applications/assets/oats/EN/OAT-011_Scraping) |

GitHub: `gh api` and repository search for third-party repositories returned "GitHub access to this repository is not enabled for this session" or unrelated results. No repository data was verified.

Repository files read [R]: `docs/DECISIONS.md`, `docs/TECHNICAL_PLAN.md` (sections 2, 3, 4.1, 4.3, 7.4 to 7.7, 10, 19.11), `docs/REQUIREMENTS_DEPTH_AND_SCALE.md`, `docs/PROMPT_DEPTH_AND_SCALE.md`, `docs/REUSE_AND_TOOLS.md`, `.claude/skills/*/SKILL.md`, `research_notes/Backend research/03_hosting_and_costs.md` and `04_agent_training_and_ai_auditor.md` (headings and key sections), `backend/requirements.txt`, `backend/core/models.py` (advisory lock grep), directory listings of `backend/`, `scripts/` and `docs/runbooks/`.
