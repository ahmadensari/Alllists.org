# Entity resolution and data quality at 100 million entries

Research date: 2026-10-06. English only. Design and planning note; no code or data was changed. It answers requirements D-04, D-05, D-09, D-10 and D-14 of `docs/REQUIREMENTS_DEPTH_AND_SCALE.md` and feeds `03_capabilities_and_skills_matrix.md`.

## How to read the grades

| Tag | Meaning |
|---|---|
| **C** | Read from this repository (file and line named). |
| **M** | Measured or computed by me in this session with a throw-away script in the scratchpad (not committed). The script is described so it can be rerun. |
| **R** | Reported: a fetched primary page, a GitHub file or API answer, or a search summary of a primary. Where a search summary only, it is marked **R-search** and is UNVERIFIED at the source. |
| **S** | Secondary: blog, aggregator, vendor marketing. |
| **I** | Inference. Inputs are stated next to the figure. |
| **H** | Hypothesis: a design choice or threshold nobody has tested yet. Calibrate before use. |

Things I could not open: `docs.overturemaps.org` and `dataingovernment.blog.gov.uk` were blocked by the egress proxy. GitHub API access to third-party repositories through `gh` was refused ("not enabled for this session"). The GitHub MCP search worked, so licences below marked **R-GitHub** were read from the `LICENSE` file of the named repository. Web search is US-only and returns summaries.

---

## 0. Summary

1. **The current `backend/intake/dedupe.py` is correct for a pilot and fails by design above about 1 million entries per country.** It compares every pair in a block with two database queries per pair, loads every entry of the country into memory (about 2.5 KB per Python `Entry` object [M]), and has no key that survives a different script, a different phone label or a city-level pin. Arithmetic in section 2.
2. **Four defects matter before any scale work.** (a) The phone hash includes the contact kind, so the same number stored as `mobile` on one entry and `whatsapp` on another never matches [C `entries/services.py:161-166`]. (b) A shared phone plus name similarity of 0.5 or more auto-merges, with no cap on how many entries share the number [C `dedupe.py:55-56`]. (c) `merge_entries` does not move secondary categories, verification, claims, consent, value metadata or branch links, and records nothing that would let it be undone [C `entries/services.py:498-552`]. (d) `DedupeCandidate.State.AUTO_MERGED` is never written, so the auto-merge error rate is invisible to the dashboard [C `grep`, `core/monitoring.py:80-90`].
3. **Design.** Resolve in staging, not after publication: cluster source records with exact keys first, then a probabilistic scorer (Splink, MIT) for the rest, then people only for the narrow band. At 100 million entries from about 300 million source records the compute is under USD 10 per full run; **human review is more than 99% of the cost** (USD 233 to 3,333 per million source records [I], section 2.9).
4. **Many-to-many.** The existing `Entry.secondary_concepts` is an auto-created join table with no role, source, confidence or evidence, and no query, roll-up or list page reads it [C]. Replace it with one `entry_concept` table (about 160 bytes a row, 48 GB at 3 memberships per entry [I]) with the place path denormalised into it so a list page is one index range scan (section 4).
5. **IDs and URLs.** Keep `uid` (ULID) as the permanent public key; the entry URL carries no place and no category, so moving an entry never changes it. Only merges, list-type renames and place renames need redirects. Use one-hop redirects with a 30-day undo window before they become 301 (section 3).
6. **Freshness.** The existing rule (every check expires: AI 180 days, surveyor and owner 365, then 90 days grace) would cost USD 6 to 20 million a year at 100 million entries if every AI check were repeated [I]. A tiered, change-detecting schedule costs about USD 0.8 to 2.7 million a year (USD 0.008 to 0.027 per entry-year) [I] (section 5). `sweep_expired` loops over every published entry with one query each: about 200 million queries, 17 hours, every hour [I].
7. **Humans.** One part-time surveyor does about 440 phone checks a month at 6 minutes each; checking every entry once by hand needs about 6,300 full-time years [I]. Human checks are therefore a scarce resource used on tier-1 entries, audits, disputes and review-band pairs only (section 6).
8. **Quality bar.** Replace the 385-record estimate with a 29-record acceptance test per stratum (zero failures proves at least 90% at 95% confidence), escalating to 385 on any failure [I].
9. **Abuse.** Competitor abuse is real at scale: Google reported blocking more than 100 million abusive Business Profile edits in 2021 and 12 million fake profiles in 2023 [R-search]. Defences: a report never changes state on its own; "closed" needs two independent signals (today one surveyor can close an entry alone [C `volunteers/services.py:82-89`]); merges involving a claimed, paid or person entry always go to a person.
10. **Work.** 22 work packages (section 10), each with named acceptance tests in the existing test folders. Nothing here requires deployment, spend or a founder decision before the pilot; items needing a decision are in section 11.

---

## 1. What the repository does today

Files read: `backend/intake/dedupe.py`, `backend/intake/importer.py` (`settle_duplicate`), `backend/intake/bulk.py`, `backend/intake/loaders.py`, `backend/intake/models.py`, `backend/entries/models.py`, `backend/entries/services.py`, `backend/analytics/rollups.py`, `backend/catalog/queries.py`, `backend/catalog/views.py` (entry page), `backend/core/jobs.py`, `backend/core/monitoring.py`, `backend/volunteers/models.py` and `services.py`, `backend/taxonomy/models.py`, `docs/TECHNICAL_PLAN.md` sections 4, 6, 7, 8.2, and the sibling notes `Backend research/03_hosting_and_costs.md` and `04_agent_training_and_ai_auditor.md`.

### 1.1 Facts

| # | Fact | Where | Grade |
|---|---|---|---|
| F1 | Thresholds `AUTO_MERGE = 0.90`, `REVIEW = 0.60`; weights phone 0.50, name 0.30, distance 0.10, address 0.10. These are hand-set, not calibrated probabilities. | `dedupe.py:9-11` | C |
| F2 | Batch blocking key is `(country_code, place_id, primary_concept_id)`; every pair in a block is scored with `combinations`. | `dedupe.py:99-104` | C |
| F3 | `features()` runs two `Contact` queries for every pair. | `dedupe.py:37-38` | C |
| F4 | `scan_all` iterates the whole queryset into a dict of lists, so all entries are in memory at once. | `dedupe.py:96-101` | C |
| F5 | Online path `candidates_for` loads every entry of the same concept whose `place_path` starts with the entry's path (no dot boundary, so `pk.punjab.sialkot` also matches `pk.punjab.sialkotcity`), plus every entry sharing any contact hash, as full model objects. | `dedupe.py:65-78` | C |
| F6 | `similarity()` is trigram Jaccard on `fold()` text. Urdu-script and Latin-script spellings of one name score 0.0 (below). | `dedupe.py:19-24` | C, M |
| F7 | Distance is binary: 1.0 if within 100 m else 0. No geo index exists; latitude and longitude are plain decimals. PostGIS is planned for S1. | `dedupe.py:45-48`; plan 4.1 | C |
| F8 | `add_contact` hashes `f"{kind}:{norm}"`, so the hash depends on the contact kind. `features()` compares hash sets across kinds `phone`, `mobile`, `whatsapp`. | `entries/services.py:161-166`; `dedupe.py:36-38` | C |
| F9 | Shared phone and name similarity at or above 0.5 gives score 0.92, above the auto-merge line. Same name within 100 m and name at or above 0.8 gives 0.92. No limit on how many entries share the number. | `dedupe.py:55-58` | C |
| F10 | Bulk publish creates one entry at a time then calls `settle_duplicate`, which scans and may merge. Each entry create and each merge writes audit rows under one global advisory lock (727001). | `bulk.py:167-185`; `importer.py:115-126`; `core/models.py` `audit()` | C |
| F11 | `merge_entries` moves 11 child sets, adds the dropped name as a `NameVariant`, re-points credit, tombstones the dropped entry with `merged_into`, writes `MergeMap` (from, to, score, decider, time) and one `ChangeLog` row. | `entries/services.py:498-552` | C |
| F12 | `merge_entries` does not touch: `secondary_concepts`, `VerificationEvent`, `VerificationCurrent`, `ValueMeta`, `Claim`, `ConsentRecord`, `CompanySection`, `StewardGrant`, branch links (`parent_entry`), the dropped entry's own `merged_from` rows, or the dropped entry's non-name fields (website, address, coordinates). | `entries/services.py:498-552` | C |
| F13 | `MergeMap` and `ChangeLog` record only that a merge happened and the dropped uid. No row ids of moved children are kept, so the plan's "Un-merge is possible from the log" (6.7) cannot be done from current data. | `entries/models.py:341-348`; plan 6.7 | C |
| F14 | The staff merge action keeps the older entry (`sorted by created_at`) whatever the state of either side. A claimed or verified newer entry loses its claim and checks silently. | `catalog/staff_views.py:245-249` | C |
| F15 | The entry page redirects a merged entry with a permanent redirect, one hop. Entries merged earlier into the now-dropped entry still point at it, so chains of two hops appear. | `catalog/views.py:311-319`; `entries/services.py:498-552` | C |
| F16 | `Entry.secondary_concepts` is a plain many-to-many field. `grep` finds it only in `models.py` and migrations: no page, roll-up, search or importer reads or writes it. List pages, roll-ups and `descendant_concept_ids` use `primary_concept` only. | `entries/models.py:46`; `catalog/queries.py:12-24`; `analytics/rollups.py:36-44` | C |
| F17 | `Product.concept` and `Speciality.concept` link a child row to a concept, separate from the entry's categories. | `entries/models.py:175-188` | C |
| F18 | `Entry.place_path` is a copy of the place's slug path, indexed for prefix scans. A place rename or move needs every entry under it rewritten. | `entries/models.py:57`; `entries/services.py:169-190` | C |
| F19 | Places have `status = merged` but no stored redirect target; there is no slug-history table for places or concepts. | `places/models.py:27,40`; `grep` for redirect or slug history | C |
| F20 | `CHECK_VALIDITY_DAYS = {surveyor 365, owner 365, ai 180}`, `GRACE_DAYS = 90`. One value per level, not per field group or list type. | `config/settings/base.py:161-162` | C |
| F21 | `sweep_expired` runs hourly inside one transaction, locks every expired row, then loops over every published entry calling `current_level` (one query each) and `entry.verification_current.all()`. | `entries/services.py:339-382`; `core/jobs.py` (`expiry_sweeper`, HOUR) | C |
| F22 | `queue_unchecked(limit=100)` runs daily and makes at most 100 verify tasks. `take_next_task` is oldest-first with `SKIP LOCKED`; no priority, no place or language affinity, no lease timeout. | `volunteers/services.py:34-63`; `core/jobs.py` | C |
| F23 | A surveyor outcome `closed` sets `PERM_CLOSED` at once, with one person's evidence text. | `volunteers/services.py:82-89` | C |
| F24 | Audit sample size 385 (95% confidence, 5% margin), accuracy bar 0.90; verifier canary accuracy under 0.8 after 3 tasks suspends. | `bulk.py:24-25`; `volunteers/services.py:109-116` | C |
| F25 | The data-quality dashboard has three metrics: expired-check share (alert at 25%), "duplicate rejection rate" (rejected over merged plus rejected candidates, alert at 10%), surveyors under 80%. `AUTO_MERGED` is never written, so auto-merges are outside the second metric. | `core/monitoring.py:64-97`; `grep AUTO_MERGED` | C |
| F26 | Bulk loaders place each record at the nearest city or area centre within 25 km (deepest within 3 km of the closest), by sorting every place of the country for every record. Many entries therefore share a city-level `place_id`, which makes the blocking key above produce very large blocks. | `intake/loaders.py:35-52,124-150` | C |
| F27 | The plan's own numbers: 1 million entries all-pairs 5e11, blocked to about 20 per block gives 9.5 million comparisons; bulk loaders about 5,000 rows a second; 1.7 KB per entry (plan) against 6.6 KB per entry (hosting note's row arithmetic). | plan 4.3, 7.2, 7.4; hosting note 2.2 | C, I |

### 1.2 Measurements I ran (reproducible)

| Test | Result | Method |
|---|---|---|
| Python cost of `similarity(name)` + `similarity(address)` + `haversine`, no database | 58 microseconds a pair, 17,000 pairs a second on one core | 40,000 random pairs of 3-word names and 6-word addresses, `core/textfold.py` copied unchanged |
| Same with trigram sets precomputed once per entry | about 99,000 pairs a second | same script |
| `fold()` speed | 7 microseconds per name (31 to 46 characters) | 50,000 calls each |
| Memory of one unsaved `Entry` instance with typical text fields | 2,503 bytes | `tracemalloc` over 2,000 instances, `config.settings.base`, venv Python |
| Trigram Jaccard after `fold()`: `محمد علی سرجیکل` against `Muhammad Ali Surgical Works` | 0.00 | no shared character, so no shared trigram |
| `Al-Noor Traders` against `Al-Noor Pharmacy` | 0.32 | correctly low, but only because both generic words are present |
| `Mughal Surgical Co` against `Mughal Surgical Company (Pvt) Ltd` | 0.53 | legal-form noise halves the score |
| `Hotel Serena Islamabad` against `Serena Hotel` | 0.44 | below the 0.5 gate in rule F9, so a shared phone would not even reach review as a strong match |
| `Muhammad Ali Surgical` against `Mohammad Ali Surgicals` | 0.67 | |
| `Royal Steel Instruments` against `Royal Steel Instrument` | 0.88 | |

### 1.3 Limits of the current pipeline, with arithmetic

Assume a query round trip on a local PostgreSQL of 0.25 to 1 ms [H]; at 0.5 ms a pair costs about 1.06 ms (two queries plus 58 microseconds), so about 1,000 to 2,000 pairs a second [I].

| Block size n | Pairs n(n-1)/2 | Time at 1,000 pairs/s | At 2,000/s | Python-only ceiling at 17,000/s |
|---|---|---|---|---|
| 20 | 190 | 0.2 s | 0.1 s | |
| 1,000 (a city's restaurants if the place is the city) | 499,500 | 8 min | 4 min | 29 s |
| 10,000 | 49,995,000 | 13.9 h | 6.9 h | 49 min |
| 100,000 | 4,999,950,000 | 58 days | 29 days | 3.4 days |

| Whole-database batch (`scan_all`) | Pairs if every block is 20 | Time at 1,000 to 2,000 pairs/s | Memory (2.5 KB an entry, all loaded) |
|---|---|---|---|
| 1 million entries | 9.5 million (matches plan 7.4) | 1.3 to 2.6 h | 2.5 GB |
| 10 million | 95 million | 13 to 26 h | 25 GB |
| 100 million | 950 million | 5.5 to 11 days | 250 GB |

Real block sizes are skewed, not uniform. If 10,000 of the blocks hold 2,000 entries each (20 million entries), those blocks alone are 10,000 times 1,999,000 equals 2.0e10 pairs, 21 times the uniform figure [I; skew is H]. Loaders put entries at city-level places (F26), which pushes towards this case.

**Online path.** For each new row, `scan_entry` fetches every entry of the concept in the place subtree (2.5 KB each) and runs two queries per candidate (F3, F5). With N existing candidates:

| N | Queries per new row | Time per row (0.25 to 1 ms a query) | 1 million new rows, sequential (0.5 ms) |
|---|---|---|---|
| 500 | 1,000 | 0.25 to 1 s | 5.8 days |
| 5,000 | 10,000 | 2.5 to 10 s | 58 days |
| 20,000 | 40,000 | 10 to 40 s | 231 days |

Against the plan's loader target of 5,000 rows a second [plan 7.2], the dedupe step alone would cap a large-city import at 0.03 to 4 rows a second [I]. **The bulk path (`bulk.publish`) and the Overture and Foursquare loaders both go through this step.**

**Merge execution.** If 300 million source records become 100 million entries by create-then-merge, there are 200 million merges. Each writes at least two audit rows under the global lock; at 2 ms a hold that is 200 million times 2 times 2 ms = 9.3 days of pure lock time, however many workers run [I]. So at scale resolution must happen before entries are created (section 2.2).

**Other limits found while reading.**

- Recall: cross-script names never match (F6); labels on phones (F8); a pin at a city centre scores "within 100 m" of every other entry at that centre (F7, F26) unless `precision_class` is checked, which it is not.
- Precision: shared switchboards, market-plaza landlines and one owner's mobile on several businesses create false merges (F9). A phone-hub rule is needed (section 2.3, key K1).
- Calibration: nothing measures auto-merge precision (F25), so the 0.90 line has never been tested against ground truth.
- Memory for the batch path is the first thing that breaks (F4), well before the arithmetic above on time.

---

## 2. Entity resolution design

### 2.1 What is an entity here (levels)

| Level | Meaning | Resolution rule |
|---|---|---|
| Organisation (brand, company) | The legal or trading body | One `Entry` per organisation only where the list needs it (manufacturer lists); hotel chains are organisations |
| Site (outlet, factory, hotel property) | A place where it operates | The normal `Entry` (one hotel, one factory). Two sites of one organisation are **linked by `parent_entry`, never merged** |
| Person | A named individual | Gated (rule 5). Never auto-merged; consent applies to the survivor |

A hotel in many lists is one site entry with many category memberships (section 4) and one place. A manufacturer in many product nodes is one entry with many memberships. A manufacturer with two factories is two site entries under one organisation entry. This keeps "same name, different address" from being merged by mistake, which is the commonest false merge for chains.

### 2.2 Pipeline (stage, block, score, decide, apply)

```
source records (immutable)            exact keys              probabilistic              people
 import row | external record  -->  K1..K4 deterministic -->  Splink score on     -->  review band,
 agent draft | owner submission      clusters (cheap)          remaining blocks        LLM pre-opinion
        |                                  |                         |                      |
        v                                  v                         v                      v
   normalise + keys             cluster id per record      cluster id + p(match)     merge_event, judgement
        \________________________________________________________________________________/
                                      one Entry per cluster, source records linked
```

Rules:

1. **Resolve in staging.** Source records get a `cluster_id` before any `Entry` exists. Absorbed records never become entries, so there is no merge, no audit pair and no redirect for them. This removes the 200 million merges and the 9.3 days of lock time above. It extends the existing pattern in `bulk.py` (stage, audit sample, publish) and `ExternalRecord` (checkpoint).
2. **Post-publication merges** (new evidence, staff action, report) use the merge service of section 2.8 and are rare: assume 1% to 3% of entries a year [H].
3. **Never delete a source record.** The cluster can be rebuilt, and unmerge is a re-clustering of recorded evidence.
4. **Models are versioned.** Every decision stores the model version, thresholds, features and the source record ids.

### 2.3 Normalisation and keys

All keys are computed once at staging and stored in `entry_key` (entry or source record, key type, key hash). Only selective key types are stored.

| ID | Key | Built from | Typical block size | Catches | Fails on / guard |
|---|---|---|---|---|---|
| K1 | Phone number hash | E.164 digits only, hashed **without the contact kind**, with the same keyed HMAC | 1 to 3 | Same number, any label | Shared lines. **Hub guard:** a number listed on more than 3 entries with different name keys is not a key; it is a hub, a feature that lowers scores |
| K2 | Website domain | registrable domain (public-suffix list) of `website`, lower-case | 1 to 5 | Same site on two lists | Platform pages (facebook.com, linktr.ee, wixsite, blogspot, google sites, marketplaces): exclude by a maintained list; hub guard as K1 |
| K3 | Registration identifier | `(scheme, value)` from `Identifier` rows (SECP, NTN, drug licence, ISO certificate, PMDC, etc.) | 1 | Strongest evidence | Different values in one scheme **veto** a merge (section 2.6) |
| K4 | Geo cell plus name token | H3 resolution 9 cell (edge about 174 m [R-search]) and its 6 neighbours, times the rarest name token | 5 to 30 | Same shop, different spelling | Only for pins with `precision_class` building or better and not a centroid hub (more than 5 entries on one exact point) |
| K5 | City plus category family plus name skeleton | `place_id` at city level, concept family, first significant token's skeleton (below) | 20 to 200 | Variant spellings, transliteration | Cap block at 500; above that split by H3 cell |
| K6 | Rare token in a city | token with high inverse document frequency in the city | 2 to 20 | Brand names and unusual words | Common words ("traders") are not keys |
| K7 | Address key | house or plot or shop number plus street or plaza or society tokens after normalisation | 1 to 5 | Same unit | Landmark-only addresses give no key |
| K8 | Social handle | normalised handle per platform | 1 to 3 | Same page | Platform default or generic handles |
| K9 | Embedding neighbours | top 10 by cosine inside (country, concept family), only for records with no K1 to K8 hit or with non-Latin names | 10 | Cross-script and unusual spellings | Tier 3 (section 2.5) |

**Pairs completeness** (share of true duplicate pairs that share at least one key) is the blocking metric: target at least 98% on the labelled set [H]. **Reduction ratio** at 100 million entries: all pairs are 100e6 times (100e6 minus 1) over 2 = 5.0e15; with 30 candidates per record there are 1.5e9 pairs, a reduction of 1 minus 3e-7 [I].

#### Name folding (script-aware)

Layers, each stored so a later layer never replaces an earlier one:

| Layer | Output | What it does | Status |
|---|---|---|---|
| F0 | `name_fold` | The existing `fold()`: NFKC, Arabic and Urdu letter unification, digits, marks, punctuation | Built [C `core/textfold.py`] |
| F1 | `name_key` | F0 plus: drop legal forms (pvt, ltd, co, company, llc, est, mfg), join split compounds (`al noor` and `alnoor`), unify `muhammad`, `mohammad`, `mohd`, `md`, unify `&` and `and`, strip Latin diacritics | Not built |
| F2 | `name_skeleton` | Consonant skeleton for Latin and Roman Urdu: digraphs reduced (`ph` f, `kh` k, `sh` s, `ch` c, `th` t), `q` k, `v` w, doubled letters collapsed, vowels and `h` dropped after the first letter | Not built |
| F3 | `name_skeleton` for Urdu and Arabic script | Map each letter to a Latin consonant class (Urdu omits short vowels, so a consonant skeleton is the natural common form), strip the Arabic article `ال`, hamza and teh marbuta variants | Not built |
| F4 | Alias table | Curated pairs for frequent trade words and brands (`سرجیکل` = surgical, `انسٹرومنٹس` = instruments) and for each country's legal forms | Plan 7.3 names it, not built |

**What I measured on a throw-away prototype of F1 to F3** (scratchpad, about 40 lines, not committed):

| Pair | Plain trigram (F0) | Skeleton trigram | Reading |
|---|---|---|---|
| `Muhammad Ali Surgical Works` and `Mohammad Ali Surgicals Pvt Ltd` | 0.44 | 0.80 | skeleton helps |
| `Mughal Surgical Co` and `Mughal Surgical Company (Pvt) Ltd` | 0.53 | 1.00 | legal forms removed |
| `Hussain Industries` and `Husain Enterprises` | 0.23 | 1.00 | but skeleton `hsn` is too short and common: **needs a minimum length and a second signal** |
| `Al-Noor Traders` and `Al Noor Pharmacy` | 0.32 | 0.55 | **worse**: stripping `traders` leaves `al nr`, which now resembles the other. Generic-word stripping must be weighted by category and word frequency |
| `Muhammad Ali Surgical Works` and `محمد علی سرجیکل` | 0.00 | 0.32 | skeleton alone does not bridge scripts (`surgical` gives `srgcl` against `srjkl`; Urdu `ع` is dropped) |
| `Al-Noor Traders` and `النور ٹریڈرز` | 0.00 | 0.12 | same |

Conclusions [I]: (1) skeleton keys improve Latin spelling variants and are good for blocking, never for a decision alone; (2) cross-script needs fuzzy skeleton comparison plus the alias table plus embeddings, not an exact key; (3) short skeletons and generic words need frequency weighting, which is what Splink's term-frequency adjustment does [R, README summary]. Roman Urdu has no standard spelling; there is published work on a phonetic encoding derived from Soundex for it (UrduPhone, arXiv 2004.00088 [R-search], rules not read) and standard Soundex and Double Metaphone are tuned for English and give sound-alike collisions [R-search]. The 500-pair labelled set already planned (plan 7.3, precision at least 95%) is the test; extend it to include 150 cross-script pairs.

ICU's `Arabic-Latin` transform exists in CLDR [R-search] and ICU is under a permissive licence [R-search]; whether it covers Urdu-specific letters (ٹ ڈ ڑ ں ے) well enough is UNVERIFIED and must be tested on the 150 pairs before it is chosen over a small hand table.

#### Address normalisation

| Step | Method | Notes |
|---|---|---|
| Structure | Existing `place_id` is the coarse structure (city, area, society). Do not re-parse it | |
| Free text | Rule-based tokeniser for South Asian and Gulf forms: expand `rd`, `st`, `blk`, `sec`, `ph`, `mkt`, `flr`; keep plot, house, shop and floor numbers as separate tokens; drop `near`, `opposite`, `behind`; keep plaza, market and society names | Landmark-heavy addresses give weak keys; mark address key as absent rather than guess |
| Parser option | libpostal: MIT [R-GitHub], 10,000 to 30,000 addresses a second on one thread, 99.45% full-parse accuracy on its own held-out OpenStreetMap-derived test set, about 2 GB of model data, designed for under 1 GB RAM per process [R, README fetched]. Accuracy on Pakistani and Gulf addresses is UNVERIFIED; the claim is for its own test set | Optional adapter behind one interface. 1 million parses is 33 to 100 s on one core [I]. The model data licence (OSM and OpenAddresses derived) is UNVERIFIED: check before shipping the model |
| Compare | Token-set Jaccard plus exact match on house or shop number; a number mismatch with the same street is a strong negative | |

#### Geo keys

H3 (Apache-2.0 [R-GitHub]) resolution 9 has an edge of about 174 m and resolution 10 about 66 m [R-search for res 9; res 10 is from memory, UNVERIFIED]; geohash length 7 is about 153 m by 153 m [R-search]. Use cell plus the six neighbours so a pair near a cell edge is not missed. Exclude any coordinate whose `precision_class` is `area` or `city`, or that comes from a place centre (`coord_source`), or that has more than 5 entries on the exact same point. Precise distance for the score uses PostGIS `ST_DWithin` on a `geography` column (planned S1; PostGIS is GPL-2.0-or-later, used as a database extension [K, UNVERIFIED]).

### 2.4 Tools compared (open source first, D-13)

| Tool | Licence | Fit | Scale facts | Recommendation |
|---|---|---|---|---|
| **Splink** | MIT [R-GitHub `LICENSE`]. 2,458 stars, pushed 2026-10-06 [R, GitHub search] | Fellegi-Sunter model, EM training without labels, term-frequency adjustment, blocking rules, DuckDB, Spark and PostgreSQL backends [R, README fetched] | "A million records on a laptop in around a minute"; "100+ million" with Spark or Athena [R, README and search] | **Adopt for batch scoring (S2 and later).** Version conflict: search shows 4.0.7 on PyPI; the README says Splink 5 was announced 2026-09-28. UNVERIFIED which to pin: read the release notes at build |
| dedupe | MIT [R-GitHub]. 4,515 stars, pushed 2026-10-05 | Supervised, active learning, learns blocking | In-memory; practical ceiling is a few million records per run [I, UNVERIFIED] | Only for a quick labelling experiment on one country; not the production path |
| recordlinkage | BSD-3-Clause [R-GitHub, licence text read]. 1,062 stars, pushed 2026-10-05 | Pandas toolkit: indexing, comparison, classifiers | In-memory, single machine | Useful for notebooks and for evaluating blocking (pairs completeness, reduction ratio) |
| Zingg | **AGPL-3.0** [R-GitHub `LICENSE`] | Spark ER with ML | Large | **Avoid** unless counsel clears AGPL network clause; Splink covers the need |
| libpostal | MIT [R-GitHub] | Address parse and expansion | see above | Optional adapter (section 2.3) |
| pg_trgm | PostgreSQL licence, a contrib module [K, UNVERIFIED] | Trigram candidates inside PostgreSQL; GIN index already exists on `name_fold` and `NameVariant.text_fold` [C `entries/migrations/0002`] | A mailing-list report says trigram GIN becomes useless around 15 billion rows [R-search]; the plan's own measure is 150 to 520 ms unscoped at 1 million entries [plan 4.3] | Keep for scoped lookups only (always filter by city and category first) |
| pgvector | PostgreSQL licence [R-GitHub `LICENSE` fragment] | Embedding neighbours in the same database | An HNSW index wants about 1.5 times the raw vectors in RAM [R-search]; 50 million 1,536-dimension vectors took 2 to 6 hours to build [R-search] | Shard by country and category family; section 2.5 |
| multilingual-e5 (base, large) | MIT [R-search] | 94 languages | Urdu quality UNVERIFIED | Evaluate against the cross-script pairs |
| bge-m3 | MIT [R-search] | 100+ languages | Urdu quality UNVERIFIED | same |
| LaBSE | Apache-2.0 [K, UNVERIFIED] | Translation-pair embeddings | | Evaluate if the two above fail |
| H3 | Apache-2.0 [R-GitHub] | Cell index | | Use |
| Nominatim | GPL-2.0 [R-search] | Self-hosted geocoder on OpenStreetMap (ODbL data) | Heavy to host | Run only if a geocoder is needed; use as a service, not linked code |
| Photon | Apache-2.0 [R-search] | Search-as-you-type over OSM | | Alternative |
| Pelias | MIT [R-search] | Geocoder | | Alternative |
| OpenCage | Commercial API over ODbL data; caches forward queries and logs for six months unless `no_record` is set [R-search] | Hosted geocoder | The right to **store** results beyond a session depends on the plan: UNVERIFIED | Do not buy until the pilot proves a need; plan 7.5 already requires terms that allow storage |
| Overture Places | Per-record licence; Foursquare-sourced part Apache-2.0; 64 million places; GERS stable IDs, changelogs and bridge files [R-search] | Baseline data and a model for stable IDs | Overture also maintains open matching and conflation libraries [R-search; repository not located, GitHub search returned nothing] | Use as a source; copy the changelog and bridge-file idea (section 3) |
| FSQ Open Source Places | Apache-2.0, over 100 million POIs, refreshed monthly [R-search] | Source | | Source |
| nomenklatura (OpenSanctions) | MIT [R-GitHub] | Resolver graph of judgements (same, not the same, undecided) giving a canonical ID per connected component [R-search] | | **Design precedent** for the judgement store and never-merge list (section 2.8). Do not adopt the code |
| Senzing | Commercial; free evaluation up to 100,000 records [R-search] | Full ER engine | | Excluded by D-13 unless Splink fails |

### 2.5 Candidate generation by tier

| Tier | Method | When | Cost shape |
|---|---|---|---|
| 1 | Exact keys K1 to K3, K7, K8 (hash join) | Always, online and batch | One indexed lookup each; no scoring cost |
| 2 | Blocking K4 to K6 plus Splink scoring (batch) or SQL features (online, one batched query per entry, not per pair) | Records with no Tier-1 hit | About 30 candidates a record |
| 3 | Embedding nearest neighbours K9 | Records with a non-Latin name, no Tier-1 or Tier-2 hit, or in the review band for a second opinion | 20% of records at most [H] |

Embedding memory [I]: 768 dimensions at 4 bytes is 3.1 KB a vector. For one country of 10 million entries: 30.7 GB in fp32, 15.4 GB at 2 bytes, 7.7 GB at 1 byte; for all 100 million: 307 GB, 154 GB, 77 GB; binary 768-bit codes would be 9.6 GB for 100 million. With the 1.5 times RAM rule for HNSW the unscoped fp32 case needs about 460 GB, so **shard by (country, category family) and embed only Tier-3 records**. Embedding time [H]: 1,000 short strings a second on one GPU gives 1 million in 17 minutes, USD 0.1 to 0.3 at USD 0.4 to 1 an hour; CPU only at 40 a second a core gives 6.9 core-hours a million, USD 0.09 to 0.42.

### 2.6 Scoring, thresholds and hard rules

**Model.** Splink Fellegi-Sunter with these comparisons: name key exact and fuzzy levels (F1, F2 trigram, Jaro-Winkler on `name_key`), alias match, K1 phone (with hub flag as a separate level), K2 domain, K3 identifier (equal, absent, **different**), H3 distance bands (0 to 30 m, 30 to 100 m, 100 to 300 m, farther, unknown), address token Jaccard and number match, category family equal, status, term-frequency adjustment on name tokens. Train by EM, then check against the labelled set.

**Why the line sits at 0.995.** Merge when p times (cost avoided by merging) exceeds (1 minus p) times (cost of a wrong merge): p is above c_wrong over (c_wrong plus c_avoid). If a wrong merge costs 100 to 200 times what a missed duplicate costs [H], the line is 0.990 to 0.995. A wrong merge damages two entries, can lose a claim and sends one business's messages to another; a missed duplicate shows twice in a list. The current 0.90 line corresponds to a ratio of 9 to 1 [I].

| Decision | Condition | Action |
|---|---|---|
| AUTO (draft entries and source records only) | p at least 0.995 **and** at least two independent strong agreements from {K3 equal, K1 equal and not a hub, K2 equal and not a platform, pin within 50 m with precise pin} **and** name key equal or skeleton similarity at least 0.85 **and** no veto | Cluster; no human |
| FAST REVIEW | p 0.95 to 0.995, or all AUTO conditions except the guards, with an LLM second opinion saying "same" | One-click confirm |
| REVIEW | p 0.70 to 0.95, or LLM unsure or "different" while p is high | Full review task (`dedupe_review`) |
| NO LINK | p below 0.70 | Not stored, except the top 3 by embedding for the monthly residual-duplicate audit |
| NEVER (veto) | Same identifier scheme with different values; different `entity_type`; both sides claimed by different owners; both with surveyor checks at addresses more than 300 m apart; a stored "not the same" judgement; one side a person without consent | Block; keep the pair out of the candidate table |
| ALWAYS REVIEW | Either side `claimed`, on a paid plan, a person, child-facing, or has a surveyor or owner check | Never automatic, even above 0.995 |
| BRANCH | Same name key, different house or shop number or pin 150 m or more apart, different phone | Create or link as a site under `parent_entry`; do not merge |

**Calibration and error control** [I, arithmetic]:

- Estimating a precision of 99.5% within plus or minus 0.5 points at 95% confidence needs n = 1.96 squared times 0.995 times 0.005 over 0.005 squared = 764 labelled pairs in the top band. Plan for 800 per country-language.
- With zero errors in n samples the 95% upper bound on the error rate is about 3 over n (rule of three): 0.78% at n = 385, 0.38% at n = 800.
- Monthly audit of 385 auto-merged pairs per country group (the existing sample size). Trigger: if the upper bound of the error rate exceeds 1%, raise the line and stop AUTO until a re-calibration. The plan's trigger (reviewers reject more than 10% of auto-merges, plan 7.4) is 10 to 20 times too loose for the cost ratio above, and the code measures review-band candidates instead (F25).
- Recall: each quarter reviewers look at a random 1,000 entries per country and the top-5 embedding neighbours of each (a method different from blocking); the duplicates found divided by 1,000 is the residual duplicate rate.
- Gold set: 3,000 pairs per country-language, drawn from the AUTO, REVIEW and NO LINK bands plus random pairs, labelled by two people with disagreements settled by a third: about 50 hours, USD 150 to 750 [I at 60 s a pair, USD 3 to 15 an hour from the sibling note].

### 2.7 Review queue

| Item | Design |
|---|---|
| Task kind | `dedupe_review` (exists in `Task.Kind`, never created by code [C]) |
| Payload | Two entries side by side, the feature table, the evidence for each field, an LLM opinion with one-line reason, the "never merge" history |
| Order | Priority by the larger of the two entries' views and paid or claimed status, then by p closest to 0.85 (most informative) |
| Time budget | 40 s a pair on average; FAST REVIEW 15 s, full review 60 to 90 s [H] |
| Decision | merge (choose survivor), not the same (writes a negative judgement), link as branch, skip |
| Quality | 5% of tasks are seeded with known answers; two reviewers on 10% |
| Volume (100 million entries) | 6 million review pairs if 2% of 300 million source records land in the review bands [H]; at 40 s that is 66,700 hours, about 42 full-time years (USD 0.2 to 1.0 million at USD 3 to 15 an hour); with an LLM pre-opinion that makes 65% of them confident, about 15 full-time years (USD 70,000 to 350,000) [I] |

### 2.8 Merge and unmerge with provenance

**Tables to add** (names are proposals):

| Table | Columns | Purpose |
|---|---|---|
| `merge_event` | id, uid, survivor_id, absorbed_id, method (auto, review, staff, report), model_version, score, features jsonb, decided_by, applied_at, state (applied, reverted), reverted_at, reverted_by, reason | One row per merge; replaces `MergeMap` (keep it as a view for compatibility) |
| `merge_item` | merge_event_id, table_name, row_id, action (moved, copied, skipped_duplicate, field_overridden, carried), before jsonb | The snapshot that makes unmerge possible |
| `entry_redirect` | from_entry_id (PK), to_entry_id, via_merge_event_id, since, ever_public bool | One-hop resolution, flattened |
| `judgement` | entry_a_id, entry_b_id (ordered), verdict (same, not_same, unsure), decided_by, decided_at, merge_event_id, expires_at | The never-merge list and the evidence of every human decision (design precedent: nomenklatura judgements [R-search]) |
| `source_record` | id, source_id, external_id, entry_id (nullable), cluster_id, raw jsonb, keys, first_seen, last_seen | Immutable inputs; extends `ExternalRecord` and `ImportRow` |

**Merge steps** (one transaction, locks taken in id order, no global lock):

1. Refuse if either side matches a "NEVER" or "ALWAYS REVIEW" condition and the caller is automatic.
2. **Choose the survivor** by rule, not by age (fixes F14): claimed over unclaimed, then higher verification level, then more complete, then older. Staff may override.
3. **Move child rows** (the 11 sets in the current code) and record each moved row id in `merge_item`. Where the survivor already has an equal row (same phone, same hours), mark the dropped row `skipped_duplicate` and keep it, flagged, rather than deleting.
4. **Union categories.** Insert the absorbed entry's `entry_concept` rows into the survivor with `ON CONFLICT DO NOTHING`; the absorbed entry's primary becomes a secondary of the survivor if it differs. (The current code loses it, F12.)
5. **Field survivorship.** For each field choose the value with the best (verification level, recency, source rank, completeness). The loser value is kept as an alternate `ValueMeta` row with its source, so nothing is lost, and the overwritten survivor value is stored in `merge_item.before`.
6. **Verification.** Verification events are append-only and bound to facts that may differ. Copy the absorbed entry's still-valid events to the survivor as `carried` events (new rows pointing to the originals); never move them. Claims and consent: if exactly one side has a claim, it survives; both claimed is a NEVER; consent records are copied with `carried`.
7. **Credit.** Keep the existing rule: the earliest `added` credit survives, the later is marked duplicate (D6).
8. **Redirect.** Write `entry_redirect(absorbed, survivor)` and **flatten**: update every `entry_redirect` row that pointed to the absorbed entry to point to the survivor, recording `via_merge_event_id` (fixes F15).
9. Write `merge_event`, `ChangeLog` and one audit row on the **per-partition** hash chain (D-10; the global lock is the first row of the facts table in `Backend research/03_hosting_and_costs.md`).

**Unmerge steps** (staff action, also automatic when a "not the same" judgement is saved on a merged pair):

1. Lock both entries; require `merge_event.state = applied`.
2. Restore moved child rows by id from `merge_item`; delete rows created by the merge (`copied`, `carried`); restore overwritten fields from `before`.
3. Clear `merged_into`, restore `publish_state` from the stored value; re-point `entry_redirect` rows with this `via_merge_event_id` back to the absorbed entry; rows from later merges stay with the survivor.
4. Mark the event `reverted`, write a `not_same` judgement, add both to the review queue with a one-line reason.
5. Credits: restore `eligible` flags from the snapshot.
6. Cooling-off URL policy in section 3.

**Concurrency and cost.** No global lock; deadlock avoided by locking the lower id first. A merge writes about 30 rows and takes 20 to 80 ms [H]. `merge_event` and `merge_item` at 1% to 3% of 100 million entries a year are 1 to 3 million events and 12 to 36 million items, about 2 to 6 GB a year [I].

### 2.9 Cost per million records

Compute price: USD 0.0125 to 0.06 per vCPU-hour all in [I; the low end is the Oracle figure USD 0.025 per two-vCPU OCPU-hour and the high end is an AWS database instance at USD 0.52 an hour for 4 vCPU and 32 GB, both UNVERIFIED-A in `Backend research/03_hosting_and_costs.md`]. Review time USD 3 to 15 an hour (sibling note, S).

| Stage | Assumption | Per 1 million source records | Per 300 million |
|---|---|---|---|
| Normalise (fold twice, phone, domain, rule-based address) | 0.1 ms a record [H; fold is 7 µs, M] | 0.028 vCPU-h, USD 0.0004 to 0.002 | USD 0.1 to 0.6 |
| libpostal (optional) | 10,000 to 30,000 a second a thread [R] | 33 to 100 s, USD under 0.002 | USD under 0.5 |
| Blocking and scoring, Splink | 1 million a minute on a laptop [R]; 8 vCPUs; Spark at 100 million with 3 times overhead [H] | 0.13 vCPU-h, USD 0.002 to 0.008 | USD 1.5 to 7 |
| Embeddings (20% of records) | GPU 1,000 a second [H] | USD 0.02 to 0.06 | USD 6 to 18 |
| LLM pre-opinion on review-band pairs | 2% of records, 600 tokens in, 80 out, USD 0.001 to 0.005 a pair [I, from the Haiku prices in `docs/MASTER_DOCUMENT.md` as cited in the sibling note] | USD 20 to 100 | USD 6,000 to 30,000 |
| Human review without LLM | 20,000 pairs, 40 s each | 222 hours, USD 667 to 3,333 | USD 0.2 to 1.0 million |
| Human review with LLM (35% left) | | USD 233 to 1,167 | USD 70,000 to 350,000 |
| **Total with LLM** | | **about USD 253 to 1,267** | **USD 76,000 to 380,000** |

Reading [I]: compute is under 1% of the cost. The levers are the review-band share (each point of the 2% is worth USD 330 to 1,670 per million without LLM), the LLM pre-opinion, and the quality of keys that keep records out of the band. A one-off run for 100 million entries costs less than a month of the hosting estimate (USD 3,700 to 29,700, `Backend research/03_hosting_and_costs.md`).

---

## 3. Canonical IDs and stable URLs

### 3.1 Rules

| ID | Rule | Why |
|---|---|---|
| U1 | `uid` (ULID) is the only public identifier of an entry, never reused, never changes. `/e/{uid}/{slug}/` carries no place and no category (plan 8.2) | Moving place or category cannot break an entry URL |
| U2 | The slug is cosmetic: any wrong slug redirects to the current one (already built [C `catalog/views.py:318-319`]) | Renames are free |
| U3 | A merge leaves an `entry_redirect` row. Resolution is one lookup and one hop; chains are flattened at merge time | Fixes F15 |
| U4 | Redirects are kept for every entry that was **ever public** (published at any time) and, for drafts that were never visible, no redirect is needed: merge them with no tombstone URL | Drafts are not indexed (R08). If 5% of 100 million IDs were ever public and merged, that is 5 million rows, about 0.3 GB [I] |
| U5 | Cooling-off: for 30 days after a merge the old URL answers with a temporary redirect and a short cache lifetime; after 30 days it becomes a permanent redirect. An unmerge inside the window restores the old page cleanly | The current code sends a permanent redirect immediately, which caches in browsers and search indexes and makes undo messy [C; the 30-day length is H] |
| U6 | If the survivor is not public (suppressed, tombstoned), the absorbed URL answers 404 or 410, never a redirect to a hidden page | No leak through the redirect |
| U7 | Sitemaps list only canonical URLs; `lastmod` comes from the survivor | |
| U8 | External IDs (Overture GERS ID, Foursquare ID, OSM ID, Wikidata, register numbers) are stored in `entry_identifier` or `source_record` and follow the survivor on merge. A later reload of the same external ID resolves through `entry_redirect` | `ExternalRecord.entry` can point at a tombstone today [C] |
| U9 | List URLs `/{place path}/{list-type-slug}/` are not stable by themselves: add `place_slug_history` and `concept_slug_history` (old slug, parent, node id, until). A rename, move or merge of a place or list type inserts a row; the resolver tries the live slug, then history, then 404 | Plan 8.2; F19. One redirect hop, permanent after 30 days as U5 |
| U10 | Place merge needs a stored target: add `merged_into` to `Place` | `status=merged` has none (F19) |
| U11 | Stable node IDs: `Concept.uid` and `Place.uid` are the keys in links, APIs, and `entry_concept`; slugs are labels | D-05 |
| U12 | Immutable place keys in the path column: make `entry.place_path` an `ltree` of **immutable place ids** (for example `12.455.9021`), not slugs; slugs live in `Place` and are resolved at the URL layer | A rename then rewrites nothing; only a move rewrites |

Overture's GERS gives the pattern at scale: IDs intended to be stable across releases, a changelog per release partitioned by type and change type (added, removed, changed), and bridge files from source IDs to GERS IDs; a split or merge is traced in the changelog (1 ID to 2 new IDs) [R-search; page not opened]. Wikidata keeps a redirect for every merged item, on the stated ground that redirects make bad merges easier to untangle [R-search]. Both support U3, U4 and the `merge_event` snapshot.

### 3.2 Cost of moving things (arithmetic) [I]

| Operation | Rows touched | Cost |
|---|---|---|
| Rename a place (slugs only; with U12) | 1 `Place` row, 1 history row | trivial |
| Rename a place (today: slug path copy) | every entry below it: for 1 million entries about 1.67 GB of WAL (1,180 B heap plus 490 B of indexes a row, section 2 of the hosting note) | 3 to 10 minutes in batches [H] |
| Move a place subtree (any design) | the same, plus roll-up cells | batch with progress marker |
| Rename a list type or concept | 1 `Concept` row, 1 history row | trivial |
| Move a node under a new parent | `concept_closure` rows of the subtree: nodes in subtree times depth (a 2,000-node subtree at depth 6 is 12,000 rows) | trivial; **do not store ancestor arrays on membership rows**, or a node with 5 million members costs 5 million updates |
| Merge two list types | re-point `entry_concept` rows of the loser (members of the node) in batches; slug history row | proportional to members |
| Split a list type | members stay on the parent until reassigned; no loss | |
| Merge two entries | about 30 rows | 20 to 80 ms |

---

## 4. Many-to-many entry-to-category model

### 4.1 Two axes

- **Place axis** is derived, not stored per list: an entry has one `place` (and `AreaServed` rows for where it sells). It appears in the list of every ancestor place automatically through the path prefix. This is the "Hotels logic" and it is why one hotel is on Hotels-Global, Hotels-Pakistan, Hotels-Punjab, Hotels-Lahore and Hotels-Gulberg with no extra rows.
- **Category axis** is stored many-to-many: an entry belongs to one **primary** node and any number of **secondary** nodes. Depth (thousands of product nodes) multiplies memberships, so this is the table that grows.
- Overlapping business districts are not a tree. If a district is a polygon that can overlap another, derive an `entry_zone(entry_id, place_id)` table by polygon containment (PostGIS `ST_Contains`, computed, not authored) [H, P2].

### 4.2 Table

`entry_concept` (replaces the auto-created `entries_entry_secondary_concepts`; the plan's `entry_concept` in 4.2.4 has the same intent but no columns):

| Column | Type | Note |
|---|---|---|
| country_code | char(2) | partition key (plan 4.1) |
| concept_id | int | the node (list type, product family, product or variant; `Concept.kind`) |
| entry_id | bigint | |
| role | smallint | 1 primary, 2 secondary, 3 inferred (from `Product` or `Speciality` rows, shown only after review) |
| rank | smallint | owner's order among secondaries (for the entry page), not a paid rank |
| state | smallint | proposed, accepted, rejected |
| source | smallint | owner, contributor, surveyor, agent, import, inferred |
| evidence_ref | bigint null | the `Product` row, certificate or source record that supports it |
| confidence | real null | |
| added_by, added_at, valid_to | | audit and expiry |
| **denormalised:** place_path (ltree), published bool, best_level smallint, last_verified_at, sort_key | | copied from the entry by the service layer, reconciled nightly (same technique as `Entry.place_path` today) |

Constraints and indexes (partition `LIST` by `country_code`, so the primary key includes it):

| ID | Index | Serves |
|---|---|---|
| I1 | primary key `(country_code, concept_id, entry_id)` | membership test, uniqueness, intersections |
| I2 | `(country_code, entry_id)` | an entry's categories (entry page chips, merge, delete, move) |
| I3 | `(country_code, concept_id, place_path, sort_key, entry_id) WHERE published` | **the list page**: node at place, keyset paging |
| I4 | partial unique `(country_code, entry_id) WHERE role = 1` | exactly one primary |
| I5 | partial `(country_code, state) WHERE state = 'proposed'` | review queue |
| I6 | `(country_code, concept_id, last_verified_at) WHERE published` | "recently checked" sort |

Keep `Entry.primary_concept` as a denormalised copy of the role-1 row for the existing `entry_list_query` index and for backward compatibility; the service layer keeps both in step, and a nightly check counts mismatches (metric M12).

**Size** [I, row arithmetic as in the hosting note section 2.1]: heap tuple about 24 + 56 = 80 bytes plus 4 for the line pointer; I1 about 36 bytes, I2 about 36, I3 and denormalised columns about 40; total about 160 bytes a row.

| Memberships per entry (mean) | Rows at 100 million entries | Size at 160 B |
|---|---|---|
| 2 | 200 million | 32 GB |
| 3 (assumed) | 300 million | 48 GB |
| 5 | 500 million | 80 GB |

For comparison the entry tables are 175 GB by the plan and about 660 GB by the hosting note's row arithmetic, so membership is 7% to 28% of the entry data [I]. Mean memberships are a hypothesis (hotels 2 to 3, restaurants 1 to 2, a leather-goods maker 8 to 15); measure after the first import.

### 4.3 Query patterns

| ID | Query | Plan | Expected cost |
|---|---|---|---|
| Q1 | List page: node C (and its descendants if C is above leaf) at place P, published, ordered, 50 rows | Index range scan on I3 with `place_path <@ P`; keyset on `(sort_key, entry_id)`; then fetch 50 entries by primary key | about 2 ms per leaf node at city level [H, same order as the plan's measured 1.7 ms for the list query] |
| Q1b | Same for a node with many descendants (a family such as "Manufacturing") | Do not expand to thousands of ids; read the pre-computed `list_top` cache or the roll-up page. Only leaf and near-leaf nodes run live | |
| Q2 | Entry's categories (page chips, "also makes") | I2 | one index scan, 1 to 15 rows |
| Q3 | Counts per (place, node) | `rollup_cell`, never `count(*)` (plan 4.4). The recount joins `entry_concept`, counting distinct entries | the plan estimates 31 cell updates per entry (7 place levels times 4.5 concept levels) [I]; with 3 memberships that is up to 93 increments an entry, 9.3 billion for 100 million entries, so recount by set-based `GROUP BY` per country, not per entry |
| Q4 | Area chips: child places having entries in node C | `rollup_cell` filtered by parent paths | |
| Q5 | Entries in both X and Y (manufacturers of gloves and jackets) | Self-join on I1 `(concept_id, entry_id)`, driving from the smaller node | O(min of the two nodes) |
| Q6 | Facet filter (material, certification, minimum order) within Q1 | `entry_facet(entry_id, facet_key, value_id)` with index `(facet_key, value_id, entry_id)`; facets are not nodes (D-03) | planner picks the more selective side; cap to two facets per page |
| Q7 | Search inside a node and place | Trigram or search engine scoped by I3 candidates, never unscoped | scoped sets stay under about 1 million |
| Q8 | Add a membership | insert with `ON CONFLICT`; check caps; update denormalised copy | |
| Q9 | Entry moves place or changes publish state | `UPDATE entry_concept ... WHERE (country, entry_id)` via I2: 1 to 15 rows | |
| Q10 | Merge two entries | Section 2.8 step 4 | |

Why the denormalised columns: a leaf node can have 50,000 members in a country; a list for one district selects 500 of them. Without `place_path` in the index the planner must fetch 50,000 entry rows (random reads at about 0.05 ms each when cached is 2.5 s) to filter 500 [I]. With I3 it reads 500 index entries [I; planner behaviour H, verify with `EXPLAIN`].

Concept ancestors: keep `concept_closure(ancestor_id, descendant_id, depth)` (nodes times depth, for 100,000 nodes at depth 6 about 600,000 rows). The current `descendant_concept_ids` runs one query per level (`analytics/rollups.py:42-47`); cache the result per node in process memory and invalidate on taxonomy version change.

### 4.4 Primary and secondary semantics, and abuse limits

| Rule | Default |
|---|---|
| Primary = what the entry mostly is: breadcrumb, entry title, `primary_concept` copy, list "total" for the payout scope | exactly one |
| Secondary = also listed here | cap 25 for most list types; manufacturers up to 100 with evidence |
| Public on a list page | a secondary membership is shown on list pages only when `state = accepted`: backed by a `Product` or `Speciality` row, a certificate, or a surveyor, owner or AI check that names it. An owner-declared membership without evidence shows on the entry page as "claims" and nowhere else |
| Category stuffing | memberships spanning more than 3 unrelated families (distance in the concept tree) raise the fraud score (section 7.4) |
| Order inside a list | by quality score and check level, then name; never by `rank`, and paid placement stays a labelled slot (rule 4) |

---

## 5. Data freshness

### 5.1 Staleness arithmetic [I]

If a fact changes at a rate λ per year and is re-checked every T years, the average share of stale values is 1 minus (1 minus e^(−λT)) over λT, which is about λT/2. For an average stale share of 5% choose T of about 0.1 over λ (checked numerically: for λ from 0.05 to 2 the average stale share is 4.84% at T = 0.1/λ, and the share stale just before a re-check is 9.5%).

| λ per year | Re-check every | Stale share just before re-check |
|---|---|---|
| 0.05 | 24 months | 9.5% |
| 0.1 | 12 months | 9.5% |
| 0.2 | 6 months | 9.5% |
| 0.5 | 73 days | 9.5% |
| 1.0 | 36 days | 9.5% |

### 5.2 Rates and schedule by field type

Observed rates for business directories are hard to find. The figures I found are for B2B **contact** databases from aggregators and vendors, not for business listings: contact data decays about 2.1% a month, 22.5% a year; "20.7% of business postal addresses change in a year" [S, search summaries from landbase.com, airscale.io and similar; UNVERIFIED, not opened]. Treat the table below as hypotheses to be replaced by measurement: re-check a random 385 entries per list type every half year and fit λ.

| Field group | λ per year (H) low-churn types / high-churn types | Interval for 5% average stale | Method (cheapest first) | Existing code |
|---|---|---|---|---|
| Existence and status (open, closed, moved) | 0.04 to 0.08 (hospitals, schools, factories) / 0.15 to 0.30 (restaurants, retail, hyper-local trades) | 12 to 24 months / 4 to 8 months | Website liveness and register status; phone reachability; surveyor call on trigger | `status`, `status_date`; checks expire at 180 or 365 days |
| Phone reachability | 0.10 to 0.15 / 0.20 to 0.30 | 8 to 12 / 4 to 6 months | Relay test delivery (`delivery_event`); automated number-type check; surveyor call | `Contact.verified_at` |
| Website liveness | 0.10 to 0.20 | monthly to quarterly (cheap) | HTTP status, redirect target, DNS, page hash | `Social.last_link_check` only for social |
| Address and pin | 0.05 to 0.10 | 12 to 24 months | Geocode agreement, surveyor visit on trigger | `coord_date`, `precision_class` |
| Opening hours (if shown) | 0.20 to 0.40 | 3 to 6 months | Page diff; owner confirmation | `Hours.confirmed_on` |
| Prices | 1 to 4 | 18 to 36 days, or show the date and promise nothing | Owner update; page diff | `price_date` (plan requires a date) |
| Services and products | 0.20 to 0.30 | 4 to 6 months | Page diff then extraction | `Product.price_date`, none for presence |
| Identifiers and certificates | event-driven | at `valid_to` minus 30 days and the day after; register diff monthly | Register lookup | `Identifier.valid_to`, `last_checked` |
| Name and legal form | 0.03 to 0.05 | 24 months | Register match | |
| Category memberships | 0.10 | 12 months for secondaries with `valid_to` | Page diff against product list | none |
| Ownership and claim | event-driven | on OTP failure or dispute | | `Claim` |

By list-type class: **health, education, institutions and factories** use the low-churn column and a 12-month cap (the existing surveyor validity is 365 days); **retail, food, hospitality and trades** the high-churn column; **individuals** only on consent events and a yearly confirm (gated).

The existing code uses one validity per level (AI 180, surveyor 365, owner 365, grace 90) for every field group and list type (F20). Replace with a table `freshness_policy(list_class, field_group, interval_days, method)`.

### 5.3 Scheduling at 100 million

| Item | Design |
|---|---|
| Table | `entry_freshness(entry_id PK, tier, next_due_at, last_checked_at, fail_count, risk)`; one row per entry, not per field; `next_due_at` is the minimum over field groups; partial index `(country_code, next_due_at) WHERE tier < 4`. 100 million rows at about 56 bytes plus index about 7.6 GB [I] |
| Claim | Workers take batches of 500 with `FOR UPDATE SKIP LOCKED` (the pattern `take_next_task` already uses), sharded by country |
| Priority | `tier` from traffic (views 90 days), paid or claimed, number of lists the entry is on, list-type λ, recent failure signals (dead link, upheld report, failed relay delivery) |
| Diff first | Fetch, normalise, hash. Unchanged hash and a previous good extraction means no model call, only a refreshed `last_checked_at`. Changed hash means extraction by the agent and an AI check on a source different from the draft (R07) |
| Politeness | Per-domain queues and delays; many entries share one domain, so fetch each URL once per cycle; robots respected (existing fetcher rules, plan 7.6) |
| Expiry | Set-based SQL in 100,000-row chunks, each its own transaction; no scan of published entries; a published entry whose every check has expired past grace is selected by an indexed query on `entry_freshness`, not by a Python loop |
| Draft on expiry | Keep plan 6.4 (stays published through grace, then draft), but apply to tier-1 and tier-2 only. For tier 3 show the date ("AI-checked 2026-04") and the label "Not verified yet" when expired, and leave the entry public |

**Why the change is needed** [I]: `sweep_expired` today (F21) loads all published entries into memory (250 GB at 100 million, 2.5 KB each) and runs at least two queries each: about 200 million queries, 16.7 hours at 0.3 ms, scheduled hourly. At steady state with 2 current verification rows per entry and about 240 days average validity there are about 0.83 million expiry events a day, which is trivial as set-based SQL.

### 5.4 Cost at 100 million [I]

Unit costs: a cheap automated check (HTTP, DNS, hash, register diff) USD 0.0002 [H]; an AI check USD 0.03 to 0.10 (plan 7.6 "short capped jobs cost USD 0.03 to 0.10 all-in", S); a surveyor call 5 minutes at USD 3 to 15 an hour.

| Scenario | Events a year | Cost a year | Per entry-year |
|---|---|---|---|
| **A. Existing rule applied literally**: every published entry AI-rechecked every 180 days to stay public | 200 million AI checks (548,000 a day) | USD 6 to 20 million | USD 0.06 to 0.20 |
| **B. Tiered, diff-first**: tier 1 (1% = 1 million) 12 cheap checks a year; tier 2 (9% = 9 million) 4; tier 3 (90% = 90 million) 1 | 138 million cheap checks (378,000 a day, 4.4 a second average) | USD 27,600 | |
| B, model calls: 60% of entries have a fetchable site, 25% of fetched pages changed | 20.7 million AI checks | USD 0.62 to 2.07 million | |
| B, humans: 0.5% of entries a year targeted (500,000 calls) | 41,700 hours, 26 full-time years | USD 125,000 to 625,000 | |
| **B total** | | **USD 0.77 to 2.72 million** | **USD 0.008 to 0.027** |

Scenario B is 2 to 60 times the yearly infrastructure at 100 million entries (USD 3,700 to 29,700 a month, USD 44,000 to 356,000 a year, hosting note section 8), consistent with that note's finding that AI cost dominates. Set a freshness budget: alert at USD 0.02 and stop expansion at USD 0.03 per entry-year, in addition to the agent stop at USD 0.30 per verified record (rule 6). The 25% change rate and 60% website share are hypotheses; measure them in the pilot.

---

## 6. Verification workflow at scale

### 6.1 Human capacity [I]

| Minutes per check | Part-time surveyor (44 h a month) | Full-time (132 productive h a month) |
|---|---|---|
| 3 (website and register confirm) | 880 a month | 2,640 |
| 6 (phone call with retries) | 440 | 1,320 |
| 8 (hard case, evidence text) | 330 | 990 |

Sources for minutes: 1 to 3 minutes per audit record and 3 to 8 per labelling item are the sibling note's figures [S, `04_agent_training_and_ai_auditor.md`]; 6 for a phone check is mine [H]. Hours a full-time year: 132 times 12 = 1,584.

| Question | Arithmetic |
|---|---|
| Check every one of 100 million entries once by hand at 6 min | 10 million hours = 6,313 full-time years |
| Check tier 1 (1 million) once | 100,000 hours = 63 full-time years |
| Targeted 0.5% a year (500,000) | 41,667 a month = 95 part-time surveyors at 440 a month |
| Dedupe review (section 2.7) | 15 to 42 full-time years |

So **Surveyor-verified stays a minority label** by arithmetic, not by policy: it is reserved for tier-1, high-risk list types (health, licences, large manufacturers), disputes and audits. The large majority of the 100 million entries will be AI-checked or Not verified yet, and the pages must say so (rule 4 stays as it is).

### 6.2 Queue design

| Item | Today | Proposed |
|---|---|---|
| Task kinds | verify, survey, dedupe_review, area_review, translate (only verify is created by `queue_unchecked`) | add `closure_confirm`, `audit`, `fraud_review`, `claim_review` |
| Order | oldest first | priority = risk, traffic, tier, age; SLA `due_at` per kind |
| Affinity | none | place subtree (steward grants, existing `StewardGrant`), language (ur, en, ar), list type, skill level |
| Lease | assigned forever | 24-hour lease, then back to open; a surveyor holds at most 10 |
| Fairness and independence | not the creator (R07) | plus not a verifier of the previous check on this entry, not the same pair twice in 30 days (the plan's weekly pair report) |
| Corroboration | one person can close | `closed` and `wrong` outcomes on tier-1 or high-risk entries need a second signal (second surveyor, or phone unreachable twice 48 hours apart, or register or site evidence) before `status` changes |
| Volume | 100 tasks a day cap | no cap on creation; cap on open tasks per place so queues are worked; Postgres `SKIP LOCKED` is far above the needed rate (about 1,400 tasks a day at 41,700 a month) |
| Metrics | `Task.minutes` | per-kind throughput, p90 age, backlog over capacity, minutes per task |

### 6.3 Sampling

- **Estimate** accuracy with the existing 385 per stratum (95% confidence, plus or minus 5 points). With hundreds of strata (source times list type times country times creation path) that is too many: 2,000 strata times 385 is 770,000 audits a period.
- **Accept or reject** with lot-quality sampling: with zero failures in n records the lot is at least p accurate at 95% confidence when n = ln(0.05) over ln(p): 29 for 90% (0.9^29 = 0.047), 59 for 95%, 299 for 99% [I; the n = 29 plan is a standard zero-defect plan, R-search]. Use **29 per stratum per period**, escalate to 385 on any failure, and stop the job kind below 90% (rule 6). 2,000 strata times 29 is 58,000 audits at 3 minutes: 2,900 hours, about 1.8 full-time years [I].
- Stratify by: source, list type, country, creation path (`created_via`), verifier, tier, model version.
- Oversample new sources and new model versions (first 3 batches) and entries with high risk scores.
- Seeded errors: 5% canaries as today (`CanaryEntry`, F24); add dedupe canaries (known same and known different pairs) for reviewers.

### 6.4 Entry quality and confidence

Two internal numbers per entry, **never shown as a fifth label** and never changed by paid rank (rule 4):

| Score | Definition | Use |
|---|---|---|
| `quality` (completeness) | share of required-for-publish and recommended fields present for the list type, each weighted. Replaces `row_quality` in `bulk.py:60-65`, which is 0.4 plus 0.6 times four flags | Publish bar, import batch quality |
| `confidence` | probability that the entry is correct and live today: log-odds sum, then logistic | List order tie-break (with check level), freshness tier, sampling weight, fraud review order |

`confidence`: L = L0(source) + sum over checks of w(level) times exp(−λ(field) times age) + sum over agreements of w(agree) − sum of penalties; p = 1/(1 + e^(−L)).

| Term | Initial weight (H) |
|---|---|
| L0 | logit of that source's measured audited accuracy (`accuracy_by_source`, exists [C `volunteers/services.py:182`]) |
| Surveyor check, per field group | +2.0 |
| Owner check | +1.5 (independent of the entry's creator) |
| AI check on a different source | +0.8 |
| Register match | +1.2 |
| Second independent source agrees on name and place | +0.6 (max 3) |
| Failed link or unreachable relay | −1.0 |
| Report upheld | −3.0 |
| Surveyor outcome `wrong` | −4.0 |
| Conflicting source | −0.8 |

Worked example: source accuracy 0.80 gives L0 = 1.386; an AI check 40 days ago at λ = 0.5 per year gives 0.8 times 0.947 = 0.76; a register match +1.2; L = 3.34, p = 0.966. Weights are placeholders; **fit them** by logistic regression on audited outcomes (`AuditSample.correct`, 5,000 or more labels) and require calibration: of entries scored 0.95 to 1.0, at least 95% correct on audit; expected calibration error at most 0.05 [H].

### 6.5 Fraud signals for fake supplier listings

Context: an email, a phone number and a self-declared company name establish almost nothing, and supplier verification is where B2B marketplaces carry most of their fraud exposure [S, search summary of vendor blogs]; Google reported blocking more than 12 million fake business profiles in 2023 [R-search], removing over 7 million fake profiles in a year with more than 630,000 found through user reports [R-search, other year not stated].

| Signal | Computed from | Tier | Repo hook |
|---|---|---|---|
| Phone or email on many unrelated entries (fan-out of 3 or more with different name keys), or across countries | K1 hub flag | strong | `Contact.value_hash` (needs kind-free hash, F8) |
| Website domain registered under 90 days, parked, template site, or shared IP, hosting or analytics id with other listings | RDAP and fetch metadata | strong | `agents/fetcher.py` |
| Description or product text nearly identical to another firm (MinHash Jaccard over 0.8) | text shingles | strong | `Entry.description`, `Product` |
| Address shared by many unrelated entries, residential, virtual office, co-working or post-office-box pattern; pin at a centroid or more than 1 km from the geocoded address | address key K7, geo | medium | `Entry.address_text`, `precision_class` |
| Category stuffing: more than 25 secondary memberships, or memberships in more than 3 unrelated families, without evidence | `entry_concept` | strong | section 4.4 |
| Capacity claims inconsistent with size (a "10,000 pieces a day" firm with `size_band` under 10; year established earlier than the domain and the register) | add-ons, `size_band`, `year_established` | medium | `Entry.addons` |
| Registration identifier fails its check digit or register lookup, is reused by another entry, or names a different business | `Identifier`, register | strong | `Identifier.last_checked` |
| Price far below the list median (z-score under -3) | price band, `Product` | medium | `Product.price_band` |
| Claim behaviour: many claims from one device or address cluster, claim within 60 seconds of creation, OTP to a number different from the stored contact, disposable email | `Claim`, request metadata | strong | `Claim`, `core/clientip.py` |
| Creator or verifier pattern: same contributor and verifier pair repeating; bursts of more than 50 entries an hour from a new account | `CreditEvent`, `Task` | strong | plan 6.4 weekly pair report |
| Paid placement bought by a new entry that has no check beyond AI | `placement`, age | rule | `access/placements.py`: require Owner-verified or Surveyor-verified plus 30 days age before any placement |
| Images are out of scope (no pictures, rule C29), so no image forensics | | | |

Score and action [H]: `risk` from 0 to 1 by a hand-weighted model first, then logistic regression on reviewer outcomes. Under 0.3 pass; 0.3 to 0.6 hold for an AI check on a different source; 0.6 and above fraud review; 0.85 and above suppress (`publish_state = suppressed`, reversible) with an appeal path. Measure precision of auto-suppression on reviewer outcomes (at least 90% upheld).

### 6.6 Abuse by competitors

| Attack | Why it works | Defence |
|---|---|---|
| False "closed", "wrong", "fake" reports to demote a rival | Google users report rivals as permanently closed; "it only takes a few reports" [S, Dark Reading summary, older article]; Google blocked more than 100 million abusive edits in 2021 [R-search] | A report never changes state alone. Reporter reputation (account age, verified phone, share of past reports upheld), weighted. Closure needs a second independent signal (section 6.2). Cap reports per reporter and per target per day; honeypot and rate limits exist [C, plan 15] |
| Mass reporting from one network | | Count distinct accounts, devices and /24 networks; 10 reports from one subnet count as 1 |
| Claim hijack of a rival's entry | Google reported more than 2 million attempted claims by hackers in 2023 [R-search] | OTP only to the stored contact; documents route to a moderator; new owner's first edits on phone, website and status are held for 7 days with notice to the old contact; dispute queue exists (`claim_dispute`) |
| Merge-away: suggest a rival as a duplicate of a weak entry | merges move data and redirect URLs | Merges involving a claimed, paid or checked entry are always reviewed; merge window with unmerge (section 2.8) |
| Edit wars through suggested edits | | Changes to phone, website, status and name on a claimed entry go to owner approval; edit velocity limits per user and per entry |
| Category cannibalisation: add a rival's firm to irrelevant nodes or stuff your own | | Secondary memberships need evidence (section 4.4); membership changes on claimed entries notify the owner |
| Fake reviews | | Reviews are gated (verified users, one per user); separate from paid rank (Q-P3) |
| Bad surveyor | One surveyor can close an entry (F23) | Canaries (exist), pair report, two-person rule, accuracy under 80% suspends (exists) |

---

## 7. Data-quality dashboard: definitions and thresholds

All metrics are computed per country partition from projections (nightly SQL), with an "as of" time. Thresholds are hypotheses (H) except where marked as existing rules.

| ID | Metric | Definition | Green | Amber | Red (action) | Exists |
|---|---|---|---|---|---|---|
| M1 | Audited accuracy | audited-correct share by source, list type, country, creation path; LQAS gate of 29 then 385 | at least 95% | 90 to 95% | under 90%: stop the job kind (rule 6) | Partly: bulk batch audit and `accuracy_by_source` |
| M2 | AI-auditor agreement | auditor recall of wrong records, precision, Cohen's kappa against humans (sibling note) | recall at least 0.80, precision at least 0.70, kappa at least 0.6 | | below: retrain or stop | Not built |
| M3 | Residual duplicate rate | duplicates found per 1,000 sampled entries by embedding top-5 review | at most 1% | 1 to 3% | over 3%: lower thresholds, add keys | Not built |
| M4 | False-merge rate | (unmerges plus audit-found wrong auto-merges) over auto-merges, 90-day window; upper 95% bound from the 385 audit | at most 0.5% | 0.5 to 1% | over 1%: stop AUTO, recalibrate | Not built (F25) |
| M5 | Review backlog | p90 age of `dedupe_review` and `fraud_review`; open over weekly capacity | under 7 days | 7 to 21 | over 21 days: add reviewers, widen FAST REVIEW | Not built |
| M6 | Expired-check share | published entries with no unexpired check over published | under 10% | 10 to 25% | 25% and over (early warning in plan 7.7 and monitoring) | Built (25% alert) |
| M7 | Overdue ratio | entries past `next_due_at` over all entries, by tier | tier 1 under 2%, tier 2 under 5%, tier 3 under 15% | 2 to 3 times those | over 3 times: scheduler or budget problem | Not built |
| M8 | Check mix | published share by label: Surveyor, Owner, AI, none; by tier | informational; tier 1 at least 60% surveyor or owner | | | Partly: `RollupCell.by_level` |
| M9 | Completeness | share of required-for-publish fields filled, per list type | at least 85% | 70 to 85% | under 70% | Partly: `with_contact_pct` |
| M10 | Geo quality | share with building-level or better pin; centroid-hub share; share of audited pins within 100 m of the surveyor's | at least 70%, hubs under 2%, at least 90% | | | Not built |
| M11 | Reachability | relay delivery success on a monthly 1% sample of entries | at least 80% | 60 to 80% | under 60% | Not built |
| M12 | Membership quality | mean memberships; share over cap; share of secondaries with evidence; audited correctness of sampled entry-node pairs; mismatches between `primary_concept` and role-1 row | audited at least 95%; evidence at least 80%; mismatches 0 | | any mismatch is a bug | Not built |
| M13 | Fraud | risk-tier counts; precision of auto-suppress on reviewer outcomes; time to takedown; claim-hijack attempts blocked; reporter reject ratio | precision at least 90% | 80 to 90% | under 80%: raise thresholds | Not built |
| M14 | Cost | cost per verified record (agent-only and all-in); freshness cost per entry-year; review minutes per pair; cost per merge | agent-only under USD 0.20; freshness under USD 0.02 | to USD 0.30; to USD 0.03 | over USD 0.30 stops the job kind (rule 6); freshness over USD 0.03 stops expansion | Partly: `cost_per_verified`, `ai_spend` |
| M15 | Verifier quality | canary accuracy, tasks per hour, minutes per task | canary at least 0.8 | | under 0.8 after 3 tasks suspends | Built (canary) |
| M16 | Redirect health | chains longer than one; absorbed IDs returning 404; broken external-ID maps | all zero | | any: bug | Not built |
| M17 | Search zero-result rate | share of searches with no result | under 10% | 10 to 15% | 15% and over (plan 7.7) | Built |
| M18 | Pipeline latency | time from source record to cluster decision; p95 | under 1 hour online, under 24 hours batch | | | Not built |

---

## 8. Requirements table (checked against the repository)

| ID | Requirement | Priority | State | Evidence |
|---|---|---|---|---|
| ER-01 | Phone key without contact kind, plus hub guard and fan-out cap | P0 | Not built | F8, F9 |
| ER-02 | Name layers F1 to F4 (name key, skeleton, Urdu and Arabic skeleton, alias table) | P0 | Partly (F0 only) | `core/textfold.py` |
| ER-03 | Address normaliser (rules, optional libpostal) | P1 | Not built | |
| ER-04 | Geo keys (H3 cell, precision gating, centroid-hub exclusion) | P0 | Not built | F7, F26 |
| ER-05 | Streaming blocking engine with key table and block caps | P0 | Partly (place and concept block only) | F2, F4 |
| ER-06 | Batched features, no per-pair queries | P0 | Not built | F3 |
| ER-07 | Splink batch pipeline with labelled-set evaluation | P1 | Not built | |
| ER-08 | Calibrated thresholds, hard rules and gates | P0 | Partly (constants only) | F1, F9 |
| ER-09 | Merge v2: snapshot, survivorship, category union, verification carry, redirect flattening, no global lock | P0 | Partly (`merge_entries` v1) | F11 to F15 |
| ER-10 | Unmerge service, judgement store, never-merge list | P0 | Not built | F13 |
| ER-11 | Staging-level resolution in bulk and loaders | P0 | Partly (stage, sample, publish exist) | F10 |
| ER-12 | `entry_concept` table with roles, caps, evidence; list pages and roll-ups read it | P0 | Partly (unused M2M field) | F16 |
| ER-13 | Slug history and redirect tables for places and concepts; place `merged_into`; `entry_redirect` | P0 | Partly (entry redirect, one hop) | F15, F19 |
| ER-14 | Freshness policy table, `entry_freshness`, set-based expiry, scheduler | P0 | Partly (expiry loop) | F20, F21 |
| ER-15 | Diff-first checker and per-check cost counters | P1 | Not built | |
| ER-16 | Verification queue v2: priority, lease, affinity, two-signal closure | P1 | Partly | F22, F23 |
| ER-17 | LQAS acceptance sampling (29 then 385) | P1 | Partly (385 only) | F24 |
| ER-18 | Entry quality and confidence scores with calibration | P1 | Partly (`row_quality`) | `bulk.py:60-65` |
| ER-19 | Fraud and risk signals service | P1 | Not built | |
| ER-20 | Report-abuse defences and reporter reputation | P1 | Partly (rate limit, honeypot) | `moderation` |
| ER-21 | Quality metrics M1 to M18 | P1 | Partly (3 metrics) | F25 |
| ER-22 | Audit hash chain per partition (no global advisory lock) | P1 (D-10) | Not built | F10 |

---

## 9. Gaps and conflicts

| # | Item |
|---|---|
| G1 | Plan 6.7 says "Un-merge is possible from the log". The log does not hold what is needed (F13). Correct the plan or build ER-09 and ER-10. |
| G2 | Plan 7.4 trigger "reviewers reject more than 10% of auto-merges" is looser than the cost ratio supports, and the dashboard computes it on review-band candidates, not auto-merges (F25). |
| G3 | The plan names an `entry_concept` table (4.2.4); the code has an unnamed auto-created join table that nothing uses (F16). |
| G4 | Size per entry: plan 1.7 KB, hosting note 6.6 KB. I show both where sizes matter. |
| G5 | Plan 6.4 says an entry returns to draft when every check has expired past grace; at 100 million entries that forces repeated AI checks on every entry (scenario A). Section 5.3 proposes limiting this to tiers 1 and 2. This changes a rule in plan 6.4 and `GRACE_DAYS` behaviour: it needs the founder (section 11). |
| G6 | Splink version: search shows 4.0.7, the fetched README refers to Splink 5 (announced 2026-09-28). UNVERIFIED which is current. |
| G7 | Decay rates are from B2B contact data, not business listings. No source found for restaurant or factory closure rates. All λ values are hypotheses. |
| G8 | Embedding quality for Urdu names (e5, bge-m3, LaBSE) was not found in any source I could open. Must be measured. |
| G9 | libpostal accuracy on Pakistani or Gulf addresses and the licence of its model data are UNVERIFIED. |
| G10 | Overture's conflation libraries are named in a search summary; I could not locate the repository (GitHub search returned nothing) or read `docs.overturemaps.org`. |
| G11 | Some of the Google figures are from different years and from news summaries of Google's own reports, not the reports. |
| G12 | The loader's place assignment (F26) is a precondition of the block-size skew; fixing blocking keys does not fix coarse place assignment. |

---

## 10. Work packages with acceptance tests mapped to the repository

Sizes: S under 1 week, M 1 to 2 weeks, L 2 to 4, XL over 4, one engineer. All tests are new `pytest` functions in the named existing test folders unless stated. No code is written by this note.

| WP | Work | Files | Size | Depends | Acceptance tests |
|---|---|---|---|---|---|
| ER-01 | `Contact.number_hash` (kind-free keyed hash) with backfill; hub flag (`fan_out`); use in `dedupe.features` | `entries/models.py`, `entries/services.py` (`add_contact`), `intake/dedupe.py`, migration | M | | `test_same_number_different_kind_matches` (mobile on one, whatsapp on other); `test_number_on_four_unrelated_entries_is_not_a_key`; `test_shared_switchboard_never_auto_merges`; extend `intake/tests/test_import_dedupe.py` |
| ER-02 | `name_key`, `name_skeleton` for Latin, Roman Urdu, Urdu, Arabic; alias table; `Entry.name_key` and `NameVariant.key` | `core/textfold.py`, `entries/models.py`, `core/tests` | L | | 650-pair gold file (500 plan + 150 cross-script): precision at least 95%, `test_gold_pairs_precision`; `test_co_vs_company_same_key`; `test_al_noor_traders_vs_pharmacy_not_same_key_after_category`; `test_short_skeleton_needs_second_signal`; existing `test_urdu_spelling_variants_match_after_fold` still passes |
| ER-03 | Address token normaliser and comparison; optional libpostal adapter behind an interface | `core/addressnorm.py` (new) | M | | 40 Pakistani and Gulf address pairs: `test_house_number_mismatch_is_negative`; `test_abbreviations_expand`; adapter test skipped when libpostal is absent |
| ER-04 | H3 cell column (or geohash 7), centroid-hub exclusion, precision gating | `entries/models.py`, `intake/dedupe.py` | M | | `test_centroid_pin_not_used_for_blocking`; `test_neighbour_cell_pair_found`; `test_area_precision_never_scores_distance` |
| ER-05 | `entry_key` table, key-join candidate generation, streaming `scan_all` (`iterator`, per-country chunks), block cap 500 with sub-block by cell | `intake/dedupe.py`, `intake/models.py` | L | ER-01, 02, 04 | `test_scan_all_never_exceeds_block_cap_pairs`; `test_scan_all_memory_is_bounded` (`tracemalloc`, 20,000 synthetic entries stay under 200 MB); `test_pairs_completeness_on_gold_set` at least 98% |
| ER-06 | `features()` batched: one prefetch per block, no per-pair queries | `intake/dedupe.py` | S | | `assertNumQueries` constant in block size (`test_features_query_count_independent_of_pairs`); performance test: 5,000-entry block scored under 60 s |
| ER-07 | Splink DuckDB job writing `dedupe_candidate`; EM training; evaluation against gold set | `scripts/er/` (new), `intake/models.py` | L | ER-05 | 1 million synthetic records in under 15 minutes on 8 vCPU (documented run); precision at p 0.995 at least 99.5% and recall at least 90% on gold; `test_splink_candidates_match_sql_features` on a 1,000-record fixture |
| ER-08 | Thresholds and rules in `score`: veto, ALWAYS REVIEW, BRANCH, person and claimed gates; model version on every candidate | `intake/dedupe.py`, `intake/importer.py` | M | ER-01 | `test_person_never_auto_merges`; `test_claimed_entry_always_review`; `test_different_licence_numbers_veto`; `test_same_name_other_address_links_as_branch`; `test_stored_not_same_judgement_blocks`; keep `test_similar_name_without_phone_goes_to_review_not_merge` |
| ER-09 | Merge v2: `merge_event`, `merge_item`, `entry_redirect` (flattened), survivor rule, category union, field survivorship, carried verification and consent, per-entry lock order, per-partition audit | `entries/models.py`, `entries/services.py` (`merge_entries`), `catalog/views.py` | XL | ER-12 | `test_merge_unions_secondary_concepts`; `test_merge_keeps_claimed_entry_as_survivor`; `test_merge_carries_valid_verification`; `test_redirect_chain_is_flattened`; `test_merge_event_records_every_moved_row`; `test_merge_without_global_lock` (no advisory lock 727001 taken); extend `entries/tests/test_rules_gaps.py::test_merge_guards` |
| ER-10 | Unmerge service, `judgement` table, staff action, never-merge check in candidates | `entries/services.py`, `catalog/staff_views.py` | L | ER-09 | `test_merge_then_unmerge_restores_rows_exactly` (row-level equality of children, fields, credits); `test_unmerge_inside_window_restores_url_200`; `test_unmerge_writes_not_same_judgement`; `test_unmerge_of_old_merge_keeps_later_merges` |
| ER-11 | Staging-level resolution: cluster within a batch and against `entry_key` before `publish`; loaders write `source_record` | `intake/bulk.py`, `intake/loaders.py`, `intake/importer.py` | L | ER-05, ER-08 | `test_bulk_duplicates_within_batch_collapse_before_entries`; `test_loader_rerun_resolves_through_redirect`; throughput test with a 20,000-entry block: at least 200 rows a second; `test_published_rows_equal_clusters` |
| ER-12 | `entry_concept` model and migration (copy from the M2M); membership service with caps and evidence rule; list queries, roll-ups and search read it; `concept_closure` | `entries/models.py`, `entries/services.py`, `catalog/queries.py`, `analytics/rollups.py`, `taxonomy/models.py` | XL | | `test_secondary_membership_appears_on_list_page`; `test_rollup_counts_entry_once_per_node`; `test_secondary_cap_enforced`; `test_unevidenced_secondary_not_on_list_page`; `test_primary_copy_matches_role_one_row`; PostgreSQL `EXPLAIN` test: list query uses I3 and no sequential scan; `test_descendants_cached_per_taxonomy_version` |
| ER-13 | `place_slug_history`, `concept_slug_history`, `Place.merged_into`, resolver fallbacks, redirect cooling-off, sitemaps exclude redirects; `place_path` as immutable id path (decision first) | `places/models.py`, `taxonomy/models.py`, `catalog/resolver.py`, `catalog/views.py`, `catalog/seo.py` | L | | `test_renamed_list_type_old_slug_redirects`; `test_merged_place_redirects_to_target`; `test_no_redirect_chain_longer_than_one`; `test_redirect_is_temporary_for_30_days_then_permanent`; `test_redirect_to_suppressed_survivor_is_404`; extend `catalog/tests/test_pages.py` |
| ER-14 | `freshness_policy`, `entry_freshness`, set-based expiry in chunks, tier assignment, scheduler with `SKIP LOCKED`; replaces the `sweep_expired` loop | `entries/services.py`, `core/jobs.py`, `entries/models.py` | L | | `test_sweep_query_count_independent_of_entry_count`; `test_due_selection_uses_next_due_index` (PostgreSQL); `test_tier_assignment_from_traffic_and_claim`; `test_tier3_expired_entry_stays_public_with_date`; keep existing expiry tests |
| ER-15 | Diff-first checker: page hash, extraction only on change, per-check cost counters in micro-units | `agents/fetcher.py`, `agents/services.py` | M | | `test_unchanged_page_makes_no_model_call`; `test_changed_page_triggers_extraction`; `test_cost_recorded_in_micro_units` |
| ER-16 | Queue v2: priority, lease, place and language affinity, closure corroboration | `volunteers/models.py`, `volunteers/services.py`, `core/jobs.py` | M | | `test_closed_needs_second_signal_on_tier1`; `test_expired_lease_returns_task`; `test_next_task_prefers_place_and_language`; `test_surveyor_never_gets_previous_verifier_pair_twice` |
| ER-17 | LQAS: 29 first, 385 on any failure, per stratum | `intake/bulk.py`, `volunteers/services.py` | S | | `test_lqas_29_zero_defects_passes`; `test_one_failure_escalates_to_385`; `test_stratum_below_90_percent_stops_job_kind` |
| ER-18 | `quality` and `confidence` scores, weights table, calibration job | `entries/scoring.py` (new), `analytics` | M | | `test_confidence_decays_with_age`; `test_paid_plan_never_changes_confidence` (rule 4); `test_calibration_error_below_005_on_fixture` |
| ER-19 | Risk signals service with each signal from section 6.5 | `moderation/risk.py` (new) | L | ER-01 | One test per signal, for example `test_phone_fan_out_raises_risk`, `test_category_stuffing_raises_risk`, `test_new_domain_raises_risk`; `test_placement_requires_verified_and_age` |
| ER-20 | Reporter reputation, weighted reports, subnet counting, held edits on claimed entries | `moderation/`, `catalog/forms_views.py` | M | | `test_single_report_never_closes_entry`; `test_ten_reports_one_subnet_count_once`; `test_new_owner_phone_change_held_seven_days` |
| ER-21 | Metrics M1 to M18 as functions with status; staff page | `core/monitoring.py`, `analytics/`, `catalog/staff_views.py` | L | | One test per metric on fixtures with each of green, amber and red; `test_auto_merge_error_rate_uses_audit_sample` |
| ER-22 | Per-partition audit chain; no advisory lock on every write | `core/models.py` (`audit`, `verify_audit_chain`) | L | | `test_audit_chain_per_country_verifies`; `test_concurrent_audits_do_not_block_across_countries`; existing chain tests pass |

**Order** (cheapest risk reduction first, no deployment): ER-01, ER-08, ER-06 (a day or two each, remove false merges and query storms); ER-09 and ER-12 together (they share the category union); ER-10; ER-02 with the gold set; ER-05 and ER-11; ER-14; the rest. ER-07 (Splink) when a country passes about 1 million entries or review volume passes what two people can clear in a week.

---

## 11. Open decisions for the founder (suggested defaults)

| # | Decision | Suggested default |
|---|---|---|
| 1 | Automatic merges: allowed only for drafts and source records, never for claimed, paid, person or child-facing entries | Yes |
| 2 | Accept that Surveyor-verified is a minority label at scale (tier 1, high-risk types, audits, disputes) and that most entries are AI-checked or Not verified yet | Yes, state it on `/how-checks-work/` |
| 3 | Change plan 6.4: tier-3 entries stay public with a dated expired label instead of returning to draft after grace | Yes (needed to avoid scenario A) |
| 4 | Freshness budget | Alert at USD 0.02, stop expansion at USD 0.03 per entry-year |
| 5 | Secondary category cap and evidence rule | 25 (100 for manufacturers), evidence required for list pages |
| 6 | Redirect policy | Temporary for 30 days, then permanent; keep redirects for every ever-public ID |
| 7 | Immutable id path for `place_path` instead of slug path | Yes, before the first large import |
| 8 | Splink and libpostal adoption | Splink at the S2 trigger; libpostal only if the 150-pair test shows a gain; check the model data licence first |
| 9 | Embedding model | Choose by recall at 10 on the cross-script gold pairs; MIT-licensed first (e5, bge-m3) |
| 10 | Internal confidence score is never shown and never changed by payment | Yes |
| 11 | Geocoder purchase (OpenCage or similar) | None until pilot; check storage terms in writing if bought |
| 12 | Log these choices in `docs/DECISIONS.md` (the build-log section) | Pending: this note did not edit it, because the task was one file only |

---

## 12. Sources

Fetched or read in this session:

- Repository files listed in section 1.
- Splink README (GitHub, fetched): MIT, "a million records on a laptop in around a minute", "100+ million", DuckDB, Spark and PostgreSQL backends, Fellegi-Sunter, EM. https://github.com/moj-analytical-services/splink
- libpostal README (GitHub, fetched): MIT, 10 to 30 thousand addresses a second a thread, 99.45% full-parse accuracy, designed for under 1 GB RAM a process. https://github.com/openvenues/libpostal
- GitHub `LICENSE` files read through code search: Splink MIT, dedupe MIT, recordlinkage BSD, libpostal MIT (bundled `sparkey` Apache-2.0), Zingg AGPL-3.0, pgvector PostgreSQL licence, H3 Apache-2.0, nomenklatura MIT.
- GitHub repository search (stars and last push): Splink 2,458 stars, libpostal 4,901, dedupe 4,515, recordlinkage 1,062, Zingg 1,252, all pushed 2026-10-05 or 2026-10-06.

Search summaries (not opened, UNVERIFIED at the source): Overture GERS stability, changelogs and bridge files (docs.overturemaps.org, geoweeknews.com, overturemaps.org); Foursquare Open Source Places Apache-2.0, 100 million places, monthly (community.openstreetmap.org, docs.foursquare.com); Overture 64 million places (geoweeknews.com); Wikidata redirects on merge (phabricator.wikimedia.org); H3 resolution 9 edge 174 m and geohash 7 cell about 153 m (tessl.io, elastic.co); pgvector HNSW memory and build time (supabase.com, enterprisedb.com, oneuptime.com); trigram GIN limits (postgresql.org mailing list); multilingual-e5 and bge-m3 MIT (promptlayer.com, thegtmdirectory.com); UrduPhone and Roman Urdu normalisation (arxiv.org/abs/2004.00088, romanalfaz.readthedocs.io); ICU and CLDR Arabic-Latin transform (unicode.org, cle.org.pk); OpenCage terms, Nominatim GPL-2.0, Photon Apache-2.0, Pelias MIT (opencagedata.com, docs.joinmobilizon.org); Google fake profiles 12 million, abusive edits 100 million, claim attempts 2 million, 7 million fake profiles (searchengineland.com, ianslive.in, stanventures.com); closed-listing abuse by rivals (darkreading.com); B2B contact decay and address change rates (landbase.com, airscale.io, firstsales.io, dqglobal.com); B2B supplier verification gap (shuftipro.com, globalsources.com); zero-defect sample size n = ln(1 - confidence) / ln(reliability) (elsmar.com, learnleansigma.com, metricgate.com); Senzing free evaluation up to 100,000 records (senzing.com); OpenSanctions open-source software under MIT (opensanctions.org).

Throw-away scripts (scratchpad, not committed): pairs per second and `fold()` timing, `Entry` memory by `tracemalloc`, name skeleton prototype and similarity table, and the arithmetic in sections 1.3, 2, 4, 5 and 6.
