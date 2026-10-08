# AllLists.org

An open-source marketplace where anyone can build a list of anything, sell it, and get paid when it sells.
Small local lists (e.g. beauty parlours on one road) are merged by the platform into bigger ones
(city → district → division → province → country → region → world), and everyone who contributed
to a list shares in its revenue.

> **Status: working software, not yet in production.** The Django application in `backend/` implements the plan in
> `docs/TECHNICAL_PLAN.md` (place tree, lists, entries with four check labels, free and subscriber views, enquiry relay,
> company pages, claims, moderation, contributor ledger and payouts, billing, placements and ads, outreach campaigns,
> statistics and extracts, loaders, monitoring). It has not yet been deployed or connected to a real payment or
> messaging provider. Decisions and assumptions below are recorded in `docs/DECISIONS.md`.

## The idea

- Anyone can create a list: shops on a road, petrol pumps in a city, doctors, schools, books by an author,
  AI tools, presidents of the world, or personal lists (books I read, things I own).
- **One page per list.** Lists sit in a hierarchy (geographic and by topic) and can be merged upward.
- Lists are **sold** by their creators, **subscribed to** for live access, and can be used to **send messages**
  to the listed businesses on behalf of paying suppliers.
- Creators and populators share revenue from sales, subscriptions, messaging and (planned) ads.
- People who already hold lists import them (paste / CSV). Businesses later claim and update their own listing.
- The platform's job is to keep the marketplace running: pricing of merged lists, quality, trust, payments.

## Who it is for

| User | What they do |
|---|---|
| Creators / populators | Build or import lists, add entries, get paid per verified entry |
| Businesses (shops, vendors) | List themselves free, claim and update their entry, optionally pay for promotion |
| Buyers (factories, distributors, suppliers) | Buy lists, subscribe to territories, pay to message shops |
| Consumers | Search local shops and products; free preview, sign up for more |
| Platform | Merges lists, sets merged prices, runs payments, moderation and payouts |

## List visibility

1. **Private** (default, personal): visible only to the owner. Never sold, exported, or used for recommendations without consent.
2. **Shared**: visible to chosen people (class lists, book club).
3. **Public free**: visible to anyone, may show ads.
4. **Public paid**: preview is free; full data requires purchase or subscription.

## Product ladder

| Product | Buyer gets | Price |
|---|---|---|
| Free preview | A few entries and shop counts; first few listings free after sign-up | Free |
| Subscription | Live, scope-based access (territory + category), rate-limited watermarked exports, alerts | Low, recurring (prepaid periods) |
| Messaging | Message delivered to opted-in shops; buyer never sees contact data | Per message / reply |
| Full list | Full data (phones, addresses, locations, ratings, size, etc.) | Highest, one-time snapshot |

Standalone lists are priced by their creators. **Merged lists are priced by the platform.**

## Decisions

1. Creators set the price of their own lists. The platform sets the price of merged lists.
2. Buyers of a list receive the data in it.
3. Contributor share of revenue steps down over time: **50% → 40% → 30%** (platform keeps the remainder).
4. Messaging revenue is shared with contributors at a lower rate than list sales.
5. Subscribers pay a lower recurring fee for live access instead of owning a copy.
6. Imported entries earn nothing until verified. Duplicate shops are credited to whoever added them first.

## Assumptions (please confirm)

- The step-down is **locked per entry at creation date**: an entry added in phase 1 keeps the phase 1 rate. Phases are set by date.
- 30% is the contributors' share in the mature phase (platform 70%).
- Messaging uses the same scale applied to profit after delivery costs.
- Subscription revenue is allocated by scope (entries in the subscriber's territory/category, equal per verified entry), plus a bonus for entries verified or updated that month.
- Payouts are held for a refund window (e.g. 14 days) before becoming withdrawable.
- Self-listed entries (a business adding itself) do not earn payouts, to prevent fake-shop farming.
- Ad revenue share, if offered, is a separate and smaller pool. Ad-network terms on sharing revenue with third parties must be checked first.

## Trust and safety

- Contributors must declare they have the right to share any list they import. The platform does not verify that claim; takedown process required.
- Entries carry source, contributor, verification status and last-verified date.
- Do not copy from Google Maps or other sources whose terms forbid it.
- Messaging only to opted-in shops, with frequency caps, one-tap opt-out and supplier verification (WhatsApp/SMS and local anti-spam rules apply; get legal advice).
- Exports are watermarked (planted trace entries) to detect resale.
- Sensitive personal lists (health, classmates, belongings) are private by default and excluded from recommendations unless the owner opts in.

## Planned architecture (MVP)

- Backend: Python 3.12, Django 5.2, PostgreSQL 16 (built that way). Server-rendered pages so list pages can be indexed; English and Urdu (right to left).
- Data model: geography/topic tree, per-list custom fields (JSONB), entries with contributor and rate phase, revenue ledger (one line per person per sale/period), subscriptions, message batches, payout records.
- Hosting: one managed host and managed Postgres. Kubernetes, Redis and a full monitoring stack are out of scope until there is traffic.
- Pages for empty or thin lists should be `noindex` until they have real content.

## MVP scope

1. Import a list (paste/CSV) with column mapping and duplicate detection
2. Geography tree and categories, custom fields per list
3. Public, indexable list pages with free preview
4. Buy a list (payment recorded manually at first), watermarked export
5. Revenue ledger with per-entry phase rates
6. Simple signup/login

Later: shop claiming, subscriptions, messaging, automatic payments and payouts, collaboration, ads, personal-list suggestions.

## Current state

| Where | What |
|---|---|
| `backend/` | The Django application (see `backend/README.md`) |
| `docs/TECHNICAL_PLAN.md` | The build plan the code follows, with rules R01 to R40 and a traceability matrix |
| `docs/DECISIONS.md` | Every decision, with the build log of what was done and why |
| `docs/MASTER_DOCUMENT.md` | Everything in one document (regenerate with `scripts/build_master_document.py`) |
| `docs/DEPLOYMENT.md`, `deploy/`, `scripts/` | How to run it for real: deploy, rollback, backup, restore drill, load test |
| `docs/runbooks/` | One page for each incident or scheduled task |

What only the owner can do: rotate the secrets that were pasted into chat early on, choose the licence, choose hosting,
a payment provider and a messaging provider, and book counsel before any messaging or list of named people goes live.

## Open questions

- Code license (open source) vs. data license: the code can be open while the list data stays proprietary or under terms.
- What triggers each phase step-down, and is an early rate capped in time?
- Final messaging share and subscription allocation rules.
- Payment and payout providers.
- Legal review: terms of service, data protection, official/government data, messaging rules.
