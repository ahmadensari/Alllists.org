---
name: depth-and-scale
description: AllLists.com rules for taxonomy depth and very large scale. Use when designing list types, product trees, manufacturing lists, schemas, search, sitemaps, migrations or anything that must work at hundreds of millions of entries.
---

# Depth and scale

Read `docs/REQUIREMENTS_DEPTH_AND_SCALE.md` first (requirements D-01 to D-14) and `research_notes/Scale research/`.

1. **Hotels logic everywhere:** a list type exists at global, country, region, city and business-district level; entries stored once; many-to-many membership.
2. **Depth, not generalisation:** model each domain to leaf level (sector, industry, product family, product, variant). Manufacturing goes deepest (leather goods, surgical goods, orthopaedic and support goods, motorcycles, EVs, EV spare parts).
3. **Facets, not types:** process, material, certification, capacity, minimum order, export markets are filters.
4. **State the scale and show arithmetic** before any design: rows, bytes per row, cost, restore time, lock time. Compare with the stage table in `research_notes/Backend research/03_hosting_and_costs.md`.
5. **Stored lists are hybrid:** store a list at a place when the type is above the depth threshold or an entry exists; resolve the rest virtually. Never run `generate_lists` unscoped; use `--levels` or `--country`.
6. **No global write hot spots:** avoid single locks or single hash chains on every write.
7. **URLs:** sharded sitemaps, facets canonicalised or noindexed, empty pages unpublished.
8. **Open source first:** check for a maintained, compatible-licence project before building; log licence and choice in `docs/DECISIONS.md`.
9. **Keep learning:** update the capabilities and skills matrix and the challenge register when you learn something; write post-incident notes.
