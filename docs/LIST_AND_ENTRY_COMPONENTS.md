# AllLists.org: components of a list and of an entry (final draft v1, for owner sign-off)

This is the specification the founder asked to finalize, because it will be replicated a very large number of times. It is built from the founder's field list, the decisions in `docs/DECISIONS.md`, and the research in `research_notes/Prototype research/`, `research_notes/Entry template verification/`, `research_notes/Service provider sources/` and `reports/Established platform list types.md`.

Status: **final draft v1**. Everything marked "Decided" comes from the owner. Everything else is my proposal and becomes final when the owner signs off (Q-S12). Items still open are listed in section 10. Text and numbers only (C29): no pictures or videos, but the design reserves a place for media later.

How to read the tables:
- **Req**: R = required to publish, S = should have, O = optional.
- **Show**: P = public to everyone, L = locked (account or paid plan), H = hidden, reached only through the platform's outreach button (E13), I = internal only.
- **Sens**: sensitivity of the data, mainly for individuals (low, medium, high).

## 1. Rules that keep the design stable at huge scale

1. **One fixed core for every entry** (section 4). It never changes shape between list types.
2. **Repeating things are child records**, not extra columns: phones, social pages, hours, services, products, specialities, identifiers, areas served, equipment (section 5).
3. **List-type add-ons come from a registry** (section 6). They can be added, never changed in meaning, and each carries a version number.
4. **Every value carries its own history** (section 7): source, licence, date, who verified it and how, when it expires, consent.
5. **Standard formats everywhere:**
   - IDs: UUID or ULID, never reused.
   - Country and region: ISO 3166-1 and 3166-2.
   - Language: BCP 47 tags (for example `ur`, `en`, `ar`).
   - Currency: ISO 4217, always with a price date.
   - Phone: international E.164 format.
   - Times: ISO 8601 in UTC, plus the local time zone name for opening hours.
   - Coordinates: WGS-84 latitude and longitude.
   - Names: Unicode, stored as typed, with search forms generated separately.
6. **Partition by country** from day one. Stable place IDs make this simple.
7. **Soft delete.** Nothing disappears silently. Removed, merged or closed entries leave a tombstone with a reason.
8. **Lists are views.** A list is a list type at a place. Entries are stored once and rolled up (C12).

## 2. The list: what is a "list"

Three kinds of objects, all needed:

| Object | What it is | Key fields |
|---|---|---|
| **List type** | A kind of thing, such as "eye hospitals" or "surgical instrument makers". It exists, empty, in every place once created (C11). | concept ID; names and aliases per language (for example "petrol pump", "gas station"); parent family; entity type (business, facility, person, institution); template ID (which add-on block entries use); natural scale (hyper-local, city, national, global; C25); crosswalk IDs to ISIC, ISCO, Overture, Foursquare, OpenStreetMap, schema.org; status |
| **Place** | A node in the tree from global down to the street or housing society (C10). | place ID; parent ID; level; names and aliases per language; ISO codes; centre point and bounding box; population or size band if known |
| **List at a place** | The page: one list type at one place. Derived, not stored as copies. | list type ID; place ID; roll-up statistics (section 3); description and inclusion rules; steward; contributor summary; freshness |

Two further kinds are variants of the same model: a **user-made list** (private, shared or public, including personal lists such as books read) and a **topic list** (apps, websites, books, tools) that uses a topic tree in place of the place tree (C27).

## 3. Components of a list page

Layout order, top to bottom. Mark: M = must at launch, S = should, L = later.

| # | Component | Show | Mark | Notes |
|---|---|---|---|---|
| L1 | Place breadcrumb (global to area), each level clickable | P | M | Also the roll-up navigator |
| L2 | List-type path (family, type) | P | M | |
| L3 | Title "{List type} in {Place}" | P | M | One fixed pattern |
| L4 | Scale tag (hyper-local, city, national, global) | P | S | C25 |
| L5 | Summary line: entries listed, entries verified, last updated | P | M | Counts must match the rows shown |
| L6 | Action row: save or follow, share, reach this list (outreach), report | P | M | See section 8 |
| L7 | Description and inclusion rules, one line on how verification works | P | M | Tells contributors what belongs and buyers what they get |
| L8 | Roll-up statistics: totals; by verification level; by child area; share with phone, with price, verified in last 12 months; median price band; top specialities | P or L | M | E14. Each statistic carries an unlocked or locked flag (CP3, CP4) |
| L9 | Child areas table with counts and links | P | M | Roll-up (C12), for example "Adyala Road 14, Bahria Town 52" |
| L10 | Filters: area, category, speciality, price band, verification level | P | M | More filters per list type later |
| L11 | Sort: name A to Z, recently verified, ranked | P | M | "How this list is ordered" link is required once paid ranking exists |
| L12 | Sponsored slots, labelled, capped at one or two | P | S | Only when sold (Q-N2). Never mixed into the verification order |
| L13 | Result rows: name, category, area, verification chip, rank, one action | P | M | Names-only for free users (E14) |
| L14 | Locked-detail marker and upgrade panel saying exactly what unlocks | P | M | |
| L15 | Pagination with a stated limit per account | P | M | Anti-scraping (P15) |
| L16 | Add an entry, suggest an area, claim your business | P | M | Contributor supply (C13) |
| L17 | Related lists: same place other types, same type nearby, parent roll-up | P | S | |
| L18 | Contributors panel and steward panel | P | S | CP9, C20 |
| L19 | Provenance: sources, licence, method, change log link | P | M | D17 |
| L20 | Disclaimer, privacy and opt-out, ad disclosure, terms | P | M | |
| L21 | Empty-list state: "No entries yet. Add the first entry or apply to steward." | P | M | Most pages are empty at launch (C11) |
| L22 | Ads for free users, none for subscribers | P | S | CP5 |
| L23 | Map of results | P | L | Text areas table until maps are added |
| L24 | Compare, user votes, awards | P | L | Not needed to test usefulness |
| L25 | Structured data (invisible), only for what is shown | I | S | Check how names-only pages qualify (Gap, section 10) |

## 4. The entry: fixed core (Tier 1, same for every list type)

The founder's list is covered: name, website, phone, address, map pin, services offered, products offered, speciality, social media pages, and the other fields named earlier (owner, WhatsApp, size, reviewer rankings).

| Key | What it holds | Format | Req | Show | Sens | How it is verified |
|---|---|---|---|---|---|---|
| `entry_id` | Permanent ID | UUID or ULID | R | I | low | n/a |
| `entity_type` | business, facility, person, institution | enum | R | P | n/a | Picks privacy rules (Q-S2) |
| `primary_category` | One list-type concept | concept ID | R | P | low | Selects the add-on template |
| `secondary_categories` | Other list types it belongs to | concept IDs | O | P | low | |
| `name` | Display name | text with language tag | R | P | low | Register match, owner |
| `name_variants` | Alternate spellings, other scripts, legal name, trade name | text list with language tags | S | P | low | Search by many spellings |
| `description` | About, 150 to 600 characters | text | S | P | low | |
| `status` | open, temporarily closed, permanently closed, moved | enum with date | R | P | low | Surveyor, owner |
| `address` | Structured address, in local script and Latin script | structured text | R | P area, L detail | medium (individuals: area only) | Geocode, visit |
| `place_ids` | The place tree nodes it sits in (country, province, city, area, society) | place IDs | R | P | low | |
| `location` | **Map pin**: latitude, longitude (WGS-84), precision class (exact, building, street, area, city), coordinate source, date | numbers | R | P at area precision, L exact | medium | Surveyor, geocode |
| `service_area` | Areas served or travel radius (mobile providers) | place IDs or radius | S (R for trades, tutors) | P | low | |
| `contacts` | Phones, WhatsApp, email (child records, section 5) | E.164, email | S | H (outreach relay) | high for individuals | OTP, call |
| `website` | Main website URL | URL | O | L | low | Liveness check |
| `social_links` | Social media pages (child records, section 5) | typed links | O | L (see Q-S13) | low | Owner confirmation, link check |
| `owner` | Owner or authorised manager name and role | text | O | L for business, H for individuals | high | Claim process |
| `size` | Employees band, beds, rooms or fleet size depending on type | band enum | O | L | low | Owner, surveyor |
| `year_established` | Year | number | O | P | low | Register |
| `parent_entry` | Chain, head office or branch link | entry ID | O | P | low | Keeps lists clean |
| `languages` | Languages served | BCP 47 list | O | P | low | |
| `hours` | Weekly hours, holidays, 24x7 flag, last confirmed date | child records | S | P | low | Owner, surveyor |
| `price_band` | One tier or local price level | enum | O | P | low | |
| `services` | **Services offered**, with prices (child records) | see section 5 | S | name P, price L | low | Mystery call, owner |
| `products` | **Products offered** (child records) | see section 5 | S | L | low | Owner, survey |
| `specialities` | **Speciality** tags | concept IDs | S | P | low | Register, owner |
| `identifiers` | Registration, licence and tax identifiers (child records) | see section 5 | S (R for regulated types) | P as number with register link | medium | Register lookup |
| `payment_methods` | Cash, card, bank transfer, wallets | enum list | O | P | low | Owner |
| `rating` | **Reviewer rankings**: score, count, authenticity statement | numbers | O | P | low | Only after review rules exist (Q-P3) |
| `verification` | Level chips with who, how, when, evidence, expiry (section 7) | structured | R | P | low | Decided (D19, D20) |
| `claim` | Claimed or not, by whom, when | structured | R | P | medium | OTP, documents |
| `provenance` | Source, licence, retrieval date, robots decision (section 7) | structured | R | P summary | low | Decided (D17) |
| `consent` | Consent status for individuals (consented, date, method) | structured | R for persons | P as a tick | high | Decided (D17) |
| `contributor_credit` | Added by, last verified by | user IDs | R | P chosen name | medium | CP9 |
| `steward` | Segment steward | user ID | O | P | low | C20 |
| `media` | Reserved: pictures and video | n/a | n/a | n/a | n/a | Not used at this stage (C29) |
| `visibility_flags` | do-not-share, noindex, suppressed | flags | R | I | n/a | Opt-out (P17) |
| `timestamps` | created, updated, last verified | ISO 8601 | R | P dates | low | |

## 5. Repeating parts of an entry (child records)

| Child record | Fields | Notes |
|---|---|---|
| **Contact** | type (phone, mobile, whatsapp, email, fax), value, label (sales, support, emergency), preferred hours, verified date, relay-only flag | E.164 phones. Never shown (E13); the outreach button reaches them. WhatsApp is a contact, not a social page |
| **Social link** | platform, handle or URL, owner-confirmed flag, last link check | Platforms: facebook, instagram, linkedin, x, youtube, tiktok, telegram, snapchat, pinterest, threads, whatsapp_channel, wechat, weibo, douyin, xiaohongshu, line, kakaotalk, vk, other. Professional profiles for people: github, kaggle, orcid, behance, dribbble, google_scholar. Outbound links use `rel="nofollow noopener noreferrer"` |
| **Opening hours** | day, open time, close time, split shifts, holiday rule, appointment-only flag, confirmed-on date | One row per day-range |
| **Service** | name (concept ID plus text), description, price, price type (fixed, from, hourly, per visit), currency, unit, price date, preparation notes | Price date is mandatory. Health prices wait for the health rules (Q-S1) |
| **Product** | name or category, brand, unit, price band, availability note | Same price-date rule if a price is shown |
| **Speciality** | concept ID, optional qualification, optional own hours (OPD timings) | |
| **Identifier** | scheme (PMDC, PEC category, NTN, SECP, GSTIN, ISO 13485, drug licence and so on), value, issuer, valid from and to, last checked, register link | Store the fact and link, never a national ID number such as CNIC |
| **Area served** | place ID or radius, notes | |
| **Equipment** | type, make and model, quantity, modality (imaging), installed year, services it supports | Optional; evidence says it is not a standard field on platforms |
| **Branch or location** | address, location, hours, contacts | When one organisation has several sites |
| **Alternate name** | text, language tag, kind (legal, trade, old) | Feeds search |

## 6. Add-on blocks by list type (Tier 2, from the registry)

The launch must-haves below come from the live-listing check and the earlier entry template (`research_notes/Entry template verification/01_live_listing_fields.md`, `research_notes/Service provider sources/entry_attributes_by_list_type.md`). Most evidence is from search snippets, so treat the lists as launch candidates.

| List type | Add-on fields (launch) |
|---|---|
| **Doctors** | specialty and qualifications; regulator number and verified flag; years of experience; practice locations with days and times; consultation fee per location with date; appointment mode; languages; gender (self-declared, optional); insurance panels |
| **Hospitals and clinics** | facility type; ownership; licence number, issuer, validity; departments with OPD timings; emergency 24x7; accreditation body, scope, expiry; doctor roster link or count; insurance panels |
| **Labs and imaging** | centre type; modalities or disciplines; test catalogue with prices and dates; preparation notes; home collection; report turnaround; accreditation; radiation licence; MRI field strength and contrast surcharge |
| **Trades (plumbers, electricians, mobile repair)** | display name; services and prices with visit charge; service area; availability and emergency; identity-verified flag and date; police check flag where done; years in trade; warranty period |
| **Schools** | registration body and ID; grades; gender mix and day or boarding; curriculum or board; fee with fee year; campuses |
| **Tutors (including Quran)** | subjects and levels (Nazra, Tajweed, Hifz, translation); mode and travel radius; hourly rate and trial flag; qualifications (degree, ijazah) with checked flag; background-check status and date. Not public until safeguarding is designed (Q-S2) |
| **Manufacturers and exporters** | business type (manufacturer, trader, wholesaler, exporter); product categories with HS code; tax and legal IDs with per-ID verified flag; registered and factory addresses; year established and years exporting; export markets; certifications with body, ID, expiry; verification tier (none, documents, on-site, third-party inspector); capacity and workforce bands; OEM flag; minimum order quantity |
| **Contractors** | entity type and registration; engineering council number, category and validity; work types; project size band; service area; insurance verified flag; years trading; past projects with consent and proof link; key equipment |
| **Real estate agents** | agency and agent name; licence and verified flag where a regulator exists; service areas and societies; listing types; years of experience; languages; active listings count |
| **Hotels** | property type; star class and rating body; rooms and room types; check-in and check-out; amenities checklist; cancellation summary; price from with currency and date; house rules. Show base rate bands only, never surge prices (Murree lesson) |
| **Pharmacies and petrol pumps** | hours with 24x7; brand; services or fuel types; payment methods; pharmacy: delivery flag, drug licence and pharmacist-in-charge; pump: ancillary services |
| **Retail and others** | opening hours; brands carried; services; payment methods; delivery flag |

## 7. Metadata on every value

| Field | Meaning |
|---|---|
| `source` | Where the value came from (register, owner, surveyor, agent, import file) with a link or ID |
| `licence` | Licence or terms that allowed use; records with forbidden terms are blocked (D17) |
| `retrieved_at` | When it was collected |
| `verification_level` | not verified yet, AI-checked, owner-verified, surveyor-verified (decided; D19). Shown as independent chips, not a ladder |
| `verified_by` and `method` | Who checked and how (register match, OTP, visit, call) |
| `verified_at` and `expires_at` | When, and when it must be re-checked. Expired checks drop back |
| `evidence` | Text record of what was seen (no photos at this stage) |
| `consent` | For individuals: consent status, date, method, takedown status |
| `confidence` | Number from 0 to 1 for AI checks (Overture uses the same idea) |

Badge wording rule: say what was checked, by whom and when, for example "DRAP licence seen 2026-10", never a bare "verified". An AI check is labelled "AI-checked".

## 8. Buttons and actions

### List page
| Action | Notes |
|---|---|
| Share: native share, WhatsApp, copy link, Facebook, email, LinkedIn; X in a "more" menu | Plain links, no third-party scripts, tracked with `utm_` tags and a `ref` code. Telegram, SMS, QR and embeds later |
| Reach this list (outreach) | Buyer chooses the channel; contacts stay hidden (E13). WhatsApp first, opt-in only, after counsel (Q-N5) |
| Save or follow | Needs an account |
| Report list | Wrong scope, abuse, duplicate |
| Add entry, suggest area, claim | Contributor funnel |
| Share my list (creators and contributors) | Pre-written message with their `ref` code; opt-in; shows chosen name only |

### Entry page
| Action | Notes |
|---|---|
| Contact through AllLists | Primary action. Never shows phone or WhatsApp number |
| Request a quote | For trades and B2B lists |
| Share: native, WhatsApp, copy, email, Facebook | Message holds name, trade and area only. Hidden for named individuals without consent, anything child-facing, and entries with a do-not-share flag |
| Save entry | To a private or shared list |
| Report entry | Closed, wrong, duplicate, fake, remove my data |
| Suggest an edit | Any signed-in user |
| Claim this business | OTP to a stored contact, then optional documents |
| Not you? Remove or correct | Required on every entry; free (P17) |
| Owner: share my listing and "listed on AllLists" text snippet | After claim; honest level wording |
| Business's own social pages | Plain outbound links, shown only where the field is visible |

Share-link formats, tracking and campaign mechanics are in `research_notes/Prototype research/02_social_buttons_and_campaigns.md`. Campaign rules to keep: no rewards for sharing itself (Meta rules), reward verified contributions, label any benefit as #ad where required, never message people who did not opt in.

### Map pin and links
Store one WGS-84 point per entry. Map links are generated from it at display time, so no provider's data is copied:
- Google Maps: link built from latitude and longitude (format from Google's documentation, not re-checked this session).
- Baidu Maps and Amap: China uses shifted coordinate systems (GCJ-02 for Amap, BD-09 for Baidu). The conversion must happen when a link is built, never in the stored value. This matters for the China market.
- Apple Maps, OpenStreetMap: plain coordinate links.
- External place IDs (Google, Baidu, Foursquare) are stored as identifiers only. Their terms limit what else may be kept, so check before storing anything beyond the ID.

## 9. Entry page layout (top to bottom)

1. Breadcrumb: place, list, entry.
2. Name with variants, category, entity type, status.
3. Trust strip: verification chips (level, who, date; click for what was checked), claimed state, last updated.
4. Action row: Contact through AllLists, Request a quote, Save, Share, Report.
5. Key facts: area and address, service area, hours with confirmed date, price band. Locked markers where the viewer's plan does not unlock.
6. About: description, specialities, languages, year established, size.
7. Type-specific block.
8. Services and prices with price dates; products.
9. Registrations and certifications with numbers and register links.
10. Ratings and reviews, with an authenticity statement, or "no rankings yet".
11. Rank in list, similar entries, other lists this entry appears in.
12. Provenance: source, licence, retrieval date, last three changes, contributor and steward credit.
13. Claim and correct: "Is this yours? Claim", "Suggest an edit".
14. Legal footer: disclaimer, privacy and opt-out, report, consent tick for individuals.

## 10. What is still open (needs the owner)

| # | Open item | Suggested default | Ref |
|---|---|---|---|
| 1 | Is the website link and the social media page links public or locked? They can reveal contacts | Locked on the free view; domain and social handles shown on paid view | Q-S13 |
| 2 | Who writes reviewer rankings and how fake ones are stopped | Verified users only, one per user, separate from paid ranking; until then show "no rankings yet" | Q-P3 |
| 3 | What a "not verified yet" entry may do | Hidden from the public; list counts say "N published, M awaiting verification" | Q-P6 |
| 4 | Names-only preview and search visibility | Test with a sample before launch; structured data only for shown content | Gap |
| 5 | EU trader-traceability rule (publishing trader contacts) versus hidden contacts | Counsel before any EU launch | Gap |
| 6 | Use of the word "verified" | Use only the four decided labels with date and method | Q-P7 |
| 7 | Whether private evidence photos may be kept internally | No pictures at this stage; decide later | C29 |
| 8 | Coordinates for China | Convert at link time only; confirm the map-data licence before any China launch | |
| 9 | Fields marked inference | Check about five live listings per list type in a session with working page access | Q-S12 |

Sign-off (Q-S12): once the owner approves this document, the Tier 1 core and the child records are frozen for version 1. Changes after that follow the rule in section 1: add, never change meaning.

## 11. Changes from the design review (v1.1)

Two independent reviews of the prototype (`research_notes/Design review/`) changed the list and entry components as follows. The page rules are in `docs/DESIGN_SYSTEM.md`.

**One line between free and paid** (replaces any per-field difference between row and entry):

| | Free visitor | Subscriber |
|---|---|---|
| List row | Name and other-language name, type, area, up to three specialities, check labels with date | Same. Subscribers also get one enquiry to many makers |
| Entry page | Everything on the row, plus area, hours, languages, year established, business type, OEM, how it was checked, one message button | Also: street address, exact map pin, size, website, social pages, export markets, minimum order, prices with dates, certificate details |
| List statistics | Count, last checked, split by check type | Also: with a checkable certificate, verified in the last 12 months |
| Never shown to anyone | Phone, WhatsApp, email, owner name of an individual | Same |

**Rules added:**
- The list page order is: title, one-line scope, trust line with a split that adds up to the total, filters and results. The statistics table, areas table and sponsored explanation are removed from above the results; areas become a filter.
- No position numbers on rows. People are never ranked.
- No per-field lock boxes. One panel names what subscribers also see, built from the fields that exist.
- Rows with no value are left out. The page never says "Not stated".
- A closed entry removes the message button and shows its checks as past.
- Only five rows show at first; "Show n more" and a stated free limit follow.
- Share: one native Share button plus WhatsApp and Copy link, the rest under "More options". Copy link gives the clean address.
- Report, claim, correct and remove are one "Something wrong?" section.
- Empty sponsored slots render nothing. Reviews and rankings sections are hidden until real.
- Dates read "18 Sep 2026" with an age, and every check shows its date.
