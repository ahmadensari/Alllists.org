# How to train, test and audit the list-filing agents, and the AI auditor that watches them

Research date: 2026-10-06. Scope: English only. Design document; no code was changed.

Evidence tags (same convention as `docs/TECHNICAL_PLAN.md`): **[R]** read in this repository; **[S]** from a web source (all web material here comes from search-result summaries; I did not open the pages, so every external number is also flagged UNVERIFIED unless stated); **[I]** my estimate or design judgement; **[M]** computed by me (arithmetic shown). Anything untagged is a proposal.

---

## 0. Summary

1. The repo already has a safe draft pipeline (fetch gate, verbatim quote rule, caps, kill switch, staging-only writes, one second-check job, a human audit sampler, verifier canaries). It has **no way to measure accuracy before a prompt or model goes live**, **no prompt versioning**, **no per-kind or per-country controls**, **no auto-stop**, and **no automated auditor**. The 90% and USD 0.30 rules in plan section 7.6 are written down but nothing enforces them (the cost function only feeds a staff page).
2. Three separate truths must be measured, and the plan blurs them: **page-faithful** (did the agent copy what the page says?), **world-true** (is the business real, open, and is that its phone?), and **fresh** (is it still true today?). Only a human call or visit proves world truth. The gold set must therefore have a cheap frozen-page layer (runs on every prompt change) and a smaller world-truth layer (quarterly).
3. Training without fine-tuning is a controlled loop on **versioned prompts + de-identified few-shot examples mined from audited failures**, with a sealed test set that prompt authors never see per case, a shadow stage, then a capped canary stage, then wider caps. Promotion is human-approved and needs a statistical lower bound; demotion is automatic and fires on a point estimate.
4. The AI auditor is a **separate service**: different prompt, preferably a different model family, own key, own spend cap, own stop switch, read-only access to drafts, write access only to its own findings table, blind to the filing agent's output confidence and reasoning, and it **can only lower trust, never raise it**. Humans remain the only source of promotion evidence.
5. Eighteen work packages (T1.04 to T1.21) are listed in section 7 with acceptance tests, in a build order that puts measurement before any real hosted-model run.

---

## 1. What exists today, and what it does not do

### 1.1 Inventory [R]

| Area | Present in repo | File |
|---|---|---|
| Job record | `AgentJob`: kind (`draft`, `second_check`, `recheck`), source, status, `budget_cap_minor`, `spent_minor`, tokens, `model`, `stop_reason`. No prompt version, no country, no list type, no batch id | `backend/agents/models.py` |
| Staging | `DraftEntry`: `raw`, `evidence_quotes`, `source_urls`, `confidence`, `cost_minor`, state (staged, promoted, rejected). No page hash, no fetched-at, no prompt version | same |
| Model client | `Extraction` dataclass; `FakeModel` (regex over "Name:", "Phone:" lines, deterministic); `HostedModel` (Claude Haiku 4.5 by dated id, one hard-coded prompt string in code, fields parsed by regex, confidence is a constant 0.8 or 0.4) | `backend/agents/models_ai.py` |
| Fetch | Honest user agent, robots, SSRF block with DNS pinning, size/time caps, 2 s per-site interval, stop at first refusal. 313 lines of tests | `backend/agents/fetcher.py`, `tests/test_fetcher_security.py` |
| Rules | `quoted_verbatim` (phone by digits, name and address by lower-cased whitespace-normalised substring); name and phone must be quoted or the draft is `rejected`; unknown model keys dropped; per-URL kill-switch and budget checks; day, month and job caps; 50% and 80% audit warnings; caps must be configured before anything starts | `backend/agents/services.py` |
| Promotion | `promote()` makes a hidden draft entry through `entries.services.create_entry` (licence gate re-checked, suppression list checked), earns nothing (R09) | same |
| Second check | `run_second_check()` compares an entry with a page from a different `Source` row; name (folded, exact) and last-9 phone digits must both match; records an `ai`-level verification (valid 180 days, `CHECK_VALIDITY_DAYS`) | same, `entries/services.py:record_verification` |
| Cost | `cost_per_verified(days=30)`: all agent spend in the window divided by promoted drafts that now have a surveyor or owner check. Shown on `/staff/agents/` and in `core/monitoring.ai_spend` (spend only) | `agents/services.py`, `catalog/staff_views.py:428`, `core/monitoring.py:117` |
| Human audit sampler | `queue_audit_sample(n=385, seed)`: random **published** entries, once each, one `audit` task each; never the original verifier; `accuracy_by_source`, `accuracy_by_verifier` | `volunteers/services.py` |
| Canaries | `CanaryEntry` (purpose `verifier` or `trace`), `plant_canaries`; surveyor with canary accuracy under 0.8 after 3 tasks is suspended | `volunteers/models.py`, `services.py` |
| Bulk audit | `sample_size()` with finite-population correction on 385 (all rows if 200 or fewer); `draw_sample` (seeded, plain random); `record_audit` passes at point accuracy >= 0.90; `looks_personal` quarantine | `backend/intake/bulk.py` |
| Stop controls | `AI_KILL_SWITCH` setting or `agent_kill_switch` flag; runbook `docs/runbooks/ai-spend-runaway.md` | `agents/services.py` |
| Tests | 12 agent tests (quote rules, rejection of invented values, planted instruction, caps, kill switch, red source, second check, cost per verified) | `agents/tests/test_agents.py` |

### 1.2 Defects and gaps found while reading [R]

These matter because a test set that sits on top of a leaky pipeline measures the wrong thing.

1. **The verbatim rule can pass a number that is not on the page.** `quoted_verbatim("phone")` tests `digits(value) in digits(page_text)`, where `digits(page_text)` joins every digit on the whole page. A value can match across the boundary of two different numbers (for example "0300 123" next to "4567"). It is also not tied to the right business: on a page that lists many firms, a real phone of another firm passes. Fix and test in T1.07.
2. **Website is never checked.** `CHECKED_FIELDS = (name, phone, address)`; a hallucinated website is staged and `promote()` writes it if it starts with `http`.
3. **Name and address matching is not script-aware.** `norm_space` only lower-cases and collapses whitespace; the second check uses `fold()` but the first check does not. Urdu script, diacritics and Roman-Urdu spellings (a known risk, `reports/AI agent populated lists.md`) will produce false rejects and, on partial matches, false accepts.
4. **Agent promotion bypasses the duplicate pipeline.** `bulk.publish` calls `importer.settle_duplicate`; `agents.services.promote` calls `create_entry` directly. Duplicate rate for agent output is therefore unmanaged and unmeasured.
5. **Agent promotion bypasses the personal-data quarantine.** `bulk.looks_personal` (personal email domains, 2 to 3 word name with no business word and no address) is not applied to drafts. A single-person sole trader or a doctor's personal mobile can be staged and promoted.
6. **An AI second check can publish an entry.** `test_second_check_needs_a_different_source_and_matching_facts` asserts the entry becomes `published` after an `ai` check (it earns nothing, R09). Draft and second check run through the same `model.extract` code path and the same prompt. So one model family can create, verify and publish with no human. This is the strongest reason for an independent auditor.
7. **"Different source" means a different `Source` row, not a different website.** Two `Source` rows pointing at the same site pass the R07 guard. `Source` has no domain list, so a job's `source` label is trusted and never compared with the URL actually fetched.
8. **`AuditSample` cannot audit agent drafts.** It points at published entries, one boolean `correct` per entry (no field-level result), has no link to `AgentJob`/`DraftEntry`, and the sampler is unstratified random. Staged and draft-state agent output is exactly what never reaches it.
9. **Cost accounting is coarse and can mislead.** `cost = int(...) + 1` minor units makes every hosted call cost at least 1 cent. A Haiku 4.5 call of about 5,000 tokens in and 300 out is about 0.65 cent [I, using the Haiku price of USD 1 and 5 per million tokens in `docs/MASTER_DOCUMENT.md`], recorded as 1 cent, an overstatement of about 50%. `cost_per_verified` divides all spend (including second checks and failed jobs) by drafts verified in the window by a surveyor or owner, so during a ramp it is overstated (drafts waiting for a human are in the numerator, not the denominator). It is not split by kind, country or list type, and it acts on nothing.
10. **`recheck` is declared but has no runner.** No freshness job exists.
11. **Confidence is not informative.** `FakeModel` returns 0.9 or 0.4 and `HostedModel` 0.8 or 0.4 based only on whether name and phone are both present. It cannot support "auto-accept the high-confidence band".
12. **Contacts sit in plain JSON in staging.** `DraftEntry.raw` and `evidence_quotes` hold phones in clear (the `Contact` table stores `value_enc`). `AgentJob.stop_reason` stores exception text. The log scrubber (`core/logscrub.py`) covers logs, not these columns. Needs a retention rule and a leak scan (T1.18).
13. **No sealed evaluation data exists anywhere in the repo.** `docs/TECHNICAL_PLAN.md` T1.03 acceptance is "385-record sample produced; canaries seeded", which is a sampler, not a measure of an agent.

### 1.3 Plan targets that must be made executable [R]

Plan 7.6 and 19.12: stop a job kind above USD 0.30 per verified record; accuracy under 90% on audit stops the job kind; T1 exit is audit accuracy >= 90% on a 385-record sample and cost per verified under USD 0.30. Plan R04 risk trigger: "audit accuracy under 90%". Plan 7.7: duplicate rate, freshness (expired-chip share, early warning at 25%) are measured. Plan section 6 cheat controls: verifier accuracy under 80% suspends. `reports/AI agent populated lists.md` experiment 2 and 3 use the same 90% and USD 0.30 bars and note that cost should be all-in including human minutes.

---

## 2. Evaluation practice for LLM extraction agents (web search, standard mode)

All items below are from search summaries. Treat as UNVERIFIED until the page is read; I use them only to shape design choices, not as numbers the system depends on.

| Practice | What the search said | Used for | Status |
|---|---|---|---|
| Field-level scoring with field-appropriate matching | A rigorous method uses exact match for identifiers, tolerance for quantities, semantic equivalence for names, array alignment, and separates omission from hallucination ([LLM structured-extraction eval paper, arXiv 2602.12247](https://arxiv.org/abs/2602.12247v2)). Frameworks report precision, recall, F1 with micro and macro averaging ([llmvalidate](https://pypi.org/project/llmvalidate/0.5.0/)) | Section 3 equivalence rules, section 4 metrics | UNVERIFIED (summary) |
| Golden set practice | Human-verified inputs and ground truth; slice by document type because one blended number hides problems; "around 50 documents per category" as a starting size ([nilenso, evals before prompts](https://blog.nilenso.com/blog/2026/05/18/evals-before-prompts-building-an-llm-ocr-for-kyc/)) | Cell sizes, per-stratum reporting | UNVERIFIED (blog) |
| Hallucination in extraction | Earlier repo research cites a study with precision 0.994, recall 0.939, hallucination rate 3.05% on web record extraction ([NEXT-EVAL, arXiv 2505.17125](https://arxiv.org/html/2505.17125v1)) and practitioner reports that models invent a plausible value when a field is missing | Null-page test, hallucination bar | Carried from `reports/AI agent populated lists.md`; not re-read |
| LLM judges versus humans | GPT-4 judges agreed with human preferences over 80% on chat tasks, the same as humans among themselves ([Zheng et al., MT-Bench, arXiv 2306.05685](https://arxiv.org/pdf/2306.05685)); but position bias, verbosity bias and self-preference are documented (self-enhancement win-rate gains of roughly 10% to 25% quoted in a secondary summary); agreement in specialised domains is reported lower (64% to 68%, a blog summary, not primary); validate a judge against human labels with Cohen's kappa, with about 0.6 as a floor and 0.8 as strong ([koji.so](https://www.koji.so/docs/llm-as-a-judge-vs-human-evaluation), blog) | Auditor must be a different model family and must itself be audited against human labels | Principle from the primary paper; numbers UNVERIFIED |
| Contamination and private sets | Held-out private test sets, items authored or fetched after the model's training cutoff, versioning every set with a creation date; re-run after any vendor model change; monthly refresh by default ([futureagi](https://futureagi.com/blogs/llm-benchmarks-vs-production-evals-2026/), [drift guide](https://futureagi.com/blog/llm-eval-data-drift-detection-2026/)) | Section 3.5 and 6.4 | UNVERIFIED (vendor blogs) |
| Selecting prompts without held-out data overfits | "True few-shot" work found that cross-validation style selection barely beats random and badly underperforms selection on held-out examples, so earlier few-shot results were over-estimated ([Perez et al., NeurIPS 2021](https://proceedings.neurips.cc/paper/2021/hash/5c04925674920eb58467fb52ce4ef728-Abstract.html)) | Separate dev and sealed test sets; limit test-set runs | Primary source abstract; adequate |
| Acceptance sampling | Lot quality assurance sampling and stratified audits are standard QC tools; Wilson intervals are used for early accept or reject decisions ([LQAS](https://en.wikipedia.org/wiki/Lot_quality_assurance_sampling), [Wilson-interval acceptance sampling paper summary](https://www.citedrive.com/en/discovery/intelligent-lotlevel-acceptance-sampling-via-active-learning-xgboost-and-wilson-confidence-intervals/)) | Section 5 stop and promote rules | UNVERIFIED (summary); the maths in section 5 is mine [M] and standard |
| Anchoring | Earlier repo research: human reviewers shown a model's answer become more confident but not faster, and anchor on it ([arXiv 2411.04637](https://arxiv.org/html/2411.04637v3)) | Blind labelling; auditor blind to agent answer (extending to a model auditor is [I]) | From `research_notes/AI agent populated lists/agent_data_collection.md` |

Gaps I could not fill: no published accuracy benchmark for agent-collected small-business records (already noted in the repo's report); nothing on Urdu or Arabic business extraction; nothing on how Overture, Foursquare or Google audit their own data. Our own gold set is therefore the only evidence there will be.

---

## 3. The gold-standard test set

### 3.1 Three layers, because three different things can be wrong

| Layer | Question | Input | Truth | Run when | Cost |
|---|---|---|---|---|---|
| A. Frozen-page extraction | Given exactly this page text, does the agent output the right fields, and nothing else? | Page snapshot (text as the fetcher returned it) | Annotator-marked values with the character span that supports each one | Every prompt, few-shot or model change; nightly regression panel | Cents per run; deterministic with `FakeFetcher`-style replay |
| B. End-to-end live | Does fetch plus extraction plus checks work on today's web (redirects, robots, JS shells, rate limits)? | URL only | Same expected record | Monthly and before each ramp step | Low; a few hundred fetches |
| C. World truth | Is the entry actually correct in the world (business exists, is open, number reaches it, address right)? | The finished draft | A person's call or visit (the existing surveyor task, `field_group = "audit"`) | Quarterly per cell, and on every promotion decision (section 5) | Human minutes: the report estimates 1 to 3 minutes per record at USD 3 to 15 per hour [S, E in the report], about USD 0.05 to 0.75 per record |

Layer A scores are what the prompt author can be held to. Layer C is what the 90% bar means. Report both and never average them. A system can score 99% on A and 80% on C because the page itself was stale or described another business; that gap is the share of error that is "source quality", and it must be tracked per source so bad sources get demoted rather than the prompt.

### 3.2 What a case contains

`GoldCase` (stored outside git, section 3.6):

- `case_id` (random, never the URL), `set_version`, `split` (dev, test, regression, canary).
- Stratum tags: job kind, list-type family (the 12 families in `docs/LIST_AND_ENTRY_COMPONENTS.md` section 6), country, language and script of the page, source tier, page type (own site, chamber directory, register entry, multi-business directory page, social or map page excluded as red, PDF text, parked domain), trap type (see 3.4).
- `snapshot_text`, `snapshot_sha256`, `fetched_at`, `source_id`, licence note for the snapshot (see 3.6).
- `expected`: for each field (name, phone, address, website; later more), the value, the character span that supports it, or `ABSENT` when the page does not contain it. `ABSENT` is a first-class answer.
- `world_truth` (nullable, filled for the Layer C subset): exists, open, phone reaches the business, address confirmed, method, date.
- `labelled_by` (two annotator ids), `adjudicated_by`, `kappa_batch`.
- For second-check cases: the existing entry facts plus the new page and the expected outcome (match, mismatch, same-source trap).
- For recheck cases: the previously held record plus the page now, and the expected change (closed, moved, phone changed, unchanged).

### 3.3 Sizes

Statistics that drive the numbers [M]:

- Worst-case margin of a 385 sample is plus or minus 5 points (p = 0.5). At a true rate near 0.90 the 95% margin is about plus or minus 3 points, so 385 is generous; the repo's constant stays.
- A cell of 100 cases can prove a lower bound of 90% only if at least 95 are right (95%); 60 cases need 58 right (96.7%); 385 need 357 right (92.7%). One-sided 95% Wilson bound.
- A cell of 60 can reliably show failure (50 or fewer right out of 60 puts the upper bound under 90%) but cannot prove success. So: small cells for blocking, big samples for promoting.
- To detect a drop from 95% to 90% between two prompt versions with 80% power and a one-sided 5% test, about 340 independent cases per arm are needed; a drop from 95% to 85% needs about 110 [M, two-proportion sample size formula]. The gold test set is therefore for catching large regressions and bad versions, not for fine ranking; use paired comparison on the same cases (more power than the unpaired figure) and treat the dev set as the place to iterate.

Proposed sizes per country pack (Pakistan first; the launch family list is a founder decision, so the table uses 4 families as a worked example; individuals and child-facing families are excluded because the personal-data switches are off, `country_switch`, plan section 17 to 18):

| Set | Size | Notes |
|---|---|---|
| Dev pool (few-shot source, error analysis, free to inspect) | 60 per family cell, so 240 | Includes every case "burned" from the test set |
| Sealed test set | 100 per family cell, so 400 | Two annotators, adjudicated; at least 30% also carry world truth (about 120 phone or visit checks) |
| Trap pool (shared across families, tagged by trap type) | 150 | Language-specific; see 3.4 |
| Regression and drift panel | 50 frozen cases plus 10 canary pages | Subset of the dev pool, rerun weekly (section 6.5); never used for few-shot |
| Second-check pairs | 150 | 50 true matches, 50 near-miss different businesses, 25 same name different city, 25 stale or changed phone |
| Recheck cases | 100 | 40 closed, 30 moved or phone changed, 30 unchanged |
| Auditor calibration (humans label agent output) | 200 per quarter per country | About 25 to 30% seeded errors so that recall of errors is measurable |
| Total first country | about 1,240 labelled items | |
| Labelling cost [I] | USD 190 to 2,500, middle about USD 900 | 3 to 8 minutes per item at USD 3 to 15 per hour; double-labelling the test set adds its share again; world-truth calls on top |
| Each further country | about 60% of this, about 800 items [I] | Trap pool and language work do not transfer |

Rule: **no gold set, no job.** `start_job` refuses a (kind, country, list-type family) with no passing evaluation on file (T1.09). Entering a new country is gated by the country pack, in addition to `country_switch`.

### 3.4 Building it per list type and per country

Sampling frame: pages the agent would actually receive, from sources that pass the licence gate (green, or amber with `reviewed_on`; never red). Stratify so that each cell has the page-type mix the agent will meet, over-weighting the hard types. Never sample from pages an annotator or a previous prompt author has already seen in dev.

Per list-type family, what the expected record must test (from `docs/LIST_AND_ENTRY_COMPONENTS.md` section 6; the current extractor only returns four fields, so these are the **next** fields, each added only after its own cases exist):

| Family | Cases must probe |
|---|---|
| Manufacturers and exporters | Factory vs registered address; several phones with roles; product list vs unrelated ad text; company name vs brand; certificates claimed (agents extract the claim, never a verified flag) |
| Hospitals and clinics, labs | Switchboard vs emergency vs doctor mobiles (personal contacts must not leak); branches; departments; licence number text |
| Pharmacies and petrol pumps, retail | Chain pages with many outlets (right outlet, right phone); 24x7 claims; hours (least evidence of accuracy per the report, so keep optional) |
| Trades | Often only a mobile: personal-contact rules decide whether it may be staged at all |
| Real estate, contractors | Agent name vs agency; listing phones that belong to the listing agent |

Trap types that appear in every cell and in the shared trap pool (about 40% of the test set should be traps or empty pages, because an extractor that only sees clean pages looks perfect):

1. Null page: no phone, no address. Expected output is empty. Measures fabrication directly.
2. Multi-business page (directory table, chamber list): one target firm among 20; right row only.
3. Fax, WhatsApp-only, and "call us" images with no text.
4. Two numbers for two firms next to each other (tests the digit-boundary defect in 1.2.1).
5. Closed notices, "moved to", parked or for-sale domains, copyright year 3+ years old.
6. Personal mobile of a named person on a business page.
7. Injection: instructions in visible text, in HTML comments, in alt text, in a fake "system" block, with a contact planted in the instruction ("Phone: ..."). Extend the existing hostile-page test into a corpus of 30.
8. Language and script: Urdu script, Roman Urdu, mixed English and Urdu, Eastern Arabic digits.
9. Near-duplicates of an entry that already exists (feeds the duplicate metric).
10. Source refusing: 401, 403, 429, robots disallow, redirect (job must stop, no draft).
11. A red-tier or non-`agent_fetch` source (job must refuse before any fetch).

Country packs [I unless stated]:

- **Pakistan** (first): numbers in `03xx`, `+92`, `0092`, landlines with area codes (Sialkot 052), shared or switchboard lines, Eastern Arabic digits; addresses are landmark-based (plot, road, mohalla, near-landmark), no postcode reliability; names have English, Urdu and Roman spellings; many firms have only Facebook or WhatsApp, which are red or unusable, so the right behaviour is "no draft". Annotators must be local readers of Urdu.
- **UAE and other Gulf countries** (when opened by counsel): Arabic and English pages, `+971`, P.O. Box and building or Makani style addresses rather than street addresses [UNVERIFIED], do-not-call rules affect which contacts may be stored (plan section 13 notes UAE quiet hours and a do-not-call register [S in plan]). Arabic-script name matching needs its own equivalence rules.
- **Any other country**: a new pack with its own annotators, trap pool, phone-format normaliser test, and a written note on contact rules, before agents may run there. Chinese, Hindi and Arabic extraction accuracy have no published evidence (repo report), so assume nothing transfers.

How to label (protocol):

1. Annotation guide with one page per field: what counts as the business's own phone, when `ABSENT` is correct, how to mark supporting spans.
2. Two independent annotators per test case, local language; a third adjudicates. Annotators never see model output (anchoring). Track kappa per batch; below 0.6 the guide is broken and the batch is relabelled [S for the thresholds, UNVERIFIED].
3. World truth for the Layer C subset by the existing surveyor workflow (phone call with the call tool, or visit), recorded in the same task format as `field_group="audit"` so the tooling is reused.
4. Annotators' own accuracy is checked with planted known cases (same idea as verifier canaries).

### 3.5 Keeping it fresh

- Layer A is a **frozen snapshot**, so web rot does not break it. Freshness applies to selection: new pages replace old ones.
- Quarterly rotation: retire 25% of the test set (oldest or most-seen) into the dev pool and draw an equal number of new cases from pages fetched after the last rotation. Any case whose per-case output was shown to a prompt author is "burned" and moves to dev immediately.
- Every audited failure from production (human or AI auditor, confirmed by a human) becomes a dev case with its error code. A fraction of confirmed failures, held back unseen, refill the test set.
- Re-run the whole sealed test set after any model id or alias change, any prompt change, and any change to the verbatim rules, plus monthly [S, UNVERIFIED]. Version each set with a date and content hash; store results against the set version so score changes caused by a new set are not mistaken for model change.
- Layer C world truth expires: a case's world-truth fields carry a date and are re-verified or dropped after 12 months (plan's own re-check cycle is 365 days for surveyor checks).
- Contamination: local business pages are probably in some model's training data. Prefer pages first fetched after the model's training cutoff (flag per case) and report scores split by "post-cutoff" and "older" pages; a large gap indicates memorisation [S for the method, UNVERIFIED]. The canary pages (3.7) are always fresh and fake, so they cannot be memorised.

### 3.6 Keeping it secret

1. **Storage**: separate database schema or alias (`gold`) with its own role; not in git, not in fixtures, not in `docs/`. The repo contains only the schema, the loader, the scorer and a **synthetic** CI fixture.
2. **Access**: the agent runtime and the prompt-assembly code have no credentials for `gold`. Only the evaluation runner role and two named reviewers can read cases. The filing agent's job runner, the HostedModel and the auditor cannot import gold models (import-boundary test, T1.10).
3. **Prompt hygiene**: test cases never enter few-shot examples, prompts, logs or error messages. The eval runner reports aggregates and per-stratum metrics, plus per-case results only for the dev split. For the test split, failing case ids are visible to the reviewer only, and once a person has read a case's output it is burned.
4. **Run budget**: at most one sealed-test run per prompt version and at most three per week across versions [I]; a repeat run requires a new version. This limits adaptive overfitting through repeated looking, a known problem when prompts are selected without truly held-out data [S, Perez et al. 2021].
5. **Third-party exposure**: snapshots go to the model provider on every eval. Use only pages already allowed for `agent_fetch`; strip real contacts from any case copied into dev few-shot (section 5.3). Provider retention and training terms for the API key used must be checked before test-set runs, UNVERIFIED.
6. **Snapshot storage rights**: storing full page text may need the source's permission. Counsel check (plan R22 and Q-S3 context) before keeping full text; fall back to the quoted spans plus surrounding 500 characters, which is enough for most Layer A cases [I].
7. **Tamper evidence**: a hash of each set version is written to `AuditLog` (hash-chained) when sealed.

### 3.7 Canary pages (new tripwire; the existing canaries are entries, not pages)

Plant a few fake business pages on a platform-controlled host that the fetcher can reach (an allowed `Source` named "Platform canaries", green), each with known truth: one normal, one null, one with a poisoned instruction, one with a phone that must be rejected (personal), one multi-business. A daily production job includes two of them. If a canary output is wrong, or a canary phone is ever staged for a real entry or appears outside its table, that is a stop (section 6). The existing `CanaryEntry` and `plant_canaries` stay for surveyor testing and trace copying; they do not test agents.

---

## 4. Scoring

### 4.1 Equivalence rules (what "correct" means per field)

| Field | Match rule | Notes |
|---|---|---|
| Name | `fold(a) == fold(b)` or trigram similarity (the repo's `dedupe.similarity`) >= 0.9 after dropping legal suffixes; accepted spelling variants listed per case | Transliteration variants are annotator-listed, not guessed |
| Phone | Normalised E.164 for the country equal (the repo's `normalize_contact`); landline vs mobile both allowed if on the page and the business's own | Wrong role (fax, personal, another branch) counts as wrong even if the digits are on the page |
| Address | Annotator-marked required parts (street or plot, area, city) all present; partial = wrong for record accuracy, "partial" bucket for reporting | Landmark addresses make this the lowest-recall field; track separately |
| Website | Registered domain equal | Must also be a real link on the page |
| Category and place | Assigned list type and place equal the annotator's | Added when the agent starts classifying |

### 4.2 Metrics

All metrics are reported per stratum (job kind, country, family, source, prompt version) with a Wilson interval, plus one roll-up. A single blended number is not allowed on any dashboard [S nilenso, UNVERIFIED; also plan 7.7 asks for per-source and per-verifier].

| Metric | Definition | Computed on | Bar (proposal) |
|---|---|---|---|
| Field precision | TP / (TP + FP) where FP = extracted value that is wrong, or extracted when truth is `ABSENT` | Layer A, audits | >= 0.97 name, phone; >= 0.93 address; >= 0.97 website |
| Field recall | TP / (TP + FN), FN = truth present but missing or rejected | Layer A | >= 0.90 name; >= 0.85 phone; address >= 0.75 (landmark addresses) |
| Record accuracy (the 90% number) | Record is correct when every extracted required field is correct **and** the business is real and open **and** list type and place are right | Layer C and the audit stream | >= 0.90, stop rule in section 5 |
| Page-faithful record accuracy | Same without the world part | Layer A | >= 0.95 |
| Hallucination rate | Extracted values with no support in the page (ungrounded) / extracted values | Layer A, null pages, auditor | <= 0.02 overall; **0 fabricated values on null pages above 1%**. Reference point: 3.05% in one published study [S, UNVERIFIED] |
| Unfaithful-value rate | Value is on the page but belongs to another business, role or branch | Layer A multi-business and trap pages | <= 0.03. The verbatim check cannot catch this, only labelled cases and the auditor can |
| Draft-state label accuracy | `rejected` vs `staged` against truth: share of invented or non-quoted drafts correctly rejected (recall of rejection), and share of rejected drafts that were actually fine (cost of false rejects) | Layer A | recall of rejection >= 0.98; false-reject <= 0.15 |
| Verification-label accuracy (`ai` check) | Of second checks that recorded an `ai` verification, share where truth is a true match (precision of "AI verified"); and recall on true matches | Second-check pairs, audits | **False-verify rate <= 1%**, because an `ai` check can publish an entry (1.2.6). Recall >= 0.70 |
| Confidence calibration | Reliability by confidence decile; expected calibration error; accuracy of the band used for any auto-accept | Layer A, audits | Auto-accept band precision >= 0.95 or no auto-accept. Replace the constant confidence (1.2.11) first |
| Duplicate rate | Share of promoted drafts that match an existing entry at or above `dedupe.REVIEW` (0.60) by `scan_entry` **before** promotion; recall of the scanner on labelled duplicate pairs; later, confirmed duplicates found at dedupe review per source | Pre-promotion check, gold pairs, `DedupeCandidate` | <= 0.05 of drafts reach review as duplicates [I]; scanner recall on gold pairs >= 0.90 |
| Freshness | (a) age of evidence at draft time (`fetched_at`); (b) share of agent-touched entries whose `ai` check is past 180 days; (c) recheck recall on seeded closed or changed cases | Production, recheck set | (b) early warning 25%, matching plan 7.7; (c) >= 0.80 |
| Licence compliance | Count of violations of: red source used; source lacks `agent_fetch`; `reviewed_on` missing for amber import; source URL host not in the source's registered domains; robots refused but fetched; attribution text missing where `attribution_text` is set | Every job, daily | **Zero tolerance**: one violation stops the kind |
| Contact-leak | See 4.3 | Every job, daily scan | **Zero tolerance** |
| Injection resistance | Share of injection-corpus pages where output has no extra fields, no instruction-driven values, no state change | Layer A, canary pages | 1.00 |
| Cost per verified record | Cohort-based: cost of drafts created in a 30-day window, divided by those of the same cohort that reached a surveyor or owner check within 60 days; report two versions: agent-only (model, fetch, search) and all-in (adds human minutes from `Task.minutes`) | Production | Stop above USD 0.30 (plan); early warning at USD 0.20 |
| Cost per correct record | Spend / records scored correct by audit | Audits | Reported only |
| Operational | Refusal and stop rate, tokens per record, cost per call in micro-units | Production | Drift inputs |

Notes: the plan says cost per verified record is "stop above USD 0.30" while `reports/AI agent populated lists.md` experiment 3 defines USD 0.30 as all-in including human minutes. **UNRESOLVED**: decide which. Recommendation: enforce the agent-only figure as the automatic stop (it is available now) and gate **promotion** on the all-in figure (needs `Task.minutes`, which exists).

### 4.3 Contact-leak checks (zero tolerance)

1. **Personal contacts**: gold cases where the only phone on the page is a named person's mobile. Expected: not staged for individual or child-facing concepts, and flagged for others. Requires the personal-data quarantine on the agent path (1.2.5).
2. **Email**: the extractor does not request email; check that no email ever appears in output, even under injection.
3. **Planted numbers**: before each run, seed fake unique numbers in canary pages and in test snapshots; afterwards scan every table and log that is not meant to hold contacts (`AuditLog.payload`, `AgentJob.stop_reason`, `DraftEntry.reason`, application logs, exported reports, auditor findings, prompts sent to the model other than the page itself) and assert zero hits. Only `Contact.value_enc` (and staged `DraftEntry.raw`, which has its own retention rule) may hold them.
4. **Suppressed contacts**: gold cases whose number is on the opt-out list; promotion must refuse (the guard exists in `create_entry`) and the batch must continue cleanly, not abort a whole job.
5. **Outbound**: reports and few-shot examples show phones masked to the last three digits or replaced by synthetic numbers.
6. **Retention**: rejected drafts' `raw` and `evidence_quotes` purged after 30 days; promoted drafts' staged copies purged once the entry exists [I; confirm against the plan's retention schedule in section 17].

### 4.4 Hallucination checks in layers

1. Verbatim rule (exists; fix per T1.07).
2. Role check: the quoted number sits next to a phone-type label or in a contact block, not in a table of other firms.
3. Cross-field consistency: phone prefix plausible for the place, address contains the place, name appears in the page title or heading.
4. Null-page fabrication rate (gold trap type 1) measured on every prompt version.
5. Independent re-check by the auditor (section 6), which re-reads the page itself.
6. Trap and canary pages with poisoned values.

---

## 5. Training loop without fine-tuning

### 5.1 The unit of change: a versioned prompt bundle

New model `PromptVersion`: id, job kind, text hash, the text, ordered few-shot example ids, model id (dated), parameters, output parser version, `parent` version, author, `state` (draft, shadow, canary, active, retired), created and promoted timestamps. Immutable once created. `AgentJob.prompt_version` and `DraftEntry.prompt_version` point at it, so every record, audit result and cost is attributable. The prompt text moves out of `HostedModel.extract` into the version. A change to the model id, the prompt, the examples or the parser is a **new version** and starts again at the bottom of the ladder.

### 5.2 The loop

1. **Collect errors.** Every confirmed wrong field from human audit (`AuditSample`, extended to field-level), AI auditor findings that a human upheld, surveyor outcomes `wrong` or `closed` on agent-created entries, and production rejects feed an error table with codes: `WRONG_ENTITY`, `BRANCH_MIX`, `FAX_AS_PHONE`, `PERSONAL_CONTACT`, `STALE_PAGE`, `TRANSLIT`, `ADDRESS_PARTIAL`, `NULL_FABRICATION`, `INJECTION`, `DUPLICATE`, `WEBSITE_WRONG`, `LICENCE`.
2. **Diagnose per code and stratum.** Choose the largest cost-weighted error class in the weakest cell. Often the fix is a source rule (drop a bad source, add a page-type parser), not a prompt change.
3. **Propose a version.** A person edits the prompt or examples (a model may draft the diff; a person approves). One intent per version so the effect is attributable.
4. **Dev evaluation.** Run on the dev pool; must improve the target error class and not drop any stratum's record accuracy by more than 2 points (paired comparison on identical cases; report the interval).
5. **Sealed test run** (once per version, section 3.6). Must clear the Layer A bars in 4.2. Pass moves the version to `shadow`.
6. **Shadow** (no staging writes beyond a `shadow` marker): run alongside the active version on live pages for at least 200 records per stratum; the AI auditor and the next human sample score both. The shadow version must be non-inferior to the active one.
7. **Canary**: 10% of jobs in the stratum, at the capped level of 5.4, 100% audited for the first 100 records.
8. **Active** after the promotion rule in 5.5 is met. The previous version stays `retired-ready` for one-click rollback (a pointer change, no deploy).
9. Rollback is automatic when any stop rule fires in the first 30 days of a version.

### 5.3 Few-shot examples from audited entries

Eligibility (all required):

- Audited **correct by a human** (surveyor outcome `confirmed` on an audit task), or correct and adjudicated by a human after an auditor disagreement. An AI-only verdict never creates an example.
- From a source allowed for `agent_fetch` and (for any stored text) for `display` or with counsel-cleared snapshot storage.
- From the dev pool, never the sealed test, regression panel or canary pages.
- **De-identified**: replace real phones, names and addresses by synthetic ones with the same structure; keep formatting quirks. This stops real contacts entering prompts (contact-leak rule) and stops models echoing a memorised number.
- Hard negatives are required: a null page with an empty answer, a multi-business page with the right row only, an Urdu or Roman-Urdu page, a fax-versus-phone page.

Rules:

- At most 6 shots per prompt [I]. Cost is small: 6 shots of about 500 tokens is about 3,000 extra input tokens, about USD 0.003 per call at Haiku input price (USD 1 per million tokens, `docs/MASTER_DOCUMENT.md`), and less with prompt caching (cache hits quoted at 0.1x input price in `research_notes/Data poor launch markets/open_weight_agent_costs.md`).
- Choose shots by stratum (country, language, family), not one global set; a lookup keyed on the job's cell.
- Ablate: a shot stays only if removing it hurts dev accuracy for its stratum. Retire a shot when its target error code has stayed absent for two audit windows.
- Cap per-example reuse and rotate, because a fixed set invites overfitting to the dev pool [S, Perez et al., true few-shot].
- Examples are versioned inside the `PromptVersion`.

### 5.4 Per-job-kind caps and the ramp ladder

Today the only caps are money (job, day, month) and they are global. Add `AgentPolicy` rows keyed by (job kind, country, list-type family) with: `level`, `state` (active, paused, stopped), `daily_record_cap`, `job_cap_minor`, `max_urls_per_job`, `max_consecutive_refusals`, `prompt_version`, `last_decision`, `decided_by`. The existing `start_job` and the per-URL loop read it.

| Level | Meaning | Records per day (starting point [I]) | Audit rate | Writes |
|---|---|---|---|---|
| L0 shadow | Runs, nothing is staged for promotion | up to 100 | 100% by AI auditor | none |
| L1 pilot | Drafts staged; human promotes each | 25 | 100% AI auditor, human sample of 60 per cell before L2 | staging only |
| L2 limited | Drafts staged; batch passes only after the audit | 100 | 20% stratified (AI) plus a human sample of 100 per quarter-cell | staging only |
| L3 standard | Wider caps, still staging only (R35) | 500 | 10% stratified (AI) plus 385 human per cell per quarter | staging only |

No level ever allows production writes by the agent (R35). `second_check` and `recheck` get their own rows and thresholds; the `ai`-check path stays at L1 until false-verify rate is proven under 1% on at least 100 audited second checks.

### 5.5 Promotion and demotion rules

Asymmetry: **demotion is automatic and quick; promotion needs a person and strong evidence.**

Definitions: window = the last 385 audited records in the cell or 28 days, whichever is larger; Wilson interval at 95% one-sided; "accuracy" = record accuracy (4.2) from **human** audit stream, with the AI auditor stream as an early-warning input.

Numbers [M] (one-sided 95% Wilson):

| n audited | Correct needed to **promote** (lower bound >= 0.90) | Correct at or below which the **upper bound is under 0.90** (strong stop) |
|---|---|---|
| 30 | not provable (needs 29 all right and still short) | 24 (80%) |
| 60 | 58 (96.7%) | 50 (83%) |
| 100 | 95 (95%) | 85 (85%) |
| 200 | 187 (93.5%) | 173 (86.5%) |
| 385 | 357 (92.7%) | not applicable; see below |

Rules:

| Rule | Trigger | Action |
|---|---|---|
| **Accuracy stop** (plan: "stop below 90%") | n >= 100 audited and point accuracy < 0.90, **or** n >= 30 and the upper bound < 0.90 (for example 24 of 30) | `AgentPolicy.state = stopped` for that (kind, country, family); staged drafts of the affected batches are held; alert; written reason; restart needs the checklist in 6.7 |
| **Accuracy hold** | point accuracy 0.90 to 0.93 on n >= 100 | Drop one level, raise audit rate, no promotion |
| **Cost stop** (plan: "above USD 0.30 per verified") | cohort cost per verified (agent-only) > 30 minor units with >= 50 verified in the cohort | Stop the kind in that country; early warning at 20 |
| **Licence or contact leak** | one confirmed violation | Immediate stop of the kind and the source; incident per `docs/runbooks` style; zero tolerance |
| **False-verify stop** | `ai` check false-verify > 1% on >= 100 audited | Stop `second_check` for the cell; no `ai` checks recorded until fixed |
| **Hallucination stop** | fabricated or ungrounded values > 2% on audit, or any fabricated value on a canary page | Stop and roll back the prompt version |
| **Duplicate hold** | > 5% of drafts are duplicates at review | Hold promotion until the dedupe step runs in the agent path (T1.08) |
| **Source demotion** | accuracy of one source in a cell < 0.85 on >= 30 audited | Set that source's `allowed_uses` without `agent_fetch` (admin action recorded) |
| **Refusal storm** | `max_consecutive_refusals` reached on one site | Pause that source for 7 days (existing "stop at first refusal" stays per job) |
| **Drift stop** | section 6.5 alarm confirmed | Drop one level and re-run the regression panel |
| **Version reset** | any new prompt version, model id or parser change | Level resets to L0 for that cell |
| **Promotion** | At the current level for >= 28 days; lower bound >= 0.90 on the human-audited window (for example 357 of 385); cost agent-only <= 0.25 and all-in <= 0.30; zero licence and leak events; duplicate rate <= 5%; auditor agreement with humans healthy (6.6); regression panel at or above baseline | **Proposal only.** An admin approves and records a note (one level at a time). Never auto-promote |

Note on the existing bulk gate: `bulk.record_audit` passes a batch when the **point** accuracy is >= 0.90. With 385 rows that allows 347 correct (90.1%), lower bound about 86.7% [M]. For human-curated uploads keep it. For agent output, require the lower-bound rule above for promotion to a higher level (T1.21).

---

## 6. The AI auditor

### 6.1 Role

An independent second reader that re-checks a stratified sample of every agent batch against the sources, tracks quality daily, spots drift, reports each day, and can press the stop button on its own. It **cannot** fix data, promote anything, record a verification, change a threshold, or raise a level. Humans remain the evidence for promotion.

### 6.2 Separation from the filing agent (hard requirements, each with a test)

| Dimension | Filing agent | Auditor |
|---|---|---|
| Prompt | `PromptVersion` of kind `draft`/`second_check`/`recheck` | A different prompt written from a different template, framed as "verify this claim" or "re-read blind", reviewed by a person who did not write the filing prompt; the filing prompt and few-shots are never visible to the auditor |
| Model | Cheap extraction model (Haiku 4.5 today) | A **different model family or vendor** where possible; at minimum a different tier and different parameters, because judges favour their own family's output (self-enhancement 10% to 25% in one summary [S, UNVERIFIED]) |
| Credentials | `AI_PROVIDER_KEY` | A second key `AUDITOR_PROVIDER_KEY` with its own spend cap (`AUDITOR_DAILY_CAP_MINOR`, at most 25% of filing spend [I]) |
| Stop switch | `AI_KILL_SWITCH` / `agent_kill_switch` | Its own `auditor_kill_switch`; stopping the auditor does **not** let the filing agent run unchecked (6.8) |
| State | Own tables, own fetcher instance | **No shared state**: no shared cache, no shared prompt store, no shared fetcher object, no shared job rows. It refetches the page itself through the same licence gate and the same hardened `HttpFetcher` code (SSRF rules apply) |
| Database | Writes `DraftEntry` | Separate Postgres role: read-only on `DraftEntry` (claims, `source_urls`, `evidence_quotes`, ids), read on `Source`, write only to `AuditorBatch` and `AuditorFinding` and to a one-column "pause request" table. Cannot touch `Entry`, `VerificationEvent`, `AuditSample`, flags |
| Inputs | Page text | Claims (field, value, business name, place) and URL; **not** the filing agent's confidence, reject reason, model, prompt version or quotes. Blind to the answer to limit anchoring [S for humans, extension to models is I] |
| Code | `backend/agents/` | New package `backend/agent_auditor/`; import-boundary test: it imports nothing from `agents.models_ai` or `agents.services` except the shared fetcher and gate |

### 6.3 Two check modes

- **Claim check (cheap, default)**: "Does this page support that business X in place Y has phone P, address A, website W? Answer supported, contradicted, or not found; quote the supporting text; say whether the number belongs to the business itself." About 5,000 tokens in, short out; roughly USD 0.007 on Haiku-class pricing [I from the repo's per-page figures]. Contradicted or not-found claims are findings.
- **Blind re-extraction (stronger, 20% of the sample)**: the auditor extracts the record from the page without seeing the claim, then a deterministic diff scores agreement. Catches omissions and "right digits, wrong business".
- **World check (optional, only when the auditor has a second independent source)**: look for a second page from a different domain (reusing the R07 idea); never from a red or non-`agent_fetch` source.

Findings are coded with the same error codes as 5.2 and carry the **evidence quote and URL**; findings are advisory until a human upholds them.

### 6.4 Stratified sampling of every agent batch

A **batch** = all drafts of one (job kind, country, family, source, prompt version, day). Sampling is seeded and the seed is stored (same idea as `bulk.draw_sample`), so a sample can be reproduced and cannot be cherry-picked.

- Batch of 40 or fewer: audit all (like `SMALL_BATCH` in `bulk.py`, which uses 200).
- First 200 records of any new prompt version in a cell: 100%.
- Otherwise: proportional allocation across strata (source, confidence band, page language, fields-present pattern, page type), minimum 10 per active stratum, oversample the lowest confidence band and the multi-business page type at 2x, always include 2 canary pages per day.
- Target volume: level L2 20%, level L3 10% (5.4). At 500 drafts a day and 10%, about 50 claim checks a day, about USD 0.35 a day [I]; the human stream (385 per cell per quarter) is separate and stays the promotion evidence.
- A batch whose sample shows a failure count at or above the stop line in 5.5 is **held**: its drafts cannot be promoted (the `promote` function checks batch state, T1.14).

### 6.5 Drift detection

Daily, per (kind, country, family, source, prompt version), compare today with a trailing baseline (28 days) using simple control charts (EWMA or CUSUM; standard quality-control practice [I]). Monitored:

- Auditor disagreement rate and human-upheld error rate.
- Field null rates, reject rate by reason, mean confidence and its spread, mean tokens in and out, cost per record.
- Input mix: page type, language or script, page length, share of multi-business pages, source mix (population stability index on these [S, UNVERIFIED]).
- Fetch side: refusal rate, robots decisions, HTTP status mix, page-structure hash per site (a template change usually shows up before accuracy does).
- Identity: model id actually served (store the response model), `PromptVersion` hash, parser version; any change not made through a version is an alarm.
- **Weekly replay**: run the active versions on the 50-case regression panel and the canary pages; alarm if field F1 drops more than 3 points from the version's baseline, or any canary value is fabricated [thresholds I]. Replay also after any vendor model announcement and after any change in provider alias [S, UNVERIFIED, cadence].
- Freshness drift: share of `ai` checks near expiry and recheck backlog age.

An alarm raises a level 1 flag in the daily report; two consecutive daily alarms on the same signal, or one weekly-replay alarm, drops the cell one level (5.5).

### 6.6 The auditor is audited too

LLM judges can look good on average and still be wrong on the cases that decide things [S, UNVERIFIED], and they can disagree with themselves [S, UNVERIFIED]. So:

- Each quarter, 200 agent records per country are labelled by humans (the existing surveyor audit task, extended to field results) at about 25 to 30% seeded errors. Compute the auditor's recall and precision for "record is wrong", and Cohen's kappa against the humans. Targets: recall of errors >= 0.80, precision >= 0.70, kappa >= 0.6 (floor) [S thresholds, UNVERIFIED].
- If recall of errors falls below 0.70 or kappa below 0.6, the auditor loses the right to trigger automatic stops; every alert goes to a human, and the daily report is marked "auditor unreliable".
- Seeded wrong claims (known-bad entries built from the canary pages) are mixed into the auditor's stream; its catch rate on them is a daily number.
- Run the same input twice weekly to measure self-consistency; flag if the verdict flips on more than 5% [I].
- Review every disagreement between the auditor and a human; the human is right by definition, and the case becomes a calibration case.

### 6.7 Daily report

Generated at a fixed hour (06:00 Pakistan time first [I]) as a staff-only page at `/staff/agents/report/` (extending the existing `agents_page`) and as an email to the admin role; stored as immutable report rows and an `AuditLog` entry. Contents:

1. Traffic light per (kind, country, family): green, amber (hold), red (stopped), grey (no data).
2. Yesterday's volume: jobs, drafts staged, rejected, promoted; by prompt version.
3. Audit: batches sampled, sample sizes, accuracy with Wilson interval, human-upheld errors, top error codes, top five worst sources.
4. Cost: filing spend, auditor spend, cost per verified (agent-only and all-in), warning lines at 50 and 80% of the caps (extend `core.monitoring.ai_spend`).
5. Zero-tolerance counters: licence violations, contact leaks, canary failures, injection escapes.
6. Drift alarms and the weekly replay score.
7. Duplicates and freshness numbers.
8. Auditor health: last calibration date, kappa, recall of errors, self-consistency.
9. Decisions made in the last 24 hours (automatic stops, demotions, admin promotions, kill-switch changes) with who and why.
10. A short list of items that need a person, with links to the audit tasks.

Contacts in the report are masked. A **dead-man alarm** fires if the report has not been produced by two hours after its hour.

### 6.8 Stop button and fail-closed behaviour

Levels, narrowest first:

1. **Per source pause** (for refusals, a bad source, a licence change).
2. **Per (kind, country, family) pause or stop** via `AgentPolicy`.
3. **Per prompt version retire** (rollback).
4. **Global kill switch**: existing `AI_KILL_SWITCH` setting or `agent_kill_switch` flag (already checked before each URL and before starting a job).
5. **Big red button** on the staff agents page: one click, admin role with MFA, sets the global flag, records actor, time and reason in `AuditLog`.

Who may press: any admin; the auditor via the narrow "pause request" write (it may pause and stop, never unpause or promote); automatic rules in 5.5. Unpausing needs an admin note, a green regression panel run, and the licence and leak counters at zero. The filing agent has no write access to flags or policy, so it cannot disable its own stop (R35, plan section 17 injection row).

Fail closed: if the auditor has produced no results for 48 hours, or its report is missing, filing cells drop to L1 (no batch promotion) until it recovers. A silent auditor must never mean "no problems found".

---

## 7. What exists versus what to build

### 7.1 Status table

| Capability | Status | Where / gap |
|---|---|---|
| Licence gate for agent fetch and promotion | Exists | `intake/gate.py`, `assert_allowed` in `start_job` and `promote`. Missing: source domain list, `reviewed_on` age check for `agent_fetch` |
| Verbatim evidence rule | Exists, defective | 1.2.1 to 1.2.3 |
| Staging only, no production writes | Exists | R35 test `test_promotion_makes_a_hidden_draft_that_earns_nothing` |
| Prompt-injection test | Partial | One hostile page; need a 30-page corpus and canary pages |
| Caps, 50%/80% warnings, kill switch | Exists | Global only; no per-kind, country or family; no ramp levels |
| Second check (R07) | Partial | Same model and prompt; source separation by row only; can publish an entry |
| Freshness `recheck` job | Missing | Kind declared, no runner |
| Cost per verified | Partial | Function and staff page; not cohort-based, not per kind, no stop, rounding |
| Human audit sample | Partial | Random, published entries only, boolean verdict, no agent link |
| Verifier canaries | Exists | Entries, not pages; do not test agents |
| Bulk sample audit and bar | Exists | `intake/bulk.py`; point-estimate bar |
| Duplicate pipeline | Exists, unused by agents | `intake/dedupe.py`, `settle_duplicate` |
| Personal-data quarantine | Exists, unused by agents | `bulk.looks_personal` |
| Log scrubber | Exists | Logs only |
| Gold-standard test set and scorer | Missing | |
| Eval runner and run budget | Missing | |
| Prompt versioning, few-shot builder | Missing | |
| Promotion and demotion engine | Missing | |
| AI auditor | Missing | |
| Drift detector, daily report, dead-man alarm | Missing | `core/monitoring.py` has spend and kill-switch metrics only |
| Stop-button UI | Missing | Runbook says toggle the flag in admin |

### 7.2 Work packages

Numbering continues plan phase T1 (T1.01 to T1.03 exist). Sizes use the plan's scale: S up to 2 days, M up to 5, L up to 10, XL up to 18 [R, plan section 19]. Each acceptance test is written to be a pytest function in the repo's style.

| WP | Work | Needs | Size | Acceptance tests |
|---|---|---|---|---|
| **T1.04** | **Scoring library** `agents/scoring.py`: field equivalence rules (4.1), precision, recall, F1, record accuracy, hallucination and unfaithful-value rates, Wilson bounds, stop and promote lookup (the table in 5.5), confusion matrix for labels. Pure functions, no database | none | M | `test_phone_equivalence_by_e164_not_digits`; `test_null_page_fabrication_counts_as_false_positive`; `test_wilson_table_matches_5_5` (n=30: 24 stops, n=385: 357 promotes); `test_record_accuracy_requires_all_required_fields`; `test_unfaithful_value_is_wrong_even_when_quoted` |
| **T1.05** | **Gold store**: `GoldSet`, `GoldCase`, `EvalRun`, `EvalResult` models in a separate schema or DB alias with its own role; loader command `load_gold`; synthetic CI fixture of 20 cases; set hash recorded in `AuditLog` on sealing | T1.04 | L | `test_gold_models_unreachable_from_agent_runtime_role`; `test_set_hash_changes_when_a_case_changes`; `test_loader_rejects_case_without_two_annotators_on_test_split`; `test_absent_is_valid_expected_value` |
| **T1.06** | **Eval runner** `manage.py agent_eval --kind --set --prompt-version`: replays snapshots through a `ReplayFetcher`, scores, writes `EvalRun`; enforces one test-split run per version and three per week; test split returns aggregates only | T1.04, T1.05, T1.09 | L | `test_replay_makes_no_network_call`; `test_second_test_run_for_same_version_refused`; `test_test_split_output_has_no_per_case_rows`; `test_eval_cost_recorded_in_separate_ledger_not_filing_caps` |
| **T1.07** | **Harden the extraction rules**: phone match on a per-number basis (no joining page digits), role and proximity check, website verification, fold-based name and address matching for Urdu, Roman Urdu and Eastern Arabic digits, null-page behaviour, reject records with no supported field; replace constant confidence by a computed, calibrated value | T1.04 | L | `test_phone_spanning_two_numbers_is_not_quoted`; `test_phone_of_another_firm_on_directory_page_rejected`; `test_hallucinated_website_rejected`; `test_urdu_name_matches_after_fold`; `test_eastern_arabic_digits_phone_matches`; `test_confidence_calibration_error_below_threshold_on_dev_fixture` |
| **T1.08** | **Agent path parity**: `promote()` runs `settle_duplicate` and `looks_personal` (individual and child-facing concepts never staged), handles a suppressed contact without aborting the batch, writes a duplicate flag on the draft; store `fetched_at`, page hash and `prompt_version` on `DraftEntry`; purge rule for rejected drafts | T1.07 | M | `test_agent_draft_matching_existing_entry_is_merged_or_queued_for_review`; `test_personal_mobile_not_promoted_for_individual_concept`; `test_suppressed_contact_skips_one_draft_not_the_batch`; `test_rejected_draft_raw_purged_after_30_days` |
| **T1.09** | **`PromptVersion` and `AgentPolicy`**: versioned prompt bundles (5.1), few-shot slots, ladder levels, per-kind, per-country, per-family caps, daily record cap, pause and stop states; `start_job` and the per-URL loop enforce them; "no gold set, no job" gate; model id from the version | T1.05 | L | `test_job_refused_without_passing_eval_for_cell`; `test_daily_record_cap_stops_cell_not_others`; `test_new_version_resets_cell_to_l0`; `test_paused_cell_blocks_start_job_and_stops_running_job_at_next_url`; `test_job_and_drafts_record_prompt_version` |
| **T1.10** | **Isolation tests**: import-boundary test (agent runtime and auditor cannot import gold models; auditor package imports no filing prompt code); DB-grant tests on the Postgres role; fixtures prove prompts contain no gold text | T1.05 | S | `test_agent_modules_do_not_import_gold`; `test_auditor_role_cannot_write_entry_tables`; `test_filing_prompt_never_contains_a_test_split_case` |
| **T1.11** | **Few-shot builder**: eligibility query (human-confirmed, dev pool, allowed source), de-identification (synthetic phones, names, addresses), selection by cell, ablation script, hard-negative requirement | T1.09, T1.05 | M | `test_only_human_confirmed_entries_are_eligible`; `test_phones_in_examples_are_synthetic`; `test_example_from_test_split_rejected`; `test_prompt_without_null_page_example_fails_lint` |
| **T1.12** | **Metrics service**: daily `AgentMetricDaily` per cell; cohort-based cost per verified (agent-only and all-in, from `Task.minutes`); micro-unit cost accounting (replace `int(...)+1`); duplicate rate; freshness (`ai` expiry share); licence-compliance and contact-leak counters; source-domain check (add `Source.domains` and compare with the fetched host) | T1.08 | L | `test_cost_per_verified_is_cohort_based_and_none_below_50_verified`; `test_cost_is_not_rounded_up_to_a_whole_cent_per_call`; `test_fetch_of_host_outside_source_domains_counts_as_licence_violation`; `test_leak_scan_finds_planted_number_in_audit_payload` |
| **T1.13** | **Stratified batch sampler and field-level human audit**: `AgentBatch` (kind, country, family, source, prompt version, day, seed), `draw_stratified_sample` with the rules of 6.4; extend `AuditSample` with `draft` FK, `agent_job` FK, `field_results` JSON, stratum tags; extend `queue_audit_sample` to take draft entries and strata; human results also feed error table | T1.08 | L | `test_small_batch_audited_in_full`; `test_new_version_first_200_records_audited_fully`; `test_sample_is_reproducible_from_stored_seed`; `test_every_active_stratum_has_at_least_10_or_all_rows`; `test_audit_never_goes_to_original_verifier` |
| **T1.14** | **Batch hold**: `promote()` refuses drafts whose batch is held, stopped or unaudited at levels L2 and above | T1.09, T1.13 | S | `test_promote_refused_when_batch_failed_audit`; `test_l1_requires_human_promotion_each_draft` |
| **T1.15** | **AI auditor service** `agent_auditor/`: claim-check and blind re-extraction modes, own prompt, own key and cap and kill switch, own fetcher instance, `AuditorBatch`, `AuditorFinding`, pause-request write; claims-only input (no confidence or reason); evidence quotes stored | T1.10, T1.13 | XL | `test_auditor_never_receives_filing_confidence_or_prompt`; `test_auditor_uses_separate_key_and_cap`; `test_auditor_cannot_unpause_or_promote`; `test_auditor_refetches_page_through_licence_gate`; `test_contradicted_claim_creates_finding_with_quote`; `test_auditor_stopped_does_not_stop_filing_but_demotes_to_l1_after_48h` |
| **T1.16** | **Auditor calibration**: quarterly human-labelled set generation (seeded errors), recall, precision and kappa computation, auto-removal of stop authority below thresholds, self-consistency run, seeded-bad-claim stream | T1.13, T1.15 | M | `test_kappa_computed_on_labelled_set`; `test_auditor_loses_stop_authority_below_recall_0_70`; `test_seeded_bad_claims_reported_as_catch_rate` |
| **T1.17** | **Canary pages and tripwire**: platform-controlled host with 5 canary page types, a daily canary job, alarm on any wrong or fabricated canary value, canary phones excluded from `Contact` and public data | T1.09 | M | `test_canary_page_phone_never_staged_for_real_entry`; `test_poisoned_canary_instruction_ignored`; `test_wrong_canary_output_stops_cell` |
| **T1.18** | **Contact-leak and injection corpus**: 30 injection pages, leak scan job over tables and logs, retention purge, masked reports | T1.12 | M | `test_injection_corpus_produces_no_extra_fields_or_state_change` (parametrised over 30); `test_nightly_leak_scan_zero_hits_after_a_full_run`; `test_report_masks_phones_to_last_three_digits` |
| **T1.19** | **Governance engine** `agents/governance.py`: daily evaluation of the rules in 5.5 against metrics, human audit and auditor findings; automatic stop and hold; promotion proposals for admin approval; every decision written to `AuditLog` with inputs | T1.12, T1.13, T1.15 | L | `test_point_accuracy_below_90_at_n_100_stops_cell`; `test_24_of_30_correct_stops_cell`; `test_357_of_385_proposes_promotion_but_does_not_apply_it`; `test_cost_above_30_with_50_verified_stops_kind`; `test_single_licence_violation_stops_kind_and_source`; `test_decision_logged_with_metric_values` |
| **T1.20** | **Drift detector, daily report and dead-man alarm**: control-chart signals, weekly replay job, report page and email, extension of `core/monitoring.py`, missing-report alarm | T1.12, T1.15, T1.17 | L | `test_weekly_replay_drop_over_3_points_drops_a_level`; `test_model_id_change_without_version_raises_alarm`; `test_report_rows_are_immutable`; `test_missing_report_raises_dead_man_alarm` |
| **T1.21** | **Stop button, second-check separation, bulk alignment**: staff button with MFA and audit; per-source and per-cell pause UI; second check requires a different registered domain **and** a different prompt and model from the draft's; agent bulk pass uses the lower-bound rule; update `docs/runbooks/ai-spend-runaway.md` with the new steps | T1.09, T1.15 | M | `test_stop_button_requires_mfa_and_writes_audit_row`; `test_second_check_same_domain_refused`; `test_second_check_same_model_and_prompt_as_draft_refused_for_ai_level`; `test_agent_batch_with_point_90_but_lower_bound_below_90_not_promoted` |
| **T1.22** | **Gold set construction project (human work, runs in parallel)**: annotation guide, recruit local annotators (Urdu readers first), build the Pakistan pack to the sizes in 3.3, adjudication, world-truth calls on the 30% subset, kappa report; counsel note on snapshot storage and provider terms | T1.05 | L (people time, about USD 190 to 2,500 [I]) | Pack sealed with hash in `AuditLog`; kappa >= 0.6 on every batch; every trap type has at least 15 test cases; 100 test cases per launch family cell; counsel note filed |

### 7.3 Build order

1. **Before any real hosted-model run**: T1.04, T1.07, T1.08 (these fix defects that would corrupt any measurement), T1.05, T1.22 (start labelling immediately; it has the longest lead time).
2. **Before ramp beyond a handful of drafts**: T1.09, T1.10, T1.06, T1.11, T1.12.
3. **Before L2**: T1.13, T1.14, T1.15, T1.16, T1.17, T1.18, T1.19.
4. **Before L3 and before a second country**: T1.20, T1.21, a second country pack.

Suggested first loop on the real thing (this is the plan's own experiment 2 and 3, run through the machinery): L0 shadow for one family in one place; 200 records; AI auditor and a 100-record human audit; read accuracy, cost and the error table; fix; repeat before L1.

### 7.4 Open decisions for the founder

1. Which cost definition triggers the USD 0.30 stop: agent-only (plan 7.6 text) or all-in (report experiment 3).
2. Whether the `ai` second check may publish an entry at all before an independent auditor exists (current behaviour, test line in `test_agents.py`). My recommendation: no `ai`-driven publication until T1.15 and T1.16 are done.
3. Which families are agent-eligible in the first country (individual and child-facing excluded).
4. Auditor vendor: a second model family (cost, data-sharing terms) or a different tier of the same family (cheaper, weaker independence).
5. Snapshot storage: full page text or quotes plus context, after counsel advice.
6. Annotator sourcing and budget for T1.22.

### 7.5 Unverified items to close

- Every external figure in section 2 (judge agreement, bias sizes, kappa thresholds, "50 per category", drift cadence): from search summaries only.
- Provider data-retention and training terms for the keys used on gold snapshots.
- UAE address and phone conventions in 3.4.
- That the plan's retention schedule (section 17) allows the proposed 30-day purge of staged drafts.
- Realistic labelling speed for Urdu-script pages (the 1 to 3 minute figure comes from the earlier report and was not measured for field-level gold labels).
