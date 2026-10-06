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
| D-06 | **Stored-list budget.** Lists for deep types are not all stored at every place. A list is stored at a place level when the type is above a depth threshold or when an entry exists there; below that it is resolved virtually so the list still "exists everywhere". The hybrid rule and thresholds are set from the row-count arithmetic in the scale research. | P0 |
| D-07 | **Search and browse at scale.** Faceted browse and search over hundreds of millions of entries with a dedicated search engine introduced at a measured trigger (for example p95 over 500 ms on Postgres). | P1 |
| D-08 | **URL and SEO control at scale.** Sitemaps sharded by country and level; facet pages canonicalised or noindexed; thin and empty pages unpublished; indexing watch at day 90. | P0 |
| D-09 | **Entity resolution at scale.** Duplicate detection by blocking, script-aware names and geo keys; merge and unmerge with provenance; stable URLs after merges. | P0 |
| D-10 | **Write hot spots removed before scale.** No single global lock or single hash chain on every write; audit chains are per partition. | P1 |
| D-11 | **Capacity plan.** Every stage (10k, 1M, 100M entries) has a stated storage, cost and restore-time target, and the metric that triggers the next stage. | P1 |
| D-12 | **Keep learning.** A research log, decision log, evaluations and post-incident notes are kept in the repository; capabilities and skills required are listed and reviewed each month (`research_notes/Scale research/03_capabilities_and_skills_matrix.md`). | P1 |
| D-13 | **Learn from open source.** Before building a component, check whether a maintained open-source project with a compatible licence solves it; record the choice and licence in the decision log. | P1 |
| D-14 | **Accuracy and prediction.** Every plan states its scale assumptions and arithmetic so later changes cost less; assumptions are re-checked against measurements at each stage. | P0 |

## Known conflict to resolve (flagged to the founder)
The founder's earlier choice stores a real list row for every list type at every place. At 100,000 list types and 1.5 million places that would be 150 billion rows, so it cannot hold once manufacturing depth is added. Default adopted until the founder decides: hybrid storage (D-06). Research: `research_notes/Scale research/01_manufacturing_depth_taxonomy.md`.
