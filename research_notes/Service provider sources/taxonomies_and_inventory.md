# Service-Provider Taxonomies and Master Inventory of Provider List Types (AllLists.org)

Research date: 2026-10-05. Method: web search only. Direct page fetches were blocked by the network egress proxy for unstats.un.org, docs.overturemaps.org, isco.ilo.org, census.gov, schema.org and wiki.openstreetmap.org, so most facts below come from search-result summaries of those sites or from third-party pages. Where a figure comes from a secondary or aggregator site this is flagged. Items I know from background knowledge but could not source are placed under Gaps or marked "UNVERIFIED" and must not be treated as confirmed. The inventory table in the last section is the author's own design, not a sourced fact.

---

## 1. Industry classifications (ISIC, NAICS, NACE, UK SIC, PSIC, NIC, CPC, UNSPSC): structure, size, licence, languages, fit for local services

### Takeaway
ISIC is the global spine: Rev. 5 has 22 sections, 87 divisions, 258 groups and 463 classes, and Pakistan's PSIC (identical to ISIC Rev. 4 to 4-digit) and India's NIC (NIC 2025 aligned to ISIC Rev. 5) can be mapped through it. All industry classifications are activity-based and far too coarse for consumer-facing list types (for example, "eye hospital" or "Quran tutor" have no dedicated code), so they suit as crosswalk tags only, not as the user-facing category tree. Licence and language terms for most of them could not be verified in this session.

### Cited Findings
- ISIC Rev. 5 was endorsed by the UN Statistical Commission at its 54th session in March 2023 — [UNSD/ECOSOC search summary](https://ecosoc.un.org/sites/default/files/documents/2023/2023-13-Classifications-E.pdf) (via search result; page itself not fetched)
- ISIC Rev. 5 structure: 22 sections, 87 divisions, 258 groups, 463 classes. ISIC Rev. 4: 21 sections, 88 divisions, 238 groups, 419 classes — [classification.codes ISIC (secondary aggregator)](https://classification.codes/classifications/industry/isic); official UNSD pages at [unstats.un.org ISIC Rev 5 intro](https://unstats.un.org/unsd/classifications/Workshops/Santiago2025/Session2.1_UNSD_Intro_to_ISIC_Rev5_rev1.pdf) could not be fetched to confirm
- ISIC Rev. 5 split Rev. 4 Section J into two sections and added 18 new intermediation-service classes; the in-store versus online retail distinction was removed — [UNSD ISIC Rev. 5 materials (search summary)](https://unstats.un.org/unsd/classifications/Workshops/AddisAbaba2026/Session3-Deck1_WorkshopAddis_intro_to_isic_rev5.pdf)
- NAICS 2022: 20 sectors, 99 subsectors, 309 industry groups, 689 five-digit industries and 1,012 six-digit US national industries — [US Census NAICS 2022 structure file (via search summary)](https://www.bls.gov/cew/classifications/industry/naics-2022.htm) (BLS page listed; counts attributed to Census structure file by the search tool)
- NACE Rev. 2.1: 22 sections, 87 divisions, 287 groups, 651 classes; developed by Eurostat with national statistical institutes, the ECB and over 270 European trade associations consulted — [JobsPipe summary (secondary)](https://jobspipe.dev/blog/nace-codes); national adoptions e.g. [Latvia CSP NACE 2.1](https://csp.gov.lv/en/classifier/nace-21), [Spain INE CNAE 2025 explanatory note](https://ine.es/en/daco/daco42/clasificaciones/cnae25/documento_explicativo_CNAE_2025_en.pdf)
- UK SIC 2007: 21 sections (A to U), divisions, groups (3-digit), classes (4-digit) and some 5-digit subclasses; ONS content including SIC 2007 is published under Open Government Licence v3.0 — [ONS UK SIC page](https://www.ons.gov.uk/methodology/classificationsandstandards/ukstandardindustrialclassificationofeconomicactivities) and [datahub.io UK SIC 2007](https://datahub.io/core/uk-sic-2007-condensed); total class count not confirmed
- Pakistan PSIC Rev-4 (2010), maintained by Pakistan Bureau of Statistics, is identical to ISIC Rev. 4 up to the 4-digit class level, with a five-level structure extending to subclasses — [PBS PSIC 2010 PDF](https://www.pbs.gov.pk/sites/default/files/other/documents/PSIC_2010.pdf), [PBS LFS PSIC document](https://www.pbs.gov.pk/sites/default/files/labour_force/publications/lfs2020_21/Pakistan_Standard_Industrial_Classification.pdf), [classification.codes PSIC](https://classification.codes/classifications/industry/psic-pakistan)
- India NIC 2008: 88 divisions, 238 groups, 403 classes, 1,304 subclasses (5-digit). NIC 2025 released by MoSPI on 18 November 2025, moves to a 6-digit structure aligned with ISIC Rev. 5 — [SetIndiaBiz NIC 2008](https://www.setindiabiz.com/wiki/nic-2008), [SetIndiaBiz NIC 2025](https://www.setindiabiz.com/wiki/nic-2025), [TaxTMI](https://www.taxtmi.com/news?id=62048) (secondary sources; MoSPI primary page not fetched)
- UNSPSC: 8-digit code, four levels (Segment, Family, Class, Commodity) plus optional business-function level; 57 segments; v26.0801 (August 2023) cited as 158,448 items; created by UNDP and Dun & Bradstreet in 1998, managed by GS1 US until 2024 then reverted to UNDP; no royalty or licence fee for basic use, paid subscriptions for modification requests, multiple users and advanced search — [Wikipedia UNSPSC](https://en.wikipedia.org/wiki/UNSPSC), [unspsc.org FAQs](https://www.unspsc.org/faqs), [Government of Canada UNSPSC download](https://buyandsell.gc.ca/procurement-data/unspsc/download-unspsc). The 158,448 figure and 57 segments come from secondary sources and look inconsistent with how UNSPSC counts are usually quoted; treat as UNVERIFIED

### Inferences
- Because PSIC equals ISIC Rev. 4 to 4 digits, an ISIC Rev. 4 crosswalk gives Pakistan coverage for free; a Rev. 4 to Rev. 5 correspondence is needed for forward compatibility and for India (NIC 2025).
- Industry codes classify the activity of an establishment, so they fit firm-type lists (bakery, clinic, petrol pump) but not individual tradespeople (mistri) or searcher vocabulary. Use them as optional crosswalk attributes, not as the primary browse tree.
- NACE Rev. 2.1 is effectively ISIC Rev. 5 at the top levels with an extra EU digit; for a global product ISIC is the better anchor and NACE/NAICS/UK SIC become optional extra crosswalks.
- UNSPSC is built for procurement of products, with services thinly covered; low value for consumer service lists, and its paid-subscription component makes it a poor base.

### Gaps
- Official licence/copyright terms for ISIC, CPC, NACE (Eurostat RAMON) and NAICS were not retrieved because the sites were blocked. Background belief (UNVERIFIED): NAICS is a US federal product reusable without fee; Eurostat reuse is generally under Commission reuse policy (CC BY 4.0 style); UN classifications are published with UN copyright but freely downloadable. Verify before relying.
- Availability of ISIC/ISCO/NACE in Urdu and Arabic was not verified. UN official languages include Arabic, so an Arabic ISIC is plausible (UNVERIFIED); no evidence found for an official Urdu version.
- UN CPC (Ver. 2.1 / Ver. 3) structure and counts were not researched in detail.
- Total code counts for UK SIC 2007, PSIC, and the official NAICS 2022 licence statement were not retrieved.
- Whether NAICS 2027 revision is under way was not checked.

---

## 2. Occupation classifications (ISCO-08, O*NET-SOC, UK SOC, national trade classifications): coverage of skilled trades and tutors

### Takeaway
ISCO-08 (436 unit groups, free to use) is the right individual-provider classification for a global product, with Major Group 7 (Craft and Related Trades Workers) covering plumbers, electricians, carpenters, bricklayers and refrigeration mechanics. O*NET-SOC 2019 (1,016 titles) is richer but US-centred; its licence (CC BY 4.0) could not be re-verified. Pakistan's NAVTTC/NVQF trade lists were not retrieved.

### Cited Findings
- ISCO-08 has 436 unit groups, 130 minor groups, 43 sub-major groups and 10 major groups; Group 7 is "Craft and Related Trades Workers", Group 2 "Professionals", Group 5 "Service and Sales Workers" — [ILO ISCO-08 structure](https://www.ilo.org/publications/international-standard-classification-occupations-2008-isco-08-structure), [ISCO site](https://isco.ilo.org/en/isco-08), [Wikipedia ISCO](https://en.wikipedia.org/wiki/International_Standard_Classification_of_Occupations)
- ISCO is available online free of charge and can be used without prior authorization — [ISCO site (search summary)](https://isco.ilo.org/en/isco-08)
- ISCO-08 structure was published in English, French and Spanish on the ILO site in 2008, and Eurostat worked with member states on other EU languages — [UNSD expert-group paper AC124-14 (search summary)](https://unstats.un.org/unsd/classifications/ExpertGroup/EGM2007/AC124-14.pdf)
- ISCO-08 is under revision by the ILO with a goal of availability for the 2030 census round; no confirmed adoption date for a successor found — [UNSD/ILO ISCO-08 progress papers](https://unstats.un.org/unsd/classifications/Meetings/UNCEISC2024_2nd/Session_3_Progress%20of%20work%20ISCO_08.pdf), [ILO ISCO news](https://isco.ilo.org/en/news/)
- O*NET-SOC 2019 taxonomy: 1,016 occupational titles, of which 923 are data-level occupations, built on 867 SOC detailed codes, 459 broad occupations, 98 minor groups and 23 major groups — [O*NET Center taxonomy](https://www.onetcenter.org/taxonomy.html), [O*NET-SOC 2019 report](https://onetcenter.org/reports/Taxonomy2019.html)
- UK SOC 2020: 412 four-digit unit groups; the ONS extended SOC 2020 expands this to 1,384 six-digit unit groups — [Lightcast UKSOC 2020 summary (secondary)](https://docs.lightcast.io/data/docs/uk-standard-occupational-classification-uksoc-2020), [ONS extended SOC](https://www.ons.gov.uk/methodology/classificationsandstandards/standardoccupationalclassificationsoc/standardoccupationalclassificationsocextensionproject)
- ONS content is under Open Government Licence v3.0 unless stated — [ONS SIC page](https://www.ons.gov.uk/methodology/classificationsandstandards/ukstandardindustrialclassificationofeconomicactivities)
- NAVTTC says it has issued NVQF-aligned qualifications in 25 important trades (including high-tech fields), with examples such as Level-5 Diplomas in Electrical Technology and Electronic Technology; an updated NAVTTC trade list dated 28 December 2025 exists on NAVTTC/Takamol portals — [Pakistan Observer](https://pakobserver.net/shafqat-terms-launch-of-level-5-qualification-a-landmark-achievement/), [TVET Reform Pakistan](https://tvetreform.org.pk/?p=6993); search result snippet only
- India's NCO 2015 was not confirmed by this search.

### Inferences
- Using ISCO-08 unit-group codes as crosswalk tags for individual providers allows mapping to national schemes via standard correspondences (O*NET, UK SOC, ESCO), but ISCO has no dedicated unit group for many modern or informal roles (mobile repair technician, Quran tutor, data scientist) so these map to broader groups (UNVERIFIED mapping suggestions below).
- NAVTTC's 25 main trades list is far shorter than the real set of informal trades (mistri-type roles), so a local alias layer is essential.
- ISCO is the right way to mark a list as "individuals" and ISIC the way to mark it as "establishments".

### Gaps
- Exact ISCO-08 codes for plumber (7126), building electrician (7411), carpenter (7115), bricklayer (7112), refrigeration and AC mechanic (7127), electronics mechanic/ICT servicer (7421/7422), other teaching professionals (2359) are from background knowledge, not verified in this session.
- ILO ISCO-08 official Arabic or Urdu translation: not verified.
- NAVTTC full trade list (plumber, electrician, AC technician, mobile repair), and Punjab TEVTA trade list: not retrieved (search returned only summaries).
- O*NET licence (CC BY 4.0) was not re-verified here, although the task brief states it.

---

## 3. Platform and map taxonomies: size, licence, multilingual support, commercial reuse

### Takeaway
Only a few platform/map taxonomies are safely reusable: Overture Maps places taxonomy (CDLA-Permissive-2.0 for the places theme, about 2,300 categories with parent/child hierarchy, rebuilt in 2026) and Foursquare OS Places categories (Apache 2.0, 1,000+ categories, up to six levels) are the cleanest. OSM tags are open under ODbL (attribution and share-alike obligations). Google Business Profile (about 4,000 categories) and Yelp categories are proprietary or term-restricted and should only inform, not be copied. Multilingual label coverage was not verified for any of them.

### Cited Findings
- Overture Maps places theme: more than 64 million places; licensed CDLA-Permissive-2.0 (several sources named, including Meta, Microsoft, PinMeTo, RenderSEO, Krick and DAC) — [Overture Places Guide](https://docs.overturemaps.org/guides/places), [Overture on AWS Open Data](https://registry.opendata.aws/overture/)
- Overture's redesigned `taxonomy` property has roughly 2,300 categories with broader/narrower relationships; top-level categories reduced from 22 to 13; 209 new categories added, 80 removed, 407 renamed (mostly plural to singular); the old `categories` property was deprecated and scheduled for removal in the June 2026 release; `basic_category` added — [Overture taxonomy guide](https://docs.overturemaps.org/guides/places/taxonomy/), [2025-12-17 release notes](https://docs.overturemaps.org/blog/2025/12/17/release-notes/), [Overture Summit 2026 taxonomy PDF](https://hosted-files.sched.co/overturesummit2026/38/Overture%20Place%20Categories%20Taxonomy.pdf), [2026-06-17 release notes](https://docs.overturemaps.org/blog/2026/06/17/release-notes/) (search summaries; pages not fetched)
- The Overture schema repository has no explicit licence statement in the README fetched; legacy YAML schema scheduled for removal December 2026 — [OvertureMaps/schema README](https://raw.githubusercontent.com/OvertureMaps/schema/main/README.md). Licence of the taxonomy file itself should be checked in the repo.
- Foursquare OS Places: more than 1,000 categories, hierarchy up to six levels, category IDs and labels, available for commercial use under Apache 2.0 — [Foursquare OS Places docs](https://docs.foursquare.com/data-products/docs/fsq-places-open-source), [Foursquare categories](https://docs.foursquare.com/developer/docs/categories), [Simon Willison on release (Nov 2024)](https://simonwillison.net/2024/Nov/20/foursquare-open-source-places)
- Google Business Profile: 4,046 categories as of 9 May 2026 (third-party count); 4,098 as of 23 October 2024 (US); each profile picks one primary and up to nine additional categories; the list changes often — [Dalton Luka GBP list](https://daltonluka.com/blog/google-my-business-categories), [classification.codes GMB](https://classification.codes/classifications/industry/gmb), [BrightLocal GBP categories](https://www.brightlocal.com/learn/google-business-profile-categories/). Google's own licence terms for reusing the category list were not found.
- Yelp Fusion API: category objects with alias, title, parentAliases, country whitelist/blacklist; Yelp content other than business IDs should not be stored beyond 24 hours; review excerpts limited; brand/attribution rules apply; 32 countries — [Zuplo Yelp API overview](https://zuplo.com/blog/2025/06/03/yelp-api), [ReviewTrackers](https://www.reviewtrackers.com/?p=30814), [APIs.io Yelp JSON-LD context](https://apis.io/jsonld/yelp/yelp-fusion-api-context/) (secondary; Yelp terms page not fetched)
- OpenStreetMap data is under ODbL: commercial use allowed with attribution, and share-alike for derived databases; "Produced Works" such as maps carry lighter obligations — [OSMF Licence and Legal FAQ](https://osmfoundation.org/wiki/Licence_and_Legal_FAQ), [OSM wiki License/Use Cases](https://wiki.openstreetmap.org/wiki/License/Use_Cases)
- Schema.org lists more than 160 LocalBusiness subtypes, including HomeAndConstructionBusiness with subtypes Electrician, GeneralContractor, HVACBusiness, HousePainter, Locksmith, MovingCompany, Plumber, RoofingContractor — [Local Search Forum thread](https://localsearchforum.com/threads/localbusiness-schema-greatly-expanded-see-full-list.46028/latest), [Hackage schema mirror](https://hackage-origin.haskell.org/package/metadata-0.1.0.2/docs/Text-HTML5-MetaData-Schema-HomeAndConstructionBusiness.html) (secondary; schema.org page was blocked)
- Sulekha: over 40 cities and 800+ categories (BW Disrupt) versus roughly 1,200 categories (other source) — [BW Disrupt](https://bwdisrupt.com/article/sulekha-catering-to-over-40-cities-across-800-plus-categories-in-local-service-market-99824); conflicting figures, dates unclear
- Urban Company: services in over 150 categories (one source) versus 50+ types; 59 cities and 4 countries (one source) versus 51 cities across India, UAE and Singapore, 47 of them in India, as at 30 June 2025, excluding KSA joint-venture cities — [Khaleej Times](https://www.khaleejtimes.com/uae/india-urban-company-reports-exponential-growth-during-raging-covid-19-pandemic?amp=1), [HDFC Sky IPO page](https://hdfcsky.com/ipo/urban-company-ipo)
- Justdial category count: not found.

### Inferences
- Overture taxonomy is the best open place-category hierarchy to adopt or fork: permissive licence, fixed IDs, hierarchy, active maintenance, and designed for global places. Its weakness is that it classifies places (premises), so individual-provider types and informal trades need AllLists additions.
- Foursquare's taxonomy is a good second reference and tie-breaker, being Apache 2.0.
- GBP's list is the most complete and service-business oriented (plumber, locksmith, tutor types), so it is valuable as a coverage checklist, but copying wholesale carries unverified legal risk; use it to find gaps, then name categories independently.
- OSM share-alike applies to databases derived from OSM data; using OSM tag keys purely as reference tags in crosswalks is lower risk than importing OSM POI data into AllLists records (needs legal review).
- Wikidata (CC0, multilingual labels) is the natural way to carry multilingual labels and synonyms, but I could not verify its licence or label coverage for Urdu/Arabic here.

### Gaps
- OSM tag counts (craft=*, shop=*, amenity=*, office=*, healthcare=*) not retrieved because the OSM wiki was blocked.
- Wikidata licence (CC0 is background knowledge, UNVERIFIED), schema.org licence (CC BY-SA 3.0 is background knowledge, UNVERIFIED) and multilingual label coverage were not retrieved.
- Overture taxonomy multilingual support (it appears to carry English names only) and the licence of the taxonomy CSV specifically were not verified.
- Yelp category count, Justdial category count, Google reuse terms were not found.
- Whether Overture's taxonomy contains specific service categories (plumber, electrician, tutor, AC repair, mobile phone repair, Quran tutor) was not confirmed; I did not see the category list.

---

## 4. Recommendation: base taxonomy, synonyms and local names, code mapping

### Takeaway
Recommended design (author's judgment based on the findings above): a two-layer AllLists "concept" taxonomy seeded from Overture places taxonomy (CDLA-Permissive-2.0) plus an AllLists-owned provider layer for individuals and informal trades, with a separate alias table for synonyms and local names, and crosswalk columns to ISIC Rev. 4/5, ISCO-08, Wikidata, Overture, Foursquare, OSM and schema.org. Not legal advice; licences should be re-verified from primary sources.

### Cited Findings
- Overture places theme under CDLA-Permissive-2.0 with a redesigned hierarchical taxonomy — [Overture Places Guide](https://docs.overturemaps.org/guides/places)
- Foursquare categories under Apache 2.0 — [Foursquare OS Places](https://docs.foursquare.com/data-products/docs/fsq-places-open-source)
- PSIC identical to ISIC Rev. 4 to 4 digits; NIC 2025 aligned to ISIC Rev. 5 — [PBS PSIC](https://www.pbs.gov.pk/sites/default/files/other/documents/PSIC_2010.pdf), [SetIndiaBiz NIC 2025](https://www.setindiabiz.com/wiki/nic-2025)
- ISCO free to use without prior authorization — [ISCO site](https://isco.ilo.org/en/isco-08)
- O*NET-SOC 2019 maps 1,016 titles to 867 SOC codes — [O*NET taxonomy](https://www.onetcenter.org/taxonomy.html)
- Yelp restricts storage of its data to about 24 hours outside live queries — [Zuplo](https://zuplo.com/blog/2025/06/03/yelp-api)

### Inferences
Proposed architecture:
1. **Concept table (language-neutral)**: `concept_id` (stable AllLists ID, never reused), `parent_id`, `kind` (place-type / individual-role / both), `default_reach` (hyper-local, city, region, national, global), `provider_form` (firm, individual, both), `customer` (household, business, both), status and version.
2. **Label and alias table**: `concept_id`, `lang` (BCP 47 such as en, ur, ur-Latn for Roman Urdu, ar, hi, pa), `text`, `kind` (preferred, synonym, local-name, abbreviation, misspelling), `region` (country or area where used, for example PK, IN, US, UK), `register` (formal, colloquial). Example: concept "fuel station" with en preferred "petrol pump" in PK/IN, "gas station" in US, "fuel station" in generic/UAE contexts (the alias table, not the concept, encodes the regional word, so one list serves all). "mistri" (ur-Latn, hi, PK/IN) points to plumber, electrician, carpenter, mason or mechanic depending on context, so model it as an ambiguous alias that maps to a parent concept "skilled tradesperson" with disambiguation prompts rather than a single concept.
3. **Crosswalk table**: `concept_id`, `system` (isic4, isic5, isco08, naics2022, nace21, psic2010, nic2025, onet, overture, fsq, osm, wikidata, schema_org, gbp), `code`, `match_type` (exact, broader, narrower, related) following SKOS mapping semantics. Store AllLists-authored mappings; do not copy proprietary lists (GBP, Yelp) into the crosswalk.
4. **Seeding**: import Overture taxonomy and Foursquare categories as initial place concepts, add ISCO-08 unit groups as individual-role concepts, then add AllLists-specific local concepts (Quran tutor, mobile repair, mistri trades, society-level services). Verify each source licence from the primary page and keep attribution notices for CDLA/Apache/ODbL material.
5. **Depth**: keep user-facing browse tree to about 3 levels (top-level group, type, sub-type) and hold finer detail as tags, because list-size and contributor effort scale poorly with deep trees.
6. **Governance**: versioned IDs, deprecation with redirects, community-proposed aliases moderated by language reviewers.
- Rejected as base: UNSPSC (procurement, paid add-ons), GBP list (reuse terms unclear, English-centric), Yelp (storage restrictions), NAICS/NACE/UK SIC (country-specific and activity-level, but fine as crosswalks).

### Gaps
- Primary-source confirmation of all licence terms (Overture taxonomy file, Foursquare taxonomy file, ISIC, Wikidata, schema.org) before launch.
- No evidence gathered on how well any taxonomy handles Urdu or Arabic labels; a native-language review pass is required.

---

## 5. Evidence on reach: how people choose providers by category

### Takeaway
Evidence found supports a tiered reach model: urgent and routine services are chosen very locally; specialist healthcare draws longer travel; contractor platforms define service radii in tens to 150 miles; remote professionals have no geography. The sources found are mostly secondary and US-centric, and BrightLocal/Google primary distance data could not be retrieved.

### Cited Findings
- Google "near me" research (as repeated by secondary sites): 76% of people who search for something nearby on a smartphone visit a related business within a day and 28% purchase; about 1.5 billion near-me searches per month; 84% of local searches on mobile — [Think with Google mobile near-me searches](https://thinkwithgoogle.com/data/mobile-near-me-searches), [BrightLocal on near-me](https://www.brightlocal.com/blog/is-googles-near-me-still-effective-for-local-seo/), [seolocal.it.com statistics (aggregator)](https://seolocal.it.com/near-me-search-statistics/). The 76% figure is old Google data repeated widely; the aggregator figures are not primary.
- Patient travel: median travel time 12.7 minutes for primary care versus 17.1 minutes for specialty care in one study; patients travel about 20% longer and 30% farther for specialists; over 50% of primary-care visits within 10 minutes' drive; outside metropolitan areas specialty-care median travel was 41.8 minutes versus 15.9 minutes inside — [Arcadia "A drive to the doctor"](https://arcadia.io/a-drive-to-the-doctor), [HealthDay summary](https://www.healthday.com/healthpro-news/public-health/patients-living-outside-metropolitan-statistical-areas-travel-farther-for-health-care-visits), [AJMC (Nov 2024)](https://www.ajmc.com/view/discrepancies-identified-between-patient-travel-patterns-geographic-market-definitions). Attribution of each figure to a specific study was not confirmed from the search snippets. All are US data.
- Rural Medicare patients: median one-way trip 7.7 miles and 11.7 minutes in one study; rural residents travel two to three times farther to specialists — [UW Center for Health Workforce Studies](https://familymedicine.uw.edu/chws/studies/access-to-physician-care-for-the-rural-medicare-elderly/)
- Thumbtack: default service area radius of 150 miles in pro settings, extendable by uploading up to 1,000 zip codes; a "works remotely" option shows a professional to customers everywhere — [Thumbtack Community threads](https://community.thumbtack.com/discussion/comment/5432), [Thumbtack Community, remote option](https://community.thumbtack.com/discussion/comment/6506/) (user-community posts, not official documentation)
- Urban Company operates city by city: 48,000+ active service professionals, over 13 million consumers across 59 cities and 4 countries (one source); 51 cities as of 30 June 2025 (another) — [Trendlyne](https://trendlyne.com/posts/5313241), [HDFC Sky](https://hdfcsky.com/ipo/urban-company-ipo); conflicting counts, likely due to date or joint-venture scope
- BrightLocal's Local Consumer Review Survey 2025 exists but the distance-willingness data was not found in retrieved summaries — [BrightLocal LCRS 2025](https://www.brightlocal.com/research/local-consumer-review-survey-2025/)

### Inferences
- Emergency and recurring home services (plumbing, electrician, AC repair, locksmith, petrol, pharmacy) are chosen on proximity and availability, supporting hyper-local (housing society to neighbourhood) lists, with a city list as the upper practical bound for marketplaces that dispatch.
- Specialist healthcare (eye surgeon, MRI centre, oncologist) shows longer travel and rural users travel much farther, supporting city and regional lists, with national lists only for rare specialisms.
- Platforms (Thumbtack, Urban Company) confirm that even "local" service marketplaces are organised by city, with radii of tens of miles; national and global lists make sense mainly for tender-based contractors, remote professionals and regulated bodies.
- US data may not transfer to Pakistan, India or the Gulf, where societies/gated communities and informal word of mouth dominate; this should be tested with early contributors.

### Gaps
- No primary BrightLocal or Google data on distance willingness by category; no Pakistan or South Asia evidence on provider search radii; no source found on national tender-based contractor selection (for example PEC contractor registration, Pakistan PPRA e-procurement); no global remote-professional marketplace statistics (for example Upwork) were gathered.

---

## 6. Inventory: service-provider list types (124 types) with natural reach

### Takeaway
The table below is the author's synthesis (not a sourced dataset) and gives 124 provider types in 15 groups, each with a proposed natural reach based on the reach evidence above. Reach codes: **HL** hyper-local (housing society, neighbourhood), **CITY**, **REG** (province, state, metro region), **NAT** national, **GLOB** global. Customer: HH household, BIZ business, BOTH. Provider form: F firms/establishments, I individuals, M mixed. All reach assignments are judgment calls to be tested with contributor data.

### Cited Findings
- The structure of the table follows the categories the task brief asked for and aligns loosely with ISIC and ISCO groupings: Group 7 of ISCO-08 for trades, Group 2 for professionals — [ILO ISCO-08](https://www.ilo.org/publications/international-standard-classification-occupations-2008-isco-08-structure)
- Schema.org's HomeAndConstructionBusiness subtypes (Electrician, GeneralContractor, HVACBusiness, HousePainter, Locksmith, MovingCompany, Plumber, RoofingContractor) corroborate rows A1 to A8 as established local-service types — [Local Search Forum](https://localsearchforum.com/threads/localbusiness-schema-greatly-expanded-see-full-list.46028/latest)
- Urban Company's focus on home and beauty services at city level supports the household and beauty rows — [HDFC Sky](https://hdfcsky.com/ipo/urban-company-ipo)

### Inferences (the inventory)

**A. Home repair and skilled trades**

| # | Type | Example sub-types | Customer | Form | Reach | Why |
|---|---|---|---|---|---|---|
| A1 | Plumbers | leak repair, bathroom fitting, tank cleaning | HH | I (some F) | HL | Founder example. Urgent, proximity-driven, trust within a society; word of mouth. |
| A2 | Electricians | wiring, fault repair, solar and UPS wiring | HH | I | HL | Urgent, small callout; society-level trust. |
| A3 | Carpenters | furniture repair, doors, kitchens | HH | I | HL to CITY | Site visit needed, moderate radius. |
| A4 | Masons and tile fixers | plaster, tiling, small renovation | HH | I | HL to CITY | On-site labour; radius limited by travel. |
| A5 | AC technicians | install, gas refill, servicing | HH, BIZ | I, F | HL to CITY | Seasonal urgent demand; short response time. |
| A6 | Painters | interior, exterior, polishing | HH | I, F | CITY | Quote-based, planned; modest radius. |
| A7 | Welders and fabricators | gates, grills, sheds | HH, BIZ | I, F | CITY | Workshop-based with site install. |
| A8 | Locksmiths | door, car, safe | HH | I | HL to CITY | Emergency service, nearest wins. |
| A9 | Roofing and waterproofing | leak sealing, heat insulation | HH | F | CITY | Planned job, quote comparisons. |
| A10 | Pest control and fumigation | termites, cockroaches | HH, BIZ | F | CITY | Booked in advance, area coverage. |
| A11 | Water tank and RO plant services | cleaning, filter change | HH, BIZ | F | HL to CITY | Recurring local routes. |
| A12 | Gas, geyser and stove repair | geyser, heater, stove | HH | I | HL | Urgent, local. |
| A13 | Generator, UPS and solar installers | inverter, panels | HH, BIZ | F | CITY to REG | Higher ticket, planned, comparison shopped. |
| A14 | Handymen / mistri (general) | mixed minor fixes | HH | I | HL | Founder alias example; ambiguous word needs disambiguation. |

**B. Appliance and device repair**

| # | Type | Example sub-types | Customer | Form | Reach | Why |
|---|---|---|---|---|---|---|
| B1 | Mobile phone repair | screen, battery, software | HH | F (shops), I | HL to CITY | Founder example. Walk-in, drop-off, proximity and market clusters. |
| B2 | Laptop and computer repair | hardware, OS install | HH, BIZ | F, I | CITY | Drop-off tolerance for a few km. |
| B3 | Home appliance repair | washing machine, fridge, TV | HH | F, I | HL to CITY | Home visit radius. |
| B4 | Car mechanics and workshops | tune-up, denting, tyres | HH, BIZ | F | CITY | Repeat service, trust and price. |
| B5 | Motorcycle repair | puncture, engine | HH | F, I | HL | Everyday need, nearest shop. |
| B6 | Tyre and battery shops | puncture, replacement | HH | F | HL to CITY | Emergency near road. |
| B7 | Car wash and detailing | wash, polish | HH | F | HL | Convenience driven. |
| B8 | Watch, shoe and bag repair | stitching, sole repair | HH | I, F | HL | Low-ticket, neighbourhood. |
| B9 | Camera, printer and photocopier repair | office machines | BIZ, HH | F | CITY | Specialist with smaller supply. |
| B10 | CCTV and security system installers | cameras, alarms | HH, BIZ | F | CITY | Quote, installation visit. |

**C. Construction, contracting and property**

| # | Type | Example sub-types | Customer | Form | Reach | Why |
|---|---|---|---|---|---|---|
| C1 | General and civil contractors | roads, buildings, tender work | BIZ, gov | F | NAT | Founder example. Selected via registration and tenders, not distance. |
| C2 | Architects and designers | residential, commercial | HH, BIZ | M | CITY to NAT | Portfolio-led; reputation travels. |
| C3 | Interior designers | home, office fit-out | HH, BIZ | M | CITY | Site visits; reputation. |
| C4 | Civil, structural and MEP engineers | design, supervision | BIZ | M | NAT | Project-based; regulatory registration. |
| C5 | Quantity surveyors and valuers | cost, property valuation | BIZ, HH | M | NAT | Professional registration. |
| C6 | Real estate agents and developers | sales, rentals | HH, BIZ | M | HL to CITY | Local knowledge is the product; society-level lists valuable. |
| C7 | Building material suppliers | cement, steel, bricks | BIZ, HH | F | CITY to REG | Delivery radius. |
| C8 | Heavy equipment rental | cranes, excavators | BIZ | F | REG to NAT | Moves long distances for big jobs. |
| C9 | Surveyors and land services | boundary, topographic | BIZ, HH | M | REG | Local land records. |

**D. Healthcare**

| # | Type | Example sub-types | Customer | Form | Reach | Why |
|---|---|---|---|---|---|---|
| D1 | General practitioners and clinics | family doctor | HH | M | HL | Proximity dominates; 12.7 min median travel in cited US data. |
| D2 | Eye doctors / ophthalmologists | cataract, LASIK, retina | HH | I | HL to CITY | Founder example; individual specialist lists work at society or city level. |
| D3 | Eye hospitals | cataract hospitals, optical chains | HH | F | CITY to REG | Founder example; patients travel farther for institutions. |
| D4 | Dentists | general, orthodontics | HH | M | HL to CITY | Frequent, moderate distance. |
| D5 | Paediatricians | child specialists | HH | I | CITY | Urgency and trust. |
| D6 | Gynaecologists and maternity | obstetrics, IVF | HH | M | CITY | Trust-driven. |
| D7 | Other specialist doctors | cardiology, neurology, ENT | HH | I | CITY to REG | Specialists draw longer travel (17.1 vs 12.7 min). |
| D8 | Hospitals | general, tertiary | HH | F | CITY to REG | Emergency nearest, elective farther. |
| D9 | Diagnostic labs | blood tests, pathology | HH | F | HL to CITY | Collection points near; home-collection radius. |
| D10 | MRI, CT and radiology centres | imaging | HH | F | CITY to REG | Founder example; equipment-limited, referral-driven. |
| D11 | Pharmacies | retail, 24-hour | HH | F | HL | Proximity, emergency. |
| D12 | Physiotherapists and rehab | sports, post-op | HH | M | HL to CITY | Repeated visits. |
| D13 | Mental health | psychologists, psychiatrists | HH | I | CITY to GLOB | Telehealth lowers geography. |
| D14 | Hakeem and homeopathic | traditional medicine | HH | I | HL to CITY | Local reputation. |
| D15 | Veterinary clinics | pets, livestock | HH | M | HL to CITY | Pet owners nearby; livestock need visits. |
| D16 | Ambulance and blood services | ambulance, blood banks | HH | F | CITY | Emergency, city level. |
| D17 | Opticians and optical shops | spectacles, lenses | HH | F | HL | Retail proximity. |

**E. Education and tutoring**

| # | Type | Example sub-types | Customer | Form | Reach | Why |
|---|---|---|---|---|---|---|
| E1 | Schools | primary, secondary, Montessori | HH | F | HL to CITY | Founder example; catchment and commute decide. |
| E2 | Colleges and universities | degree, vocational | HH | F | NAT to GLOB | Students move; international comparison. |
| E3 | Quran tutors | home tutors, online | HH | I | HL to GLOB | Founder example; home tuition is local, online Quran teaching is global. |
| E4 | Madrasas and hifz schools | residential, day | HH | F | CITY to REG | Reputation, residential option. |
| E5 | Academic tutors | maths, science, O/A levels | HH | I | HL to CITY | Home tuition radius; online option. |
| E6 | Coaching centres and academies | MDCAT, CSS, IELTS | HH | F | CITY | Class-based, commute. |
| E7 | Language teachers | English, Arabic, German | HH | I | CITY to GLOB | Online makes geography optional. |
| E8 | Vocational training institutes | TEVTA, NAVTTC courses | HH | F | CITY to REG | Public programmes by district. |
| E9 | Daycare and play groups | child care | HH | F | HL | Pick-up distance. |
| E10 | Driving schools | cars, motorcycles | HH | F | HL to CITY | Practice requires proximity. |
| E11 | Music, art and sports coaches | cricket, swimming, gym | HH | I, F | HL to CITY | Regular sessions. |

**F. Legal, finance and professional services**

| # | Type | Example sub-types | Customer | Form | Reach | Why |
|---|---|---|---|---|---|---|
| F1 | Lawyers | family, property, criminal | HH, BIZ | I, F | CITY to NAT | Court jurisdiction defines geography. |
| F2 | Corporate and tax lawyers | company, IP, tax | BIZ | F | NAT | Specialist, remote-capable. |
| F3 | Notaries and oath commissioners | attestation | HH, BIZ | I | HL to CITY | Walk-in, local office. |
| F4 | Accountants and auditors | bookkeeping, audit | BIZ, HH | F, I | CITY to NAT | Trust, but remote delivery common. |
| F5 | Tax consultants | income tax, sales tax | HH, BIZ | I | CITY to NAT | Seasonal, remote possible. |
| F6 | Banks and branches | branches, ATMs | HH, BIZ | F | HL to NAT | ATM/branch local, bank list national. |
| F7 | Insurance agents | life, motor, health | HH, BIZ | I | CITY | Relationship sales. |
| F8 | Money changers and remittance | currency, transfer | HH | F | CITY | Local counters. |
| F9 | Loan and microfinance providers | microcredit | HH, BIZ | F | REG to NAT | Licensed lenders by region. |
| F10 | Management and business consultants | strategy, HR | BIZ | M | NAT to GLOB | Remote-friendly. |
| F11 | Recruitment agencies | local, overseas | BIZ, HH | F | NAT to GLOB | Overseas placement is cross-border. |
| F12 | Translators and interpreters | document, certified | HH, BIZ | I | NAT to GLOB | Remote delivery. |
| F13 | Immigration and visa consultants | study, work visa | HH | F | NAT to GLOB | Cross-border. |

**G. IT, data and digital professions**

| # | Type | Example sub-types | Customer | Form | Reach | Why |
|---|---|---|---|---|---|---|
| G1 | Data scientists | ML, analytics | BIZ | I | GLOB | Founder example; remote work, global talent market. |
| G2 | Software developers | web, mobile, backend | BIZ | I, F | GLOB | Remote delivery. |
| G3 | Software houses and agencies | outsourcing | BIZ | F | NAT to GLOB | Clients worldwide. |
| G4 | Web designers and SEO | websites, marketing | BIZ | I, F | NAT to GLOB | Remote delivery. |
| G5 | Cybersecurity professionals | pen test, audit | BIZ | M | GLOB | Remote and credential-based. |
| G6 | Cloud and DevOps engineers | AWS, Azure | BIZ | I | GLOB | Remote. |
| G7 | IT support and network installers | LAN, helpdesk | BIZ, HH | F, I | CITY | On-site work. |
| G8 | Freelance digital creatives | design, video, writing | BIZ | I | GLOB | Marketplace-driven. |
| G9 | Digital marketing and social media | ads, content | BIZ | I, F | NAT to GLOB | Remote. |

**H. Beauty, wellness and personal care**

| # | Type | Example sub-types | Customer | Form | Reach | Why |
|---|---|---|---|---|---|---|
| H1 | Beauty parlours | facials, bridal makeup | HH | F, I | HL to CITY | Founder example; frequent, proximity, home service possible. |
| H2 | Barbers and salons (men) | haircut | HH | F | HL | Weekly use, nearest. |
| H3 | Bridal makeup artists | wedding | HH | I | CITY | Event-specific, reputation. |
| H4 | Spas and massage | wellness | HH | F | CITY | Destination service. |
| H5 | Gyms and fitness | gym, yoga | HH | F | HL | Daily commute limit. |
| H6 | Tailors and boutiques | stitching, bridal | HH | I, F | HL to CITY | Local relationships, fittings. |
| H7 | Dry cleaners and laundry | pickup | HH | F | HL | Route-based. |
| H8 | Dieticians and nutrition | weight, clinical | HH | I | CITY to GLOB | Online consult possible. |

**I. Food, retail and daily needs**

| # | Type | Example sub-types | Customer | Form | Reach | Why |
|---|---|---|---|---|---|---|
| I1 | Bakeries | bread, cakes | HH | F | HL | Founder example; daily, walkable. |
| I2 | Restaurants and cafes | dine-in | HH | F | HL to CITY | Local discovery. |
| I3 | Caterers and cooks | weddings, home cooks | HH, BIZ | F, I | CITY | Event service within a city. |
| I4 | Grocery and supermarkets | kiryana | HH | F | HL | Proximity. |
| I5 | Petrol pumps | fuel, CNG | HH, BIZ | F | HL to CITY | Founder example; on-route, brand and fuel availability. |
| I6 | Water and gas delivery | bottled water, LPG | HH | F | HL | Route-based. |
| I7 | Meat and dairy suppliers | fresh | HH | F | HL | Daily freshness. |

**J. Transport, logistics and travel**

| # | Type | Example sub-types | Customer | Form | Reach | Why |
|---|---|---|---|---|---|---|
| J1 | Movers and packers | house shifting | HH, BIZ | F | CITY to NAT | Inter-city moves. |
| J2 | Courier and logistics | parcels, freight | BIZ, HH | F | NAT to GLOB | Network services. |
| J3 | Taxi and ride services | cabs, rent-a-car | HH | F, I | CITY | Operating zone. |
| J4 | Truck and goods transporters | freight | BIZ | F | NAT | Routes between cities. |
| J5 | Travel agents and tour operators | umrah, tours | HH | F | NAT to GLOB | Cross-border, trust. |
| J6 | Customs clearing agents | import, export | BIZ | F | NAT | Port-based. |

**K. Events and creative services**

| # | Type | Example sub-types | Customer | Form | Reach | Why |
|---|---|---|---|---|---|---|
| K1 | Wedding halls and marquees | venues | HH | F | CITY | Capacity and location. |
| K2 | Photographers and videographers | wedding, commercial | HH, BIZ | I, F | CITY to REG | Travel for events. |
| K3 | Event planners and decorators | weddings | HH, BIZ | F | CITY | Local vendors. |
| K4 | Printing and signage | flex, cards | BIZ, HH | F | CITY | Turnaround. |

**L. Public, community and civic**

| # | Type | Example sub-types | Customer | Form | Reach | Why |
|---|---|---|---|---|---|---|
| L1 | Mosques and prayer services | imams, nikah | HH | F, I | HL | Congregational proximity. |
| L2 | NGOs and charities | zakat, welfare | HH | F | CITY to NAT | Cause-based. |
| L3 | Police and emergency services | stations, rescue | HH | F | CITY | Jurisdiction. |
| L4 | Government service offices | NADRA, utilities | HH, BIZ | F | CITY to NAT | Jurisdictional. |

**M. Agriculture and rural**

| # | Type | Example sub-types | Customer | Form | Reach | Why |
|---|---|---|---|---|---|---|
| M1 | Agri inputs and seed dealers | fertiliser | BIZ | F | REG | District-level supply. |
| M2 | Tractor and farm machinery repair | mechanics | BIZ | I, F | REG | Rural radius. |
| M3 | Agronomists and advisers | crop advice | BIZ | I | REG to NAT | Local conditions. |

**N. Domestic and household help**

| # | Type | Example sub-types | Customer | Form | Reach | Why |
|---|---|---|---|---|---|---|
| N1 | Maids and cleaners | home cleaning | HH | I, F | HL | Trust and local. |
| N2 | Drivers and chauffeurs | personal driver | HH | I | HL to CITY | Local hire. |
| N3 | Gardeners | lawn, plants | HH | I | HL | Society-level. |
| N4 | Security guards and agencies | guards | HH, BIZ | F | CITY | Local deployment. |
| N5 | Nannies and elder care | home care | HH | I | HL to CITY | Trust, on-site. |

**O. Specialised business services**

| # | Type | Example sub-types | Customer | Form | Reach | Why |
|---|---|---|---|---|---|---|
| O1 | Engineering consultants (specialised) | oil and gas, power | BIZ | F | NAT to GLOB | Project-based. |
| O2 | Testing and certification labs | ISO, material testing | BIZ | F | NAT | Accreditation-based. |
| O3 | Industrial suppliers and fabricators | machinery | BIZ | F | NAT | Supply chain. |
| O4 | Waste and recycling services | scrap, collection | HH, BIZ | F | CITY | Collection routes. |

That is 14 + 10 + 9 + 17 + 11 + 13 + 9 + 8 + 7 + 6 + 4 + 4 + 3 + 5 + 4 = 124 listed rows, comfortably above the 80-type minimum. (Counts are the author's own tallies of the rows above.)

**Founder examples mapped to indicative classification codes (UNVERIFIED, from background knowledge; verify against official structures):**

| Founder example | Indicative ISIC Rev. 4 | Indicative ISCO-08 | Note |
|---|---|---|---|
| Plumbers | 4322 | 7126 | Rev. 4 class covers plumbing, heat and AC installation |
| Electricians | 4321 | 7411 | |
| Mobile phone repair | 9512 | 7422 | Repair of communication equipment |
| Quran tutors | 8549 / 8559 | 2359 | Informal religious education fits "other teaching" |
| Beauty parlours | 9602 | 5142 | Hairdressing and other beauty treatment |
| Bakeries | 1071 | 7512 | Manufacture of bakery products (retail sale also under 47xx) |
| Petrol pumps | 4730 | 5223 | Retail sale of automotive fuel |
| Eye doctors / eye hospitals | 8620 / 8610 | 2212 | Medical practice vs hospital activities |
| MRI and diagnostic centres | 8690 | 3212 | Other human health activities |
| Schools | 8510 / 8521 | 2341 / 2330 | Primary / secondary education |
| Contractors | 4100 / 4290 / 4390 | 1323 | Construction classes; managers |
| Data scientists | 6201 / 6311 | 2120 / 2511 | No dedicated ISCO-08 unit group |

### Gaps
- The inventory is a design proposal, not validated demand data. No dataset of actual listing volumes per type (for example Google Maps counts in Karachi, Lahore or Islamabad) was gathered.
- Reach assignments are not backed by category-specific distance studies, apart from the general primary versus specialist healthcare pattern.
- Classification crosswalk codes in the last table were not verified against UNSD or ILO pages.
- Sub-types should be expanded in local languages (Urdu, Arabic, Punjabi, Hindi) with native speakers.

---

## Source limits and verification summary

- Blocked sites during this research (egress proxy): unstats.un.org, docs.overturemaps.org, isco.ilo.org, census.gov, schema.org, wiki.openstreetmap.org. All claims attributed to these sites come from search-result summaries and should be re-verified.
- Figures from secondary or aggregator sites (classification.codes, JobsPipe, SetIndiaBiz, Lightcast, seolocal.it.com, community forums) are flagged inline.
- Unverified background-knowledge items: NAICS/Eurostat/UN licence wording, Wikidata CC0, schema.org CC BY-SA 3.0, specific ISIC/ISCO codes, OSM tag counts.
- Conflicts noted: Urban Company city counts (59 versus 51) and category counts (150+ versus 50+); Sulekha categories (800+ versus about 1,200); GBP category counts (4,046 in May 2026 versus 4,098 in October 2024); UNSPSC item count (158,448) is suspect.
