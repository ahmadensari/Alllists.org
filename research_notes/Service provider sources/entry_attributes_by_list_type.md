# Entry attributes by list type: a complete entry template per AllLists list type (research as of 2026-10-05)

## Method note and honesty statement (read first)

- Only three web searches succeeded in this session (schema.org LocalBusiness properties; Google Business Profile attributes; NPPES/NPI fields). The session's WebSearch budget (200 calls) was then exhausted, and every WebFetch attempt (schema.org, support.google.com) returned EGRESS_BLOCKED. No page for Practo, Zocdoc, Justdial, Yelp, Yellow Pages, Urban Company, Angi, Thumbtack, TaskRabbit, PEC, IndiaMART, Alibaba, ORCID, Kaggle or any school/tutor platform was opened or searched in this session.
- Therefore: sections marked "Source-backed" rest on search snippets (cited with URLs). Everything else is an INFERENCE from general knowledge of how these platforms and registers work, and is labelled [INFERENCE] or [UNVERIFIED]. Treat it as a hypothesis list to check against live listings (open 5 real profiles per type and tick fields off) before freezing templates.
- No numeric figures are asserted from sources here except those quoted from earlier repo notes (flagged with the note's own caveat). Any other number is marked UNVERIFIED.
- Planning research, not legal advice. Pakistan context is drawn from existing repo notes (`pakistan_registries_and_bodies.md`), which were themselves built from search snippets.

### Source-backed findings (snippets only)
- schema.org LocalBusiness represents a physical business or branch, with properties including `openingHoursSpecification`, `geo` (GeoCoordinates), `areaServed`, `paymentAccepted`, `priceRange` and `currenciesAccepted` (ISO 4217). — [schema.org/LocalBusiness](https://schema.org/LocalBusiness) (via search summary; page itself blocked); [google.schema.org](https://google.schema.org/LocalBusiness)
- Google Business Profile: the primary category decides which attributes are available, whether reviews and Q&A are shown, whether primary hours show, and access to secondary hours, Posts and the product editor. Attribute groups: accessibility, from-the-business, amenities, health and safety, highlights, payments, service options (online appointments, onsite services, online estimates, pickup, delivery). Payments: cash-only, cheques, major card brands, debit, NFC mobile. — [Search Engine Journal GBP attributes guide](https://www.searchenginejournal.com/local-seo-gbp-attributes-guide/); [Synup](https://synpost.synup.com/google-business-profile-attributes/); [Local University](https://localu.org/selecting-your-primary-category-on-google-my-business-proceed-with-care/)
- NPPES/NPI registry: NPI number, name (individual or organisation), credential, primary specialty and taxonomy code, state licence number and issuing state paired with the taxonomy, gender (individuals), practice address with phone and fax, mailing address, authorised official (organisations), status, enumeration and last-update dates, other identifiers, other names, HIE endpoints. — [Gigasheet NPPES data dictionary](https://support.gigasheet.com/support/solutions/articles/69000877029-nppes-npi-data-dictionary-field-reference); [Snowflake NPPES data dictionary](https://data-docs.snowflake.com/foundations/sources/nppes/data-dictionary)
- Pakistan registry facts reused from the repo (snippet-level, see that note for caveats): PMDC online lookup by registration number/name/father's name shows licence validity and qualifications; PEC constructor categories C-A to C-6 with older cost limits; provincial healthcare commissions license facilities; Pakistan has no enacted comprehensive data protection law as of May 2026 (draft Personal Data Protection Bill 2025; PECA 2016 applies). — `/home/user/Alllists.org/research_notes/Service provider sources/pakistan_registries_and_bodies.md`

### Legend for tables
- Value: B = buyer value (helps a customer choose), T = trust value (helps believe the entry), M = matching/search value (filter or rank), S = SEO/structured-data value.
- Who can verify: Self (owner claims), Doc (document upload checked by us), Reg (official register lookup), Field (agent visit/call/mystery shopper), Peer (customer reviews/endorsements), Plat (external profile such as GitHub/ORCID/Google), Auto (automated check, e.g. phone OTP, URL liveness).
- Sens: L low (business data), M medium (could identify an individual), H high (personal, child-related, health or financial; hold only with explicit consent and access control).

---

## A. Common core (every entry, every list type)

| Field group | Fields | Why it matters | Verifier | Sens |
|---|---|---|---|---|
| Identity | entry_id (stable, never reused); entry_type (person / business / facility / institution); legal name; trading/display name; alternate names and transliterations (Urdu/Arabic/Hindi script, spelling variants); short tagline; description (plain text, 150-600 chars); founded year; owner/operator type (sole proprietor, partnership, company, trust, government, NGO); parent/brand/chain link; branch-of link | Dedupe, search recall (people search many spellings), schema.org Organization/Person mapping [INFERENCE] | Self, Reg | L (M if sole proprietor named) |
| Category | primary category (controlled vocabulary, one only); secondary categories (max about 5); services/keywords tags; list_type; taxonomy codes where one exists (NPI taxonomy, PEC category, HS code) | GBP shows the primary category drives attributes and features, so one primary + attribute sets per type is the proven pattern ([SEJ](https://www.searchenginejournal.com/local-seo-gbp-attributes-guide/)) | Self, Auto | L |
| Location | street address (structured: building/plot, street, locality, city, district, province/state, postcode, country ISO-3166); landmark/"near" text; geo coordinates (lat, long, precision flag: rooftop / street / area-centroid); Plus Code / what3words optional; area hierarchy IDs (country > province > district > city > locality/neighbourhood > sector/society/block); location_visibility (exact / area-only / hidden); service-at-premises flag (storefront vs home-based vs mobile); floor/unit; parking/access notes | schema.org `geo` and `areaServed`; place-based organisation is AllLists' core model; home-based providers need area-only display | Auto, Field | L for businesses; H for a home address of an individual (show area only) |
| Service area | areaServed (list of area-hierarchy IDs and/or radius km from base point); travel charge note; remote/online flag | schema.org `areaServed`; essential for trades, tutors, mobile services | Self | L |
| Contact channels | primary phone (E.164), phone type (landline / mobile / WhatsApp-enabled), WhatsApp number flag, email, website URL, social/profile URLs, booking URL, contact person name and role, preferred contact method and contact hours, contact_visibility (public / on request / via relay) | Buyer action path; relay numbers protect individuals | Auto (OTP/ping), Field | L for business lines; H for personal mobiles (see C) |
| Hours | weekly opening hours with multiple intervals per day; timezone; 24x7 flag; holiday/closure exceptions; "appointment only" flag; prayer-break / lunch-break notes; seasonal hours; last-confirmed date for hours | schema.org `openingHoursSpecification`; GBP primary and secondary hours | Self, Field | L |
| Verification | verification_level (0 unverified/scraped; 1 contact reached or phone OTP; 2 document/registry checked; 3 field-visited or mystery-shopped; 4 continuous/partner-attested); per-field verification flags (identity, location, licence, hours, prices); verified_by (method + actor); verified_date; expiry_date of the verification | Trust ladder; lets buyers filter by level; per-field flags stop a verified name from lending credibility to a stale price | Platform process | L |
| Source and provenance | source_type (owner-submitted, registry, public website, partner feed, crowd contribution, agent-collected, user-submitted); source_url; source_name; retrieval_date; licence/terms of the source; record_confidence score; contributor_id; change history (who, when, old/new) | Legal defensibility and dispute handling; repo legal notes show source terms drive risk | Auto | L |
| Consent and rights | listing basis (owner-consented / public-business-info / registry-public); consent timestamp and scope (what fields may be shown, shared, sold, used for ads); marketing-contact opt-in; takedown/opt-out flag and date; for individuals: age-of-majority confirmation; jurisdiction of data subject | Required where data protection law applies (EU/UK/India etc.); good practice even where Pakistan law is not yet enacted | Self (recorded) | M |
| Freshness | created_at; last_updated_at; last_verified_at; next_review_due; staleness status (fresh/aging/stale/closed) | Stale data is the main failure mode of directories [INFERENCE] | Auto | L |
| Status | operating status (open, temporarily closed, permanently closed, moved, not yet open); successor entry link; duplicate-of link | Prevents sending buyers to closed premises | Field, Peer | L |
| Media | logo; cover photo; gallery (storefront, interior, work samples); alt text; photo owner and licence; video link; photo date | Trust and conversion; images need clear licence | Self, Auto | L (M if faces; H if children/patients) |
| Reviews and reputation | rating average, review count, rating source (own vs imported with licence), review text with reviewer pseudonym, review verified-purchase/verified-contact flag, owner reply, complaint count, response rate/time | Core trust signal (Yelp, Google, Urban Company all centre on this [INFERENCE]); reviews are personal data of reviewers | Peer, Auto | M |
| Claim status | claim_state (unclaimed / claim pending / claimed / disputed); claimant identity, role and proof; claimed_date; plan tier (free/paid/featured); sponsored flag | GBP-style claim flow lets owners correct data and drives monetisation [INFERENCE from GBP model] | Doc, Auto | M |
| Languages and accessibility | languages spoken (ISO 639); wheelchair access, women-only/family seating, prayer facility, sign language (as relevant) | GBP accessibility attributes ([SEJ](https://www.searchenginejournal.com/local-seo-gbp-attributes-guide/)); local fit in Pakistan (language, gender access) [INFERENCE] | Self, Field | L |
| Pricing basics | price band ($ to $$$$ or local-currency tier); currency (ISO 4217); payment methods accepted (cash, card, bank transfer, mobile wallet such as JazzCash/Easypaisa [INFERENCE], cheque, cryptocurrency flag); invoice/receipt availability | schema.org `priceRange`, `paymentAccepted`, `currenciesAccepted`; GBP payment attributes | Self, Field | L |
| External identifiers | registry IDs (list typed ids below), Google Place ID (store only if licence allows), Wikidata/OSM IDs, GS1/GLN, tax IDs (see per-type) | Entity matching and verification; see Maps terms caution in the legal-limits note | Reg | L (M for sole proprietor tax IDs/CNIC; never store CNIC publicly) |

---

## B. Add-on field tables per list type

Notes: fields marked [UNVERIFIED] are my recollection of the platform pattern; nothing below was checked on the named platforms in this session except where a citation appears.

### 1. Generic local business (LocalBusiness, GBP, Yelp, Justdial, Yellow Pages)
Reference sets: schema.org LocalBusiness properties (hours, geo, areaServed, payment, price range); GBP attribute groups (accessibility, amenities, payments, service options); Yelp/Justdial/Yellow Pages style fields [UNVERIFIED].

| Field | Why it matters | Value | Verifier | Sens |
|---|---|---|---|---|
| Services/products list with short descriptions | Search match on "what do you do" | B, M | Self, Field | L |
| Brands carried / stocked | Brand-led search (retail, auto parts) | B, M | Self, Field | L |
| Service options (walk-in, appointment, delivery, pickup, online estimate, home visit) | GBP "service options" attribute | B | Self | L |
| Amenities (Wi-Fi, parking, AC, family area, prayer space, toilets) | GBP amenities | B | Self, Field | L |
| Highlights/specialities (free-text tags) | Differentiation | B | Self | L |
| Price band + sample prices/menu/catalogue link | schema.org `priceRange` | B | Self, Field | L |
| Business registration no. (SECP/NTN/STRN in Pakistan; GSTIN in India) | Legal existence check | T | Reg (SECP/FBR) | L for companies; M for sole proprietors |
| Years in business; staff size band | Maturity signal | T | Self | L |
| Certifications/licences (trade licence, food authority, fire safety) | Regulated trades | T | Doc, Reg | L |
| Delivery coverage and fees | Buyer planning | B | Self | L |
| FAQ/Q&A | GBP Q&A depends on category | B | Self | L |
| Special offers/posts with validity dates | Engagement, monetisation | B | Self | L |

### 2. Doctors and clinicians (Practo, Zocdoc, NPI, PMDC-style)
Reference: NPI fields (credential, taxonomy, licence + state, gender, practice address/phone, status dates) are source-backed; Practo/Zocdoc fields below are [UNVERIFIED].

| Field | Why it matters | Value | Verifier | Sens |
|---|---|---|---|---|
| Full name, title (Dr/Prof), photo | Identity; patients recognise faces | T | Reg, Self | M |
| Regulator and registration number (PMDC no.; NPI) | Primary legitimacy check; PMDC lookup shows licence validity and qualifications ([repo note](pakistan_registries_and_bodies.md)) | T | Reg | L (public register) |
| Licence status/validity/expiry | Expired licences are a safety issue | T | Reg | L |
| Qualifications with institution and year (MBBS, FCPS, MRCP, PhD) | Patient trust; PMDC tracks recognised PG programmes | T, B | Reg, Doc | L |
| Specialty and sub-specialty (taxonomy code) | Search by condition/specialty; NPI taxonomy | M | Reg, Doc | L |
| Conditions treated / procedures performed / interests | Matches patient queries | M, B | Self | L |
| Years of experience (derived from first registration) | Practo-style sort key [UNVERIFIED] | B | Reg-derived | L |
| Practice locations (each with hospital/clinic link, days/times, room/floor) | Doctors work at several sites; NPI holds practice location | B | Self, Field | L |
| Hospital affiliations/visiting privileges | Trust, referral | T | Facility confirm | L |
| Consultation fee (new, follow-up, online, home visit), currency, fee date | Strong buyer filter | B | Self, Field | L |
| Appointment mode (in-person, video, phone), booking link, walk-in vs appointment | Action path | B | Self | L |
| Availability: weekly slots, next available, accepting new patients | schema.org Physician has accepting-new-patients concept [UNVERIFIED]; Zocdoc-style | B | Self, Plat | L |
| Languages spoken | NPI-adjacent; local fit | M | Self | L |
| Gender | NPI holds gender; patients (esp. women) filter by it | M | Reg, Self | M |
| Insurance/panel acceptance, corporate panels | Cost filter | B | Self, Facility | L |
| Memberships (CPSP, OSP, PMA), fellowships | Credibility | T | Doc | L |
| Awards, publications, talks | Credibility | T | Plat | L |
| Patient reviews with verified-visit flag | Practo/Zocdoc core | T | Peer | M (reviewer health inference) |
| Clinic contact number (reception) vs doctor's personal mobile | Protect doctor privacy | B | Self | M-H (see C) |
| Telemedicine licence/platform | Regulated in some jurisdictions | T | Reg | L |

### 3. Hospitals, clinics, eye hospitals
| Field | Why it matters | Value | Verifier | Sens |
|---|---|---|---|---|
| Facility type (tertiary hospital, secondary, clinic, day-care surgical, eye hospital, maternity home, lab collection point) | Right-level care search | M | Reg, Self | L |
| Ownership (govt, private, trust/charity, military, teaching) | Fees/eligibility expectations | B | Self, Reg | L |
| Licence/registration with provincial healthcare commission (e.g., PHC, SHCC), licence no., validity | Legal operation; PHC offers public verification ([repo note](pakistan_registries_and_bodies.md)) | T | Reg | L |
| Accreditations (JCI, ISO 9001/15189, national, NABH for India) | Quality signal; JCI/NABH existence from background knowledge [UNVERIFIED] | T | Doc, accreditor's list | L |
| Bed count (total, ICU, NICU, private/ward) | Capacity | B, T | Self (hard to verify), Field | L |
| Departments/specialties and sub-specialty centres (e.g., retina, cornea, glaucoma, paediatric ophthalmology, oculoplasty) | Specialty search for eye hospitals | M | Self, Field | L |
| Procedures/services list with price ranges (cataract/phaco, LASIK, injections) | Buyer value; high willingness to compare | B | Self, Field | L |
| Equipment (OCT, fundus camera, visual field analyser, phaco machine, femtosecond laser, MRI/CT, ventilators) | Capability proof; priced-service and installed-base lists [INFERENCE] | B, T | Self, Field | L |
| Emergency services (24x7 ER, trauma level, ambulance, eye emergency, on-call times) | Time-critical filter | B | Self, Field | L |
| Doctor roster link (each doctor entry links to facility) | Graph of lists | B | Auto | L |
| Insurance/panel list (private insurers, Sehat Card-type govt schemes [UNVERIFIED], corporate) | Payment filter | B | Self, Field | L |
| Visiting hours, OPD hours, appointment channels, online reports portal | Practicality | B | Self | L |
| Patient facilities (pharmacy, lab, cafeteria, prayer area, parking, wheelchair access) | GBP accessibility style | B | Field | L |
| Charity/free treatment programmes, zakat eligibility | Pakistan relevance [INFERENCE] | B | Self, Doc | L |
| Infection control/radiation licence (PNRA for X-ray/CT per repo note) | Regulated diagnostic equipment | T | Reg | L |
| Complaints/adverse event record (if public) | Safety | T | Reg | M (defamation risk if unsourced) |
| Public health-system identifiers (facility code, NPI-type org ID, authorised official) | NPI includes authorised official for orgs | T | Reg | M (person's name) |

### 4. Diagnostic equipment / MRI centres with priced services
| Field | Why it matters | Value | Verifier | Sens |
|---|---|---|---|---|
| Centre type (standalone imaging, hospital department, lab chain collection point) | Context | M | Self | L |
| Modalities available (MRI, CT, X-ray, ultrasound, DEXA, mammography, nuclear, PET, ECG, echo, pathology) | Primary search filter | M | Self, Field | L |
| Equipment per modality: make, model, field strength (e.g., 1.5T/3T), slice count, install year, open/closed bore | Quality and capability driver; buyers compare 1.5T vs 3T [INFERENCE] | B, T | Self, Doc (purchase/AERB-type licence), Field | L |
| Regulatory licence for radiation equipment (PNRA in Pakistan per repo note; AERB India [UNVERIFIED]) | Safety/legal | T | Reg | L |
| Accreditation (ISO 15189, CAP, NABL) | Quality | T | Doc | L |
| Test/scan catalogue with price per test, currency, price date, what's included (contrast, report, film/CD), turnaround | Core of "priced services" | B | Self, Field | L |
| Package prices (executive check-up, cardiac, women's) | Compare | B | Self | L |
| Referral requirement (doctor referral needed vs walk-in); preparation instructions | Practicality | B | Self | L |
| Reporting: radiologist name/qualification, report turnaround, online report access, second-opinion service | Trust | T, B | Self | M (named clinician) |
| Home sample collection/mobile service, coverage areas | Pathology convenience | B | Self | L |
| Appointment/slot booking, same-day availability, 24x7 | Urgency | B | Self | L |
| Insurance/panel/corporate rate acceptance | Payment | B | Self | L |
| Machine downtime/maintenance notices | Avoids wasted trips | B | Self | L |
| Patient-safety info (MRI-conditional implants, pregnancy, sedation, paediatric) | Safety | T | Self | L |

### 5. Tradespeople and skilled individuals (Urban Company, Angi, Thumbtack, TaskRabbit)
Platform field sets below are [UNVERIFIED] recollection (profile, services with prices, reviews, background checks, service area, availability).

| Field | Why it matters | Value | Verifier | Sens |
|---|---|---|---|---|
| Display name (first name + initial option); photo | Humanise; reduce exposure | T | Doc (ID match) | M |
| Trade(s) and specialisations (e.g., AC repair, wiring, geyser, mobile screen replacement) | Search | M | Self, Field | L |
| Services menu with price (fixed/starting/hourly/visit charge), unit, currency, price date | Buyers compare; Urban Company-style fixed prices [UNVERIFIED] | B | Self, Peer | L |
| Visit/inspection fee and what's waived | Avoid disputes | B | Self | L |
| Service area (areas/radius), travel limits | Matching | M | Self | L |
| Years of experience; jobs completed; repeat-customer share | Trust | T | Self, Peer | L |
| Training/certifications (technical board diploma, NAVTTC, manufacturer authorisation) | Quality | T | Doc | L |
| Licence where required (electrician licence, gas fitter) | Safety-critical trades | T | Doc, Reg | L |
| Tools/equipment owned; parts supply (provides parts / customer buys) ; warranty period on work | Capability, risk | B, T | Self | L |
| Availability: weekly hours, same-day, emergency/24x7 call-out, next free slot | Matching | B | Self | L |
| ID verification (CNIC check done: yes/no, date) — store the fact, not the number | Trust badge | T | Doc | H (hold CNIC image only if essential, encrypted) |
| Police/character verification | Home-entry safety | T | Doc | H |
| Reference contacts / past customer testimonials | Trust | T | Peer | M |
| Insurance/liability cover | Rare among individuals | T | Doc | L |
| Languages; gender (women customers may prefer same-gender provider) | Matching | M | Self | M |
| Work photos (before/after) | Evidence | T | Self | L-M |
| Team vs solo; employer/crew lead | Accountability | T | Self | L |
| Reviews with verified-job flag; cancellation/no-show rate | Core | T | Peer | M |
| Preferred contact via relay/WhatsApp | Protect personal number | B | Auto | H (see C) |

### 6. Contractors and construction firms
Pakistan anchor: PEC constructor categories C-A to C-6 with project cost limits (older policy, undated; UNVERIFIED current values) — [repo note](pakistan_registries_and_bodies.md).

| Field | Why it matters | Value | Verifier | Sens |
|---|---|---|---|---|
| Legal entity type, registration (SECP), NTN/STRN, FBR active-taxpayer status | Legal/tender eligibility | T | Reg | L (company); M (sole prop) |
| Regulator licence: PEC registration no., category (C-A ... C-6), field(s) of work (civil, electrical, mechanical, etc.), validity date | PEC registration is the legal gate and tender requirement | T | Reg, Doc | L |
| Single-project value limit / annual turnover capacity | Eligibility for project size (e.g., PEC cost limits) | M | Reg (category), Doc | L |
| Other licences (provincial contractor class e.g., "Class A" in some jurisdictions [INFERENCE], developer authority enlistment such as DHA) | Local eligibility | T | Reg, Doc | L |
| Work types (residential, commercial, roads, dams, MEP, interiors, renovation) | Search | M | Self | L |
| Past projects: name, client (if consent), location, value band, year, role, completion certificate | Strongest evidence of capacity | T, B | Doc, Field, Peer | M (client confidentiality) |
| Key personnel: PEC-registered engineers, project managers, headcount | Capability | T | Doc | M (named staff) |
| Plant and equipment owned/leased (excavators, batching plant, cranes, formwork) | Capacity and cost | B | Self, Field | L |
| Certifications: ISO 9001/14001/45001 | Quality/safety | T | Doc | L |
| Bonding/financial: bid/performance bond capacity, bank reference, audited turnover band, litigation/blacklisting status | Owner risk | T | Doc, Reg (blacklist notices) | M-H (financials) |
| Insurance (contractors' all-risk, workers' comp) | Risk | T | Doc | L |
| Safety record; HSE policy | Risk | T | Doc | L |
| Subcontracting practices; in-house vs outsourced trades | Delivery risk | B | Self | L |
| Tender awards/enlistment on EPADS/PPRA, authority lists | Independent validation | T | Reg | L |
| Warranty/defects liability terms | Buyer protection | B | Self | L |
| Service area/mobilisation range | Matching | M | Self | L |
| Dispute/complaint history | Trust | T | Peer, Reg | M (defamation risk) |

### 7. Schools and tutors (including Quran tutors)
Safeguarding data for tutors teaching children is the highest-risk segment (see C).

| Field | Why it matters | Value | Verifier | Sens |
|---|---|---|---|---|
| Entity: school / academy / coaching centre / individual tutor / online platform | Different risk and fields | M | Self | L / M for individuals |
| School registration/recognition (PEIRA/provincial authority, board affiliation) | Legitimacy | T | Reg | L |
| Grades/levels offered; boys/girls/co-ed; shifts; medium of instruction | Core filters | M | Self, Field | L |
| Curriculum/board (Matric/FSc board, Cambridge O/A level, IB, Montessori, Hifz/Dars-e-Nizami) | Core filter | M | Self, Doc | L |
| Fees: admission, monthly tuition, annual charges, per-hour tutoring fee, trial lesson price, fee year, concessions/scholarships | Primary buyer decision | B | Self, Field | L |
| Subjects taught (tutor); exam prep (SAT, MDCAT, ECAT, IELTS); Quran tutor subjects (Nazra, Tajweed, Hifz, translation, Arabic) | Matching | M | Self | L |
| Tutor qualifications, degrees, ijazah/sanad (Quran), teaching certificates | Quality | T | Doc | L-M |
| Years of teaching experience; students taught; results/pass rates | Outcome signal | T | Self, Doc | L (unverified stats risky) |
| Teaching mode: online, in-person at student's home, at tutor's place, centre; platforms used (Zoom, Skype) | Core filter | M | Self | L |
| Tutor gender; students' gender accepted (e.g., female tutor for girls) | Cultural, safety-driven filter in Pakistan/Gulf [INFERENCE] | M | Self | M-H |
| Languages of instruction (Urdu, English, Arabic, Pashto, Punjabi...) | Matching | M | Self | L |
| Safeguarding: background/police/character check status and date, references, child-protection policy, parent-in-room/recorded-session policy | Child safety | T | Doc, Field | H |
| Schedule/availability, class size, one-to-one vs group | Practicality | B | Self | L |
| Facilities (labs, library, transport, hostel), campus photos | School choice | B | Self, Field | L |
| Admissions: process, test, deadlines, intake months | Practicality | B | Self | L |
| Trial class offered; refund/cancellation policy | Buyer risk | B | Self | L |
| Reviews from parents (verified-contact) | Trust | T | Peer | M (children may be identifiable; strip names) |
| Demo video/intro recording | Trust | T | Self | M-H (voice/face; child voices excluded) |

### 8. Professionals and talent (e.g., data scientists)
Overlaps with repo note `global_talent_lists.md`.

| Field | Why it matters | Value | Verifier | Sens |
|---|---|---|---|---|
| Name, headline, photo, location (city/country), time zone | Identity | T | Plat (LinkedIn/GitHub) | M |
| Role types (data scientist, ML engineer, analyst, MLOps) and seniority | Matching | M | Self | L |
| Skills with level and years (Python, SQL, PyTorch, Spark, Power BI) | Matching | M | Self, Plat | L |
| Domain experience (health, fintech, agri, NLP, CV) | Matching | M | Self | L |
| Tools/stack and cloud certifications (AWS/GCP/Azure, Databricks) | Hiring filter | M, T | Doc (credential IDs) | L |
| Education and institutions | Trust | T | Doc | L |
| Employment history (employers, dates) | Trust | T | Plat | M |
| Portfolio links: GitHub, Kaggle (rank/tier), Hugging Face, ORCID, Google Scholar, personal site | Verifiable evidence | T | Plat | L (public links) |
| Publications/patents/talks (DOI) | Evidence | T | Plat (ORCID/DOI) | L |
| Projects with outcomes | Evidence | B, T | Self | L-M (client confidentiality) |
| Engagement type: full-time, contract, freelance, advisory; remote/on-site/hybrid; willingness to relocate | Matching | M | Self | L |
| Rate: hourly/day/project, currency, range, negotiable flag; salary expectation (private) | Buyer filter; sensitive | B | Self | M-H (salary privacy) |
| Availability: start date, hours per week, notice period | Matching | B | Self | L |
| Languages (spoken, with level) | Matching | M | Self | L |
| Work authorisation/visa, country of tax residence | Hiring compliance | B | Self | M-H |
| References/endorsements | Trust | T | Peer | M |
| Contact via platform relay; opt-in for recruiters | Anti-spam, consent | B | Auto | M-H |
| Public vs private sections (what recruiters may see) | Consent | — | Self | M |

### 9. Manufacturers, suppliers, wholesalers (IndiaMART, Alibaba)
| Field | Why it matters | Value | Verifier | Sens |
|---|---|---|---|---|
| Business type: manufacturer, trader, wholesaler, distributor, exporter, service provider | Core filter; IndiaMART-style [UNVERIFIED] | M | Self, Field | L |
| Products (name, category, HS/HSN code, specs, brands, photos, catalogue PDF) | Search | M, B | Self | L |
| Price: unit price or range, price basis (ex-works/FOB/CIF), currency, price date | Buyer comparison | B | Self | L |
| MOQ (min order quantity, unit); sample availability and cost | Alibaba/IndiaMART listing staples [UNVERIFIED] | B | Self | L |
| Production capacity (units/month), shifts, machinery list, factory area, workforce band | Capability | B, T | Field, Doc | L |
| Lead time; packaging; payment terms (advance, LC, credit); incoming/outgoing shipping | Practicality | B | Self | L |
| Certifications (ISO, CE, BIS, GMP, Halal, SGS audits, DRAP for pharma) | Compliance | T | Doc | L |
| Export markets, export experience (years), IEC/export licence | Importer filter | M, T | Self, Doc | L |
| Tax/legal IDs: NTN/STRN (Pakistan), GSTIN/PAN/IEC (India), unified social credit code (China), DUNS | Legitimacy; GST verifiable via portal [UNVERIFIED] | T | Reg | L (company); M (sole prop) |
| Registered address vs factory address vs warehouse (separate geo for each) | Avoids ghost traders | T | Field | L |
| Customisation/OEM/private label offered | Buyer filter | M | Self | L |
| Year established; annual turnover band; key customers (with consent) | Trust | T | Self, Doc | M (turnover is commercially sensitive) |
| Stock availability / ready stock list | Fast buyers | B | Self | L |
| Trade-association membership (chamber, TDAP, FPCCI-type [UNVERIFIED]) | Trust | T | Doc | L |
| Response rate / enquiry response time; verified-supplier badge type | Trust | T | Platform | L |
| Contact person and role | RFQ routing | B | Self | M |

### 10. Petrol pumps, pharmacies, retail shops
| Field | Why it matters | Value | Verifier | Sens |
|---|---|---|---|---|
| Brand/marketer (PSO, Shell, Total, Attock, etc. [INFERENCE]; pharmacy chain; shop brand) | Brand-loyal search | M | Self, Field | L |
| Opening hours incl. 24x7 and night-shift status | GBP primary hours; critical for fuel/pharmacy | B | Self, Field | L |
| Services: fuel grades (petrol, diesel, CNG, LPG, EV charging), air, tyre, car wash, convenience store, ATM | Specific need matching | B | Self, Field | L |
| Fuel price display, last-updated (regulated pump prices published nationally [INFERENCE]; local list variation) | Buyer value | B | Auto/Field | L |
| Pharmacy: DRAP/provincial drug licence no., pharmacist-in-charge name and registration, controlled-drug licence, cold-chain, 24x7, home delivery, online ordering, prescription service | Legal/safety (drug inspectors per repo note) | T | Reg, Doc | M (pharmacist named) |
| Medicines/categories stocked (brands, generics, surgical, baby, OTC); stock-check call or inventory API | Buyer value | B | Self | L |
| Retail: product categories, brands, sizes, price band, warranty/returns, installments, delivery | Matching | B | Self | L |
| Payment methods: cash, cards, mobile wallets, QR, credit/khata | schema.org `paymentAccepted`; GBP payments | B | Self, Field | L |
| Service options: walk-in, delivery, pickup, curbside (GBP service options) | | B | Self | L |
| Facilities: parking, restroom, prayer area, wheelchair access | GBP accessibility | B | Field | L |
| Safety/legal: petroleum licence (OGRA/explosives dept [UNVERIFIED]), fire safety, weights-and-measures calibration seal date | Trust at pumps | T | Reg, Field | L |
| Owner/dealer name, manager phone | Escalation | B | Self | M |
| Promotions, loyalty programme | Engagement | B | Self | L |
| Queue/crowd info (live) | Convenience | B | Peer | L |

---

## C. Fields that are sensitive or risky to hold

| Field | Concern (legal/safety) | Recommended handling |
|---|---|---|
| Personal mobile numbers of individuals (tradespeople, tutors, doctors, freelancers) | Personal data; harassment, spam, WhatsApp scraping, doxxing; under EU/UK GDPR, India DPDP Act and similar laws a person can demand deletion; Pakistan has no enacted general law as of May 2026 per repo note, but PECA 2016 and draft PDP Bill apply/loom [repo note] | Collect with explicit consent; show via call/WhatsApp relay or click-to-reveal with logging; allow opt-out; never publish scraped personal mobiles |
| Home address of individuals | Stalking/burglary risk, especially women and tutors | Show area/neighbourhood only; exact address private |
| CNIC / national ID numbers and images, passports | Identity theft; heavily regulated in many jurisdictions | Store only a "verified" flag and date; if a copy is essential, encrypted, access-logged, deleted after check |
| Children's tutors and anything about children (students' names, photos, ages, reviews naming kids) | Child safeguarding; consent of parents; risk of predators using the list; reputational defamation if a tutor is accused unverified | Verified safeguarding checks, parent-in-room policy fields, relay-only contact, no child data on public pages, careful moderation, takedown route |
| Quran tutors online (often unlicensed individuals, cross-border contact with minors) | Child-safety and fraud (prepaid fees, fake ijazah) | Level-gated verification, trial lesson, platform relay, report button; flag unverified credentials |
| Health data (patient reviews that reveal conditions, health outcomes, patient photos, appointment data) | Special-category data under GDPR; HIPAA if US-covered entity; privacy and dignity; consent needed for before/after photos | Do not hold patient-level data; sanitise reviews; no patient photos without written consent; keep bookings off the public list |
| Doctor medical-negligence/complaint records | Defamation/consent; official records may have access limits | Only link to official public decisions with source and date |
| Personal salary expectation, nationality, visa, age, religion, ethnicity of talent | Discrimination law exposure; sensitive personal data | Optional, private by default, not searchable |
| Gender and "same-gender only" preferences | Valid user filter but personal data; also discrimination risk if used for hiring | Show as self-declared service preference only |
| Police/character certificates | Criminal-record data, strictly regulated in many jurisdictions | Hold only a pass/fail flag and date |
| Customer reviews with reviewer identity | Personal data of reviewers; defamation of providers | Pseudonymise; moderation; right of reply; takedown procedure |
| Scraped data from Google, Yelp, LinkedIn, Facebook | Terms of service and database/copyright claims (see legal-limits note) | Record source terms per field; do not import fields whose terms forbid reuse; use only public registry data or owner submissions |
| Business financials (turnover, bonding capacity) | Commercial confidentiality | Show as bands with consent; or private-to-buyer |
| Exact GPS of home-based service providers | As home address | Use area centroid |

---

## D. Launch versus later (recommended)

Rule of thumb [INFERENCE]: launch with fields that (1) can be verified cheaply, (2) drive the buyer's first decision, (3) carry low privacy risk. Everything in Section A is "launch" except: media gallery (one photo launch), reviews (later; start with claim/verify), external identifiers beyond registry ID (later), languages/accessibility (launch for hospitals and tutors only).

| List type | Must-have for launch | Later |
|---|---|---|
| Common core | entry_id; name; primary category; address + geo + area ID; one public phone/WhatsApp; hours; verification_level; source_url + retrieved date; consent flag; last_verified; claim_state; status | Alternates/translations, media gallery, ratings, payment-methods, change history UI, social links |
| 1 Local business | Services/products tags; payment methods; price band; service options; registration no. (if company) | Brands list, FAQ, offers/posts, staff size |
| 2 Doctors | Name; regulator + reg no. + licence status; qualifications; specialty; practice location(s) with days/times; consultation fee; languages; gender | Procedures/conditions detail, publications, panel list, reviews, telemedicine, online booking |
| 3 Hospitals/clinics/eye hospitals | Facility type; ownership; licence no. + validity; departments/specialties; emergency 24x7 flag; OPD hours; panel/insurance list; key equipment list | Bed counts by ward, accreditation docs, price lists, charity programmes, complaint links |
| 4 Diagnostics/MRI | Modalities; equipment make/model/field strength; radiation licence; price list for top 10-20 tests with price date; turnaround; referral requirement; hours | Package prices, radiologist roster, report portal, machine downtime, panel rates |
| 5 Tradespeople | Trade(s); service area; price list (visit charge + 3-5 services); years of experience; availability; ID-verified flag; contact via relay | Certifications, tools, warranty, before/after photos, references, insurance |
| 6 Contractors | Entity + PEC no. + category + fields; work types; 3 past projects (with proof link); key equipment owned; NTN status | Bonding, financial bands, safety record, HSE docs, key personnel, litigation history |
| 7 Schools/tutors | Entity type; grades/subjects; curriculum/board; fees with year; mode (online/in-person); gender served/tutor gender; safeguarding check status for child-facing tutors; registration/recognition | Results, facilities, admissions detail, demo videos, parent reviews |
| 8 Talent | Role; skills + years; portfolio links (GitHub/Kaggle/ORCID); engagement type; rate band; availability; languages; location/time zone | Publications list, certifications with IDs, visa, references, project case studies |
| 9 Manufacturers/suppliers | Business type; products + categories; MOQ; capacity band; certifications; export markets; NTN/STRN/GSTIN; factory address | Price lists, lead times, OEM details, turnover band, customer references, ready stock |
| 10 Pumps/pharmacies/retail | Hours (24x7 flag); brand; services/fuel types; payment methods; for pharmacy: drug licence no. + pharmacist-in-charge | Live fuel/stock info, delivery, loyalty, calibration seal date, promotions |

---

## E. Gaps and unverified items

- Not researched in this session (budget exhausted, fetches blocked): Practo, Zocdoc, Justdial, Yelp, Yellow Pages, Urban Company, Angi, Thumbtack, TaskRabbit, IndiaMART, Alibaba, ORCID, Kaggle, GitHub profile schemas, school directories, tutor platforms (e.g., Tutors.com-type, Quran academy platforms), PEC portal, PNRA, provincial healthcare commission forms, DRAP drug licence forms, OGRA licence forms. All their field lists above are INFERENCE/UNVERIFIED.
- schema.org types for Physician, Hospital, MedicalClinic, Dentist, Pharmacy, GasStation, School, ProfessionalService were not read; the specific schema.org property names for these (e.g., accepting-new-patients, medicalSpecialty, available services, health plan networks) are from memory and should be checked at schema.org/Physician and schema.org/Hospital.
- Google Business Profile category list and attribute catalogue per category not retrieved; support.google.com was blocked. The attribute groups quoted come from third-party blogs.
- No current fee, count or capacity figure is asserted; PEC category limits in the repo are older and undated and must be re-confirmed.
- Whether PMDC, PEC, provincial healthcare commissions or FBR allow reuse/bulk export of registry fields (so they can be stored, not just checked) is not verified.
- Legal analysis is thin: GDPR/UK GDPR, India DPDP Act 2023, Pakistan PECA and PDP Bill, HIPAA, child-protection regimes. Counsel needed before storing health, child, ID or character-check data.
- Gender-based filters, caste/religion-adjacent fields, and discrimination law implications are flagged but not researched.
- Controlled vocabularies (categories, specialties, trades) and unit standards are not defined here; next step is to pick a base taxonomy (e.g., NUCC taxonomy for clinicians [UNVERIFIED], HS/HSN for products, PEC categories for contractors).
- Suggested next step: sample 5 live listings per list type, tick fields against Sections A/B, drop fields nobody fills, and compute fill rates; and confirm per-field legal basis with counsel.

---

## Summary of findings

1. Only three sources could be consulted (schema.org LocalBusiness, GBP attributes, NPPES fields); the rest is inference. The template is a hypothesis to validate against live listings, not a verified standard.
2. The proven pattern across schema.org, GBP and NPI is: a common core (identity, geo, areaServed, hours, payment, price band) plus a category-driven attribute set. The recommended model is one primary category per entry and a type-specific add-on table.
3. The strongest trust fields differ by type: registry number and validity for clinicians, facilities and contractors; equipment make/model plus licence for diagnostics; ID-verified flag and priced services for tradespeople; verifiable profile links for talent; tax IDs and certifications for suppliers; drug licence and hours for pharmacies.
4. Priced services (diagnostics, trades, hospitals, tutors) are the highest buyer value but also the stalest field; every price needs a currency and a price date.
5. The riskiest data is about individuals and children: personal mobiles, home addresses, CNIC, tutor safeguarding records, patient information. Hold flags and relays, not raw documents, and gate child-facing tutors behind verification.
6. Launch with about 10-12 core fields plus 5-8 per type; defer galleries, reviews, financial bands and long histories.
