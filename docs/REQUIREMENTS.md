# AllLists.org: Requirements Register (draft for owner review)

This register collects every requirement, decision and open question found in the material shared so far.
It is a working document: nothing here is built, and nothing marked "unconfirmed" should be coded yet.

## How to read this

**Sources**

| Code | Source |
|---|---|
| U | The owner's own messages in this session (highest authority) |
| C1 | ChatGPT chat: "create an open-source website, one page per list" (original vision) |
| C2 | ChatGPT chat: full plan, MVP scope, 3-hour prototype (React / Flask / GKE) |
| C3 | ChatGPT chat about "Lists all deployment .docx" (the 450-page document). **Second-hand: ChatGPT said it only saw parts** |
| C4 | ChatGPT deployment and server-setup chats (Google Cloud VM, SSH, Nginx) |
| C5 | ChatGPT "debugging mode" chat (backend rewrite and feature list) |
| R | The GitHub repository as it stands |

**Status**

- **Decided**: stated by the owner.
- **Proposed**: suggested in a chat, not yet confirmed by the owner.
- **Conflict**: two sources disagree. Needs a decision.
- **Later**: acknowledged but not for the first version.

**Not seen by me:** the `.docx` files (including the 450-page document), and the ChatGPT share link (blocked by this environment's network policy). Anything from them is second-hand.

---

## A. Vision and scope

| ID | Requirement | Source | Status |
|---|---|---|---|
| A1 | A marketplace where anyone can create a list of anything and sell it at their own price | U, C1 | Decided |
| A2 | The platform earns by taking a share of every sale; contributors earn the rest | U | Decided |
| A3 | Open-source website | C1 | Proposed (code vs. data licensing undecided, see Q-L1) |
| A4 | One page per list (a dedicated, indexable page) | C1 | Proposed |
| A5 | Must scale to a very large number of list pages ("billions") | C1 | Proposed. Risky for search engines; quality threshold needed |
| A6 | The platform's job is to keep the marketplace running; people build and people sell | U | Decided |
| A7 | Examples in scope: shops on a road, petrol pumps in a city, schools, doctors, lawyers, books, AI tools, presidents of the world, car makers, gold mines, high-rises in Manhattan, class fellows, personal belongings | U, C1 | Decided |

## B. Users and roles

| ID | Requirement | Source | Status |
|---|---|---|---|
| B1 | Roles: admin, creator, subscriber | R, C5 | Proposed |
| B2 | Roles: admin, moderator, user | C2 | Conflict with B1 (names differ) |
| B3 | Two kinds of contributor: **list maker** (owns and prices a list) and **populator** (adds entries) | U | Decided |
| B4 | Businesses can add themselves to the relevant list, and later claim their entry | U | Decided |
| B5 | Buyers: factories, distributors, wholesalers, suppliers, researchers, ordinary consumers | U (my analysis) | Proposed |
| B6 | Email/password registration | C2, R | Proposed |
| B7 | Google and Facebook login | C2 | Later |
| B8 | Multi-factor authentication | C2, C4 | Later |
| B9 | User profile customization (themes, avatars) | C2 | Later |

## C. Lists and hierarchy

| ID | Requirement | Source | Status |
|---|---|---|---|
| C1 | ~~Lists start small (road/town) and are merged upward~~ **Replaced on 2026-10-05 by the top-down model (C10 to C16).** Same hierarchy, opposite direction of creation | U | Superseded |
| C2 | Hierarchy must also work for topics (e.g. AI tools → AI writing tools), not just places | U (my inference), C1 | Proposed |
| C3 | Users can drill down ("go deeper") and zoom out between levels | C1 | Proposed |
| C4 | Categories and subcategories (professionals, businesses, places, items) | C1 | Proposed |
| C5 | Lists have different fields (phone, address, location, ratings, business size, and whatever else a list needs) | U | Decided |
| C6 | ~~Entries carry contact info, location, description~~ **Superseded on 2026-10-05 by C17** | R | Superseded |
| C17 | **An entry has these fields:** (1) name, (2) address, (3) owner, (4) phone number, (5) WhatsApp number, (6) social media page, (7) rankings by reviewers, (8) size, (9) available goods, (10) services, and others as each list needs (C5) | U (2026-10-05) | **Decided.** Privacy and quality conditions below (C18, C19) |
| C18 | The **owner** field and any personal phone number are personal data in many countries (especially sole traders). They are shown or used only with the owner's claim or a lawful basis; agents do not collect named-owner data without one. Buyers never see contact fields (E13) | my design (legal research) | Proposed. Needs counsel per launch country |
| C19 | **Rankings by reviewers** need rules: who may review (customers, buyers, both), one review per verified user, fake-review detection, owner reply, and a clear separation from paid ranking (E15). Rules on fake and undisclosed paid reviews exist in several markets | my design | Proposed. Open: who reviews and how (Q-P3) |
| C7 | A list can be merged into several parents? (e.g. both a city list and a category list) | none | **Open** |
| C8 | Merge is performed by the platform, not by users | U | Decided |
| C9 | Lists can be hierarchical by `parent_list_id` (existing schema) | R | Superseded by C10 (a list is a category at a place, not a parent/child record) |
| C10 | **Global from day one, top-down.** The place hierarchy runs global → region → country → state/province → division/district → city → area (road or street). Every list type exists at every place | U (2026-10-05) | **Decided** |
| C11 | **Creating a list type in one place opens it everywhere.** A "petrol pumps" list created in Islamabad automatically exists, empty and open for contributions, in New York, Lagos and every other city | U (2026-10-05) | **Decided** |
| C12 | A list is a pair: a category (e.g. petrol pumps) at a place (e.g. Islamabad). Higher-level lists are **roll-ups** of everything below them, not copies | U (2026-10-05), my design | **Decided** (roll-up mechanism is my design, proposed) |
| C13 | Contributors add entries to any place's list, and **may add areas** (e.g. Adyala Road, Abraham Street) under a city | U (2026-10-05) | **Decided.** Needs rules for approving, naming and de-duplicating user-added areas (Q-O2) |
| C14 | The place tree is seeded from open geographic data (e.g. GeoNames, CC-BY) so that top levels are not user-made; levels differ by country, so level types are generic, not fixed | my design, research notes | Proposed. Avoid GADM (non-commercial); treat OpenStreetMap-derived data under its share-alike licence |
| C15 | A shared, multilingual category taxonomy with synonyms ("petrol pump", "gas station", "fuel station", "filling station" are one category) | my design | Proposed. Who may propose categories, and who approves, is open (Q-O3) |
| C16 | Lists with too few entries are not indexed by search engines and show an invite to be the first contributor | my design (research report) | Proposed |
| C20 | **People may own a segment of a list and correct it** (for example the petrol pumps on one road, or bakeries in one district). Ownership grants the right to verify and correct entries in that segment | U (2026-10-05) | **Decided in principle.** Open: exclusive or shared, how a segment is claimed, how it lapses if the owner goes inactive, how disputes and abuse are handled, whether owners are paid as agents (Q-P2). Being researched |

## D. Getting content in, and keeping it good

| ID | Requirement | Source | Status |
|---|---|---|---|
| D1 | People who already hold lists (e.g. a government officer's non-confidential petrol pump list) paste or upload them | U | Decided |
| D2 | Bulk import (paste/CSV) with column mapping | U (my design) | Proposed |
| D3 | Duplicate detection and removal on import | C3, U (my design) | Proposed |
| D4 | Validation of list data | C3 | Proposed |
| D5 | Imported entries earn nothing until verified | U (my design) | Proposed |
| D6 | First adder of a duplicate entry gets the credit | my design | Proposed |
| D7 | Businesses claim their own entry (phone/WhatsApp code) and keep it current | U (claim), my design (verification) | Proposed |
| D8 | Self-listed entries do not earn payouts (anti-fraud) | my design | Proposed |
| D9 | Entries record source, contributor, verification status, last-verified date | my design | Proposed |
| D10 | Community-driven quality checks | C3 | Later |
| D11 | Contributors declare they have the right to share an imported list; takedown process | my design | Proposed |
| D12 | Entry data must not be copied from sources whose terms forbid it (e.g. Google Maps) | my design | Proposed |
| D13 | Report-an-error flow for any entry | my design | Proposed |
| D14 | **AI agents draft lists from many sources**, then owners and contributors verify. Starting launch markets are places where business data is poor (Pakistan, the Middle East and other countries to be researched) | U (2026-10-05) | **Decided** as direction |
| D15 | Agent source list proposed by the founder: chambers of commerce, trade associations, people's own listings, Google Maps, Facebook, Baidu Maps, general internet research. **Research so far puts the last three scraping routes in the "do not use" tier** (terms and case law), while chambers, associations, owner submissions, government registries and open datasets are the safe tiers. A per-source permission table is being researched | U, legal research | **Open: needs the source-permission table and counsel** |
| D16 | Open baseline data (Overture, Foursquare Open Source Places, government registries) is licensed in as the starting layer; agent output stays private and unindexed until verified; unverified agent pages are not published at scale | U (2026-10-05, agrees with report), AI report | **Decided** |
| D17 | Every record stores its source, licence, collection date, robots decision and consent status | my design (legal research) | Proposed |
| D18 | **Draft-first: keep adding data initially; it becomes reliable later when it is owned and manually verified.** Agent-gathered entries go in at the "draft" state and move to "verified" and then "claimed" through owner claims and manual checks | U (2026-10-05) | **Decided as direction.** Conditions in P14 (what draft entries may and may not do) |
| D19 | **Verification levels (trust categories) on every entry:** (a) verified by the owner, (b) verified by independent data surveyors, (c) verified by AI, (d) not verified yet, and others as needed. The level, who did it, the method, the date and the evidence are stored and shown | U (2026-10-05) | **Decided.** Design notes below |
| D20 | Design notes for D19: **(1)** label the AI level "AI-checked", not "verified", so buyers are not misled; **(2)** an AI check should use different sources or methods from the AI draft, because the same model repeating its own error is not independent; **(3)** surveyors are independent of the contributor who added the entry, with seeded fake entries and sampled audits to catch cheating; **(4)** each level expires and must be re-checked (business data goes stale quickly); **(5)** an entry can hold several levels at once (for example owner and surveyor); **(6)** buyers can filter and price by level, and the whole-list statistics (E14) show counts per level; **(7)** only owner-confirmed entries are messageable (opt-in); **(8)** contributor payouts apply to surveyor and owner levels, not to AI-checked or unverified | my design (research notes) | Proposed |

## E. Products, access and pricing

| ID | Requirement | Source | Status |
|---|---|---|---|
| E1 | Creators set the price of their own lists | U | Decided |
| E2 | **The platform sets the price of merged lists** | U | Decided (formula not defined, see Q-M3) |
| E3 | First few listings are free to view for people who sign up | C1 | Proposed |
| E4 | A free public preview of each list page (needed for search indexing) | my design | Proposed |
| E5 | ~~Buyers receive the data in the list~~ **Superseded on 2026-10-05 by E13.** Original text: buyers receive phone numbers, addresses, locations, ratings, business size, whatever the list holds | U | Superseded |
| E6 | View-only, time-limited access after payment, with paid renewals; data cannot be downloaded | C3 | **Adopted as the default** (resolves the old E5 conflict, see E13) |
| E7 | Subscriptions: lower recurring fee for live, scope-based access (territory + category) | U | Decided |
| E8 | Optional platform-wide subscription to all premium content | C1 | Proposed |
| E9 | Pay-per-view access | C3 | Proposed (overlaps E6) |
| E10 | Exports are rate-limited and watermarked (planted trace entries) to detect resale | my design | Proposed |
| E11 | API access for premium users or businesses | C3, C4 | Later |
| E12 | Pricing ladder: free preview → subscription → messaging → full list | my design, U | Proposed (full list is now the premium rung, see E13) |
| E13 | **Downloading the data is not allowed except at a heavy price (about USD 1,000).** The default product is outreach: the buyer chooses the outreach method and the platform delivers it; the buyer never sees the contact data | U (2026-10-05) | **Decided.** Price basis open: a flat figure versus a price scaled by list size and freshness (Q-N1) |
| E14 | Each list page shows the first few entries plus statistics about the whole list (counts by area, category, verification and freshness), without exposing the rest | U (2026-10-05) | **Decided** |
| E15 | **Listed businesses pay to rank higher in a list** (paid position) | U (2026-10-05) | **Decided.** Needs: auction or fixed price, "sponsored" labelling, and who earns the revenue (Q-N2) |
| E16 | **Government and institutions** (for example tax authorities) may buy lists or list statistics | U (2026-10-05) | **Decided in principle.** Needs a data-sharing policy disclosed to contributors and listed businesses (Q-N3) |
| E17 | The platform is positioned as a cheaper, more targeted alternative to Google and Meta advertising for reaching businesses in a territory or trade | U (2026-10-05) | **Decided as positioning.** Must be tested: cost per reply or lead against Google and Meta (Q-N4) |

## F. Money: revenue sharing

| ID | Requirement | Source | Status |
|---|---|---|---|
| F1 | Contributors get a share of the funds from sold lists | U, C1 | Decided |
| F2 | Contributor share steps down over time: **50% → 40% → 30%**; the platform keeps the remainder | U | Decided |
| F3 | The rate that applies is locked per entry on the day it was added | my assumption | **Unconfirmed** |
| F4 | What triggers each step-down (date, platform size, per entry, per contributor) | none | **Open** |
| F5 | Share per contributor: equal per verified entry (or another basis) | U ("equal or any other base") | Proposed |
| F6 | Revenue also shared from advertising | C1, C2 | Proposed (see H) |
| F7 | Revenue sharing applies "in any case", at a lower share to contributors for messaging than for list sales | U | Decided (figure open) |
| F8 | Subscription revenue allocated by scope (entries in the subscriber's territory/category) plus a freshness bonus | my design | Proposed |
| F9 | Payouts held for a refund window (e.g. 14 days) | my design | Proposed |
| F10 | Admin can configure sharing percentages; payout reports | C2 | Proposed |
| F11 | Payout ledger: one line per person per sale or period (auditable) | my design | Proposed |
| F12 | Payment gateway and payout method (Pakistan: wallets, bank transfer; international: ?) | none | **Open** |
| F13 | Multi-currency, VAT/GST/tax handling | C4 | Later |
| F14 | Seller identity checks (KYC) for payouts | my design | Proposed |

## G. Outreach and messaging

| ID | Requirement | Source | Status |
|---|---|---|---|
| G1 | Platform sends wholesale suppliers' messages to listed shops, for a fee, **without revealing contacts to the supplier** | U | Decided |
| G2 | Email outreach tools for list buyers to contact entries, with campaign analytics | C3 | **Resolved by E13:** the buyer picks the method, the platform sends it, and contacts stay hidden |
| G3 | Channels the buyer can choose: WhatsApp, SMS, email, in-app inbox, phone | U (2026-10-05: the buyer chooses the outreach method), C3 | Decided that the buyer chooses; the list of channels is **open** and legal limits differ by country |
| G4 | Shops opt in (by category and channel); frequency caps; one-tap opt-out | my design | Proposed |
| G5 | Supplier verification and message review before sending | my design | Proposed |
| G6 | Delivery, read, reply and order tracking per campaign | my design, C3 | Proposed |
| G7 | Compliance with anti-spam rules (CAN-SPAM and the local equivalents; WhatsApp/SMS policy) | C3, my design | Proposed (needs legal advice) |
| G8 | Notifications to users, including expiring-access reminders | C3 | Proposed |

## H. Advertising

| ID | Requirement | Source | Status |
|---|---|---|---|
| H1 | Ads shown on list pages | C1 | Proposed |
| H2 | A share of ad revenue goes to creators | C1, C2 | Proposed. Check the ad network's terms on revenue sharing |
| H3 | Featured/sponsored placement sold directly to businesses | my design | Superseded by E15 (paid ranking is now decided) |
| H4 | Affiliate-link revenue | C2 | Later |

## I. Personal and private lists

| ID | Requirement | Source | Status |
|---|---|---|---|
| I1 | Users make personal lists: books read, classmates, belongings, places visited, medicines taken | U, C1 | Decided |
| I2 | Private by default; can be shared with chosen people or made public | C1 | Proposed |
| I3 | Partially public lists (title visible, contents private) | C1 | Proposed |
| I4 | Shared/collaborative lists (classmates, family, book club) | C1, C2 | Proposed |
| I5 | The system suggests public lists based on users' private lists | C1 | **Privacy risk**: needs explicit opt-in; health data excluded |
| I6 | List templates ("books I read", "track medications") | C1, C2 | Proposed |
| I7 | Notifications when a similar public list appears | C1 | Later |
| I8 | Personal lists are never sold, exported or used for recommendations without the owner's consent | my design | Proposed |

## J. Search, discovery and AI

| ID | Requirement | Source | Status |
|---|---|---|---|
| J1 | Search with filters (location, category, rating, price) | C1, C2 | Proposed |
| J2 | Full-text search, autocomplete | C2 | Later |
| J3 | Recommendation engine (TF-IDF now, collaborative filtering later) | R, C4 | Proposed |
| J4 | SEO-friendly URLs mirroring the hierarchy (`/country/province/city/road/category`) | my design | Proposed |
| J5 | Pages for empty or thin lists are not indexed | my design | Proposed |
| J6 | Product-level local search ("where can I buy X near me") | my design | Later |
| J7 | Favorites | C2 | Later |
| J8 | Ratings and reviews of entries | C1, my design | **Open** (who rates, how, anti-abuse) |

## K. Dashboards and engagement

| ID | Requirement | Source | Status |
|---|---|---|---|
| K1 | Creator dashboard: lists, views, earnings, payouts | C1, C2, C3 | Proposed |
| K2 | Buyer dashboard: purchases, subscriptions, expiry dates | C1, C3 | Proposed |
| K3 | List performance analytics (views, clicks) | C2 | Proposed |
| K4 | Activity logs for collaborative edits | C2 | Later |
| K5 | Gamification | C3 | Later |
| K6 | Business view for factories/suppliers: territory coverage, campaign results | my design | Later |

## L. Admin and moderation

| ID | Requirement | Source | Status |
|---|---|---|---|
| L1 | Review reported lists and entries; remove harmful content | C2 | Proposed |
| L2 | Ban or suspend accounts; manage roles | C2 | Proposed |
| L3 | Analytics: API usage, active users, traffic | C2 | Later |
| L4 | Audit log of system actions | R (schema) | Proposed |
| L5 | Seller/contributor dispute handling and refunds | my design | Proposed |

## M. Security, privacy and compliance

| ID | Requirement | Source | Status |
|---|---|---|---|
| M1 | Passwords hashed; token-based authentication | R, C2, C5 | Proposed |
| M2 | Encryption in transit (HTTPS) and at rest | C2, C3 | Proposed |
| M3 | Role-based access control | C3 | Proposed |
| M4 | Anti-scraping, CAPTCHA, content protection | C3 | Proposed (conflicts with SEO goals unless scoped to paid data) |
| M5 | GDPR and CCPA compliance | C2, C3 | Proposed |
| M6 | WCAG 2.1 accessibility | C2 | Proposed |
| M7 | Rate limiting on the API | C2 | Proposed |
| M8 | Secrets only in environment variables; none in the repository | my design | Proposed |
| M9 | **Credentials have already been exposed** (database password and app secret in the public repo; an access token, a key passphrase and a password pasted in chats) | R, C4 | **Action needed: rotate** |
| M10 | Local data-protection and anti-spam law for Pakistan (and any other launch country) | none | **Open: legal advice** |

## N. Platform, technology and non-functional

| ID | Requirement | Source | Status |
|---|---|---|---|
| N1 | Python backend with PostgreSQL | R, C2, C3 | Proposed |
| N2 | Frontend: React SPA with Redux and Tailwind | C2 | Conflict with my advice: server-rendered (Next.js/Astro) for SEO |
| N3 | Multilingual support with real-time language switching | C2 | Proposed. Urdu (right-to-left) and English likely needed early |
| N4 | Offline/service-worker support | C2 | Later |
| N5 | Kubernetes on Google Cloud, Prometheus, Grafana, Terraform | C2 | Not recommended for the first version |
| N6 | Redis caching, task queues (Celery), database replication/sharding, CDN, auto-scaling | C4 | Later |
| N7 | Distributed storage for media and large lists | C3 | Later |
| N8 | Database optimized for hierarchical data | C3 | Proposed |
| N9 | CI/CD through GitHub Actions | C2, R | Proposed (CI currently fails: no tests) |
| N10 | Daily database backups | C4 | Proposed |
| N11 | Local development with Docker Compose | C2 | Optional |
| N12 | Real-time analytics for creators and admins | C4 | Later |

## O. Deployment and operations (current state)

| ID | Fact | Source |
|---|---|---|
| O1 | Google Cloud VM named `all-lists-server`, Ubuntu with Python 3.8 (out of support) | C4 |
| O2 | The domain `alllists.org` exists; DNS not yet pointed at the server; no HTTPS | C4 |
| O3 | Code is on GitHub (repo made public during the chat) and also on GitLab | C4 |
| O4 | The server copy was assembled by hand-pasting files and has diverged from the repo | C4 |
| O5 | The backend failed to start (stray text in files, Flask/Werkzeug mismatch) | C4 |
| O6 | The owner is non-technical and wants **one step at a time**, with a hassle-free deployment | U |
| O7 | An ephemeral external IP is in use (changes on reboot) | C4 (inferred) |
| O8 | The repo's current backend cannot run even with correct dependencies | R, my review |

---

## O2. Commerce layer (vision stated 2026-10-05; staged, not for version 1)

The owner's longer-term vision: lists of salons, spare-parts shops, bakeries, mobile stores and so on become a way for factories to reach shops directly, with no middlemen, shipping from factory to shop. It is described as a "reverse Alibaba" or a "specialised Amazon" with very targeted marketing.

| ID | Capability | Source | Status |
|---|---|---|---|
| V1 | **Demand intelligence:** companies see what is in demand in a trade and place (counts, searches, requests), built from aggregate list data | U | Vision. First step is the whole-list statistics already decided in E14 |
| V2 | **Product requests:** shops post what they want and companies receive the requests (request for quotation) | U | Vision. Asset-light, can follow the outreach product |
| V3 | **Product testing:** companies pilot or test new products with a targeted set of shops (samples, surveys, trial orders) | U | Vision |
| V4 | **Direct sell offers** to shops, with no middlemen | U | Vision. The outreach product (E13) is the first step |
| V5 | **Direct shipping** from factory to shop through the platform | U | Vision. Needs payments, escrow, logistics partners, returns, disputes, import/export and tax compliance |
| V6 | Very targeted audience: ads reach only shops in the relevant trade and place, instead of broad Google and Meta advertising | U | Decided as positioning (E17) |
| V7 | Shop-side controls: topics, channels and frequency caps, so many companies do not flood the same shops | my design | Proposed. Needed from the first outreach campaign |
| V8 | Verified factory and shop accounts (KYC) before offers and orders | my design | Proposed |

**Staging proposed:** (1) directory plus statistics plus paid outreach; (2) product requests and test panels, still data and messaging only; (3) transactions through partners for payments and logistics. The platform should own logistics or credit only if the earlier stages show demand. Each stage is gated on evidence (reply rates, repeat buyers, shops asking to order).

---

## P. Conflicts that need a decision

| # | Conflict | Sources | My recommendation |
|---|---|---|---|
| P1 | ~~Buyers receive the data vs. view-only, no downloads~~ | U vs C3 | **Resolved 2026-10-05 (E13):** no download except at about USD 1,000; outreach and view-only access are the default |
| P2 | ~~Messaging via WhatsApp/SMS with hidden contacts vs. email tools for buyers~~ | U vs C3 | **Resolved 2026-10-05 (E13, G2, G3):** the platform sends on the buyer's chosen method and contacts stay hidden |
| P11 | **Global from day one** versus the research recommendation to start with one trade in a few cities | U (C10) vs research report | **Partly resolved.** The data model and place tree are global from day one (cheap to do). Marketing, selling and messaging are switched on country by country, because privacy, messaging and tax law differ per country. Contributions about businesses in any country raise that country's data-protection duties from the first entry |
| P12 | Top-down generated lists (C10 to C12) versus "creators set the price of their own lists" (E1) | U vs U | **Open.** If every list at every place exists automatically, nobody "creates" a list to price. Decide whether the platform prices all lists (with E2) and whether the creator of a new list type or area earns anything beyond per-entry credit (Q-O1) |
| P14 | **Draft-first collection (D18) versus "agent output stays private and unindexed until verified; no unverified pages at scale" (D16)** | U vs U | **Proposed resolution, needs the owner's decision.** Collecting draft data early is accepted. Draft entries may be shown to owners so they can claim and correct them, and may be shown publicly only with a clear "unverified" label above a minimum quality bar (for example two sources agree, working phone or website, business-level fields only). They must **not** be sold as verified, **not** counted in paid-list statistics as verified, **not** messageable until the owner opts in, **not** indexed by search engines at scale, and **earn no contributor payout** until verified (Q-P6) |
| P13 | Paid ranking (E15) at which level? | U (E15, C10) | **Open.** A business can rank at its area, its city, or higher; each level is a different price and a different audience (Q-O4) |
| P8 | Outreach is now the main product, but the business-case research ranked message campaigns as the riskiest product and recommended launching them last | U (E13) vs research report | **Open.** Legal exposure moves to the platform as the sender (Pakistan's cybercrime law s.25, US TCPA and CAN-SPAM, EU ePrivacy and GDPR, WhatsApp opt-in). Decide the first country and channel with a lawyer before building |
| P9 | Paid ranking (E15) versus contributors paid per verified entry, and versus the verified-quality promise | U (E15) | **Open.** Who earns paid-ranking revenue, and how paid positions are labelled |
| P10 | Government as a buyer (E16) versus businesses' and contributors' willingness to list | U (E16) | **Open.** Disclose the policy; consider starting with aggregate statistics only |
| P3 | Role names admin/creator/subscriber vs admin/moderator/user | R vs C2 | Use a role set that includes both: admin, moderator, plus the capabilities creator/buyer/subscriber |
| P4 | React SPA (N2) vs. server-rendered pages for search ranking | C2 vs my advice | Server-rendered |
| P5 | Anti-scraping/CAPTCHA (M4) vs. public indexable pages (J4) | C3 vs my design | Protect only the paid data and exports |
| P6 | Billion-page scale (A5) vs. search engines penalizing thin pages (J5) | C1 vs my design | Index only pages above a quality threshold |
| P7 | Heavy infrastructure (N5) vs. a small first launch | C2 vs my advice | One server or one managed host first |

## Q. What I still don't know

1. **The contents of the 450-page document and the other attached `.docx` files.** The largest gap. Only a partial ChatGPT summary exists.
2. **The ChatGPT conversations in full** (the share link is blocked for me).
3. **The state of the code on the server and on GitLab**: whether a finished version exists that differs from this repo.
4. Branding: logo, colors, tone.
5. Launch geography, languages and first target categories.
6. Who the first contributors and first paying customers will be.
7. Budget, timeline and team (who else will work on this).
8. Legal entity, payment accounts, and who handles accounting and tax.
9. Which payment providers and payout methods you can actually use.
10. How merged lists are priced, in concrete terms.
11. Refund and dispute policy.
12. Who moderates and verifies data day to day.
13. Your domain registrar and the VM's exact setup.

## R. Questions for the owner

**Blocks coding (answer first)**

1. Do buyers download the data, view it online for a limited time, or both? (P1)
2. Which channels will the messaging service use: WhatsApp, SMS, email, in-app? (P2)
3. How should merged list prices be calculated? Suggestion: a per-entry rate, adjusted for how many entries are verified and how recent they are.
4. What triggers each step in 50% → 40% → 30%, and is an early rate locked on each entry? (F3, F4)
5. What share of messaging revenue goes to contributors? (F7)
6. Which payment provider will take money in and pay contributors out? (F12)
7. Is a list in the first version a flat directory entry (name, phone, address) or does each list define its own fields? (C5)
8. Can an entry belong to several merged lists (geographic and by category)? (C7)

**Can be decided during build**

9. Are personal lists in version 1 or later? (I)
10. Are ratings and reviews in version 1? (J8)
11. Are ads in version 1? (H)
12. Which languages at launch (English, Urdu)?
13. What are the first 2–3 categories and the first city?
14. Code license versus data license (Q-L1).

**Business and legal**

15. Who will review the terms of service, data-protection position and messaging rules?
16. Who can verify entries, and are contributors paid before or after verification?

**Added 2026-10-05 (from the decisions on downloads, outreach, ranking and government buyers)**

- **Q-N1.** Is the USD 1,000 download price flat, or scaled by list size and freshness? (A list of 50 entries and a list of 50,000 entries cannot cost the same.)
- **Q-N2.** How is paid ranking sold (fixed monthly price, auction, tiers), how many paid positions per list, and does any of that revenue go to the contributors of the entry or the list? Paid positions must be labelled "sponsored".
- **Q-N3.** What is the policy for selling to government: aggregate statistics only, or full lists? Will it be disclosed to contributors and listed businesses before they join?
- **Q-N4.** How is "cheaper and more targeted than Google and Meta" measured: cost per reply, per lead, or per order? What is the target price per message or per reply?
- **Q-N5.** Which outreach channels does the buyer choose from in the first country (WhatsApp, SMS, email, phone, in-app), and who bears the legal responsibility for message content?
- **Q-N6.** Which country and which trade come first? This decides which messaging laws apply (see the business case report).

**Added 2026-10-05 (from the top-down, global-from-day-one decision)**

- **Q-O1.** Who earns when a brand-new list type is created, and who sets prices now that every list exists everywhere? Suggestion: the platform sets all prices; the creator of a new list type earns a small bonus on early sales; entry credit works as before.
- **Q-O2.** Who may add an area (Adyala Road, Abraham Street)? Suggestion: any contributor may propose, a moderator or a duplicate check approves, and the name is matched against existing areas first.
- **Q-O3.** Who may propose and approve categories (taxonomy)? Suggestion: seed from an open taxonomy, let contributors suggest, moderators approve, and merge synonyms.
- **Q-O4.** At which level does a business pay to rank (area, city, country)? Suggestion: sell per level, with the city level as the first product.
- **Q-O5.** In which countries is selling and outreach switched on first? (Structure is global, but each country needs legal clearance before messaging is enabled.)

**Added 2026-10-05 (from the launch-market, source and entry-field decisions)**

- **Q-P1.** Which countries and trades come first? Pakistan and the Middle East are named; a research round on data-poor launch markets is under way.
- **Q-P2.** How does segment ownership work: exclusive or shared, how claimed, how lost, and are owners paid (fixed fee per verified entry, share of sales, or both)?
- **Q-P3.** Who may write the "rankings by reviewers" on entries (customers, buyers, both), and how are fake reviews prevented?
- **Q-P4.** Which of the founder's agent sources are used (chambers, associations, owner submissions, registries, open data) and which are excluded (Google Maps, Facebook and Baidu Maps scraping), after counsel reviews the permission table?
- **Q-P6.** What may a draft entry do? Suggested: be visible to its owner and to moderators; be publicly visible only with an "unverified" label above a quality bar; never be sold as verified, messaged, indexed at scale or paid for. How many manual checks are needed before it counts as verified (for example owner claim, or a sampled check)? **Partly answered 2026-10-05:** the owner agreed to the first suggestion and added verification levels (D19). Working reading, to be confirmed: "not verified yet" entries are visible only to owners and moderators; entries at "AI-checked" or higher may be shown publicly with a clear level badge and date.
- **Q-P7.** What does each level require exactly (AI-checked: which automated checks and sources; surveyor-verified: phone, visit or both, with what evidence; owner-verified: which claim method), how long does each level last before re-check, and who pays the surveyors?
- **Q-P5.** Are agent networks really free? Being tested: open-weight models and agent frameworks cut model costs, but proxies, verification and human review remain.

---

## Contributor pay, access tiers and revenue streams (decisions of 2026-10-05)

The owner's stated principles: **better usage and returning clients**, and **revenue streams**, to be designed together.

| ID | Decision or idea | Source | Status |
|---|---|---|---|
| M1 | **People are not paid up front. Contributors get their share only when a list is sold.** Many volunteers (students and others) are expected to contribute | U | **Decided.** This replaces my earlier suggestion of fixed cash bounties per verified entry. Risk: early revenue is zero, so motivation must come from non-cash rewards (see M9) |
| M2 | **Businesses will eventually pay to be on the list**, once the platform is well known. Whether unpaid businesses are **hidden or merely ranked lower** is still to be explored | U | **Decided in principle, mechanism open** (Q-R1) |
| M3 | **Access depends on level.** Small segments (for example schools on one road) may be free; larger roll-ups (for example schools in a city) require payment | U | **Decided as direction** (reading of an ambiguous sentence, please confirm, Q-R2). Risk in P15 |
| M4 | **A free preview shows names only; the other fields appear after payment** | U | **Decided as an option to test.** Consistent with E14 |
| M5 | **Free users see advertisements; subscribers see none** | U | **Decided as an option to test** (Q-R3: which ads, and who earns ad revenue) |
| M6 | **Governments and institutions may buy lists** | U | Already recorded as E16 |
| M7 | Revenue streams considered so far: list purchases, subscriptions, outreach delivered by the platform, paid ranking and listing by businesses, advertising to free users, the heavy-price download, institutional sales | U, earlier decisions | The mix and the order are to be strategised (see strategy table in the chat summary and Q-R4) |
| M8 | Every access or pricing rule is judged on two tests: **does it improve usage and bring clients back**, and **does it add revenue** | U | **Decided as the design test** |
| M9 | Non-cash contributor rewards to keep volunteers: reputation levels, certificates or letters useful for students' CVs, visible credit on the entries and segments they own, and free or discounted access to data in proportion to verified contributions ("give to get") | my design | Proposed (Q-R5) |
| P15 | **Free small segments versus paid roll-ups:** if every road is free, a visitor can collect all roads and rebuild the paid city list | my analysis | **Open.** Mitigations to decide: names-only on free views, account and rate limits, daily caps, anti-bot checks, terms of use, watermarking, and charging more as the list gets bigger |
| P16 | **No cash payments** (M1) versus the verification levels (D19) that need people to verify entries: surveyor verification is unpaid | U vs U | **Open.** Verification capacity will depend on volunteers and on owners; the 1,000-record pilot should measure how many checks volunteers actually complete |
| P17 | **Charging businesses to appear (M2)** versus rules that let people remove or correct their own data for free (sole traders' personal data) and consumer-protection rules on directory fees | my analysis | **Open, needs counsel.** Do not charge a fee for removing personal data; charge for visibility, ranking and extra features instead |

- **Q-R1.** If businesses pay to be listed: is the list hidden for unpaid businesses, or are they shown lower with fewer fields? Suggested starting point: all listed, free basic entry, paid for rank, badge, extra fields and leads, and decide on hiding only after traffic exists.
- **Q-R2.** Please confirm the reading of "Adyala Road free, Rawalpindi paid": small segments free (names only), city and larger roll-ups paid.
- **Q-R3.** Which ads do free users see (platform-sold supplier ads in the relevant trade and place, or general ad networks), and does any ad revenue go to contributors and segment owners?
- **Q-R4.** Which revenue streams switch on first, and at what traffic level do paywalls and business fees start?
- **Q-R5.** Which non-cash rewards will you offer volunteers?

---

## Strategy decisions recorded 2026-10-05

| ID | Decision | Source | Note |
|---|---|---|---|
| S1 | The idea is judged **workable enough to refine fully before any coding** | U | The research calls it plausible but unproven; the first proof is a buyer paying for a verified list |
| S2 | **Coding starts only after refinement, and proceeds top to bottom** (global structure first, then country, region, city, area), within the phased plan | U | No code is written until the owner says so |
| S3 | **All countries are included in the structure, but go-to-market focuses on countries with lighter data-usage restrictions first** | U | Consistent with P11. Design for later strict markets from the start: per-record provenance, consent status, opt-out and deletion (D17), so data collected early can be carried into stricter markets |
| S4 | The product aims to become a **high-end product** as it reaches high-end markets | U | In high-end markets the buyer pays for verified, owner-claimed, compliant data, not raw volume; accuracy and compliance records are what make it high-end |

---

## Next step

Share the `.docx` files (put them in the repository under `docs/source/`, or paste their text) and unlock `chatgpt.com` for this environment, so I can read the sources directly. Then this register gets corrected against the real documents and the Questions in section R get answered. Only then should coding start.
