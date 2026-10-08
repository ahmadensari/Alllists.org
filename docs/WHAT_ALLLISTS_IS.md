# What AllLists.com is for

Written 2026-10-06 from the decision log, technical plan, research reports and the code as built. English only (standing rule). "Built" means in the repository and covered by tests; it does not mean live, filled with real data, hosted or connected to payments.

## 1. The idea in one paragraph

AllLists.com is a global marketplace of lists. For any kind of thing (hotels, schools, hospitals, factories, plumbers, pharmacies, petrol pumps, software tools) at any place, from the whole world down to a business district or a housing society, a visitor finds one trustworthy list. People who hold lists can load them and sell access to them. The platform takes a share of each sale, and contributors share the rest only when a list sells. Nobody is paid up front.

## 2. The problem it solves

| Problem today | What AllLists does |
|---|---|
| Local data is scattered across Google Maps, Justdial, chambers, registers, spreadsheets and WhatsApp groups | One place tree and one list per type per place, so there is one address for "hotels in Murree" |
| Existing directories mix paid and honest ranking, and show stale entries without saying so | Every entry shows who checked it, how, and when; paid rank can never change a check label |
| Data owners cannot earn from a list they built | Contributors earn when a list sells, at phase rates of 50%, 40% and 30%, locked per entry |
| Buyers get contact files that are old and unverified | Contacts are never shown; messages are relayed; every record has source, licence, date and consent status |
| Poorly served markets (Pakistan, the Gulf, parts of Africa and Asia) have thin data | Launch starts where data is poor and rules are lighter, then moves up-market |

## 3. How lists are structured

- **Place tree:** world, region, country, state or province, division or district, city, area (road, street, neighbourhood, housing society). Contributors may add areas.
- **List type:** a category such as hotels or plumbers. Creating a list type in one place opens it, empty, in every place. The founder chose to store a real list row for every list type at every place; the `generate_lists` command does this in one step and is built and tested.
- **Lists roll up:** "Hotels in California" includes the hotels in its cities; "Hotels, USA" includes California; "Hotels, global" includes all countries.
- **Natural scale:** each type has a level where it is most useful and sold. Plumbers in a society are hyper-local; contractors are national; data scientists are global.
- **Entries are stored once.** An entry appears on every list it belongs to. Storage grows with entries, not with lists.
- **Topic lists** (apps, websites, books, AI tools, public figures) use a topic tree and are monetised by sponsorship and affiliate links, not list sales.
- **Personal lists** (books read, belongings, classmates) stay private by default.
- **Text and numbers only** for now: no pictures or videos.

## 4. What an entry holds

A common core (name, address, owner, size, goods, services, social page, reviewer rankings) plus fields specific to the list type, such as a school's board and fees, a hospital's departments, an MRI centre's equipment and priced services, a manufacturer's capacity and certificates. 32 list types and 11 field templates are loaded in the code today; research has identified about 200 more, listed in `docs/LISTS_IDENTIFIED.md`. Phone, WhatsApp and email are stored encrypted and never displayed.

## 5. Trust

Every entry carries one of four labels, with who, how, when and evidence stored in an append-only record:

1. **Surveyor-verified** (a person visited or phoned)
2. **Owner-verified** (the owner claimed and confirmed it)
3. **AI-checked** (an agent checked it against sources)
4. **Not verified yet** (visible only to owners and moderators until it reaches AI-checked)

Checks expire; expired entries stay visible, labelled, for a 90-day grace period, then return to draft. Small samples are audited, and an agent job kind stops if audit accuracy falls under 90%.

## 6. Who fills it

| Source | How it works |
|---|---|
| Agents | Draft entries from permitted sources (chambers, associations, registries, open data); capped by spend, off by default, with a kill switch; scraping Google Maps and Facebook is excluded until counsel advises |
| Contributors and volunteers | Students and others add and verify entries; non-cash rewards (levels, certificates, visible credit) and a share of sales |
| Stewards | Revocable ownership of a place segment, with a review queue |
| Owners | Claim and correct their own entry; paid owners get a company page |
| List holders | Import lists they hold; large uploads need staging and an accuracy check (not yet built) |
| Open baseline data | GeoNames and Overture for places; licensed in as the starting layer |

## 7. Who pays and how the platform earns

| Stream | Detail | Built |
|---|---|---|
| Subscriptions | Lower recurring fee for live access; subscribers see no ads; scope by place level | Yes |
| Placements and text ads | Two "Sponsored" slots per list; ads shown to free viewers only; staff approval after payment | Yes |
| Company pages | Full page with extra sections, labelled company-provided; checks and rank cannot be bought | Yes |
| Data extracts | Heavy-priced (about USD 1,000 minimum) with planted trace entries to identify leaks | Yes |
| Delivered outreach | Opt-in messages sent by the platform, contacts stay hidden | Partly |
| Ad networks, Meta ads | Not built; the security policy blocks remote scripts | No |
| Real payment gateway | Manual and signed-webhook paths only; no provider chosen | No |

Evidence from the research: about 1% to 3% of listings pay at Justdial and IndiaMART, revenue concentrates in a thin top tier, and the list types that pay are property, vehicles, urgent services, health facilities and industrial suppliers. The biggest unmeasured cost is selling.

## 8. What visitors and users can do

- Find a list by browsing the tree, by a guided country, city and keyword path, or by one search bar (prototype in `prototype/finder.html`).
- See the first few entries and statistics for free; unlock full lists and roll-ups by subscribing.
- Send a message to an entry; the platform relays it.
- Report something wrong, request removal, opt out.
- Sign up with email, Google or ORCID; two-factor sign-in is built.

## 9. Safeguards

Contacts never shown. Individuals (doctors, tutors, tradespeople) only with consent; child-facing lists not public until safeguarding is designed; health prices dated and sourced. Append-only audit, two-person approval on payouts, KYC for payouts, takedown and erasure, throttling and quotas, trace entries for leak detection, security headers. The founder's rule that providers carry legal responsibility is an aim, not a legal shield; counsel is needed (see `research_notes/Platform requirements/03_legal_responsibility_rule.md`).

## 10. Current state

| Area | State |
|---|---|
| Plan, research, design system, decision log | Done |
| Software (Django, PostgreSQL), 622 tests, CI green | Built |
| One-command list generation | Built; list types, place data and domain still to load |
| Finder prototype with smooth scrolling | Built as a static prototype |
| Real data, hosting, payments, messaging providers | Not done |
| Bulk upload with staging and accuracy check | Not built |
| Phone login, login pop-up, consent banner, help page | Not built |
| Counsel, secret rotation, licence choice, Urdu review (paused) | Owner tasks |

## 11. What success looks like

1. A pilot city with one trade, filled and checked, shows entries accurate at 90% or better after 30 days.
2. At least some buyers pay a deposit for a verified list, at three times the measured cost per verified entry.
3. At least 20% of submitted pages are indexed by day 90.
4. Contributors receive their first share of a real sale.
5. Only then does it scale to more cities, list types and countries.

## 12. Stages

Launch is staged and each stage pays for the next: S0 one small server; S1 managed database, one app server and a CDN; S2 a read replica and worker server. Order of work: finish list generation and data load, bulk upload, payments and phone login, port the new finder pages into the product, pilot city, then expand.

## 13. Open owner decisions

Hosting and payment provider; licence for code and data; counsel; pilot city and trade; ad network versus own ads; bulk-partner policy; which agent sources are allowed; rotation of exposed secrets; when to lift the English-only rule.
