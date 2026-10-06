# Scale research: summary (2026-10-06)

Four notes in `research_notes/Scale research/`. All web and GitHub facts are from search snippets or GitHub metadata, not primary pages, unless stated. Sizes and times are arithmetic, not measurements.

## 1. Manufacturing depth taxonomy (`01_*`, seed of 1,170 nodes)
- No outside tree is deep enough (HS 9018 covers all surgical instruments in 13 subheadings; EV chargers, motor controllers and battery management have no HS code). We author our own tree.
- Five levels (sector, industry, family, product, variant), depth 7 absolute cap. One primary parent plus up to 3 secondary parents. A manufacturer has 1 primary and up to 24 secondary products.
- Capabilities are facets, not types (leather gloves would go from 19 products to 27,360 types otherwise).
- Estimate for all manufacturing: about 12,400 nodes at levels 1 to 4, about 52,000 at levels 1 to 5 (range 32,000 to 92,000). The 12 named sectors come to about 24,900 nodes; the seed has 1,059 of them.
- Licences: adopt as text NAICS, HTS, Wikidata labels, Shopify taxonomy (MIT); crosswalk only HS, ISIC, CPC, UNSPSC, GPC, eCl@ss (WCO and UN permissions needed before publishing the codes); look only at IndiaMART and Alibaba trees.

## 2. Big-site architecture (`02_*`)
- Four code problems come first: roll-up recount loads whole cells into Python; the audit lock is held per transaction (bulk publish would take weeks of lock time at 100M); the sitemap is rebuilt on every request; `publish_cap_per_week` is not read.
- A list is a saved filter. Store a roll-up cell only at 25 or more entries (or pinned/indexable): about 144 million cells (43 GB) at largest scale.
- Postgres trigram to about 1M entries, then a search-engine bake-off (OpenSearch default); partition at about 10M entries; outbox table before Kafka; ClickHouse for logs only.
- SEO risk is thin and duplicate pages, not sitemap size. Index a list at its natural scale; empty lists resolve virtually, noindex.
- Open source reuse: Splink, pgBackRest, Patroni, Superset, OpenSearch or Typesense, PeerDB or Debezium, Overture tools. Patterns only: Saleor, Spree, Vendure. Do not copy Sharetribe Go.
- Licence conflicts: Overture divisions may be ODbL (derived from OpenStreetMap); Typesense, Citus, ParadeDB, Nominatim are GPL or AGPL.

## 3. Capabilities and skills (`03_*`)
- 16 capability areas with levels at 10k, 1M and 100M entries; 62 challenges with solutions; 17 new skills in three waves (wave 1: taxonomy-depth, entity-resolution, scale-migrations, large-scale-data, open-source-check); learning loop with weekly research log, monthly matrix review (first due 2026-11-06), evals, incident notes.
- Default first hire: part-time Postgres and security reviewer at the S1 to S2 boundary.

## 4. Entity resolution and data quality (`04_*`)
- Current dedupe fits a pilot and breaks above about 1M entries per country. Four defects: phone hash includes the contact kind; shared-phone plus 0.5 name similarity auto-merges with no cap; merge drops categories, verification, claims and consent with no undo; auto-merge outcomes are never recorded.
- Resolve in staging before entries exist; exact keys, then Splink (MIT), then people for the narrow band; auto-merge only at p >= 0.995 plus two strong agreements.
- Replace the unused category M2M with an `entry_concept` table (role, evidence, confidence, place path); about 48 GB at 3 memberships per entry.
- Freshness on the current rule would cost USD 6 to 20 million a year at 100M entries; tiered change-detecting schedule USD 0.8 to 2.7 million. Human review is over 99% of cleaning cost.

## Decisions adopted by default (founder may change)
1. E28 stands: lists exist only where entries exist; empty (place, type) pages resolve virtually, noindex, link to the nearest populated lists.
2. Store threshold: 25 members, 10 verified, or pinned.
3. Build our own manufacturing tree; staff approve new nodes, agents propose with three independent evidences.
4. No HS or ISIC codes are published until written WCO and UN permission.
5. Overture divisions treated as share-alike until checked; place tree from GeoNames plus Overture Places only.
6. "Return to draft after the grace period" applies to the two highest tiers of entries only.
7. Counsel to confirm unmodified GPL and AGPL services are acceptable.

## Code work this implies (not started)
Fix recount, audit-lock and sitemap hot spots; per-partition audit chain; `entry_concept` table and multi-parent concepts with slug history; staged entity resolution; calibrate dedupe thresholds; add Splink and a migration linter.
