# Page anatomy of LIST pages and ENTRY pages across comparable platforms (prototype research, 2026-10-05)

Purpose: give the founder one checklist of every component a list page and an entry page can carry, which established platforms show each, and what the AllLists prototype should include. Text and numbers only (decision C29): no images, no video. No code. This file does not repeat the list-type, category or field-template findings in `research_notes/Established platform list types/01` to `06` or `research_notes/Service provider sources/entry_attributes_by_list_type.md`; it adds page anatomy, trust and compliance components, and the AllLists-specific components from `docs/DECISIONS.md`.

## 0. Method, evidence limits and legend (read first)

- Method: WebSearch (standard). The shared search budget for the session ran out after about 23 successful queries (out of the roughly 35 planned), so Yelp's own page, Justdial badge meanings, Airbnb, Product Hunt and Goodreads details could not be re-queried. WebFetch was tried on 6 pages (practo.com, trustseal.indiamart.com, support.google.com, goodreads.com, en.wikipedia.org, documentation.g2.com) and every one returned EGRESS_BLOCKED. So no page was read directly. Everything here comes from search snippets (model-summarised), help-centre titles, or earlier notes in this repo.
- All URLs below were returned by search on 2026-10-05. Page dates are unknown unless stated. Anything undated is therefore treated as possibly stale.
- Evidence column "Ev": **S** = at least one platform's component was seen in a snippet or earlier repo note, with a URL in section 1 or a cited note. **B** = background knowledge of how the platform usually looks, no URL this session: **UNVERIFIED**, must be checked against a live page before it is used in a public document.
- Platform codes: GM Google Maps/Business Profile; JD Justdial; YP Yelp; IM IndiaMART; AL Alibaba; PR Practo; ZD Zocdoc; UC Urban Company; ZM Zameen; PH Product Hunt; G2 G2; GR Goodreads Listopia; WP Wikipedia list pages; AB Airbnb; BK Booking.com; LI LinkedIn; TA Tripadvisor. Others used: HG Healthgrades, MH Marham, DF Doctify, PF Property Finder, BY Bayut, HZ Houzz, CT Checkatrade, TT Thumbtack, NX Nextdoor, CL Clutch, AN AlternativeTo.
- Priority: **Must** = prototype fails its purpose without it; **Should** = include if time allows in the first build; **Later** = design a slot, do not build now.
- Strongest recommendation for the next step: a 2-hour screenshot audit (a person with a normal browser opens one live list page and one live entry page on each of the 16 platforms and ticks this file's tables). That would convert every B to S. I could not do it from this environment.

---

## 1. Platform-by-platform anatomy (what was confirmed, what is background)

Each block gives (a) list or results page, (b) entry page, (c) trust and compliance. Items followed by (S) have a source; items followed by (B) are background and UNVERIFIED.

### 1.1 Google Maps / Business Profile (GM)
- (a) Results list with map beside it, "Sponsored" label on paid business listings. A "Sponsored" tag was reported moving to the top-left corner of business listings in Search (https://ppcnewsfeed.com/ppc-news/google-tests-new-ad-label-position-in-business-listings/, undated) while another report says Google replaced "Sponsored" with an "Ads" label in Search (https://www.seroundtable.com/amp/google-replaces-sponsored-label-with-ads-label-29707.html, undated): the wording has changed over time, so do not copy it; use our own plain word (S). Filters for rating and opening hours, sort by relevance/distance (B). Saved lists (Favorites, Want to go, custom), private or shared or collaborative, shared by link (S; see `06_topic_and_curated_lists.md`, TechCrunch 2017-02-13).
- (b) Name, category, address, hours, phone, website, directions, photos, reviews, Q&A, posts, attributes (accessibility, amenities, payments, service options) (S; see entry_attributes file). "Suggest an edit" and "Report a problem" (S, https://www.zoho.com/publish/google-business-profile-guide/support/ and https://support.google.com/maps/answer/16109801, title only). "Claim this business" flow (S, https://maps.google.co.uk/intl/en/business/resources/getting-set-up/claim-verify-google-my-business-listing/). Q&A answers by the business are labelled "owner" (S, https://www.podium.com/article/google-my-business-questions-answers, secondary). UNVERIFIED whether Google Q&A is still live in 2026: check before copying.
- (c) The primary category decides which attributes, reviews and Q&A appear (S, entry_attributes file). Verification is a separate step from claiming (postcard, phone, email, video: B).

### 1.2 Justdial (JD)
- (a) Search by city or locality plus category plus keyword (S, https://yespress.io/justdial.md, UNVERIFIED). Result card carries rating, rating count, a "verified" flag, phone number and a listing link (S: the scraper schema at https://apify.com/themineworks/justdial-business, tertiary). Paid tiers Platinum/Gold/Silver rank businesses higher (S, prior note 01, UNVERIFIED). "Show number", "Send enquiry", "Get best deal", sort and quick-filter chips (B).
- (b) Name, address, phone as the main product, ratings, hours, services, photos, year established, "claim/free listing" prompts (B).
- (c) What "verified" means on Justdial: NOT FOUND in any source. Removal: a business or person is told to email privacy@justdial.com (third-party page https://www.offlist.me/justdial-removal, UNVERIFIED), and users complain removal is slow (https://www.consumercomplaints.in/justdial-com-not-removing-my-business-details-even-after-requesting-on-phone-and-through-email-c3541130, a complaint, one-sided). Lesson: a visible takedown path matters.

### 1.3 Yelp (YP)
- (a) Search results: sponsored results labelled and placed at top of relevant results (S, https://sfist.com/2009/04/02/yelps_yelp_reviews_mixed/ , 2009 and old); category and attribute filters, sort "Recommended / Highest rated / Most reviewed" (B). Editorial lists such as Top 100 Local Businesses (S, prior note 01).
- (b) Name, category, rating, review count, price band ($ to $$$$), hours, address, map, phone, website, "Request a quote" for home services, "Claimed" tick (B). Reviews split into "recommended" and "not currently recommended" by automated software (S, but only from low-quality pages: https://s10500.lovable.app/insights/yelp-recommendation-software-explained, https://www.npr.org/sections/alltechconsidered/2010/03/yelpola_businesses_claim_yelp.html; the 25 to 35 percent filtered figure is UNVERIFIED and should not be quoted).
- (c) Claims about a paid verification badge for home and professional services come from one low-quality page: UNVERIFIED. Businesses cannot pay to unhide reviews (same page, UNVERIFIED).

### 1.4 IndiaMART (IM)
- (a) Product or supplier search results with "Contact supplier" and "Get latest price" buttons (B). Supplier directory by product, city, business type (S, prior note 02).
- (b) Company page shows TrustSEAL and GST badges. TrustSEAL is described as "genuine sellers certified by IndiaMART for legal status, existence and quality standards"; each seal has its own certificate page headed "Following details of the company have been verified*" listing Director or Proprietor, GSTIN, business address and Import Export Code (S, https://trustseal.indiamart.com/members/arihant-crystal and 8 sibling pages; https://export.indiamart.com/ for "Verified Exporter"). Response rate, member-since, years in business, employee band (B).
- (c) The certificate is a separate public page that states which fields were checked: a good model for per-field verification (S).

### 1.5 Alibaba (AL)
- (a) Product-led list with supplier cards: price tiers, MOQ, "Verified" badge, Trade Assurance mark, "Chat now" (S/B: https://www.cosmosourcing.com/blog/what-are-alibaba-verified-suppliers, secondary; MOQ tiers shown at https://seller.alibaba.com/blogs/2026/southeast-asia/industrial-machinery/moq-bulk-pricing-guide-alibaba-b2b).
- (b) Supplier profile: company type, years on platform, factory size, staff, certificates, main products, export markets, reviews, "Contact supplier" (B); tiered price table (S).
- (c) "Verified Supplier" means documents checked online and an on-site inspection by an outside firm (SGS, TUV Rheinland, Intertek) (S, cosmosourcing page above and https://www.intertek.com/news/2010/11-16-audit-services-alibaba/ dated 2010). Trade Assurance holds payment in escrow (S, secondary).

### 1.6 Practo (PR) and Marham (MH), Doctify (DF)
- (a) Doctor list ordered by a proprietary relevance score using location, speciality, patient feedback, bookings in last 30 days and availability; badges such as "most booked / recommended" (S, prior note 04, 2014 blog, UNVERIFIED as current).
- (b) Profile shows a "Medical Registration Verified" badge, recommendation count and patient stories, surgeries and treatments, specialisation and experience, multiple clinics with hours, qualifications, feedback categories, video and in-clinic booking (S, practo.com doctor pages returned by search, e.g. https://www.practo.com/mumbai/doctor/dr-nitin-rathod-general-physician). Marham: "PMDC Verified", fee for online consult, weekly slots (S, prior note 04). Doctify: review verified by mobile number (S, prior note 04, undated).
- (c) Registration verification is an explicit badge near the name. Doximity builds stub profiles from the public register and doctors claim them for free (S, prior note 04): the same pre-built-then-claim path AllLists plans.

### 1.7 Zocdoc (ZD)
- (a) Search by location, speciality, insurance, availability, symptoms or procedure; results show real-time openings; filters insurance in-network, languages, gender, under-18 patients (S, https://www.zocdoc.com/about/ai-llm-info/ and prior note 04).
- (b) Profile with verified patient reviews, in-network insurers, booking, digital intake forms (S).
- (c) Review authenticity rule stated publicly: a verified review needs a Zocdoc booking, an attended or interacted appointment, and submission from the logged-in account or a visit-specific link; label "Verified patient" (S, https://thepapergown.zocdoc.com/facts/verified-reviews-real-patients/). Sponsored listing treatment: NOT FOUND.

### 1.8 Urban Company (UC)
- (a) Category and city pages, URLs by city plus locality (S, prior note 03). Service menu with fixed prices and a cart ("Add"), rating shown per service (B).
- (b) No individual-professional page: customer sees the brand, price per package, rating, what is included (S for model, prior note 03; B for layout).
- (c) Trust is a platform promise (trained, background-checked, insured, "UC promise") rather than a per-entry badge (S, secondary: https://valueforstartups.in/09-urban-company, https://voice.lapaas.com/startup/urban-company/business-model/).

### 1.9 Zameen (ZM) with Property Finder (PF) and Bayut (BY)
- (a) Property results filtered by city, area, type, price, size; map view and area guides; agent and agency directories (S, prior note 05; B for layout).
- (b) Listing has a property ID in its URL (e.g. https://www.zameen.com/Property/..-54361826-6948-4.html, S), a blue or green check mark indicating the property was verified to physically exist and a "reserve" button (S, https://www.zameen.com/blog/common-property-frauds-to-avoid.html), and call, email, SMS and WhatsApp buttons (B). Agent card on Property Finder: super-agent status, verification status, ratings and reviews, WhatsApp response time, claimed deals (S, prior note 05). Bayut sells TruCheck (listing verification) and TruBroker (agent recognition) (S, prior note 05).
- (c) Zameen disclaims responsibility for user ads and says users answer for accuracy and legality (S, same blog and app page https://apps.apple.com/app/id903880271, snippet). "Report ad" button (B).

### 1.10 Product Hunt (PH)
- (a) Daily and weekly leaderboard ranked by community upvotes; Collections that users curate, bookmark and share, shown on user profiles and sometimes on the home page (S, https://techcrunch.com/?p=1093542). Paid slots labelled PROMOTED, ads dominate revenue (S, prior note 06).
- (b) Product page: tagline, description, makers, upvote count, comments, links, topics, similar products, "Follow", "Share", "Report" (B).
- (c) Maker and hunter roles are visible credit (B).

### 1.11 G2 (G2)
- (a) Category page with ranking by verified reviews, Grid Report quadrants (Niche, Contenders, High Performers, Leaders), filters by segment, sponsored placements mixed with organic (S, prior note 06 and https://www.g2.com/ai-instructions).
- (b) Product page: star rating and count, ratings by feature, pricing, vendor info, "claimed profile" (B), review list with labels.
- (c) Every reviewer is validated (LinkedIn or business email) and every review human-moderated; labels "Validated Reviewer", "Verified Current User" (screenshot-validated) and "Business Partner" (conflict of interest, not counted in score); review must reflect experience within two years (S, https://sell.g2.com/g2-trust-and-safety, https://sell.g2.com/review-validity, https://documentation.g2.com/help/docs/how-g2-ensures-authentic-reviews). Best published model for review-authenticity statements.

### 1.12 Goodreads Listopia (GR)
- (a) List page shows title, creator and creation date, number of books and number of voters, tabs "All Votes" and "Add Books to This List", a "People Who Voted on This List" panel, a Like action, voting links beside each book, and the list is re-scored about every five minutes (S, https://indiesunlimited.com/2012/06/26/tutorial-using-goodreads-listopia-to-your-advantage/ dated 2012, plus list pages such as https://www.goodreads.com/list/show/203246.no_substance_just_vibes?tab=book). Score = number of votes and how high voters ranked the book (S). Anyone can add to open lists (S). Tags, comments, report link: B.
- (b) Entries are book cards with rank, score and "add to shelf" (B).
- (c) Open-edit lists show the community-maintained model that AllLists contributors will use (S).

### 1.13 Wikipedia list pages (WP)
- (a) Lead section that "introduces the subject and defines the scope and inclusion criteria", then the list or table (possibly in sub-sections), each item supported by references; notability applies to the list's grouping (S, https://wikipedia.com/wiki/MOS:SAL and https://wikipedia.com/wiki/MOS:LIST). Sortable tables, "See also", hatnote, categories, "last edited" line, history tab, talk page, Wikidata link, cite-this-page (B).
- (b) Each row is the entry: columns are the entity's properties, with a reference column (S, prior note 06).
- (c) Neutral, referenced, no ranking by votes (S, prior note 06).

### 1.14 Airbnb (AB) and Booking.com (BK)
- (a) Results with map, price per night, filters, sort, "Guest favourite" or "Superhost" marks, wishlist heart, share (B). Booking.com shows "Ad" or sponsored marks in results (B, not confirmed).
- (b) Listing: title, host profile (shown on the listing and linked: S, https://www.airbnb.com/help/article/3812), rating and category ratings, reviews, amenities, house rules, cancellation policy, price breakdown, map with approximate location until booking, "Report this listing" (B).
- (c) Booking.com: a review can only be left after a booking; 370 million "verified" reviews; "Best of Booking" requires more than 50 reviews in the past 14 months (S, https://www.booking.com/reviews.html and https://www.bookingholdings.com/brands/booking/). Approximate location until booking is a model for hiding exact contact data.

### 1.15 LinkedIn profile (LI)
- (a) People search results with mutual connections; Services Marketplace by service, location, language (S, prior note 05).
- (b) Name, headline, location, "About this profile", experience, education, skills, recommendations, contact info panel, follow/connect/message, "People also viewed", report/block (B).
- (c) Verification checkmark: clicking it shows what was verified (identity, workplace, or school); the badge is free and cannot be bought (S, https://www.linkedin.com/help/linkedin/answer/a1492056, secondary https://socialbee.com/blog/how-to-get-verified-on-linkedin/); recruiter verification added 2024 (S, https://www.axios.com/2024/04/09/linkedin-recruiters-job-scams).

### 1.16 Tripadvisor (TA)
- (a) City page "Restaurants in X": URL carries a place ID (e.g. g255060) and a category (S, https://www.tripadvisor.com.au/Restaurants-g255060-zfn20932011-Sydney_New_South_Wales.html); filters for cuisine, price band ($ to $$$$), meal type, minimum rating, online reservation, Travellers' Choice winners (top 10 percent of listings); ranking by a Popularity Index of review quality, quantity and recency; paid listings mixed with organic and labelled (S, https://apify.com/duncan_cf/tripadvisor-restaurants.md, https://www.hospitalitynet.org/news/4120110.html).
- (b) Listing: rank "#N of M restaurants in city", rating, review count, cuisine, price, hours, address, map, claim ("Is this your business?"), suggest edits, owner responses (B).
- (c) A UK advertising watchdog ruled that Tripadvisor could not guarantee review authenticity (https://www.pinsentmasons.com/out-law/news/tripadvisor-authenticity-claims-misleading-and-unsubstantiated-ad-watchdog-rules, about 2011 to 2012, undated in snippet) and since then it publishes a Transparency Report: 2.7 million fraudulent reviews blocked in 2024, review boosting 54 percent of fraud (S, https://www.hospitalitynet.org/news/4126305.html, March 2025). The "rank #N of M" line is an elegant roll-up statistic shown on the entry itself.

---

## 2. Master table of LIST-page components

Priority reasons relate to the founder's decisions (global place tree, names-only free preview, outreach button, verification levels, text and numbers only).

| # | Component | Platforms showing it | Purpose | AllLists prototype | Reason | Ev |
|---|---|---|---|---|---|---|
| L1 | Place breadcrumb (Global > Country > Province > District > City > Area) with each level clickable | TA (place ID in URL), NX topic+city+state, UC locality URLs, ZM, GM | Navigation, SEO, orientation | **Must** | The place tree is the product (C10, C12); breadcrumb is also the roll-up navigator | S |
| L2 | List-type (category) breadcrumb or tree path | YP, TA, JD, Foursquare category tree (prior note 01) | Move between "plumbers" and "electricians" in the same place | **Must** | Lists are "category at a place" (C12) | S |
| L3 | Sibling-place switcher (neighbouring areas, parent, child) | ZM, TA, NX | Lateral discovery | **Should** | Cheap to build once the tree exists; drives page views | B |
| L4 | H1 title in plain pattern "{List type} in {Place}" | TA, YP, NX, WP ("List of"), GR | Match search wording, say what the page is | **Must** | One sentence, same pattern everywhere | S |
| L5 | Scale tag (hyper-local / city / national / global) | None (AllLists-specific, see section 5) | Tell reader the list's natural scale | **Should** | C25; helps explain why a list is short or long | B |
| L6 | Description with scope and inclusion criteria | WP (required lead), GR (list description), TA (B) | Say what is on the list and what is excluded | **Must** | Needed so contributors know what to add and buyers know what they are buying | S |
| L7 | Result count (total entries, and count shown) | ZD, ZM, YP, JD, TA, GR (books and voters) | Set expectation, show size | **Must** | Also the first roll-up statistic | S |
| L8 | Roll-up statistics block (counts by verification level, by sub-area, by speciality; share with phone, share with price; median price band) | G2 Grid (quadrants), GR (voters), ZM area guides (B), TA rank-of-M | Decision aid; the E14 "statistics about the whole list" | **Must** | Decided (E14); also the main hook that cannot be copied from the free names | S |
| L9 | Freshness: "last updated" and "last verified" for the list and a freshness mix (share verified in last 12 months) | WP ("last edited" B), GR (re-scored about every 5 min) | Let readers judge staleness, the main failure of directories | **Must** | Cheap, text only; nobody in the sample puts a freshness mix on list pages, so it differentiates | S |
| L10 | Filters: sub-area, category, speciality, price band, verification level, open now, rating, accepts X | TA (cuisine, price, meal, rating, reservation, Travellers' Choice), ZD (insurance, language, gender, availability), PF/PakWheels (prior 05), YP | Narrow results | **Must** (sub-area, category, verification level, price band) / **Should** (rest) | Verification-level filter is a trust lever; others depend on list type | S |
| L11 | Sort options (relevance, rating, most reviewed, nearest, name A-Z, recently verified, price) | PR (relevance algorithm), ZD, TA (Popularity Index), GR (score), G2 | Order results | **Must** (name A-Z, recently verified, default "ranked") / **Should** (rest) | Paid ranking must be a separate, labelled slot, not hidden in the sort (open decision Q-N2) | S |
| L12 | "How this list is ordered" note | TA (Popularity Index explained), ZD (how search works), G2 (AI-instructions page), PR | Disclose ranking basis | **Must** | Needed once paid rank exists; keeps trust and meets ad-labelling norms | S |
| L13 | Result card (compact entry: name, category, area, verification chip, rating, price band, one action) | All | Scannable row | **Must** | See entry card rows E1 to E12 for which fields | S |
| L14 | Names-only preview rows for free users with locked-detail marker | None found as exact model (WP/GR show all; Apollo/ZoomInfo gate contacts, prior note 05) | Show value without giving away the paid list | **Must** | Decided (E14, CP3, P15) | B |
| L15 | Pagination or "load more" with a stated limit | TA, YP, ZM (paged); GR (tabs) | Control volume and scraping | **Must** | Limit per account is a decided mitigation (P15) | B |
| L16 | Map of results (list/map toggle, pins) | GM, TA, AB, ZM, BK, JD | Spatial browsing | **Later** | Text and numbers only (C29); a text "areas below" table does the job now | B |
| L17 | Featured or sponsored slot(s), clearly labelled, capped in number | GM (Sponsored/Ads), YP (sponsored result), PH (PROMOTED), G2/Capterra (paid placement), TA (paid mixed in) | Revenue | **Should** | Slot design now so labels exist; paid ranking is City level first (Q-N2); sale not in prototype | S |
| L18 | Display ads for free users, none for subscribers | YP, PH, WP none | Revenue | **Should** | Decided (CP5); keep slots empty or house text in prototype | S |
| L19 | Sub-list navigation: child areas with counts ("Adyala Road 14, Bahria Town 52") | NX (neighbourhood), ZM (area pages), TA (neighbourhoods) | Drill down and show roll-up | **Must** | Roll-up is core (C12); this is how a city page leads to area pages | S |
| L20 | Related lists: same place other types; same type neighbouring places; parent roll-up | WP ("See also"), TA, GR (similar lists, B), NX | Discovery, internal links | **Should** | Low cost; seeds cross-selling later | B |
| L21 | Add-an-entry / suggest-an-area prompt | GM ("add your business"), TA (add business, B), GR (add books) | Contributor supply | **Must** | Contributors are the supply (C13) | S |
| L22 | Claim-your-business prompt ("Is this your business?") | GM, YP, TA, JD, Doximity stubs (prior 04) | Owner verification, monetisation path | **Must** | Owner-verified level depends on it (D19) | S |
| L23 | Save/follow list and alerts when list changes | GM (lists), PH (collections), GR (Like), AB wishlist, ZM saved search (B) | Return visits | **Should** | Needs account; alert-by-email can wait | S |
| L24 | Share (link, WhatsApp text) | GM (share by link), Amazon lists (prior 06), AB | Distribution; WhatsApp is the main channel in the target markets | **Should** | Plain share links cost nothing | S |
| L25 | Report list (wrong scope, abuse, duplicate) | GM (Report a problem), ZM (Report ad, B), GR (B) | Quality and compliance | **Must** | Needed for takedown path (DSA Art 16 style notice; section 4) | S |
| L26 | Voting or ranking by users | GR, PH, AN, Ranker (prior 06) | Community ordering | **Later** | Reviewer rankings are an open decision (Q-P3) and vote-ranking conflicts with paid ranking | S |
| L27 | Contributors panel (top contributors, count, levels) | GR ("people who voted"), WP (history, B), HZ-type awards | Credit; retention (CP9) | **Should** | Decided non-cash reward is visible credit | S |
| L28 | Stewardship panel (who maintains this segment, how to apply, how to dispute) | WP (talk page, B), none among commercial sites | Governance | **Should** | C20 open details: show "steward: none, apply" or name | B |
| L29 | Data sources, licence and methodology note (including how verification works) | WP (references per item), G2 (how reviews are authenticated), TA transparency report | Defensibility; trust | **Must** | D17: source, licence, date, consent per record; list-level summary is needed | S |
| L30 | Disclaimer (listing accuracy, no endorsement) | ZM (disclaims responsibility for user ads), BK | Legal | **Must** | Cheap; counsel to word it | S |
| L31 | Editorial or award marks on list rows ("Top rated", "Travellers' Choice") | TA, YP Top 100, HZ Best of | Quality signal | **Later** | Needs enough reviews to be meaningful | S |
| L32 | Compare entries side by side | G2, AL, PR (B) | Decision aid | **Later** | Not needed to test usefulness | B |
| L33 | Language and currency switch (English/Urdu, PKR/USD) | LI, AL, BK, DF (country sites) | Reach | **Should** | Names and addresses in Urdu script are key (entry_attributes file); full translation later | B |
| L34 | Paywall / upgrade panel stating exactly what is unlocked | PR (SaaS side), Apollo-type (prior 05) | Conversion | **Must** | Free preview needs an explicit boundary (E14); text only | B |
| L35 | Empty-state page ("No entries yet; be the first; claim steward role") | None (AllLists-specific) | Every list type exists empty in every place (C11) | **Must** | Most pages will be empty at launch; the empty state is the contributor funnel | B |
| L36 | Structured data (not visible): ItemList plus LocalBusiness or Organization per item, BreadcrumbList | Google guidance: carousels need a summary page with some information about every entity, linking to detail pages (S, https://developers.google.com/search/docs/appearance/structured-data/carousels-beta); LocalBusiness (S, https://developers.google.com/search/docs/data-types/local-business) | Search visibility | **Should** | Free traffic; but check that names-only previews still qualify as visible content for markup (open question, section 7) | S |
| L37 | Export / download | Apollo, ZoomInfo sell lists (prior 05); WP data dumps (B) | Product for buyers | **Later** | Decided: no download except about USD 1,000 (E13); outreach button replaces it | S |
| L38 | Result-page "report an ad" link | EU DSA ad rules (section 4) | Compliance | **Later** | Only when ads are sold | S |

---

## 3. Master table of ENTRY components

"Card" = shown on a list row; "Page" = shown only on the entry page. Contact items follow the decision that contacts stay hidden and the buyer uses the outreach button (E13); for individuals, area only (Q-S2).

| # | Component | Platforms showing it | Purpose | AllLists prototype | Reason | Ev |
|---|---|---|---|---|---|---|
| E1 | Name (display name; legal name and alternate spellings on page) | All | Identity; Urdu/English variants | **Must** | Search by many spellings (entry_attributes file) | S |
| E2 | Category (primary) and secondary tags | GM (1 + up to 9, prior 01), YP, JD, TA | Classify; drives which fields appear | **Must** | One primary category per entry selects the field template (C26) | S |
| E3 | Entity type (business, facility, person, institution) | FB Pages types (prior 01), NPI (prior entry file) | Different rules per type | **Must** | Individuals carry privacy rules (Q-S2) | S |
| E4 | Verification badge(s) with level, by whom, date, and a click-through explanation | IM (TrustSEAL certificate page), AL (verified supplier), PR (registration verified), ZM (check mark), LI (click shows type), G2 (labels), PF/BY (verification status) | Trust | **Must** | Decided: four levels with who, how, when, evidence (D19, D20); see section 5 | S |
| E5 | Per-field verification flags (identity, location, licence, hours, prices) | IM (certificate lists fields checked), entry_attributes file proposal | Stop a verified name from lending credibility to stale prices | **Should** | Cheap if stored; display as small text | S |
| E6 | "Claimed" / "Claim this business" state | GM, YP, TA, JD, Doximity stubs | Owner path, monetisation | **Must** | Needed for owner-verified (D19) | S |
| E7 | Status (open, temporarily closed, permanently closed, moved) | GM, YP, TA | Avoid wasted trips | **Must** | Closed entries are the commonest complaint about directories (B) | B |
| E8 | Rating and review count (reviewer rankings) | GM, JD, YP, TA, PR, ZD, G2, AB, BK, LI recommendations | Decision aid | **Should** | Reviewer rankings are a decided field (C17) but who writes them is open (Q-P3); show "no rankings yet" until the rule is set | S |
| E9 | Review authenticity statement ("verified users only, one per user, how checked") | ZD (verified patient rule), G2 (validation, labels), BK (post-booking only), TA (transparency report), EU Omnibus duty to say whether verified | Honesty and law | **Must** (if any review shown) | Required statement in EU and good practice anywhere; text only | S |
| E10 | Owner reply to reviews; response rate/time | GM, YP, TA, PF (WhatsApp response time) | Fairness, trust | **Later** | Needs reviews first | S |
| E11 | Address (structured, with area hierarchy links); exact vs area-only | GM, all directories; AB (approximate until booking) | Where | **Must** | Place is the organising principle; individuals area-only | S |
| E12 | Service area / areas served | UC (micro-locality), NX, TT, schema.org areaServed (S, entry_attributes) | Mobile providers | **Must** (trades, tutors) | Core for skill lists (C22) | S |
| E13 | Map and directions | GM, all | Navigate | **Later** | Text and numbers only; show coordinates and landmark text now | B |
| E14 | Phone | GM, JD, YP, ZM | Contact | **Must (as hidden field)** | Stored but not shown; replaced by outreach button for the free view (E13) | S |
| E15 | WhatsApp | PF (response time), ZM (B), JD (B) | Main channel in PK | **Must (as hidden field)** | Same rule; also drives first outreach channel (Q-N5) | S |
| E16 | Website and social links | GM, YP, TA, FB | Verify and research | **Should** | Showing the website link leaks contact; show domain only on paid view; decide with counsel | B |
| E17 | Email | GM (B), B2B (IM, AL) | Contact | **Must (as hidden field)** | Hidden, relay only | B |
| E18 | Outreach / "Contact via AllLists" button | IM ("Contact supplier"), AL ("Contact supplier", "Chat now"), JD ("Send enquiry"), YP ("Request a quote"), ZM (call/WhatsApp buttons), TT (request quote, B) | Lead action without exposing contacts | **Must** | Decided (E13): buyer picks an outreach method; platform delivers; contacts hidden | S |
| E19 | Request-a-quote form (what, when, budget) | YP, TT, Bark, IM, AL | Structured demand | **Should** | Adds value for trade and B2B lists; can follow the plain outreach button | S |
| E20 | Opening hours (weekly, holidays, 24x7, appointment only) and last-confirmed date | GM, YP, TA | Practicality | **Must** (retail, health) | Basic; add "confirmed on" date | S |
| E21 | Price band ($ to $$$$ or local tier) | YP, TA, GM, schema.org priceRange | Cost filter | **Should** | One field; cheap | S |
| E22 | Services and prices table (item, price, unit, currency, price date) | UC (fixed catalogue), PR (consult fee), Fiverr (packages), MDSave/1mg (test prices, prior 04), TaskRabbit (hourly rate), AL (tier table) | Compare and buy | **Must** for priced lists (MRI, plumbers, tutors) | C21 decided; price date is essential; health rules before any price (Q-S1) | S |
| E23 | Specialities / treatments / products carried / equipment list | PR (surgeries and treatments), HZ, CL (focus %), MRI centres (prior 04) | Match query | **Must** | Type-specific block (C26) | S |
| E24 | Registrations, licences and certifications with number, issuer and validity, linking to the register | PR (medical registration), IM (GSTIN, IEC), HZ (verified licence), CT (up to 12 checks), AL (certificates) | Strongest trust fact | **Must** (regulated types) | D21: sources are registers; PMDC, PEC, PHC lookups (prior notes) | S |
| E25 | Description / about (150 to 600 characters) | All | Explain | **Must** | Cheap | S |
| E26 | Qualifications, experience years, languages, gender (individuals) | PR, MH, DF, Care.com, Superprof (prior 03, 04) | Choose a person | **Should** | Only with consent for named individuals (Q-S2) | S |
| E27 | Year established; staff size; branches/parent link | CL, AL, IM, GM (chains) | Maturity; dedupe | **Should** | Chain and branch links keep the list clean | S |
| E28 | Payment methods accepted | GM attributes (S, entry_attributes) | Practical | **Later** | Low value for test | S |
| E29 | Attributes: amenities, accessibility, service options (home visit, delivery) | GM | Filters | **Later** | Add per list type after template review | S |
| E30 | Photos, logo, video | All | Conversion | **Later (excluded)** | Decided: no pictures or videos (C29) | S |
| E31 | Reviews list (text, reviewer pseudonym, date, verified label) | GM, YP, TA, G2, ZD, BK | Evidence | **Later** | Depends on Q-P3 | S |
| E32 | Q&A | GM (owner label), AB | Pre-sale questions | **Later** | Moderation cost; UNVERIFIED if GM still runs it | S |
| E33 | Save entry (to a private or shared list) | GM, AB, TT, PH, LinkedIn | Shortlist | **Should** | Fits "personal lists private by default" (seed set) | S |
| E34 | Share entry | GM, ZM, AB | Distribution | **Should** | Share link without contact | S |
| E35 | Report entry (closed, wrong, duplicate, fake, remove my data) | GM (Suggest an edit/Report a problem), ZM (Report ad, B), TA (B) | Quality, legal | **Must** | A takedown path is both a trust and a legal component (section 4) | S |
| E36 | Suggest an edit (any signed-in user) | GM, TA, WP | Crowd maintenance | **Must** | Draft-first data (D18): corrections must be easy | S |
| E37 | Similar / nearby entries in the same list | GM ("People also search"), TA, ZM, Houzz, LI "People also viewed" (B) | Keep users in the product | **Should** | Same-list neighbours at least | B |
| E38 | Other lists this entry appears in (doctors at this hospital, shops in this market) | none directly; schema graph (S, entry_attributes: "graph of lists") | Navigate the list graph | **Should** | AllLists-specific; builds roll-up logic | S |
| E39 | Rank in list ("#3 of 41 eye hospitals in Rawalpindi") | TA ("#N of M") (B), PR badges | Quick context | **Should** | Uses the roll-up count; must say how ranked | B |
| E40 | Last updated and last verified dates | WP (B), GM (hours date, B), NPPES last-update dates (S, entry_attributes) | Staleness | **Must** | D17 and freshness fields | S |
| E41 | Source and licence line ("Source: PMDC register, 2026-09-12") | WP (references), IM (certificate), NPPES (S) | Provenance; defensibility | **Must** | Decided (D17) | S |
| E42 | Change history (who, when, what) | WP (history, B), entry_attributes proposal | Dispute handling | **Should** | Stored always, shown simply as last 3 changes | S |
| E43 | Contributor credit ("Added by", "Verified by", level) | PH (makers), GR (creator), WP (history) | Reward (CP9) | **Must** | Decided visible credit; show pseudonym or chosen name | S |
| E44 | Steward / owner of segment | none in commercial sites | Governance | **Should** | C20; open details | B |
| E45 | Sponsored / featured marker and plan tier | GM, YP, PH, TA, JD (Platinum/Gold/Silver, S prior 01) | Revenue and disclosure | **Should** | Label wording ours; separate from verification | S |
| E46 | Consent and takedown status (for individuals: "listed with consent on date") | none public; NPPES holds takedown fields (B) | Legal basis | **Must** (individuals) | D17 consent status; shows only as "consented" tick | B |
| E47 | Privacy and opt-out link on every entry | JD (email privacy route, S third-party), GM (remove content, B) | Rights | **Must** | No charge to remove personal data (P17) | S |
| E48 | Disclaimer line (data accuracy; not an endorsement) | ZM (S) | Legal | **Must** | Same as L30 | S |
| E49 | Registry identifiers (reg no., GSTIN/NTN, PEC category, NPI-type) | IM, PR, HZ, NPPES | Entity matching | **Should** (shown as number + link) | Never show CNIC; store fact not number (entry_attributes) | S |
| E50 | Availability / next slot / accepting new clients | ZD (real-time openings), PR | Convert | **Later** | Needs integrations | S |
| E51 | Type-specific blocks (doctor, MRI services, contractor, tutor, manufacturer) | PR, ZD, UC, AL, IM | Complete template | **Must** (one or two types) | Prototype tests two types fully (suggest eye hospitals and a trade) | S |
| E52 | Structured data: LocalBusiness / Organization / Person with openingHours, geo, areaServed, priceRange | schema.org + Google (S, https://developers.google.com/search/docs/data-types/local-business) | Search visibility | **Should** | Only for what is publicly shown | S |
| E53 | Breadcrumb at top of entry (place > list > entry) | TA, GM (B) | Navigation | **Must** | Cheap | B |
| E54 | Safeguarding indicator (child-facing tutors: police check status, relay-only contact) | Care.com background check (prior 03), UC | Safety | **Later** | Decided not public until safeguarding designed (Q-S2) | S |
| E55 | Contact preference (via platform only; hours to contact) | Nextdoor (B), PF (WhatsApp response time) | Manage expectations | **Should** | Pair with outreach button | S |

---

## 4. Trust and compliance components

### 4.1 What badges mean on comparable platforms (use to word our own)

| Platform | Badge or label | What it claims | Who checks and how | Paid? | Source (all 2026-10-05; page dates unknown unless stated) |
|---|---|---|---|---|---|
| IndiaMART | TrustSEAL | Legal status, existence; certificate lists Director/Proprietor, GSTIN, address, IEC | IndiaMART staff or agents (method not stated) | Paid product (B) | https://trustseal.indiamart.com/members/arihant-crystal ; https://export.indiamart.com/ |
| IndiaMART | GST verified | GSTIN valid, registered business | Tax-portal lookup (B) | n/a | same export page |
| Alibaba | Verified Supplier | Documents checked online plus on-site inspection | Outside firms (SGS, TUV Rheinland, Intertek) | Supplier pays (B) | https://www.cosmosourcing.com/blog/what-are-alibaba-verified-suppliers ; https://www.intertek.com/news/2010/11-16-audit-services-alibaba/ (2010) |
| Alibaba | Trade Assurance | Payment held in escrow until receipt | Platform | n/a | same cosmosourcing page |
| Practo / Marham | Medical Registration Verified / PMDC Verified | Doctor appears on the regulator's register | Platform lookup (B) | n/a | practo.com doctor pages; prior note 04 |
| Zocdoc | Verified patient (review) | Reviewer booked and attended | Booking system | n/a | https://thepapergown.zocdoc.com/facts/verified-reviews-real-patients/ |
| G2 | Validated Reviewer; Verified Current User; Business Partner | Identity validated; screenshot shows use; conflict of interest flagged and not scored | G2 moderators | n/a | https://sell.g2.com/review-validity |
| LinkedIn | Verification checkmark | Identity, workplace or school; click to see which | ID vendors, work email code | Free, never sold | https://www.linkedin.com/help/linkedin/answer/a1492056 |
| Zameen | Blue or green check | Property physically exists | Zameen team (B) | Reserve button B | https://www.zameen.com/blog/common-property-frauds-to-avoid.html |
| Property Finder / Bayut | Verification status; Super agent; TruCheck; TruBroker | Listing and agent verified; performance tier | Platform (prior note 05) | Partly paid (UNVERIFIED) | prior note 05 |
| Google Local Services | Google Verified / Google Screened | Business checks done (home; business categories) | Google | Pay-per-lead | prior note 01 |
| Houzz | Verified licence | Licence number matched in participating US states | Houzz | n/a | prior note 03 |
| Checkatrade | Vetted (up to 12 checks) | Identity, qualifications, credit, insurance, references | Checkatrade | Membership | prior note 03 |
| Healthgrades | Hospital rating badge | Procedure-outcome rating | Healthgrades; hospitals must contract to use the badge in ads | Yes | prior note 04 (conflict of interest) |
| Tripadvisor | Travellers' Choice | Top 10 percent by quality, quantity, recency | Algorithm | No | https://www.hospitalitynet.org/news/4120110.html |
| Booking.com | Verified review | Guest booked and stayed | Booking system | n/a | https://www.booking.com/reviews.html |
| Yelp | Paid verification badge (select categories) | Licence and insurance check | Yelp | Annual fee | Low-quality source only: UNVERIFIED |
| Justdial | "Verified" flag | NOT FOUND | NOT FOUND | NOT FOUND | field exists per https://apify.com/themineworks/justdial-business |

Pattern to copy: every strong badge says what was checked, by whom and, ideally, links to the evidence (IndiaMART certificate, LinkedIn click-through, G2 label definitions). Pattern to avoid: a single unexplained tick (Justdial, Yelp) or a badge the rated party can buy (Healthgrades hospital badges, Yelp paid badge, Houzz paid plans).

### 4.2 Legal and policy anchors (for counsel, not legal advice)

| Topic | Component it drives | Source and date | Note |
|---|---|---|---|
| Fake reviews | Review authenticity statement; ban on paid or fake reviews; moderation | US FTC final rule, 16 CFR Part 465, effective 21 Oct 2024 (https://www.govinfo.gov/content/pkg/FR-2024-08-22/html/2024-18519.htm) | Covers AI-generated reviews, paid reviews, insiders without disclosure, review suppression; civil penalties |
| Review verification disclosure | "Reviews are from verified users" statement | EU Omnibus Directive 2019/2161, applied from 28 May 2022 (https://business.trustedshops.com/blog/eu-omnibus-directive-new-regulations-how-they-affect-you, secondary) | Must say whether and how reviews are checked; applies where EU consumers are served; UNVERIFIED for us |
| Notice and action | Report buttons (L25, E35) with confirmation of receipt | EU DSA Article 16 (https://prighter.com/resources/laws/dsa/quick-access) | Low-threshold electronic mechanism; applicability depends on service type |
| Ad labelling | "Sponsored" labels (L17, E45) incl. who paid | EU DSA Article 26 (same) | Also the norm on every platform in section 1 |
| Trader traceability | Business name, address, phone, email visible for traders on marketplaces | EU DSA Article 30 (same) | Conflicts with our hidden-contact rule if AllLists becomes a "marketplace" where traders contract with consumers; legal review needed before launch in EU |
| Personal data | Consent status, opt-out, no CNIC, area-only for individuals | Pakistan has no enacted general data protection law as of May 2026 (draft bill 2025; PECA 2016 applies) per `Service provider sources/pakistan_registries_and_bodies.md`; Justdial routes removal through privacy@ (https://www.offlist.me/justdial-removal, third-party) | Decided: no charge to remove data (P17) |
| Authenticity claims | Do not claim "guaranteed authentic" | UK ad regulator against Tripadvisor (https://www.pinsentmasons.com/out-law/news/tripadvisor-authenticity-claims-misleading-and-unsubstantiated-ad-watchdog-rules, about 2011 to 2012) | Say "checked by X on date", not "100 percent genuine" |
| Transparency | Yearly numbers of removed content | Tripadvisor Transparency Report 2025 (https://www.hospitalitynet.org/news/4126305.html, March 2025) | Later, but log the data from day one |
| Structured data | Mark-up must match visible content | Google structured data guidelines (https://developers.google.com/search/docs/data-types/local-business) | Check for hidden/paywalled content rules (gap) |

---

## 5. Components unique to AllLists (from `docs/DECISIONS.md`)

None of the 16 platforms combine these; each has partial precedents shown in brackets.

### 5.1 Verification levels (D19, D20): who, how, when, evidence

Decided: four levels on every entry, with who, how, when and evidence stored. Requirements, durations and who pays surveyors are open (Q-P7, settle in the 1,000-record pilot), so the cells marked (proposal) are my suggestions, not decisions. Show levels as independent chips, not a single ladder: an entry can be both AI-checked and owner-verified, and "surveyor-verified" is not automatically "better" than "owner-verified" (it checks something different).

| Level (decided) | Who (proposal) | How (proposal) | When and expiry (proposal) | Evidence stored (proposal; text and numbers) | Public wording (proposal) | Precedent |
|---|---|---|---|---|---|---|
| Not verified yet | Nobody; imported or contributed draft | Source recorded only | n/a | source, licence, retrieval date, contributor id | "Not verified yet. Source: X" | Doximity stub (prior 04) |
| AI-checked | AllLists agent | Cross-checks at least two independent sources: register match, website or phone liveness, address geocode; records confidence | On creation and every 6 to 12 months; expires and drops to "not verified yet" if not rechecked | source URLs, fields matched, confidence score, check date, agent version | "Checked by AllLists AI on date against N sources" | IM (fields listed), GM auto checks (B) |
| Owner-verified | The owner or authorised manager | Claim with OTP to a phone or WhatsApp number, plus optional document upload reviewed by staff; owner confirms fields | At claim; re-confirm yearly | claimant identity and role, OTP time, document type and reviewer, fields confirmed | "Confirmed by the owner on date" | GM claim-and-verify, LI click-through (S) |
| Surveyor-verified | A named volunteer or paid surveyor who is not the owner | Field visit or call with a checklist; geo-coordinates and timestamp; mystery-call for prices | At visit; expires after 12 months (UNVERIFIED target) | surveyor id, method (visit/call), coordinates, timestamp, checklist values, notes; photo evidence is excluded at this stage (C29): decide if evidence photos may be kept internally | "Visited/called by surveyor on date" | Alibaba on-site (S), Checkatrade checks (S) |
| Per-field flags (extra) | as above | which of name, address, phone, hours, prices, licence were confirmed | per field | field list and dates | small text under facts | IM certificate (S) |

Open point that changes the list page: a "not verified yet" entry is, by default, visible only to owners and moderators (Q-P6 suggested default). Then the list page's count and roll-ups must say "N published, M awaiting verification (not shown)", or the numbers and rows will not agree.

### 5.2 Roll-up statistics (C12, E14)
- Components: total entries below this place; count by verification level; count by child area (table); share with price; share verified in last 12 months; median price band for priced lists; top specialities. (Precedents: TA "#N of M", G2 Grid, GR voters count.)
- Shown at every level; city and above are paid in the working reading of CP3/CP4, so the prototype needs an "unlocked / locked" flag per statistic.
- Component the others lack: "what is in the parent that is not in this list" (e.g. 52 in Bahria Town, 310 in Rawalpindi).

### 5.3 Names-only preview for free users (E14, CP3, P15)
- Rows show: name, category, area, verification chip, rank position. Hidden: phone, WhatsApp, email, website, address detail, prices, specialities detail.
- A visible lock marker per hidden field group, a count ("43 more with details") and an explicit upgrade panel (L34). Per-account daily limit and anti-bot checks are decided mitigations.
- Ambiguity to resolve (owner's wording was ambiguous, DECISIONS section 6): "first few entries plus statistics" versus "small segments free with names only". Layout must support both: first N rows full-name, rest as count.

### 5.4 Outreach button instead of showing contacts (E13)
- One primary button "Contact through AllLists" on each entry and, for buyers of a segment, "Reach everyone in this list" with a choice of channel (WhatsApp first, opt-in, platform-sent; Q-N5 default). Contacts are never shown. Precedents: IM/AL "Contact supplier", JD "Send enquiry", YP "Request a quote" (S, section 1).
- Components around it: channel picker, message template with character count, estimated recipient count, consent/opt-in state of recipients, send log, opt-out link in every message. Counsel first (DECISIONS section 9).

### 5.5 Contributor credit (CP1, CP9)
- On list: contributors panel (count, top names, levels). On entry: "Added by", "Last verified by". Credit is the non-cash reward and CV certificate evidence. Need: choice of display name, pseudonym option, correction if credited wrongly. Do not show payout shares (F2 steps 50/40/30 are internal).

### 5.6 Stewardship (C20, Q-P2 suggested default)
- Revocable stewardship of a segment (e.g. a society or road): shown as "Steward: name or none"; "Apply to steward"; review queue; dispute link; no fee, no recruitment commission. Steward can correct entries and approve edits but does not hide competitors (to be written as a rule). Precedent: Wikipedia talk and history (B), none among commercial directories.

### 5.7 Other AllLists-only components implied by decisions
- Empty-list state in every place (C11).
- Scale tag and "this list also exists in N places" link (C11, C25).
- Topic-list variant (apps, books, tools) with topic breadcrumb instead of place breadcrumb and sponsorship/affiliate labels (C27).
- Private personal lists (seed set): owner-only banner, never indexed.
- Source, licence, date and consent status per record (D17), including list-level summary.
- Free users see ads, subscribers none (CP5): ad slot that disappears when signed in as subscriber.
- Paid ranking separate from verification and from reviewer ranking (suggested for Q-P3/Q-N2).
- Price date on every price, and the health rules before any health price (Q-S1).

---

## 6. Proposed layout order (top to bottom, text and numbers only)

### 6.1 LIST page (e.g. "Eye hospitals in Rawalpindi")
1. Global strip: site name, search, language, sign-in / plan indicator.
2. Place breadcrumb (Global > Pakistan > Punjab > Rawalpindi), then list-type path (Health > Hospitals > Eye hospitals). L1, L2.
3. H1: "{List type} in {Place}" and one-line sub-title with scale tag. L4, L5.
4. Summary line: "N listed, M verified, last updated date". L7, L9.
5. Action row: Save/follow, Share, Reach this list (outreach), Report list. L23 to L25, 5.4.
6. Description with scope and inclusion criteria, and one line on how verification works. L6, L29.
7. Roll-up statistics block (table of numbers; locked items marked). L8, 5.2.
8. Sub-areas table with counts (links to area lists). L19.
9. Filter and sort bar (sub-area, category, verification level, price band; sort A-Z, recently verified, ranked) plus "how ordered" link. L10 to L12.
10. Sponsored slot (labelled, at most 1 to 2, only when sold). L17.
11. Result rows (names-only for free users; full for subscribers), with verification chip and one action per row. L13, L14.
12. Pagination or limit notice; upgrade panel listing exactly what unlocks. L15, L34.
13. Contribute: add an entry, suggest an area, "Is this yours? Claim it". L21, L22.
14. Related lists and parent roll-up links. L20.
15. Contributors and steward panels. L27, L28.
16. Provenance: sources, licence, methodology, change log link; disclaimer. L29, L30.
17. Footer: report, privacy and opt-out, ad disclosure, terms. (Ad slot for free users sits between 11 and 12 and in the footer, labelled.)
18. Invisible: structured data (ItemList, BreadcrumbList). L36.
Empty-list variant: steps 2 to 6, then an empty-state panel (L35) that replaces 7 to 12.

### 6.2 ENTRY page (e.g. one eye hospital)
1. Breadcrumb: place > list > entry. E53.
2. Name (with alternate spellings), category, entity type, status. E1 to E3, E7.
3. Trust strip: verification chips with level, who, date (click for what was checked), claimed state, "last updated". E4, E6, E40.
4. Primary action row: Contact through AllLists (outreach), Request a quote (if type allows), Save, Share, Report. E18, E19, E33 to E35.
5. Key facts block: area and address (area-only for individuals), service area, hours with confirmed date, price band. E11, E12, E20, E21. Hidden-field markers where the viewer's plan does not unlock.
6. About: description, specialities, languages, year established, staff band. E25 to E27.
7. Type-specific block: e.g. facility type, departments, equipment, emergency, panels; or trade licence and warranty. E23, E51.
8. Services and prices table with price date. E22.
9. Registrations and certifications with numbers and register links. E24, E49.
10. Ratings and reviews block: rating, count, authenticity statement; "no rankings yet" until rules exist. E8, E9. (Reviews list and owner replies later: E10, E31.)
11. Rank in list and similar entries; other lists this entry belongs to. E37 to E39.
12. Provenance: source, licence, retrieval date, change history (last 3), contributor and steward credit. E41 to E44.
13. Claim and correct: "Is this yours? Claim", "Suggest an edit". E6, E36.
14. Legal footer: disclaimer, privacy and opt-out, report, consent status for individuals. E46 to E48.
15. Invisible: structured data for what is publicly shown. E52.

---

## 7. Gaps, conflicts and next steps

1. Direct page reading failed for every platform (egress proxy) and the search budget ended early. Priority checks: Justdial badge meanings; Yelp's own help pages on recommended reviews, claimed and paid badges; Airbnb and Booking listing anatomy; Product Hunt; Goodreads report/tags; whether Google Maps Q&A still exists in 2026; Wikipedia list tool links. Suggested fix: the 2-hour screenshot audit in section 0.
2. Unverified or low-quality sources used: lovable.app Yelp pages, scraper pages (Apify), secondary SEO blogs (socialbee, cosmosourcing, podium). They support the existence of a component but not its exact wording; wording must be taken from live pages.
3. Conflict on ad label wording at Google ("Sponsored" vs "Ads"): both reported, undated. We choose our own wording and keep it consistent.
4. Paywall versus search visibility: names-only previews are central to the model (E14, P15) but structured data and indexing rules for gated content (Google paywalled-content guidance, B) were not researched. Risk: markup that describes content the visitor cannot see.
5. DSA Article 30 trader traceability asks marketplaces to publish trader contact details, which conflicts with our hidden-contact rule if AllLists is judged a marketplace in the EU. Not researched further: counsel question.
6. Review rules (who writes, one per user, anti-fake) are open (Q-P3). The review components E8 to E10, E31 are specified only as slots.
7. Mobile-first layout, accessibility (screen readers, Urdu right-to-left layout), page speed on low-end phones and data cost were not covered; for Pakistan these matter more than any component above.
8. Not covered in depth: list-page anatomy of Foursquare, NHS service search, Rightmove, PakWheels, Daraz seller pages, Marham list pages (names only in notes), and admin-side components (claim flow screens, moderation queue, steward console). The prototype also needs these if owners and stewards are tested.
9. Numbers in section 1 (e.g. Booking.com 370 million reviews, Tripadvisor 2.7 million fraudulent reviews) are from snippets of vendor or press pages; do not publish without opening the source.
10. Naming: "verified" is used by every platform for different checks. Decide whether AllLists uses the word at all or only the four decided labels with date and method.
