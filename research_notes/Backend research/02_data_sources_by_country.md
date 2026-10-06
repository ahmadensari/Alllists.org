# Data sources by country: lawful, high-value sources for agents and importers (20 launch countries)

Prepared 2026-10-06 for the AllLists.org founder. Planning research, not legal advice. Companion file: `02_sources.csv` (one row per source, 186 rows, same ratings).

## 1. What this is and how far to trust it

Decisions D14 to D21 say agents draft entries from many sources (D14), open baseline data is licensed in as the starting layer (D16), every record keeps its source, licence, date and consent status (D17), and service providers are identified from established sources first: registers, licensing bodies, chambers, open data (D21). D15 is still open: Google Maps, Facebook and Baidu scraping are in the do-not-use tier pending counsel, and Q-S3 asks for written terms from each register. This file is the per-source permission table those decisions call for.

**Method.** WebSearch (standard mode) only. One attempt to open a Federal Register page was blocked by the egress proxy, so no official page was opened. Every fact comes from a search-result summary, from the earlier research in `reports/Service provider sources.md` and `research_notes/Service provider sources/`, or from background knowledge. Licence text in particular was almost never read at source.

| Tag | Meaning |
|---|---|
| [S] | Seen in a search-result summary during this task |
| [R] | Carried over from earlier repo reports, which are themselves snippet-based |
| [BG] | Background knowledge, not seen in any search result this session. Re-check before use |
| [I] | Inference by this file |
| UNVERIFIED | The source's own terms of use were not read. Treat as amber until someone reads them |

Counts, dates and licence names are as reported in snippets. Dates are often missing.

## 2. The red, amber, green rule used here

This follows `backend/intake/gate.py` and `docs/MASTER_DOCUMENT.md` section 7.1. The gate blocks `red` outright, requires `allowed_uses` to include the use (`import`, `agent_fetch`, `display`), and for amber sources requires a recorded terms review (`reviewed_on`) before import. Green sources need no review in the code.

| Rating | Rule applied in this file | What an agent may do |
|---|---|---|
| GREEN | An explicit open licence that allows commercial reuse (seen in a snippet, or a standard licence I am confident of, tagged [BG]), and the data is about organisations or places, or personal fields can be dropped mechanically | Bulk import and agent fetch; store licence text and attribution; show in the provenance block |
| AMBER | Public data whose terms were not read, or lookup-only registers, or share-alike or paid licences, or any register of named individuals | Import only after a human reads the terms and records `reviewed_on`. Individual-level registers (doctors, lawyers, engineers, sole traders) are used to verify a person someone else nominated, not to import a list |
| RED | Terms or law forbid it, account or captcha or OTP gated, bought or resold lists, or the licence bars sale of the data | Never ingested (R22) |

Three consequences of the code and this rule that the founder may want to decide:

1. **Green skips the terms review in code.** Several greens here rest on [BG] licence knowledge. Suggest that every source, green included, must carry `licence_text` and `reviewed_on` before first import (a change to `assert_allowed`, not made here).
2. **OpenStreetMap, OpenCorporates and Healthsites are ODbL (share-alike).** If their records are merged into AllLists entries and AllLists offers a derived database, that database must be offered under the ODbL. This collides with the USD 1,000 paid download and the no-download rule. Keep ODbL data as a separate layer used for matching and verification, or take the legal advice first. Overture places (CDLA-Permissive-2.0) and Foursquare (Apache-2.0) carry no such duty.
3. **Account-gated registers are red for agents even when the data is public after sign-up** (Turkey MERSIS, Sri Lanka eROC). A human may verify one record; an agent may not hold the login.

## 3. Result at a glance

Across 186 sources: **34 green, 132 amber, 20 red**. Global open datasets: 8 green, 11 amber. Per country (green / amber / red):

| Country | Green | Amber | Red | Start here |
|---|---|---|---|---|
| Pakistan | 0 | 14 | 0 | PHC, PEIRA, HEC, DRAP and PNRA lists for institutions; SECP lists by paid request; chambers with permission; people verify-only |
| India | 1 | 6 | 0 | data.gov.in (GODL-India), UDISE+ and AISHE for institutions; NMC verify-only |
| Bangladesh | 1 | 5 | 0 | data.gov.bd, RJSC lookups, DGHS registry if public; BGMEA/BKMEA with permission |
| UAE | 1 | 6 | 0 | Bayanat (CC BY 4.0), Dubai Pulse, Dubai Municipality contractor data |
| Saudi Arabia | 4 | 4 | 0 | Saudi Open Data Platform (ODC attribution), Balady; per-record Ministry of Commerce query |
| Egypt | 0 | 6 | 0 | Thin: Overture, Foursquare and OSM baseline plus the Ministry of Health centres list and chambers |
| Turkey | 0 | 5 | 1 | Health ministry open data (check contents), HDX Healthsites, YOK, TOBB chamber lookups |
| Nigeria | 0 | 8 | 0 | CAC search, NAFDAC Greenbook; COREN and CORBON as badges |
| Kenya | 0 | 8 | 0 | KMPDC 2026 licensed facility list; NCA and EBK with active-licence filter |
| South Africa | 0 | 7 | 1 | DBE school master list, cidb contractors; CIPC only by licensed API |
| Indonesia | 0 | 7 | 0 | Satu Data Indonesia, SATUSEHAT (if public), Dapodik school profiles, AHU |
| Vietnam | 0 | 5 | 0 | National Data Portal and business registration portal (no API) |
| Brazil | 0 | 8 | 0 | CNPJ monthly files and CNES establishments (read terms first) |
| Mexico | 2 | 4 | 0 | INEGI DENUE (5-6M establishments, free-use terms), datos.gob.mx |
| United Kingdom | 4 | 4 | 0 | Companies House, CQC, FSA ratings, charities, GIAS |
| United States | 5 | 4 | 0 | NPPES organisations, FDA, SEC, IRS TEOS, NCES |
| Germany | 2 | 6 | 0 | GovData and Destatis (Datenlizenz Deutschland); Handwerkskammer lookups |
| France | 4 | 2 | 0 | SIRENE, FINESS, Annuaire de l'education (Licence Ouverte) |
| Philippines | 2 | 6 | 0 | data.gov.ph, PSA OpenSTAT; NHFR, CHED, DepEd for institutions |
| Sri Lanka | 0 | 6 | 1 | Open data portal, UGC list, Ceylon Chamber directory with permission |

What the pattern says:

- **Explicit open licences cluster in a few places:** India (GODL-India), France (Licence Ouverte), UK (Open Government Licence), Germany (Datenlizenz Deutschland), Mexico (INEGI free-use terms, Libre Uso MX), UAE (CC BY 4.0 on Bayanat), Saudi Arabia (ODC attribution), the US federal government, and the global layers (Overture, Foursquare, GeoNames, Wikidata, GLEIF, ROR).
- **Most of the rest is amber because the register exists but its terms are unread.** That is a documentation task (Q-S3), not a legal block: email each body for written terms, then flip the row.
- **Registers of named people are verify-only everywhere.** No country gave evidence of an open licence for a bulk list of named doctors, lawyers or engineers. The only person-level bulk files found are France's RPPS extract, the US NPPES individual file and Kenya's published KMPDC practitioner list, and none has verified reuse terms for named people.
- **The informal long tail has no register in any country** (plumbers, electricians, tutors, domestic help). Sources are OSM, owner submissions and society opt-in (D21).
- **Strongest single sources by value:** Mexico DENUE, France SIRENE, UK Companies House with CQC and FSA, India data.gov.in, Brazil CNPJ and CNES (after terms review), Kenya KMPDC (facilities), Overture and Foursquare as the global baseline.

## 4. Global open datasets

These are the starting layer (D16). Use them to build the place tree and the draft set, then enrich from the country registers below. Cross-link records through Wikidata, GLEIF and ROR identifiers where present.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [Overture Maps - places theme](https://docs.overturemaps.org/attribution) | Local businesses, schools, hospitals, religious sites, landmarks (any list type with a physical place) | CDLA-Permissive-2.0 for places [S]; per-record licence field is kept (repo rule); attribution required | Parquet on S3/Azure, CLI, DuckDB; bulk by region | Monthly-ish releases (2026-01-21 to 2026-08-19 seen) [S] | Low-medium: business names, phones, websites; some sole-trader names; confidence score 0-1 per place [S] | **GREEN** |
| [Overture Maps - addresses, divisions, base, buildings themes](https://docs.overturemaps.org/attribution) | Address points, admin areas, land use, buildings (place tree and geocoding) | Mixed per record: some inputs are OSM (ODbL, share-alike) [BG]; read the per-feature licence | Same as places | Monthly-ish | Low (addresses are not tied to people in the file) | **AMBER** |
| [Foursquare Open Source Places (FSQ OS Places)](https://docs.foursquare.com/data-products/docs/fsq-places-open-source) | 100M+ POIs worldwide; 22 core attributes (name, address, geo, website, category, social handles) [S] | Apache-2.0, commercial use allowed [S] | Parquet on S3, Hugging Face, Snowflake; bulk | Monthly [S] | Low-medium: social handles and some sole-trader names | **GREEN** |
| [GeoNames](https://www.geonames.org/export/) | Place names, admin hierarchy, postal codes, coordinates (the place tree, not businesses) | CC BY 4.0, credit with a link [S] | allCountries.zip and per-country dumps at download.geonames.org/export/dump/ | Daily dump [S] | None | **GREEN** |
| [OpenStreetMap (planet, Geofabrik country extracts)](https://osmfoundation.org/wiki/Licence_and_Legal_FAQ) | POIs (shops, clinics, schools, workshops), roads, admin areas; best for the informal long tail in South Asia and Africa [I] | ODbL 1.0: attribution plus share-alike for any adapted database [S] | Geofabrik daily extracts [S], planet file, Overpass API (rate limited) | Minute-level planet; Geofabrik daily | Low-medium: some mappers add personal phone numbers | **AMBER** |
| [Wikidata](https://dumps.wikimedia.org/wikidatawiki/entities/) | Organisations, universities, hospitals, companies, places with identifiers (cross-walk key between sources) | CC0 for structured data [S] | Weekly JSON dump at dumps.wikimedia.org/wikidatawiki/entities/ [S]; SPARQL; API | Weekly dump; live edits | Low for organisations; HIGH for person items (filter them out) | **GREEN** |
| [Wikipedia and Wikimedia Commons text and images](https://dumps.wikimedia.org/legal.html) | Descriptions of institutions, universities, hospitals | Text CC BY-SA 4.0 (share-alike) [BG]; images vary per file | Dumps, API | Twice-monthly dumps [BG] | Low-medium (biographies of living people) | **AMBER** |
| [GLEIF Golden Copy (LEI)](https://www.gleif.org/en/lei-data/gleif-golden-copy/download-the-golden-copy) | Legal entities with an LEI (large firms, banks, funds, exporters); parent-child links | CC0 [BG]; snippet confirms free daily files but does not show the licence | Golden Copy and delta files download (daily; 8-hour, 24-hour, 7-day, 31-day deltas) [S] | Daily [S] | Low | **GREEN** |
| [ROR (Research Organization Registry)](https://ror.org/) | Universities, research institutes, hospitals-as-research-orgs (113,528 records in v1.60 [S]) | CC0 [S] | Zenodo data dump (JSON and CSV), REST API | Versioned releases several times a year [S] | None | **GREEN** |
| [OpenAlex (institutions table)](https://openalex.org/) | Institutions (universities, hospitals, companies in research); works and authors exist but are person data | CC0 snapshot on public AWS bucket [R]; since 13 Feb 2026 the API needs a free key and has usage pricing [R, UNVERIFIED] | S3 snapshot; API | Roughly monthly snapshot [BG] | Low for institutions; HIGH for authors (do not import) | **GREEN** |
| [ORCID public data file](https://info.orcid.org/documentation/integration-guide/working-with-bulk-data/) | Researchers who chose public visibility (use only after a person registers and signs in) [R] | CC0 file; ORCID asks that emails are not used for bulk mail and that opt-out is offered [R] | Annual public data file; public API | Annual | HIGH: named individuals | **AMBER** |
| [OpenCorporates](https://opencorporates.com/terms-of-use-2/) | Company registry records from 140+ jurisdictions (cross-check and gap filling) | ODbL share-alike for the open tier; commercial users need a paid licence [S] | API key required; free for open-data projects under same licence [S] | Varies by registry | Low-medium (officers are named) | **AMBER** |
| [Healthsites.io (Global Healthsites Mapping Project)](https://wiki.openstreetmap.org/wiki/Global_Healthsites_Mapping_Project) | Health facilities worldwide (OSM-derived), including Turkey and Pakistan sets on HDX/opendata.com.pk [R] | ODbL [S] | API, GeoJSON, Shapefile, KML, CSV [S] | Continuous from OSM; snapshots vary | Low | **AMBER** |
| [Humanitarian Data Exchange (HDX)](https://data.humdata.org/faqs/licenses) | Health sites, admin boundaries, schools, populated places for many countries | Licence is chosen by each data owner (CC licences and others); read it per dataset [S] | CKAN downloads and API | Per dataset | Low-medium per dataset | **AMBER** |
| [OpenAddresses](https://openaddresses.io/) | Address points by country from government sources | Per-source licence, mixed [BG] | Bulk downloads by source | Per source | Low | **AMBER** |
| [AllThePlaces (open spiders of chain store locators)](https://alltheplaces.xyz/) | Chain and franchise outlets (a source inside Overture: 1.75M features in the April 2026 release [S]) | Output published openly [BG]; the underlying websites are scraped, so check per brand | GitHub project, daily outputs | Daily | Low | **AMBER** |
| [Web Data Commons (schema.org markup extracted from Common Crawl)](https://webdatacommons.org/structureddata/) | LocalBusiness, Organization, Place markup from business websites | Facts are extracted from third-party pages; rights stay with each site owner; Common Crawl terms not read [BG, UNVERIFIED] | Yearly dumps | Yearly | Medium: contact details of sole traders | **AMBER** |
| Owner and contributor submissions with consent (claim flow, housing-society opt-in, officer-pasted lists with declared rights D11) (`docs/MASTER_DOCUMENT.md#71`) | Any list type; the only route for informal trades (plumbers, tutors, domestic help) | Contributor grants the licence and declares the right to share (D11); consent status stored (D17) [R] | Web form, CSV paste, claim by OTP | On submission; re-confirm every 90 days [R, I] | Medium: consent and removal route required | **GREEN** |
| [A business's own website, read by an agent that respects robots.txt and terms (agent_fetch, one record at a time)](https://developers.google.com/search/docs/crawling-indexing/robots/intro) | Fills gaps: website, phone, hours, category for a business already in the draft set | Site terms apply; robots.txt must allow; repo default is amber [R] | backend/agents fetcher (no redirects, public IPs only, size cap) | Per job | Medium: staff names and personal mobiles on the page | **AMBER** |

**How to combine them [I].** Place tree from GeoNames and Overture divisions. Draft businesses from Overture places and Foursquare (dedupe by name, address, coordinates; use the Overture confidence score). Institutions (universities, research bodies, hospitals) cross-linked through ROR, Wikidata and OpenAlex. Large firms through GLEIF. OSM fills informal trades and shops where nothing else exists, kept as its own ODbL layer. Everything else enters through the country sources, owner claims or consented submissions.

## 5. Country sections

Each table lists the source, the list types it covers, licence and terms, how to get it in bulk (or why not), update rhythm, personal-data risk, and the gate rating. Source names link to the page where one was seen or is well known; entries with a repo path in backticks are internal.

### Pakistan

**Privacy law.** No enacted comprehensive data protection law as of May 2026; the Personal Data Protection Bill 2025 is a draft; PECA 2016 applies [R]. Collect consent and offer removal from day one anyway.

**Start with.** Facilities and institutions first: PHC licence numbers, PEIRA and HEC lists for schools and universities, DRAP and PNRA lists as verification layers, SECP company lists by paid request, TDAP and chamber lists with written permission. Individuals (PMDC, bar, ICAP) are verify-only. Plumbers, electricians, tutors and domestic help have no register, so use society opt-in (D21).

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [PMDC online register](https://pmdc.pk/) | Doctors, dentists (366,443 reported, undated [R, UNVERIFIED]); lookup shows licence validity and qualifications | Terms not found; UNVERIFIED | One-record search by registration no., name or father's name; no export found [R] | Live (renewals); unknown | HIGH: named individuals, father's name | **AMBER** |
| [Punjab Healthcare Commission (HCE portal, licence verify)](https://os.phc.org.pk/verify.aspx) | Hospitals, clinics, labs, diagnostic centres: 64,000+ registered, 41,000+ licensed [R, undated] | Terms not found; UNVERIFIED | Verify by licence number; browse/list view unconfirmed [R] | Live; unknown | Low (facilities); owner names may appear | **AMBER** |
| [KP HCC, Sindh HCC, IHRA (Islamabad), Balochistan HCC](https://ihra.gov.pk/) | Private health facilities by province (KP 23,041 registered; Sindh about 14,000 of an estimated 100,000 [R, undated]) | Terms not found; UNVERIFIED | No public searchable list found [R]; cross-check only | Unknown | Low | **AMBER** |
| [DRAP (lists of pharmaceutical units, Registered Drugs Index)](https://www.dra.gov.pk/) | Drug manufacturers (about 1,380), importers and distributors (about 2,500) [R]; retail pharmacies are provincial and have no national list [R] | Terms not found; UNVERIFIED | Web lists and PDFs on dra.gov.pk | Unknown | Low | **AMBER** |
| [PNRA licensed radiation facility lists](https://pnra.org/r-safety.html) | X-ray, CT, medical radiation, nuclear medicine facilities (MRI is not radiation-licensed, so MRI centres are not covered [I]) | Terms not found; UNVERIFIED | Links to PDF/web lists on pnra.org/r-safety.html [R] | Unknown | Low | **AMBER** |
| [opendata.com.pk (Pakistan Health Sites, Pakistan Health Facilities, PBS public health facilities 2021)](https://opendata.com.pk/dataset/pakistan-health-sites) | Mostly government health facilities with type and coordinates | Licence per dataset; Health Sites is OSM/Healthsites-derived (ODbL) [R] | CSV and ZIP download [R] | Static snapshots (2021 and earlier) | Low | **AMBER** |
| [PEIRA registered private educational institutions (Islamabad)](https://psms.peira.gov.pk/admin/rpt_registered_peis.php) | Private schools and colleges registered or renewed under the 2024 Rules [S] | Terms not found; UNVERIFIED | Public paginated report psms.peira.gov.pk (rpt_registered_peis.php) [S] | Rolling with renewals | Low | **AMBER** |
| [HEC recognised universities and campuses](https://www.hec.gov.pk/english/universities/Pages/DAIs/HEC-recognized-Campuses.aspx) | 179 degree-awarding institutions (older figure) [S]; campuses | Terms not found; UNVERIFIED | Web list by province and sector on hec.gov.pk | Updated at HEC discretion | Low | **AMBER** |
| [SECP company register (eServices)](https://eservices.secp.gov.pk/) | Companies: CUIN, name, kind, incorporation date, registered office, status [S] | Not an open licence; basic search free, certified extracts PKR 200-3,000; list supply is a paid service (PKR 2 per data field, minimum PKR 500) [S] | Per-company search; lists by paid request to SECP | Live | Low-medium: directors in extracts | **AMBER** |
| [Pakistan Engineering Council (PEC) constructor and consultant register](https://www.pec.org.pk/) | Contractors C-A to C-6 (cost-capacity categories) and consulting engineers [R] | Terms not found; public online search unconfirmed [R, UNVERIFIED] | Unknown | Unknown | Medium: individual engineers and sole proprietors | **AMBER** |
| [PPRA / EPADS tender award notices](https://www.ppra.org.pk/) | Firms that won public contracts (contractors, suppliers) with value and date | Public notices; reuse terms not found; UNVERIFIED. The supplier register itself is probably login-gated [R] | Web and PDF notices; the 51,000-supplier register is not confirmed public [R] | Continuous | Low-medium | **AMBER** |
| [TDAP Pakistan Exporters Directory](https://www.pakistanexportersdirectory.gov.pk/) | Exporters by HS code, product category, size band (large, medium, small) [S] | Terms not found; repo default is amber [R] | Web search at pakistanexportersdirectory.gov.pk; launched 2017 [S]; current status unverified | Unknown | Medium: contact people | **AMBER** |
| [Chambers and associations: FPCCI (general body, executive committee, bilateral business councils), KCCI (18,000+ members [S]), LCCI, RCCI, ABAD, OSP branches](https://fpcci.org.pk/) | Manufacturers, traders, builders, eye specialists (with permission) | Member lists are the chamber's property; repo default is amber [R]; seek written permission | PDF lists (FPCCI posts them [S]), member pages, officer-supplied CSV under D11 | Annual | Medium-high: proprietors' mobiles | **AMBER** |
| [ICAP and ICMAP member directories; Pakistan Bar Council and provincial bar rolls](https://icap.org.pk/) | Accountants, advocates (verification of nominated individuals) | Terms not found; UNVERIFIED | Member directory lookups; some PDF rolls | Unknown | HIGH: named individuals | **AMBER** |

**Gaps.** Terms of use for every portal above are unread (Q-S3). PEC public search, PEIRA terms, KP/Sindh/Balochistan lists and data.gov.pk licence were not confirmed.

### India

**Privacy law.** Digital Personal Data Protection Act 2023, with rules phasing in [BG, UNVERIFIED]. Business data is lower risk than named doctors or proprietors.

**Start with.** data.gov.in under GODL-India is the cleanest bulk source in the whole 20-country set for government facility and school data. Use UDISE+ and AISHE for institutions. NMC and the GST/Udyam/FSSAI tools verify nominated records only.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [Open Government Data Platform India (data.gov.in)](https://data.gov.in/) | 230,000+ datasets as of July 2026 [S]: facilities, schools, hospitals, industrial units, tourism, ministry registers | GODL-India: commercial and non-commercial use, adaptation and derivative works for shareable non-sensitive data [S]; check each dataset's own terms | Portal downloads and API with free key [S] | Per dataset (many are annual) | Low (non-sensitive data only) | **GREEN** |
| [UDISE+ (school directory and dashboards)](https://udiseplus.gov.in/) | Government and private schools, 14.72 lakh [S]; school-level facilities | A copy is on OGD (so GODL-India applies to that copy) [S]; udiseplus.gov.in own terms not read | Dashboards, reports, APIs for researchers [S]; OGD downloads | Annual | Low at school level (teacher and student level is restricted) | **AMBER** |
| [AISHE (higher education institutions) and AICTE approved institutions](https://aishe.gov.in/) | Universities, colleges, technical institutions | Terms not read; UNVERIFIED [BG for AICTE dashboard] | Annual survey reports, web lists, dashboards | Annual | Low | **AMBER** |
| [NMC Indian Medical Register (IMR) and new National Medical Register](https://nmc.org.in/information-desk/indian-medical-register) | Doctors: 1.4M+; number, council, qualification, university, address, year [R] | Terms not found; UNVERIFIED. Apify scrapers exist but that is not permission [R] | Public search; no bulk found; data current to about 2021 with gaps (Karnataka, Arunachal, Delhi) [R] | Stale (2021) until NMR is complete | HIGH: named individuals with addresses | **AMBER** |
| [MCA company master data (View Company/LLP Master Data)](https://www.mca.gov.in/) | Companies and LLPs: CIN, name, address, status, class, dates | Terms not read; bulk is sold through paid APIs and resellers [S]; whether any MCA data is on OGD under GODL is not confirmed [R] | Per-company lookup with export to Excel [S] | Live | Low-medium (directors) | **AMBER** |
| [Per-record verifiers: GST taxpayer search, Udyam (MSME) verify, FSSAI licence check](https://services.gst.gov.in/services/searchtp) | Verification of a nominated business by GSTIN, Udyam number or FSSAI number [S] | Lookup tools; captcha gated (GST, Udyam) [S]; automated bypass would be red | One record at a time by number or PAN [S] | Live | Medium: sole proprietors; PAN-linked | **AMBER** |
| [Export promotion councils and chambers (FIEO, EEPC, CII, FICCI, state chambers)](https://www.fieo.org/) | Exporters, manufacturers by sector | Member directories belong to each body; terms not read [BG, UNVERIFIED] | Web directories; ask for CSV under D11 | Annual | Medium-high | **AMBER** |

**Gaps.** MCA reuse terms, AISHE and AICTE terms, and which health or industrial datasets sit on OGD are unconfirmed. NMC data is stale (2021).

### Bangladesh

**Privacy law.** No settled comprehensive data protection statute was verified; a personal data protection ordinance was reported in 2025 [BG, UNVERIFIED]. Counsel to confirm.

**Start with.** data.gov.bd for open datasets, RJSC for company lookups, DGHS registry for facilities if public. BMDC is verify-only. Garment exporters (BGMEA, BKMEA) are the high-value B2B list but need member-body permission.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [data.gov.bd national open data portal](https://data.gov.bd/) | Datasets from 35+ ministries and agencies (health, education, local government) | In general the Open Government Licence (commercial use allowed) [S]; confirm per dataset | Portal downloads | Per dataset | Low | **GREEN** |
| [RJSC (Registrar of Joint Stock Companies and Firms), e-service](https://app.roc.gov.bd/psp/nc_search) | Companies, firms, societies, trade organisations | Terms not found; UNVERIFIED. Name search free; extracts BDT 200-2,000 [S] | Per-record search; no public API [BG] | Live | Low-medium | **AMBER** |
| [BMDC verification portal](https://verify.bmdc.org.bd/) | Physicians (134,568), dentists (14,323), medical assistants (2,918), undated [R]; about 36,000 practise without renewal [R] | Terms not found; UNVERIFIED | verify.bmdc.org.bd lookup | Live | HIGH: named individuals | **AMBER** |
| [DGHS Facility Registry (Shared Health Record) and Hospitals and Clinics Branch](https://info.shr.dghs.gov.bd/) | Government and private hospitals, clinics, diagnostic centres, blood banks [S] | Terms not found; public access unconfirmed [S, UNVERIFIED] | Registry inside SHR; public export unknown | Unknown | Low | **AMBER** |
| [BPERB licensed engineers database; IEB](https://en.wikipedia.org/wiki/Professional_Engineers_of_Bangladesh) | Licensed engineers | Terms not found; public search unconfirmed [R, UNVERIFIED] | Unknown | Unknown | Medium-high | **AMBER** |
| [BGMEA, BKMEA, FBCCI, DCCI, MCCI, CCCI member directories](https://www.bgmea.com.bd/) | Garment and knitwear manufacturers and exporters, traders | Member directories belong to each body [BG, UNVERIFIED] | Web directories; ask for CSV under D11 | Annual | Medium | **AMBER** |

**Gaps.** BMDC fields and whether the 134,568 figure is current, DGHS registry export, BPERB access. Forged skill certificates are documented (Feb 2026), so any certificate number is a claim until checked [R].

### UAE

**Privacy law.** Federal Decree-Law 45/2021 (PDPL); DIFC and ADGM have their own regimes [BG].

**Start with.** Bayanat (CC BY 4.0) and Dubai Pulse give the only explicit open terms. Dubai Municipality's contractor and consultant data is the strongest contractor lead. Doctor lookups are verify-only.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [Bayanat (national open data portal)](https://bayanat.ae/) | Federal and emirate datasets (health, education, economy) | CC BY 4.0 [S] | Portal downloads and API | Per dataset | Low | **GREEN** |
| [Dubai Pulse / Dubai Data](https://www.dubaipulse.gov.ae/) | 420+ open and shared datasets from 35 entities (e.g. municipality, KHDA schools, DHA) [S] | Open datasets vs shared datasets; terms of use per dataset [S] | Portal downloads and API; shared sets need an agreement | Per dataset | Low-medium | **AMBER** |
| [Dubai Municipality: Consultants, Contractors and Suppliers Data](https://www.dm.gov.ae/municipality-business/consultants-contractors-and-suppliers-data/) | Registered engineering consultancies and contracting companies [R] | Terms not found; format unverified [R, UNVERIFIED]; a 2025 law makes DM keep a unified contractor register [R] | Published on dm.gov.ae (format unknown) | Unknown | Low | **AMBER** |
| [Dubai DET (ex-DED) licence search; Abu Dhabi ADDED/TAMM licence finder](https://dubaidet.gov.ae/) | Mainland licensed businesses with activity code (3,000+ activities) [S] | Terms not found; UNVERIFIED | Per-record lookups; no bulk found; TAMM is login-based for most services [S] | Live | Low-medium | **AMBER** |
| [DHA Sheryan, DOH Abu Dhabi, MOHAP professional and facility lookups](https://sheryan.dha.gov.ae/) | Doctors, nurses, dentists, pharmacists, facilities | Terms not found; UNVERIFIED. No bulk or public DOH/MOHAP register found [R] | Lookup by ID; mirrors like zavis.ai are third-party and not official [R] | Live | HIGH for professionals; low for facilities | **AMBER** |
| [KHDA private school directory and inspection ratings (Dubai)](https://web.khda.gov.ae/) | Private schools, curriculum, fees, ratings | Terms not read [BG, UNVERIFIED]; some KHDA data is on Dubai Pulse [S] | Web pages; Dubai Pulse datasets | Annual | Low | **AMBER** |
| [Chambers (Dubai Chambers, Abu Dhabi Chamber, Sharjah CCI) and free zone public registers (DMCC, JAFZA, DIFC)](https://www.dubaichamber.com/) | Member companies by sector; free-zone licensees | Terms not read [BG, UNVERIFIED] | Web directories and public register pages | Live | Low-medium | **AMBER** |

**Gaps.** Whether DET, DOH or MOHAP expose any facility directory; DM data format; KHDA terms.

### Saudi Arabia

**Privacy law.** Personal Data Protection Law, in force 2023 with enforcement from September 2024 [BG].

**Start with.** Saudi Open Data Platform (ODC attribution licence) and Balady, with Monsha'at and Council of Engineers statistics for sizing. The Ministry of Commerce query is per-record.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [Saudi Open Data Platform (open.data.gov.sa)](https://open.data.gov.sa/) | Datasets from MoH (hospital indicators by region, mental health, rehab), Balady, Ministry of Commerce, Monsha'at [S] | Open Data Commons Attribution Licence [S] | Portal downloads and API | Per dataset | Low | **GREEN** |
| [Balady (municipal) open data](https://www.balady.gov.sa/en/open-data) | Municipal licensing and commercial outlets (contents unverified) | Creative Commons per portal statement [S]; actual datasets UNVERIFIED | Portal downloads | Per dataset | Low | **GREEN** |
| [Ministry of Commerce commercial register query](https://mc.gov.sa/en/OpenData) | Registered establishments by name or unified national number | Free public query, no login [S]; reuse terms UNVERIFIED | Per-record; open data page at mc.gov.sa/en/OpenData [S] | Live | Medium: sole traders | **AMBER** |
| [Monsha'at open data](https://monshaat.gov.sa/en/node/12825) | Counts of SMEs by size, activity, region (2019-2022) [S]; market sizing, not a list | Open data licence [S] | Portal downloads | Annual | None | **GREEN** |
| [SCFHS practitioner verification (Mumaris)](https://scfhs.org.sa/en/node/1992) | Doctors and health practitioners | Terms not read; lookup needs national ID, Iqama, passport or file number [R] | Verify one person with the person's own identifier; not browsable [R] | Live | HIGH: needs national identifiers (never store) | **AMBER** |
| [Saudi Contractors Authority (Muqawil) classification](https://muqawil.org/en/contractor-classification/info) | About 142,000 contractors (undated) [R]; classification by field and grade | Terms not read; public search unconfirmed [R, UNVERIFIED] | Muqawil platform | Unknown | Low-medium | **AMBER** |
| [Saudi Council of Engineers open data](https://saudieng.sa/English/HelpandSupport/OpenData/Pages/OpenDataPolicy.aspx) | Six statistics datasets (engineer counts); accreditation e-services [S] | Open data policy page [S]; downloads in several formats | Portal downloads | Unknown | Low (statistics) | **GREEN** |
| [Council of Saudi Chambers and 28 regional chambers (Riyadh, Jeddah, Eastern Province and others)](https://www.saudichambers.org.sa/) | Member companies by sector with business directory [S] | Directory belongs to each chamber; terms not read [UNVERIFIED] | Web directories | Unknown | Medium | **AMBER** |

**Gaps.** Whether Balady and MoH datasets hold facility-level lists; Muqawil access; SCFHS partnership route.

### Egypt

**Privacy law.** Personal Data Protection Law 151 of 2020 [BG].

**Start with.** Thin. Use Overture, Foursquare and OSM for the baseline; the Ministry of Health centres list, chamber directories and the CKAN portal for cross-checks.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [Egypt Open Data Portal (data.gov.eg, CKAN) and CAPMAS](https://data.gov.eg/) | Ministry datasets, statistics, public-health indicators [S] | Open Data Policy sets licensing rules; the licence of individual datasets is UNVERIFIED [S] | CKAN downloads | Per dataset | Low | **AMBER** |
| [GAFI and ITDA commercial register](https://www.gafi.gov.eg/) | Companies (GAFI incorporation) and commercial register (ITDA, Ministry of Supply) [S] | Terms not found; public lookup UNVERIFIED [S] | Investor service centre; no bulk found | Live | Low-medium | **AMBER** |
| [Federation of Egyptian Chambers of Commerce (fedcoc.org.eg) and Federation of Egyptian Industries](http://www.fedcoc.org.eg/) | Traders by governorate chamber; manufacturers | Directories belong to the bodies; terms not read [UNVERIFIED] | Web directories | Unknown | Medium | **AMBER** |
| [Ministry of Health: Secretariat of Specialized Medical Centers](https://en.wikipedia.org/wiki/List_of_hospitals_in_Egypt) | 82 centres and hospitals (47 multi-specialty, 12 single-specialty, 8 day-surgery, 12 oncology) with a map [S] | Terms not read; UNVERIFIED | Public website with interactive map | Unknown | Low | **AMBER** |
| [Egyptian Medical Syndicate (230,000+ members) and GAHAR accredited facilities](https://en.wikipedia.org/wiki/Egyptian_Medical_Syndicate) | Doctors; accredited health facilities | No public searchable register or directory found [R] | Verification would be by request | Unknown | HIGH for doctors | **AMBER** |
| [GOV.UK Egypt: doctors and medical facilities (list for British nationals)](https://www.gov.uk/government/publications/egypt-list-of-medical-facilities-practitioners/egypt-doctors-and-medical-facilities) | A curated, non-comprehensive list of private doctors and hospitals | Published by the UK government; Open Government Licence is likely [BG]; listed individuals did not agree to be in our directory | Web page | Occasional | Medium: named doctors | **AMBER** |

**Gaps.** No official register of doctors, contractors or schools with public access was found. Largest gap among the 20.

### Turkey

**Privacy law.** KVKK (Law 6698); VERBIS registry of data controllers [BG].

**Start with.** Health ministry open data portal (check contents), HDX Healthsites, YOK for universities, per-chamber member lookups through TOBB. MERSIS is account-gated and therefore red.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [TOBB and local chambers of commerce and industry](https://www.tobb.org.tr/Sayfalar/Eng/TicaretOdalari.php) | 1.4M member firms in 365 chambers and exchanges (178 chambers of commerce and industry, 113 commodity exchanges) [S] | Member data belongs to chambers; terms not read [UNVERIFIED] | TOBB lists chambers; each chamber has a member lookup (TicaretOdalari page) [S] | Live | Medium: sole traders | **AMBER** |
| [MERSIS (Ministry of Trade central registry)](https://mersis.gtb.gov.tr/) | Company name, tax number, address, status, representatives | Free only after signing up [S]; account-gated, so red for agents. If a public no-login query is confirmed, re-rate to amber | Query by name, tax number, trade registry or MERSIS number | Live | Medium: representatives named | **RED** |
| [Ministry of Health open data portal (acikveri.saglik.gov.tr) and veri.gov.tr](https://acikveri.saglik.gov.tr/) | Possibly hospitals and clinics with names and addresses (contents unverified) [R] | Licence UNVERIFIED | Portal downloads | Unknown | Low | **AMBER** |
| [Turkey Healthsites (HDX, OSM-derived)](https://data.humdata.org/) | Health facilities | ODbL via Healthsites.io; licence on HDX not checked [R] | HDX download | Snapshot | Low | **AMBER** |
| [YOK (Council of Higher Education) university list and YOK Atlas](https://www.yok.gov.tr/) | About 200+ universities: 129 state, about 75 foundation [S]; programme statistics | Terms not read; UNVERIFIED | Web lists | Annual | Low | **AMBER** |
| [Istanbul Metropolitan Municipality and Izmir open data portals](https://data.ibb.gov.tr/) | City facilities, licensed premises layers (contents unverified) [S] | Per-portal licence UNVERIFIED | Portal downloads and API | Per dataset | Low | **AMBER** |

**Gaps.** Contents and licence of veri.gov.tr and acikveri.saglik.gov.tr; contractor registry (not found); TOBB reuse terms.

### Nigeria

**Privacy law.** Nigeria Data Protection Act 2023 [BG].

**Start with.** CAC search and NAFDAC Greenbook for firms and manufacturers; COREN and CORBON as verification badges; chambers and MAN for manufacturers with permission.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [CAC public search](https://search.cac.gov.ng/) | Registered companies, business names, incorporated trustees | Free public search (replaced the NGN 500 paid search) [R]; reuse terms UNVERIFIED | Per-record search; extracts and certified copies are paid [R] | Live | Medium: proprietors and directors | **AMBER** |
| [NAFDAC Greenbook](https://greenbook.nafdac.gov.ng/) | Registered products (about 9,000: drugs 7,500, devices 1,100, vaccines 150, herbals 130, vet 90) with applicant and manufacturer [S] | Terms not read; UNVERIFIED | Public search at greenbook.nafdac.gov.ng | Live | Low | **AMBER** |
| [MDCN master register](https://mdcn.gov.ng/page/services/primary-source-verification) | Doctors and dentists | No public name search found; verification goes through DataFlow [R] | Request-based | Unknown | HIGH | **AMBER** |
| [PCN (Pharmacists Council) premises registration](https://www.pcn.gov.ng/) | Pharmacies (community, hospital, online) and pharmacists [S] | Public list not found; UNVERIFIED | Annual premises registration via PCN-Core app; public lookup unknown | Annual | Medium | **AMBER** |
| [COREN and CORBON verification portals](https://bumap.corbon.gov.ng/search/) | Engineers and engineering firms (COREN); builders, building firms, technicians and craftsmen (CORBON) [R] | Terms not read; UNVERIFIED | Verify by number, name, licence ID or QR code [R]; no bulk | Live | Medium-high | **AMBER** |
| [NUC accredited universities and JAMB institution lists](https://nuc.edu.ng/) | Universities, polytechnics, colleges of education | Terms not read [BG, UNVERIFIED] | Web lists and PDFs | Annual | Low | **AMBER** |
| [Lagos Chamber (LCCI), Manufacturers Association of Nigeria (MAN), NACCIMA directories](https://lagoschamber.com/) | Manufacturers, traders | Member directories belong to each body [BG, UNVERIFIED] | Web directories; ask for CSV under D11 | Annual | Medium | **AMBER** |
| [GOV.UK Nigeria: List of Medical Facilities](https://www.gov.uk/government/publications/nigeria-list-of-medical-facilitiespractitioners/nigeria-list-of-medical-facilities) | Curated list of hospitals and clinics for British nationals | Published by the UK government; licence likely OGL [BG]; non-comprehensive [R] | Web page | Occasional | Low-medium | **AMBER** |

**Gaps.** MDCN public search, PCN premises list, NHIA accredited facilities (no central list found), any open data portal licence.

### Kenya

**Privacy law.** Data Protection Act 2019; data controllers register with the ODPC [BG].

**Start with.** Best African source of facilities: KMPDC publishes a 2026 licensed list. NCA and EBK for contractors and engineers, with an active-licence filter. BRS is paid per record.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [KMPDC registers: health facilities and ambulances](https://registers.kmpdc.go.ke/) | All licensed facilities (public, private, mission; hospitals, clinics, nursing homes); 2026 list published [S]; 544 facilities shut and 454 licences cancelled in 2025 [S] | Terms not read; UNVERIFIED | Public register portal registers.kmpdc.go.ke; search by facility; downloadable list for 2026 reported [S] | Annual licence cycle; live status | Low | **AMBER** |
| [KMPDC registers: practitioners and specialists](https://registers.kmpdc.go.ke/) | Doctors, dentists, specialists, interns (licensed for current year) | Terms not read; UNVERIFIED | Public search and published 2026 list [S] | Annual | HIGH: named individuals | **AMBER** |
| [NCA contractor register](https://www.nca.go.ke/local-contractors) | Contractors in 8 categories (NCA 1-8); 18,000 registered (undated) and 150,000+ accredited workers [R] | Terms not read; UNVERIFIED. Needs an active-licence filter after the January 2026 de-registration warning [R] | 'Search Registered Contractors' on nca.go.ke; no bulk found | Annual renewals | Medium: sole proprietors and accredited workers | **AMBER** |
| [Engineers Board of Kenya (EBK) register](https://ebk.or.ke/) | Registered engineers and firms; list published in the Kenya Gazette and on the website [S] | Gazette notices are public documents; reuse terms UNVERIFIED | Gazette PDF and website | Periodic | HIGH: named individuals | **AMBER** |
| [BRS eCitizen business search](https://brs.ecitizen.go.ke/) | Companies, business names, LLPs | Paid per-record (name search KES 150; CR12 KES 650) [S]; not bulk | brs.ecitizen.go.ke | Live | Medium | **AMBER** |
| [Kenya Open Data (opendata.go.ke)](https://www.opendata.go.ke/) | Government datasets (schools, health facilities, counties) | 2013 statement: no restriction on commercial reuse, acknowledge source [S]; current licence and portal status UNVERIFIED | Portal downloads | Stale in places [BG] | Low | **AMBER** |
| [Ministry of Education NEMIS and school lists](https://nemis.education.go.ke/) | 9,112 public secondary and 3,915 private schools captured [S] | No public download confirmed; UNVERIFIED | NEMIS is an internal system; county school lists appear as PDFs | Unknown | Low at school level; HIGH at learner level (never) | **AMBER** |
| [Pharmacy and Poisons Board licensed premises; KNCCI and KAM directories](https://pharmacyboardkenya.org/) | Pharmacies, wholesalers; traders and manufacturers | Terms not read [BG, UNVERIFIED] | Web lists and directories | Annual | Medium | **AMBER** |

**Gaps.** KMPDC and NCA reuse terms; whether NCA offers any export; current status of opendata.go.ke.

### South Africa

**Privacy law.** POPIA, which also protects juristic persons [BG].

**Start with.** DBE school master list, cidb contractors, municipal open data. CIPC needs a licensed API or reseller. Stats SA is red for a downloadable product because its terms bar sale.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [CIPC (Companies and Intellectual Property Commission)](https://www.cipc.co.za/) | Companies and close corporations: enterprise number, status, address | Free enterprise search ended in 2021; disclosure certificate R30; developer API (APIVerse) needs application and approval, pricing not public [S] | Licensed API or resellers; no open bulk | Live | Medium: directors | **AMBER** |
| [HPCSA register of practitioners](https://www.hpcsa.co.za/Dynamic/Search) | Doctors, dentists, psychologists, allied health | Terms not read; UNVERIFIED | Registration status check; QR practising card [S]; no bulk | Live | HIGH: named individuals | **AMBER** |
| [DBE EMIS Master List of Schools (2016-2021 on DataFirst)](https://www.datafirst.uct.ac.za/dataportal/) | Public and independent schools: name, province, district, phase, quintile, coordinates | DataFirst access terms not read; UNVERIFIED | Downloadable datasets with metadata [S] | Annual (latest year seen: 2021) [S] | Low at school level | **AMBER** |
| [cidb Register of Contractors](https://www.cidb.org.za/) | Contractors by grade (1-9) and class of work | Public register; terms not read [BG, UNVERIFIED] | Web search; downloads unconfirmed | Live | Medium | **AMBER** |
| [DHET registers of private colleges and higher-education institutions; SAQA NLRD providers](https://www.dhet.gov.za/) | Registered private colleges, accredited providers | Terms not read [BG, UNVERIFIED] | PDF and web lists | Periodic | Low | **AMBER** |
| [Stats SA data](https://www.statssa.gov.za/) | Statistics, census, business frame aggregates | Free for non-commercial use only; neither the data nor processed versions may be sold without permission [S]. A paid download built on it would breach this | Downloads | Per release | Low | **RED** |
| [data.gov.za and municipal open data](https://data.gov.za/) | Municipal facilities, clinics, schools layers | Per-dataset licence; UNVERIFIED [BG] | CKAN downloads | Per dataset | Low | **AMBER** |
| [Chambers and associations (Cape, Gauteng, SACCI, BUSA members)](https://www.sacci.org.za/) | Member firms by sector | Directories belong to each body [BG, UNVERIFIED] | Web directories | Annual | Medium | **AMBER** |

**Gaps.** CIPC API pricing and terms, DataFirst access terms, cidb download rights, HPCSA bulk route.

### Indonesia

**Privacy law.** Personal Data Protection Law 27/2022, with full effect from October 2024 [BG].

**Start with.** Satu Data Indonesia, SATUSEHAT facility index (if public), Dapodik school profiles, PDDikti for institutions (never lecturers or students), AHU for entities.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [Satu Data Indonesia (data.go.id)](https://data.go.id/) | Central, regional and agency datasets (health, education, economy) | Licence per dataset; UNVERIFIED | Portal downloads and API | Per dataset | Low | **AMBER** |
| [SATUSEHAT Master Sarana Index and RS Online (SIRS)](https://kemkes.go.id/id/satusehat-platform-layanan-kesehatan-digital-indonesia) | 60,000+ facilities: 10,000+ primary care, 17,000 private clinics, 3,000 hospitals, 1,000 labs, 30,000+ pharmacies [R] | Whether public is unconfirmed; UNVERIFIED | Kemenkes systems; public export unknown | Unknown | Low | **AMBER** |
| [Dapodik school data (Kemendikdasmen)](https://dapo.kemendikdasmen.go.id/) | Schools: institutional data, facilities (student, teacher and staff data exist in the system and must not be imported) | Terms not read; UNVERIFIED | Public school profile pages [BG]; no bulk confirmed | Semester | Low at school level; HIGH for teachers and students | **AMBER** |
| [PDDikti (higher education database)](https://pddikti.kemdiktisaintek.go.id/) | Universities, programmes, accreditation; the database also holds lecturers and students (do not import persons) | Terms not read; UNVERIFIED | Public search | Semester | HIGH for lecturers and students; low for institutions | **AMBER** |
| [AHU Online (Ministry of Law) and OSS-RBA (NIB)](https://ahu.go.id/) | Registered legal entities; business identification numbers (NIB replaced TDP and other permits) [S] | Terms not read; AHU is a public lookup [S]; OSS needs an account (red if used logged in) | Per-record search on ahu.go.id | Live | Medium | **AMBER** |
| [LPJK / SIKI construction registry (SBU, SKK)](https://siki.pu.go.id/) | Construction firms with SBU certificates; workers with SKK | Public SIKI search not confirmed [R, UNVERIFIED] | Unknown | Unknown | Medium-high for workers | **AMBER** |
| [KADIN Indonesia and sector association directories](https://kadin.id/) | Member firms | Member directories belong to each body [BG, UNVERIFIED] | Web directories | Annual | Medium | **AMBER** |

**Gaps.** Public access to SATUSEHAT MSI, SIKI, Dapodik export and dataset licences.

### Vietnam

**Privacy law.** Decree 13/2023 on personal data protection; a Personal Data Protection Law was reported passed in 2025 [BG, UNVERIFIED].

**Start with.** National Data Portal and the business registration portal (Vietnamese only, no API). Health and education lists are ad hoc per ministry or province.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [National Business Registration Portal (dangkykinhdoanh.gov.vn)](https://dangkykinhdoanh.gov.vn/) | Enterprises: name, enterprise ID, address, business lines, legal representative, status [S] | Basic info free; terms not found; UNVERIFIED | Vietnamese-only web search; no public API [S] | Live | Medium: legal representative named | **AMBER** |
| [National Data Portal (data.gov.vn, open.data.gov.vn)](https://data.gov.vn/) | Open datasets (health, education, economy) | Licence varies by dataset [S] | CSV, JSON, GeoJSON, API [S] | Per dataset | Low | **AMBER** |
| [Ministry of Health and provincial Departments of Health licence lists](https://moh.gov.vn/) | Licensed hospitals, polyclinics, specialised clinics (licences issued by MoH and provincial health agencies [S]) | Lists appear ad hoc (e.g. facilities eligible for foreigner health checks [S]); terms UNVERIFIED | Web and PDF lists per province | Ad hoc | Low | **AMBER** |
| [MOET lists of schools, universities and foreign-invested institutions](https://moet.gov.vn/) | Universities, colleges, international schools | Terms not read [BG, UNVERIFIED] | Web lists | Annual | Low | **AMBER** |
| [VCCI directory and VCCI-linked associations](https://vcci.com.vn/) | Exporters, manufacturers, SMEs | Directory belongs to VCCI [BG, UNVERIFIED] | Web directory | Unknown | Medium | **AMBER** |

**Gaps.** Dataset licences, any bulk route for the registry, MoH master facility list.

### Brazil

**Privacy law.** LGPD; MEI and EI records are natural persons [S].

**Start with.** CNPJ monthly files and CNES establishment files are the best bulk government sources outside India, the UK, France and Mexico. Both lack a licence statement in the snippets, so read the terms and record reviewed_on before import (likely upgrade to green).

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [Receita Federal CNPJ dados abertos](https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj) | All Brazilian legal entities: name, status, CNAE activity, address, partners (QSA) [S] | Public open files; the licence text is not shown in the snippets, so UNVERIFIED (likely upgradable to green). Brazil's open-data decree makes government data open by default [BG] | Monthly bulk files at arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj [S] | Monthly [S] | Medium: MEI and EI are natural persons under LGPD; partner CPF is masked; new MEI records have no CPF since Dec 2022 [S] | **AMBER** |
| [CNES establishments (DATASUS)](https://cloud.r-project.org/web/packages/healthbR/vignettes/cnes-health-facilities.html) | All health establishments, public and private: type, beds, equipment, services (13 file types, 2005-2024) [R] | Licence not read; UNVERIFIED. CNES is described as a public registry [S] | Monthly .dbc files by state on the DATASUS FTP; R packages healthbR and microdatasus read them [R] | Monthly [R] | Low for establishments | **AMBER** |
| [CNES professionals file (same source)](https://cloud.r-project.org/web/packages/healthbR/vignettes/cnes-health-facilities.html) | Health professionals linked to establishments | Person-level data under LGPD; do not import rows about named people; keep only counts by specialty per establishment [I] | Same monthly files | Monthly | HIGH | **AMBER** |
| [INEP school census (Censo Escolar) and school catalogue](https://www.gov.br/inep/pt-br) | Schools: public and private, level, location | INEP moved to simplified microdata in 2022 and withheld student and teacher level data for LGPD reasons [S]; terms UNVERIFIED | Downloads at inep.gov.br | Annual | Low at school level | **AMBER** |
| [dados.gov.br national open data portal](https://dados.gov.br/) | Datasets from federal bodies | Terms of use on the portal wiki; CC BY 4.0 is used at some Brazilian portals [S]; confirm per dataset | Portal downloads and API | Per dataset | Low | **AMBER** |
| [CFM and state CRM portals](https://portal.cfm.org.br/) | Doctors: name, CRM number, state, specialty (400,000+) [R] | CFM warns doctors about data disclosure; Resolution 2,309/2022 governs data handling [R]; terms UNVERIFIED | Per-record search; no bulk | Live | HIGH: named individuals | **AMBER** |
| [e-MEC (higher education institutions and courses)](https://emec.mec.gov.br/) | Accredited universities, colleges, courses | Terms not read [BG, UNVERIFIED] | Public search; open data files [BG] | Continuous | Low | **AMBER** |
| [CNI, FIESP, Fecomercio and chamber member directories](https://www.portaldaindustria.com.br/) | Manufacturers, traders | Member directories belong to each body [BG, UNVERIFIED] | Web directories | Annual | Medium | **AMBER** |

**Gaps.** CNPJ and CNES licence text, CFM/CRM terms, CREA/Confea (nothing found).

### Mexico

**Privacy law.** Federal private-sector data protection law; the 2025 replacement of the earlier statute is reported [BG, UNVERIFIED].

**Start with.** DENUE is the single most useful business directory in the set (5-6M establishments with an explicit free-use term). Add CLUES for health and the SEP catalogue for schools.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [INEGI DENUE (National Statistical Directory of Economic Units)](https://www.inegi.org.mx/app/mapa/denue/) | 5-6 million establishments: name, activity (SCIAN), size band, address, coordinates, often phone and email; 2024 Economic Census edition [S] | INEGI Terminos de Libre Uso: commercial reuse with attribution [S] | REST API (a free token is required per INEGI docs [BG]; one summary says no key [S]) and bulk downloads by state and activity [BG] | Several editions a year [BG] | Medium: sole traders' names and contacts | **GREEN** |
| [datos.gob.mx national open data portal](https://datos.gob.mx/) | Datasets from federal bodies (health CLUES, education, tourism) | Libre Uso MX terms: free reuse with attribution [S] | CKAN downloads and API | Per dataset | Low | **GREEN** |
| [CLUES (Clave Unica de Establecimientos de Salud) catalogue, Secretaria de Salud / DGIS](https://www.dgis.salud.gob.mx/) | Hospitals, clinics, health centres, public and private | Published as open data [BG]; licence text UNVERIFIED | Catalogue download [BG] | Monthly [BG] | Low | **AMBER** |
| [SEP school catalogue (Catalogo de Centros de Trabajo) and SIGED](https://www.sep.gob.mx/) | 260,000+ schools [S] | Terms not read [UNVERIFIED] | Catalogue file [BG]; SIGED is internal | Periodic | Low at school level | **AMBER** |
| [SIEM (Sistema de Informacion Empresarial Mexicano)](https://siem.economia.gob.mx/) | Businesses registered with chambers (Secretaria de Economia) | Government directory; reuse terms not read [BG, UNVERIFIED] | Web search by state and activity | Live | Medium: contact people | **AMBER** |
| [Cedula profesional lookup (SEP Registro Nacional de Profesionistas)](https://cedulaprofesional.sep.gob.mx/) | Licensed professionals (doctors, lawyers, architects) | Terms not read [BG, UNVERIFIED] | Per-record lookup by name or cedula number | Live | HIGH | **AMBER** |

**Gaps.** DENUE token requirement and bulk route, CLUES and SEP licence text, SIEM terms.

### United Kingdom

**Privacy law.** UK GDPR and Data Protection Act 2018; an individual not told within one month is a breach (Article 14) [R]; PECR governs electronic marketing [BG].

**Start with.** Companies House, CQC, FSA ratings, charities and GIAS are all open and daily or monthly. Drop named managers, trustees and head teachers.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [Companies House free company data product and API](https://www.data.gov.uk/dataset/companies-house-free-company-data-product) | All live companies: name, number, type, registered office, SIC code, status, accounts dates (no officers) [S] | Open licence; Open Government Licence v3.0 [BG]; monthly snapshot is free [S] | Monthly snapshot ZIPs of CSV within 5 working days of month end [S]; free REST API with key | Monthly snapshot; API live | Low-medium: sole-trader company addresses | **GREEN** |
| [CQC care directory and API](https://www.cqc.org.uk/about-us/transparency/using-cqc-data) | Hospitals, GP practices, dentists, care homes, clinics with ratings and service types [S] | Open Government Licence [S] | API and downloadable data sheets; updated daily [S] | Daily [S] | Low: registered managers named (drop them) | **GREEN** |
| [Get Information About Schools (GIAS)](https://get-information-schools.service.gov.uk/Downloads) | Every educational establishment in England, with type, phase, address, Ofsted link | Government data; OGL is likely [BG, snippet silent] | Downloads page generates a ZIP/CSV on demand [S] | Daily [S] | Low-medium: head teacher name fields (drop them) | **AMBER** |
| [Food Standards Agency Food Hygiene Rating Scheme](https://ratings.food.gov.uk/open-data/) | Restaurants, takeaways, caterers, shops that handle food, with ratings | Open Government Licence v3.0 [S] | API (XML, JSON) with no registration; per-authority XML files [S] | Daily to weekly [BG] | Medium: includes sole traders' premises | **GREEN** |
| [Charity Commission register of charities (England and Wales)](https://register-of-charities.charitycommission.gov.uk/) | Charities, schools trusts, community groups, with income | Open data downloads and API [S]; OGL is likely [BG] | Downloadable register extracts and API | Weekly to monthly [BG] | Medium: trustees named (drop them) | **GREEN** |
| [NHS England Organisation Data Service (ODS)](https://digital.nhs.uk/services/organisation-data-service) | GP practices, pharmacies, hospitals, trusts | Open data under OGL [BG, UNVERIFIED] | Downloadable files and API | Weekly to monthly [BG] | Low | **AMBER** |
| [data.gov.uk and local authority open data (licensing, planning, food premises)](https://www.data.gov.uk/) | Premises licences, taxi, alcohol, care providers by council | Mostly OGL; read per dataset [BG] | CKAN downloads | Per dataset | Low-medium | **AMBER** |
| [GMC, GDC, SRA and trade-scheme registers (Gas Safe, NICEIC, FCA)](https://www.gmc-uk.org/registration-and-licensing/the-medical-register) | Doctors, dentists, solicitors, regulated trades and finance firms | Public lookups; terms not read [BG, UNVERIFIED] | Per-record lookup; some APIs | Live | HIGH for named individuals | **AMBER** |

**Gaps.** GIAS and Charity Commission licence text (OGL assumed from background), NHS ODS terms.

### United States

**Privacy law.** No federal comprehensive law; state laws apply; California covers business contacts and job applicants and the Delete Act reaches data brokers [R].

**Start with.** NPPES organisations, FDA registrations, SEC, IRS TEOS and NCES are federal public data with no use restriction found. State licence boards and Secretary of State registries vary by state.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [CMS NPPES NPI file (organisations, Type 2)](https://www.cms.gov/medicare/regulations-guidance/administrative-simplification/data-dissemination) | Hospitals, clinics, labs, group practices, DME suppliers with name, address, taxonomy | FOIA-disclosable public data; no charge [S]. CMS announced changes to NPPES data dissemination in a Federal Register notice of 31 July 2025 that this search could not open [S, UNVERIFIED] | Monthly full-replacement ZIP plus weekly incremental and monthly deactivation files [S] | Monthly and weekly [S] | Low for organisations | **GREEN** |
| [CMS NPPES NPI file (individual providers, Type 1)](https://www.cms.gov/medicare/regulations-guidance/administrative-simplification/data-dissemination) | Doctors, dentists, nurses, therapists with name, practice address, phone, taxonomy | Same file; individuals' records should not be bulk-published (state privacy laws, CCPA covers business contacts) [R] | Same files | Monthly and weekly | HIGH: named individuals | **AMBER** |
| [FDA establishment registration and listing](https://www.fda.gov/) | Food, drug, device manufacturers and importers | CC0 per pilot research; repo default green [R] | Bulk files | Continuous | Low | **GREEN** |
| [SEC EDGAR (company tickers, submissions, bulk JSON)](https://www.sec.gov/page/sec-api-documentation) | Listed and filing companies with SIC code, address, filings | US government filings are public; automated access must follow SEC fair-access limits and set a user agent [S, BG] | ftp.sec.gov and nightly bulk ZIP at about 3 a.m. ET [S]; data.sec.gov submissions JSON [S] | Nightly [S] | Low | **GREEN** |
| [IRS Tax Exempt Organization Search bulk data](https://www.irs.gov/charities-non-profits/exempt-organizations-select-check) | Charities, nonprofits, schools, churches: Pub. 78, revocation list, 990-N, 990 series [S] | US government data; downloads offered [S] | Bulk downloads on irs.gov [S] | Monthly [BG] | Low: EINs of organisations | **GREEN** |
| [NCES Common Core of Data (public schools, districts) and Private School Universe Survey; IPEDS colleges](https://nces.ed.gov/ccd/) | Public schools and districts with address and phone; private schools; colleges | US government statistical data; CCD datasets 1995 to latest; Build a Table tool [S] | Downloads | Annual | Low at school level | **GREEN** |
| [State licensing boards (contractors, medical, cosmetology) e.g. California CSLB](https://www.cslb.ca.gov/Resources/FormsAndApplications/FULL_FILE_-_UPDATE_FILE_ORDER_FORM.pdf) | Licensed contractors and professionals by state | Varies by state; CSLB sells a Full File and Update File at USD 235 each [S]; resale terms UNVERIFIED | Mostly per-record web search; a few states sell bulk files | Live | HIGH for individuals (home addresses sometimes shown) | **AMBER** |
| [State Secretary of State business registries and SAM.gov entity data](https://sam.gov/) | Companies and LLCs; federal contractors | Terms vary by state; some sell bulk; SAM.gov public extract terms not read [BG, UNVERIFIED] | State portals; SAM.gov bulk extract | Live to daily | Medium: registered agents and sole proprietors | **AMBER** |
| [City and state open data portals (NYC, Chicago, Los Angeles, Texas)](https://opendata.cityofnewyork.us/) | Business licences, health inspections, permits | Per-portal terms, often permissive; read per dataset [BG] | Socrata and CKAN downloads | Per dataset | Low-medium | **AMBER** |

**Gaps.** The July 2025 NPPES dissemination notice (could not be opened); resale terms for state files; SAM.gov extract terms.

### Germany

**Privacy law.** GDPR and BDSG; UWG section 7 limits B2B marketing contact [BG].

**Start with.** GovData and Destatis are open (Datenlizenz Deutschland). The Handelsregister is free to view but not an open bulk source. Handwerkskammer registers are the lead for trades.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [Handelsregister (common registers portal)](https://www.handelsregister.de/) | Companies: HRA/HRB entries (about 150 local court registers behind one portal) [S] | Free to view since August 2022 [S]; automated bulk retrieval is limited by portal rules [BG, UNVERIFIED] | Per-record search on handelsregister.de; paid structured data via vendors | Live | Medium: managing directors named | **AMBER** |
| [Unternehmensregister and Bundesanzeiger](https://www.unternehmensregister.de/) | Annual accounts and notices of companies; Bundesanzeiger updates daily [S] | Public notices; reuse terms restrictive [BG, UNVERIFIED] | Web search | Daily [S] | Medium | **AMBER** |
| [GovData (national open data portal)](https://www.govdata.de/) | 120,000+ datasets: facilities, schools, hospitals, transport (September 2024) [S] | Datenlizenz Deutschland (dl-de/by-2-0 and dl-de/zero-2-0) allows commercial reuse with attribution [S]; some datasets use other licences | CKAN downloads and API | Per dataset | Low | **GREEN** |
| [Destatis GENESIS-Online](https://www.destatis.de/EN/Press/2021/07/PE21_351_p001.html) | 1.2 billion statistical values from 306 statistics [S]; business and education aggregates (not lists) | Open data; Datenlizenz Deutschland attribution [S, BG] | API and downloads | Per release | None | **GREEN** |
| [G-BA structured quality reports of hospitals](https://www.g-ba.de/) | All German hospitals with departments and case counts (XML) | Published by the Federal Joint Committee; reuse terms UNVERIFIED [BG] | XML files by reporting year [BG] | Annual | Low | **AMBER** |
| [Bundesaerztekammer Arztsuche and Kassenaerztliche Vereinigung doctor search; Stiftung Gesundheit Arzt-Auskunft](https://www.bundesaerztekammer.de/arztsuche) | Physicians by region and specialty | Chambers and KVs run search tools [S]; Arzt-Auskunft is offered for embedding on websites (licence needed) [S]; no open bulk | Per-search web tool; paid embed | Live | HIGH: named individuals | **AMBER** |
| [Handwerkskammern (Handwerksrolle) and IHK company search](https://www.zdh.de/) | Craft businesses (plumbers, electricians, bakers, roofers) by chamber; member firms | Public lookups per chamber; the IHK Act limits use of member data [BG, UNVERIFIED] | Per-chamber web search | Live | Medium: sole traders | **AMBER** |
| [Hochschulkompass (HRK)](https://www.hochschulkompass.de/) | Universities, programmes | Terms not read [BG, UNVERIFIED] | Web search and lists | Continuous | Low | **AMBER** |

**Gaps.** Handelsregister automated-access rules, G-BA and Hochschulkompass terms, HWK and IHK reuse rules.

### France

**Privacy law.** GDPR; CNIL enforces Article 14 against scrapers (KASPR, EUR 240,000) [S].

**Start with.** SIRENE, Annuaire de l'education and FINESS are all open under the Licence Ouverte and bulk-downloadable on data.gouv.fr. RPPS is person-level and amber.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [Base SIRENE (INSEE)](https://www.data.gouv.fr/fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/) | All businesses and establishments: SIREN/SIRET, name, address, NAF code, status, size band; about 9M legal entities, 10M active establishments [S] | Licence Ouverte (open licence), free reuse since 1 January 2017 [S] | Monthly stock CSV files and daily update files on data.gouv.fr [S]; API | Monthly stock, daily updates [S] | Medium: sole traders (entrepreneurs individuels); non-diffusible entries must be dropped [BG] | **GREEN** |
| [Annuaire de l'education (Ministry of National Education)](https://www.data.gouv.fr/datasets/annuaire-de-leducation) | Public and private schools, medico-social institutions, information centres; sources ONISEP and RAMSESE [S] | data.gouv.fr dataset; Licence Ouverte is likely [BG] | Download and API on data.gouv.fr [S] | Frequent | Low-medium: head names in some fields (drop them) | **GREEN** |
| [FINESS (national file of health and social establishments)](https://drees.solidarites-sante.gouv.fr/sources-outils-et-enquetes/le-fichier-national-des-etablissements-sanitaires-et-sociaux-finess) | Hospitals, clinics, labs, pharmacies of record, care homes, social structures with category and legal status | Full extract on data.gouv.fr [S]; Licence Ouverte is likely [BG] | Download 'Extraction FINESS' on data.gouv.fr [S] | Frequent | Low | **GREEN** |
| [RPPS and Annuaire Sante (health professionals)](https://annuaire.sante.fr/) | Doctors, dentists, nurses, pharmacists and their practice situations; data from the professional orders and ARS [S] | Free to read or manually download excerpts at annuaire.sante.fr [S]; open extract terms UNVERIFIED | Excerpt downloads and API | Frequent | HIGH: named individuals; GDPR Article 14 notice duty applies | **AMBER** |
| [data.gouv.fr and annuaire-entreprises.data.gouv.fr API](https://www.data.gouv.fr/) | National portal; company search API built on SIRENE and RNE | Licence Ouverte for most datasets [BG]; confirm per dataset | CKAN-style downloads; free API [BG] | Per dataset | Low-medium | **GREEN** |
| [Chambers of commerce and trades (CCI, CMA) and professional orders (CNOM, CNOP, avocats)](https://www.cci.fr/) | Craft and trade firms; regulated professionals | Directories and annuaires belong to each body [BG, UNVERIFIED] | Web directories | Live | HIGH for individuals | **AMBER** |

**Gaps.** Confirm Licence Ouverte on each dataset; RPPS extract terms; non-diffusible handling in SIRENE.

### Philippines

**Privacy law.** Data Privacy Act 2012 [BG].

**Start with.** data.gov.ph and PSA OpenSTAT are open with attribution. NHFR, CHED and DepEd give institutions. SEC, DTI and PRC are per-record.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [SEC eSEARCH](https://www.sec.gov.ph/) | Corporations, partnerships, foreign branches [S] | Basic name search free, no account; certified documents PHP 50-500 per document with an account [S]; reuse terms UNVERIFIED | Per-record search | Live | Medium | **AMBER** |
| [DTI Business Name Registration System verification](https://bnrs.dti.gov.ph/verification) | Sole-proprietor business names (five-year registration) [S] | Terms not read; UNVERIFIED | bnrs.dti.gov.ph/verification per-record | Live | HIGH: sole proprietors are individuals | **AMBER** |
| [PSA OpenSTAT](https://openstat.psa.gov.ph/) | Statistics (not lists) | Open data licence: free use, re-use and redistribution with source attribution [S] | PC-Axis tables and downloads | Per release | None | **GREEN** |
| [data.gov.ph](https://data.gov.ph/) | Datasets from national agencies | Free and without restriction unless otherwise indicated; credit the agency [S] | Portal downloads | Per dataset | Low | **GREEN** |
| [DOH National Health Facility Registry (NHFR)](https://nhfr.doh.gov.ph/) | Official master list of health facilities [S] | Terms not read; public export unconfirmed; UNVERIFIED | Registry web search | Unknown | Low | **AMBER** |
| [CHED lists of higher education institutions; DepEd masterlist of schools](https://ched.gov.ph/list-of-higher-education-institutions-2/) | Universities and colleges; basic education schools | CHED lists are PDFs and web pages [S]; DepEd terms not read [BG, UNVERIFIED] | PDF and web lists | Annual | Low | **AMBER** |
| [PRC LERIS licence verification](https://verification.prc.gov.ph/) | Licensed professionals (engineers, doctors, accountants, architects) | Free verification by name or licence number [R]; terms UNVERIFIED | Per-record; no bulk | Live | HIGH: named individuals | **AMBER** |
| [PhilGEPS merchants and PCCI / PHILEXPORT directories](https://www.philgeps.gov.ph/) | Government suppliers; exporters and traders | Terms not read [BG, UNVERIFIED] | Web search and directories | Live | Medium | **AMBER** |

**Gaps.** NHFR export, DepEd file terms, PhilGEPS terms.

### Sri Lanka

**Privacy law.** Personal Data Protection Act No. 9 of 2022 [BG].

**Start with.** Open data portal (licence varies), UGC list, Ceylon Chamber directory with permission. eROC is account-gated and therefore red; SLMC is verify-only.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [Registrar of Companies eROC](https://eroc.drc.gov.lk/) | Companies by name or registration number [S] | An account is required for all access; paid extracts LKR 500-5,000; partial English interface [S]. Account-gated, so red for agents | Per-record, login | Live | Medium | **RED** |
| [Open Data Portal Sri Lanka (data.gov.lk, ICTA)](https://data.gov.lk/) | Agriculture, demography, economy, infrastructure, transport datasets [S] | Licence listed as 'Open (varies)' [S] | Portal downloads and API | Per dataset | Low | **AMBER** |
| [UGC recognised universities and institutions](https://www.ugc.ac.lk/) | 17 state universities [S] plus recognised degree-awarding institutes | Terms not read [UNVERIFIED] | Web lists | Annual | Low | **AMBER** |
| [SLMC registers (MySLMC)](https://slmc.gov.lk/en/public/registers) | Medical practitioners, specialists, dentists, pharmacists, midwives, paramedical staff [S] | Free search 24 hours; terms not read [S] | Per-record search; no bulk | Live | HIGH: named individuals | **AMBER** |
| [Ceylon Chamber of Commerce Directory of Members and SME registry](https://www.chamber.lk/) | 630 member companies in the directory [S]; SME registry launched by the Chamber [S] | Directory belongs to the Chamber; written permission needed | Printed and web directory | Annual | Medium | **AMBER** |
| [Private health and training regulators (PHSRC registered private medical institutions; TVEC registered training institutes)](https://tvec.gov.lk/) | Private hospitals, labs; NVQ training providers | Public lists likely; terms not read [BG, UNVERIFIED] | Web lists and PDFs | Periodic | Low | **AMBER** |
| [Department of Census and Statistics](https://www.statistics.gov.lk/) | Statistics and establishment census aggregates [BG] | Terms not read [UNVERIFIED] | Downloads | Per release | None | **AMBER** |

**Gaps.** Dataset licences, PHSRC and TVEC lists, whether a bulk company extract can be bought.

## 6. Sources to exclude

All red. They come from repo rule R22 (scraped Google Maps, Facebook, Baidu, Amap, logins, anti-bot bypass, bought lists), decision D15, and the findings above. The reasons are contract terms, privacy law and the earlier hiQ and KASPR outcomes.

A caution on the Meta ruling: in Meta v. Bright Data (January 2024) the court held that logged-off scraping of public data did not breach Meta's terms [S]. Some scrapers cite it. It decides one contract claim in one court. It does not cover logged-in access, GDPR Article 14, copyright or database rights, and it does not make the data licensed. The gate stays red.

| Source | List types | Licence and terms | Access | Update | Personal-data risk | Gate |
|---|---|---|---|---|---|---|
| [Google Maps Platform (Places API, Place Details, Geocoding) and any scraping of Google Maps](https://cloud.google.com/maps-platform/terms/maps-service-terms/index-20240422) | Business names, addresses, phones, ratings, reviews | Terms bar export, extraction, scraping and bulk download of Maps content, including places data, business names, addresses and reviews, and caching beyond narrow limits [S]; repo rule R22 | Scrapers and SERP APIs | n/a | Reviews are personal data of reviewers | **RED** |
| [Google Business Profile, Google Search results, Google Scholar](https://policies.google.com/terms) | Business profiles; ranked results; academic profiles | Terms prohibit automated access [BG]; Scholar has no API and blocks fast queries [R] | n/a | n/a | Medium-high | **RED** |
| [Facebook and Instagram pages, groups, Marketplace (Meta)](https://www.facebook.com/terms.php) | Business pages, contacts, groups | Terms ban collecting data by automated means [S]. In Meta v. Bright Data (N.D. Cal., 23 Jan 2024) the court found no breach of contract by logged-off scraping of public data [S]; that narrow ruling does not cover logged-in access, privacy law or copyright, so the repo keeps this red (D15, R22) | n/a | n/a | HIGH | **RED** |
| [LinkedIn profiles and company pages (and tools like Kaspr built on them)](https://www.linkedin.com/legal/user-agreement) | People and companies | hiQ v. LinkedIn ended with USD 500,000 judgment, permanent injunction and deletion order (Dec 2022) [R]; CNIL fined KASPR EUR 240,000 for scraping contact details beyond what users expected, including breach of the Article 14 notice duty [S] | n/a | n/a | HIGH | **RED** |
| [Yelp (Fusion API and site)](https://terms.yelp.com/developers/api_terms/) | Reviews, local businesses | Content may not be cached over 24 hours; commercial use needs written consent; no use to train generative AI [S] | API | n/a | Medium | **RED** |
| [Tripadvisor (Content API and site)](https://tripadvisor-content-api.readme.io/reference/terms-of-use) | Hotels, restaurants, attractions | Scraping and browser automation prohibited; only location_id may be cached without limit [S] | API | n/a | Medium | **RED** |
| [Justdial, IndiaMART, Sulekha, Zameen, Dubizzle, OLX, Property Finder, Jiji and other directories or classifieds](https://www.justdial.com/Terms-of-use) | Business listings, dealer and agent contacts | Site terms bar scraping; in India scraping can also raise liability under the IT Act, 2000 [S]; these are also AllLists's competitors | Scrapers (Apify, Oxylabs) sell the data [S] | n/a | HIGH | **RED** |
| [Baidu Maps and Amap (Gaode)](https://lbsyun.baidu.com/) | China POIs | Named red in the repo (R22, D15). Their terms were not retrievable in this search, so the platform terms are UNVERIFIED | Scraping | n/a | Medium | **RED** |
| [Bought or rented lists and data-broker files (ZoomInfo, Apollo, InfobelPRO, Dun & Bradstreet extracts, B2B list vendors)](https://www.infobelpro.com/) | Contacts and firmographics | Licences bar resale and often require seed-record audit; repo rule R22 names bought lists red [R] | Purchase | n/a | HIGH | **RED** |
| [Third-party scrapes and mirrors of official registers (Apify actors for NMC, GSTIN, CNES; zavis.ai doctor profiles; ePharma doctor chambers; masothue-style tax code sites)](https://apify.com/) | Doctors, firms | Shows the data is reachable, not that it is permitted; they carry their own terms and personal data [R] | Resold feeds | n/a | HIGH | **RED** |
| Registers behind logins, OTP, captcha or national-ID checks (TAMM, UAE Pass, MERSIS, eROC, NADRA, Aadhaar-linked, GST and Udyam captcha tools used by bots) (`backend/intake/gate.py`) | Any | The gate treats logins and anti-bot bypass as red (R22); a human may verify one record, an agent may not | n/a | n/a | HIGH | **RED** |
| National ID numbers (CNIC, Aadhaar, Emirates ID, Iqama, CPF, NIK) and tax numbers of individuals (`docs/DECISIONS.md`) | Identifiers | Never collect or store; use only to verify with the owner's consent [I] | n/a | n/a | HIGH | **RED** |
| [Published taxpayer and election lists naming individuals (FBR Active Taxpayer List by CNIC, bar council voter-list PDFs)](https://www.fbr.gov.pk/) | Individuals | Published for tax or election purposes; commercial reuse is questionable [R, I] | PDF and web lists | Annual | HIGH | **RED** |
| [WhatsApp, Telegram and Facebook group member lists; Truecaller-style crowd contact books](https://www.whatsapp.com/legal/terms-of-service) | Phones of tradespeople | Members did not consent to a public directory; platform terms bar it [BG] | n/a | n/a | HIGH | **RED** |
| [GitHub, Kaggle, Upwork, Fiverr profiles pulled for recruiters](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies) | Talent lists | GitHub bars selling users' personal data to recruiters; Upwork bars robots without written permission; Kaggle terms are a binding contract [R] | API and scraping | n/a | HIGH | **RED** |
| [Foursquare Premium attributes and paid Places API (anything beyond the open 22 core fields)](https://docs.foursquare.com/data-products/docs/fsq-places-open-source) | Extra attributes | Open licence covers FSQ OS Places only; premium fields are a paid product [R] | API | n/a | Low | **RED** |
| Leaked, breached or unattributed datasets, and any source without a recorded licence and date (`docs/DECISIONS.md`) | Any | Violates D17 (every record keeps source, licence, date, consent status) | n/a | n/a | HIGH | **RED** |

Red also covers three register rows in the country tables: Turkey MERSIS (account gated), Sri Lanka eROC (account gated) and South Africa Stats SA (licence bars sale).

## 7. Personal-data rules for every row

These apply regardless of rating. They come from the repo (D17, section 7.1) and the earlier reports; counsel should confirm each country.

1. **Drop the person, keep the place.** For registers that name individuals (managers, trustees, head teachers, directors, partners, lecturers, students), import the organisation fields and discard the person fields at load time.
2. **Individuals are verify-only.** For doctors, lawyers, engineers, accountants and sole traders, use the register to badge a person someone else nominated (for example "PMDC verified"). Do not scrape or import the roll. The register terms were not read for any of them.
3. **Never store national or tax ID numbers** of individuals (CNIC, Aadhaar, Emirates ID, Iqama, CPF, NIK, SSN). Use them only to verify, with the owner's consent.
4. **Notice duty.** In the UK, EU and Brazil, a person whose data we hold but did not get from them must be told (UK/EU GDPR Article 14, within one month; LGPD transparency). Poland fined Bisnode about EUR 220,000 for skipping this on 5.7 million records [R]; CNIL fined KASPR EUR 240,000 [S].
5. **Record the evidence.** Each import stores source, licence text, terms URL, attribution, date fetched, `reviewed_on` and `reviewed_by` (D17, R21).
6. **Honour removal.** Offer a removal route from day one, including in Pakistan where the law is still a draft.
7. **Respect robots.txt and rate limits** on every agent fetch (the fetcher already refuses redirects, private addresses and oversize pages).

## 8. What to do next

1. **Load the green global layer first:** Overture places and Foursquare by launch country, GeoNames, Wikidata and ROR identifiers. This is the D16 baseline and needs no permission beyond attribution.
2. **Load the green national layers** where the licence is explicit: India data.gov.in, Mexico DENUE and datos.gob.mx, France SIRENE, FINESS and Annuaire de l'education, UK Companies House, CQC, FSA and charities, Germany GovData, UAE Bayanat, Saudi open data, US NPPES organisations, FDA, IRS and NCES.
3. **Send the Q-S3 emails** for the amber sources that carry the most value and have bulk files: Brazil CNPJ and CNES, Kenya KMPDC and NCA, Pakistan PHC, PEIRA, HEC, SECP list supply and TDAP, Dubai Municipality contractors, Indonesia SATUSEHAT, Philippines NHFR, Turkey health open data. Ask for written terms, whether bulk or partnered access is allowed, and personal-data rules. Record `reviewed_on` when a reply arrives.
4. **Read the terms for [BG] and UNVERIFIED greens** (GLEIF CC0, the UK OGL assumptions, Balady, Annuaire de l'education, FINESS) before they go live.
5. **Decide the ODbL question** (section 2, point 2) before any OSM, OpenCorporates or Healthsites data is merged into published entries.
6. **Ask counsel** (Q-P4) to confirm the exclusion list and the individual-register rule.
7. **For the informal long tail,** use owner claim, society opt-in and OSM, not scraping.

## 9. Limits of this research

- No official page was opened. Search snippets are often undated, and several carry figures that conflict or look old (for example Bangladesh BMDC counts, Saudi contractor numbers, Pakistan PHC totals).
- Licence text was read for none of the registers. The ratings are a first screen.
- Rows tagged [BG] come from memory and may be out of date.
- Google Maps, Meta, Yelp and Tripadvisor terms were read only through summaries of the terms.
- Not covered: sector-specific lists beyond health, education, companies, contractors, chambers and open data (for example lawyers' firms, travel agents, NGOs, mosques), and non-English-language portals beyond what snippets revealed.
- Cross-check against `docs/DECISIONS.md` D14 to D21: nothing here reopens a decided item. D15 and Q-S3 remain open until counsel and the written replies arrive.
