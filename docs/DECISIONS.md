# AllLists.org: Decision Log

This is the short list of what the owner has decided or agreed, so that coding does not reopen settled questions.
The long register with sources, evidence and open questions is `docs/REQUIREMENTS.md`. IDs in brackets point to it.
The research reports are in `reports/`. Almost all figures in them come from search summaries and are graded there.

**Rule:** nothing in "Decided" or "Agreed" is debated again unless the owner says so. Items in "Open" need an owner decision before the part they affect is built. No code is written until the owner asks.

Last updated: 2026-10-05 (service-provider round).

## 1. Vision and model

| Decision | Ref |
|---|---|
| A marketplace where anyone can create and sell lists of anything; the platform keeps a share and contributors share the rest when a list is sold | A1, A2 |
| The platform sets the price of merged (higher-level) lists | E2 |
| The idea is workable enough to refine fully first. Coding starts only after refinement, top to bottom (global structure first, then country, region, city, area) | S1, S2 |
| Build in phases, never everything at once | S2 |
| Launch globally with no spending, growing by a study-then-snowball approach; each stage pays for the next (working view; costs that cannot be zero are open) | C28 |
| All countries are in the structure; go-to-market starts where data is poor and rules are lighter (Pakistan, the Middle East and other countries); the product becomes high-end as it reaches high-end markets | S3, S4, D14 |
| Top research priority: which list types pay at Justdial, IndiaMART and other platforms; focus on those in all countries | S5 |

## 2. Structure of lists

| Decision | Ref |
|---|---|
| Global from day one, top-down: global, region, country, state or province, division or district, city, area (road, street, neighbourhood, housing society) | C10 |
| Creating a list type in one place opens it, empty, in every place (petrol pumps in Islamabad also exists in New York) | C11 |
| A list is a category at a place; higher levels roll up what is below | C12 |
| Contributors add entries to any list and may add areas (Adyala Road, Abraham Street) | C13 |
| People may own a segment of a list and correct it (details open) | C20 |
| Each list type has a natural scale: hyper-local (plumbers, eye doctors and eye hospitals in a society), national (contractors) or global (data scientists); the place tree applies to all | C25 |

## 3. What an entry holds

| Decision | Ref |
|---|---|
| Fields: name, address, owner, phone, WhatsApp number, social media page, reviewer rankings, size, available goods, services, and others as a list needs | C17 |
| Equipment and priced services can be part of an entry (MRI machines in Islamabad with services and prices) | C21 |
| Skill-based lists of individuals at neighbourhood level are in (plumbers in Bankers Society, mobile phone repair services, Quran tutors in an area, and many more) | C22, C23 |
| Verification levels on every entry: owner-verified, surveyor-verified, AI-checked, not verified yet, with who, how, when and evidence stored | D19, D20 |
| Topic lists that are not about places (apps, websites, books, tools) are in; they use a topic tree and are monetised by sponsorship, affiliate links and ads, not by list sales (working view) | C27 |
| Browsing path: world page, then country, then each next level, until the list is reached; addresses follow the place tree | C38 |
| Automatic location: find the user's place, show lists there first, let them widen or search country-wide, then apply the payment policy; addresses stay the same for everyone | C39 |
| Text and numbers only for now: no pictures or videos | C29 |
| Modern, dynamic page of 2026: CSS-first motion and server-rendered pages with small interaction; libraries only where CSS cannot do the job; motion respects reduced-motion settings (working view) | C36 |
| Base structure: a few templates, shared parts and registries; one change reaches every page that uses it; no hand-made pages | C34 |
| Every list type gets a complete entry template: a common core plus type-specific fields, based on what established platforms and registers hold (research under way) | C26 |
| Keep adding data first (draft-first); reliability comes later through ownership and manual verification | D18 |

## 4. Where data comes from

| Decision | Ref |
|---|---|
| People who hold lists import them; businesses add themselves later and claim their entry | D1, B4 |
| AI agents draft entries from many sources; owners and contributors verify | D14 |
| Open baseline data is licensed in as the starting layer; unverified agent pages are not published at scale | D16 |
| Service providers are identified from established sources first (professional and trade registers, licensing bodies, chambers, open data, talent platforms with open licences), then lists are built from them | D21 |
| Every record keeps its source, licence, date and consent status | D17 |

## 5. Contributors and ownership

| Decision | Ref |
|---|---|
| Volunteers (students and others) contribute; no one is paid up front; contributors get their share only when a list is sold | CP1 |
| Non-cash rewards keep volunteers: levels, certificates useful for a CV, visible credit, free or discounted access in proportion to verified contributions | CP9 |
| Contributor share steps down 50%, 40%, 30% (how it steps is open, see section 9) | F2 |

## 6. Access, pricing and revenue

| Decision | Ref |
|---|---|
| No download except at a heavy price (about USD 1,000); buyers instead choose an outreach method and the platform delivers it, contacts stay hidden | E13 |
| Each list page shows the first few entries plus statistics about the whole list | E14 |
| Small segments free with names only; details and larger roll-ups (city and above) paid (the owner's wording was ambiguous; working reading) | CP3, CP4 |
| Mitigations against rebuilding paid lists from free ones: names-only on free views, accounts, limits, anti-bot checks, terms, charge more as lists get bigger | P15 |
| Free users see advertisements; subscribers see none | CP5 |
| Subscribers pay a lower recurring fee for live access | E7 |
| Paid companies get a full company page on the list: the entry template with more sections the company provides, labelled as company-provided; checks and rank stay separate and cannot be bought | C35 |
| Businesses pay to rank higher; later they pay to be on the list (hidden or merely ranked lower is not decided) | E15, CP2 |
| Do not charge to remove personal data; charge for visibility, ranking, badge, extra fields and leads | P17 |
| Governments and institutions may buy lists or statistics | E16 |
| Research how established platforms earn, to calibrate our revenue streams (under way) | E18 |
| The platform is positioned as a cheaper, more targeted alternative to Google and Meta advertising (to be tested) | E17 |
| Every access or pricing rule is judged on two tests: better usage and returning clients, and revenue | CP8 |

## 7. Later vision (staged, not version 1)

Demand intelligence, product requests from shops, product testing, direct sell offers and direct factory-to-shop shipping, built in stages with partners for payments and logistics (O2, V1 to V8).

## 8. Seed list types named by the owner (for seeding and testing)

Petrol pumps; schools (on a road, in a city); beauty parlours and salons; bakeries; mobile stores; mobile phone repair services; spare parts shops; furniture stores; medical stores and pharmacies; doctors, nurses, lawyers; bookshops; hardware shops; MRI machines with services and prices; plumbers and other skill-based lists; Quran tutors in an area; surgical instrument makers and football makers in Sialkot, fan and sanitaryware makers in Gujranwala, furniture makers in Faisalabad, hotels in Murree; eye doctors and eye hospitals in a society; contractors (national); data scientists (global); factories and suppliers; and personal lists (books read, belongings, classmates) that stay private by default. Research in `reports/Which lists pay.md` ranks which of these are likely to pay.

## 9. Open: owner decisions still needed (with my suggested defaults)

| Open item | Suggested default | Ref |
|---|---|---|
| Domain: alllists.org or alllists.com | Confirm which you own | |
| First country, city and trade | Pakistan, one city, one trade; sell to buyers in Pakistan and the Gulf. Candidate trade after the cluster discussion: surgical instrument makers in Sialkot (export buyers abroad), tested as in Q-S7 | Q-N6, Q-P1 |
| How the 50, 40, 30 steps work: by date, by merge level, or both; locked per entry? | Date phases, locked on each entry | F3, F4 |
| What a "not verified yet" entry may do | Visible only to owners and moderators; public with badge from "AI-checked" up | Q-P6 |
| Requirements and duration of each verification level; who pays surveyors | Settle in the 1,000-record pilot | Q-P7 |
| Download price basis | Scaled by size and freshness, USD 1,000 minimum | Q-N1 |
| Paid ranking: how sold, which level, who earns | City level first | Q-N2, Q-O4 |
| Which ads free users see; whether ad revenue is shared | Supplier ads in the relevant trade and place; sharing decided later | Q-R3 |
| Hidden or merely lower-ranked for unpaid businesses | All listed; decide after traffic exists | Q-R1 |
| Government policy | Aggregate statistics only at first | Q-N3 |
| First outreach channels | Opt-in, platform-sent; WhatsApp first, after counsel | Q-N5 |
| Which agent sources are used and which are excluded | Chambers, associations, owner submissions, registries and open data in; scraping Google Maps, Facebook and Baidu Maps out until counsel advises | Q-P4 |
| How segment ownership works (exclusive or shared, how claimed and lost) | Revocable stewardship with a review queue; no fee, no recruitment commission | Q-P2 |
| Who may write reviewer rankings and how fake reviews are stopped | Verified users only, one per user, owner reply, separate from paid ranking | Q-P3 |
| Who earns when a new list type or area is created | Platform prices; creator earns a small early-sales bonus | Q-O1 |
| Code licence versus data licence | Code open; list data under terms | A3 |
| Which registers may be used and how (terms, bulk or partnered access, personal data) | Email each body for written terms; start with facility and school registers, not individuals | Q-S3 |

### Added by the service-provider round (details in `reports/Service provider sources.md`, section 6)

| Open item | Suggested default | Ref |
|---|---|---|
| Pilot city and first source pack | One city: eye hospitals and eye doctors first, then schools, then contractors | Q-P1 |
| Named individuals (doctors, lawyers, tradespeople, tutors) | Only with the person's consent; contact through the platform; area only, no home address | Q-S2 |
| Housing society partnership | One-society pilot; opt-in link; no fee, no recruitment commission | Q-P2 |
| Child-facing tutors and Quran tutors | Not public until safeguarding and relay-only contact are designed; schools and centres first | Q-S2 |
| Talent list (data scientists) timing | Design now; launch after a pilot of about 50 consented people and counsel review | |
| API and custom extracts | No API at launch; custom research for institutions case by case | |
| Per-listing fees for individuals in some types | None at launch; revisit with traffic | |
| Health-sector rules for prices and ads | Adopt the report's health rules before collecting any price | Q-S1 |
| Counsel | Book before any messaging test, list of individuals, health or child data, or talent list | |
| Which proposed list types from the platform catalogue join the seed list | Take the report's top ranked group (urgent home and trade firms, health facilities and equipment, Sialkot-type clusters, importers and buy leads); delay children's services, health data, named individuals | Q-S8 |
| Sign off the list and entry component specification (core fields frozen for version 1) | Approve `docs/LIST_AND_ENTRY_COMPONENTS.md` after reading section 10 | Q-S12 |
| Website and social page links: public or locked | Locked on the free view | Q-S13 |
| Choose one first trade in writing | Sialkot surgical instruments, as a verified-supplier register, tested for eight weeks first | Q-S16 |
| How the contributor share is defined | Net revenue, with a time cap on each entry's phase rate (suggested 36 months) | Q-S15 |
| The name and domain | Keep AllLists; check alllists.org ownership; price alllists.com; protect .app, .io and .pk; fallback ListAtlas | Q-S19 |

## Build log

- 2026-10-05: First software build. Django 5.2 + SQLite (PostgreSQL via env) in `backend/`, replacing the Flask draft. Implements place tree, list views, entries with checks, free/subscriber visibility, company page, enquiry relay, report/claim, share registry, EN/UR, edge-header location, contributor phase rates locked per entry and sale distribution. Not yet built: payments, email relay delivery, subscriptions, moderation UI, search engine, ads. Stack choice (Q-S9/Q-S18) used the recorded default and can still be changed.
- 2026-10-05: Technical plan written (`docs/TECHNICAL_PLAN.md`): 40 enforceable rules (R01 to R40), modular-monolith architecture, full schema, 94 work packages in phases P0 to P6 plus an agent track, owner-decision register with assumed defaults (including new questions Q-T1 to Q-T11), and a traceability matrix over every requirement ID. Coding follows this plan; the first Django build is kept only where section 24 says so.
- 2026-10-05: Coding started per `docs/TECHNICAL_PLAN.md`. Done: P0.02 (legacy files removed), P0.03 (compose), P0.04 (CI on PostgreSQL, Python 3.11 to 3.13, blocking flake8, migrate-reverse check), P0.05 (bandit, pip-audit in CI), P0.07 (settings package, module skeletons), P0.09 (session hook), P0.10 partly (pull-request template, CONTRIBUTING; **LICENSE not added**, awaiting the owner's licence decision). P1: `core` (ULID, audit hash chain, change log, flags, country switches, field encryption, `fold()`), `places`, `taxonomy` (concepts, synonyms, add-on registry, reserved slugs), `entries` (schema, verification state machine with guards, publish bar, claims, consent, credit eligibility, expiry and grace), `intake` source gate. Append-only enforced by PostgreSQL triggers. 80 tests. Not done: P0.01 (owner must rotate secrets), P0.06 (hosting), import UI, duplicate pipeline, roll-ups, staff console, loaders.
- 2026-10-05 (second coding step): added `analytics` roll-up cells (P1.05), merge service with first-adder credit (P1.14), paste and CSV import with header guessing in English, Urdu and Roman Urdu (P1.16), duplicate pipeline v1 with block, score and decide (P1.18), admin screens for pilot data entry, and `seed_pilot` (Sialkot structure, surgical-instrument list type, starter sources, Pakistan country switch with everything off but browsing). 99 tests pass on PostgreSQL. Dedupe thresholds (auto-merge 0.90, review 0.60) are first guesses to be calibrated on the 500 labelled pairs in the pilot.
- 2026-10-05 (third coding step, public pages): `lists` demo app replaced by `catalog` (addresses `/pk/punjab/sialkot/surgical-instrument-makers/`, entry pages `/e/{uid}/{slug}/`, Urdu under `/ur/`), `access.policy` (one visibility table), private fragments under `/_f/`, SEO rules (noindex unless switch on and 10 verified; filters never indexed; sharded sitemaps; robots.txt allows thin pages), English and Urdu strings, share registry, place and list pages in light and dark. Decisions and deviations taken while building: (1) the shared page shell shows names-only fields for every viewer, richer free details (type, specialities) and all subscriber details arrive in a private fragment, so one address gives the same bytes to everyone (R05); (2) the scope rule (names only wider than your own place) applies to list rows; entry pages are not scope-limited, so one message button is free everywhere (policy table changed accordingly); (3) the dashboard prefix is `/account/` because two-letter system addresses collide with country codes (`/me/` is Montenegro); system slugs are refused as place slugs; (4) no gettext tools exist in this environment, so strings live in Python catalogues with plural forms (moving to .po later is mechanical); (5) pages show 25 rows with page links; the "five rows then Show more" free-limit comes with quotas (P3.03); (6) theme and list or card view are kept in the browser (localStorage), not cookies the server reads; (7) query count per list page is constant in the number of rows (23 now).
- 2026-10-05 (fourth coding step; the founder said never to ask and to keep working until the product is delivered, so defaults in `docs/TECHNICAL_PLAN.md` section 21 are now the decisions in force until changed): accounts (sign-up, email confirmation, Argon2id, login throttling with lockout, TOTP two-step with recovery codes, staff routes need role plus verified second step, account deletion, password reset), roles and capabilities table, scoped subscriptions and entitlements (manual grant), forms (add entry with rights declaration, suggest area, claim by one-time code or documents, something wrong, message, one enquiry to many for subscribers), enquiry relay with contact-extraction scan, opt-in and one-tap opt-out with a global suppression list that blocks re-import, reports with rate limits and honeypot, takedown and erasure with tombstones, suggested edits, surveyor task queue with canary accuracy and suspension, contributor page, and the staff console (duplicates, areas, claims, reports, suggestions, erasure, imports, sources, tasks, audit with chain check, country switches, outbox). Built-in exceptions to record: (1) the assigned surveyor can reveal an entry's contact numbers for that one task, each reveal audited, because verification needs a call (rule R02 still holds for visitors, buyers and subscribers); (2) a claimant who proves control of a stored contact with a one-time code becomes owner at once and opts in to enquiries, recorded against the claimant with the method, with the documents route going to a moderator; (3) a claim code is not consumed unless the opt-in box is ticked.
- 2026-10-05 (fifth coding step): free quotas (counted on the private details fragment, so the shared page stays cacheable; 40 rows a day anonymous, 100 for accounts; subscribers exempt; alarm at 500 and hard stop at 2000 fragment requests a day per address), security headers with a strict content policy, log scrubber, route access map with tests for every route, search (list types by synonym and typo, places in both scripts, entry names only inside a scope, zero-result flow), events catalogue, company page (owner edits sections and certificates, moderator approves each save, public with "Provided by the company" and "Company says" until a check is recorded, hidden when the plan lapses, not for individuals or child services), append-only double-entry ledger with a database balance trigger, rate phases locked on first publish, contributor allocation (equal slice per verified eligible entry, locked phase rate, 36-month cap to the lowest rate, largest-remainder rounding, property tests), holds, exact refunds, payouts with the two-person rule, orders and manual payment recording, signed idempotent payment webhook, tax lines from configuration, and invoices. Self-listed entries sit outside the allocation denominator so they do not dilute others.
- 2026-10-05 (sixth coding step: agent track, scheduled jobs, audit and canaries, outreach campaigns): the agent track (fetcher with address-safety guard, robots check and stop-on-refusal; model interface with a fake model for tests; every extracted value must carry verbatim evidence from the page; daily and monthly caps and a kill switch, all defaulting to zero so nothing runs until the owner sets them; drafts staged and never published directly; a second check from a different source), scheduled jobs with a run log, audit samples of 385 published entries re-checked by a different person, planted fake entries to score surveyors, and outreach campaigns (verified supplier, approved templates only, country switch, daily caps, quiet hours, automatic pause above 2 percent opt-outs or 10 percent failures, signed delivery callbacks, cost per reply report, funded through a billing order). A share of each sale goes to a campaign pool only when `OUTREACH_SHARE_PERCENT` is set; it is unset by default, so no campaign can be created until the owner decides the share (assumed default in plan section 21 stays "not set"). Messages go through a sandbox provider until a real provider is chosen.
- 2026-10-05 (seventh coding step, phase P5 money and promotion): (1) sponsored places: two slots per list (setting `PLACEMENT_SLOTS`), sold per place and list type, only for published open entries that really sit on that list; the slot is labelled and links to a "How this list is ordered" page; the sponsored entry still appears in its normal alphabetical position and shows its true check label (an expired check shows "Not verified yet"); the shared page address changes when a placement starts or ends, so caches stay correct; revenue is platform money outside the contributor pool. (2) Text ads: owner submits, staff approve after payment, shown only in the private details part for free viewers, text only with the same contact-leak scan as enquiries, clicks counted by a redirect that points to the entry page. (3) Statistics reports are aggregates only with counts under 5 hidden; extracts are staff-only, made for a paid extract order or a stated purpose, never contain contact values, people, do-not-share entries or child-facing lists, and carry planted made-up businesses unique to each extract so a leak can be traced; there is no user download route and a test enforces that. (4) Subscription sales now feed the contributor pool: net revenue is split across verified entries in the subscriber's scope, weight 1.0 plus 0.25 for entries re-verified in the last 90 days (`FRESHNESS_BONUS`, `FRESHNESS_DAYS`), then each entry earns its locked phase rate. (5) Payouts need approved payout details (encrypted legal name, account and tax number; changing them sends them back to review; nobody approves their own); payout batches are created by one person, approved by another, and marked paid only with a bank reference for every payout; a daily reconciliation recomputes clearing, fees, tax, holding, payable and payout balances from the records behind them and reports any difference without fixing it. (6) Invoices are numbered per year without gaps, keep the tax rate and the buyer's details as at the order, and a refund issues a credit note instead of editing the invoice; revenue is reported per currency, with an indicative USD line only when rates are configured.
- 2026-10-05 (eighth coding step: loaders, contributor rewards, data-subject rights, operations, adapters): (1) open-data loaders read local files only (GeoNames dumps, Overture divisions and places as JSON lines, Foursquare places, own CSV); a record whose category has no list type is skipped, never guessed; everything loads as a draft with no credit; reruns skip loaded records; the source gate applies. (2) Onboarding is five questions, four right and the rights box ticked; surveyor screens send the unprepared to it. Levels give a certificate each (with a public check page) and, from level 2, 30 days of access to the contributor's own city; "Added by" credit shows only when the contributor opted in, the entry is checked and it is not a person; share links carry the contributor's `ref` code and visits are counted once a day per visitor through the private part of the page, so cached pages stay identical. (3) Consent register and withdrawal, staff-run subject access (never shows stored values) and an account holder's own data file. (4) Service health page and hourly alert email (each distinct alert at most once a day); backups and restore drills are recorded and go red when stale; deploy, rollback, backup and restore scripts, unit files, proxy files and twelve runbooks written. (5) Database roles: the application role cannot update, delete or truncate the append-only tables, and the read-only role cannot read sensitive tables. (6) Search sits behind a backend interface with two implementations that pass the same tests. (7) Two-step sign-in can be switched on by anyone and is forced for staff roles; Google and ORCID sign-in use the code flow with PKCE and never take over an account by an unconfirmed email; a read-replica router and a load-test script are in place for stage S2. Not exercised against real services yet: payment provider, messaging provider, real servers, real Google and ORCID credentials.
- 2026-10-05 (security review of the branch, fixes): (1) a person who added an entry cannot prove ownership of it with a code sent to a contact they supplied, and an owner check by the creator never makes their own credit payable (documents claims still work, reviewed by a moderator, and an independent surveyor check or someone else's claim does make the credit payable); (2) the list type decides whether an entry is a person, the add form no longer trusts a form value, and the service never lets a people-list entry be stored as a business; (3) a subscription now needs a place (no world-wide access at the city price), a region costs 10 times and a country 20 times the city price, and a subscription with no list type costs 3 times (`SUBSCRIPTION_SCOPE_MULTIPLIER`, `SUBSCRIPTION_ANY_TYPE_MULTIPLIER`); list access needs both a place and a list type; (4) a payout records a keyed fingerprint of the approved payout details and cannot be approved or paid if they changed or lost approval; staff can cancel a payout, which frees the reserved amount; (5) an enquiry's reply address must be one clean email address. Findings left as they are: free-text relay is limited by the daily cap and the opt-in rule, and the page fetcher is not reachable from any request and must be hardened (redirect and DNS checks) before it is exposed.
- 2026-10-05 (rigorous testing round; the founder asked for rigorous tests): coverage 94 percent before this round; added a site-wide matrix (every route, seven kinds of visitor, both methods: no server errors, access levels enforced, no contact value or ciphertext in any page, shared pages identical for everyone, private pages never cacheable), a staff console matrix (every queue and action, every role), fuzz and property tests (folding, contact filter, import parser, one-time codes against the published RFC vectors, random URLs), concurrency tests with real threads, command and production-settings tests, and a mutation check script that breaks one rule at a time and lists the changes no test noticed. Real defects these found and that are now fixed: (1) a pasted CSV with a bare carriage return, or only blank control characters, crashed the import with a server error; (2) a non-ASCII one-time code crashed the two-step sign-in with a server error; (3) any request with a NUL character in the address, query or a form value crashed pages (now answered 400 before it reaches the code); (4) two payments for one order with different references both fulfilled it (now the order row is locked, so one wins and the other is refused); (5) the same payment reference arriving twice at once broke the transaction; (6) a replayed sale arriving at the same moment hit a database error (now serialised by an advisory lock); (7) four payout requests at once could pay out four times the payable balance (now serialised per person); (8) account, staff and form pages carried no cache header (now private and no-store by default, and only shared pages, static files and sitemaps may be stored); (9) loading Overture divisions after GeoNames made a twin country (now linked); (10) production did not insist that the active encryption key is one of the keys; (11) the leak tracer could name the wrong extract because trace addresses are not unique (now it matches only the unique name or website, and names are never reused); (12) the page fetcher was hardened: one lookup whose answer is pinned for the connection (DNS rebinding), robots.txt fetched under the same rules without redirects, only ports 80 and 443, and IPv6 forms that carry an IPv4 address refused. Production now redirects to HTTPS (except the health check) and sends HSTS for 30 days, to be raised once HTTPS is proven.
- 2026-10-05 (real-server run, still the testing round): ran the production settings under gunicorn, a browser (light and dark, English and Urdu, phone width) and a real HTTP sign-up journey. Found and fixed: (1) the login name of a checker was shown publicly beside every check ("by <login name>"); a name is now shown only when the person chose to be credited and under the public name they chose, so checks carry the checker's id, not a name; (2) the development encryption key was new on every start, so data seeded in one run could not be read in the next (now derived from the development secret; production is unchanged and refuses to start without real keys); (3) with hashed static file names a forgotten `collectstatic` would have broken every page (now falls back to the plain file name; `deploy.sh` always runs it). Verified in the browser: details load into the shared page for a visitor who chose their own place, Urdu is right to left, no horizontal scroll at 390 px, no console or content-policy errors, no contact value anywhere.

## Build log: one-command list generation (2026-10-06)

Founder decisions (answered in the session): lists are **stored rows**, one per list type per place (E27, supersedes the "virtual views" working view in C29 for storage; entries are still stored once); place tree from **GeoNames + Overture**; domain **alllists.com** (replaces the alllists.org default in section 9); list set to load is **all 113 platform types + the 124 inventory + the owner's seed list**, merged and de-duplicated.
Built: `taxonomy.PlaceList` (unique per place and type) and `manage.py generate_lists [--levels ...] [--country XX] [--dry-run]`, one SQL insert, safe to repeat. Not yet done: loading the merged ~200 list types (only the 32 seeded types exist), loading the full GeoNames/Overture tree, switching domain settings to alllists.com. Cost warning: ~200 types times millions of places is hundreds of millions of rows; use `--levels` to start with world to city.

## Rule: English only for now (2026-10-06, founder instruction)

For the time being all work is in English only: pages, labels, messages, documents, list names, and new data. No new Urdu or other translations are written or reviewed; existing Urdu labels and the right-to-left support stay in the code, unused and untouched, until the founder lifts this rule. Default language stays `en` (`LANGUAGE_CODE`). Supersedes earlier notes that call for an Urdu review before launch.

## Build log: extended list types and domain (2026-10-06)

`manage.py seed_taxonomy --extended` loads the merged research set (inventory plus platform catalogue, 235 unique types in `backend/taxonomy/data/list_types.csv`) on top of the 32 seeded types; safe to repeat; individuals and child-facing types are created gated (contacts hidden). Default templates are not yet assigned to the new types. The domain in code, deploy files and the user agent is now alllists.com. Run `seed_taxonomy --extended`, load places, then `generate_lists --levels world,country,admin1,city` to create the stored lists.

## Build log: visitor address trust (2026-10-06)

The visitor address now comes from Cloudflare's header only when `BEHIND_CLOUDFLARE=1`; otherwise the socket address is used, so quota and throttle keys cannot be forged by sending the header (security requirement AS-01). Set the variable on the real server once Cloudflare fronts the site.

## Build log: bulk upload pipeline (2026-10-06)

`intake/bulk.py` adds staged bulk upload on top of the existing import (requirements BU-*): `stage` parses and scores rows in chunks of 2,000 with a checkpoint and creates no entries; rows that look like named people are held (personal email, short name with no business word, or any row for an individual or child-facing list type) and never published by this path; `draw_sample` picks a repeatable sample (385 for large batches, every row up to 200); `record_audit` needs every sampled row judged and passes only at 90% accuracy or better; `publish` creates drafts in chunks, resumable, only after a passed audit; `rollback` withdraws unverified drafts. Limit without counsel: 1,000,000 rows per batch (default, owner to confirm). Not yet built: upload screen, background worker for 10M-row batches, uploader fraud checks, per-batch lawful-basis record.
