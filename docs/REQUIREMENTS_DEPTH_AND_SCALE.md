# Requirements: maximum depth and very large scale

Added 2026-10-06 on the founder's instruction. These are standing requirements for every part of the project.

## The Hotels logic (the pattern for everything)
A list type exists at every place level: global, country, region or state, city, and business district or area (for example Hotels-Global, Hotels-USA, Hotels-California, Hotels-cities in California, Hotels in one business district). Entries are stored once and appear on every list they belong to. This pattern applies to every list type, including manufacturing.

## Requirements

| ID | Requirement | Priority |
|---|---|---|
| D-01 | **Depth over generalisation.** Every domain is modelled to its full practical depth in a structured tree (sector, industry, product family, product, variant). No catch-all "other manufacturers" lists except as a temporary parent. | P0 |
| D-02 | **Manufacturing goes deeper than services.** Manufacturers of leather goods, surgical goods, orthopaedic and support goods, motorcycles, EVs and EV spare parts each have their own subtree, with thousands of list types in total. Each leaf is a list type that follows the Hotels pattern across places. | P0 |
| D-03 | **Capabilities are facets, not list types.** Process, material, certification, capacity, minimum order, export markets and similar properties are filters on a list, so the tree does not explode. | P0 |
| D-04 | **Many-to-many membership.** One manufacturer attaches to many product nodes (one primary, others secondary). One entry, one record, many lists. | P0 |
| D-05 | **Stable identifiers.** Every node has a permanent ID and slug; renames and merges leave redirects. Crosswalk to HS, ISIC, UNSPSC, GPC and Wikidata codes where licences allow. | P0 |
| D-06 | **Lists exist only where entries exist (decision E28, founder).** An entry has one home place, set by its address (a Lahore company never appears in Islamabad). It counts for that place and every place above it (city, district, state, country, world) and for its product node and every node above it. Empty combinations are never created or shown. Higher levels sum what is below automatically. | P0 |
| D-15 | **Free and paid views.** Free viewers see names with their city. A subscription for a place unlocks, for that place and below, the contact route, exact location, address, social media, website, product categories and page details. A city subscription does not unlock the state above it. | P0 |
| D-07 | **Search and browse at scale.** Faceted browse and search over hundreds of millions of entries with a dedicated search engine introduced at a measured trigger (for example p95 over 500 ms on Postgres). | P1 |
| D-08 | **URL and SEO control at scale.** Sitemaps sharded by country and level; facet pages canonicalised or noindexed; thin and empty pages unpublished; indexing watch at day 90. | P0 |
| D-09 | **Entity resolution at scale.** Duplicate detection by blocking, script-aware names and geo keys; merge and unmerge with provenance; stable URLs after merges. | P0 |
| D-10 | **Write hot spots removed before scale.** No single global lock or single hash chain on every write; audit chains are per partition. | P1 |
| D-11 | **Capacity plan.** Every stage (10k, 1M, 100M entries) has a stated storage, cost and restore-time target, and the metric that triggers the next stage. | P1 |
| D-12 | **Keep learning.** A research log, decision log, evaluations and post-incident notes are kept in the repository; capabilities and skills required are listed and reviewed each month (`research_notes/Scale research/03_capabilities_and_skills_matrix.md`). | P1 |
| D-13 | **Learn from open source.** Before building a component, check whether a maintained open-source project with a compatible licence solves it; record the choice and licence in the decision log. | P1 |
| D-14 | **Accuracy and prediction.** Every plan states its scale assumptions and arithmetic so later changes cost less; assumptions are re-checked against measurements at each stage. | P0 |

## Resolved conflict
The earlier choice (a stored list for every type at every place) would have reached about 150 billion rows at manufacturing depth. The founder resolved it on 2026-10-06: lists exist only where entries exist, placed by the entry's address, with roll-up to every level above (D-06). The code already works this way (`analytics.RollupCell` holds only non-empty cells).
