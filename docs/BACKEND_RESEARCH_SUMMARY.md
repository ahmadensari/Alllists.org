# Backend research: summary and decisions (2026-10-06)

Four research notes, all in `research_notes/Backend research/`. Prices, licences and platform facts come from search snippets and are UNVERIFIED unless a note says otherwise. Figures marked "arithmetic" are derived from the code, not measured on a live database.

## 1. Entry fields per list type (`01_*`)
- 29 families cover all 235 list types. One common core of 27 fields plus 555 type-specific fields (586 rows in `01_entry_fields.csv`).
- Required to publish: 72 family fields. Filterable: 329. Shown free: 404; subscribers: 131.
- Sensitivity tags: 41 personal-data, 21 child-related, 10 health-price, 9 commercial.
- Prices are the stalest and riskiest fields: every money value carries currency and date; health prices wait for the health rules (Q-S1).
- Owner questions: 29 families or merge to 25; free asking prices on property and vehicle listings; gender fields; public emergency helplines; splitting combined list types.

## 2. Data sources per country (`02_*`)
- 186 sources rated: 34 green, 132 amber, 20 red (16 exclusions). Pakistan is all amber (14 sources).
- Strongest: Overture and Foursquare as baseline; Mexico DENUE, France SIRENE and FINESS, UK Companies House, India data.gov.in, Brazil CNPJ and CNES, Kenya KMPDC.
- No open licence exists for bulk lists of named doctors, lawyers, engineers; no register covers plumbers, electricians or tutors, so they need owner or society consent.
- Share-alike sources (OpenStreetMap, OpenCorporates, Healthsites) conflict with the no-download and paid-download rules.
- Gap: several greens rest on background knowledge; green sources should also need licence text and a review date.

## 3. Hosting and cost (`03_*`)
- Database size (arithmetic): 0.16 GB at 10k entries, 18.7 GB at 1M, 0.84 TB at 100M (low case 0.1 GB, 12.9 GB, 257 GB).
- `PlaceList` costs 144 bytes a row. 235 types times 1.5M places is 352M rows (51 GB). An unscoped run on the global tree is 45.6M rows (6.6 GB). Use `--country` and `--levels`.
- Monthly infrastructure (UNVERIFIED): 10k entries USD 20-200 by provider; 1M entries USD 240-1,200; 100M entries USD 5,000-38,000.
- At 100M entries a logical restore takes about 3.3 hours against a 1-hour goal; physical backups and a standby are needed.
- AI filling at USD 0.04-0.20 per record costs USD 40k-200k per million records and dwarfs hosting.
- Pakistan payments: Stripe unavailable; Easypaisa about 1%, JazzCash 1.25-2.32%, Raast QR 0%, Safepay 2.9% + PKR 30.
- Repo risks: one global advisory lock and hash chain for every audited write (about 3.5 days of lock time at 100M creates); `PlaceList` has no country code for partitioning; TECHNICAL_PLAN text still says lists are computed.
- Recommended path: one Mumbai, Delhi or Dubai VM at about USD 25-45 a month, Cloudflare Free, off-provider backup; managed Postgres or standby at about 50k entries.

## 4. Agent training and AI auditor (`04_*`)
- Existing pipeline has good guards but no accuracy measurement and no AI auditor.
- Defects that would corrupt measurement: phone quote check can match digits across numbers or another firm; website never checked; promotion skips the duplicate and personal-contact checks; an `ai` second check can publish with the same model and prompt; "different source" means a different source row, not a different site; audit samples cover published entries only; cost rounds up to one cent per call.
- Gold set: about 1,240 labelled items for the first country (USD 190-2,500 to label); no gold set, no job.
- Training without fine-tuning: immutable prompt versions (dev, sealed test, shadow, canary, active); few-shot examples only from human-confirmed entries; caps per kind, country and family.
- Stop below 90% point accuracy with n at least 100; promote only with a lower confidence bound of at least 0.90 (357 of 385); stop above USD 0.30 per verified record; stop on any licence or contact leak. Demotion automatic, promotion human-approved.
- AI auditor: separate package, different prompt (preferably a different model family), own key and spend cap, read-only database access, sees claims and URL only, can lower trust never raise it, daily report, five-level stop button, fails closed after 48 hours silent. 19 work packages (T1.04-T1.22).

## Defaults adopted (founder may change)
1. Keep 29 families for now. 2. Asking prices on classified listings free; service prices locked. 3. Keep clientele and female-staff-only facts; self-declared gender optional; counsel before tutors and domestic workers. 4. Public helplines only for government and emergency bodies from an official source. 5. Leave out share-alike sources. 6. Require licence text and review date for green sources. 7. `ai` checks may not publish until the AI auditor exists. 8. Stricter pass rule for agent output than 90% point estimate.

## Next work (after founder's go-ahead on the sequence)
Fix the measurement defects (T1.04, T1.07, T1.08), build the gold-set loader and scorer, then the AI auditor package; correct TECHNICAL_PLAN text on stored lists; add a country code to `PlaceList`.
