# Entry field templates per family (backend research 01)

Research date: 2026-10-06. Status: proposal for owner sign-off under decision C26; nothing here changes code. English only (founder rule of 2026-10-06).

Companion file: `research_notes/Backend research/01_entry_fields.csv` (family,key,label,type,required,show,filterable,row_descriptor,sensitivity). It holds the same fields as the tables below, one row per field, plus the common core under family `core`.

## 1. Summary

- **29 families cover all 235 list types** in `backend/taxonomy/data/list_types.csv` (every slug is mapped; no type is left over). The brief said about 25; the four extra families exist because safeguarding (tutors, domestic workers), listing items (property, classifieds, opportunity posts) or entity shape (topic items, personal items) differ too much to share a template. They can be merged back if the owner prefers (section 9).
- **One common core of 27 fields** (the Tier 1 core already in `docs/LIST_AND_ENTRY_COMPONENTS.md` section 4) plus **555 type-specific fields**, an average of about 19 per family (range 13 to 28). Of the family fields, 72 are required to publish, 329 are filterable, 404 are shown free (P), 131 to subscribers (L), 13 owner-only (O), 4 internal (I), 3 hidden behind the outreach relay (H).
- **Sensitivity tags** on family fields: 41 personal-data, 21 child-related, 10 health-price, 9 commercial (an extra tag beyond the three the brief named). Whole families are gated by those tags, not just fields (section 5).
- **Evidence is thin where the brief most needs it.** Justdial's own pages did not surface in four searches (only scraper descriptions did); Practo's own doctor pages did not surface in two sessions; Zameen's project pages and PakWheels' full field list were seen only through scraper descriptions. About 40 searches were run across this and the earlier round (2026-10-05); everything is a search snippet, never a page read (WebFetch was not used). Each platform line is graded in section 2.
- **What platforms actually hold converges** across categories on the same short list: identity, category, address and geo, hours, a price or price band, a licence or registration with a verified flag, years in business, service options, rating. The type-specific part is small and regulator-driven. AllLists additions that no platform checked holds as a standard field: equipment records with make, model and field strength (C21), per-ID verified flags, dated check labels, accreditation scope, safeguarding status for child-facing providers.
- **Prices are the stalest and riskiest fields.** Every money value carries currency and price date; health prices (doctor fees, test and scan prices, procedure prices) are not collected until the health rules are adopted (Q-S1).

## 2. Evidence and method

**Tools.** WebSearch in standard mode, about 28 queries on 2026-10-06 targeted at the platforms named in the brief, plus the 35 queries of the earlier round recorded in `research_notes/Entry template verification/01_live_listing_fields.md` and `research_notes/Service provider sources/entry_attributes_by_list_type.md`. Repo documents read in full: `docs/DECISIONS.md` (C17, C21, C26, sections 3, 9, 11), `docs/LIST_AND_ENTRY_COMPONENTS.md`, `backend/taxonomy/seeds.py`, `services.seed_manufacturer_template`, `AddonField` model, `list_types.csv`, the three Pilot trade notes (template and entry-field sections).

**Grades used below.**
- **[C]** confirmed in a 2026-10-06 search result. Almost all [C] items rest on scraper-tool descriptions (Apify and similar), aggregator copies or help-centre snippets, not on the platform's own page. Treat as S-grade unless the line says the platform's own page was returned.
- **[P]** carried from the 2026-10-05 notes (their own grades apply; mostly snippet-level, some from platform pages).
- **UNVERIFIED** single-sourced, inferred, regulator-driven with no platform evidence, or undated. Figures (prices, counts, limits) are always UNVERIFIED as to currency.

**Platform matrix (what each platform holds, as far as this research could see).**

| Platform | Fields seen | Grade | Families it informs |
|---|---|---|---|
| Justdial | name, phone, address, area, city, business type, composite rating, review count, verified flag, WhatsApp numbers, web URL, pincode, lat/long; year established, services, amenities, payment options named as extra fields; 48.8 million listings by March 2025 (finance-page snippet) | [C] scraper descriptions only; Justdial pages did not surface | repair_and_trade_services, retail_shops, personal_care_wellness_fitness, transport |
| IndiaMART | help centre: GST number, firm type and company size, turnover details; supplier pages: nature of business, legal status of firm, annual turnover, GST number and registration date, IEC, address with PIN; TrustSEAL documentary verification (paid); employee count not confirmed | [C] and [P] (help.indiamart.com and member pages returned) | manufacturers_and_exporters, suppliers_distributors_and_equipment |
| Practo | clinic and hospital pages: timings, services, facilities (ICU, CCU, lab, blood bank, CT), doctors; lab tests with free home collection and reports in 24 hours. Doctor profile fields only through copies on Credihealth, Bajaj Finserv Health, Drlogy: qualifications, experience, registration number, specialisation, fee by mode and clinic, address, timings, services, languages, memberships | [C] partly platform pages (clinic, hospital, labs), doctors S-grade | medical_practitioners, health_facilities, diagnostics_and_imaging |
| Zameen | listings: title, price PKR, bedrooms, bathrooms, area and unit (marla, kanal, sqft, sqm), location, city, type, purpose, date added, agency, contact, lat/long, description, amenities; instalment listings: initial amount, monthly instalment, remaining instalments; agency pages: name, team and roles, about, areas, listing counts, free or premium; editorial review of agency profiles. Project and society page fields not confirmed | [C] listing pages returned, field lists from scrapers | property_listings, real_estate_agents_and_developers |
| PakWheels | make, model, trim, model year, mileage, fuel type, engine cc, transmission, assembly (local or imported), body type, colour, registration city, price | [C] listing pages returned plus scraper lists | classified_listings |
| Thumbtack | rating, review count, hires, response time, Top Pro, background-check badge (all account owners must pass a check), license badge, years in business, employee count, services, weekly hours, payment methods, credentials, project photos, FAQs, social links | [C] Thumbtack safety and pro-center pages plus scrapers | repair_and_trade_services, construction_and_design_firms |
| Yelp | name, alias, rating, review count, price range, phone, address, coordinates, categories, weekly hours, 20+ attributes (bool, single, multi choice: WiFi, parking, alcohol, noise), menu, owner profile, health score where available | [C] scraper and API docs | food_and_beverage_outlets, personal_care_wellness_fitness |
| ThomasNet | primary company type (for example custom manufacturer), year founded, employee range, annual sales bracket, capabilities, equipment, product lines, brands carried, certifications (ISO 9001, AS9100, ITAR, NADCAP), ownership and diversity status; OEM, contract manufacturer, distributor filters | [C] scrapers and trade-press page | manufacturers_and_exporters, suppliers_distributors_and_equipment, b2b_support_and_trade_bodies |
| Clutch | hourly rate band, minimum project size, employee band, founded year, locations, focus areas, industries, client size segments, cost rating | [C] Clutch profile pages returned | digital_talent_and_agencies, professional_advisers |
| Zomato | cuisines, establishment types, cost for two, hours, dining and delivery ratings, address, coordinates, phone, chain, amenities, popular dishes, online ordering, delivery time, offers | [C] scraper pages | food_and_beverage_outlets |
| Upwork | headline, hourly rate, total earned, job success score, skills, location, availability badge, portfolio, verified flag, agency link | [C] scraper pages | digital_talent_and_agencies |
| Care.com | display name, categories, city and postal code, bio, years of experience, hourly rate range, CareCheck status and date, care age groups, credentials, languages, CPR, availability by day and time | [C] Care.com profile pages returned | domestic_and_care_workers |
| Alibaba | factory size, staff count, annual revenue band, response rate, OEM/ODM tag, Gold years, assessed flag | [C] scraper descriptions; verification tiers [P] | manufacturers_and_exporters |
| Urban Company | screening steps only (background check, skill assessment, interview, training); earlier round has fixed prices, guarantee, ratings | [C] weak, [P] | repair_and_trade_services |
| Google Business Profile | attributes by category: accessibility, identity (women-owned), service options (online care, appointment only, language assistance), amenities, payments, planning; gyms get activities and services groups | [C] and [P] (support.google.com returned in one result) | all local business families |
| Charity Navigator | EIN, mission, programmes, beacon ratings, governance, financials from Form 990 | [C] | government_civic_community |
| G2 and Capterra | pricing plans, platforms, support and training, typical customers, vendor name, location, website, founded year, features, integrations | [C] scrapers | topic_and_curated_lists, digital_talent_and_agencies |
| Eventbrite | name, description, dates, venue, geo, category, tags, organiser, currency, ticket price range, free flag, refund policy | [C] help pages returned | opportunity_posts, venues_and_event_services |
| Airbnb and Booking | property type, guest capacity, bedrooms, beds, bathrooms (shared or private), amenities, house rules, cancellation policy | [C] help pages | accommodation_and_travel |
| schema.org JobPosting | title, employmentType, baseSalary, jobLocation, validThrough, hiringOrganization, experienceRequirements | [C] schema.org page returned | opportunity_posts |

**Search outcomes that returned nothing useful (so the field is UNVERIFIED):** Justdial listing page layout for pharmacies, gyms, salons (four queries); Zameen project and society page fields; OLX and PakWheels mobile, livestock and pet field lists; Pakistan wedding hall platform field lists (results were Indian sites); PSQCA sanitaryware standard; Urban Company professional profile fields. Not searched at all this round: Marham, Oladoc, Property Finder, Checkatrade (covered in the earlier round [P]).

## 3. Conventions

**Types** (the eight the brief named plus one that the code already has): `text`, `number`, `money` (amount plus ISO 4217 currency plus price date inside the value record), `enum` (values listed in Notes), `bool`, `date`, `concept_list` (controlled vocabulary or taxonomy concepts), `place_list` (place tree nodes). `identifier_list` is the existing `AddonField` type for registrations (scheme, number, issuer, validity, register link, per-ID verified flag); 36 fields use it. Enum values are in the Notes column of each table because the CSV has no column for them.

**Req**: R required to publish, S should have, O optional. The CSV `required` column is true only for R.
**Show**: P free visitors, L subscribers, H hidden and reached only through the outreach relay (E13), I internal, O owner only (an addition for personal lists, which are private by default). Phone, WhatsApp and email are never shown to anyone (decision section 11).
**Filter / Row**: filterable on the list page; Row marks the one add-on field that adds a descriptor to each result row (one per family; the core always shows name, type, area, up to three specialities and check labels).
**Sensitivity**: `none`, `personal` (could identify or expose an individual), `child` (child-related: children are subjects, users or at risk), `health_price` (price of a health service, held back until Q-S1 rules are adopted), `commercial` (turnover, capacity, budget bands; an extra tag). Combined with `+` in the tables and `|` in the CSV.
**Source**: reg register or regulator list, own owner or claimant, sur AllLists survey (field surveyor, call or mystery call), agt AI agent from open sources (draft only; D14, D18), auto automated check.

**Differences from the code to settle before building** (nothing was edited):
1. `identifier_list` exists in `AddonField.Type` but not in the brief's list; keep it.
2. Show value `O` (owner only) does not exist; personal lists need it. Alternative: treat them as a separate private object type.
3. `entity_type` needs values for listing (property, classified, opportunity), topic item and personal item.
4. `backend/taxonomy/seeds.py` has 11 templates and assigns Data scientists to the `doctors` template and Bakeries and Beauty parlours to `retail`; the new families fix this (section 8). The 235 CSV types have no template yet (decision log, 2026-10-06).

## 4. Common core (applies to every entry in every family)

These are the existing Tier 1 fields from `docs/LIST_AND_ENTRY_COMPONENTS.md` section 4 expressed as scalar and list fields. Repeating parts stay child records (contacts, social links, opening hours, services with prices, products, identifiers, areas served, equipment, branches, alternate names; spec section 5) and are not repeated per family. Verified-by, method, evidence, expiry, licence and retrieval date live in the per-value metadata (spec section 7), not as fields.

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `entity_type` | Entity type | enum | R | P | yes |  | none | own/agt | business, facility, person, institution, listing; picks privacy rules (add listing for classified and property items) |
| `primary_category` | Primary list type | concept_list | R | P | yes |  | none | agt/own | exactly one list-type concept; selects the family template |
| `secondary_categories` | Other list types | concept_list | O | P | yes |  | none | own | up to about 5 |
| `name` | Name | text | R | P |  | yes | none | reg/own/agt | display name; people: first name plus initial allowed |
| `name_variants` | Other names and spellings | text | S | P |  |  | none | own/agt | legal, trade, old names; feeds search |
| `description` | About | text | S | P |  |  | none | own | 150 to 600 characters |
| `status` | Operating status | enum | R | P | yes |  | none | sur/own | open, temporarily_closed, permanently_closed, moved |
| `address_area` | Area (place tree nodes) | place_list | R | P | yes | yes | none | agt/own/sur | country down to society; always shown |
| `address_street` | Street address | text | R | L |  |  | personal | own/sur/reg | individuals: area only, never a home address |
| `latitude` | Map pin latitude | number | R | L |  |  | personal | sur/agt | exact pin subscribers only; area centroid for home-based providers |
| `longitude` | Map pin longitude | number | R | L |  |  | personal | sur/agt | WGS-84 |
| `location_precision` | Pin precision | enum | R | P |  |  | none | auto | exact, building, street, area, city |
| `service_area` | Areas served | place_list | S | P | yes |  | none | own | required for mobile trades, tutors, carers |
| `contacts` | Phones, WhatsApp, email | text | S | H |  |  | personal | own/sur/reg | child records; never shown, outreach relay only (E13) |
| `website` | Website | text | O | L |  |  | none | own/agt | liveness-checked |
| `social_links` | Social pages | text | O | L |  |  | none | own/agt | typed child records |
| `owner_name` | Owner or manager | text | O | L |  |  | personal | own | hidden for individuals |
| `size_band` | Size band | enum | O | L |  |  | none | own/sur | employees, beds, rooms or fleet by type |
| `year_established` | Year established | number | O | P |  |  | none | reg/own |  |
| `parent_entry` | Chain or head office | text | O | P |  |  | none | agt/own | entry link |
| `languages` | Languages served | concept_list | O | P | yes |  | none | own | BCP 47 |
| `price_band` | Price level | enum | O | P | yes |  | none | own/sur | tiers 1 to 4, local price level |
| `payment_methods` | Payment methods | concept_list | O | P | yes |  | none | own/sur | cash, card, bank transfer, JazzCash/Easypaisa style wallets |
| `specialities` | Specialities | concept_list | S | P | yes | yes | none | reg/own | up to three shown on the row |
| `identifiers` | Registrations and licences | identifier_list | S | P |  |  | none | reg | scheme, value, issuer, validity, register link; never a national ID number |
| `hours_summary` | Hours and 24x7 flag | text | S | P | yes |  | none | own/sur | child records; filter is open_now and open_24x7 |
| `verification_level` | Check chips | enum | R | P | yes |  | none | auto | not_verified, ai_checked, owner_verified, surveyor_verified; each with date, who, how |
| `claimed` | Claimed by owner | bool | R | P | yes |  | none | own |  |
| `consent_status` | Consent (individuals) | enum | R | P |  |  | personal | own | required for persons; shown as a tick |
| `last_verified_on` | Last verified | date | R | P |  |  | none | auto |  |
| `do_not_share` | Do-not-share flag | bool | R | I |  |  | none | own | noindex, suppress share buttons |

Placement of free versus subscriber (decision section 11, kept): free sees name, other-language name, type, area, up to three specialities, check labels with dates; entry page adds hours, languages, year established, business type; subscribers add street address, exact pin, size, website, social pages, prices with dates, certificate details, and the family fields marked L below.

## 5. Family index

| # | Family | Entity | List types | Individuals | Child-facing | Health | Fields | Required to publish |
|---|---|---|---|---|---|---|---|---|
| 1 | `repair_and_trade_services` | business or person | 35 | 7 | 0 | 0 | 19 | provider_mode, trades |
| 2 | `construction_and_design_firms` | business | 9 | 0 | 0 | 0 | 16 | practice_type, fields_of_work, work_types |
| 3 | `real_estate_agents_and_developers` | business or person | 4 | 0 | 0 | 0 | 15 | business_role, listing_types, areas_served |
| 4 | `property_listings` | listing | 2 | 0 | 0 | 0 | 23 | purpose, property_type, asking_price, price_date, area_size, area_unit, listed_by_seller_type, listing_expires_on |
| 5 | `medical_practitioners` | person | 14 | 9 | 0 | 13 | 19 | system_of_medicine, specialty |
| 6 | `health_facilities` | facility | 10 | 0 | 0 | 10 | 18 | facility_type, departments |
| 7 | `diagnostics_and_imaging` | facility or equipment record | 5 | 0 | 0 | 5 | 21 | centre_type, modalities |
| 8 | `pharmacy_and_optical` | business | 3 | 0 | 0 | 3 | 16 | outlet_type |
| 9 | `education_institutions` | institution | 14 | 0 | 5 | 0 | 23 | institution_type, grades_offered |
| 10 | `tutors_and_instructors` | person (or small firm) | 7 | 6 | 4 | 0 | 20 | subjects, safeguarding_status, safeguarding_checked_on |
| 11 | `domestic_and_care_workers` | person (or agency) | 6 | 4 | 1 | 0 | 18 | roles |
| 12 | `professional_advisers` | person or firm | 9 | 3 | 0 | 0 | 13 | practice_areas |
| 13 | `financial_providers` | business or person | 5 | 1 | 0 | 0 | 13 | provider_type, institution_name, regulator_licence |
| 14 | `digital_talent_and_agencies` | person or firm | 18 | 8 | 0 | 0 | 25 | role_types, skills, recruiter_opt_in |
| 15 | `opportunity_posts` | listing | 5 | 0 | 0 | 0 | 22 | post_kind, post_title, category, post_place, deadline, post_status |
| 16 | `personal_care_wellness_fitness` | business or person | 9 | 2 | 0 | 0 | 16 | outlet_type, clientele |
| 17 | `food_and_beverage_outlets` | business | 6 | 0 | 0 | 0 | 16 | outlet_type, cuisines |
| 18 | `retail_shops` | business | 9 | 0 | 0 | 0 | 15 | shop_type, product_categories |
| 19 | `fuel_and_utility_supply` | business | 3 | 0 | 0 | 0 | 14 | fuel_types |
| 20 | `classified_listings` | listing | 3 | 0 | 0 | 0 | 25 | item_kind, condition, seller_type, asking_price, price_date, listing_expires_on |
| 21 | `transport_and_logistics` | business | 7 | 0 | 0 | 0 | 18 | service_type, coverage |
| 22 | `accommodation_and_travel` | business | 3 | 0 | 0 | 0 | 25 | property_type |
| 23 | `venues_and_event_services` | business | 6 | 0 | 0 | 0 | 19 | venue_kind |
| 24 | `manufacturers_and_exporters` | business | 11 | 0 | 0 | 1 | 28 | business_type, product_categories |
| 25 | `suppliers_distributors_and_equipment` | business | 7 | 0 | 0 | 1 | 24 | trade_role, product_categories |
| 26 | `b2b_support_and_trade_bodies` | business or institution | 5 | 0 | 0 | 2 | 19 | service_kind, scope_of_services |
| 27 | `government_civic_community` | institution | 6 | 0 | 0 | 0 | 20 | body_type, jurisdiction |
| 28 | `topic_and_curated_lists` | topic item | 9 | 1 | 0 | 0 | 21 | item_kind, topic_ids, official_url, source_citation |
| 29 | `personal_lists` | personal item | 5 | 5 | 0 | 0 | 14 | item_kind |

Total list types mapped: 235 of 235. The required set per family is deliberately small (1 to 8 fields) so that agent-drafted entries can be published as drafts quickly (D18); the core adds name, primary category, area, status, verification level, claim state, consent for persons and last verified date.

## 6. Families

Notation in the type lists: [i] individual, [c] child-facing, [h] health flag in `list_types.csv`. The family is chosen from the list type; where a list type mixes unlike things (for example "Accountants, tax specialists, financial planners, banks, insurers") the entry's `primary_category` decides which enum value applies.

### 6.1 Repair and trade services (on-site trades, repair shops, installers, cleaners)

Family key `repair_and_trade_services`. Entity: business or person. Template applies to 35 list types:
Plumbers; Electricians [i]; Carpenters [i]; Masons and tile fixers [i]; AC technicians; Painters; Welders and fabricators; Locksmiths [i]; Roofing and waterproofing; Pest control and fumigation; Water tank and RO plant services; Gas, geyser and stove repair [i]; Generator, UPS and solar installers; Handymen / mistri (general) [i]; Mobile phone repair; Laptop and computer repair; Home appliance repair; Car mechanics and workshops; Motorcycle repair; Tyre and battery shops; Car wash and detailing; Watch, shoe and bag repair; Camera, printer and photocopier repair; CCTV and security system installers; Tractor and farm machinery repair; Plumbers and electricians; Carpenters, painters, handymen, masons, tilers; AC and appliance repair; Pest control; House, deep, sofa and carpet cleaning; Roofers, waterproofing, solar, windows, doors, flooring, other LSA home jobs; Landscapers, gardeners, tree service; Furniture assembly, TV mounting, junk removal [i]; Home inspectors; kitchen, bath and modular-kitchen remodellers; Car repair, wash, tyres, towing.

**What established platforms hold**

- Urban Company: fixed pre-booking prices per service, locality pages, visit charge, service guarantee, professionals background-verified, training before bookings [P: Oct 5 note, 2+ sources]. A 2026-10-06 search added only the screening steps (background check, skill assessment, interview, training) and no profile field list [C, weak].
- Thumbtack pro profile: services, specialities, years in business, employee count, licences with a licence badge, background-check badge, weekly business hours, payment methods, rating, review count, hires, response time, social links [C, 2026-10-06, snippet plus scraper pages].
- TaskRabbit: tasks done per category, tools and vehicles, hourly minimums, Elite flag [P].
- Justdial (scraper descriptions only): name, phone, address, area, city, category, rating, review count, verified flag, WhatsApp numbers, lat/long, pincode; year established, services, amenities and payment options also named [C but S-grade: Justdial pages themselves did not surface].
- Google Business Profile: service options (onsite services, online estimates), payments, accessibility, attributes change with primary category [P].

**Registers and bodies that hold it**

Pakistan: NAVTTC, TEVTA and PSDF training or certificate records, electrician and gas-fitter licensing where provincial rules exist (UNVERIFIED), local trade associations; no national trade register [P: pakistan_registries note]. India: no common register. Brand authorisation lists (device makers) for repair shops (UNVERIFIED).

**Gating and sensitivity**

Individuals (electricians, carpenters, masons, locksmiths, handymen, gas and geyser repair, furniture assembly): relay-only contact, area-only location, consent required, no company page (Q-S2). Home-entry trades (locksmiths, maids) show a police-check flag only, never the certificate.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `provider_mode` | How the service is delivered | enum | R | P | yes |  | none | own/sur | fixed_premises, mobile_on_site, both |
| `trades` | Trades and services offered | concept_list | R | P | yes | yes | none | own/agt | plumbing, AC repair, mobile screen replacement |
| `brands_serviced` | Brands serviced | concept_list | O | P | yes |  | none | own | devices, vehicles, appliances |
| `visit_charge` | Visit or inspection charge | money | S | L |  |  | none | own/sur | say whether waived on booking |
| `starting_price` | Typical starting price | money | S | L |  |  | none | own/sur | per-service prices are child records |
| `rate_unit` | Rate basis | enum | S | L |  |  | none | own | fixed, from, hourly, per_visit, per_day |
| `prices_checked_on` | Prices checked on | date | S | L |  |  | none | sur | mandatory whenever any price is held |
| `emergency_service` | Emergency call-out | bool | S | P | yes |  | none | own/sur |  |
| `same_day_available` | Same-day service | bool | O | P | yes |  | none | own |  |
| `parts_policy` | Parts policy | enum | O | P |  |  | none | own | provider_supplies, customer_supplies, both |
| `warranty_days` | Warranty on work (days) | number | S | P | yes |  | none | own | Urban Company shows 30 days |
| `years_in_trade` | Years in trade | number | S | P |  |  | none | own |  |
| `trade_licence` | Trade licence or certificate | identifier_list | O | P |  |  | none | reg/own | required for regulated trades (gas, electrical) once a register is found |
| `training_certificates` | Training or manufacturer authorisation | identifier_list | O | L |  |  | none | own/sur | NAVTTC, TEVTA, brand authorisation |
| `identity_checked` | Identity checked | bool | S | P | yes |  | personal | sur | fact and date only; never the ID number |
| `police_check_passed` | Police check passed | bool | O | P | yes |  | personal | sur | flag and date; home-entry trades |
| `team_size` | Team size | enum | O | L |  |  | none | own | solo, 2_5, 6_20, 20_plus |
| `insurance_cover` | Liability insurance | bool | O | L |  |  | none | own |  |
| `gender_self_declared` | Gender (self-declared) | enum | O | P | yes |  | personal | own | optional; customers filter on it |

### 6.2 Construction and design firms (contractors, architects, engineers, valuers, surveyors, consultants)

Family key `construction_and_design_firms`. Entity: business. Template applies to 9 list types:
General and civil contractors; Architects and designers; Interior designers; Civil, structural and MEP engineers; Quantity surveyors and valuers; Surveyors and land services; Engineering consultants (specialised); General contractors, builders, design-build firms; Architects; interior designers.

**What established platforms hold**

- Houzz Pro: category, licence number with a Verified License status, areas served, typical job cost range, awards [P, 2 pages].
- Checkatrade: 12 checks incl. qualifications, credit check, trading history, public liability insurance proof, ID, 5 references called, minimum 2 years in trade [P, S-grade, 3 sources].
- Angi: certified if rating at least 3, owner background check within 2 years, licences maintained [P].
- PEC register (Pakistan): constructor categories C-A, C-B, C-1 to C-6 and operator categories O-A to O-6, renewal by 31 March; figures UNVERIFIED as current [P].
- ThomasNet and Clutch carry capability or service-line profiles for B2B engineering firms (see manufacturers and agencies families).

**Registers and bodies that hold it**

PEC (constructors, engineers, consultants), PCATP for architects and town planners (UNVERIFIED), SECP (company), FBR Active Taxpayer List, PPRA and EPADS enlistment, development authority enlistments (LDA, CDA, DHA). Public availability of the PEC register in bulk is not confirmed [P].

**Gating and sensitivity**

Sole-practitioner architects, engineers and valuers are named individuals (consent, area only). Client names on past projects only with consent. Litigation and blacklisting fields are not collected until sourced (defamation risk).

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `practice_type` | Practice type | enum | R | P | yes | yes | none | own/reg | contractor, architect, interior_designer, engineer, quantity_surveyor, valuer, land_surveyor, consultant, inspector |
| `professional_registrations` | Regulator registrations | identifier_list | S | P |  |  | none | reg | PEC, PCATP, ICAP and so on; number, category, validity |
| `registration_category` | Registration category or class | text | S | P | yes |  | none | reg | for example C-A to C-6 |
| `fields_of_work` | Fields of work | concept_list | R | P | yes |  | none | reg/own | civil, electrical, mechanical, MEP, interiors |
| `work_types` | Work types | concept_list | R | P | yes |  | none | own | residential, commercial, roads, renovation |
| `project_size_band` | Typical project size | enum | S | P | yes |  | none | own/reg | small, medium, large |
| `project_value_min` | Typical project value from | money | O | L |  |  | commercial | own | Houzz shows a cost range |
| `project_value_max` | Typical project value to | money | O | L |  |  | commercial | own |  |
| `insurance_verified` | Public liability insurance verified | bool | S | P | yes |  | none | sur | with expiry in the check record |
| `years_trading` | Years trading | number | S | P |  |  | none | reg | derived from registration where possible |
| `references_checked` | References checked by us | number | O | P |  |  | none | sur | count, Checkatrade-style |
| `past_projects_consented` | Past projects shown with consent | number | O | L |  |  | commercial | own | count only; projects are child records with proof link |
| `key_equipment` | Key equipment owned | concept_list | O | L |  |  | none | own/sur |  |
| `engineers_on_staff` | Registered engineers on staff | number | O | L |  |  | none | own |  |
| `quality_certifications` | ISO and safety certificates | identifier_list | O | L | yes |  | none | own/reg | ISO 9001, 14001, 45001 |
| `enlisted_with` | Enlisted with authorities | concept_list | O | P | yes |  | none | reg | PPRA, EPADS, LDA, CDA |

### 6.3 Real estate agents, developers, projects and housing societies

Family key `real_estate_agents_and_developers`. Entity: business or person. Template applies to 4 list types:
Real estate agents and developers; New-build projects, housing societies, plot maps; Real estate agents, agencies, developers, builders; Property managers, landlords, photographers, stagers, mortgage lenders.

**What established platforms hold**

- Zameen agency pages: agency name, team members and roles, about text, areas of operation, properties for sale and for rent counts, free or premium status; profiles reviewed by Zameen editorial staff [C+P, 2026-10-06 and Oct 5].
- Property Finder (UAE): verified status, broker licence (BRN/RERA) checked against the regulator, languages, year experience began, active listings, rating [P].
- Zameen project and society pages: field list not confirmed in this session [UNVERIFIED]. Approvals in Pakistan run through layout plan approval then NOC from the authority (CDA, LDA) [C, Zameen news snippet].

**Registers and bodies that hold it**

Development authorities (CDA, LDA, RDA and so on) for approved schemes and NOCs; provincial real estate regulatory authorities (Punjab and Islamabad created them, UNVERIFIED); SECP for developers; ABAD for builders [P]. No national agent licence confirmed.

**Gating and sensitivity**

Individual agents are named persons (consent, relay contact). Show approval status of schemes as a dated fact with the authority name, never as 'legal' or 'illegal'.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `business_role` | Business role | enum | R | P | yes | yes | none | own/agt | agency, agent, developer, builder, property_manager, mortgage_lender, stager_photographer, project, housing_society |
| `agency_name` | Agency name | text | S | P |  |  | none | own | for agents working under an agency |
| `licence` | Agent or developer licence | identifier_list | S | P |  |  | none | reg | only where a regulator exists |
| `listing_types` | Listing types handled | concept_list | R | P | yes |  | none | own | sale, rent, commercial, plots, new_projects |
| `areas_served` | Areas and societies served | place_list | R | P | yes |  | none | own |  |
| `years_experience` | Years of experience | number | S | P |  |  | none | own |  |
| `active_listings_count` | Active listings | number | O | P |  |  | none | auto | derived from listings, never typed |
| `approval_authority` | Scheme approving authority | text | S | P |  |  | none | reg | projects and societies |
| `approval_status` | Approval status | enum | S | P | yes |  | none | reg | approved, layout_approved, applied, not_found, unknown; dated |
| `project_stage` | Project stage | enum | O | P | yes |  | none | own/sur | planning, under_construction, ready, completed |
| `possession_year` | Possession year | number | O | P |  |  | none | own |  |
| `total_area_acres` | Scheme area (acres) | number | O | L |  |  | none | reg/own |  |
| `plot_sizes` | Plot sizes offered | concept_list | O | P | yes |  | none | own | marla and kanal sizes |
| `payment_plan_offered` | Instalment plan offered | bool | O | P | yes |  | none | own |  |
| `languages_spoken` | Languages spoken | concept_list | O | P | yes |  | personal | own |  |

### 6.4 Property listings (for sale, to rent, share, swap, hostels, parking)

Family key `property_listings`. Entity: listing. Template applies to 2 list types:
Property for sale, residential and commercial; Property to rent, share or swap; hostels; parking.

**What established platforms hold**

- Zameen listings (via scraper descriptions): title, price in PKR, bedrooms, bathrooms, area with unit (marla, kanal, sqft, sqm), location, city, type (house, apartment, plot), purpose (sale or rent), date added, agency, contact, lat/long, description, amenities; instalment listings add initial amount, monthly instalment, remaining instalments [C, S-grade].
- Zameen listing verification mark (blue or green check) [P, UNVERIFIED].
- Property Finder: verified agent badge and total active listings [P].

**Registers and bodies that hold it**

Land records (provincial revenue departments, Punjab Land Records Authority style) are not open to bulk reuse (UNVERIFIED). Housing society approvals as in the agents family.

**Gating and sensitivity**

Individual landlords and sellers are private persons: exact address hidden, contact by relay. Listings expire (default 60 days) and drop to hidden unless re-confirmed; stale listings are the main failure of classifieds [INFERENCE].

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `purpose` | Purpose | enum | R | P | yes |  | none | own | sale, rent, share, swap |
| `property_type` | Property type | enum | R | P | yes | yes | none | own | house, apartment, plot, commercial, room, hostel_bed, parking, farm |
| `asking_price` | Price or rent | money | R | L |  |  | none | own | price date is the listing date; open question whether price is free (see section 10) |
| `price_date` | Price date | date | R | L |  |  | none | auto |  |
| `price_negotiable` | Negotiable | bool | O | L |  |  | none | own |  |
| `rent_period` | Rent period | enum | O | L |  |  | none | own | day, month, year |
| `security_deposit` | Security deposit | money | O | L |  |  | none | own |  |
| `area_size` | Area size | number | R | P | yes |  | none | own |  |
| `area_unit` | Area unit | enum | R | P | yes |  | none | own | marla, kanal, sqft, sqm, sqyd, acre |
| `bedrooms` | Bedrooms | number | S | P | yes |  | none | own |  |
| `bathrooms` | Bathrooms | number | S | P | yes |  | none | own |  |
| `furnishing` | Furnishing | enum | O | P | yes |  | none | own | furnished, semi, unfurnished |
| `floor_number` | Floor | number | O | P |  |  | none | own |  |
| `construction_year` | Construction year | number | O | P |  |  | none | own |  |
| `possession_status` | Possession status | enum | O | P | yes |  | none | own | ready, under_construction, off_plan |
| `instalment_plan` | Instalments available | bool | O | P | yes |  | none | own | Zameen shows this |
| `initial_amount` | Initial amount | money | O | L |  |  | none | own |  |
| `monthly_instalment` | Monthly instalment | money | O | L |  |  | none | own |  |
| `remaining_instalments` | Remaining instalments | number | O | L |  |  | none | own |  |
| `amenities` | Amenities | concept_list | O | P | yes |  | none | own | gas, electricity, parking, lift |
| `listed_by_seller_type` | Listed by | enum | R | P | yes |  | personal | own | owner, agent, developer |
| `listing_expires_on` | Listing expires | date | R | P |  |  | none | auto | freshness rule |
| `documents_checked` | Ownership documents checked | bool | O | P | yes |  | none | sur | fact and date only |

### 6.5 Medical practitioners (doctors, dentists, therapists, nurses, hakeems, dietitians)

Family key `medical_practitioners`. Entity: person. Template applies to 14 list types:
General practitioners and clinics [h]; Eye doctors / ophthalmologists [ih]; Dentists [h]; Paediatricians [ih]; Other specialist doctors [ih]; Physiotherapists and rehab [h]; Mental health [ih]; Hakeem and homeopathic [ih]; Dieticians and nutrition [i]; Doctors and specialists by specialty [ih]; Eye doctors and eye care [h]; Dentists and dental practices [h]; Physiotherapists, psychologists, dietitians, audiologists [ih]; Nurses, nurse practitioners, physician assistants [ih].

**What established platforms hold**

- Practo: its own doctor pages did not surface in two sessions. Aggregators that copy the same shape (Credihealth, Bajaj Finserv Health, Drlogy) show qualifications, years of experience, medical council registration number, specialisation, consultation fee by mode and clinic, clinic address and timings, services, languages, memberships [C, 2026-10-06, S-grade]. Practo clinic and hospital pages show timings, services, facilities (ICU, CCU, lab, blood bank, CT) and doctors [C].
- Oladoc and Marham (Pakistan): PMDC-verified flag, years of experience, fee in PKR per location, qualifications, video consultation, reviews with sub-scores, wait time [P, 2+ sources].
- Zocdoc: gender, NPI, languages, insurance, board certification, accepting new patients, earliest availability [P].
- NPPES/NPI registry fields: credential, taxonomy code, state licence, gender, practice address [P].
- schema.org MedicalOrganization has isAcceptingNewPatients and healthPlanNetworkId [P].

**Registers and bodies that hold it**

PMDC (doctors and dentists; online lookup by registration number or name shows validity and qualifications, single-record search, personal data so verify-only), CPSP, Pakistan Nursing Council and Pakistan Pharmacy Council (UNVERIFIED), national homoeopathic and unani councils (UNVERIFIED). Abroad: NPPES (US), GMC (UK, UNVERIFIED) [P].

**Gating and sensitivity**

Named individuals: consent, area-only location, relay contact (Q-S2). All fee fields are health prices: nothing collected or shown until the health rules are adopted (Q-S1). Do not hold patient reviews that reveal conditions. Doctor negligence or complaint records only as links to official public decisions.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `system_of_medicine` | Discipline | enum | R | P | yes | yes | none | reg/own | allopathic, dental, homeopathic, unani, ayurvedic, physiotherapy, psychology, nursing, nutrition, audiology, optometry |
| `specialty` | Specialty | concept_list | R | P | yes |  | none | reg/own | primary specialty; taxonomy code where one exists |
| `sub_specialties` | Sub-specialties | concept_list | O | P | yes |  | none | own | for example retina, cornea, glaucoma |
| `qualifications` | Qualifications | text | S | P |  |  | none | reg/own | degree, institution, year; PMDC lookup shows these |
| `regulator_registration` | Regulator registration | identifier_list | S | P |  |  | none | reg | PMDC and similar; number, status, validity; number is public-register data |
| `registration_checked_on` | Registration checked on | date | S | P |  |  | none | reg |  |
| `years_experience` | Years of experience | number | S | P | yes |  | none | reg/own | derive from first registration where the register gives it |
| `conditions_treated` | Conditions or procedures | concept_list | O | P | yes |  | none | own |  |
| `appointment_mode` | Appointment mode | enum | S | P | yes |  | none | own | walk_in, appointment, both |
| `video_consultation` | Video consultation | bool | O | P | yes |  | none | own | Oladoc and Marham show it |
| `home_visit` | Home visits | bool | O | P | yes |  | none | own |  |
| `accepting_new_patients` | Accepting new patients | bool | O | P | yes |  | none | own | Zocdoc and schema.org |
| `consultation_fee` | Consultation fee (typical) | money | S | L |  |  | health_price | own/sur | fee belongs to the doctor-location pair; child records per location |
| `followup_fee` | Follow-up fee | money | O | L |  |  | health_price | own |  |
| `video_fee` | Video consultation fee | money | O | L |  |  | health_price | own |  |
| `fee_checked_on` | Fee checked on | date | S | L |  |  | health_price | sur | mandatory with any fee |
| `insurance_panels` | Insurance and panels | concept_list | O | L | yes |  | none | own |  |
| `memberships` | Professional memberships | concept_list | O | P |  |  | none | own/reg | CPSP, PMA, specialty societies |
| `gender_self_declared` | Gender (self-declared) | enum | O | P | yes |  | personal | own | optional; patients filter on it |

### 6.6 Health facilities and services (hospitals, clinics, maternity, care homes, ambulance, blood banks, vets)

Family key `health_facilities`. Entity: facility. Template applies to 10 list types:
Eye hospitals [h]; Gynaecologists and maternity [h]; Hospitals [h]; Veterinary clinics [h]; Ambulance and blood services [h]; Hospitals, clinics, GP surgeries [h]; Hospitals ranked by specialty or accreditation [h]; Care homes; mental, sexual-health, pregnancy, vaccination services [h]; Vets, pet groomers, boarders, walkers, shelters [h]; Ambulance and blood banks [h].

**What established platforms hold**

- Practo clinic and hospital pages: location, facility type, doctors, timings, services, facilities such as ICU, CCU, laboratory, blood bank, CT scan [C, 2026-10-06].
- HealthWire/hospital sites: OPD timings by weekday, doctor count, per-speciality department pages [P, S-grade].
- NABH (India) accreditation registry records scope of accreditation by clinical services, diagnostics, support services [P].
- schema.org Hospital/MedicalClinic: availableService, medicalSpecialty, isAcceptingNewPatients, healthPlanNetworkId [P].
- Bed counts, procedure prices, equipment lists and complaint records: not found as standard live fields [P: kept as later or inference].

**Registers and bodies that hold it**

Provincial healthcare commissions (PHC Punjab licence verification is a public per-licence lookup, KP HCC, SHCC Sindh, IHRA Islamabad), DRAP, PNRA for radiation sources, opendata.com.pk for public facilities (CSV), NABH and JCI accreditor lists [P]. Veterinary: provincial veterinary councils (UNVERIFIED).

**Gating and sensitivity**

Procedure and service prices are health prices (Q-S1). Care homes and mental, sexual-health, pregnancy and vaccination services reveal sensitive status by association: list the facility only, never visitors, and no reviews that name conditions. Complaint records: link to official decisions only.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `facility_type` | Facility type | enum | R | P | yes | yes | none | reg/own | hospital, clinic, dispensary, specialist_centre, day_surgery, maternity_home, care_home, ambulance_service, blood_bank, vet_clinic, pet_service, vaccination_centre, mental_health_centre |
| `ownership` | Ownership | enum | S | P | yes |  | none | reg/own | public, private, charity, military, teaching |
| `facility_licence` | Healthcare licence | identifier_list | S | P |  |  | none | reg | commission, number, validity; required for regulated types |
| `accreditations` | Accreditations | identifier_list | O | P | yes |  | none | reg/own | body, scope, expiry (NABH shows scope) |
| `departments` | Departments and OPD specialities | concept_list | R | P | yes |  | none | own/sur | each with own OPD timings as child records |
| `emergency_24x7` | Emergency 24x7 | bool | S | P | yes |  | none | own/sur |  |
| `procedures_offered` | Procedures and services | concept_list | O | P | yes |  | none | own | schema.org availableService |
| `procedure_price_from` | Typical procedure price from | money | O | L |  |  | health_price | own/sur | later; no live evidence it is a standard field |
| `price_checked_on` | Price checked on | date | O | L |  |  | health_price | sur |  |
| `doctor_count` | Doctors on roster | number | O | P |  |  | none | auto | derived from roster links |
| `bed_count` | Beds (total) | number | O | L |  |  | none | own | later; hard to verify |
| `insurance_panels` | Insurance and panels | concept_list | O | L | yes |  | none | own |  |
| `charity_or_zakat` | Free or zakat-eligible care | bool | O | P | yes |  | none | own | Pakistan relevance [INFERENCE] |
| `patient_facilities` | Patient facilities | concept_list | O | P | yes |  | none | sur | pharmacy, lab, parking, prayer area, wheelchair access |
| `online_reports` | Online reports | bool | O | P | yes |  | none | own |  |
| `ambulance_types` | Ambulance types | concept_list | O | P | yes |  | none | own | ambulance services only |
| `ambulance_coverage` | Ambulance coverage | place_list | O | P | yes |  | none | own |  |
| `species_served` | Animals treated | concept_list | O | P | yes |  | none | own | vets and pet services only |

### 6.7 Diagnostics and imaging (labs, MRI/CT/X-ray centres, installed machines)

Family key `diagnostics_and_imaging`. Entity: facility or equipment record. Template applies to 5 list types:
Diagnostic labs [h]; MRI, CT and radiology centres [h]; Diagnostic and pathology labs with test prices; collection points [h]; Imaging centres (MRI, CT, X-ray, ultrasound) [h]; Installed medical machines (MRI, CT, PET) [h].

**What established platforms hold**

- Oladoc and Marham lab pages: per-test price and discount, fasting requirement per test, free home sample collection, sample-transport fee, report access [P].
- Chughtai, Husaini and Aga Khan lab pages: test catalogue, branch counts, PNAC certification, online reports [P, S-grade, prices undated].
- Practo labs: tests and packages, free home sample collection, reports within 24 hours [C, 2026-10-06].
- Machine make, model, field strength, install year, licence: not a standard platform field [P: Entry template note]; it is a deliberate AllLists addition (C21).

**Registers and bodies that hold it**

PNRA licences for X-ray, CT and nuclear medicine, provincial healthcare commissions for lab licences, PNAC (ISO 15189 and ISO 17025 accreditation, name from [P] note UNVERIFIED), CAP and NABL abroad [P].

**Gating and sensitivity**

Test, scan and package prices are health prices (Q-S1): hold nothing until the rules are adopted, then always with currency and price date. Patient-level data is never held. The installed-machine record is an equipment record linked to its hosting centre.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `centre_type` | Centre type | enum | R | P | yes | yes | none | own/reg | laboratory, imaging, both, collection_point, machine_record |
| `modalities` | Modalities | concept_list | R | P | yes |  | none | own/sur | MRI, CT, X-ray, ultrasound, DEXA, mammography, PET, ECG, echo |
| `disciplines` | Lab disciplines | concept_list | O | P | yes |  | none | own | pathology, microbiology, histopathology |
| `home_collection` | Home sample collection | bool | S | P | yes |  | none | own |  |
| `home_collection_fee` | Home collection fee | money | O | L |  |  | health_price | own |  |
| `report_turnaround_hours` | Report turnaround (hours) | number | O | P |  |  | none | own |  |
| `online_reports` | Online reports | bool | O | P | yes |  | none | own |  |
| `referral_required` | Doctor referral | enum | O | P | yes |  | none | own | required, not_required, either |
| `radiation_licence` | Radiation licence | identifier_list | S | P |  |  | none | reg | PNRA; imaging only |
| `accreditations` | Lab accreditations | identifier_list | O | P | yes |  | none | reg/own | ISO 15189, PNAC, CAP |
| `mri_field_strength_tesla` | MRI field strength (T) | number | O | P | yes |  | none | own/sur | 1.5 or 3; one per machine record |
| `equipment_count` | Machines in centre | number | O | P |  |  | none | own/sur | child records hold make, model, install year |
| `test_price_from` | Typical test price from | money | O | L |  |  | health_price | own/sur | catalogue prices are child records |
| `contrast_surcharge` | Contrast surcharge | money | O | L |  |  | health_price | own |  |
| `price_checked_on` | Prices checked on | date | O | L |  |  | health_price | sur | mandatory |
| `insurance_panels` | Insurance and corporate rates | concept_list | O | L | yes |  | none | own |  |
| `machine_make` | Machine make | text | O | P | yes |  | none | own/sur | machine_record only |
| `machine_model` | Machine model | text | O | P |  |  | none | own/sur | machine_record only |
| `machine_install_year` | Machine install year | number | O | P |  |  | none | own | machine_record only |
| `machine_status` | Machine status | enum | O | P | yes |  | none | own | operational, down, decommissioned; machine_record only |
| `services_supported` | Scans supported by machine | concept_list | O | P | yes |  | none | own | machine_record only |

### 6.8 Pharmacies, medical stores and opticians

Family key `pharmacy_and_optical`. Entity: business. Template applies to 3 list types:
Pharmacies [h]; Opticians and optical shops [h]; Pharmacies and medical stores [h].

**What established platforms hold**

- Google Business Profile attributes for pharmacies: wheelchair access, drive-through, delivery and pickup service options, payments [P, S-grade].
- Justdial and Practo pharmacy fields: not found [P].
- Drug licence number and pharmacist-in-charge appear on no platform checked; kept because regulators require them [P: inference].

**Registers and bodies that hold it**

DRAP and provincial drug inspectors (licence per outlet; online verification not confirmed), Pakistan Pharmacy Council (UNVERIFIED) [P].

**Gating and sensitivity**

No patient prescription or order data. Pharmacist name is a named individual (L, consent).

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `outlet_type` | Outlet type | enum | R | P | yes | yes | none | own/agt | pharmacy, medical_store, chain_outlet, optician, optical_shop, hearing_aid_centre |
| `brand` | Chain or brand | text | O | P | yes |  | none | own/agt |  |
| `drug_licence` | Drug licence | identifier_list | S | P |  |  | none | reg/sur | number, issuer, validity |
| `pharmacist_in_charge_registered` | Pharmacist in charge registered | bool | O | P | yes |  | none | reg |  |
| `pharmacist_name` | Pharmacist in charge | text | O | L |  |  | personal | own/reg | named person |
| `open_24x7` | Open 24x7 | bool | S | P | yes |  | none | own/sur |  |
| `home_delivery` | Home delivery | bool | S | P | yes |  | none | own |  |
| `drive_through` | Drive-through | bool | O | P | yes |  | none | own |  |
| `prescription_service` | Prescription fulfilment | bool | O | P | yes |  | none | own |  |
| `cold_chain` | Cold-chain storage | bool | O | P | yes |  | none | own |  |
| `controlled_drug_licence` | Controlled-drug licence | bool | O | L |  |  | none | reg |  |
| `categories_stocked` | Categories stocked | concept_list | O | P | yes |  | none | own | generics, surgical, baby, OTC |
| `eye_test_available` | Eye test on site | bool | O | P | yes |  | none | own | opticians |
| `optometrist_on_site` | Qualified optometrist on site | bool | O | P | yes |  | none | own | opticians |
| `brands_stocked` | Frame and lens brands | concept_list | O | P | yes |  | none | own | opticians |
| `insurance_panels` | Panels accepted | concept_list | O | L | yes |  | none | own |  |

### 6.9 Education institutions (schools, colleges, universities, coaching, vocational, madrasas, Quran academies, driving schools, daycare)

Family key `education_institutions`. Entity: institution. Template applies to 14 list types:
Schools; Colleges and universities; Madrasas and hifz schools [c]; Coaching centres and academies; Vocational training institutes; Daycare and play groups [c]; Driving schools; Schools, with board and district; Colleges, universities, courses, exams, rankings, study abroad; Coaching centres, vocational and computer training; Quran academies (Tajweed, Hifz, Noorani Qaida) [c]; Madrasas by wafaq board [c]; Driving schools and instructors; Daycare, preschools, babysitters, nannies, carers [c].

**What established platforms hold**

- Niche K-12: tuition, boarding cost, school type, grade levels, religious affiliation, acceptance rate, student-teacher ratio, clubs, survey scores [P, 2 pages].
- GreatSchools: summary rating from test score, progress, equity (US state data; not replicable in Pakistan) [P].
- doris.school (Pakistan): curriculum, boys-only or co-ed, day or boarding, age range, campuses, annual tuition range [P, S-grade, figures undated].
- Care.com and Superprof cover individual carers and tutors, see other families [C].

**Registers and bodies that hold it**

PEIRA (Islamabad private schools), provincial school education departments and private school regulatory authorities, BISE boards (affiliation), HEC recognised universities (179, list page), NAVTTC and TEVTA (vocational), five wafaq boards for madrasas, NEMIS statistics for sizing [P].

**Gating and sensitivity**

Daycare, preschools, madrasas, hifz schools and Quran academies are child-facing: safeguarding fields are required before publishing; no child names, photos or reviews that identify a child; staff names are L. Fees need fee year.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `institution_type` | Institution type | enum | R | P | yes | yes | none | reg/own | school, college, university, coaching_centre, vocational_institute, madrasa, quran_academy, driving_school, daycare, preschool, language_centre |
| `registration` | Registration and recognition | identifier_list | S | P |  |  | none | reg | authority, ID, validity; required where a register exists |
| `board_affiliation` | Board or affiliation | concept_list | S | P | yes |  | none | reg/own | BISE, Cambridge, IB, wafaq board, HEC |
| `curriculum` | Curriculum | concept_list | S | P | yes |  | none | own | Matric/FSc, O/A level, Montessori, Hifz, Dars-e-Nizami |
| `grades_offered` | Grades or levels offered | text | R | P | yes |  | none | own/sur | shown on the row |
| `programmes` | Programmes and courses | concept_list | O | P | yes |  | none | own | colleges, vocational, language centres |
| `gender_mix` | Gender | enum | S | P | yes |  | none | own | boys, girls, co_education |
| `day_or_boarding` | Day or boarding | enum | O | P | yes |  | none | own | day, boarding, both |
| `medium_of_instruction` | Medium of instruction | concept_list | O | P | yes |  | none | own |  |
| `age_min_years` | Youngest age taken (years) | number | O | P | yes |  | none | own | daycare, preschool |
| `age_max_years` | Oldest age taken (years) | number | O | P |  |  | none | own |  |
| `monthly_fee` | Monthly tuition | money | S | L |  |  | none | own/sur |  |
| `admission_fee` | Admission fee | money | O | L |  |  | none | own |  |
| `fee_year` | Fee year | number | S | L |  |  | none | own/sur | mandatory with any fee |
| `concessions_offered` | Scholarships or concessions | bool | O | P | yes |  | none | own |  |
| `campuses` | Campuses | number | O | P |  |  | none | own |  |
| `student_count_band` | Students (band) | enum | O | L |  |  | none | own |  |
| `student_teacher_ratio` | Student-teacher ratio | number | O | L |  |  | none | own |  |
| `facilities` | Facilities | concept_list | O | P | yes |  | none | sur | lab, library, transport, hostel |
| `admissions_open` | Admissions open | bool | O | P | yes |  | none | own | dated |
| `child_protection_policy` | Child protection policy | bool | S | P | yes |  | child | own/sur | required for child-facing types |
| `staff_background_checked` | Staff background-checked | bool | S | P | yes |  | child | sur | flag and date only |
| `staff_child_ratio` | Staff to child ratio | number | O | L |  |  | child | own | daycare |

### 6.10 Tutors and instructors (academic, test-prep, language, music, art, sports, Quran, driving)

Family key `tutors_and_instructors`. Entity: person (or small firm). Template applies to 7 list types:
Quran tutors [ic]; Academic tutors [ic]; Language teachers [i]; Music, art and sports coaches; Academic and test-prep tutors [ic]; Language, music, art and sports teachers [i]; Quran tutors (individual) [ic].

**What established platforms hold**

- Wyzant profiles: hourly rate, background-check status shown even as 'none', approved subjects, travel radius, lesson type, cancellation notice, education [P, 2 profiles].
- Superprof: price, rating, review count, response time, face-to-face or online, free first lesson, level taught; Quran teachers state ijazah, Tajweed, Hifz, Nazra, translation, riwayat, ages [P, 2+ sources].
- Preply: bio, headshot, intro video, certificate upload with a platform badge, team review [P, S-grade].
- Care.com style carer fields are in the domestic family [C].
- Tutor gender and 'students' gender accepted' appear on no checked platform; they are Pakistan and Gulf practice [INFERENCE].

**Registers and bodies that hold it**

No tutor register. Ijazah and sanad are checked from the issuing institution or teacher (manual). Teaching degrees: HEC attestation is a possible check (UNVERIFIED). Driving instructors: provincial licensing (UNVERIFIED).

**Gating and sensitivity**

Child-facing and the highest-risk family. Not public until safeguarding and relay-only contact are designed; schools and centres first (Q-S2). No home address, no personal mobile, no reviews naming a child, no demo video of children. Safeguarding status shown as 'none' rather than hidden.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `subjects` | Subjects taught | concept_list | R | P | yes | yes | child | own | row descriptor |
| `levels` | Levels | concept_list | S | P | yes |  | child | own |  |
| `exam_prep` | Exam preparation | concept_list | O | P | yes |  | child | own | MDCAT, ECAT, IELTS, SAT |
| `quran_subjects` | Quran subjects | concept_list | O | P | yes |  | child | own | Nazra, Tajweed, Hifz, translation, riwayat; Quran tutors only |
| `teaching_modes` | Teaching modes | concept_list | S | P | yes |  | child | own | home_visit, online, tutor_place, centre |
| `travel_radius_km` | Travel radius (km) | number | O | P | yes |  | personal | own | from area centroid, not from home |
| `hourly_rate` | Hourly rate | money | S | L |  |  | none | own |  |
| `trial_class` | Trial lesson | enum | O | P | yes |  | none | own | free, paid, none |
| `qualifications` | Qualifications | text | S | P |  |  | personal | own/sur | degrees, ijazah, sanad |
| `qualification_checked` | Qualification document checked | bool | S | P | yes |  | none | sur | fact and date |
| `ijazah_checked` | Ijazah or sanad checked | bool | O | P | yes |  | none | sur | Quran tutors |
| `years_teaching` | Years teaching | number | S | P | yes |  | none | own |  |
| `class_format` | Individual or group | enum | O | P | yes |  | none | own | individual, group, both |
| `student_age_groups` | Student age groups taken | concept_list | S | P | yes |  | child | own | kids, teens, adults |
| `tutor_gender` | Tutor gender (self-declared) | enum | S | P | yes |  | personal, child | own | filter used for girls' tuition |
| `accepts_student_gender` | Students accepted | enum | O | P | yes |  | personal, child | own | any, girls_only, boys_only |
| `safeguarding_status` | Safeguarding check | enum | R | P | yes |  | child | sur | none, references_checked, police_check_passed; required for child-facing |
| `safeguarding_checked_on` | Safeguarding check date | date | R | P |  |  | child | sur | expires; 2-year rule (Angi pattern) is a suggestion |
| `parent_present_policy` | Parent-present policy | enum | S | P | yes |  | child | own | required, optional, not_applicable |
| `cancellation_notice_hours` | Cancellation notice (hours) | number | O | L |  |  | none | own | Wyzant shows it |

### 6.11 Domestic and care workers (maids, drivers, gardeners, nannies, elder care, guards, housekeepers, home cooks)

Family key `domestic_and_care_workers`. Entity: person (or agency). Template applies to 6 list types:
Maids and cleaners; Drivers and chauffeurs [i]; Gardeners [i]; Security guards and agencies; Nannies and elder care [ic]; Housekeepers, domestic workers, home cooks [i].

**What established platforms hold**

- Care.com: display name, categories, city and postal code, bio, years of experience, hourly rate range, CareCheck completion flag with status and date, care age groups, credentials, languages, CPR/First Aid, pets and smoking, availability by day and time [C, 2026-10-06].
- Urban Company: housekeeping professionals pass background check, skill assessment, interview, training [C, weak].
- TaskRabbit: tasks done per category, tools, vehicles [P].

**Registers and bodies that hold it**

No register for individuals. Security guard agencies: provincial home department or security agency licensing (UNVERIFIED). Drivers: provincial driving licence authority (check fact only, never the number).

**Gating and sensitivity**

Named individuals with access to homes and children or elders: consent, relay contact, area only, police and identity checks as flags only. Care of children or elders is child-related or vulnerable-person data. No company page for individuals.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `roles` | Roles | concept_list | R | P | yes | yes | personal | own | maid, driver, gardener, nanny, elder_carer, cook, guard |
| `employment_type` | Employment type | enum | S | P | yes |  | personal | own | live_in, live_out, part_time, hourly, agency_placed |
| `years_experience` | Years of experience | number | S | P | yes |  | personal | own |  |
| `rate_amount` | Rate | money | S | L |  |  | personal | own | private by default |
| `rate_period` | Rate period | enum | S | L |  |  | personal | own | hour, day, month |
| `duties` | Duties | concept_list | S | P | yes |  | none | own |  |
| `care_for` | Care for | concept_list | O | P | yes |  | child | own | children, elderly, special_needs |
| `first_aid_trained` | First aid trained | bool | O | P | yes |  | none | own |  |
| `driving_licence_checked` | Driving licence checked | bool | O | P | yes |  | personal | sur | drivers; fact only |
| `vehicle_types_driven` | Vehicle types driven | concept_list | O | P | yes |  | none | own |  |
| `identity_checked` | Identity checked | bool | S | P | yes |  | personal | sur | fact and date |
| `police_check_passed` | Police check passed | bool | S | P | yes |  | personal | sur | flag and date |
| `reference_checked` | References checked | bool | O | P | yes |  | personal | sur |  |
| `agency_name` | Placing agency | text | O | P |  |  | none | own |  |
| `security_licence` | Guard agency licence | identifier_list | O | P |  |  | none | reg | agencies only |
| `guards_available` | Guards available | number | O | L |  |  | none | own | agencies only |
| `armed_or_unarmed` | Armed or unarmed | enum | O | P | yes |  | none | own | agencies only |
| `gender_self_declared` | Gender (self-declared) | enum | O | P | yes |  | personal | own | households filter on it |

### 6.12 Professional advisers (lawyers, notaries, accountants, tax and immigration consultants, management and agri advisers)

Family key `professional_advisers`. Entity: person or firm. Template applies to 9 list types:
Lawyers; Corporate and tax lawyers; Notaries and oath commissioners [i]; Accountants and auditors; Tax consultants [i]; Management and business consultants; Immigration and visa consultants; Agronomists and advisers [i]; Lawyers by speciality.

**What established platforms hold**

- Clutch (agencies and consultants): hourly rate band, minimum project size, employees band, founded year, locations, focus areas, industries, client size segments [C, 2026-10-06].
- Thumbtack and Yelp carry lawyers and accountants with licence badge and categories [C, weak].
- Lawyer and accountant register fields (bar number, ICAP membership) from regulators [P].

**Registers and bodies that hold it**

Bar councils (provincial and Pakistan Bar Council), ICAP and ICMAP (member lists), FBR (tax practitioner records, UNVERIFIED), notary appointments by government; abroad: state bars, SRA (UK, UNVERIFIED) [P].

**Gating and sensitivity**

Individuals need consent; fee fields are commercial, not health. Do not publish disciplinary records unless an official public decision is linked with source and date.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `practice_areas` | Practice areas | concept_list | R | P | yes | yes | none | reg/own | corporate, tax, family, criminal, audit, immigration, agriculture |
| `bar_or_body_registration` | Regulator or body registration | identifier_list | S | P |  |  | none | reg | bar council, ICAP, ICMAP; number, status |
| `registration_checked_on` | Registration checked on | date | S | P |  |  | none | reg |  |
| `court_levels` | Court levels | concept_list | O | P | yes |  | none | own | lawyers |
| `qualifications` | Qualifications | text | S | P |  |  | none | reg/own |  |
| `years_practising` | Years practising | number | S | P | yes |  | none | reg |  |
| `consultation_fee` | Consultation fee | money | O | L |  |  | none | own | price date required |
| `fee_basis` | Fee basis | enum | O | P | yes |  | none | own | hourly, fixed, retainer, contingency |
| `free_first_consultation` | Free first consultation | bool | O | P | yes |  | none | own |  |
| `firm_size_band` | Firm size | enum | O | L |  |  | none | own |  |
| `countries_advised` | Countries covered | place_list | O | P | yes |  | none | own | immigration and visa consultants |
| `licence_scheme` | Consultant licence | identifier_list | O | P |  |  | none | reg | immigration and overseas-employment licences where they exist (UNVERIFIED) |
| `notary_appointment` | Notary appointment | identifier_list | O | P |  |  | none | reg | notaries and oath commissioners |

### 6.13 Financial providers (banks, microfinance, money changers, remittance, insurers and agents, planners, mortgage lenders)

Family key `financial_providers`. Entity: business or person. Template applies to 5 list types:
Banks and branches; Insurance agents [i]; Money changers and remittance; Loan and microfinance providers; Accountants, tax specialists, financial planners, banks, insurers.

**What established platforms hold**

- schema.org BankOrCreditUnion and LocalBusiness carry hours, geo, paymentAccepted, priceRange [P, snippet].
- Branch locators on bank sites are the primary live source; Justdial and Google list branches with hours and ATMs [P, UNVERIFIED].
- No platform checked publishes live exchange rates as a stable field; rates are volatile and are not stored.

**Registers and bodies that hold it**

State Bank of Pakistan (banks, exchange companies, microfinance banks, licensed lists), SECP (insurers, NBFCs, insurance agents), PMRC for housing finance (UNVERIFIED) [P: partly].

**Gating and sensitivity**

Exchange and loan rates are not stored (stale within a day). Individual insurance agents and financial planners are named persons.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `provider_type` | Provider type | enum | R | P | yes | yes | none | reg/own | bank_branch, microfinance, money_changer, remittance_agent, insurer, insurance_agent, financial_planner, mortgage_lender |
| `institution_name` | Institution or brand | text | R | P | yes |  | none | reg |  |
| `regulator_licence` | Regulator licence | identifier_list | R | P |  |  | none | reg | SBP, SECP |
| `branch_code` | Branch code | text | O | P |  |  | none | reg |  |
| `atm_available` | ATM on site | bool | O | P | yes |  | none | own/sur |  |
| `services` | Services | concept_list | S | P | yes |  | none | own |  |
| `products` | Products | concept_list | O | P | yes |  | none | own | loan types, policy types |
| `currencies_exchanged` | Currencies exchanged | concept_list | O | P | yes |  | none | own | money changers |
| `insurers_represented` | Insurers represented | concept_list | O | P | yes |  | none | own | agents |
| `shariah_compliant` | Shariah-compliant products | bool | O | P | yes |  | none | own |  |
| `loan_amount_min` | Smallest loan | money | O | L |  |  | none | own |  |
| `loan_amount_max` | Largest loan | money | O | L |  |  | none | own |  |
| `terms_disclosed` | Markup or fees disclosed | bool | O | P | yes |  | none | own |  |

### 6.14 Digital talent and agencies (data scientists, developers, cyber, cloud, creatives, marketers, software houses, agencies, translators, recruiters, researchers, candidates)

Family key `digital_talent_and_agencies`. Entity: person or firm. Template applies to 18 list types:
Recruitment agencies; Translators and interpreters [i]; Data scientists [i]; Software developers; Software houses and agencies; Web designers and SEO; Cybersecurity professionals; Cloud and DevOps engineers [i]; IT support and network installers; Freelance digital creatives [i]; Digital marketing and social media; Data scientists, analysts, ML engineers [i]; Software, web and app developers [i]; Designers, illustrators, writers, translators, video and audio creatives [i]; Digital marketers, virtual assistants, consultants; Software, design and marketing agencies; call centres; Researchers and journals; Candidates, CV databases, profiles by skill [i].

**What established platforms hold**

- Upwork: hourly rate, total earned, job success score, skills, location, availability badge, portfolio, verified flag, agency link, hours worked [C, 2026-10-06, scraper pages].
- Clutch: hourly rate band, minimum project size, employee band, founded year, focus areas, industries, client segments [C].
- G2 and Capterra (software vendors): pricing plans, platforms, support and training options, typical customers, vendor name, location, website, founded year [C].
- GitHub, Kaggle, ORCID, Google Scholar as verifiable profile links [P].

**Registers and bodies that hold it**

No register. Verifiable evidence comes from platform profiles (GitHub, Kaggle, ORCID) and credential IDs; companies from SECP, PSEB (Pakistan Software Export Board, UNVERIFIED), PASHA membership (UNVERIFIED).

**Gating and sensitivity**

Talent list is paused: launch only after a pilot of about 50 consented people and counsel review. Rates, visa and salary expectations private by default and never searchable. Recruiter contact only by opt-in relay.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `role_types` | Role types | concept_list | R | P | yes | yes | none | own/agt | data scientist, ML engineer, web developer, SEO, UX designer, translator |
| `seniority` | Seniority | enum | S | P | yes |  | none | own | junior, mid, senior, lead, principal |
| `skills` | Skills | concept_list | R | P | yes |  | none | own/agt | level and years are child records |
| `years_experience` | Years of experience | number | S | P | yes |  | none | own |  |
| `domains` | Domain experience | concept_list | O | P | yes |  | none | own |  |
| `tools_stack` | Tools and stack | concept_list | O | P | yes |  | none | own |  |
| `engagement_types` | Engagement types | concept_list | S | P | yes |  | none | own | full_time, contract, freelance, advisory |
| `work_mode` | Work mode | enum | S | P | yes |  | none | own | remote, hybrid, on_site |
| `availability` | Availability | enum | S | P | yes |  | none | own | immediate, two_weeks, one_month, unavailable |
| `hours_per_week` | Hours per week | number | O | P |  |  | none | own |  |
| `timezone` | Time zone | text | O | P |  |  | none | own |  |
| `rate_min` | Rate from | money | O | L |  |  | personal | own | private by default |
| `rate_max` | Rate to | money | O | L |  |  | personal | own |  |
| `rate_unit` | Rate unit | enum | O | L |  |  | personal | own | hour, day, month, project |
| `verified_profiles` | Verified profiles | concept_list | S | P | yes |  | none | auto | GitHub, Kaggle, ORCID, Scholar; owner control proven by link-back |
| `profile_links` | Portfolio links | text | O | L |  |  | none | own | public links only |
| `credentials` | Certifications | identifier_list | O | L |  |  | none | own | credential ID and issuer |
| `publications_count` | Publications | number | O | L |  |  | none | agt | from ORCID or DOI |
| `education` | Education | text | O | L |  |  | personal | own |  |
| `client_industries` | Industries served | concept_list | O | P | yes |  | none | own | agencies |
| `min_project_size` | Minimum project size | money | O | L |  |  | none | own | agencies; Clutch field |
| `team_size_band` | Team size | enum | O | L |  |  | none | own | agencies |
| `open_to_relocate` | Open to relocate | bool | O | H |  |  | personal | own |  |
| `work_authorisation` | Work authorisation | text | O | H |  |  | personal | own | private, not searchable |
| `recruiter_opt_in` | Recruiters may contact | bool | R | I |  |  | personal | own | default false |

### 6.15 Opportunity posts (jobs, customer requests, buy leads, RFQs, tenders, businesses for sale, events)

Family key `opportunity_posts`. Entity: listing. Template applies to 5 list types:
Importers and buyers; buy leads, RFQs, tenders; Businesses for sale; Job vacancies and employers with reviews and salaries; Customer requests (jobs, projects, care jobs); Events, festivals, what's on.

**What established platforms hold**

- schema.org JobPosting: title, employmentType, baseSalary, jobLocation, validThrough, hiringOrganization, experienceRequirements [C, 2026-10-06].
- Eventbrite: name, description, date range, venue, geo, category and subcategory, tags (up to 10), organiser, currency, min and max ticket price, free flag, refund policy, online events [C].
- IndiaMART buy leads, Alibaba RFQs, Pakistan Trade Portal and PPRA/EPADS tenders hold the buyer-demand shape (product, quantity, destination, deadline) [P: Pilot trade notes].
- Business-for-sale boards (BizBuySell style) hold asking price, revenue and reason for sale [UNVERIFIED].

**Registers and bodies that hold it**

PPRA/EPADS for public tenders; company registries (SECP) to check the poster. No register for jobs or requests.

**Gating and sensitivity**

Posts expire and drop to hidden at the deadline. Care jobs and household requests reveal a household: show area only and hide requester identity (personal, child where children are mentioned). Salaries are shown only if the employer gave them.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `post_kind` | Post kind | enum | R | P | yes | yes | none | own | job_vacancy, customer_request, buy_lead, rfq, tender, business_for_sale, event |
| `post_title` | Title | text | R | P |  |  | none | own |  |
| `category` | Category | concept_list | R | P | yes |  | none | own |  |
| `post_place` | Place | place_list | R | P | yes |  | none | own |  |
| `deadline` | Deadline or valid through | date | R | P | yes |  | none | own | post expires and is hidden after this date |
| `employment_type` | Employment type | enum | O | P | yes |  | none | own | jobs; schema.org values |
| `experience_required` | Experience required | text | O | P |  |  | none | own |  |
| `salary_min` | Pay from | money | O | L |  |  | none | own | jobs |
| `salary_max` | Pay to | money | O | L |  |  | none | own |  |
| `budget_min` | Budget from | money | O | L |  |  | none | own | requests, RFQs |
| `budget_max` | Budget to | money | O | L |  |  | none | own |  |
| `quantity_text` | Quantity and unit | text | O | L |  |  | none | own | RFQs, buy leads |
| `delivery_place` | Delivery place | place_list | O | P | yes |  | none | own |  |
| `tender_authority` | Tender authority | text | O | P |  |  | none | reg |  |
| `tender_reference` | Tender reference | text | O | P |  |  | none | reg |  |
| `requester_type` | Requester type | enum | S | P | yes |  | personal | own | household, business, institution; household identity never shown |
| `event_start` | Event start | date | O | P | yes |  | none | own | events |
| `event_ticket_price` | Ticket price | money | O | L |  |  | none | own | events; free flag via 0 |
| `asking_price` | Asking price | money | O | L |  |  | none | own | business for sale |
| `annual_revenue_band` | Annual revenue band | enum | O | L |  |  | commercial | own | business for sale |
| `post_status` | Post status | enum | R | P | yes |  | none | own | open, filled, closed |
| `involves_children` | Involves children | bool | S | I |  |  | child | own | care jobs; forces area-only display |

### 6.16 Personal care, wellness and fitness (salons, barbers, parlours, spas, gyms, yoga, makeup artists, tailors, laundry)

Family key `personal_care_wellness_fitness`. Entity: business or person. Template applies to 9 list types:
Beauty parlours; Barbers and salons (men); Bridal makeup artists [i]; Spas and massage; Gyms and fitness; Tailors and boutiques; Dry cleaners and laundry; Beauty, grooming, massage at home; makeup artists [i]; Salons, barbers, nail salons, spas, gyms, yoga.

**What established platforms hold**

- Google Business Profile: attributes depend on category; gyms and salons get accessibility, crowd, planning (appointment required), amenities, activities, services, languages, payments; identity attributes such as women-owned [C, 2026-10-06].
- Urban Company beauty and salon-at-home: trained, background-checked professionals, fixed prices [P, C weak].
- Justdial: services, amenities, payment options, year established named for such listings [C, S-grade].
- Yelp: 20+ attributes (bool, single and multi choice), hours, price range [C].

**Registers and bodies that hold it**

No register for salons. Gyms and spas: municipal trade licences (UNVERIFIED). Trainers: certifying bodies (international, UNVERIFIED).

**Gating and sensitivity**

Women-only and men-only status is a service fact, not a person attribute, and is shown. Individual makeup artists and tailors are named persons (consent, relay). No before-and-after photos (C29).

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `outlet_type` | Outlet type | enum | R | P | yes | yes | none | own/agt | salon, barber, beauty_parlour, spa, gym, yoga_studio, tailor, boutique, laundry, dry_cleaner, makeup_artist |
| `clientele` | Clientele | enum | R | P | yes |  | none | own/sur | women_only, men_only, unisex, family |
| `price_from` | Services priced from | money | S | L |  |  | none | own/sur | menu items are child records |
| `price_checked_on` | Prices checked on | date | S | L |  |  | none | sur |  |
| `appointment_mode` | Appointments | enum | S | P | yes |  | none | own | walk_in, appointment, both |
| `home_service` | Home service | bool | S | P | yes |  | none | own |  |
| `bridal_packages` | Bridal packages | bool | O | P | yes |  | none | own |  |
| `brands_used` | Brands used | concept_list | O | P | yes |  | none | own |  |
| `female_staff_only` | Female staff only | bool | O | P | yes |  | none | sur |  |
| `facilities` | Facilities | concept_list | O | P | yes |  | none | sur | shower, sauna, parking, women section |
| `membership_fee_monthly` | Monthly membership | money | O | L |  |  | none | own | gyms |
| `trainer_certified` | Certified trainers | bool | O | P | yes |  | none | own | gyms |
| `classes_offered` | Classes | concept_list | O | P | yes |  | none | own | gyms, yoga |
| `turnaround_days` | Turnaround (days) | number | O | P |  |  | none | own | tailors, laundry |
| `pickup_delivery` | Pickup and delivery | bool | O | P | yes |  | none | own | laundry, tailors |
| `custom_stitching` | Custom stitching | bool | O | P | yes |  | none | own | tailors, boutiques |

### 6.17 Food and beverage outlets (restaurants, cafes, bakeries, caterers, home cooks, butchers, dairy)

Family key `food_and_beverage_outlets`. Entity: business. Template applies to 6 list types:
Bakeries; Restaurants and cafes; Caterers and cooks; Meat and dairy suppliers; Restaurants, cafes, takeaways by cuisine; Bakeries and cake shops.

**What established platforms hold**

- Zomato: cuisines, establishment types, cost for two, opening hours, dining and delivery ratings, address, coordinates, chain or group, amenities, popular dishes, online ordering and delivery time, offers [C, 2026-10-06, scraper pages].
- Yelp: categories, price range, hours, attributes such as WiFi, parking, alcohol, noise, delivery and reservation options, menu, health inspection score where available [C].
- Google Business Profile: dine-in, takeout, delivery, payments, planning attributes [P].

**Registers and bodies that hold it**

Provincial food authorities (Punjab Food Authority licences and inspection grades, UNVERIFIED), halal certification bodies (PHA, UNVERIFIED), municipal trade licences.

**Gating and sensitivity**

Low sensitivity. Home cooks are named individuals (consent, relay). Live menu prices are not stored; cost for two is a dated band.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `outlet_type` | Outlet type | enum | R | P | yes | yes | none | own/agt | restaurant, cafe, fast_food, takeaway, bakery, cake_shop, caterer, home_cook, butcher, dairy |
| `cuisines` | Cuisines | concept_list | R | P | yes |  | none | own/agt |  |
| `service_modes` | Service modes | concept_list | S | P | yes |  | none | own | dine_in, takeaway, delivery, catering |
| `cost_for_two` | Cost for two | money | O | L |  |  | none | own/sur | Zomato field; dated band |
| `cost_checked_on` | Cost checked on | date | O | L |  |  | none | sur |  |
| `halal_status` | Halal status | enum | S | P | yes |  | none | own/reg | halal_certified, halal_declared, unknown |
| `food_licence` | Food authority licence | identifier_list | O | P |  |  | none | reg |  |
| `dietary_options` | Dietary options | concept_list | O | P | yes |  | none | own | vegetarian, vegan, gluten_free |
| `seating_capacity` | Seating capacity | number | O | P |  |  | none | own |  |
| `family_section` | Family section | bool | O | P | yes |  | none | sur |  |
| `amenities` | Amenities | concept_list | O | P | yes |  | none | sur | parking, wifi, kids area, prayer space |
| `delivery_radius_km` | Delivery radius (km) | number | O | P | yes |  | none | own |  |
| `delivery_fee` | Delivery fee | money | O | L |  |  | none | own |  |
| `catering_min_guests` | Catering minimum guests | number | O | P |  |  | none | own |  |
| `catering_price_per_head` | Catering price per head | money | O | L |  |  | none | own |  |
| `reservations` | Reservations taken | bool | O | P | yes |  | none | own |  |

### 6.18 Retail shops and dealers (grocery, hardware, mobiles, books, furniture, spares, building materials, agri inputs, flowers, car and bike dealers)

Family key `retail_shops`. Entity: business. Template applies to 9 list types:
Building material suppliers; Grocery and supermarkets; Agri inputs and seed dealers; Car and bike dealers; Auto parts and accessories; Shops: furniture, books, electronics, clothing, music, home and garden; Mobile phones and accessories, new and used; Hardware shops; Grocery, flower, laundry, delivery.

**What established platforms hold**

- Justdial: listing fields name, phone, address, category, rating, verified flag, year established, payment options [C, S-grade].
- Google Business Profile and schema.org LocalBusiness: hours, geo, areaServed, paymentAccepted, priceRange, service options (delivery, pickup) [P].
- PakWheels dealer pages and OLX shops: dealer or owner flag, new or used (UNVERIFIED for dealer pages).
- Mobile retail in Pakistan turns on PTA approval and warranty [INFERENCE; the OLX/PakWheels query did not return field lists, so UNVERIFIED].

**Registers and bodies that hold it**

No register for shops. Brand authorised-dealer lists (manufacturer sites); agri input dealer licences (provincial agriculture departments, UNVERIFIED); municipal trade licence.

**Gating and sensitivity**

Low sensitivity. Stock levels and live prices are not stored.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `shop_type` | Shop type | enum | R | P | yes |  | none | own/agt | general, specialist, chain_outlet, dealer, wholesale_counter, showroom |
| `product_categories` | Product categories | concept_list | R | P | yes |  | none | own/agt |  |
| `brands_carried` | Brands carried | concept_list | S | P | yes | yes | none | own | row descriptor |
| `new_or_used` | New or used | enum | S | P | yes |  | none | own | new, used, both |
| `authorised_dealer_of` | Authorised dealer of | concept_list | O | P | yes |  | none | own/reg | checkable on brand dealer lists |
| `delivery` | Delivery | bool | S | P | yes |  | none | own |  |
| `delivery_area` | Delivery area | place_list | O | P | yes |  | none | own |  |
| `installments_offered` | Instalment plans | bool | O | P | yes |  | none | own |  |
| `warranty_offered` | Warranty | enum | O | P | yes |  | none | own | none, shop, manufacturer, both |
| `returns_policy` | Returns policy | text | O | L |  |  | none | own |  |
| `pta_approved_stock` | PTA-approved phones | bool | O | P | yes |  | none | own | mobile shops |
| `vehicle_makes_sold` | Vehicle makes sold | concept_list | O | P | yes |  | none | own | dealers |
| `inspection_offered` | Inspection before sale | bool | O | P | yes |  | none | own | dealers |
| `input_dealer_licence` | Input dealer licence | identifier_list | O | P |  |  | none | reg | agri inputs and seed dealers |
| `home_installation` | Home installation | bool | O | P | yes |  | none | own | furniture, appliances |

### 6.19 Fuel stations and utility supply (petrol pumps, CNG, EV charging, water and gas delivery)

Family key `fuel_and_utility_supply`. Entity: business. Template applies to 3 list types:
Petrol pumps; Water and gas delivery; Petrol (gas) stations.

**What established platforms hold**

- CarDekho fuel station pages (India): address, timings, fuel types (petrol, diesel, CNG, LPG), services (air filling, oil check, pollution check, store), 24-hour operation [P, S-grade].
- Google Business Profile: petrol-station attributes (restrooms, car wash, EV charging) and EV charging as its own use case [P, 2 sources].
- Fuel brand and posted price: not found in results; regulated national prices are published separately [INFERENCE].

**Registers and bodies that hold it**

OGRA licensing of petroleum retail outlets and the explosives department licence (UNVERIFIED), weights and measures calibration seals (UNVERIFIED); marketing company dealer lists (PSO, Shell and others, UNVERIFIED).

**Gating and sensitivity**

Posted prices are volatile: do not collect at launch. Show last-updated only if a price field is ever added.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `brand` | Marketing company or brand | text | S | P | yes | yes | none | own/sur |  |
| `fuel_types` | Fuel types | concept_list | R | P | yes |  | none | own/sur | petrol, diesel, CNG, LPG, EV charging |
| `open_24x7` | Open 24x7 | bool | S | P | yes |  | none | own/sur |  |
| `ancillary_services` | Ancillary services | concept_list | O | P | yes |  | none | sur | air, car wash, tyre shop, ATM, store, prayer area, restrooms |
| `ev_connector_types` | EV connector types | concept_list | O | P | yes |  | none | sur |  |
| `ev_charger_kw` | EV charger power (kW) | number | O | P | yes |  | none | sur |  |
| `petroleum_licence` | Outlet licence | identifier_list | O | P |  |  | none | reg | OGRA and explosives licence (UNVERIFIED) |
| `calibration_seal_date` | Pump calibration seal date | date | O | P |  |  | none | sur |  |
| `delivery_products` | Delivered products | concept_list | O | P | yes |  | none | own | bottled water, tanker water, LPG cylinders |
| `cylinder_sizes_kg` | Cylinder sizes (kg) | concept_list | O | P | yes |  | none | own |  |
| `tanker_capacity_litres` | Tanker capacity (litres) | number | O | P | yes |  | none | own |  |
| `delivery_time_hours` | Typical delivery time (hours) | number | O | P |  |  | none | own |  |
| `posted_fuel_price` | Posted fuel price | money | O | L |  |  | none | sur | later; volatile |
| `posted_price_date` | Posted price date | date | O | L |  |  | none | sur |  |

### 6.20 Classified listings (new and used cars, bikes, rickshaws, vans, trucks, tractors, boats, general items, livestock and pets)

Family key `classified_listings`. Entity: listing. Template applies to 3 list types:
Used and new cars, with curated lists (hybrid, imported, luxury); Bikes, rickshaws, vans, trucks, buses, tractors, caravans, boats; General for-sale classifieds; livestock, pets, pigeons.

**What established platforms hold**

- PakWheels: make, model, model year, mileage, registration city, engine cc, transmission, assembly (local or imported), body colour, fuel type, body type, price, trim [C, 2026-10-06, listing and scraper pages].
- OLX Pakistan: category tree incl. animals (livestock, dogs, cats, birds) and mobiles; per-category field lists not returned [C partial; UNVERIFIED].
- Gari.pk: vehicle scraper exists; fields not read [UNVERIFIED].

**Registers and bodies that hold it**

Provincial vehicle registration (Excise and Taxation) for registration status; not open to bulk reuse (UNVERIFIED). Do not publish the registration number or chassis number (links to the owner).

**Gating and sensitivity**

Sellers are often private persons: area only, relay contact. VIN and registration number are personal data, hidden. Listings expire (default 60 days).

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `item_kind` | Item kind | enum | R | P | yes | yes | none | own | car, motorcycle, rickshaw, van, truck, bus, tractor, boat, general_item, livestock, pet |
| `condition` | Condition | enum | R | P | yes |  | none | own | new, used, imported_used |
| `seller_type` | Seller type | enum | R | P | yes |  | personal | own | owner, dealer |
| `asking_price` | Asking price | money | R | L |  |  | none | own | date is listing date; see section 10 on free or locked |
| `price_date` | Price date | date | R | L |  |  | none | auto |  |
| `price_negotiable` | Negotiable | bool | O | L |  |  | none | own |  |
| `listing_expires_on` | Listing expires | date | R | P |  |  | none | auto |  |
| `make` | Make | concept_list | S | P | yes |  | none | own | vehicles |
| `model` | Model | text | S | P | yes |  | none | own |  |
| `model_year` | Model year | number | S | P | yes |  | none | own |  |
| `mileage_km` | Mileage (km) | number | S | P | yes |  | none | own |  |
| `fuel_type` | Fuel type | enum | S | P | yes |  | none | own | petrol, diesel, hybrid, electric, cng, lpg |
| `engine_cc` | Engine capacity (cc) | number | S | P | yes |  | none | own |  |
| `transmission` | Transmission | enum | S | P | yes |  | none | own | manual, automatic |
| `assembly` | Assembly | enum | S | P | yes |  | none | own | local, imported |
| `body_type` | Body type | enum | O | P | yes |  | none | own |  |
| `colour` | Colour | text | O | P | yes |  | none | own |  |
| `registration_city` | Registered in | place_list | O | P | yes |  | none | own |  |
| `registration_status` | Registration status | enum | O | P | yes |  | none | own | registered, unregistered, in_process |
| `owner_count` | Previous owners | number | O | P |  |  | none | own |  |
| `inspection_report` | Inspection | enum | O | P | yes |  | none | sur | none, seller, third_party |
| `vin` | Chassis number | text | O | H |  |  | personal | own | never shown |
| `species_breed` | Species and breed | text | O | P | yes |  | none | own | livestock, pets |
| `age_months` | Age (months) | number | O | P | yes |  | none | own | livestock, pets |
| `vaccination_status` | Vaccination status | enum | O | P | yes |  | none | own | vaccinated, not_vaccinated, unknown |

### 6.21 Transport and logistics (movers, couriers, taxis, ride services, car rental, truck transporters, customs agents)

Family key `transport_and_logistics`. Entity: business. Template applies to 7 list types:
Movers and packers; Courier and logistics; Taxi and ride services; Truck and goods transporters; Customs clearing agents; Movers, packers, helpers; Car rental, taxis, drivers.

**What established platforms hold**

- Justdial and Urban Company list movers and packers with services and prices [P, UNVERIFIED for field detail].
- Freight and customs: IndiaMART and Alibaba service categories; Pakistan customs clearing agents are licensed by customs (UNVERIFIED).
- Google Business Profile service options (delivery, pickup) [P].

**Registers and bodies that hold it**

Customs (FBR) clearing agent licences, TDAP, provincial transport authority route permits for goods and passenger vehicles, motor vehicle fitness certification (all UNVERIFIED), PIFFA freight forwarders association (UNVERIFIED).

**Gating and sensitivity**

Driver identities are individuals (domestic family rules apply to named drivers). Live rates are not stored.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `service_type` | Service type | enum | R | P | yes | yes | none | own/agt | movers, courier, ride_hailing, taxi, car_rental, truck_transport, freight_forwarder, customs_agent |
| `coverage` | Coverage area | place_list | R | P | yes |  | none | own |  |
| `vehicle_types` | Vehicle types | concept_list | S | P | yes |  | none | own |  |
| `fleet_size` | Fleet size | number | O | L |  |  | none | own |  |
| `capacity_tonnes_max` | Largest load (tonnes) | number | O | P | yes |  | none | own |  |
| `pricing_basis` | Pricing basis | enum | S | P | yes |  | none | own | per_km, per_trip, per_kg, per_hour, per_day, per_container, quote |
| `rate_from` | Rate from | money | O | L |  |  | none | own |  |
| `rate_checked_on` | Rate checked on | date | O | L |  |  | none | sur |  |
| `goods_insured` | Goods insured | bool | O | P | yes |  | none | own |  |
| `insurance_cover_limit` | Insurance cover limit | money | O | L |  |  | none | own |  |
| `tracking_available` | Tracking available | bool | O | P | yes |  | none | own |  |
| `international_service` | International service | bool | O | P | yes |  | none | own |  |
| `cod_available` | Cash on delivery | bool | O | P | yes |  | none | own | couriers |
| `driver_included` | Driver included | bool | O | P | yes |  | none | own | car rental |
| `packing_included` | Packing included | bool | O | P | yes |  | none | own | movers |
| `storage_available` | Storage available | bool | O | P | yes |  | none | own |  |
| `customs_licence` | Customs agent licence | identifier_list | O | P |  |  | none | reg | UNVERIFIED register |
| `route_permit` | Route or operator permit | identifier_list | O | P |  |  | none | reg | UNVERIFIED |

### 6.22 Accommodation and travel (hotels, guest houses, resorts, campgrounds, vacation rentals, travel agents, tour operators)

Family key `accommodation_and_travel`. Entity: business. Template applies to 3 list types:
Travel agents and tour operators; Hotels, B&Bs, resorts, campgrounds; Vacation rentals, tours, cruises, flights.

**What established platforms hold**

- schema.org Hotel/LodgingBusiness: checkinTime, checkoutTime, numberOfRooms, petsAllowed, starRating with the rating body, amenityFeature [P, 3 mirrors].
- Booking.com extranet: room descriptions, amenities, house rules, check-in and check-out, cancellation policy, room types, rates [P, S-grade].
- Tripadvisor property setup: address, business type, rooms, maximum occupancy, amenities checklist [P].
- Airbnb and Booking vacation rentals: property type, guest capacity, bedrooms, beds, bathrooms (shared or private), amenities, house rules, cancellation policy [C, 2026-10-06].
- Murree needs: distance to Mall Road, seasonal price bands, snow access, generator, Tourism Department registration, rate-list compliance [P: Pilot note; registry current status UNVERIFIED].

**Registers and bodies that hold it**

Provincial tourism departments (hotel and guest house registration, rate lists), Punjab Tourism and Murree Development Authority (UNVERIFIED), IATA and Pakistan Hajj and Umrah operator licences from the religious affairs ministry (UNVERIFIED), rating bodies (Hotelstars and others abroad) [P].

**Gating and sensitivity**

Show base rate bands only, dated, never surge prices (Murree lesson, Q-N5 style rule). Link to official advisories. Do not display last-minute availability.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `property_type` | Property type | enum | R | P | yes | yes | none | own/agt | hotel, guest_house, resort, hostel, bnb, campground, vacation_rental, apartment_hotel, tour_operator, travel_agent |
| `star_class` | Star class | number | O | P | yes |  | none | reg/own | with rating body in the check record |
| `rating_body` | Rating body | text | O | P |  |  | none | reg | schema.org starRating.author |
| `rooms` | Number of rooms | number | S | P |  |  | none | own |  |
| `room_types` | Room types | concept_list | S | P | yes |  | none | own |  |
| `guest_capacity` | Guest capacity | number | O | P | yes |  | none | own | vacation rentals |
| `bedrooms` | Bedrooms | number | O | P | yes |  | none | own | vacation rentals |
| `check_in_time` | Check-in time | text | S | P |  |  | none | own | HH:MM |
| `check_out_time` | Check-out time | text | S | P |  |  | none | own | HH:MM |
| `amenities` | Amenities | concept_list | S | P | yes |  | none | own/sur | Wi-Fi, parking, breakfast, pool, AC, 24-hour desk |
| `house_rules` | House rules | concept_list | O | P | yes |  | none | own | pets, ID and couples policy where relevant |
| `cancellation_policy` | Cancellation policy | enum | S | P | yes |  | none | own | free, partial, non_refundable, varies |
| `price_from` | Base rate from | money | S | L |  |  | none | own/sur | base band, never surge |
| `price_basis` | Price basis | enum | S | L |  |  | none | own | per_room_night, per_person, per_unit |
| `price_season` | Price season | enum | O | L |  |  | none | own | winter, summer, holiday, shoulder |
| `price_checked_on` | Price checked on | date | S | L |  |  | none | sur |  |
| `landmark_distance_m` | Distance to main landmark (m) | number | O | P | yes |  | none | sur | Murree: Mall Road |
| `all_weather_access` | All-weather road access | enum | O | P | yes |  | none | sur | yes, partial, no |
| `backup_power` | Backup power | enum | O | P | yes |  | none | sur | none, generator, ups, solar |
| `parking_spaces` | Parking spaces | number | O | P |  |  | none | sur |  |
| `tourism_registration` | Tourism registration | identifier_list | S | P |  |  | none | reg | UNVERIFIED current register |
| `tour_types` | Tour types | concept_list | O | P | yes |  | none | own | tour operators |
| `destinations` | Destinations | place_list | O | P | yes |  | none | own | tour operators |
| `travel_licence` | Travel or Hajj licence | identifier_list | O | P |  |  | none | reg | IATA, ministry licence (UNVERIFIED) |
| `booking_url` | Booking link | text | O | L |  |  | none | own |  |

### 6.23 Venues and event services (wedding halls, marquees, event planners, photographers, DJs, attractions, cinemas, clubs)

Family key `venues_and_event_services`. Entity: business. Template applies to 6 list types:
Wedding halls and marquees; Photographers and videographers; Event planners and decorators; Attractions, museums, landmarks, outdoors; Cinemas, arcades, casinos, venues, bars, clubs; Wedding planners, caterers, DJs, decorators, halls; photographers.

**What established platforms hold**

- WeddingBazaar and VenueLook (India): capacity, price per plate, parking, rooms, bridal room, electricity backup, decoration and food policies [C, snippet lists the generic fields; Pakistan sources not read, so UNVERIFIED for Pakistan].
- Karachi banquet roundups (Graana): capacity (1,000 to 2,000), catering, valet parking, decoration [C, S-grade].
- Eventbrite style fields for ticketed attractions: category, venue, ticket price, refund policy [C].

**Registers and bodies that hold it**

Municipal and development authority marquee and banquet licences, cinema licensing by provincial censor boards (all UNVERIFIED). No register for event planners.

**Gating and sensitivity**

Photographers and DJs who are individuals follow the named-person rules. Alcohol, gambling and age-restricted venues: flag and age limit, no promotion; legal review by country.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `venue_kind` | Venue or service kind | enum | R | P | yes | yes | none | own/agt | wedding_hall, marquee, lawn, banquet, cinema, arcade, museum, attraction, outdoor_site, club, event_planner, photographer, decorator, dj |
| `guest_capacity_min` | Capacity from | number | S | P | yes |  | none | own/sur |  |
| `guest_capacity_max` | Capacity up to | number | S | P | yes |  | none | own/sur |  |
| `indoor_outdoor` | Indoor or outdoor | enum | O | P | yes |  | none | own | indoor, outdoor, both |
| `air_conditioned` | Air conditioned | bool | O | P | yes |  | none | sur |  |
| `catering_policy` | Catering policy | enum | O | P | yes |  | none | own | in_house_only, external_allowed, both |
| `price_per_head` | Price per head | money | O | L |  |  | none | own |  |
| `hire_rate_from` | Hire rate from | money | O | L |  |  | none | own |  |
| `price_checked_on` | Prices checked on | date | O | L |  |  | none | sur |  |
| `bridal_rooms` | Bridal rooms | number | O | P |  |  | none | sur |  |
| `parking_capacity` | Parking capacity | number | O | P |  |  | none | sur |  |
| `backup_power` | Backup power | bool | O | P | yes |  | none | sur |  |
| `event_services` | Event services offered | concept_list | O | P | yes |  | none | own | decoration, DJ, photography, mehndi |
| `booking_deposit_percent` | Booking deposit (percent) | number | O | L |  |  | none | own |  |
| `advance_booking_days` | Advance booking (days) | number | O | P |  |  | none | own |  |
| `entry_fee` | Entry fee | money | O | L |  |  | none | own | attractions |
| `age_restriction` | Age restriction | text | O | P | yes |  | none | own |  |
| `accessibility` | Accessibility | concept_list | O | P | yes |  | none | sur |  |
| `venue_licence` | Venue licence | identifier_list | O | P |  |  | none | reg | UNVERIFIED |

### 6.24 Manufacturers and exporters (cluster makers, factories, contract manufacturers, certified supplier lists)

Family key `manufacturers_and_exporters`. Entity: business. Template applies to 11 list types:
Industrial suppliers and fabricators; Textile and garment makers and exporters; Chemicals, dyes, metals, minerals, ores; Sialkot cluster: surgical instruments, sports goods, gloves, leather goods; Food, agri, FMCG, fertiliser, seeds, farm machinery; Packaging materials and machines; Electronics, electrical, appliances, gifts, home products (makers); Furniture and furniture-hardware makers and wholesalers; Lab and measuring instruments [h]; Contract manufacturers and machine shops by process; Certified, women-owned and audited supplier lists (ISO, halal, GOTS).

**What established platforms hold**

- IndiaMART: help centre says profile Additional Details hold GST number, firm type and company size, turnover details; supplier pages show nature of business, legal status of firm, annual turnover, GST number and registration date, IEC [C, 2026-10-06]. TrustSEAL is a paid documentary verification of existence, legal status, approvals; verified pages list company name, business type, established year, proprietor, GSTIN, address, IEC [P, 2+ sources]. Employee count is not confirmed as a standard field [C].
- Alibaba: factory size, staff count, annual revenue band, response rate, OEM/ODM tags, years as Gold supplier, assessed supplier flag [C, scraper-field descriptions]. Verified Supplier uses on-site and third-party inspectors [P, S-grade]. Audit dimensions: company overview, production capacity, process, export situation [P, S-grade].
- Made-in-China: audit report in five parts (general, foreign trade, R&D, management and certification, production and quality control) [P].
- ThomasNet: primary company type (for example custom manufacturer), year founded, employee range, annual sales bracket, capabilities, equipment, product lines, brands carried, certifications (ISO 9001, AS9100, ITAR, NADCAP), ownership type and diversity status, OEM/contract/distributor filters [C, 2026-10-06].
- Pakistan Energy Label for fans: NEECA registration, PS:1/2010 standard, test report from an ISO/IEC 17025 laboratory [C]. PSQCA certification marks scheme exists; sanitaryware standard not found [C].
- Pilot notes carry the Sialkot, fan, sanitaryware, furniture field sets in full [P].

**Registers and bodies that hold it**

SECP (company), FBR NTN and Active Taxpayer List, TDAP exporter directory and Pakistan Trade Portal profiles, DRAP establishment licences (surgical devices), SIMAP, SCCI, KCCI membership letters, IAF CertSearch for ISO certificates, EUDAMED and openFDA registration lookups, PSQCA and NEECA lists [P].

**Gating and sensitivity**

Commercial fields (turnover, capacity, customers) are bands and subscriber-only. A paid page never changes a check label (spec section 12). Sanctions screening is internal. Sole-proprietor owner names only with consent. Price lists are not collected at pilot (health-pricing rules apply to surgical devices, Q-S1).

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `business_type` | Business type | enum | R | P | yes | yes | none | own/sur | manufacturer, trader, wholesaler, exporter, sub_contractor |
| `product_categories` | Product categories | concept_list | R | P | yes |  | none | own/agt | each with HS code in child record |
| `tax_ids` | Tax and legal IDs | identifier_list | S | P |  |  | none | reg | NTN, STRN, CUIN, GSTIN, IEC, with a verified flag per ID |
| `year_established` | Year established | number | S | P |  |  | none | reg/own |  |
| `years_exporting` | Years exporting | number | O | P |  |  | none | own |  |
| `export_markets` | Export markets | place_list | O | L | yes |  | none | own |  |
| `certifications` | Certifications | identifier_list | O | L | yes |  | none | reg/own | body, ID, scope, expiry |
| `regulatory_registrations` | Regulatory registrations | identifier_list | O | L | yes |  | none | reg | DRAP licence, FDA FEI, EUDAMED SRN, CE |
| `product_standards` | Product standards and marks | identifier_list | O | P | yes |  | none | reg | PSQCA mark, PS:1/2010, Pakistan Energy Label |
| `verification_tier` | Verification tier | enum | S | P | yes |  | none | sur | none, documents, on_site, third_party |
| `capacity_band` | Capacity band | enum | O | L |  |  | commercial | own/sur |  |
| `monthly_capacity` | Monthly capacity | number | O | L |  |  | commercial | own | unit in note child |
| `workforce_band` | Workforce band | enum | O | L |  |  | none | own/sur | 1-10, 11-50, 51-200, 201-1000, 1000+ |
| `factory_area_sqm` | Factory area (sqm) | number | O | L |  |  | none | own/sur |  |
| `oem` | OEM or private label | bool | S | P | yes |  | none | own |  |
| `customisation` | Customisation capability | concept_list | O | P | yes |  | none | own/sur | own forging, die, CNC, laser marking |
| `materials` | Materials | concept_list | O | P | yes |  | none | own | steel grades, wood types, brass |
| `moq` | Minimum order | text | O | L |  |  | none | own | existing seed key, text with unit |
| `lead_time_days` | Lead time (days) | number | O | L |  |  | none | own |  |
| `sample_policy` | Sample policy | enum | O | L |  |  | none | own | free, paid, refundable, none |
| `payment_terms` | Payment terms | concept_list | O | L |  |  | none | own | advance, LC, credit |
| `sub_contracting` | Sub-contracting | enum | O | L |  |  | none | own | none, some_stages, extensive |
| `audits` | Social and buyer audits | identifier_list | O | L |  |  | none | own | SMETA, BSCI; date and result summary |
| `trade_body_memberships` | Trade body memberships | concept_list | O | P | yes |  | none | own/reg | SIMAP, SCCI, KCCI |
| `dealer_network_places` | Dealer network cities | place_list | O | P | yes |  | none | own | fans, sanitaryware, furniture |
| `warranty_years` | Warranty (years) | number | O | P | yes |  | none | own | fans, sanitaryware |
| `factory_address` | Factory address | text | S | L |  |  | none | reg/sur | separate from registered address; exact pin L |
| `turnover_band` | Annual turnover band | enum | O | L |  |  | commercial | own | not prominent on TrustSEAL |

### 6.25 Suppliers, distributors, importers and equipment (wholesalers, reps, importers, machinery dealers and rental, data vendors, catalogues)

Family key `suppliers_distributors_and_equipment`. Entity: business. Template applies to 7 list types:
Heavy equipment rental; Used equipment for sale; equipment suppliers and importers [h]; Heavy and construction machinery, new, used, rental; Industrial machinery, machine tools, spares; Manufacturers' reps, distributors, wholesalers, wholesale markets; Company lists sold as data; prospects by filter; Product catalogues and third-party sellers.

**What established platforms hold**

- IndiaMART and ThomasNet filter by company type (OEM, contract manufacturer, distributor), product lines and brands carried [C].
- Alibaba and Global Sources supplier profiles: main products, export markets, assessed flag [C, scraper-field descriptions].
- Used equipment boards and rental companies: make, model, year, hours of use, rental rate by period (field lists not read; UNVERIFIED).
- Company-list vendors (data sellers) describe dataset size and filters [UNVERIFIED].

**Registers and bodies that hold it**

SECP, FBR, TDAP importers and exporters, DRAP medical device importer licences (UNVERIFIED), chambers, wholesale market associations.

**Gating and sensitivity**

Commercial bands only. Data-vendor entries must show the licence under which their data was collected (D17). Used medical equipment sellers need a note that devices are regulated and prices are health-sector prices (Q-S1).

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `trade_role` | Trade role | enum | R | P | yes | yes | none | own/agt | distributor, wholesaler, importer, reps_agent, equipment_dealer, rental_company, market_unit, data_vendor, marketplace_seller |
| `product_categories` | Product categories | concept_list | R | P | yes |  | none | own/agt |  |
| `brands_distributed` | Brands distributed | concept_list | S | P | yes |  | none | own |  |
| `territory` | Territory covered | place_list | S | P | yes |  | none | own |  |
| `hs_codes` | HS codes | concept_list | O | L |  |  | none | own |  |
| `import_origins` | Import origins | place_list | O | L | yes |  | none | own | importers |
| `stock_availability` | Stock availability | enum | O | P | yes |  | none | own | ready_stock, made_to_order, mixed |
| `moq` | Minimum order | text | O | L |  |  | none | own |  |
| `price_basis` | Price basis | enum | O | L |  |  | none | own | ex_works, fob, cif, delivered |
| `payment_terms` | Payment terms | concept_list | O | L |  |  | none | own |  |
| `warehouse_places` | Warehouse places | place_list | O | L |  |  | none | own |  |
| `equipment_condition` | Equipment condition | enum | O | P | yes |  | none | own | new, used, refurbished, rental |
| `equipment_types` | Equipment types | concept_list | O | P | yes |  | none | own |  |
| `equipment_makes` | Equipment makes | concept_list | O | P | yes |  | none | own |  |
| `rental_rate_from` | Rental rate from | money | O | L |  |  | none | own |  |
| `rental_period` | Rental period | enum | O | L |  |  | none | own | hour, day, week, month |
| `operator_included` | Operator included | bool | O | P | yes |  | none | own |  |
| `spares_and_service` | Spares and service support | bool | O | P | yes |  | none | own |  |
| `importer_licence` | Importer licence | identifier_list | O | P |  |  | none | reg | medical devices need DRAP (UNVERIFIED) |
| `market_name` | Wholesale market | text | O | P | yes |  | none | own |  |
| `buys_products` | Products bought | concept_list | O | P | yes |  | none | own | importers and buyers |
| `typical_order_band` | Typical order size band | enum | O | L |  |  | commercial | own |  |
| `dataset_size_band` | Dataset size band | enum | O | L |  |  | none | own | data vendors |
| `data_licence_basis` | Data licence basis | text | O | P |  |  | none | own | data vendors; D17 |

### 6.26 B2B support and trade bodies (testing labs, certification bodies, printing, warehousing, waste and recycling, chambers, associations, trade shows)

Family key `b2b_support_and_trade_bodies`. Entity: business or institution. Template applies to 5 list types:
Printing and signage; Testing and certification labs [h]; Waste and recycling services; Business services: freight, customs, warehousing, printing, IT, testing labs [h]; Chambers, associations, trade shows, country pavilions.

**What established platforms hold**

- ThomasNet: certifications and capability descriptions for service suppliers [C].
- IAF CertSearch and national accreditation bodies publish certification and laboratory scope [P].
- Association directories (chambers, SIMAP and similar) are the primary source for membership [P].
- Justdial and IndiaMART carry printing, packaging and warehousing categories [P, UNVERIFIED for fields].

**Registers and bodies that hold it**

PNAC (laboratory accreditation, name UNVERIFIED), PSQCA labs, EPA licences for waste (UNVERIFIED), chambers and trade associations, TDAP trade show calendar (UNVERIFIED).

**Gating and sensitivity**

Low sensitivity. Testing price lists are commercial, subscriber-only and dated.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `service_kind` | Service kind | enum | R | P | yes | yes | none | own/agt | testing_lab, certification_body, inspection, warehousing, printing, signage, waste_collection, recycling, association, chamber, trade_show |
| `scope_of_services` | Scope of services | concept_list | R | P | yes |  | none | own |  |
| `accreditations` | Accreditations | identifier_list | S | P | yes |  | none | reg | ISO/IEC 17025, ISO 17065; scope and expiry |
| `accreditation_scope` | Accreditation scope | text | O | P |  |  | none | reg |  |
| `tests_offered` | Tests offered | concept_list | O | P | yes |  | none | own |  |
| `turnaround_days` | Turnaround (days) | number | O | P |  |  | none | own |  |
| `sample_pickup` | Sample pickup | bool | O | P | yes |  | none | own |  |
| `price_list_from` | Typical price from | money | O | L |  |  | none | own |  |
| `price_checked_on` | Price checked on | date | O | L |  |  | none | sur |  |
| `warehouse_area_sqft` | Warehouse area (sqft) | number | O | L |  |  | none | own |  |
| `storage_types` | Storage types | concept_list | O | P | yes |  | none | own | dry, cold, bonded |
| `print_methods` | Print methods | concept_list | O | P | yes |  | none | own | offset, digital, screen, flex |
| `waste_types` | Waste types handled | concept_list | O | P | yes |  | none | own |  |
| `waste_licence` | Waste licence | identifier_list | O | P |  |  | none | reg | UNVERIFIED |
| `recycling_capacity_tpd` | Recycling capacity (tonnes per day) | number | O | L |  |  | none | own |  |
| `member_count` | Members | number | O | P |  |  | none | own | associations |
| `membership_categories` | Membership categories | concept_list | O | P | yes |  | none | own |  |
| `sector_focus` | Sector focus | concept_list | O | P | yes |  | none | own |  |
| `next_edition_date` | Next edition date | date | O | P | yes |  | none | own | trade shows |

### 6.27 Government, civic and community (offices, police, emergency, mosques, NGOs, charities, causes, community notices)

Family key `government_civic_community`. Entity: institution. Template applies to 6 list types:
Mosques and prayer services; NGOs and charities; Police and emergency services; Government service offices; Government bodies and public offices; Causes, communities, NGOs; community notices (lost and found, travel partners).

**What established platforms hold**

- Charity Navigator: EIN, mission, programmes, ratings from several beacons, governance, financial data from IRS Form 990 [C, 2026-10-06]. Pakistan equivalents: SECP section 42 and provincial NGO registration (UNVERIFIED).
- Government service offices: Google Maps and agency sites hold hours and services; no aggregator checked [UNVERIFIED].
- Community notices (lost and found, travel partners): classifieds pattern [UNVERIFIED].

**Registers and bodies that hold it**

SECP (non-profit companies), provincial social welfare departments, FBR approved non-profit list, Pakistan Centre for Philanthropy (UNVERIFIED), government directories, opendata.com.pk.

**Gating and sensitivity**

Government policy is aggregate statistics only at first (Q-N3). Public helplines are an exception to 'never show phone' and need an owner decision. Mosque denomination, sect or ethnicity is never collected. Community notices may name people and children: short expiry, area only, personal and child tags.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `body_type` | Body type | enum | R | P | yes | yes | none | reg/own | ministry, department, local_government, police, fire_rescue, court, regulator, mosque, ngo, charity, community_group, notice |
| `jurisdiction` | Jurisdiction | place_list | R | P | yes |  | none | reg |  |
| `services_provided` | Services provided | concept_list | S | P | yes |  | none | reg/own | CNIC, passport, licence, tax, land record |
| `appointment_mode` | Appointments | enum | O | P | yes |  | none | own | walk_in, appointment, both |
| `online_services_url` | Online services link | text | O | P |  |  | none | reg |  |
| `official_fee_schedule_url` | Official fee schedule link | text | O | P |  |  | none | reg |  |
| `public_helpline` | Public helpline | text | O | P |  |  | none | reg | public emergency or service number; exception needs owner decision |
| `ngo_registration` | NGO or charity registration | identifier_list | S | P |  |  | none | reg | authority, number, validity |
| `mission_summary` | Mission | text | S | P |  |  | none | own |  |
| `programme_areas` | Programme areas | concept_list | O | P | yes |  | none | own |  |
| `tax_exempt` | Approved non-profit status | bool | O | P | yes |  | none | reg | FBR list |
| `zakat_eligible` | Accepts zakat | bool | O | P | yes |  | none | own |  |
| `donation_methods` | Donation methods | concept_list | O | L |  |  | none | own |  |
| `annual_expenditure_band` | Annual expenditure band | enum | O | L |  |  | commercial | own |  |
| `volunteer_opportunities` | Volunteers needed | bool | O | P | yes |  | none | own |  |
| `mosque_capacity` | Mosque capacity | number | O | P | yes |  | none | sur | mosques |
| `mosque_facilities` | Mosque facilities | concept_list | O | P | yes |  | none | sur | women's section, wudu, parking |
| `jumuah_time` | Jumuah time | text | O | P |  |  | none | own |  |
| `notice_kind` | Notice kind | enum | O | P | yes |  | personal, child | own | lost, found, travel_partner, general |
| `notice_expires_on` | Notice expires | date | O | P |  |  | personal | auto | short default expiry |

### 6.28 Topic and curated lists (software, AI tools, websites, apps, resources, books, films, public figures, institutions, awards, top-10s)

Family key `topic_and_curated_lists`. Entity: topic item. Template applies to 9 list types:
Software by category in ranked grids; "alternatives to X"; product launches; AI tools by function; Websites and web tools by task; mobile apps by country; Developer resource lists ("awesome"); Books, films, TV, music, podcasts, games; Public figures (presidents, ministers, CEOs, judges, award winners); people from a place [i]; Institutions with standard IDs (airports, universities, ports); fact lists, timelines; Best-of, awards and tested-product lists by place; Voted Top 10s, playlists, inspiration boards.

**What established platforms hold**

- G2 and Capterra: pricing plans, platforms or deployment, support and training options, typical customers, vendor name, location, website, founded year, features and integrations [C, 2026-10-06].
- Standard IDs for institutions and works: ISBN, IMDb, IATA and ICAO airport codes, UN/LOCODE, Wikidata QID, GRID or ROR for universities (the last two UNVERIFIED).
- Awards and best-of lists cite the awarding body and year (Wirecutter style, UNVERIFIED).

**Registers and bodies that hold it**

Wikidata, GeoNames, OpenStreetMap, Overture, ROR, ISBN agencies (open or licensed baselines, licences to be recorded per D17). Public-figure data only from public records and only about public roles.

**Gating and sensitivity**

Topic lists use the topic tree, not the place tree (C27), and are monetised by sponsorship and affiliate links, not list sales: affiliate relationships are internal and disclosed. Public figures: public role only, no home address, birth date only if already public; people are never ranked.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `item_kind` | Item kind | enum | R | P | yes | yes | none | agt/own | software, ai_tool, website, mobile_app, library, book, film, tv_show, music, podcast, game, public_figure, institution, fact, award_entry, product |
| `topic_ids` | Topics | concept_list | R | P | yes |  | none | agt | topic tree nodes |
| `official_url` | Official link | text | R | P |  |  | none | agt/own |  |
| `creator_or_vendor` | Creator or vendor | text | S | P | yes |  | none | agt |  |
| `first_release_date` | First release | date | O | P | yes |  | none | agt |  |
| `platforms` | Platforms | concept_list | O | P | yes |  | none | agt | web, android, ios, windows, linux, api |
| `pricing_model` | Pricing model | enum | O | P | yes |  | none | agt/own | free, freemium, paid, subscription, open_source, one_time |
| `starting_price` | Starting price | money | O | L |  |  | none | own | price date required |
| `price_checked_on` | Price checked on | date | O | L |  |  | none | agt |  |
| `licence` | Licence | text | O | P | yes |  | none | agt | open source licence name |
| `available_in` | Available in | place_list | O | P | yes |  | none | agt | apps by country |
| `editorial_pick` | Editorial pick | bool | O | P | yes |  | none | own | never ranks people |
| `alternatives_to` | Alternative to | concept_list | O | P | yes |  | none | agt |  |
| `standard_ids` | Standard IDs | identifier_list | O | P |  |  | none | reg | ISBN, IATA, ICAO, Wikidata |
| `award_name` | Award or list name | text | O | P | yes |  | none | agt |  |
| `award_year` | Award year | number | O | P | yes |  | none | agt |  |
| `person_role` | Public role | text | O | P | yes |  | personal | reg/agt | public figures only |
| `term_start` | Term start | date | O | P |  |  | personal | reg |  |
| `term_end` | Term end | date | O | P |  |  | personal | reg |  |
| `source_citation` | Source | text | R | P |  |  | none | agt | curated entries must cite |
| `affiliate_link` | Affiliate link in use | bool | O | I |  |  | none | own | disclosed on page |

### 6.29 Personal lists (wish lists, registries, task lists, saved places, watch and reading lists, alumni and classmates)

Family key `personal_lists`. Entity: personal item. Template applies to 5 list types:
Wish lists and registries (wedding, baby) [i]; Task lists and templates [i]; Saved places and map layers [i]; Watch and reading lists [i]; Alumni and classmates [i].

**What established platforms hold**

- Amazon-style registries and Goodreads-style shelves are the pattern; no field list checked [UNVERIFIED].
- Alumni and classmate lists: sensitive because they name individuals and children [INFERENCE].
- Personal lists are private by default and are not public lists in the market sense (decision section 8).

**Registers and bodies that hold it**

None.

**Gating and sensitivity**

Private by default (show = O, owner only). Sharing is a deliberate act; anything naming other people, children, babies or class lists needs the owner's confirmation that members consented. No indexing, no sales.

**Fields** (core fields also apply)

| Key | Label | Type | Req | Show | Filter | Row | Sensitivity | Source | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `item_kind` | Item kind | enum | R | O | yes | yes | none | own | wish_item, task, saved_place, book, film, show, alumnus, registry_item |
| `item_note` | Note | text | O | O |  |  | personal | own |  |
| `item_status` | Status | enum | O | O | yes |  | none | own | wanted, owned, in_progress, done |
| `quantity` | Quantity | number | O | O |  |  | none | own |  |
| `target_price` | Target price | money | O | O |  |  | none | own |  |
| `due_date` | Due date | date | O | O | yes |  | none | own |  |
| `saved_place` | Place | place_list | O | O | yes |  | none | own | saved places and map layers |
| `date_consumed` | Date finished | date | O | O | yes |  | none | own |  |
| `personal_rating` | My rating | number | O | O |  |  | none | own |  |
| `registry_event_date` | Event date | date | O | O |  |  | child | own | weddings and baby registries |
| `alumnus_name` | Person name | text | O | O |  |  | personal, child | own | alumni and classmates |
| `school_or_class` | School or class | text | O | O | yes |  | personal, child | own |  |
| `class_year` | Class year | number | O | O | yes |  | personal | own |  |
| `member_consent_confirmed` | Members consented to listing | bool | S | I |  |  | personal, child | own | required before sharing a list of people |

## 7. Cross-family findings and rules

1. **Price rule.** Every `money` value carries ISO 4217 currency and a price date in its metadata. The explicit `price_checked_on` and `*_checked_on` fields exist so a list can say "prices checked in the last 12 months" and so catalogue child records (test lists, menus, tuition tables) have one family-level date. A price without a date is not shown.
2. **Health-price gate (Q-S1).** Ten fields carry `health_price`: doctor fees (4), procedure, test, contrast and home-collection prices, and the dates that go with them. Hold them back, or collect and keep hidden, until the health rules are adopted. The rest of the doctor, hospital and lab entries can be built now.
3. **Individuals (Q-S2).** Where `form = individual` in the CSV (about 60 list types) or the family has persons, apply: consent status required, area-only location, relay-only contact, no company page, identity and police checks as flag plus date only. Self-declared gender is stored where customers use it as a filter (doctors, tradespeople, carers, tutors); it is tagged personal, optional, and is never an automatic filter default. Discrimination risk of gender filters in hiring-adjacent lists (talent, domestic workers) needs counsel.
4. **Child-facing gate (Q-S2).** Tutors, Quran tutors, madrasas, daycare, nannies and carers, and anything naming children: not public until safeguarding and relay-only contact are designed. Safeguarding status is a required field for these, shown as `none` rather than hidden. Class lists and baby registries are personal lists with owner-only show.
5. **Registrations.** Store scheme, number (public register data only), issuer, validity, register link and a per-ID verified flag with date. Never store CNIC or any national ID number; store "identity checked" and a date. Badge text says what was checked, for example "PMDC registration seen 2026-10" (spec section 7).
6. **Row descriptors.** One add-on field per family adds the descriptor on each row (for example `trades`, `specialty` is in `system_of_medicine`'s place for doctors via core specialities, `grades_offered`, `brands_carried`, `business_type`). The core's `specialities` already supplies up to three tags, so the add-on row field is usually the entity kind.
7. **Free versus subscriber.** About 73 percent of family fields are free (404 of 555). Subscriber fields are prices, certificate details, capacity and turnover bands, exact addresses, and staff or owner names. This keeps the free view useful (what, where, how checked) and puts the buyer's second decision (cost, capability, proof) behind the plan, consistent with decision section 11.
8. **Commercial bands, not values.** Turnover, capacity, budget and revenue are enum bands with a date, tagged `commercial`. IndiaMART's own TrustSEAL page does not put turnover or employees up front, and Alibaba shows staff counts and revenue only as bands.
9. **Freshness.** Property, classified, opportunity and notice entries expire (default 60 days or the deadline) and drop to hidden; closed entries remove the message button (decision section 11).
10. **Fields no platform showed that AllLists keeps on purpose:** equipment records (C21), accreditation scope, per-ID verified flags, price dates, safeguarding status, approval status of housing schemes with authority name, distance to landmark and all-weather access for Murree, Pakistan Energy Label and PSQCA marks for fans.
11. **Fields from the earlier drafts dropped or moved to later** because no live evidence: bed counts by ward, equipment lists on hospital pages, fuel prices, complaint records, litigation, bonding and financial bands, parent-in-room and child-protection fields beyond the flags above (kept, because safeguarding needs them, but UNVERIFIED as platform practice).

## 8. Fit with the existing code and seeds

Current seed templates and where they go. Rule 3 of the spec (add, never change meaning) means renamed keys are added as new keys and the old ones deprecated.

| Seed template (`seeds.py`) | Seed list types using it | New family |
|---|---|---|
| doctors | Doctors, Eye doctors, Nurses, **Data scientists** | medical_practitioners; **Data scientists move to digital_talent_and_agencies** (seed error) |
| hospitals | Hospitals, Eye hospitals | health_facilities |
| labs_imaging | MRI and imaging centres, Laboratories | diagnostics_and_imaging |
| pharmacies_pumps | Medical stores and pharmacies, Petrol pumps | split: pharmacy_and_optical and fuel_and_utility_supply |
| schools | Schools | education_institutions |
| tutors | Quran tutors, Tutors | tutors_and_instructors |
| trades | Plumbers, Electricians, Mobile phone repair | repair_and_trade_services |
| contractors | Contractors | construction_and_design_firms |
| real_estate | Real estate agents | real_estate_agents_and_developers |
| hotels | Hotels | accommodation_and_travel |
| manufacturers | Football makers, Fan makers, Sanitaryware makers, Furniture makers, Factories and suppliers, Surgical instrument makers | manufacturers_and_exporters (the 11 seeded fields are kept with the same keys) |
| retail | Bookshops, **Bakeries**, Mobile stores, Spare parts shops, Furniture stores, Hardware shops, **Beauty parlours and salons** | retail_shops; Bakeries move to food_and_beverage_outlets; Beauty parlours and salons move to personal_care_wellness_fitness |

Key renames to treat as new keys: doctors `regulator_number` to `regulator_registration` (text becomes identifier_list), `languages_spoken` to core `languages`; hospitals `licence_number` to `facility_licence`, `accreditation` to `accreditations`; labs `accreditation` to `accreditations`; schools `registration_body` to `registration`, `grades` to `grades_offered`; contractors `category` to `registration_category`, `registration_body` to `professional_registrations`; hotels `check_in` and `check_out` to `check_in_time` and `check_out_time`, `star_class` kept; pharmacies `delivery` to `home_delivery`, `licence_number` unchanged as `drug_licence`; trades `display_name` to core `name`; real_estate `licence_number` to `licence`, `areas_served` kept as `areas_served`. Manufacturer keys are unchanged (`business_type`, `product_categories`, `tax_ids`, `year_established`, `years_exporting`, `export_markets`, `certifications`, `verification_tier`, `capacity_band`, `workforce_band`, `oem`, `moq`).

## 9. Decisions and questions for the owner

1. **Family count.** 29 families against about 25. Cheapest merges: personal_lists into topic_and_curated_lists (differ only in show and consent), pharmacy_and_optical into retail_shops (loses the licence fields), property_listings with classified_listings (listing items), financial_providers into professional_advisers. That gives 25. Cost: more variant-only fields per template.
2. **Asking prices on property and vehicle listings.** The decision log puts prices behind subscription. On Zameen and PakWheels the price is the first thing a visitor sees (listing pages returned with price in the title). A locked price on a classified listing may make the list useless for free users. Suggested: free for classified listings, locked for service prices.
3. **Gender fields** (self-declared gender, tutor gender, accepted student gender, female-staff-only, clientele): useful in Pakistan and the Gulf, personal data, and a discrimination question in hiring-adjacent lists. Suggested: keep clientele and female_staff_only (service facts), keep gender_self_declared optional, and get counsel on tutors and domestic workers before launch.
4. **Public helplines** (police 15, rescue 1122 and similar) versus "never show a phone". Suggested: allow `public_helpline` only for government bodies and emergency services, from an official source.
5. **Entity types and the owner-only show value** (section 3).
6. **Talent and child-facing families** stay built but unpublished until counsel and the safeguarding design (Q-S2), as the decision log already says.
7. **Combined catalogue list types** such as "Roofers, waterproofing, solar, windows, doors, flooring, other LSA home jobs" or "Doctors and specialists by specialty" are really lists of lists. They share a family template but should probably be split into narrower list types later; the template does not need to change.

## 10. UNVERIFIED register and next verification steps

Highest-risk guesses, in order:
- Pakistan register names and reach: Pakistan Nursing Council, Pakistan Pharmacy Council, PCATP, provincial veterinary councils, PNAC, PSEB, PASHA, provincial tourism department registers, OGRA and explosives licences, customs clearing agent licences, route permits, food authority grades, halal certifiers, security agency licensing, real estate regulatory authorities. All named from background knowledge or the 2026-10-05 notes, none checked this round.
- Platform field lists seen only through scraper descriptions (Justdial, Zameen, PakWheels, Zomato, Upwork, Alibaba, Yelp, Thumbtack): the platform's own pages were not read.
- Safeguarding fields (parent-present policy, child-protection policy, staff background check, staff to child ratio) are reasoned, not observed on any platform; only Wyzant shows a background-check status and Care.com a CareCheck flag.
- Gender-related fields and Pakistan-specific filters (family section, women-only, PTA approval, zakat) are local practice, not found on any checked platform.
- Wedding-venue, vehicle-for-hire, funeral and similar Pakistani field sets: no Pakistani source read.

Next steps, as the earlier drafts already proposed: with a session that can open pages, read 5 live listings per family (priority: Marham and Oladoc doctors, Zameen agency and project pages, PakWheels, Justdial pharmacy and salon pages, Zomato Pakistan) and tick fields against these tables; compute fill rates and drop fields nobody fills; email each register body for written reuse terms (Q-S3) before storing anything beyond a verified flag; have counsel review the personal, child and health-price tags before any collection.

## 11. Files

- This file: `research_notes/Backend research/01_entry_fields_per_family.md`.
- Machine-readable: `research_notes/Backend research/01_entry_fields.csv` (586 data rows: 27 core and 555 family fields, 29 families). Columns: family, key, label, type, required, show, filterable, row_descriptor, sensitivity. Source (register, owner, survey, agent), enum values and notes are in the tables here, not in the CSV.
