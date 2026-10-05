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
