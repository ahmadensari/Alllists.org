# 07 Search and ranking solutions

Date: 2026-10-08. Status: research note, no code changed. English only.
Inputs: saved results in `research_notes/Scale research/benchmarks/results/`, scripts in `benchmarks/`, notes 02 and 03 of this folder, and `backend/catalog/search.py`, `search_backend.py`, `queries.py`.
Challenges covered: C10 (facets), C27 (index sync), C28 (fairness), C29 (cold start), C30 (position bias), C31 (evaluation), C32 (zero results, typos, Roman Urdu), C33 (unscoped cost), C34 (blended results), C35 (autocomplete).

Grades: **M** measured in the saved files (this note quotes them, nothing was re-run); **R/S** from note 02 (not re-opened here, UNVERIFIED unless note 02 says otherwise); **I** inference (inputs stated); **H** hypothesis or design judgement.

## 0. Rules of this note

- No database server was started and no new benchmark was run. Every Postgres number below is read from a saved file.
- Where a run was aborted or never produced a file, the gap is written down. Nothing is filled in.
- Two scripts that need no database server were run: `esci_eval.py --selftest` (section 7). `demo_ranking.py` needs the bench database, so it was **not** run (section 7).

## 1. What was measured and how far to trust it

### 1.1 Set-up (M, from `gen_data.py`, `run_bench.py`, `build_*.json`)

- Synthetic entries, 1,000,000 and 5,000,000 rows (generation of 5M took 42.6 s). Countries weighted pk 55, in 12, ae 8, us 8, sa 7, gb 6, bd 2, tr 2. In Pakistan 45% of names are Latin, 38% Roman Urdu, 17% Urdu script (elsewhere 90 / 5 / 5). Word pairs let the same name exist in two scripts. The Urdu side is "not a reviewed lexicon" (`bench_vocab.py` header).
- PostgreSQL 16, single client, **warm cache**: all 12 relations were pre-warmed into memory (`pg_prewarm`) before timing. `jit = off`. Statement timeout 4,000 ms; a timed-out query is recorded as 4,000 ms with a timeout count.
- Machine: the files do not record CPU, RAM or `shared_buffers` for the bench cluster. The current sandbox shows 4 cores and 15 GB (I; assumed the same machine). Treat all numbers as "small 4-core box, warm cache", not as production.
- Methods: `repo` = a copy of the SQL shape of `ModelBackend.entries()` (the `similarity()` function, OR over a variant subselect, `contains`). `like` = `name_fold LIKE '%q%'` on the pg_trgm GIN index. `tsv` = `to_tsquery('simple', 'a & b:*')` on a stored tsvector GIN, take 200 by stored prior, rerank 25 by word similarity and prior. `tsvrank` = same match ordered by `ts_rank`. `wsim` = pg_trgm word similarity `q <% name` (threshold 0.4). `btree` = prefix `LIKE 'q%'` on a text_pattern_ops btree. `dict` = typo correction by trigram lookup in a word table (69,438 words at 1M, 131,349 at 5M), then `tsv`.
- Scopes: unscoped, country (pk), city, area, city plus list type (1M only), and "nocc" variants without the `country_code` predicate (that is the shape of the real code, which filters on `place_path` only; 1M only).

### 1.2 Completeness of the files (read this before the tables)

| File | State |
|---|---|
| `search_1m.jsonl` / `.log` | Complete: 98 cells (7 scopes), warm run. |
| `search_1m_first_touch.jsonl` | Complete, 98 cells, a second pass over the same cells. Close to the warm run (for example unscoped common `tsv` p50 7.6 ms vs 12.5 ms; city common `tsv` 67.8 vs 60.7 ms). Not used further. |
| `partial_search_1m_first_cells.*`, `aborted_search_1m_run2.*` | **Aborted runs**: 9 cells each (unscoped common/mid only). Not used; they agree with the full run within noise. |
| `aborted_search_5m_first_touch.*` | **Aborted**: 3 cells. Not used. |
| `search_5m.jsonl` | Interrupted: 33 cells. Covers unscoped, country (common, mid, rare). Load average about 1.0 (clean). |
| `search_5m_rest.jsonl` | Interrupted: 16 cells (country two/typo/prefix, city common/mid). The log ends with a **statement-timeout traceback while sampling queries** for the next city cell. Load average 2.2 to 3.8. |
| `search_5m_rest2.jsonl` | Interrupted: 13 cells (city two/typo/prefix, area common, area mid `repo`). The log ends there. Load average 3.1 to **8.2**. |
| 5M coverage | 62 of the 98 cells exist. **Missing at 5M**: area mid/two/typo/prefix, city_concept, city_nocc and area_nocc (all methods). No 5M figure exists for them. |

Load caveat (M): `taxonomy_machine_load_2026-10-07.log` shows other benchmarks (a sitemap job, `pgbench`, a `CREATE TABLE AS`) running on the same 4-core machine at the same time as the later 5M runs. The 5M city and country-typo/prefix figures (`rest`, `rest2`) are therefore **inflated by unknown amounts** and are upper bounds. The unscoped and first country 5M cells (`search_5m.jsonl`) were taken at load 1.0.

Other limits: one client only (no concurrency test); synthetic names with no real query log; 20 to 77 queries per cell (the `repo` cells have only 20 or fewer to 48 because they are slow), so p95 on a cell is a rough figure; the p95 of cells with 20 queries is close to the maximum.

### 1.3 Index sizes and build times (M, `build_*.json`, `post_*.json`)

| Object | 1M size | 1M build | 5M size | 5M build |
|---|---|---|---|---|
| Entry table (heap, without tsvector) | 114 MB | n/a | 612 MB | n/a |
| Entry table with `tsv` column | 163 MB | add column 12.9 s | 874 MB | 56.5 s |
| Primary key | 22 MB | 0.7 s | 112 MB | 2.6 s |
| btree for list queries | 28 MB | 1.8 s | 78 MB | 10.2 s |
| btree name prefix (`text_pattern_ops`) | 29 MB | 0.7 s | 119 MB | 2.4 s |
| **GIN trigram on `name_fold`** | **46 MB** | 5.6 s | **186 MB** | 31.9 s |
| **GIN tsvector** | **14 MB** | 1.8 s | **50 MB** | 9.7 s |
| Partial index on stored prior | 13 MB | 0.3 s | 45 MB | 1.5 s |
| Variant table (heap / btree / trigram GIN) | 12 / 4 / 8 MB | 0.2 + 1.3 s | 57 / 20 / 36 MB | 0.2 + 4.8 s |
| Word table (heap / trigram GIN) | 3.7 / 1.9 MB | 2.5 s | 6.3 / 3.3 MB | 13.4 s |

Sizes in decimal MB. Both text indexes together cost 60 MB at 1M and 236 MB at 5M (about 60 and 47 bytes per row), small next to the heap. Index writes: not measured in this set (`write_cost.py` exists; no saved output was read for this note).

## 2. Postgres search latency

All figures are p50 / p95 in milliseconds, warm cache, one client. "to" = timed out at 4,000 ms. Rows returned are about 25 unless stated. 5M cells marked `*` come from the loaded runs (`rest`, `rest2`) and are upper bounds.

### 2.1 Unscoped (whole table)

| Query | Method | 1M | 5M |
|---|---|---|---|
| Common word | `like` (trigram) | 0.9 / 3.4 | 0.8 / 2.3 |
| Common word | `tsv` + prior | 12.5 / 19.5 | 8.5 / 27.6 |
| Common word | `tsvrank` (`ts_rank`) | 65.9 / 143.9 | 485 / 787 (n=48) |
| Common word | `wsim` | 256 / 654 | 1,103 / 3,466 (n=20) |
| Common word | `repo` shape | 2,752 / 3,276 | all 20 timed out |
| Mid word | `like` | 7.6 / 15.8 | 19.5 / 47.2 |
| Mid word | `tsv` | 7.9 / 91.1 | 101 / 260 |
| Mid word | `tsvrank` | 9.4 / 17.3 | 44.1 / 62.7 |
| Mid word | `repo` | 2,597 / 3,001 | all timed out |
| Rare word | `like` | 1.1 / 1.9 | **all 20 timed out** (cause not investigated) |
| Rare word | `tsv` | 0.25 / 0.5 | 0.46 / 0.79 |
| Two words | `like` | 4.6 / 13.6 | 12 of 20 timed out, rest slow (p50 4,000) |
| Two words | `tsv` | 4.2 / 10.7 | 23.6 / 75.8 |
| Typo (one edit) | `wsim` | 39.7 / 145 (recall 0.81) | 195 / 775 (recall 0.82) |
| Typo | `dict` then `tsv` | 5.1 / 30.3 (recall 0.87) | 4.6 / 33.2 (recall 0.79) |
| Typo | `repo` | 2,644 / 2,975 (recall 0.80) | all timed out (recall 0.0) |
| Autocomplete 2 to 4 letters | `btree` prefix | 3.8 / 11.4 | 5.6 / 62.6 |
| Autocomplete | `like` | 2.0 / 13.9 | 1.6 / 34.2 |
| Autocomplete | `tsv` prefix | 20.2 / 75.8 | 26.8 / 154 |

### 2.2 Country scope (pk)

| Query | Method | 1M | 5M |
|---|---|---|---|
| Common | `like` | 1.8 / 4.0 | 1.5 / 4.6 |
| Common | `tsv` | 17.7 / 30.0 | 22.3 / 40.2 |
| Common | `repo` | 2,046 / 2,496 | all timed out |
| Mid | `like` / `tsv` | 6.1 / 25.6 and 6.2 / 36.8 | 22.2 / 52.2 and 163 / 311 |
| Rare | `like` / `tsv` | 1.0 / 2.6 and 0.4 / 0.7 | 2.4 / 4.8 and 0.5 / 0.8 |
| Two words | `like` / `tsv` | 4.7 / 14.0 and 4.1 / 11.4 | 17.5 / 51.8* and 15.2 / 78.7* |
| Typo | `wsim` | 66.9 / 127 (recall 0.83) | 273 / 833* (recall 0.91) |
| Typo | `dict` | 7.0 / 28.9 (recall 0.83) | 10.0 / 37.8* (recall 0.87) |
| Autocomplete | `btree` / `like` / `tsv` | 4.0 / 28.8, 3.9 / 17.6, 16.6 / 104 | 6.3 / 43.5*, 4.2 / 54.4*, 35.0 / 178* |

### 2.3 City scope (city path plus country predicate) and area scope

| Query | Method | 1M city | 5M city* | 1M area | 5M area* |
|---|---|---|---|---|---|
| Common | `like` | 59 / 109 | 203 / 470 | 61 / 107 | 227 / 565 |
| Common | `tsv` | 61 / 99 | 237 / 424 | 65 / 89 | 240 / 404 |
| Common | `wsim` | 91 / 225 | 462 / 1,392 (n=39) | not run | not run |
| Common | `repo` | 597 / 1,052 | 3,083 / 4,000 (10 of 20 timed out) | 500 / 599 | all but a few timed out (18 of 20) |
| Mid | `like` / `tsv` | 43 / 54 and 45 / 59 | 75 / 209 and 97 / 208 | 47 / 60 and 47 / 60 | not run |
| Two words | `like` / `tsv` | 44 / 59 and 44 / 57 | 23 / 47 and 21 / 72 | 44 / 59 and 46 / 68 | not run |
| Typo | `wsim` | 48 / 86 (recall 0.81) | 181 / 410 (0.94) | 46 / 94 (0.81) | not run |
| Typo | `dict` | 42 / 70 (0.83) | 51 / 195 (0.95) | 20 / 66 (0.88) | not run |
| Autocomplete | `btree` | 9.6 / 46.6 | 45 / 460 (max 3,087) | 25 / 89 | not run |
| Autocomplete | `like` | 65 / 852 | 75 / 3,780 (2 timeouts) | 79 / 959 | not run |
| Autocomplete | `tsv` | 49 / 95 | 60 / 234 | 49 / 84 | not run |
| City plus list type, common (1M) | `like` / `tsv` | 64 / 108 and 63 / 96 | not run | | |

Note: the 5M "two words" city figure is lower than the 1M one because the 5M run drew different sample queries (about 9 rows returned versus 5 at 1M); do not read it as 5M being faster. At 1M the "nocc" cells (the repository's real SQL shape, no country predicate) show the same pattern: `repo` 532 to 641 ms p50, `like` and `tsv` 4 to 44 ms.

### 2.4 Scripts: Latin, Roman Urdu, Urdu (M, field `by_script_p50_p95_n`)

Because the Pakistan mix is 45 / 38 / 17, Urdu-script queries exist only in country, city and area cells and they are few (10 to 14 per cell).

| Cell | Latin p50 / p95 | Roman Urdu p50 / p95 | Urdu script p50 / p95 |
|---|---|---|---|
| 1M country, typo, `dict` | 7.3 / 29.5 (n=38) | 5.9 / 23.3 (n=26) | 11.6 / 24.6 (n=13) |
| 1M country, typo, `wsim` | 71 / 142 | 64 / 107 | 57 / 74 |
| 1M country, prefix, `btree` | 9.2 / 29.6 | 2.3 / 10.9 | 2.5 / 36.6 (n=11) |
| 1M city, prefix, `btree` | 12.0 / 49.7 | 1.2 / 49.7 | 1.4 / 18.4 (n=10) |
| 5M* country, typo, `dict` | 9.1 / 26.7 | 9.0 / 46.4 | 19.2 / 49.8 (n=14) |
| 5M* country, prefix, `tsv` | 65 / 190 | 30 / 96 | 11.6 / 134 (n=14) |
| 5M* city, typo, `dict` | 52 / 199 | 31 / 151 | 31 / 183 (n=11) |

Reading (I): on this synthetic data the three scripts behave alike with the same methods, because trigrams and the `simple` text configuration are script-agnostic. This says nothing about **language quality**: the data has no real Urdu spelling variation (alef/hamza forms, joined or split words, Arabic versus Urdu letters), no Roman Urdu spelling variants (`mohammad / muhammad / mohammed`), and no transliteration matches across scripts beyond the stored variant rows. Those need the native-speaker judgement set (section 7). H: `simple` tokenising of Urdu needs a fold step (the project's `fold()` in `core/textfold`) and an explicit normalisation test list before any claim of Urdu support.

### 2.5 What the numbers say

1. **The repository's current entry query shape is the problem, not Postgres.** `ModelBackend.entries()` uses `similarity()` as a function, `OR`, a variant subselect and a `contains`. That blocks the trigram index (the saved plans show a sequential scan with a hashed subplan). At 1M it costs 2.0 to 3.3 s at country or unscoped level and **0.5 to 0.64 s p50 (p95 0.6 to 1.05 s) at city and area level**. At 5M it times out at 4 s in most cells. Search results are only requested with a scope (`search.run()` scans entries only when `scope_place` is set), so the live exposure is the city and area rows: already above the plan's S3 gate of 500 ms at 1M.
2. **A rewrite with the same Postgres removes most of it at 1M and 5M.** `tsv` + stored prior (200 candidates, rerank 25) is 4 to 65 ms p50 at 1M for every scope, and p95 under 125 ms. At 5M, unscoped and country p95 are under 310 ms; city and area common words reach p95 about 400 to 565 ms under load (upper bound).
3. **`ts_rank` order is not usable at scale** (BS-11 in note 02 is confirmed): common word, unscoped, 66 ms p50 at 1M, 485 ms at 5M. Order by the stored prior and rerank a small candidate set instead.
4. **Trigram word similarity (`wsim`) is the expensive part of typo handling**: 195 ms p50 and 775 ms p95 unscoped at 5M. The word-dictionary method (`dict`) is 5 ms p50 and 33 ms p95 and has similar recall (0.79 to 0.95 depending on cell). The word table is tiny (3 to 6 MB heap).
5. **Typo recall is about 0.8 to 0.95 in the top 25** (the share of typo queries whose source entry is in the top 25); one in six to one in five typos still fail. Treat 0.87 as the figure to beat.
6. **Prefix autocomplete**: the btree prefix index is the best choice (p50 under 10 ms except city scope at 5M, p95 up to 460 ms under load). The `like` (trigram) route for 2 to 4 letter prefixes has a bad tail at city scope (p95 850 to 960 ms at 1M; 3,780 ms at 5M with timeouts). Do not use trigram `like` for prefixes.
7. **Odd cells to investigate before relying on them (M, cause unknown)**: 5M unscoped rare-word `like` and two-word `like` time out although `tsv` answers in under 80 ms. Likely a planner choice between the prior index and the trigram index; no EXPLAIN comparison was done at 5M in the files read. Do not generalise.

## 3. When to move to a search engine (trigger point)

Plan trigger from note 02 and the matrix: p95 over 500 ms or zero-result rate over 15% at the S3 gate (plan 3.5 and 10.1).

Our reading of the data (H, based on section 2):

| ID | Trigger | Evidence now | Action |
|---|---|---|---|
| ST-1 | Entry search inside a place scope has p95 > 500 ms on the **rewritten** query | Not met at 1M. At 5M city common word 404 to 565 ms under load, so borderline | Re-measure on production hardware, clean machine, concurrency 20 |
| ST-2 | Whole table fuzzy search wanted (no scope) | `dict` route is fine to 5M (p95 33 ms) | No engine needed for this |
| ST-3 | Zero-result rate > 15% after synonym and Roman Urdu table work | No query log exists yet | Measure with the weekly review (C32) |
| ST-4 | Live facet counts over a large scope are needed on every page | Not measured (section 8) | Engine aggregations, or keep precomputed counts |
| ST-5 | A single table passes about 5 to 10 million entries per search node, or index writes slow the main database | 5M table 874 MB, indexes 236 MB: still fits memory on a modest node (I) | Plan the bake-off at 3 to 5 million entries; do not wait for 10 million |
| ST-6 | Fix the `ModelBackend.entries()` query first | Current shape already above 500 ms at city scope at 1M | **Do this before any engine work** (the saved plans show why) |

Our default (H): rewrite the Postgres query (ST-6) now, re-test, and run the bake-off when ST-1 or ST-5 is hit, which at the current growth plan is S3. Adding an engine earlier would cost operations work for a problem that a query rewrite fixes.

## 4. Engine bake-off: OpenSearch vs Typesense vs Meilisearch

### 4.1 Was any engine test run?

**No engine result file exists.** `benchmarks/engine_bakeoff.py` and `run_engines.sh` were written (versions named in the script: Meilisearch v1.54.3, Typesense 30.2, OpenSearch 3.9.0, binaries taken from the vendors' public images; OpenSearch with a 3 GB heap, security off), and the script is set up to load 1M documents and compare p50 and p95 on the same queries, plus RSS and disk. But no `engine_queries_1m.json`, no per-engine result and no log was found under `benchmarks/results/` or elsewhere on disk. **State for the founder: the engine bake-off was not run, or its output was lost. Nothing about engine latency, RAM or disk is measured.** Every engine statement below is a note 02 figure (R/S, not re-opened in this session) or a design judgement.

### 4.2 Comparison on what is known

| Point | OpenSearch | Typesense | Meilisearch |
|---|---|---|---|
| Licence (note 02) | Apache-2.0 | GPL-3.0 (server). Calling it over HTTP does not make our code GPL (our judgement; counsel to confirm) | Community MIT; Enterprise BUSL |
| Scale shape | Sharded and replicated. 10 to 50 GB per shard guidance | Whole index in RAM; high-availability clusters replicate, not shard (UNVERIFIED) | Community is one node; sharding is Enterprise only |
| RAM at 100M documents (note 02, I) | 30 GB raw, 90 to 150 GB indexed, 3 to 10 primary shards. Heap and page-cache sizing not estimated: **to measure** | 60 to 90 GB per node (2 to 3 times searchable data). "3 nodes of 64 GB" in the hosting note is too small if so | Not estimated in note 02. One node must hold it: **to measure** |
| Faceting | Aggregations, mature; heavy facets need care (eager global ordinals) | Built-in `facet_by` | Built-in facets |
| Geo | Geo points and shapes (UNVERIFIED-M) | Geosearch built in | Geosearch built in |
| Urdu analysis | Custom analyzer chain is possible: `arabic_normalization`, `persian_normalization` filters (the bake-off script uses them). ICU plugin not tested | Per-field locale setting; Urdu support **not verified** | Language detection and tokenisation for Arabic script **not verified** |
| Typo tolerance | Fuzzy queries, suggesters; tuning needed | Strong default (`num_typos`, prefix) | Strong default |
| Cost remark | Cloud cost not studied | Cloud cost not studied | Cloud overage about USD 20,000 a month at 100M documents (hosting note, UNVERIFIED) |
| Default (note 02) | Default candidate | Single-node alternative | Fine to about 10M on one node |

### 4.3 Bake-off protocol (H; to be run at the S3 gate, not now)

1. **Data**: the real field shapes, 10 million documents first, then extrapolate memory and disk to 100 million and mark the extrapolation I (note 02 asks for a pass at 3 times the 100M projection). Fields: name, aliases, three scripts, country, place ancestors, concept ancestors, level, score, verified age, closed, geo point.
2. **Queries**: the same sets used here (common, mid, rare, two words, typo, prefix; unscoped, country, city, list) plus the judgement list (section 7) for quality, plus 5-facet list queries. Include 500 real Urdu and Roman Urdu queries from the native-speaker set.
3. **Measure per engine**: index build time; docs per second at ingest; query p50 and p95 at concurrency 1, 10 and 50; RSS and disk after index and after queries; behaviour during a full reindex and during an alias swap; restart and recovery time; time to add a node; memory per 1M documents; monthly cost at the three sizes on managed or self-hosted.
4. **Quality**: NDCG@10 on the judgement set with the same ranking formula expressed in each engine (section 6). Typo recall at 25. Urdu normalisation cases written by a native speaker (alef forms, hamza, ya/ye, kaf/kaaf, zero-width joiner, digits).
5. **Pass rule** (note 02): the cheapest engine that passes at 3 times the expected 100M projection with p95 under 150 ms for scoped and 300 ms for unscoped fuzzy queries, and typo recall at 25 not below the Postgres `dict` figure (0.87).
6. **Gates**: the existing contract tests must pass unchanged (section 9: `test_search.py` today; a contract suite for backends is planned). A sixth candidate, `pg_search` (AGPL), only if the host allows extensions.
7. **Scale model**: one index per country group plus a global alias (note 02); shards sized 10 to 50 GB.

## 5. Facet design (C10)

Measured: **nothing**. `bench_facets.py` exists (live `GROUP BY` of level and script counts versus a precomputed JSON cell, at 1M and 5M) but there is no saved output. Do not quote facet timings from this note.

Design (H, from note 02 section 3.3 and the C10 row):

- Facets are filters, not list types (D-03). A facet value is a field on the search document. It never creates a page.
- Facet fields: check level, script/name language, completeness bucket, opening-hours open now, distance band, price band, list-type specific attributes (allowlist per type).
- Counts: large cells from the roll-up store with "as of" time; small cells (under about 1,000 entries in scope, I) live. Top 20 values per facet. No precomputed cross product.
- URLs: filters are query parameters, sorted, canonical, `noindex` (built in `seo.py`), blocked in `robots.txt`. A small allowlist of indexable combinations (for example "verified only" on big lists) is decided per list type.
- Page weight: plain links, not a script widget (11 KB budget).
- Cache: facet queries cached by scope + sorted filters for 60 s.
- Acceptance: see section 9.

## 6. Ranking design (C28 to C30, C34)

Everything here is a design (H). No ranking code beyond the alphabetical default list order and the labelled paid slots exists.

### 6.1 Pipeline

1. **Retrieve** candidates: text match (folded name plus aliases plus variants) inside the scope, up to 200 (this is the measured `tsv` pattern in section 2).
2. **Score** with fixed weights (no learning at first).
3. **Group** results by type: list types, places, entries, with caps per group (C34). One blended score only after evaluation shows it helps.
4. **Insert** labelled paid slots outside the organic list.

### 6.2 Score parts

`score = text * (a + b * prior)` style products beat plain sums in the only comparison available (`demo_ranking.py` includes `product` and `blend_add`; no saved output, so this is not a finding). Start with:

| Part | Meaning | Rule |
|---|---|---|
| Text relevance | Exact name > prefix > word match > fuzzy; alias and script variant count as the name | Must pass a floor; fuzzy matches below the floor are dropped |
| Quality prior (stored `static_score`) | Completeness, name quality, source count, contact present, photo present | Computed at write time and indexed (partial index 13 MB at 1M, 45 MB at 5M, M) |
| Verification level | Surveyor-verified and Owner-verified above AI-checked above Not verified yet | Fixed step, not a weight tuned on clicks. Expired verification counts as lower |
| Freshness | `exp(-age_days / 365)` of the last check; closed or stale beyond a limit goes to the bottom or is hidden | Closed or unpublished are never shown (label I) |
| Place fit | Exact place > child area > parent | Distance sort only on request (PostGIS, S2) |
| Paid | **Not a ranking feature.** Placements are separate labelled slots (built: `access/placements.py`) | Organic order independent of payment; a "How this list is ordered" page; exposure audit by seller size, country and new versus old |

### 6.3 Cold start (C29)

- New entries get the prior only from their data quality (no clicks needed).
- A time-boxed boost (for example 14 days) for entries that are verified and new, and a small exploration share (for example 1 slot in 10 on page 1, chosen from new verified entries, labelled in the audit not on the page). Share and length are our guesses to tune (H).
- No boost for unverified new entries.

### 6.4 Position bias (C30)

- Until there is click data, nothing to correct. Do not train on clicks yet.
- When there is: a small randomised bucket (swap adjacent positions for 1% of sessions), inverse propensity weighting from that bucket, and interleaving for A/B tests. Enquiry events (the closed catalogue in `analytics/events.py`) are better signals than clicks. Learning to rank only after judgements and enquiry data exist.

### 6.5 Requirements table

| ID | Requirement | Priority | State (repo check) |
|---|---|---|---|
| RK-1 | Entry search query that uses the trigram or text index (no `similarity()` function in the filter) | P0 | Not built (`ModelBackend.entries()` uses the slow shape) |
| RK-2 | Stored quality prior column and index | P0 | Not built (no `static_score` in `backend/`) |
| RK-3 | Ranking uses text, prior, verification level, freshness with fixed weights | P1 | Not built (alphabetical and by checked date only, `queries.list_rows_queryset`) |
| RK-4 | Paid slots separate and labelled | P0 | Built (`access/placements.py`) |
| RK-5 | Organic order independent of payment, with tests | P0 | Partly (separation by design; no exposure audit) |
| RK-6 | "How this list is ordered" page | P1 | Not built |
| RK-7 | Cold-start boost and exploration share | P2 | Not built |
| RK-8 | Click and enquiry log with a randomised bucket for position bias | P2 | Not built |
| RK-9 | Grouped results with caps per group | P1 | Built (concepts, places, entries groups in `search.run`); caps partly |
| RK-10 | Typo correction through a word dictionary | P1 | Not built (trigram similarity on labels and names only) |

## 7. Evaluation: judgement list and NDCG@10 (C31)

### 7.1 The judgement seed (M, `judgement_seed.csv`)

146 queries. By segment: hotels 41, schools 40, plumbers 33, surgical 32. By language: English 93, Roman Urdu 47, Urdu script 6. By query type: torso 46, head 41, tail 36, typo 16, navigational 5, near-me 2. Result type: entries 125, list 21. **Every row has status `seed_unjudged`**: the file holds the intent (exact and substitute concepts and places, complements, must-terms), not human labels. The plan asks for 200 queries scored by native speakers; the seed is 73% of that size and has only 6 Urdu-script queries. Missing before it counts: native-speaker review of every row, many more Urdu-script queries, near-me queries, and tail queries from a real log.

### 7.2 Labels and metrics (`esci_eval.py`)

- Labels: **E** exact (right list type and place), **S** substitute (right type in the same province, or related type in the right place), **C** complement, **I** irrelevant (also closed, unpublished, or missing a must-term brand word).
- Gains: STRICT E 1.0, S 0.1, C 0.01, I 0 (the Amazon KDD Cup 2022 setting, R, not re-opened); TOLERANT E 1.0, S 0.5, C 0.1, I 0 (our proposal for a directory where a nearby result still helps).
- Metrics: NDCG@10 (linear gains, ideal list built from all judged candidates), MRR, precision@10 of E, zero-result rate.
- Self test run now (M): `python3 esci_eval.py --selftest` printed `esci_eval selftest ok`.

### 7.3 Ranking demo

`demo_ranking.py` compares six rankers (`alpha`, `random`, `text`, `prior`, `blend_add`, `product`) over the synthetic 1M table by NDCG@10 on the seed. It needs the bench database and `numpy`/`psycopg`; **it was not run and no saved output exists (`results/ranking_demo.json` absent).** So no NDCG number is reported. The script's own header warns that the synthetic "closed" flag depends on verification level and age by construction, so any gain from a prior is built in and must not be used as a forecast. The proper evidence is NDCG@10 on human labels (section 7.1), real data and a clean baseline (alphabetical, which is today's list order).

### 7.4 Process (H)

1. Native speakers label top-20 candidates per query for the current ranker and for each new variant (pooling). 2. Report NDCG@10 strict and tolerant, MRR, zero-result rate, per segment and per language. 3. A candidate ranker ships only if NDCG@10 rises with no drop in the Urdu and Roman Urdu segments. 4. An LLM judge may add labels only after agreement with the humans is measured (calibration, kappa) on 200 shared rows (C31). 5. Weekly zero-result and no-click query review (C32). 6. Interleaving for live A/B tests when traffic allows.

## 8. Index sync: outbox and alias swap (C27)

### 8.1 Design (H)

- **Outbox**: a trigger on entry, variant, verification and place-name tables writes `(entry_id, version, op)` to an `outbox` table in the same transaction. Consumers claim batches with `FOR UPDATE SKIP LOCKED`, coalesce to the highest version per entry, and upsert into the engine with an **external version** so that old and duplicate events cannot overwrite newer ones. Deletes are tombstones with a higher version. Old done rows: partitioned by day and dropped, not deleted.
- **Full rebuild**: build a new versioned index (`entries_v2026_10_08`), replay from a snapshot while the outbox keeps queuing, apply queued events, compare counts and checksums, then move the alias in one atomic call. Keep the previous index for rollback for a day.
- **Nightly check**: count and checksum compare of Postgres versus index per country group; mismatches re-queued.
- **Lag target**: search shows a change within 5 seconds at p95 (H) and the lag is exported as a metric.

### 8.2 `outbox_sim.py` results

`outbox_sim.py` is written (five tests: T1 write overhead of the trigger; T2 consumer throughput with 1 and 4 workers; T3 convergence under 20% duplicate, shuffled, reordered events and 15% simulated worker crashes, must equal the source of truth; T4 outbox age under 2,000 writes per second with 2 consumers; T5 clean-up cost). **No result file was found (`results/outbox_sim.json` absent). The simulation was not run, or its output was lost, so there are no measured numbers for it.** The script asserts zero mismatches in T3, but that has not been seen to pass in this evidence. Do not quote lag or throughput figures.

## 9. Acceptance test names (proposed, none exists except where marked)

Existing in `backend/catalog/tests/test_search.py` (checked): `test_synonym_and_typo_find_the_list_type`, `test_places_found_in_both_scripts`, `test_entries_found_by_name_typo_and_urdu_variant_only_inside_a_scope`, `test_drafts_never_appear`, `test_search_page_groups_and_zero_result_flow`, `test_search_fragment_returns_only_rows`, `test_header_search_form_and_scope_hint_on_list_pages`, `test_new_list_type_is_found_immediately`. Note 02 mentions `catalog/tests/test_search_backends.py`; that file **does not exist** in the repository (the contract suite is not built).

Proposed:

| Area | Test name |
|---|---|
| Contract | `test_every_backend_passes_contract_concepts_places_entries` |
| Contract | `test_backends_agree_on_top_3_for_seed_queries` |
| Query shape | `test_entry_search_plan_uses_text_index_not_seq_scan` (EXPLAIN on a 100k fixture) |
| Latency | `test_scoped_search_p95_under_budget_at_1m` (slow marker, run on the bench box) |
| Typos | `test_typo_recall_at_25_not_below_baseline` (baseline 0.87) |
| Scripts | `test_roman_urdu_and_urdu_variants_find_same_entry` |
| Scripts | `test_urdu_normalisation_cases_alef_hamza_ya_kaf` |
| Autocomplete | `test_prefix_autocomplete_uses_btree_and_returns_in_prior_order` |
| Autocomplete | `test_autocomplete_never_returns_unpublished_or_closed` |
| Ranking | `test_ranking_order_independent_of_payment` |
| Ranking | `test_paid_slots_labelled_and_outside_organic_list` |
| Ranking | `test_closed_and_expired_entries_rank_below_verified_fresh` |
| Ranking | `test_new_verified_entry_boost_expires_after_window` |
| Evaluation | `test_ndcg_at_10_matches_hand_computed_example` (selftest exists in `esci_eval.py`) |
| Evaluation | `test_judgement_list_has_no_unlabelled_rows_before_release` |
| Evaluation | `test_ndcg_does_not_drop_in_urdu_segment` |
| Facets | `test_facet_filters_are_noindex_and_canonical` (partly built in SEO tests) |
| Facets | `test_facet_counts_match_list_page_total` |
| Facets | `test_no_facet_combination_in_sitemap` |
| Sync | `test_outbox_row_written_in_same_transaction` |
| Sync | `test_outbox_rollback_leaves_no_event` |
| Sync | `test_old_event_cannot_overwrite_newer_version` |
| Sync | `test_duplicate_and_reordered_events_converge` |
| Sync | `test_delete_then_stale_update_does_not_resurrect` |
| Sync | `test_worker_crash_after_apply_is_replayed_safely` |
| Sync | `test_alias_swap_is_atomic_and_rollback_works` |
| Sync | `test_nightly_count_checksum_compare_requeues_mismatch` |
| Zero results | `test_zero_result_query_is_logged_without_identifiers` |
| Zero results | `test_start_this_list_flow_shown_on_zero_results` |

## 10. Matrix status check (from note 03, against the repository)

| Challenge | Matrix status | This note's finding |
|---|---|---|
| C10 Facets | Built (never indexed); counts partly | Facet timings not measured (no saved output) |
| C27 Index sync | Not built | Design only; simulation has no saved result |
| C28 Fairness | Built (slots) | Agreed; exposure audit missing |
| C29 Cold start | Not built | Design only |
| C30 Position bias | Not built | Design only |
| C31 Evaluation | Not built | Seed of 146 unjudged queries and a tested metric library exist; no labels |
| C32 Zero results, typos | Built (flow); curation open | Typo recall about 0.8 to 0.95 in the top 25 on synthetic data |
| C33 Unscoped cost | Built (scoping) | Unscoped entry scan is avoided; current entry query shape is slow when scoped (RK-1) |
| C34 Blended results | Partly | Grouping built; no evaluation |
| C35 Autocomplete | Partly | btree prefix measured: good to 5M unscoped; city scope tail needs work |

## 11. Conflicts and gaps

- Note 02 and the code comment say unscoped fuzzy search costs "150 to 520 ms at a million entries" (plan 4.3). The saved run shows 2.6 to 3.3 s p50 for the repository's query shape at 1M unscoped. The older figure may have used a different query or hardware; unresolved. The code comment is therefore not a reliable budget.
- Note 02 expects a bake-off with 10M documents; no engine run exists.
- Note 02 mentions a contract test file that is missing.
- 5M figures are incomplete and partly loaded (section 1.2).
- No concurrency, no cold-cache, no write-while-reading, no production hardware.
- No real Urdu lexicon or query log.

## 12. Open decisions for the founder (suggested defaults)

| # | Decision | Suggested default |
|---|---|---|
| 1 | Rewrite `ModelBackend.entries()` before any engine work (RK-1) | Yes; small code task, then re-measure at 1M and 5M on a clean box |
| 2 | Repeat the 5M runs on a quiet machine and finish the missing cells | Yes, when heavy work resumes; paused now by your instruction |
| 3 | Run the engine bake-off at 3 to 5M entries or at S3 | At S3 trigger (ST-1 or ST-5); keep OpenSearch as default candidate |
| 4 | Commission native-speaker labelling (200 queries, Urdu-heavy) | Yes; it unblocks every ranking decision |
| 5 | Fixed-weight ranking first, learning later | Yes |
| 6 | Cold-start boost length and exploration share | 14 days and 1 in 10, tune after data |
| 7 | Counsel review of GPL (Typesense) and BUSL (Meilisearch Enterprise) before choosing | Yes, only if either engine wins the bake-off |
