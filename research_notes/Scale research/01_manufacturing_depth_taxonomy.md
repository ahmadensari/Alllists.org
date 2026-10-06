# Product and industry depth taxonomy for manufacturing: sources, structure, deep trees, scale and seed

Research date: 2026-10-06. English only. Status: research and design, no code changed. Companion file: `01_manufacturing_seed.csv` (same folder, 1,170 nodes). Written for the founder rule in `docs/REQUIREMENTS_DEPTH_AND_SCALE.md` (D-01 to D-06, D-15) and decision E28 in `docs/DECISIONS.md`.

How to read the flags:

- `R` reported: read at the source, or stated by a search summary of a primary page. Where I only saw a search summary I say so.
- `S` secondary: a blog, vendor, aggregator or news page.
- `I` inference: my arithmetic from stated inputs. `H` hypothesis: my guess, needs a test.
- `UNVERIFIED`: not opened at the source, or sources disagree.
- Licence labels used in section 1: **ADOPT** (copy into our database and publish), **ADOPT-ATTR** (same, with the notice the licence asks for), **XWALK** (store only the code as a mapping, not their wording), **LOOK** (read for ideas, store nothing), **COUNSEL** (terms unclear, get written permission first).

Method: 26 standard web searches (snippets only, no page fetched with WebFetch), the repository files named in the brief, and one data file: the Harmonized System 2022 table from the `datasets/harmonized-system` repository on GitHub (its `datapackage.json` states version 2022.0, licence ODC-PDDL-1.0, source UN Comtrade `R`). I used that table only to count codes and to check that every HS code in the seed exists. Nothing here is legal advice.

---

## 0. Bottom line

1. **No outside classification is deep enough, so we author our own tree.** HS has 5,612 six-digit subheadings `R`, of which about 4,480 are manufactured goods `I` (section 3.1). But HS 9018 (all medical, surgical, dental and veterinary instruments) has 13 subheadings, and one of them is a catch-all (901890). TDAP says up to 10,000 surgical products are exported from Sialkot `S, UNVERIFIED`. HS therefore resolves about 0.13% of that range (13 of 10,000). EV chargers, motor controllers and battery management systems have no HS code of their own; they sit inside 8504.40 and 8537.10 with phone chargers and switchgear `I`.
2. **Use outside systems as scaffolding and crosswalks, never as the tree.** Safe to adopt as text: NAICS and the US HTS (US government works, public domain `R`), Wikidata labels and aliases (CC0 `R`), and the MIT-licensed Shopify taxonomy for attribute vocabularies `R`. HS, ISIC, CPC, UNSPSC, GS1 GPC and eCl@ss are crosswalk-only: we store their codes as identifiers and write our own names. The IndiaMART and Alibaba trees are look-only.
3. **Five levels, one primary parent, facets for everything that is an adjective.** Sector, industry, family, product, variant. Standard depth 5; extended depth 6 to 7 only where an assembly tree exists (vehicles, machinery, EV parts). Capabilities (process, material, certification, capacity, MOQ, export markets) are facets. If they were types, leather gloves alone would grow from 19 products to 27,360 types (section 2.7).
4. **How many list types.** Base estimate for all manufacturing: 12,394 nodes at levels 1 to 4 and 51,966 at levels 1 to 5 (range 32,000 to 92,000) `I`. The 12 sectors named by the founder come to about 24,900 nodes. The seed holds 1,059 of them (4.3%); it is a deep sample, not the full tree.
5. **Storage: follow E28, do not pre-create rows.** Full materialisation for 10,000 types at the founder's five place levels is 14.3 billion rows, 2.1 TB at 144 B a row; for 100,000 types 143 billion rows, 20.7 TB; for 500,000 types 717 billion rows, 103 TB `I`. Rows only where entries exist (E28) come to about 58 million cells for 5 million manufacturing entries with 3 product memberships each (range 42 to 124 million), 17.5 GB at the 302 B roll-up cell size `I, H`. The "list exists everywhere" principle (C11) is kept by resolving empty combinations virtually, which the code already does.
6. **Two repository findings matter more than any storage choice.** (a) Roll-ups, `recount_cell` and `refresh_for_entry` use only `Entry.primary_concept` and one parent chain, so secondary products and multi-parent nodes never count `R` (read from `backend/analytics/rollups.py`). (b) `generate_lists` in its default mode makes two queries per cell in a Python loop, which cannot work for tens of millions of cells (section 4.7).
7. **Open decisions** are in section 6.2. The most important: confirm E28 as final over C11 for empty pages; written permission from the WCO (and counsel's view) on storing HS code numbers; who approves new nodes.

---

## 1. Sources and licences

### 1.1 Evaluation

All sizes carry a grade. Licence statements come from search summaries unless stated; no licence page was opened, so every verdict marked COUNSEL or UNVERIFIED needs a written check before launch.

| # | Source | What it gives | Size and date | Licence or terms found | Verdict |
|---|---|---|---|---|---|
| 1 | **UN HS (WCO)**, HS 2022, next edition HS 2028 | Goods by 2, 4, 6 digits; the spine of customs everywhere | 5,612 subheadings, 1,228 headings, 96 chapters `R`; 21 sections `R`. HS 2028 was provisionally adopted in March 2025 with 299 sets of amendments, in force 1 Jan 2028 `R` | WCO "sole owner of all intellectual property rights to the commodity descriptors and commercial names, the accompanying six-digit HS codes, the Explanatory Notes" and the Classification Opinions; use of the Explanatory Notes database is personal and non-commercial `R` (search summary). A copy of the table is published under ODC-PDDL by the datasets project, sourced from UN Comtrade `R`; whether that dedication can cover WCO text is a legal question | **XWALK + COUNSEL.** Store code numbers as identifiers (`hs2022`, later `hs2028`), write our own names. Ask the WCO for written permission |
| 2 | **ISIC Rev 4 and Rev 5** (UNSD) | Activities (what a firm does), not products | Rev 5: 22 sections, 87 divisions, 258 groups, 463 classes `R`; endorsed by the UN Statistical Commission in March 2023 `R`. Rev 4: 21 sections, 88 divisions, 238 groups, 419 classes `I` (from memory, UNVERIFIED) | UN copyright notice: no reproduction without written permission except as the terms provide `R` (general UN notice; ISIC-specific terms not found, UNVERIFIED) | **XWALK + COUNSEL.** Seed uses Rev 4 class codes; Rev 5 mapping later from the UNSD correspondence tables |
| 3 | **CPC** v2.1 and v3 | Products and services by origin | v2.1: 2,887 subclasses `R`. CPC v3 adopted 2025, aligned to ISIC Rev 5 and HS 2022 `R` | As ISIC (UN notice) | **XWALK**, optional. Low value for depth beyond HS |
| 4 | **UNSPSC** | Products and services, four levels, eight digits | 158,448 items in v26.0801 (Aug 2023) `R`. Managed by GS1 US until Dec 2024, since then by UNDP `R` | "Free of charge", but UNDP is "sole owner of all intellectual property rights" `R` | **XWALK.** Titles reusable only after reading the full terms (UNVERIFIED). Useful cross-check at commodity level |
| 5 | **GS1 GPC** | Segment, family, class, brick, plus attributes; retail bias | Free to download as XLSX, JSON, XML; updated twice a year `R` | GS1 IP policy: work-group participants grant GS1 members a royalty-free or RAND licence `R`; terms for non-members UNVERIFIED | **XWALK.** Ask GS1 for written terms |
| 6 | **eCl@ss** 14.0 | Industrial product classes with property lists (best source for technical specs) | More than 48,000 classes, about 23,000 features, about 140,000 keywords `R` | Free for registered users `R`; the terms limit passing files on and using them inside software products `R` (stated for mapping tables) | **XWALK + LOOK.** Use the property lists as a guide when designing spec facets (motors, batteries); ship none of their text |
| 7 | **NAICS 2022** (US Census) | US industries; sector 31-33 is manufacturing | Sector 31-33: 21 subsectors, 86 industry groups, 346 six-digit industries `R`. Total code counts in snippets conflict (1,012 national industries asked; 2,125 and 1,039 returned) | Codes made by the Census Bureau are public domain under 17 U.S.C. 105 `R` | **ADOPT.** Structure and titles may be copied; US-centric, so crosswalk only for non-US use |
| 8 | **US HTS** (USITC) | HS plus US 8-digit rate lines and 10-digit statistical lines: the only free depth below six digits | 19,187 ten-digit lines in 2020 `R` | A US government document, public domain `R` | **ADOPT.** A free depth source for hints (for example splits inside 9018.90); keep as `hts` crosswalk. Other national schedules (EU TARIC, UK, India, Pakistan PCT) not checked, UNVERIFIED |
| 9 | **Google product taxonomy** | Retail categories | About 5,595 unique categories `S`; another count says over 6,600 `S`; up to 7 levels `S` | No licence text found | **XWALK**, retail only; shallow for industrial goods. Store no text |
| 10 | **Shopify Standard Product Taxonomy** | Categories, attributes and values (colour, material, size) | More than 10,000 categories, over 2,000 attributes, 26 verticals `R` (search summary of the repository) | MIT `R` | **ADOPT-ATTR** for attribute and value vocabularies. Weak on industrial parts. Check the `LICENSE` file |
| 11 | **Wikidata** | Item IDs, labels, aliases in many languages | About 118.7 million items (Jan 2026) `R`. A study retrieved 1.5K product classes covering 23K entities; "many of its classes are incomplete" `R` | Structured data CC0 (public domain); other text CC BY-SA 4.0 `R` | **ADOPT** labels, aliases and QIDs (CC0). Do not copy Wikipedia descriptions (CC BY-SA). Do not rely on its class tree |
| 12 | **Overture Maps** | Business categories for places | About 2,082 unique place categories (Apr 2025) `R`; places data under CC0, Apache-2.0 and CDLA-Permissive-2.0 `R`. A sibling note (`02_big_site_architecture.md`) reports that the divisions theme is ODbL (OSM-derived), UNVERIFIED by me | See left. Conflicts with the repository rule that share-alike sources are left out | **XWALK** for mapping imported business categories to a product node. No product depth in it |
| 13 | **OpenStreetMap** | Tags such as `craft=*`, `man_made=works`, `industrial=*` | n/a | ODbL share-alike; extracting a substantial part into a new database makes it a derivative database `R` | **LOOK.** Already excluded by the backend research default. Tag names may inform ideas; store no data |
| 14 | **IndiaMART tree** | Seller categories | 98,000 product categories across 56 industry groups, 108 to 119 million products `S` | Proprietary; scraping terms not read (INFERENCE: prohibited) | **LOOK.** Use the counts only as a calibration point |
| 15 | **Alibaba tree** | Buyer categories | 5,900 product categories in 40 sectors `S` | Proprietary | **LOOK.** Same |

### 1.2 What the evidence says about depth

- The two competitor trees differ by 17 times (5,900 against 98,000 categories) `I`. The right depth depends on how buyers search, not on a standard. Our base estimate (12,394 types at levels 1 to 4, 51,966 at levels 1 to 5) lies between the two.
- HS gives structure, not depth. Where HS has a rich split (footwear: 6403 has 8 subheadings; furniture 9403 has 12; tyres 4011 has 8) the seed follows it. Where HS has a catch-all (901890, 940290, 871410, 850440) the seed splits it by our own product knowledge and keeps the HS code as the nearest parent.
- Chapter counts that matter here (computed from the 2022 table `R`): chapter 84 has 538 subheadings, 85 has 296, 90 has 143, 61 has 106, 62 has 104, 87 has 98, 94 has 54, 95 has 39, 41 has 37, 42 has 20, 64 has 25.
- **HS 2028** (299 sets of amendments `R`) will move codes. A crosswalk row must carry its edition (`hs2022`, `hs2028`), never a bare "HS".

### 1.3 Policy proposed

1. The tree is **authored by us**: our names, our IDs, our slugs. Outside systems supply scaffolds (NAICS, HTS, ISIC, HS) and aliases (Wikidata CC0).
2. `ConceptCrosswalk` holds one row per (node, system, edition, code, match type). Existing field `system` is 20 characters, enough for `hs2022`, `isic4`, `isic5`, `cpc21`, `cpc3`, `naics2022`, `unspsc`, `gpc`, `eclass14`, `gpt`, `wikidata`, `hts`, `overture`. Add `edition` and a `licence_class` column (ADOPT, XWALK, COUNSEL) so a licence change can switch a system off in one place `H`.
3. New nodes come from catalogues, trade-body product lists and standards, found by agents as **proposals with verbatim evidence from at least three independent makers**, and approved by staff. Agents never create nodes (rule 6 of `alllists-rules` caps agents).
4. Product names are facts, but the arrangement of someone's tree is a creative work. We do not copy another site's arrangement (hence IndiaMART and Alibaba are look-only).

---

## 2. Level structure and rules

### 2.1 Levels

A level is a **role**, not an absolute number. Standard depth is five. A node's `level` is stored, so a sector that needs an extra step (vehicles) can add one and the roles stay readable.

| Level | Role | Example (leather) | Example (surgical) | Typical count per sector `I` | Listable? |
|---|---|---|---|---|---|
| 1 | **Sector** | Leather, footwear and leather goods | Surgical and medical goods | 1 (about 26 to 30 in all manufacturing) | Yes |
| 2 | **Industry** (ISIC-class sized) | Leather gloves | Surgical instruments (reusable) | 5 to 12 (about 560 in all) | Yes |
| 3 | **Product family** (HS-heading sized) | Sports leather gloves | Forceps and clamps | 25 to 80 (about 3,400 in all) | Yes |
| 4 | **Product** (HS-subheading sized or finer) | Cricket batting gloves | Artery and haemostatic forceps | 100 to 400 (about 8,400 in all) | Yes |
| 5 | **Variant** (named type inside a product) | Lined winter leather gloves | Kelly artery forceps | 400 to 4,000 (about 39,600 in all) | **On demand** (rule T3) |
| 6 to 7 | **Part or spec step**, only in assembly-tree sectors | n/a | n/a | rare | No, unless approved |

Rules:

- **T1.** Levels 1 to 4 are list types (`Concept.kind = list_type`). They always exist in the tree.
- **T2.** A node at level 5 is a **variant**: it starts as an alias and filter chip on its level-4 parent and is stored as `kind = product` (a non-listable spec node; the enum value already exists in `Concept.Kind`).
- **T3.** A level-5 variant is promoted to `list_type` when at least 10 entries sit under it in some country (the same number as `ListTypeSettings.index_threshold`, default 10 `R`). Demotion is manual only. This is the type-level twin of the place-level rule in section 4: depth is stored where data exists.
- **T4.** Levels 6 and 7 are allowed only where an assembly tree is real (vehicle systems, machinery, EV parts: system, subsystem, component, part, variant). They are `kind = product`, never listable without staff approval. Hard cap: depth 7, so a stored path stays under 200 characters (7 segments of up to 27 characters) `I`.
- **T5.** No catch-all nodes ("other", "n.e.c.", "miscellaneous"). An HS residual subheading is imported as status `residual`, hidden, and must be split or merged before launch. This is requirement D-01. The seed has no node whose name says "other" or "n.e.c." (checked). The 18 skeleton sectors are thin (levels 1 and 2 only) and are the temporary parents that D-01 allows until they are split.
- **T6.** The existing family concept "Manufacturing and trade" stays as the root. The seed's 30 sectors hang under it (`parent_id` blank in the CSV).

### 2.2 Naming

| ID | Rule |
|---|---|
| N1 | A node name is a **plural noun phrase** in sentence case, British spelling (orthopaedic). The US spelling is an alias. |
| N2 | The name must stand alone: "Cricket batting gloves", never "Batting". Maximum 6 words and 60 characters. |
| N3 | Use "and", never "&" or "/". No "etc", "other", "n.e.c.", "various". |
| N4 | No brand names, no company names, no place names. Exceptions: a pattern name that is the trade's generic term (Kelly forceps, Chesterfield sofas, Peshawari chappals) is allowed because it names a product type. |
| N5 | Adjectives, materials, processes, certificates and sizes are never nodes (section 2.6). |
| N6 | One concept, one node. Synonyms, plurals, spelling variants and local trade names are labels on the node (`ConceptLabel` kinds `synonym`, `local`, `misspelling`; table exists `R`). Examples in the seed: "khussa" for leather slippers, "Qingqi" for motorcycle rickshaws, "padestal fans" (a common misspelling, `H`) for pedestal fans. |
| N7 | The list title is built, not stored: "{node name} manufacturers in {place}". The role is a facet (`business_type`: manufacturer, exporter, sub_contractor, trader, wholesaler, as in `seed_manufacturer_template` `R`). A trader is a filter value on the same list, not a second tree. |

### 2.3 Slugs and addresses

| ID | Rule |
|---|---|
| S1 | A node has a **base slug** from its name: lower case ASCII, diacritics folded (the project already has `core.textfold.fold`), apostrophes removed, "&" becomes "and", every other run of characters becomes one hyphen. Maximum 80 characters. |
| S2 | The **list-type slug** is the base slug plus `-manufacturers`: `/pk/punjab/sialkot/cricket-batting-gloves-manufacturers/`. The suffix keeps product slugs from colliding with place slugs and system slugs, which share one address space (`ReservedSlug` `R`). |
| S3 | Base slugs are unique across the whole tree, not only within a parent. Where two nodes would collide, the node with the narrower meaning takes a distinguishing word: "Leather gloves", "Textile gloves", "Surgical and examination gloves", never two bare "Gloves". The seed passes this check (no duplicate slug among 1,170). |
| S4 | A rename writes the old slug to a history table and answers 301. A merge does the same. Entry pages already do this for merged entries `R` (`catalog/views.py`, `entry_page`); concepts have no such table yet (section 6.1). |
| S5 | The five manufacturing types seeded on 2026-10-05 map to seed nodes, with old addresses redirected: Surgical instrument makers to *Surgical instruments (reusable)*; Football makers to *Footballs and soccer balls*; Fan makers to *Fans and air-moving products*; Sanitaryware makers to *Sanitaryware, taps and bathroom fittings*; Furniture makers to *Furniture*. "Factories and suppliers" has no product and is the catch-all that D-01 forbids; it stays only as a temporary parent until its entries are re-tagged. |

### 2.4 Identifiers

| ID | Rule |
|---|---|
| I1 | The permanent ID is the existing `Concept.uid` (ULID, from `UidModel` `R`). It is never reused and never changes. The integer `id` is internal. |
| I2 | The seed `id` column is a **seed key**: block `n x 1000` per file (leather 1xxx, surgical 2xxx, orthopaedic 3xxx, two- and three-wheelers 4xxx, EV 5xxx, EV parts 6xxx, sports 7xxx, fans 8xxx, sanitaryware 9xxx, furniture 10xxx, textiles and apparel 11xxx, other sectors 12xxx). The loader stores it as a crosswalk row with system `seed`, so a second run changes nothing. |
| I3 | **Merge:** the loser keeps its row with `status = merged` and a pointer; its slug redirects; entries are re-pointed in a queue; cells are recounted. **Split:** the old node stays as a parent; new children are created; entries go to a re-tag queue. **Retire:** `status = retired`; rows are never deleted. |
| I4 | Entries never store a slug; they store node IDs. Slugs can change without touching 5 million entries. |

### 2.5 Multiple parents

A leather football goalkeeper glove belongs under leather gloves and under sports protective gear. The seed carries 21 such links.

| ID | Rule |
|---|---|
| M1 | **One primary parent** decides the breadcrumb, the canonical address and the path. |
| M2 | Up to **3 secondary parents** (`ConceptEdge(parent, child, is_primary=false, reason)`), at the same level as the primary parent. Reasons: `use`, `material`, `regulatory`, `trade`. |
| M3 | The graph is acyclic (checked on write). |
| M4 | Counts: an entry counts **once** at each ancestor, however many paths lead there. Upper cells count distinct entries. |
| M5 | A secondary edge needs at least 3 makers findable by both routes; otherwise use a "see also" link. This keeps the graph small `H`. |

Sample of the 21 links in the seed (each parent is exactly one level above the child; the check is in section 5):

| Node | Also under |
|---|---|
| Biker leather jackets | Motorcycle riding jackets and pants |
| Cricket batting gloves | Cricket protective gear |
| Wicketkeeping gloves | Cricket protective gear |
| Football goalkeeper gloves | Football shin guards and goalkeeper gear |
| Boxing gloves | Boxing hand protection |
| Golf gloves | Golf clubs, balls and bags |
| Motorcycle riding gloves | Motorcycle riding gloves and boots |
| Leather football boots | Football boots |
| Plaster of Paris splints and rolls | Surgical consumables and disposables |
| Orthopaedic and diabetic footwear | Leather footwear |
| Motorcycle batteries | Batteries and accumulators |
| Electric forklifts and pallet trucks | Lifting and handling equipment |

### 2.6 One manufacturer, many nodes

An entry attaches to nodes through a relation that carries a role and evidence. The repository has the start of this: `Entry.primary_concept` plus `Entry.secondary_concepts` (a plain many-to-many) `R`. At manufacturing depth it needs more.

| ID | Rule |
|---|---|
| A1 | Exactly **one primary** attachment per entry (the product line with the most evidence or revenue share). Enforced by a partial unique index. |
| A2 | Up to **24 secondary** attachments (soft warning above 10). A firm that claims more is pointed to a higher node. |
| A3 | Attach at the **deepest node the evidence supports**. If the evidence names only a family (for example an export record under HS 9018.90), attach to the family with a `broad` flag; such rows list last. |
| A4 | Each attachment row carries `source`, `evidence_ref`, a check label (one of the four) and a date. It is a field value, so it fits `ValueMeta` and the verification state machine `R`. |
| A5 | **Ranking inside a node:** primary before secondary, then check label, then freshness. Paid placement stays separate and never changes a label (rule 4). |
| A6 | Product-level attributes (materials, MOQ per product, lead time, price band, spec range) sit on the attachment, not on the company. Company-level facts (workforce band, capacity band, export markets, certificates) stay in the add-on block. |
| A7 | Agents may propose attachments with verbatim evidence. They may not create nodes, and a primary attachment from an agent stays "AI-checked" until a person confirms. |
| A8 | **Process-only businesses** (dyeing houses, embroidery units, plating shops, washing units) attach to the product they process, with `business_type = sub_contractor` and the process as a facet. There is no "dyeing" list type; there is "Dyed and printed cotton fabric" with the process facet. |

### 2.7 Capabilities are facets, not types

**The test.** A property is a node only if all four hold: (1) it names a *thing* that a buyer asks for as a distinct product; (2) it changes what is made (different tooling, material flow or HS heading); (3) at least three makers are expected in some country; (4) it is a noun phrase, not an adjective, a process, a certificate, a grade or a number. Everything else is a facet.

| Property | Verdict | Reason |
|---|---|---|
| Football; Kelly artery forceps; electric motorcycle | Node | Distinct product; own tooling or HS line |
| Hand-stitched, thermally bonded | Facet `process` | Process |
| Stainless steel 420, goatskin, NdFeB magnets | Facet `material`, value with a crosswalk (AISI, DIN, ISO 7153-1 `UNVERIFIED`) | Material |
| FIFA Quality Pro, ISO 13485, CE MDR, PEL star rating | Facet `cert` or `standard` (identifier list, scope per product) | Certificate |
| Size 5, 56 inch sweep, 48 V, 7 kW | Facet `spec` (number band) | Number |
| MOQ, capacity band, lead time, payment terms, export markets | Facets (company or product scope) | Commercial |
| OEM, ODM, private label, own brand | Facet `brand_type` | Business model |
| LFP, NMC, sodium-ion cell chemistry | Facet `material`, with a **promoted facet landing page** because buyers search "LFP battery makers" | Adjective, but high search demand |
| Sialkot style, Chinioti carving, Kolhapuri | Facet `style` or `origin` | Origin or style |

**Why it matters, with arithmetic `I`.** Leather gloves have 19 products in the seed. Suppose capabilities were types: 6 materials x 4 processes x 5 certificates x 4 MOQ bands x 3 capacity bands = 1,440 combinations per product, so 19 x 1,440 = **27,360 types** instead of 19. Applied to all 8,433 estimated products the count is 8,433 x 1,440 = **12.1 million types**, before any place is considered.

**Facet registry (design).**

| Part | Content | Size `H` |
|---|---|---|
| `FacetDef` | key, label, kind (enum, multi-enum, number band, bool, identifier list, place list), scope (company, product, both), applies-to (a node; inherited by every descendant), filterable, show (P, L, H, I as in `AddonField` `R`) | About 16 universal (from the 6.24 field table `R`: business type, capacity band, workforce band, MOQ, lead time, certifications, regulatory registrations, standards, export markets, OEM, sample policy, payment terms, trade-body membership, verification tier, year established, factory area) plus about 300 sector and spec facets |
| `FacetValue` | slug, label, aliases, crosswalk to a standard where one exists | About 3,000 to 15,000 values. The seed already uses 26 facet keys and 559 distinct values over 12 sectors; values saturate because vocabularies are reused (steel grades, certificates) |
| Entry values | company scope in the add-on JSON; product scope on the attachment row; filterable values also in a narrow table `(entry, concept, facet, value)` | 5 million entries x 3 attachments x 6 filterable values = 90 million rows, about 11 GB at 120 B a row with indexes `H` |

**Where facets live in the CSV.** The `facets` column lists the facet groups that apply at that node and the values that matter for it, as `group=value|value;group=value`. A child inherits every group of its ancestors. Only 70 of the 1,170 rows carry facet groups, because facets are declared as high as they are true (sector, industry, family). The reserved key `also_under=slug|slug` holds the secondary parents. Universal facets are not repeated in the file.

### 2.8 Natural scale and the place levels

`Concept.natural_scale` (hyper_local, city, national, global `R`) says at which place level a list is most useful. For manufacturing the seed uses: **city** for sectors and industries (many makers everywhere), **national** for most families and products, **global** for narrow products with few makers (about 90 nodes: neurosurgery instruments, ultra-fast DC chargers, solid-state cells). A rule of thumb `H`: expected makers worldwide under 1,000 gives global; 1,000 to 50,000 gives national; over 50,000 gives city. The natural scale drives indexing, not storage: a page is indexed at its natural level and one level down only when the entries differ enough from the parent (the near-duplicate problem noted in `02_big_site_architecture.md`, finding 7).

**"Business district" for manufacturing** is an industrial estate, export processing zone, special economic zone or market cluster (Sialkot Small Industrial Estate, Sundar Industrial Estate). The place tree has `area`, `society` and `street` levels `R`, but no kind marker. Add a `place_kind` tag at area level (section 6.1). Polygons for industrial land use are in OpenStreetMap (ODbL, excluded), so estates must come from government lists and contributors `H`.

---

## 3. Worked deep trees

The full trees are in the CSV. Below, each sector shows its industries and families (the number in brackets is the count of nodes below), then one or two paths expanded to the bottom with their facets. "Product" lines carry the HS 2022 code in square brackets. The levels are roles, so depth varies between sectors (4 or 5).

### 3.1 Arithmetic: how big is all manufacturing

**Base from HS** `R, I`. The 2022 table has 5,612 six-digit subheadings. Sections VI to XX (chemicals through miscellaneous manufactures) hold 923 + 211 + 69 + 146 + 140 + 797 + 47 + 151 + 55 + 570 + 834 + 172 + 208 + 18 + 142 = **4,483** subheadings, 79.9% of the total. Add section IV (food, drink, tobacco) at 220 and the figure is 4,703, 83.8%. Sections I to III (live animals, plants, fats) and V (minerals) are mostly not manufacturing.

**Model.** For each sector, products at level 4 = HS6 count x m4 (how many of our products fit in one HS subheading); variants at level 5 = level 4 x m5; families at level 3 = level 4 / 2.5 (`H`; in the seed the 113 families that have children average 3.8 products, but 379 of 492 families are still leaves, so the true ratio is unknown; at 3.8 the level 1 to 4 total would fall by about 1,150, or 9% `I`); industries at level 2 = families / 6 (the seed averages 5.9 families per industry over the 12 named sectors `R`, computed from the CSV); one sector node. The multipliers are **hypotheses `H`** set by how much finer our trade's own vocabulary is than HS: bulk commodities (chemicals, basic metals) 1.0 to 1.5; textiles and wood 1.5 and 2 to 3; hardware, apparel and electrical 2.0 and 5; surgical goods 8 and 12 because HS has a catch-all; two-wheeler parts 15 and 9 because parts catalogues are enormous.

| Sector | HS base | HS6 | m4 | L4 | m5 | L5 | L3 | L2 | Total L1-L5 |
|---|---|---|---|---|---|---|---|---|---|
| Leather, footwear and leather goods | HS 41, 42, 43, 64 | 94 | 2 | 188 | 6 | 1,128 | 75 | 12 | 1,404 |
| Textiles | HS 50-60, 63 | 587 | 1.5 | 880 | 3 | 2,640 | 352 | 59 | 3,932 |
| Apparel and garments | HS 61, 62, 65 | 218 | 2 | 436 | 5 | 2,180 | 174 | 29 | 2,820 |
| Wood, cork and wood products | HS 44-46 | 146 | 1.5 | 219 | 2 | 438 | 88 | 15 | 761 |
| Furniture and bedding | HS 9401-9404 | 36 | 4 | 144 | 6 | 864 | 58 | 10 | 1,077 |
| Paper, printing and packaging | HS 47-49 | 140 | 1.5 | 210 | 2 | 420 | 84 | 14 | 729 |
| Chemicals, paints and cosmetics | HS 28-29, 31-38 | 878 | 1 | 878 | 1.5 | 1,317 | 351 | 58 | 2,605 |
| Pharmaceuticals (needs its own drug tree) | HS 30 less 3005, 3006 | 34 | 1 | 34 | 1.5 | 51 | 14 | 2 | 102 |
| Rubber and plastics | HS 39-40 less sanitaryware, tyres, gloves | 192 | 1.5 | 288 | 3 | 864 | 115 | 19 | 1,287 |
| Building materials, ceramics, glass, cement | HS 68-70, 2523 | 156 | 2 | 312 | 4 | 1,248 | 125 | 21 | 1,707 |
| Basic metals | HS 72, 74-76, 78-81 | 346 | 1 | 346 | 1.5 | 519 | 138 | 23 | 1,027 |
| Fabricated metal, tools and hardware | HS 73, 82, 83 | 224 | 2 | 448 | 5 | 2,240 | 179 | 30 | 2,898 |
| Machinery | HS 84 | 538 | 1.5 | 807 | 6 | 4,842 | 323 | 54 | 6,027 |
| Electrical equipment and electronics | HS 85 | 296 | 1.5 | 444 | 5 | 2,220 | 178 | 30 | 2,873 |
| Instruments, watches and optical | HS 90 less medical, 91 | 159 | 1.5 | 238 | 4 | 952 | 95 | 16 | 1,302 |
| Road vehicles and conventional parts | HS 87 less two-wheelers | 79 | 1.5 | 118 | 12 | 1,416 | 47 | 8 | 1,590 |
| Other transport | HS 86, 88, 89 | 74 | 1.2 | 89 | 3 | 267 | 36 | 6 | 399 |
| Jewellery, music, brooms, pens, other | HS 71, 92, 96 | 121 | 2 | 242 | 4 | 968 | 97 | 16 | 1,324 |
| Food, beverages and tobacco (manufactured part) | HS 04, 07-24 | 607 | 1.2 | 728 | 3 | 2,184 | 291 | 48 | 3,252 |
| Sports goods and toys | HS 95 | 39 | 4 | 156 | 8 | 1,248 | 62 | 10 | 1,477 |
| Surgical and medical goods | HS 9018-9020, 9022, 9402, 3005, 3006, 4015, 8419.20 | 41 | 8 | 328 | 12 | 3,936 | 131 | 22 | 4,418 |
| Orthopaedic, rehabilitation and support goods | HS 9021, 8713, 6115 | 19 | 10 | 190 | 8 | 1,520 | 76 | 13 | 1,800 |
| Two- and three-wheel vehicles and parts | HS 8711, 8712, 8714, 4011.40 | 18 | 15 | 270 | 9 | 2,430 | 108 | 18 | 2,827 |
| Electric vehicles | HS 8703.40-.80, 8704.51-.60, 8702.40, 8701.24 | 10 | 8 | 80 | 4 | 320 | 32 | 5 | 438 |
| EV components and spare parts (bottom-up) | share of HS 8507, 8501, 8504, 8536, 8544 | 40 | 8 | 320 | 10 | 3,200 | 128 | 21 | 3,670 |
| Fans and air-moving products (bottom-up) | HS 8414.5x, 8414.60, 8414.90 | 4 | 10 | 40 | 4 | 160 | 16 | 3 | 220 |
| **Total** | | **5,096** | | **8,433** | | **39,572** | **3,373** | **562** | **51,966** |

Totals `I`: levels 1 to 4 = 26 + 562 + 3,373 + 8,433 = **12,394**; adding variants gives **51,966**. If the variant multipliers are halved the total is 32,180; if doubled, 91,538. Overlaps are small by design: about 44 subheadings are counted in both a sector row and a bottom-up row (EV parts and fans), and the food row includes some raw produce.

Cross-checks `I`: eCl@ss 14 has more than 48,000 classes over all industries and services `R`, UNSPSC 158,448 items `R`, IndiaMART 98,000 categories `S`, Alibaba 5,900 `S`. A 52,000-node manufacturing tree is the same order as eCl@ss; the 12,400 listable core is twice Alibaba's browse tree.

**Pharmaceuticals** are costed at 102 nodes only because a drug list needs the ATC or INN drug vocabularies, which have their own licences (not researched) and a different logic (molecule, dose form, strength). Out of scope here; see section 6.2.

**Pilot check.** Sialkot surgical instruments: the seed gives 189 nodes (of them 110 products and 35 variants); the estimate for the whole sector is 4,418. The pilot register of about 1,800 to 2,500 firms `S` (`01_sialkot_surgical_sources.md`) would sit on about 150 listable nodes at first, which is a workable number for a verified-supplier register.

### 3.2 Seed coverage by sector

| Seed sector | Sector | Industry | Family | Product | Variant | Seed total | Estimated full tree (section 3.1) | Seed coverage |
|---|---|---|---|---|---|---|---|---|
| Leather, footwear and leather goods | 1 | 8 | 40 | 87 | 5 | 141 | 1,404 | 10.0% |
| Surgical and medical goods | 1 | 5 | 38 | 110 | 35 | 189 | 4,418 | 4.3% |
| Orthopaedic, rehabilitation and support goods | 1 | 8 | 49 | 63 | 0 | 121 | 1,800 | 6.7% |
| Two- and three-wheel vehicles | 1 | 8 | 70 | 19 | 0 | 98 | 2,827 | 3.5% |
| Electric vehicles | 1 | 5 | 22 | 5 | 0 | 33 | 438 | 7.5% |
| Electric mobility components and spare parts | 1 | 7 | 42 | 45 | 0 | 95 | 3,670 | 2.6% |
| Sports goods and toys | 1 | 10 | 47 | 20 | 0 | 78 | 1,477 | 5.3% |
| Fans and air-moving products | 1 | 6 | 26 | 5 | 0 | 38 | 220 | 17.3% |
| Sanitaryware, taps and bathroom fittings | 1 | 5 | 31 | 27 | 0 | 64 | 777 | 8.2% |
| Furniture | 1 | 7 | 43 | 27 | 0 | 78 | 1,077 | 7.2% |
| Textiles | 1 | 6 | 39 | 24 | 0 | 70 | 3,932 | 1.8% |
| Apparel and garments | 1 | 9 | 42 | 2 | 0 | 54 | 2,820 | 1.9% |
| **Named sectors total** | 12 | | | | | **1059** | **24,860** | **4.3%** |

The seed covers 4.3% of the estimated nodes of the 12 sectors. It follows HS where HS has a split, adds our own splits where HS has a catch-all, and gives the trade's own names for variants where we know them. It was not built from search data, so it is a sample of the vocabulary, not a ranking of demand. Surgical instruments carry the deepest sample (35 variants) because Sialkot is the pilot trade. A family shown without a number is still a leaf.

### 3.3 Leather, footwear and leather goods

**Leather, footwear and leather goods** (141 nodes in the seed)
- Leather tanning and finishing (28 below): Bovine and buffalo leather (9); Sheep and lamb leather (2); Goat and kid leather (2); Exotic and reptile leather (3); Patent, metallised and chamois leather (3); Composition and reconstituted leather; Sole and technical leather (2)
- Leather garments (10 below): Leather jackets (6); Leather trousers and shorts; Leather skirts and dresses; Leather aprons and protective garments
- Leather gloves (22 below): Fashion and dress leather gloves (4); Industrial and work leather gloves (4); Sports leather gloves (11)
- Belts and small leather goods (16 below): Leather belts (5); Leather wallets and purses (5); Leather key cases and small cases; Leather mobile phone and tablet cases; Leather pen, spectacle and cigar cases; Leather watch straps
- Leather bags and luggage (19 below): Leather handbags (6); Leather business bags (3); Leather travel bags (3); Leather backpacks and rucksacks; Leather tool bags and tool belts; Leather camera and instrument cases; Leather jewellery and watch boxes
- Leather footwear (31 below): Men's leather dress shoes (3); Women's leather shoes (2); Leather sandals and open footwear (4); Leather boots (5); Safety and work footwear (3); Leather sports and casual shoes (4); Shoe components (3)
- Saddlery, harness and animal goods (4 below): Horse saddles; Bridles, reins and halters; Dog collars and leashes; Horse blankets and rugs
- Fur and shearling products (2 below): Fur coats and jackets; Fur trim and accessories

Deep path, leather gloves (one industry, 3 families, 19 products):

- Leather gloves (industry) [HS 4203]
  - Fashion and dress leather gloves (family) [HS 420329]
    - Ladies dress leather gloves (product) [HS 420329]
    - Men's driving leather gloves (product) [HS 420329]
    - Lined winter leather gloves (product) [HS 420329]
    - Leather mittens (product) [HS 420329]
  - Industrial and work leather gloves (family) [HS 420329]
    - Welders leather gloves (product) [HS 420329]
    - Driver and general work leather gloves (product) [HS 420329]
    - Cut-resistant leather gloves (product) [HS 420329]
    - Heat-resistant leather gloves (product) [HS 420329]
  - Sports leather gloves (family) [HS 420321]
    - Cricket batting gloves (product) [HS 420321]
    - Wicketkeeping gloves (product) [HS 420321]
    - Football goalkeeper gloves (product) [HS 420321]
    - Boxing gloves (product) [HS 420321]
    - MMA and grappling gloves (product) [HS 420321]
    - Baseball and softball gloves (product) [HS 420321]
    - Golf gloves (product) [HS 420321]
    - Cycling and gym gloves (product) [HS 420321]
    - Motorcycle riding gloves (product) [HS 420321]
    - Equestrian riding gloves (product) [HS 420321]
    - Ski and snowboard gloves (product) [HS 420321]

Facets at the industry: `material` = cowhide, goatskin, deerskin, sheepskin, pigskin, synthetic leather; `process` = cut-and-sew, pre-sewn, fourchette construction, welt; `standard` = EN 388, EN 407, EN 420, ISO 11999; `cert` = ISO 9001, OEKO-TEX. These are values to filter on, not 5 x 4 x 4 more lists. Footwear sits in the same sector (HS 64) with 7 families (men's dress shoes, women's shoes, sandals, boots, safety footwear, sports and casual shoes, components). Known weak mappings: sports gloves are coded to HS 4203.21 (leather); a synthetic goalkeeper glove is not (it is 6216 or 9506.99). The HS code is a hint, not a rule.

### 3.4 Surgical instruments and goods

**Surgical and medical goods** (189 nodes in the seed)
- Surgical instruments (reusable) (104 below): Forceps and clamps (25); Surgical scissors (8); Scalpels, blades and knives (4); Retractors (10); Bone and orthopaedic surgical instruments (9); Probes, dilators and sounds (4); Specula and examination instruments (5); Suction tubes and cannulae (2); Laparoscopic reusable instruments (3); Specialty surgical instruments (17); Surgical instrument sets and trays (6)
- Dental instruments and supplies (11 below): Dental extraction forceps (3); Dental elevators and luxators; Dental scalers and curettes; Dental mirrors, explorers and probes; Dental pluggers and amalgam instruments; Dental handpieces and burs; Dental impression trays and cements; Dental chairs and units
- Beauty, manicure and grooming instruments (6 below): Nail clippers and cuticle nippers; Manicure and pedicure sets; Tweezers and eyebrow tools; Barber scissors and thinning shears; Facial and comedone extractors; Razors and shaving instruments
- Surgical consumables and disposables (37 below): Surgical and examination gloves (4); Sutures and needles (4); Syringes and needles (4); Catheters and tubes (6); Infusion and transfusion sets (2); Wound care and dressings (5); Surgical masks, gowns and drapes (4); Ostomy and continence products
- Hospital furniture and equipment (25 below): Hospital beds and trolleys (4); Operating theatre equipment (4); Sterilisation equipment (2); Patient monitoring and diagnostics (7); Respiratory and oxygen equipment (3)

Deep path, forceps and clamps (one family, 7 products, 18 variants):

- Forceps and clamps (family) [HS 901890]
  - Artery and haemostatic forceps (product) [HS 901890]
    - Kelly artery forceps (variant) [HS 901890]
    - Halsted mosquito forceps (variant) [HS 901890]
    - Rochester-Pean forceps (variant) [HS 901890]
    - Crile artery forceps (variant) [HS 901890]
    - Kocher forceps (variant) [HS 901890]
  - Tissue and dissecting forceps (product) [HS 901890]
    - Adson tissue forceps (variant) [HS 901890]
    - Allis tissue forceps (variant) [HS 901890]
    - Babcock intestinal forceps (variant) [HS 901890]
    - DeBakey atraumatic forceps (variant) [HS 901890]
    - Russian tissue forceps (variant) [HS 901890]
    - Dressing forceps (variant) [HS 901890]
  - Sponge and swab holding forceps (product) [HS 901890]
  - Towel clamps (product) [HS 901890]
  - Needle holders (product) [HS 901890]
    - Mayo-Hegar needle holders (variant) [HS 901890]
    - Olsen-Hegar needle holders (variant) [HS 901890]
    - Castroviejo needle holders (variant) [HS 901850]
    - Tungsten carbide needle holders (variant) [HS 901890]
  - Vascular clamps (product) [HS 901890]
    - Satinsky vascular clamps (variant) [HS 901890]
    - Bulldog clamps (variant) [HS 901890]
    - DeBakey vascular clamps (variant) [HS 901890]
  - Intestinal and bowel clamps (product) [HS 901890]

Facets at the industry: `material` = stainless steel 410, 420, 304, 316L, titanium, tungsten carbide inserts; `process` = forging, die-cutting, CNC machining, hand-finishing, laser marking, heat treatment, electropolishing; `standard` = ISO 7153-1, DIN 58298, ASTM F899 (not verified at source, `UNVERIFIED`); `cert` = ISO 13485, CE MDR, FDA establishment registration, DRAP establishment licence (the evidence ladder in `01_sialkot_surgical_sources.md` section 5.4 `R`). Sector facets: regulatory class (I, IIa, IIb, III), sterility, reuse. Eponyms (Kelly, Halsted, Mayo, Adson) are accepted as pattern names under rule N4 because they are the trade's own vocabulary and each has several makers in Sialkot `S`. The beauty and manicure instruments of Sialkot (HS 8214) are a separate industry because TDAP says Sialkot makes 99% of Pakistan's dental, veterinary and beauty instruments `S`.

### 3.5 Orthopaedic, rehabilitation and support goods

**Orthopaedic, rehabilitation and support goods** (121 nodes in the seed)
- Braces and supports (44 below): Neck supports (4); Shoulder and arm supports (4); Elbow, wrist and hand supports (5); Back and spine supports (6); Hip and thigh supports (2); Knee supports (6); Ankle and foot supports (7); Hernia and maternity supports (2)
- Compression and elastic garments (5 below): Graduated compression stockings; Anti-embolism stockings; Lymphoedema garments and sleeves; Post-surgical compression garments; Elastic knee and ankle sleeves
- Fracture and immobilisation products (6 below): Plaster of Paris splints and rolls; Fibreglass casting tape; Thermoplastic and aluminium splints; Thomas and traction splints; Skin traction kits; Padding and stockinette for casts
- Walking aids and mobility products (16 below): Crutches (2); Walking sticks and canes; Walkers and rollators; Wheelchairs (5); Mobility scooters; Bathroom and toilet aids (2); Anti-decubitus mattresses and cushions
- Orthopaedic implants and trauma (27 below): Fracture fixation plates (4); Orthopaedic screws (4); Intramedullary nails (3); External fixators; Orthopaedic wires and pins; Joint replacement implants (4); Spinal implants (3); Craniomaxillofacial plates and screws; Orthopaedic implant instrument sets
- Prosthetics and orthotics (8 below): Prosthetic feet; Prosthetic knee joints; Prosthetic sockets and liners; Prosthetic pylons and adapters; Upper-limb prostheses; Ankle-foot orthoses; Clubfoot braces; Orthopaedic and diabetic footwear
- Hearing and daily-living aids (2 below): Hearing aids; Daily living aids
- Rehabilitation and physiotherapy equipment (4 below): Therapy electrotherapy devices; Traction tables and physiotherapy beds; Exercise bands, balls and balance boards; Hot and cold therapy packs

Deep path, knee supports:

- Knee supports (family) [HS 902110]
  - Elastic knee sleeves and caps (product) [HS 902110]
  - Hinged knee braces (product) [HS 902110]
  - Patella stabilising braces (product) [HS 902110]
  - Knee immobilisers (product) [HS 902110]
  - ACL and ligament braces (product) [HS 902110]
  - Osteoarthritis unloader braces (product) [HS 902110]

Facets: `material` = neoprene, elastic cotton, spandex, thermoplastic, aluminium stays, carbon fibre; `process` = cut-and-sew, thermoforming, injection moulding, knitting; `spec` = size, left-right, compression level; `standard` = ISO 13485, ISO 22523 (`UNVERIFIED`). Implants (plates, nails, joints, spinal) are their own industry because their evidence is regulatory (CE MDR, FDA 510(k), DRAP) and their makers are few and global.

### 3.6 Motorcycles and two- and three-wheelers

**Two- and three-wheel vehicles** (98 nodes in the seed)
- Motorcycles with internal combustion engines (18 below): Commuter and standard motorcycles (3); Sports and supersport motorcycles (2); Naked and street motorcycles; Cruiser motorcycles; Touring and adventure motorcycles; Off-road, dirt and trail motorcycles; Scooters (2); Mopeds and step-through motorcycles; Motorcycles 800cc and above; Quad bikes and all-terrain vehicles; Motorcycle sidecars
- Electric two-wheelers (14 below): Electric motorcycles (2); Electric scooters (3); Electric mopeds; Electric bicycles (4); Electric bike conversion kits
- Three-wheelers (5 below): Passenger auto-rickshaws; Cargo three-wheelers and loaders; Motorcycle rickshaws; Electric rickshaws; Electric cargo three-wheelers
- Bicycles (9 below): Road and city bicycles; Mountain bicycles; BMX and freestyle bicycles; Children's bicycles and tricycles; Folding bicycles; Bicycle frames and forks; Bicycle wheels, rims and spokes; Bicycle saddles and handlebars; Bicycle brakes and gear systems
- Motorcycle engines and engine parts (18 below): Cylinder blocks and cylinder heads; Pistons, rings and pins (3); Connecting rods and crankshafts; Camshafts, valves and rocker arms; Engine gaskets, seals and oil seals; Carburettors and throttle bodies; Fuel injectors and fuel pumps; Air filters and oil filters; Spark plugs and ignition coils; CDI units and magnetos; Starter motors and kick starters; Clutch assemblies; Gearbox and transmission parts; Chain and sprocket kits; Motorcycle silencers and exhaust systems
- Motorcycle chassis, brakes and wheels (10 below): Motorcycle frames and swingarms; Front forks and rear shock absorbers; Motorcycle wheels, rims and spokes; Motorcycle tyres; Motorcycle inner tubes; Brake discs, drums and shoes; Brake pads; Brake calipers and master cylinders; Brake and clutch levers and cables; Motorcycle stands and crash guards
- Motorcycle body, electrical and accessories (11 below): Fuel tanks and body panels; Motorcycle seats; Mirrors, handlebars and grips; Motorcycle lighting; Motorcycle horns; Motorcycle batteries; Wiring harnesses and switches; Regulators and rectifiers; Speedometers and instrument clusters; Motorcycle luggage racks and panniers; Motorcycle covers
- Motorcycle riding gear (4 below): Motorcycle helmets; Motorcycle riding jackets and pants; Motorcycle riding gloves and boots; Motorcycle body armour and protectors

Deep path, commuter and standard motorcycles:

- Commuter and standard motorcycles (family) [HS 871120]
  - Entry commuter motorcycles up to 110cc (product) [HS 871120]
  - Commuter motorcycles 125cc to 150cc (product) [HS 871120]
  - Premium commuter motorcycles 150cc to 250cc (product) [HS 871120]

The brand (Honda, Yamaha, Hero) is never a node; it is a facet and an entry. Engine size, cooling, fuel system and fitment ("fits CD70") are `spec` and `compatibility` facets. Parts follow HS 8714.10 (motorcycle parts) and 8409.91 (engine parts) as the parent codes, but are split into three parts industries (engine, chassis and brakes, body and electrical) plus riding gear, because those codes are catch-alls.

### 3.7 Electric vehicles

**Electric vehicles** (33 nodes in the seed)
- Battery electric passenger cars (8 below): Electric hatchbacks and city cars; Electric sedans; Electric SUVs and crossovers; Electric MPVs and minivans; Electric sports and luxury cars; Electric microcars and quadricycles; Electric golf carts and utility carts; Electric tourist and sightseeing vehicles
- Hybrid and range-extender cars (4 below): Full hybrid cars (HEV); Plug-in hybrid cars (PHEV); Range-extender electric cars (EREV); Diesel hybrid cars
- Electric commercial vehicles (9 below): Electric light commercial vehicles; Electric trucks (2); Electric buses (3); Electric garbage and municipal trucks
- Electric off-road and industrial vehicles (4 below): Electric forklifts and pallet trucks; Electric tractors; Electric construction and mining vehicles; Electric airport ground support vehicles
- Electric vehicle conversion and retrofit (2 below): ICE-to-EV conversion kits; Retrofit electric drive units

Deep path, battery electric passenger cars:

- Battery electric passenger cars (industry) [HS 870380]
  - Electric hatchbacks and city cars (family) [HS 870380]
  - Electric sedans (family) [HS 870380]
  - Electric SUVs and crossovers (family) [HS 870380]
  - Electric MPVs and minivans (family) [HS 870380]
  - Electric sports and luxury cars (family) [HS 870380]
  - Electric microcars and quadricycles (family) [HS 870380]
  - Electric golf carts and utility carts (family) [HS 870310]
  - Electric tourist and sightseeing vehicles (family) [HS 870380]

HS 2022 has dedicated lines for electric vehicles `R` (computed from the table): 8703.80 (cars, electric only), 8703.40 to 8703.70 (hybrids), 8704.60 (goods vehicles, electric), 8702.40 (buses, electric), 8701.24 (road tractors, electric), 8711.60 (motorcycles, electric). The seed uses them as parents.

### 3.8 EV spare parts and components

**Electric mobility components and spare parts** (95 nodes in the seed)
- Traction battery systems (29 below): Lithium-ion cells for vehicles (6); Battery modules; Battery packs by vehicle type (6); Lead-acid traction batteries; Battery management systems (3); Battery enclosures and trays; Battery cooling plates and thermal pads; Busbars and battery interconnects; High-voltage fuses and contactors; Battery cell materials (4)
- Electric drive systems (21 below): Traction motors (6); Motor controllers and inverters (4); Reduction gearboxes and e-axles (2); Motor components (4); Throttles, pedal-assist and speed sensors
- Charging equipment (18 below): Onboard chargers; DC-DC converters for vehicles; AC wall chargers (EVSE) (3); DC fast chargers (3); Two- and three-wheeler chargers; Battery swapping stations; Charging connectors, inlets and cables (4); Charging controllers and management software hardware
- High-voltage electrical and electronic systems (6 below): Power distribution units and HV junction boxes; High-voltage cables and harnesses; High-voltage connectors; Vehicle control units; Telematics and connectivity modules; Digital instrument clusters
- Thermal management systems for EVs (5 below): Electric air-conditioning compressors; Electric coolant pumps; Battery chillers and heat exchangers; PTC and high-voltage heaters; EV heat pump systems
- EV chassis and body parts (5 below): Regenerative and electro-hydraulic braking parts; Electric power steering motors; Electric vacuum pumps for brakes; Low-rolling-resistance EV tyres; Lightweight aluminium battery and body structures
- Electric two- and three-wheeler chassis, axle and body parts (3 below): E-rickshaw differentials and rear axles; E-rickshaw and e-loader body parts; E-rickshaw and e-bike wiring harnesses

Deep path, lithium-ion cells for vehicles, and charging equipment:

- Lithium-ion cells for vehicles (family) [HS 850760]
  - Cylindrical cells (18650, 21700, 4680) (product) [HS 850760]
  - Prismatic cells (product) [HS 850760]
  - Pouch cells (product) [HS 850760]
  - Sodium-ion cells (product) [HS 850780]
  - Solid-state and semi-solid-state cells (product) [HS 850780]
  - Lithium titanate (LTO) cells (product) [HS 850760]

- Charging equipment (industry) [HS 8504;8536]
  - Onboard chargers (family) [HS 850440]
  - DC-DC converters for vehicles (family) [HS 850440]
  - AC wall chargers (EVSE) (family) [HS 850440]
    - Portable EV chargers (Mode 2) (product) [HS 850440]
    - Single-phase AC wall chargers up to 7kW (product) [HS 850440]
    - Three-phase AC chargers 11kW to 22kW (product) [HS 850440]
  - DC fast chargers (family) [HS 850440]
    - DC chargers 30kW to 60kW (product) [HS 850440]
    - DC chargers 120kW to 180kW (product) [HS 850440]
    - Ultra-fast DC chargers above 350kW (product) [HS 850440]
  - Two- and three-wheeler chargers (family) [HS 850440]
  - Battery swapping stations (family) [HS 850440]
  - Charging connectors, inlets and cables (family) [HS 8544;8536]
    - Type 1 and Type 2 connectors and cables (product) [HS 854442]
    - CCS and CHAdeMO connectors (product) [HS 853669]
    - GB/T and NACS connectors (product) [HS 853669]
    - Vehicle charging inlets and sockets (product) [HS 853669]
  - Charging controllers and management software hardware (family) [HS 903289]

Facets at the sector: `supply_type` = OEM, aftermarket, refurbished; `voltage_class` = 12 V to 800 V; `compatibility` = vehicle class and make-model fitment. Facets at battery systems: chemistry (LFP, NMC, NCA, LTO, sodium-ion, solid-state), nominal voltage, capacity, cycle life, IP rating; `standard` = UN 38.3, UNECE R100, IEC 62660, ISO 12405, AIS-048 (`UNVERIFIED`). HS fit is weak and said so: batteries are 8507.60, motors 8501.32 and 8501.52, chargers and inverters 8504.40, relays 8536.41, but BMS, VCU and charging controllers have no HS home (seed uses 9032.89 and 8537.10, `I`). EV components also attach to conventional parts (8708 brakes, steering) and to electrical sectors (secondary parents). EV spare parts are not a separate tree: a spare motor is a traction motor with `supply_type = aftermarket` and a `compatibility` value (e-rickshaw, scooter, car). Only parts that exist for one vehicle type, such as e-rickshaw rear axles and body parts, have nodes of their own.

### 3.9 Football and sports goods

**Sports goods and toys** (78 nodes in the seed)
- Footballs and soccer balls (15 below): Match footballs (2); Training footballs (3); Futsal and indoor footballs; Beach soccer balls; Mini and skills footballs; Football components (4)
- Cricket goods (13 below): Cricket bats (3); Cricket balls (3); Cricket protective gear (3); Cricket stumps, bails and kit bags
- Hockey, rugby and team ball sports (8 below): Hockey sticks; Hockey balls and goalkeeping kit; Rugby balls; Volleyballs; Basketballs; Handballs and netballs; American footballs; Baseballs and softballs
- Racket sports and golf (5 below): Badminton rackets and shuttlecocks; Tennis rackets and balls; Squash rackets and balls; Table tennis bats, balls and tables; Golf clubs, balls and bags
- Boxing, martial arts and combat sports (6 below): Boxing hand protection (1); Punching bags and speed bags; Boxing headguards and body protectors; Martial arts uniforms; Martial arts belts, pads and kick shields
- Gym and fitness equipment (6 below): Dumbbells, barbells and weight plates; Kettlebells; Weight benches and racks; Treadmills and cardio machines; Skipping ropes, resistance bands and yoga mats; Gym gloves and weightlifting belts
- Athletics, swimming and water sports (3 below): Athletics equipment; Swimming goggles, caps and fins; Surfboards and water sports equipment
- Winter, camping and outdoor sports (4 below): Skis, snowboards and skates; Tents and camping shelters; Sleeping bags; Fishing rods, reels and tackle
- Sports protective gear and apparel (5 below): Football shin guards and goalkeeper gear; Football and team jerseys; Tracksuits and sports shirts; Football boots (1)
- Toys and games (2 below): Soft toys and dolls; Board games and puzzles

Deep path, footballs and soccer balls:

- Footballs and soccer balls (industry) [HS 9506]
  - Match footballs (family) [HS 950662]
    - Thermally bonded match footballs (product) [HS 950662]
    - Hand-stitched match footballs (product) [HS 950662]
  - Training footballs (family) [HS 950662]
    - Machine-stitched PU training footballs (product) [HS 950662]
    - PVC training and promotional footballs (product) [HS 950662]
    - Rubber moulded footballs (product) [HS 950662]
  - Futsal and indoor footballs (family) [HS 950662]
  - Beach soccer balls (family) [HS 950662]
  - Mini and skills footballs (family) [HS 950662]
  - Football components (family) [HS 9506;4016;5903]
    - Football panels and die-cut sheets (product) [HS 950699]
    - Football bladders (product) [HS 401699]
    - Laminated synthetic leather for footballs (product) [HS 590320]
    - Football stitching thread and valves (product) [HS 540110]

Facets: `material` = PU, PVC, TPU, EVA, latex bladder, butyl bladder; `process` = hand-stitched, machine-stitched, thermally bonded; `spec` = size 1 to 5, panel count, pressure; `standard` = FIFA Quality, FIFA Quality Pro, IMS. The Sialkot supply chain is made of stage makers (panel cutting, printing, stitching, bladders), so components are nodes (they are products with different makers), and the stage is the `process` facet on the finished ball.

### 3.10 Fans

**Fans and air-moving products** (38 nodes in the seed)
- Ceiling fans (9 below): AC induction ceiling fans (3); DC and BLDC inverter ceiling fans (2); Decorative and designer ceiling fans; Industrial and high-volume low-speed ceiling fans
- Pedestal, table and wall fans (6 below): Pedestal and stand fans; Table and desk fans; Wall and bracket fans; Tower fans; Rechargeable and USB fans; Window and wall exhaust fans
- Industrial fans and blowers (6 below): Axial flow fans; Centrifugal fans and blowers; Roof extractors and ventilators; Cooling tower fans; Jet and tunnel ventilation fans; Poultry and greenhouse fans
- Automotive and electronic cooling fans (2 below): Car and truck cooling fans; Computer and electronics cooling fans
- Air coolers and evaporative cooling (2 below): Room air coolers; Industrial evaporative coolers
- Fan components (6 below): Ceiling fan motors and stators; Fan blades; Fan capacitors; Fan regulators and speed controllers; Fan bodies, canopies and covers; Fan copper and aluminium winding wire

Deep path, ceiling fans:

- Ceiling fans (industry) [HS 841451]
  - AC induction ceiling fans (family) [HS 841451]
    - Ceiling fans 56 inch (1400mm) (product) [HS 841451]
    - Ceiling fans 48 inch (1200mm) (product) [HS 841451]
    - Ceiling fans 42 inch and 36 inch (product) [HS 841451]
  - DC and BLDC inverter ceiling fans (family) [HS 841451]
    - BLDC ceiling fans with remote (product) [HS 841451]
    - Solar DC ceiling fans (product) [HS 841451]
  - Decorative and designer ceiling fans (family) [HS 841451]
  - Industrial and high-volume low-speed ceiling fans (family) [HS 841459]

Facets: `spec` = sweep (mm), RPM, power (W), air delivery, motor type, blade count; `material` = aluminium blades, pressed steel, ABS, copper or aluminium winding; `standard` = PS 1 (UNVERIFIED which edition), IEC 60335-2-80 (UNVERIFIED); `cert` = Pakistan Energy Label (PEL), PSQCA mark, SASO, CE (`01_entry_fields_per_family.md` 6.24 `R`). "BLDC inverter fan" is a node (different motor, different supply chain, a government target `S`); "56 inch" is a `spec` value, and also a convenient variant node because the trade names fans by sweep.

### 3.11 Sanitaryware

**Sanitaryware, taps and bathroom fittings** (64 nodes in the seed)
- Ceramic sanitaryware (24 below): Water closets and toilet pans (6); Flushing cisterns (2); Wash basins (5); Bidets; Urinals (3); Ceramic kitchen and laundry sinks; Ceramic shower trays and bathtubs; Ceramic bathroom accessories
- Taps, mixers and valves (17 below): Basin taps and mixers (4); Kitchen sink taps and mixers (2); Bath and shower mixers (3); Angle valves and stop cocks; Health faucets and bidet sprays; Flush valves and cistern fittings; Tap cartridges and aerators; Showers and shower heads
- Metal and stainless sanitaryware (7 below): Stainless steel kitchen sinks (2); Stainless steel wash basins; Cast iron and enamelled steel bathtubs; Steel bathtubs and shower trays; Grab bars and sanitary hardware
- Plastic and acrylic sanitary products (6 below): Acrylic and plastic bathtubs; Plastic and acrylic shower trays; Toilet seats and covers; Plastic cisterns and concealed flushing tanks; PVC squat pans and bidets; Shower cabins and enclosures
- Bathroom accessories and furniture (4 below): Towel rails, robe hooks and holders; Floor drains, traps and waste fittings; Bathroom vanities and cabinets; Bathroom mirrors

Deep path, water closets:

- Water closets and toilet pans (family) [HS 691010]
  - Floor-mounted one-piece water closets (product) [HS 691010]
  - Floor-mounted two-piece close-coupled water closets (product) [HS 691010]
  - Wall-hung water closets (product) [HS 691010]
  - Back-to-wall water closets (product) [HS 691010]
  - Squat pans (product) [HS 691010]
  - Rimless water closets (product) [HS 691010]

The pilot note says ceramics and fittings are two buyer sets (`03_other_clusters_and_murree.md` section 1, item 3 `R`); they are two industries here. Facets: `material` = vitreous china, fireclay (ceramic); brass, zinc alloy, stainless steel (taps); `process` = slip casting, pressure casting, glazing, tunnel kiln, roller kiln; `spec` = flush volume, trap type, rough-in; `cert` = WaterMark, WRAS, SASO, PSQCA (the sanitaryware standard was not found in the pilot research, a gap `R`).

### 3.12 Furniture

**Furniture** (78 nodes in the seed)
- Living room furniture (13 below): Sofas and sofa sets (6); Armchairs and accent chairs; Coffee tables and side tables; TV units and entertainment lounges; Display cabinets and crockery units; Shoe racks and entryway furniture; Ottomans, poufs and benches
- Dining and kitchen furniture (9 below): Dining table sets (3); Dining chairs; Sideboards and buffets; Bar stools and bar counters; Modular kitchen cabinets; Pantry and storage units
- Bedroom furniture (18 below): Beds (6); Wardrobes and almirahs (2); Dressing tables and mirrors; Bedside tables and chests of drawers; Mattresses and bedding (4); Cradles and cots
- Office furniture (11 below): Office desks and executive tables; Workstations and cubicles; Office chairs (3); Conference and meeting tables; Filing cabinets and storage; Steel lockers; Reception counters; Library and warehouse shelving
- Institutional and hospitality furniture (10 below): School and college furniture (3); Hostel and dormitory furniture; Hotel bedroom furniture; Restaurant and banquet furniture; Auditorium and cinema seating; Mosque and religious furniture; Hospital and clinic furniture
- Outdoor and garden furniture (5 below): Rattan and cane furniture sets; Teak and wooden garden benches; Metal and wrought iron garden furniture; Plastic chairs and tables; Garden swings and hammocks
- Furniture components and hardware (4 below): Furniture hinges, slides and handles; Furniture foam and upholstery materials; Hand-carved wooden panels and mouldings; Furniture polish and finishing

Deep path, sofas and sofa sets:

- Sofas and sofa sets (family) [HS 940161]
  - Three-seater and two-seater sofas (product) [HS 940161]
  - Sectional and L-shaped sofas (product) [HS 940161]
  - Recliner sofas and armchairs (product) [HS 940161]
  - Wooden-frame sofa sets (product) [HS 940161]
  - Sofa beds (product) [HS 940141]
  - Chesterfield and classic sofas (product) [HS 940161]

Facets: `material` = sheesham, kikar (acacia), deodar, teak, oak, walnut, MDF, plywood, rattan, leather, fabric; `process` = hand-carved, CNC carved, veneered, lacquered, upholstered, knock-down; `style` = modern, classic, carved. The pilot note re-scopes furniture to the Chiniot, Gujrat and Faisalabad belt `R`; that is a place question, solved by the place tree, not by new nodes. Furniture sells visually and our pages are text only (C29), so wood, finish and dimensions as facets matter more here than anywhere `I`.

### 3.13 Textiles and garments

**Textiles** (70 nodes in the seed)
- Yarn and thread (13 below): Cotton yarn (4); Polyester and synthetic yarn (3); Blended yarn; Viscose and rayon yarn; Wool and acrylic yarn; Sewing thread
- Woven fabrics (16 below): Grey (greige) cotton fabric; Dyed and printed cotton fabric (6); Polyester and synthetic woven fabric (2); Viscose and rayon woven fabric; Wool and worsted fabric; Silk fabric; Linen and flax fabric; Jute fabric and hessian
- Knitted fabrics (5 below): Single jersey and rib fabric; Interlock and fleece fabric; Terry and towelling fabric; Pique and polo fabric; Lace and elastic knitted fabric
- Home textiles (18 below): Bed linen and bedsheets (3); Towels (4); Blankets and throws (2); Curtains and drapes; Quilts, comforters and duvets; Tablecloths and napkins; Prayer mats; Tents, tarpaulins and canvas goods; Sacks and bags of textile materials
- Carpets, rugs and floor coverings (5 below): Hand-knotted carpets and rugs; Machine-made carpets; Tufted carpets and rugs; Kilims and flat-woven rugs; Prayer rugs and mats
- Technical textiles and trimmings (6 below): Nonwoven fabrics; Industrial belting and coated fabrics; Webbing, tapes and elastics; Lace, embroidery and trimmings; Rope, twine and cordage; Labels, badges and woven trims

**Apparel and garments** (54 nodes in the seed)
- Men's and boys shirts (7 below): Formal and dress shirts; Casual shirts; Polo shirts; T-shirts (2); Kurtas and traditional menswear
- Men's and boys trousers and suits (6 below): Jeans and denim trousers; Chinos and casual trousers; Formal trousers; Suits and blazers; Waistcoats and vests; Shorts and cargo pants
- Women's and girls apparel (8 below): Dresses; Blouses and tops; Skirts and culottes; Shalwar kameez and kurtis; Abayas, hijabs and modest wear; Sarees and lehengas; Women's trousers and leggings; Lingerie and bras
- Knitwear and sweaters (4 below): Pullovers and sweaters; Cardigans and jerseys; Hoodies and sweatshirts; Thermal underwear
- Underwear, socks and hosiery (4 below): Men's briefs and boxers; Socks; Tights and stockings; Pyjamas and nightwear
- Children's and infants wear (2 below): Babywear and rompers; School uniforms
- Uniforms and workwear (4 below): Industrial workwear and coveralls; Military and police uniforms; Medical scrubs and lab coats; Chef and hospitality uniforms
- Outerwear (4 below): Down and puffer jackets; Windbreakers and rain jackets; Fleece jackets; Overcoats and parkas
- Garment accessories (5 below): Textile gloves; Caps and hats; Scarves, shawls and mufflers; Neckties and bow ties; Handkerchiefs

Deep paths, cotton yarn and men's shirts:

- Cotton yarn (family) [HS 5205]
  - Carded cotton yarn (product) [HS 520512]
  - Combed cotton yarn (product) [HS 520523]
  - Open-end cotton yarn (product) [HS 520512]
  - Organic and BCI cotton yarn (product) [HS 520523]

- Men's and boys shirts (industry) [HS 6205;6105]
  - Formal and dress shirts (family) [HS 620520]
  - Casual shirts (family) [HS 620520]
  - Polo shirts (family) [HS 610510]
  - T-shirts (family) [HS 610910]
    - Round-neck T-shirts (product) [HS 610910]
    - Printed and promotional T-shirts (product) [HS 610910]
  - Kurtas and traditional menswear (family) [HS 620590]

Facets: textiles `fibre`, `process` (ring spun, air-jet, dyeing, printing, finishing), `cert` (OEKO-TEX, GOTS, BCI, GRS); apparel `gender`, `season`, `cert` (WRAP, BSCI, OEKO-TEX, SA8000), `process` (cut-make-trim, full package FOB, embroidery, printing, washing). Dyeing and finishing are processes: a dye house attaches to the fabric it finishes with `business_type = sub_contractor` (rule A8). Apparel is the least covered sector in the seed (54 nodes of about 2,820); the garment type list is the product level and the fit, fabric and wash are facets.

### 3.14 Other sectors (skeleton only)

The seed also holds 18 skeleton sectors with industries taken from ISIC classes (wood, paper and printing, chemicals, pharmaceuticals, rubber and plastics, building materials, basic metals, fabricated metal, electronics, electrical equipment, machinery, road vehicles, other transport, jewellery and misc, food, beverages, tobacco, petroleum): 111 rows, level 1 and 2 only. They show where each HS chapter and ISIC class lands; their depth is the next job.

---

## 4. How "list type x place" scales from 10,000 to 500,000 types

### 4.1 Inputs

| Input | Value | Grade |
|---|---|---|
| Place levels named by the founder (Hotels logic): world, country, region (state or province, `admin1`), city, business district (`area`) | 1; 250; 4,500; 130,000; 1,300,000. **Total 1,434,751** | Countries `I`. `admin1` `H` (GeoNames gives per-country counts, for example Thailand 77 and Tajikistan 5 `R`, but no global total was found). Cities: GeoNames `cities1000` has about 130,000 entries `R`; `cities15000` about 25,000 `R`. Areas `I`: 1.5 million places at the 100-million-entry stage less 194,000 up to city level (hosting note `R`) = about 1.3 million; Overture `division_area` holds 1,067,718 features (June 2026) `R` |
| Row of `PlaceList` | 144 B (60 B heap, 84 B indexes) | `R` hosting note section 2.2 |
| Row of `RollupCell` (non-empty cell) | 302 B | `R` hosting note |
| Insert speed | 352 million rows in 1 to 4 hours = about 24,000 to 98,000 rows a second; WAL about 2.5 times stored size | `R/EST` hosting note |
| Type counts | 235 today; 10,000; 50,000; 100,000; 500,000 | Scenarios. Composition from section 3.1: levels 1 to 3 = 3,961; level 4 = 8,433 (base, estimated) |
| Manufacturing entries | 10,000 (pilot), 100,000, 1 million, 5 million (the 100-million-entry stage, 5% share) | `H` |
| Memberships per entry | 3 on average (1 primary, 2 secondary); sensitivity 2 and 8 | `H` |
| Cell touches per membership | place chain 4.3 x type chain 5.2 (depth 4.3 plus 20% for second parents) = **22.4** | `I` |

Types are cheap; place x type is what explodes. A node costs about 1.3 KB across `Concept`, four labels with their search indexes, settings, reserved slug and crosswalk rows `H`, so 12,394 types are 16 MB, 51,966 are 68 MB and 500,000 are 650 MB.

### 4.2 Option A: a stored row for every type at every place (decision E27, superseded)

Rows = types x 1,434,751 places (five levels), 144 B each.

| Types | Rows | Size | WAL (x2.5) | Insert time at 24k to 98k rows/s |
|---|---|---|---|---|
| 235 (today) | 337 million | 48.6 GB | 121 GB | 1 to 4 hours |
| 10,000 | 14.3 billion | **2.1 TB** | 5.2 TB | 41 to 166 hours (6.9 days) |
| 50,000 | 71.7 billion | 10.3 TB | 25.8 TB | 203 to 830 hours (34.6 days) |
| 100,000 | 143.5 billion | **20.7 TB** | 51.7 TB | 407 to 1,661 hours (69 days) |
| 500,000 | 717 billion | **103 TB** | 258 TB | 2,033 to 8,303 hours (346 days) |

If all ten place levels (3.2 million places, high case `R` hosting note) are used: 10,000 types give 32 billion rows (4.6 TB); 100,000 types 320 billion (46 TB); 500,000 types 1.6 trillion (230 TB). The restore time at the measured 70.6 MB/s (hosting note) for 2.1 TB is 8.1 hours, and the table could not be rebuilt in a maintenance window. **Verdict: impossible beyond about 235 types.** The founder's earlier "150 billion rows" warning (D-06 conflict note) is the 100,000-type line here.

### 4.3 Option B: hybrid with a pre-seeded spine

Store a list at a place when the type is shallow enough for that place level, plus every cell that has an entry. Types shallower than a depth limit exist "empty" at big places. Rows = types (world) + 250 x types to depth 4 + 4,500 x types to depth 3 + 25,000 (cities of 15,000 people or more) x types to depth 2, for the recommended policy.

| Policy | Rule | Rows, 10,000 types | Rows, 50,000 | Rows, 500,000 | Size |
|---|---|---|---|---|---|
| Lean | world: all; country: depth 4; admin1: depth 2; city (15k+): depth 1 | 5.8 million | 6.4 million | 6.9 million | 0.8 to 1.0 GB |
| **Recommended** | world: all; country: depth 4; admin1: depth 3; city (15k+): depth 2 | 35.0 million | 35.7 million | 36.1 million | 5.0 to 5.2 GB |
| Rich | world: all; country: depth 5; admin1: depth 4; every city (130k): depth 3 | 562 million | 582 million | 599 million | 81 to 86 GB |

The spine hardly changes as types grow from 10,000 to 500,000, because it depends only on how many types sit at depths 1 to 3 (3,961 in the base estimate), not on the long tail of variants. That is the finding: **depth, not type count, drives stored rows.** A spine only buys empty pages at big places, and empty pages are what we do not want indexed.

### 4.4 Option C: rows only where entries exist (decision E28, adopted by the founder)

An entry's address sets its one home place. It counts for that place and every place above, and for its node and every node above (D-06). Model `I`: for each (place level, type depth) the number of possible cells M = nodes at that depth x active places; attachments A fall into them; distinct cells = skew x M x (1 - e^(-A/M)), with skew 0.6 `H` for concentration in popular cells. Active places at 5 million entries `H`: world 1, country 220, admin1 3,800, city 45,000, area 120,000 (30% of entries have an area-level home).

| Manufacturing entries | Memberships (A) | Non-empty cells | As `RollupCell` (302 B) | As `PlaceList` (144 B) |
|---|---|---|---|---|
| 10,000 (pilot) | 30,000 | 247,550 | 75 MB | 36 MB |
| 100,000 | 300,000 | 2.09 million | 630 MB | 300 MB |
| 1 million | 3 million | 15.5 million | 4.7 GB | 2.2 GB |
| **5 million** | 15 million | **58.1 million** | **17.5 GB** | 8.4 GB |
| 5 million, 2 memberships each | 10 million | 41.8 million | 12.6 GB | 6.0 GB |
| 5 million, 8 memberships each | 40 million | 123.5 million | 37.3 GB | 17.8 GB |

Where the 58.1 million cells sit (5 million entries, 3 memberships): world 31,000; country 3.7 million; admin1 16.5 million; city 27.6 million; area 10.2 million. The upper bound with no sharing is 15 million x 22.4 = 335 million cells. The sibling note (`02_big_site_architecture.md` 3.1) reaches 72 to 144 million with other inputs (300 million memberships, 6 place levels); both are `H` and land in the same range.

**Option C with a store threshold.** Memberships counted over all cell touches: 335 million. A cell can hold 25 members only if at least 25 memberships fall in it, so at most 335 million / 25 = **13.4 million cells** can reach 25 `I`. Store a cell when it has at least 25 members, or at least 10 verified entries (an indexable page, `index_threshold` `R`), or is pinned (sponsored, stewarded, claimed, created by a person). The other cells, at least 44.7 million of the 58.1 million, are answered live: one page of 25 rows is one index range scan, measured at 1.7 ms for a list query and 50 ms for a country-wide category (plan 4.3, quoted in the hosting note `R`). The 13.4 million cells cost at most 4.0 GB as `RollupCell`.

### 4.5 Comparison

| Option | Rows at 10,000 types | Rows at 100,000 types | Storage for 100,000 types | Notes |
|---|---|---|---|---|
| A. Every type at every place | 14.3 billion | 143.5 billion | 20.7 TB | Impossible |
| B. Recommended spine only (empty) | 35 million | 35.7 million | 5.1 GB | Cheap, but stores empty lists |
| B+C. Spine plus entry cells | about 93 million | about 94 million | about 22 GB | Spine adds about 5 GB |
| **C. Entry cells (E28)** | 58 million (5M entries) | 58 million | 17.5 GB | Independent of type count once entries are fixed |
| **C + threshold (25 / 10 verified / pinned)** | at most 13.4 million | at most 13.4 million | at most 4.0 GB | Below threshold, answered live |

Reading: with E28 the number of **stored** lists grows with entries and memberships, not with types or places. Going from 10,000 to 500,000 types changes the type tables from 13 MB to 650 MB and does not change the cell count except through more memberships.

### 4.6 Recommendation

| ID | Recommendation |
|---|---|
| R1 | **E28 stands.** A stored list is a non-empty roll-up cell. `PlaceList` is kept only for pinned cells (sponsored, stewarded, claimed, created by a person). `generate_lists --all` stays a small-seed tool. |
| R2 | **No spine of empty rows.** The recommended spine costs 5 GB and buys empty pages. If the founder wants Hotels-style world and country pages always present, store only world and country at depth 4: 250 x 12,394 = 3.1 million rows (0.45 GB). |
| R3 | **Virtual resolution keeps C11 true.** An empty (place, type) request returns 200, `noindex,follow`, with links to the nearest populated lists (same type at the parent place; child places; parent type at the same place) and an "add the first entry" action. The code already resolves any list-type slug under any place and returns a zero cell `R` (`catalog/resolver.py`, `catalog/queries.py::rollup`), so this holds at any type count. |
| R4 | **Store threshold:** 25 members, or 10 verified, or pinned. Everything else is a live query. |
| R5 | **Variants are listable on demand** (rule T3, 10 entries). |
| R6 | **Roll-ups in batch, set-based, tree-reduced.** Compute leaf cells by `GROUP BY` over the membership table, then add up along the place chain and the type chain. Per-write increments would touch 22.4 cells per membership and make the world-level and sector-level cells a write hot spot (requirement D-10). 15 million memberships x 22.4 = 335 million touches for the first load. Partition `RollupCell` by country group (`02_big_site_architecture.md` BS-02). |
| R7 | **Ancestor lookup by closure table or stored path**, not by walking `parent`. Closure rows: 51,966 nodes x about 4.5 ancestors = about 234,000 rows at base; 500,000 nodes x 5 = 2.5 million `I`. A sector-level cell has up to 40,000 descendants, too many for an `IN` list. Cells larger than a set size serve a cached top-N page (ranked) and use counts from the roll-up, not live counts. |
| R8 | **Index by natural scale** (section 2.8): global-scale types index at world and country; national-scale types down to the state, and the city only with 10 verified entries; city-scale types down to the district. Facet pages are noindex except promoted landing pages. |

### 4.7 What the repository does today (read from code, `R`)

| ID | Finding | File |
|---|---|---|
| F1 | `refresh_for_entry` and `recount_all` loop over `concept_chain(entry.primary_concept)`: **secondary products and second parents never count.** | `backend/analytics/rollups.py` |
| F2 | `recount_cell` builds a Python list of every entry in the cell (`_entries_in`). A sector cell or the world cell loads millions of rows. | same |
| F3 | `descendant_concept_ids` runs one query per tree level and returns every descendant ID. | same |
| F4 | `recount_all` calls `recount_cell` once per distinct (place, concept) and each call re-reads entries. | same |
| F5 | `generate_lists` default mode (`from_entries`) does `Place.objects.filter(path=...).first()` and `get_or_create` for every cell: 2 queries a cell. At 58.1 million cells and about 1 ms a query that is 2 x 58.1 million x 1 ms = 116,000 s = **32 hours** of query time alone `I`. `--prune` loads every `PlaceList` row with its place into Python. | `backend/core/management/commands/generate_lists.py` |
| F6 | `Concept` has `parent` only: no level, no stored path, no multi-parent, no `merged_into`, no slug history. `Kind.PRODUCT` exists and is unused. | `backend/taxonomy/models.py` |
| F7 | `resolve()` finds a list type by slug under any place and returns a page with a zero cell when there are no entries. Virtual resolution already works. | `backend/catalog/resolver.py` |
| F8 | `ConceptCrosswalk.system` is 20 characters, with no edition or licence class. | `backend/taxonomy/models.py` |
| F9 | `seed_extended_list_types` reads `name, slug, family, scale, form, child, health, source`; it cannot load the new CSV (`parent_id`, `level`, `hs_code`, `facets`). | `backend/taxonomy/seeds.py` |
| F10 | `Entry` has the primary list index `entry_list_query (country, place_path, primary_concept, publish_state)`; secondary memberships have no list index. | `backend/entries/models.py` |

---

## 5. The seed file

`01_manufacturing_seed.csv`: header `id,parent_id,level,name,slug,hs_code,isic_code,synonyms,natural_scale,facets`, 1,170 rows, UTF-8, `\n` line ends.

| Column | Meaning |
|---|---|
| `id` | Seed key (rule I2): file block x 1,000 plus order. Not the permanent ID |
| `parent_id` | Primary parent's `id`; blank for the 30 sectors (their parent is the existing family "Manufacturing and trade") |
| `level` | `sector`, `industry`, `family`, `product`, `variant` (rule 2.1). In the seed, 18 skeleton sectors have levels 1 and 2 only |
| `name` | Our own wording under rules N1 to N7 |
| `slug` | Base slug (rule S1). The list-type slug adds `-manufacturers` (S2) |
| `hs_code` | HS 2022 code or codes, 2, 4 or 6 digits, no dots, joined with `;`. The nearest code, not always an exact match |
| `isic_code` | ISIC Rev 4 two- or four-digit code, joined with `;` |
| `synonyms` | Aliases joined with `;` (plurals, trade names, local names, other spellings) |
| `natural_scale` | `city`, `national` or `global` (section 2.8): 114 city, 966 national, 90 global |
| `facets` | `group=value|value;group=value`; inherited down; reserved key `also_under` for secondary parents |

**Counts.** 1,170 nodes: 30 sectors, 177 industries, 489 families, 434 products, 40 variants. The 12 named sectors hold 1,059 nodes; the 18 skeleton sectors hold 111. 270 distinct HS6 codes are used; 128 rows carry more than one HS code (sector and industry rows); 1,166 rows have an HS code; all 1,170 have an ISIC code; 416 rows have synonyms (602 aliases); 70 rows carry facet groups (26 facet keys, 559 distinct values); 21 rows have secondary parents. Longest slug 58 characters, mean 26.

**Checks run (script, outside the repository).** Every HS code exists in the HS 2022 table (100%); every ISIC code is in the Rev 4 list (division or class); every slug is unique; every parent exists; no row is deeper than level 5; every `also_under` target exists and sits exactly one level above its child; no name contains "other", "n.e.c." or "miscellaneous". **Not checked:** whether each HS or ISIC code is the *right* one. The mapping is my judgement, so grade `I`, `UNVERIFIED`. Known weak points: HS 4203.21 for sports gloves that are not leather; HS 9506.99 as a catch-all for cricket, boxing and martial-arts goods; HS 3922 and 7324 for sanitaryware (right headings, many products inside); ISIC for fans (2750 domestic, 2819 non-domestic, `UNVERIFIED`), EV chargers (2790, `UNVERIFIED`) and battery materials (2011, 2029); battery-material HS codes (2841, 2820.90, 3801.10, 3824.99, 3920.62) are approximate. Before the first load, the AI auditor and one trade reviewer per sector should sample every HS and ISIC mapping in the 12 named sectors (`ai-auditor` skill; rule 6 needs 90% accuracy).

**Loader design (not built).** Read the CSV in `id` order; map each `id` to a ULID through a `seed` crosswalk row; create nodes with the parent, labels (name and synonyms), crosswalks (`hs2022`, `isic4`), settings and, for `kind = list_type`, a reserved slug; create `ConceptEdge` rows from `also_under`; write facet definitions and values from `facets`; dry run first, and report counts. All 40 variants in the seed (35 surgical, 5 leather) load as `kind = product` (rule T2) and are promoted by the 10-entry rule; staff may promote the surgical ones by hand for the pilot.

---

## 6. Requirements and open decisions

### 6.1 Requirements

Status checked against the repository on 2026-10-06: **built**, **partly**, **not built**.

| ID | Requirement | Priority | Status |
|---|---|---|---|
| MD-01 | `Concept` gains `level` (1 to 7), `listable`, status values `residual`, `merged`, `retired`, `merged_into` and a stored `path` | P0 | Not built (F6) |
| MD-02 | `ConceptEdge` for up to 3 secondary parents, with reason and a cycle check | P0 | Not built |
| MD-03 | Closure table or path prefix, used by roll-ups and list queries | P0 | Not built (F3) |
| MD-04 | Entry-to-node relation with role (primary, secondary), evidence, check label, `broad` flag and product attributes; partial unique index for one primary | P0 | Partly (primary FK and a plain many-to-many) |
| MD-05 | Roll-ups count secondary memberships and all parents, as set-based batch with distinct counts, partitioned by country group | P0 | Not built (F1 to F4) |
| MD-06 | Facet registry (`FacetDef`, `FacetValue`), product-scope values, narrow filter table | P0 | Partly (`AddonField` and `AddonTemplate` give company-scope facets with a `filterable` flag) |
| MD-07 | Concept slug history with 301; rules S1 to S5; list-type slug suffix | P0 | Partly (`ReservedSlug`; no history) |
| MD-08 | Crosswalk gains `edition` and `licence_class`; system list as in 1.3 | P1 | Partly (table exists; F8) |
| MD-09 | Idempotent CSV loader for the seed with dry run and report | P0 | Not built (F9) |
| MD-10 | Virtual empty list page with links to the nearest populated lists and "add the first entry" | P0 | Partly (resolution works, F7; nearest-list links not checked) |
| MD-11 | Store rule: non-empty cell, and 25 members or 10 verified or pinned | P1 | Partly (E28 built, no threshold) |
| MD-12 | `generate_lists` and roll-up rebuild as set-based SQL in chunks, per country, no per-cell queries | P0 | Not built (F5) |
| MD-13 | Promotion job: a variant becomes a list type at 10 entries | P1 | Not built |
| MD-14 | Node proposal queue: agent proposals with at least three independent verbatim evidences, duplicate check by folded label and Wikidata QID, staff approval | P1 | Not built |
| MD-15 | `place_kind` tag at area level: business district, industrial estate, export processing zone, special economic zone, market | P1 | Not built |
| MD-16 | Written permission requests to WCO, UNSD, GS1, UNDP and ECLASS e.V.; counsel's view on storing code numbers | P0 | Not done |
| MD-17 | Seed audit: every HS and ISIC mapping in the 12 named sectors sampled by the AI auditor and one trade reviewer per sector | P0 | Not done |
| MD-18 | Indexing by natural scale; promoted facet landing pages; sitemap shards | P1 | Partly (`index_threshold`, `indexable_list` exist) |
| MD-19 | Taxonomy tests: acyclic, unique slug, depth at most 7, HS code exists in the stated edition, no catch-all names | P1 | Not built (run once by script for the seed) |
| MD-20 | Index for secondary memberships (concept, country, place path, entry) | P0 | Not built (F10) |

### 6.2 Open decisions for the founder, with suggested defaults

| # | Decision | Suggested default |
|---|---|---|
| OD-1 | Empty (place, type) page: 200 noindex page, or 404 | 200, `noindex,follow`, nearest-list links (R3). It satisfies C11 and E28 together |
| OD-2 | URL form: `-manufacturers` suffix and a role-less tree (traders are a filter) | Yes. Separate trader or retail lists only where a different buyer exists (spare parts shops stay in the retail family) |
| OD-3 | Variant promotion threshold | 10 entries, the same as `index_threshold` |
| OD-4 | Maximum depth | 5 standard, 7 absolute, levels 6 and 7 only for assembly trees |
| OD-5 | Secondary parents | Up to 3, each with a reason |
| OD-6 | Who approves new nodes | Staff taxonomist; agents propose with three independent evidences; no auto-creation |
| OD-7 | HS code numbers | Store as a private crosswalk now; show on public pages only after the WCO answers in writing |
| OD-8 | ISIC edition | Rev 4 now; add Rev 5 from UNSD correspondence tables |
| OD-9 | Pharmaceuticals and food | Skeleton only; each gets its own drug or food vocabulary later (licences not researched) |
| OD-10 | Spine of empty upper-level lists | None. If wanted, world and country at depth 4: 3.1 million rows, 0.45 GB |
| OD-11 | Seed review before load | AI auditor plus one trade reviewer per sector; pilot trade (Sialkot surgical) first |
| OD-12 | Industrial estates as places | Add `place_kind`; fill from government lists and contributors, not OpenStreetMap |
| OD-13 | The seeded "Factories and suppliers" type | Retire after its entries are re-tagged to product nodes (D-01) |
| OD-14 | Use of the MIT-licensed Shopify taxonomy for attribute vocabularies | Yes, with the MIT notice kept, after checking the repository `LICENSE` file |

### 6.3 Gaps and conflicts

- **No licence page was opened.** Every licence statement is from a search summary. WCO, UN, GS1, UNDP and ECLASS terms need to be read and, where unclear, asked in writing (MD-16).
- **ISIC Rev 4 counts** (21, 88, 238, 419) are from memory, `UNVERIFIED`. Rev 5 counts are reported (22, 87, 258, 463).
- **NAICS counts conflict** in snippets (1,012, 1,039, 2,125). The manufacturing figures (21 subsectors, 86 groups, 346 industries) come from one Census-linked summary.
- **Overture:** places data licences are reported as permissive; a sibling note says the divisions theme is ODbL. I did not resolve it.
- **Node estimates rest on multipliers I chose** (m4, m5, 2.5 and 6). They are hypotheses; the range 32,000 to 92,000 only varies m5. A sample of 20 real catalogues per sector would calibrate them.
- **Entry numbers** (5 million manufacturing entries; 3 memberships; 5% share) are guesses. IndiaMART reports 8 million sellers `S` including traders; no source gives world manufacturer counts (UNIDO publishes establishment counts for 79 to 138 countries by year `S`, not opened).
- **Place counts:** no global `admin1` count found (4,500 `H`). The 1.3 million business-district figure is derived, not counted.
- **Wikidata product coverage is not measured by us.** The one study found reports incomplete classes.
- **Sialkot figures** (10,000 products; 99% share) come from TDAP snippets `S, UNVERIFIED` via `01_sialkot_surgical_sources.md`.
- **The seed is a sample** (4.3% of the 12 sectors). Counts in section 3 are estimates, not an inventory.
- **Not logged in `docs/DECISIONS.md`** (the brief limited me to the two files). The recommendations R1 to R8 and OD-1 to OD-14 are proposals, not decisions; E28 is the only decision they rely on. Suggested log line: "2026-10-06 research: product depth taxonomy and scale note written; seed of 1,172 nodes; no decision taken."

### 6.4 Sources

Searches run 2026-10-06 (standard mode, snippets only). Pages named in results:

- HS: https://en.wikipedia.org/wiki/Harmonized_System ; https://www.mayerbrown.com/ja/insights/publications/2020/01/harmonized-system-nomenclature-2022-edition-accepted-by-world-customs-organization ; https://www.wcoomd.org/zh-cn/media/newsroom/2025/april/hsc-provisionally-adopts-the-recommendation-for-hs-2028-amendments-at-75th-session.aspx ; https://xtares.admin.ch/tares/html/licence_notes_e.html ; https://datahub.io/core/harmonized-system ; data file https://raw.githubusercontent.com/datasets/harmonized-system/main/data/harmonized-system.csv (read directly).
- ISIC and CPC: https://ecosoc.un.org/sites/default/files/documents/2023/BG-3j-ISIC-Rev5-E.pdf ; https://unstats.un.org/unsd/classifications/Workshops/AddisAbaba2026/Session3-Deck1_WorkshopAddis_intro_to_isic_rev5.pdf ; https://unstats.un.org/unsd/classifications/Family/Detail/1074 ; https://unstats.un.org/unsd/classifications/Workshops/AddisAbaba2026/Session4-Introduction-to-the-CPC-Ver-3-0.pdf ; UN copyright notice https://www.un.org/en/aboutun/copyright/ .
- UNSPSC: https://www.unspsc.org/ ; https://www.onetcenter.org/dictionary/29.1/mssql/unspsc_reference.html . GPC: https://www.gs1.org/sites/default/files/gpc_development_and_implementation_1.pdf ; https://ref.gs1.org/gs1/ip-policy . eCl@ss: https://eclass.eu/shop/en/product/eclass-14-0 ; https://en.wikipedia.org/wiki/ECLASS .
- NAICS: https://www.census.gov/data/tables/2022/econ/economic-census/naics-sector-31-33.html ; https://worldoftaxonomy.com/codes/naics_2022/31-33 . HTS: https://www.usitc.gov/sites/default/files/tariff_affairs/documents/2020_hts_item_count.pdf .
- Google taxonomy: https://webappick.com/google-product-category-taxonomy-guide/ . Shopify: https://github.com/Shopify/product-taxonomy . Wikidata: https://www.wikidata.org/wiki/Wikidata:Licensing . Overture: https://docs.overturemaps.org/guides/places/taxonomy/ ; https://stac.overturemaps.org/2026-06-17.0/divisions/division_area/collection.json . OSM: https://lists.openstreetmap.org/pipermail/legal-talk/2013-March/007498.html .
- Competitor calibration: IndiaMART https://en.wikipedia.org/wiki/IndiaMART ; https://www.shiprocket.in/blog/most-selling-products-on-indiamart/ ; Alibaba https://www.worldfirst.com/sg/blog/selling-online/how-to-sell-on-alibaba-com/ .
- Geography: https://hash.ai/@geonames/cities ; https://geonames.org/statistics/thailand.html .
- Repository (read): `docs/DECISIONS.md`, `docs/REQUIREMENTS_DEPTH_AND_SCALE.md`, `backend/taxonomy/{models,seeds,services}.py`, `backend/taxonomy/data/list_types.csv`, `backend/analytics/{models,rollups}.py`, `backend/core/management/commands/generate_lists.py`, `backend/catalog/{resolver,queries,seo,views}.py`, `backend/entries/models.py`, `research_notes/Pilot trade research/`, `research_notes/Backend research/01_entry_fields_per_family.md` (6.24, 6.25), `03_hosting_and_costs.md`, `research_notes/Scale research/02_big_site_architecture.md`.
