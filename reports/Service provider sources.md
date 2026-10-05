# Service provider sources: where the lists can come from, how platforms earn, and what each entry should hold

Prepared 2026-10-05 for the founder of AllLists.org. Planning research, not legal advice.

## How to read the tags in this report

Official sites were blocked in the research environment. Almost every fact below comes from a search-result summary of a page, not from the page itself. Three tags are used throughout:

| Tag | Meaning |
|---|---|
| [unverified] | A figure or claim from a single secondary source, an undated summary, or a source that conflicts with another. Check it before you rely on it. |
| [inference] | Our own reasoning or judgement. No source says it. |
| (no tag) | Reported in a search summary of the source named. Still not opened by us. |

Nothing in "Decided" or "Agreed" in `docs/DECISIONS.md` is reopened here. Where this report touches a decided item, it says so and works inside it.

---

## Summary of the answer

**1. Who the providers are and where to find them.** The research built a catalogue of 124 service-provider list types in 15 groups (home trades, repair, construction, health, education, professional services, IT, beauty, food and retail, transport, events, civic, farming, domestic help, business services). Each has a natural scale: hyper-local, city, national or global. That scale is our judgement, not a measured fact, and it needs testing with early contributors.

**2. The pattern in the sources.** Organisations are easy to source from official registers. Individuals are not. In Pakistan, hospitals, private schools and universities have public or semi-public lists. Contractors have a legal register (PEC) but we could not confirm a public search. Doctors can be looked up one at a time (PMDC). Plumbers, electricians, tutors and Quran teachers have no register at all. For them, the best source is the housing society, the resident and the provider themselves, with consent. Outside Pakistan, only Brazil showed official bulk files (hospitals and clinics). Most other registers are look-up-one-record tools.

**3. Global talent (data scientists).** Only two sources have open reuse terms: the ORCID public data file and OpenAlex. Both cover researchers only. LinkedIn, Upwork, Google Scholar and most platform terms forbid scraping. GitHub bans selling user data to recruiters. So the safe design is a consent-based list: people register, prove they own their GitHub, Kaggle, Hugging Face or ORCID profile, and choose what buyers see.

**4. How platforms earn.** Four forms carry most of the money: advertising or paid visibility, subscriptions to data or search tools, take rates on work done through a marketplace (Upwork 18.7%, Fiverr 27.7%), and data licences. Recruiter and employer products are the biggest earners among the talent platforms. Pure data subscriptions have high margins (ZoomInfo gross margin 84%) but weak retention. Selling raw name-and-address lists earns little, because free data sets the price near zero. Value sits in the verified layer: confirmed contact, category, freshness and territory.

**5. What this means for AllLists.** The decided revenue model fits the evidence. Start with free pages, ads for free users, and paid outreach delivered by the platform. Add paid ranking and profile upgrades once there is traffic. Keep the USD 1,000 download as a protective price. Treat institutional licences and AI-data deals as later upside. Do not count on take rates yet, because they need payments and liquidity.

**6. What each entry holds.** One common core for every entry (identity, category, location, service area, contact, hours, verification, source, consent, freshness, status, claim state) plus an add-on set per list type. Prices are the most valuable and the stalest field, so every price needs a currency and a date. Personal mobiles, home addresses, ID numbers, child-related data and health data are sensitive and need special handling.

**7. What to decide now.** Section 6 lists eleven decisions, each with a suggested default. The main ones: the pilot city and first source pack (eye care in one city), whether registers are used to verify or to import, how individuals consent, and whether the talent list launches now or after a pilot.

---

## 1) The natural scale of each list type

### What "scale" means

A list type has a natural scale: how far a buyer is willing to go to pick a provider. The decided structure (global to housing society) applies to every type. The natural scale only tells us where to focus first and what the first useful list looks like.

| Scale | Test | Founder example |
|---|---|---|
| Hyper-local (housing society, neighbourhood) | Urgent or frequent need. Trust is local. The provider comes to you or you walk to them. | Plumbers in a housing society |
| City | Planned or specialist need. People travel across the city or compare quotes. | Eye hospitals, MRI centres |
| National | Chosen by registration, tender or reputation, not distance. | Contractors |
| Global | Work is delivered remotely. Skill, rate and time zone matter, not place. | Data scientists |

### Evidence for the scale, and its limits

- Near-me searches are common and lead to visits. Google data repeated by secondary sites says 76% of people who search nearby on a phone visit a related business within a day [unverified, old, repeated widely].
- In one set of US studies, median travel was 12.7 minutes for primary care and 17.1 minutes for specialist care, and rural patients travel much farther to specialists. These are US figures from snippets, with study attribution not confirmed.
- Service marketplaces work city by city. Urban Company runs in about 51 to 59 cities depending on the source and date [unverified, sources conflict]. Thumbtack's default service radius is 150 miles, with a "works remotely" option (user-community posts, not official documentation).
- US data may not transfer. In Pakistan, societies and word of mouth dominate [inference]. Test the scale of each type with the first contributors.

### The inventory by group

The table summarises the 124-type inventory. The inventory is our own design, not a sourced data set. The scale in each row is a typical range, and many types straddle two scales.

| Group | Types | Examples | Typical scale |
|---|---|---|---|
| A. Home repair and trades | 14 | plumbers, electricians, AC technicians, carpenters, mistri | Hyper-local to city |
| B. Appliance and device repair | 10 | mobile repair, laptop repair, car mechanics, tyre shops | Hyper-local to city |
| C. Construction and property | 9 | contractors, architects, engineers, estate agents, material suppliers | City to national (contractors, engineers national; agents hyper-local) |
| D. Healthcare | 17 | GPs, eye doctors, eye hospitals, labs, MRI centres, pharmacies | Hyper-local (GPs, pharmacies) to city or region (specialists, hospitals) |
| E. Education and tutoring | 11 | schools, Quran tutors, academic tutors, coaching centres | Hyper-local to city; online tutors global |
| F. Legal, finance, professional | 13 | lawyers, accountants, tax consultants, banks, translators | City to national; some global |
| G. IT, data and digital | 9 | data scientists, developers, software houses | Global (individuals), national to global (firms) |
| H. Beauty, wellness, personal care | 8 | beauty parlours, barbers, gyms, tailors | Hyper-local |
| I. Food, retail, daily needs | 7 | bakeries, petrol pumps, grocery | Hyper-local |
| J. Transport, logistics, travel | 6 | movers, couriers, travel agents | City to national |
| K. Events and creative | 4 | wedding halls, photographers | City |
| L. Civic and community | 4 | mosques, NGOs, government offices | Hyper-local to national |
| M. Agriculture and rural | 3 | seed dealers, farm machinery repair | Region |
| N. Domestic and household help | 5 | maids, drivers, gardeners, guards | Hyper-local |
| O. Specialised business services | 4 | testing labs, industrial suppliers, waste services | National |

Total: 124 types.

### How the founder's examples sit

| Example | Natural scale | Why |
|---|---|---|
| Plumbers in a housing society | Hyper-local | Urgent, trust-based. A city list is the upper limit. |
| Eye doctors in a society | Hyper-local to city | Individual specialists work at society or city level. |
| Eye hospitals | City to region | Patients travel farther for institutions. |
| MRI centres | City to region | Equipment-limited and referral-driven. |
| Contractors | National | Chosen through registration and tenders. |
| Data scientists | Global | Remote work. |
| Quran tutors | Hyper-local to global | Home tuition is local. Online Quran teaching is global. |

### One taxonomy underneath

The sources suggest one design, which is a proposal and not a decision [inference].

- Industry codes (ISIC; Pakistan's PSIC is identical to ISIC Rev. 4 to four digits) classify firms. Occupation codes (ISCO-08, 436 unit groups, free to use) classify individuals. Both are too coarse for consumer lists. "Eye hospital" and "Quran tutor" have no code of their own. Use them as crosswalk tags only.
- The cleanest open place taxonomy found is Overture Maps (about 2,300 categories, CDLA-Permissive-2.0 licence for the places theme). Foursquare's open categories (Apache 2.0, more than 1,000) are a second reference. Licence of the taxonomy files themselves is [unverified].
- Do not copy the Google Business Profile or Yelp category lists. Reuse terms are unclear or restrictive.
- Add an AllLists-owned layer for individuals and informal trades, plus an alias table for local words. "Mistri" is ambiguous: it can mean plumber, electrician, carpenter or mason, so it should point to a parent "skilled tradesperson" with a prompt to choose.
- Keep the browse tree to about three levels and hold finer detail as tags.
- Urdu and Arabic label coverage in every taxonomy is unverified. A native-language review is needed.

---

## 2) Where the providers can be identified from

### The rule that shapes everything

Decision D21 says to identify providers from established sources first. The research found a clear split:

- Organisations (hospitals, private schools, universities, large contractors, companies) appear in registers and can be sourced with low personal-data risk.
- Individuals (doctors, lawyers, tradespeople, tutors) appear in registers only for regulated professions, and those registers are mostly one-record look-ups. Informal workers appear in no register.

A look-up tool is useful in a different way from a bulk list. It lets us add a badge such as "PMDC verified" to a record someone else nominated. It does not let us build a list.

### Pakistan, sector by sector

| Sector | Source | What it offers | Size (as reported) | Access and risk |
|---|---|---|---|---|
| Doctors, dentists | PMDC | Online search by registration number, name or father's name. Shows licence validity and qualifications. | 366,443 practitioners, date not shown [unverified] | One record at a time. No export found. Personal data. Do not scrape. |
| Eye doctors | Ophthalmological Society of Pakistan (OSP) | Voluntary society with 13 branches. OSP Lahore has a members page. | About 2,000 ophthalmologists | Needs permission. Verify each name on PMDC. |
| Hospitals, clinics, labs | Punjab Healthcare Commission (PHC) | Licence verify page, by licence number. | More than 64,000 registered, over 41,000 licensed [unverified, undated] | Per-licence check. Bulk unclear. A "PHC licensed" badge is a real quality filter, because registered is more than licensed. |
| Same, other regions | KP Health Care Commission; Sindh Healthcare Commission; Islamabad regulator (IHRA); Balochistan | Registration and licensing. | KP about 23,041 registered; Sindh about 14,000 registered of an estimated 100,000 facilities [unverified, undated] | No public searchable list found. Use for cross-checks. |
| Pharmacies | Provincial drug control; DRAP | Retail licences are provincial. DRAP lists manufacturers and drug indexes. | DRAP: about 1,380 manufacturers, about 2,500 importers and distributors | No national public list of pharmacies found. Verification layer only. |
| X-ray, CT, radiology | PNRA | Links to lists of licensed X-ray and medical radiation facilities. | Not found | Format and contents unverified. A possible regulator-grade source for MRI and CT. |
| Public health facilities | opendata.com.pk | CSV of facility names, type and coordinates. | Mostly government facilities | Low risk. Does not cover private eye hospitals. |
| Schools | PEIRA (Islamabad) | Public paginated reports of registered and unregistered private institutions. | Not counted | Low risk (institutions). Terms unverified. |
| Schools, Punjab | PEPRIS (PITB) | Private school registration system. | More than 86,000 institutes registered | Public look-up not confirmed. |
| Schools, national | Pakistan Education Statistics 2023-24 | Totals for market sizing. | 203,411 institutions, 60,904 private | Reports only. |
| Universities | HEC | Public list of recognised universities and campuses. | 179 universities [unverified, date not shown] | Low risk. |
| Madrasas | Directorate General of Religious Education | Registration under the directorate. | 18,600 registered; about 35,000 estimated [unverified, counts vary] | Not examined for list access. |
| Contractors | PEC (Pakistan Engineering Council) | Legal registration gate. Constructor categories C-A to C-6 with project-cost limits. | Only 2016 counts found [unverified] | Whether a public searchable register exists is not confirmed. Category limits come from a 2017 mirror and may be out of date. |
| Contractors, public work | PPRA / EPADS | E-procurement supplier registration. | More than 51,000 suppliers, over 10,000 agencies | A procurement system, not an open directory. Tender award notices may help. |
| Contractors, authorities | CDA, DHA and similar | Scattered PDF lists. DHA enlists PEC-registered contractors (C-5 and above) and vendors. | One 2012 CDA file found | Scrape-and-date or request. |
| Builders | ABAD | Builders' association. | 1,000+ members in 2017 | Partnership route. |
| Lawyers | Pakistan Bar Council; provincial bar councils | Rolls of advocates. KP Bar Council posts per-district PDF lists. | Counts not found | The KP lists are voter lists made for elections. Commercial reuse is questionable. |
| Accountants | ICAP; ICMAP | ICAP has a member directory. | ICAP about 10,096 to 11,285 (sources differ); ICMAP over 7,000 | Opt-in with member number. |
| Tax practitioners | FBR | Registered, no public list found. | Not found | Not a source. |
| Companies | SECP | Free basic search. Fee for data. SECP treated a 2024 scraping incident as unauthorised and tightened access. | Not counted | Manual look-ups only. Do not scrape. |
| Taxpayers | FBR Active Taxpayer List | Downloadable Excel file, weekly. | Not counted | Contains names of individuals. Use only to confirm a business someone nominated. |
| Exporters | TDAP Pakistan Exporters' Directory | Search by product, HS code and company. | Status and size not verified | Worth a written enquiry. |
| Skilled trades | NAVTTC, TEVTA, PSDF | Testing centres and training programmes. TEVTA trains about 220,000 students a year in 403 institutes. | See left | No public register of individual plumbers or electricians found. Graduate lists are personal data. |
| Housing societies | DHA and others | Keep their own vendor lists and gate records. | Not found | The natural partner for local trades. |

NAVTTC has issued qualifications in 25 important trades, which is far fewer than the real set of informal trades. A local alias layer is therefore essential.

### Pakistan: the legal setting

Pakistan had no enacted comprehensive data protection law as of May 2026. The Personal Data Protection Bill 2025 was still a draft. The Prevention of Electronic Crimes Act 2016 applies. Collect consent and offer a removal route from day one anyway, since the draft law is consent-based. Counsel should confirm.

### Ranked build order for Pakistan

The ranking is by ease and legitimacy of the source, not by revenue. `reports/Which lists pay.md` ranks by likelihood of payment and proposes three first tests (health facilities with equipment, urgent trade firms, manufacturers and exporters). The two lists overlap at eye care, health facilities and contractors. Use the source order below for the first data, and the revenue tests there to decide what to sell.

1. **Eye hospitals and eye doctors in one pilot city.** Start from hospital websites, OSP branch pages (with permission) and CPSP-accredited training institutions. Add "PHC licensed" and "PMDC verified" badges. No eye hospital directory was found, so this is a gap we could fill.
2. **Schools and universities.** Islamabad from PEIRA, Punjab through PEPRIS if public, universities from HEC. Low risk, good traffic. Schools are a free anchor, not a first revenue list.
3. **Contractors.** PEC category by city, checked against tender award notices and society enlistments. Show source and date on every row.
4. **Hospitals, labs, diagnostic centres by province.** Pharmacies and radiology use drug inspectors and PNRA as verification layers.
5. **Manufacturers and exporters.** TDAP directory (status unverified), chambers and trade associations. These were not researched in depth.
6. **Plumbers, electricians, AC technicians, tutors.** Through housing-society partnerships and the providers themselves, with consent. An optional NAVTTC or TEVTA certificate badge, checked by certificate number.

How the society route works [inference]: the society manager or welfare committee sends an opt-in link to residents and tradespeople. AllLists adds a verified badge. The society gets a branded list. This is a partnership model, not a data purchase.

### Other countries

All of this rests on snippets. No official page was opened. Ranking is our judgement.

| Rank | Country | Source | Provider type | Evidence of access | First list |
|---|---|---|---|---|---|
| 1 | Brazil | CNES (DATASUS) | Hospitals, clinics, professionals | Monthly bulk files, 13 file types, 2005 to 2024 | Eye hospitals and clinics |
| 2 | Kenya | KMPDC | Doctors, hospitals, clinics | Public search of practitioners and facilities with current-year licence status | Eye hospitals, specialists |
| 3 | Kenya | NCA | Contractors | Public search, eight tiers (NCA 1 to 8) | Contractors (needs active-licence filter) |
| 4 | India | NMC Indian Medical Register | Doctors | Public search, rich fields | Eye doctors (data current to about 2021, gaps in some states) |
| 5 | UAE (Dubai) | Dubai Municipality | Contractors, consultants | Published as data on a government site, format unverified | Contractors in Dubai |
| 6 | Saudi Arabia | Contractors Authority | Contractors | Public status unconfirmed | About 142,000 contractors reported [unverified, undated] |
| 7 | Indonesia | SATUSEHAT facility index | Hospitals, clinics, pharmacies | Public access unconfirmed | More than 60,000 facilities |
| 8 | Nigeria | COREN, CORBON | Engineers, builders, technicians | Look-up by identifier | Verification badges |
| 9 | Bangladesh | BMDC | Doctors, dentists | Public portal | Verification badge |
| 10 | Philippines | PRC LERIS | Licensed professionals | Free look-up by name or number | Verification only |
| 11 | Saudi, UAE | SCFHS; DHA Sheryan | Doctors | Look-up by ID | Verification only |
| 12 | Turkey, Egypt | Health ministry open data; Medical Syndicate | Facilities, doctors | Unverified | Needs more research |

Three cautions:

- Kenyan lists need a filter for active licences. In January 2026 the NCA warned thousands of contractors of de-registration for unpaid fees.
- Third-party scrapes (Apify tools for India's register, commercial doctor sites in the UAE and Bangladesh) show the data is reachable. They do not show it is permitted. Treat them as proof of demand, not as clean sources.
- Brazil's CFM publishes a limited field set and warns doctors about data disclosure. Brazil's data law (LGPD) applies. Licence terms for CNES were not read.

India publishes an open-data licence (GODL-India, 2017) that allows commercial reuse of shareable, non-sensitive government data. Whether the medical register falls under it was not found.

### What is blocked or unverified

- Terms of use, fields, export routes and counts for nearly every portal above.
- For other countries: schools, lawyers and accountants, trade and skills registers, business registries and chamber directories were not searched or not found. These are the biggest holes.
- Personal-data rules in each country were not researched.
- Individual tradespeople appear in no confirmed public register in Pakistan or the other markets (Nigeria's CORBON craftsmen register and Kenya's accredited worker figure are leads only).
- Fake certificates are a documented problem. Bangladesh ordered action against forged skill certificates in February 2026. Treat any certificate number as a claim until checked.

---

## 3) Global talent lists (data scientists)

### Sources, in three tiers

| Tier | Source | What the notes found | Use |
|---|---|---|---|
| Open (CC0) | ORCID public data file | Annual file of public records, released under CC0. People choose visibility. Asks that emails not be used for bulk junk mail and that an opt-out be offered if emails are used commercially. | Match data after a person registers. |
| Open (CC0) | OpenAlex | CC0 snapshot on a public AWS bucket. Since 13 February 2026 the API needs a free key and uses usage-based pricing [unverified, secondary source]. | Same. |
| Conditional API | Semantic Scholar | API licence from AI2, which can end use at any time. | Read the licence in full first. |
| Conditional API | GitHub | Acceptable-use excerpt bars using the API to sell users' personal information to recruiters and headhunters. | Read data only for a user who linked their own account. |
| Conditional API | Hugging Face | Rate-limited API. Content policy covers privacy. | Same. |
| Conditional API | Kaggle | Terms are a binding contract. Clauses on automated access were not read [unverified]. | Same, after reading the terms. |
| Closed | LinkedIn, Upwork pages, Google Scholar | LinkedIn's contract terms were enforced against hiQ. Upwork bars robots without written permission. Google Scholar has no API and blocks fast queries [unverified]. | Do not use. |

Only the open tier is safe for bulk reading, and it covers researchers only.

### Rules

1. **No scraping of platforms.** In hiQ v. LinkedIn, a US court found the anti-scraping terms enforceable as contract. The case ended with a USD 500,000 judgment, a permanent injunction and deletion of data and code (December 2022). Earlier rulings on whether scraping public pages is a crime are from background knowledge and unverified here.
2. **Notice duty in the EU and UK.** If we hold data about a person that we did not get from them, they must be told within one month. Poland fined Bisnode about EUR 220,000 (2019) for skipping this on 5.7 million scraped records. A cost excuse was rejected.
3. **California.** Business and job-applicant data is now covered in full by California's privacy law. The Delete Act lets residents send one deletion request to all registered data brokers, and from 1 August 2026 more than 600 brokers must process these every 45 days [secondary sources]. Whether a consent-only directory counts as a data broker is not verified. Counsel should say.
4. **Platform contracts bind us beyond the law.** GitHub's rule and ORCID's anti-spam request apply even to open or consented data.

Two exits show how hard a pure talent board is on a developer community. Kaggle closed its job board in 2022 and Stack Overflow ended Jobs and Developer Story in March 2022 [both unverified, secondary sources]. The reasons are not established.

### Design (our proposal, not sourced)

- **Entry:** self-registration. Optional "Sign in with ORCID". The person controls visibility, rate, availability and contact preference, and can delete the profile at any time.
- **Verification ladder.** The decision log fixes four named levels (owner-verified, surveyor-verified, AI-checked, not verified yet). For talent, map the evidence like this and keep the decided names:
  - Self-declared, email checked.
  - Linked accounts proven by sign-in or a code in the profile (GitHub, Kaggle, Hugging Face, ORCID), with public stats read through official APIs for that user only.
  - Evidence-backed claims: Kaggle tier, ORCID Trust Markers, matched publications, merged open-source work.
  - Human or test review (portfolio check, short assessment, reference), needed for paid placement.
- **Contact:** the platform relays contact. Buyers get no exports. This fits the decided no-download rule and GitHub's and ORCID's terms.
- **Re-confirm every 90 days.** Rate and availability go stale fast [inference].
- **Who buys:** recruiters, startups and small staffing firms are the named buyers. Universities and governments are possible but unevidenced.
- **Pool size:** a verified pool is small. One vendor blog counts 612 Kaggle Grandmasters and 2,973 Masters [unverified, likely dated]. Seat revenue from so few people is limited. Intro or success fees are likelier.

### Does the same approach fit other professions?

Yes, where a free, readable proof source exists: software engineers (GitHub), researchers (ORCID, OpenAlex). Designers and translators fall back on portfolios and certificates, and the list then loses its main edge over Upwork.

### Gaps

- No evidence of willingness to pay for a small consented list. No reply-rate data for consented versus scraped outreach.
- Papers with Code, DBLP, professional association directories, Toptal, Fiverr and Freelancer terms were not checked.
- Counsel review of every legal point is outstanding.

---

## 4) How established platforms earn

### Revenue streams by platform type

All figures are as shown in search summaries. No filing was opened. Directory figures for Justdial and IndiaMART are in `reports/Which lists pay.md` and are not repeated, except the headline pattern.

| Platform type | Platform | How it earns | Figures cited in the notes |
|---|---|---|---|
| **Directories** | Justdial, IndiaMART | Businesses pay for ranking, campaigns and tiers. | Only about 1% to 3% of listings pay; revenue sits in a thin top tier and the entry tier churns. See `Which lists pay.md`. Fuller detail for 35 directory and lead platforms is in the next table. |
| | Zameen, Dubizzle | Agency subscriptions, paid listings, developer deals. | Dubizzle revenue USD 183M in 2024, recurring 12-month packages. See `Which lists pay.md`. |
| | Yelp | Advertising from service businesses. | Services advertising USD 947.6M, up 8%. See `Which lists pay.md`. |
| | Urban Company | Commission or platform fee. | 73.4% of revenue from commissions and platform fees. |
| | Thumbtack | Fee per lead, Pro subscription, booking commission. | Lead prices about USD 8 to 150 or more by job size [V, vendor blogs]. Revenue figures for Thumbtack are not usable and are left out. |
| | Zocdoc | Fee per new patient booking. | USD 35 to 110 per booking by specialty and location (Zocdoc pages via search). |
| **Talent and jobs** | LinkedIn | Marketing, talent, premium and sales products. | FY2025 revenue USD 17.81B, up 9% (one summary). FY2026 growth 11%. Premium over USD 2B [secondary]. Dollar splits by line are inconsistent and unusable [unverified]. |
| | LinkedIn Recruiter | Seat subscription. | Recruiter Lite about USD 170 a month; full Recruiter roughly USD 8,000 to 15,000 per seat a year [unverified, third-party blogs]. |
| | Indeed, Glassdoor (Recruit) | Employers pay for sponsored jobs. | US revenue up 19% to USD 1.41B in January to March 2026 while postings fell about 7%. Employers pay more per job on fewer jobs. |
| | Naukri (Info Edge) | Recruiter subscriptions and billings. | Recruitment revenue INR 2,374 crore, about 72% of group revenue. Segment margin about 54% (our arithmetic) [inference]. |
| | Upwork | Take rate on work, plus ads and paid plans. | Revenue about USD 788M. Take rate 18.7% (18.0% a year earlier). Freelancer fee 0% to 15% since May 2025. |
| | Fiverr | Take rate, buyer fee, seller services. | Revenue USD 430.9M, take rate 27.7%. Annual active buyers down 13.6% to 3.1M. |
| | Toptal | Client markup. | Take rate not published. Third parties guess 40% to 60% [unverified]. |
| | Stack Overflow | Teams, ads, talent, data licences. | Prosus paid USD 1.8B in 2021 and has written down much of it. Revenue mix of about USD 90M is a third-party estimate [unverified]. |
| | Kaggle | Competitions, courses, past job board. | No revenue disclosed. |
| | Recruiter sourcing tools | Seat subscriptions and credits. | SeekOut about USD 149 per user a month; Juicebox USD 99 to 179; Apollo USD 49 to 119 [unverified, vendor blogs]. |
| **Data and B2B** | ZoomInfo | Subscriptions. | FY2025 revenue USD 1,249.5M. Gross margin 84%. Net revenue retention 89% in Q2 2026 (customers renewing and spending less than a year ago on average). Growth about 1%. |
| | Dun & Bradstreet | Data and analytics sold to finance and sales teams. | FY2024 revenue USD 2,381.7M, adjusted EBITDA margin 38.9%. |
| | PitchBook | Licences. | USD 664.5M in 2025, up 8.6%. Growth came from more licences in large accounts and price rises. |
| | Definitive Healthcare | Subscriptions and services. | FY2025 revenue USD 241.5M, down about 4%. Professional services grew 46% to 49%. |
| | Foursquare | Free open data set; paid API. | API price USD 15.00 per 1,000 calls at entry, falling to 1.25 at volume. Richer "Premium" fields cost 25% to 40% more at the same tier. |
| | OpenCorporates | Free share-alike keys for non-profits; paid keys for commercial use. | GBP 2,250 to 12,000 a year by plan, capped calls. |
| | Overture Maps | Funded by member dues, not data sales. | USD 3,000 to 3 million a year by member level. |
| | Geofabrik | Free map extracts; paid custom exports and services. | Custom export about EUR 350 to 500 for a European country. |
| | Wikimedia Enterprise, Reddit | Data licences to AI firms. | Wikimedia Enterprise USD 8.3M (about 4% of revenue). Reddit about USD 140M in 2025 (about 5% of revenue) [secondary]. |
| **Data marketplaces** | AWS Data Exchange | Small seller fee. | 3% on public offers, 1.5% on large private offers and renewals. |
| | Datarade | Provider subscriptions plus commission. | 30% commission reported [unverified]. |
| | Snowflake Marketplace | Indirect, through buyers' compute. | A 25% to 30% fee circulates [unverified]. Not found in Snowflake's own pages. |

### Directory, local-search and lead platforms: the second note

A separate note covers 35 directory, review, lead and classifieds platforms. Its flags are kept here: [derived] means our arithmetic from cited numbers, [V] means a vendor, agency or aggregator blog, and [unverified] means no trustworthy source or sources conflict. Every figure comes from a search summary of a filing or article. No primary document was opened. The figures that note marks as unusable are not used: Thumbtack revenue, G2 revenue, Sulekha revenue, the Jiji revenue split, Zocdoc enterprise revenue, Yelp's paying-location count and the Europages price.

| Stream | Who uses it | Figures cited |
|---|---|---|
| Subscription or annual package for agents, dealers and advertisers | Justdial, IndiaMART, Rightmove, Dubizzle, Property Finder, Solocal, Thryv, Trustpilot | Rightmove 2025 revenue GBP 425.1M, agency 71.7% of it, underlying operating margin 70%, average GBP 1,530 per agency branch per month [derived monthly basis]. Dubizzle UAE adjusted EBITDA margin 46% in H1 2025 (IPO and press figure, not audited). Property Finder UAE EBITDA margin above 60% in H1 2025 (press). Solocal 2025 revenue EUR 324.5M, with its Priority Listing product about 37% of group revenue [derived]. Trustpilot 2025 revenue USD 261.1M, one stream (business subscriptions), average contract USD 9,781. |
| Pay per click or performance advertising | Yelp, Tripadvisor hotels, Zomato, Nextdoor, Google Local Services Ads | Yelp 2025 advertising USD 1,391.3M, about 95% of net revenue [derived]. Tripadvisor hotel click advertising USD 550.3M. Nextdoor 2025 revenue USD 257.6M, mostly advertising. |
| Pay per lead or contact credit | IndiaMART, Angi, Thumbtack, Clutch, Google LSA, Property Finder | Clutch from USD 25 per lead with a USD 1,000 monthly minimum. Google LSA about USD 53 per lead on average, plumbing 57 [V]. Angi's network leads fell 79% in 2025 after a "homeowner choice" change, while its own-site leads rose 23%. |
| Paid verification or trust badge | IndiaMART TrustSEAL and Verified Exporter, Alibaba.com, Google, Meta Verified | IndiaMART Verified Exporter Rs 1.15 to 6.5 lakh a year. Alibaba Verified about USD 12,500 a year [V]. Meta Verified USD 21.99 a month per page at launch (current price not confirmed). |
| Commission or booking fee | Urban Company, Zomato, Viator, Zocdoc, Zillow Flex | Urban Company revenue about 36% of transaction value [derived], loss-making in Q1 FY27. Viator about 20% of booking value [derived]. Zillow Flex 20% to 40% of agent commission on closed deals. |
| Software bundled for businesses | Thryv, Solocal, Yelp, Zillow, IndiaMART (Busy), Practo | Thryv SaaS revenue USD 461.0M, up 34.2% in 2025 but up only 5% in Q1 2026. Solocal's Connect product fell 15% in 2025. |
| Data licensing and API | Dun & Bradstreet, Yelp, Kompass | Yelp data licensing is small (inside about USD 65M to 75M of "Other" revenue [derived]) but grew above 30% in Q4 2025. |
| Job postings | Glassdoor, Naukri, Craigslist, OLX | Craigslist jobs about 35.6% of estimated revenue (estimates only, not company figures). |

What this note adds to the first one:

- **The free-to-paid pattern is the same everywhere.** About 1.2% of Justdial's listings are paid campaigns and about 2.6% of IndiaMART's storefronts [derived]. Trustpilot is about 2% of its businesses [derived, rough]. Revenue sits in a thin premium tier.
- **Margins are best where the platform is dominant in a local market and sells annual subscriptions to agents and dealers.** Rightmove 70%, OLX 49% EBITDA in H1 FY26, Dubizzle UAE 46%. Commission models earn much less (Practo about 6% [derived]). Margins are company-level, not per stream.
- **Growth now comes from add-ons to an existing audience,** such as messaging, rentals, mortgages, data and AI-answer visibility. Rightmove shifted growth away from raising core prices. IndiaMART's Silver price rise backfired.
- **Pay-for-outcome pricing is rising where the platform can see the outcome** (a booking, a closed sale, a completed job). Subscriptions persist where the outcome happens off the platform (property agents, dealers, small shops).
- **What failed:** print directories (Thryv is selling its print arm for USD 142M), daily deals, consumer subscriptions (Tripadvisor Plus shut after about three years), buying inventory (Zillow Offers), and food delivery for Yelp (Eat24). 
- **Realised revenue per paying customer is low for small-business directories:** about Rs 19,000 a year at Justdial [derived], Rs 67,000 to 69,000 at IndiaMART, against about GBP 18,400 per agency branch at Rightmove [derived]. High-ticket sellers pay more.
- **Gaps:** no platform discloses stream-level margin, churn or revenue by customer size except IndiaMART. No evidence exists on how a contributor-built directory earns in its first two years, or on what Pakistani businesses would pay.

### What the evidence says across the table

- **Largest and most profitable:** advertising and recruiter products at big networks, and enterprise subscriptions in large accounts. Naukri's recruitment segment and Indeed show high margins.
- **High margin, weak stickiness:** pure data subscriptions. ZoomInfo's net retention is below 100%. Definitive's revenue is shrinking. Value comes from keeping customers, not from the cost of the data.
- **Take rates sit in two bands:** about 18% to 19% on open freelance marketplaces, about 28% on Fiverr. They need payments flowing through the platform and enough buyers and sellers. Fiverr's falling buyer count shows demand is not guaranteed.
- **AI-data licensing is real but small:** about 4% to 5% of revenue at Wikimedia and Reddit. It is lumpy and concentrated.
- **Where AI answers replace visits,** traffic-based income erodes. Stack Overflow questions are reported down about 80% in a year [secondary]. Shiksha billings fell 13% in one quarter, which analysts link to AI search (see `Which lists pay.md`).
- **Raw base data is free.** Overture, Foursquare and OpenStreetMap give name, address and coordinates away. Paid products add convenience, verification, freshness and support. This is the strongest lesson for AllLists.
- **Pricing axes data sellers use:** per seat, per credit, per API call with volume tiers, per licence term and scope, and flat enterprise fees. Licences commonly bar resale, include "seed" records for audit and give audit rights. These controls cannot bind the free parts of a list, so restrictions should attach to the verified layer.

### Where the notes are thin

No figure exists for any Pakistani or South Asian buyer. Revenue is not disclosed for Kaggle, Toptal (verified), Foursquare, Mapbox, Crunchbase or Glassdoor alone. `revenue_streams_directories.md` was not in the research folder when this report was written. Directory revenue evidence therefore comes only from `Which lists pay.md`.

### Ranked menu of revenue streams for AllLists

This menu works inside the decisions already made. One adjustment: the research notes put "self-serve export credits" first. The decision log says no download except at a heavy price, so credits here buy delivered outreach, not files.

| Rank | Stream | Status in decisions | Evidence | Timing and risk |
|---|---|---|---|---|
| 1 | Free list pages: first few entries plus statistics, advertisements for free users | Decided (E14, CP5) | Free listings are 97% to 99% of listings at Justdial and IndiaMART. | From day one. Builds the audience everything else needs. Ad prices in our markets unknown. |
| 2 | Paid outreach delivered by the platform: opt-in, per enquiry or in credit packs, contacts hidden | Decided (E13) | Closest to lead pricing: IndiaMART lead Rs 22 to 33 versus US leads USD 39 to 150 (different products). Lead quality is the standing complaint at both Indian platforms. | First paid product. Needs opt-in, delivery proof, and counsel on WhatsApp. |
| 3 | Paid visibility: ranking, badge, extra fields, leads. City level first | Decided (E15, P17) | Revenue sits in a thin top tier. Sell first in high-ticket types in the biggest cities. Do not raise the entry price sharply. | Needs traffic and claimed listings. Pay-to-rank can harm trust, so label it and keep it apart from verification. |
| 4 | Subscription for live access at a low recurring fee | Decided (E7) | Seat evidence is weak: ZoomInfo retention 89%, PitchBook lost small clients. | Test with institutions before individuals. |
| 5 | Depth upcharge: verified owner contact, equipment and priced-service fields | Within E13 and P17 | Foursquare charges 25% to 40% more for richer fields. | Once verified data exists. |
| 6 | Heavy download, about USD 1,000 minimum | Decided (E13) | Only plausible for large verified niche lists: about USD 0.20 a record at 5,000 entries, USD 2 at 500. | Keep as a protective test price. |
| 7 | Institutional and territory licences, statistics to government | Decided (E16) | PitchBook and D&B show the model works in large accounts. No government buyer of contributor-built lists was found. | Year two onward. Aggregate statistics first. |
| 8 | Services: custom research, custom extracts | Not decided | Geofabrik and Definitive show services revenue from data. | Early cash, low scale. Needs a founder decision, see section 6. |
| 9 | Metered API on verified fields | Not decided | Foursquare, OpenCorporates and Mapbox price this way. | Close to bulk access. Not at launch (section 6). |
| 10 | Talent list: seat subscription at the low end (about USD 100 to 250 a month), intro or success fee, sponsored challenges | Not decided | Priced against Juicebox, SeekOut and hireEZ low tiers. Niche AI directories run on sponsors and events. | After a pilot and counsel. |
| 11 | Marketplace listing (AWS, Datarade) | Not decided | AWS fee 3%, Datarade about 30% [unverified]. | Needs a deep audited data set. |
| 12 | AI-data licences and agent access | Not decided | 4% to 5% of revenue at Wikimedia and Reddit. | Upside only. |
| Not early | Transaction take rate; individual premium memberships | Later vision (V1 to V8) | Needs in-platform payments and liquidity. LinkedIn Premium works at huge member counts. | Revisit with payment partners. |

Pharmacies are a useful reminder that who pays matters more than the category. A shop may not pay for a listing, but a distributor may pay for the shop list (see `Which lists pay.md`).

---

## 5) The entry template

### Principle

The proven pattern in schema.org, Google Business Profile and the US NPI registry is a common core plus a set of attributes chosen by the primary category. AllLists should do the same: one primary category per entry and one add-on table per list type.

Only three sources were read for this section (schema.org LocalBusiness properties, Google Business Profile attribute groups, NPPES/NPI fields), all through snippets. Everything else is [inference] from how Practo, Zocdoc, Justdial, Urban Company, IndiaMART and similar platforms are generally understood to work. Before freezing templates, open five real profiles per type and tick off the fields.

### The common core (every entry)

| Group | Fields | Note |
|---|---|---|
| Identity | Stable entry ID (never reused), type (person, business, facility, institution), legal name, display name, alternate names and spellings in Urdu and Roman Urdu, short description, owner type, brand or branch link | Spelling variants drive search. |
| Category | One primary category, up to about five secondary, service tags, list type | Matches the one-primary pattern. |
| Location | Structured address, landmark, coordinates with a precision flag, area-hierarchy IDs, visibility setting (exact, area only, hidden), premises flag (storefront, home-based, mobile) | Home-based providers show area only. |
| Service area | Areas served or radius, remote flag | Essential for trades and tutors. |
| Contact | Primary phone, type (landline, mobile, WhatsApp), email, website, social page, preferred method and hours, visibility (public, on request, via relay) | Decided fields include WhatsApp number and social page. |
| Hours | Weekly hours, 24x7 flag, closures, appointment-only, last confirmed date | |
| Verification | Level (the four decided names), per-field flags, who, how, when, evidence, expiry | Decided in D19 and D20. Per-field flags are our suggestion: a verified name should not lend credibility to a stale price [inference]. |
| Source and provenance | Source type, URL, name, retrieval date, licence or terms, contributor ID, change history | Decided in D17. |
| Consent and rights | Basis for listing, consent time and scope, marketing opt-in, takedown flag | For individuals, confirm adult. |
| Freshness | Created, updated, last verified, next review due | Stale data is the main failure of directories [inference]. |
| Status | Open, temporarily closed, closed, moved; successor link; duplicate link | |
| Claim | Unclaimed, pending, claimed, disputed; plan tier; sponsored flag | Supports revenue streams 3 and 5. |
| Pricing basics | Price band, currency, payment methods | Every price carries currency and date. |
| Reviews | Rating, count, source, verified-contact flag, owner reply | Decided: verified users only (suggested default). Start with claim and verify; add reviews later. |
| Media | Logo, one photo at launch, licence and owner of each image | Gallery later. |
| Identifiers | Registry IDs for the type, tax ID flag | Never publish a national ID number. |

### Add-on fields by list type

"Launch" means cheap to verify, drives the first buyer decision, and has low privacy risk. Everything else waits.

| List type | Launch fields | Later |
|---|---|---|
| Generic local business (bakery, shop, salon) | Products or services tags, payment methods, price band, service options (walk-in, delivery, home visit), company registration number if any | Brands, FAQ, offers, staff size |
| Doctors | Name, regulator and registration number, licence status, qualifications, specialty, practice locations with days and times, consultation fee with date, languages, gender | Conditions treated, publications, insurance panels, telemedicine, booking links |
| Hospitals, clinics, eye hospitals | Facility type, ownership, healthcare commission licence number and validity, departments and sub-specialty centres, 24x7 emergency flag, OPD hours, insurance and panel list, key equipment (for eye care: OCT, phaco, laser) | Bed counts, accreditation documents, price lists, charity programmes |
| Diagnostics and MRI centres | Modalities, equipment make, model and field strength, radiation licence, price list for the top 10 to 20 tests with date, turnaround, referral requirement, hours | Package prices, radiologist roster, report portal, downtime notices |
| Tradespeople | Trade, service area, visit charge and 3 to 5 priced services, years of experience, availability, ID-verified flag, contact through relay | Certifications, tools, warranty, before and after photos, references |
| Contractors | Entity type, PEC number and category, fields of work, work types, three past projects with proof, key equipment, tax-filer status | Bonding and financial bands, safety record, key personnel, complaint history |
| Schools and tutors | Entity type, grades or subjects, board or curriculum, fees with year, mode (online, home, centre), gender served and tutor gender, safeguarding check status for child-facing tutors, registration or recognition | Results, facilities, admissions detail, demo videos, parent reviews |
| Talent (data scientists) | Role, skills with years, portfolio links (GitHub, Kaggle, ORCID), engagement type, rate band, availability, languages, location and time zone | Publications, certification IDs, visa status, references |
| Manufacturers and suppliers | Business type, products and categories, minimum order, capacity band, certifications, export markets, tax IDs, factory address | Price lists, lead times, OEM details, turnover band, references |
| Petrol pumps, pharmacies, retail | Hours with 24x7 flag, brand, services or fuel types, payment methods; pharmacy: drug licence number and pharmacist in charge | Live fuel or stock information, delivery, loyalty, calibration seal date |

The founder's own examples ride on these: equipment and priced services (decision C21) sit in the hospital and diagnostics rows, and skill-based individuals (C22, C23) in the tradespeople and tutor rows.

### Prices are the best field and the worst

Priced services carry the highest buyer value in diagnostics, trades, hospitals and tutoring. They also go stale fastest. Chughtai Lab shows a list price and a discounted price for the same test, so an entry needs both, plus an "as of" date. Health rules to adopt (hypotheses, not legal advice, from `Which lists pay.md`): show each facility's own published price with source and date, avoid "cheapest" claims, label paid placement, never imply a licence unless a licence record was seen, and hold no patient data.

### Sensitive fields

| Field | Risk | Suggested handling |
|---|---|---|
| Personal mobile numbers of individuals | Spam, harassment, deletion rights in many countries. Pakistan has no general law yet. | Collect with consent. Show through relay or click-to-reveal. Never publish scraped personal mobiles. Fits the decided hidden-contacts rule. |
| Home address of an individual | Stalking and burglary, especially for women and tutors | Area only. Exact address private. |
| National ID (CNIC) and passport | Identity theft | Store a "checked" flag and date, not the number. If a copy is unavoidable, encrypt it, log access and delete it after the check. |
| Anything about children, and tutors who teach children | Safeguarding, consent, defamation if an unproven accusation appears | Verified safeguarding check status, relay-only contact, no child data on public pages, moderation and a takedown route. |
| Online Quran tutors | Cross-border contact with minors, fake credentials, prepaid-fee fraud | Level-gated verification, trial lesson, platform relay, report button. Flag unverified ijazah. |
| Health data | Special-category data. Patient reviews can reveal conditions. | No patient-level data. Clean reviews. No patient photos without written consent. |
| Doctor complaint records | Defamation | Link only to official public decisions, with source and date. |
| Police or character certificates | Criminal-record data | Hold a pass or fail flag and date only. |
| Talent salary, nationality, visa, age, religion | Discrimination law and privacy | Optional, private by default, not searchable. |
| Customer reviewer identity | Personal data of reviewers | Use pseudonyms, allow owner reply, keep a takedown procedure. |
| Business financials | Commercial confidentiality | Show as bands with consent. |
| Scraped Google, Yelp, LinkedIn, Facebook fields | Terms and database rights | Do not import. Use registries and owner submissions. Already the suggested default for Q-P4. |

Counsel is needed before storing health, child, ID or character-check data.

---

## 6) Recommendations and decisions needed

### Recommendations

1. **Source organisations from registers, and individuals from consent.** Use registers to verify and badge records. Do not scrape PMDC, SECP or any portal.
2. **Start with eye care in one city.** It matches your examples, it has real sources (hospital sites, OSP, PHC, PMDC), and no eye hospital directory exists. Add schools next for traffic. Add contractors from PEC.
3. **Make housing-society partnerships the route for local trades.** One society, one trade, opt-in.
4. **Adopt one taxonomy design now:** Overture plus an AllLists layer for individuals and informal trades, an alias table (Urdu, Roman Urdu, regional words), and crosswalk codes to ISIC and ISCO.
5. **Build the talent list as consent-based, after a pilot.** Never harvest.
6. **Price in the verified layer.** Free base data sets the floor near zero, so charge for confirmation, freshness, delivered outreach and visibility.
7. **Test before building more.** The pre-sell experiments in `Which lists pay.md` still apply. Add one test for this report: measure the cost of a verified entry in eye care.

### Decisions for the founder

Items already settled are not repeated. These are new or still open. Items marked "Open already" are in the decision log's open table and are listed here only with guidance.

| # | Decision | Suggested default |
|---|---|---|
| 1 | Pilot city and first source pack | One city. Eye hospitals and eye doctors first, then schools, then contractors. Pakistan first, as already suggested. |
| 2 | Use of registers (Open already, Q-S3) | Use registers to verify records someone nominated and to show a badge. Email each body for written terms before any bulk use. Start with facility and school registers, not individuals. |
| 3 | Named individuals (doctors, lawyers, tradespeople, tutors) | Only with the person's own consent. Contact through relay. Area only, no home address. Firms first. |
| 4 | Housing society partnership terms | A pilot with one society. The society sends an opt-in link and gets a branded list. No fee, no recruitment commission (matches the suggested stewardship default). |
| 5 | Taxonomy base | Adopt the Overture-plus-local-layer design. Confirm licences from primary pages first. |
| 6 | Natural scale per list type | Use the inventory scale as a starting label. Review with the first contributors. |
| 7 | Child-facing tutors and Quran tutors | Not published publicly until a safeguarding check and relay-only contact are designed. Schools and centres can go first. |
| 8 | Talent list timing | Design now. Launch after a pilot of about 50 consented data scientists and counsel review. Seat price near USD 100 to 250 a month and an intro-fee option, to be tested. |
| 9 | API and custom extracts | No API at launch, because it sits close to the no-download rule. Allow custom research for institutions case by case, priced like the download. |
| 10 | Prices and health policy | Adopt the health rules in section 5 before collecting any price. |
| 11 | Counsel | Book counsel for Pakistan and the Gulf before any messaging test, any list of individuals, any health or child data, and the talent list (EU, UK, California exposure from day one). |

---

## 7) What is unverified and how to verify

### Why the gaps exist

The official sites were blocked in the research environment. For Pakistan this included pmdc.pk, secp.gov.pk, fbr.gov.pk, os.phc.org.pk, pnra.org, dra.gov.pk and pakistanbarcouncil.org. Elsewhere it included unstats.un.org, docs.overturemaps.org, isco.ilo.org and most filings and platform terms pages. So terms of use, fields, counts and bulk-access routes are mostly unknown.

### What to check, in order

1. **Open the pages from an unblocked connection.** Confirm what each portal shows, whether it lists records or only looks up one, and what its terms say about copying.
2. **Re-check the figures used in this report.** In particular, PMDC's 366,443, PHC's 64,000 and 41,000, KP's 23,041, Sindh's 14,000, HEC's 179 and the PEC category limits (2017 mirror). Also the platform figures that came from filings seen only in summaries.
3. **Sample five live listings per list type** and tick off the template fields. Drop fields nobody fills.
4. **Read the full terms** of ORCID, OpenAlex, GitHub, Kaggle, Hugging Face and Semantic Scholar before any commercial use.
5. **Confirm taxonomy licences** (Overture taxonomy file, Foursquare categories, ISIC, ISCO) and Urdu label coverage.
6. **Get counsel** on the points above.

### Bodies to email

Ask each for written terms, field list, update frequency and a bulk or partnership route. Offer the verified-status badge as the value we give back.

| Body | Ask |
|---|---|
| Pakistan Medical and Dental Council | Whether specialty is shown, any export or data-sharing route, terms of use |
| Punjab Healthcare Commission | Fields in the licence verify page, a browse view, bulk or partnership access |
| KP Health Care Commission, Sindh Healthcare Commission, Islamabad Healthcare Regulatory Authority, Balochistan Healthcare Commission | Whether any public list exists |
| Ophthalmological Society of Pakistan (and branches) | Member directory use with member consent |
| PEIRA, PITB (PEPRIS), provincial education departments | School list access and terms |
| Higher Education Commission | List reuse terms |
| Pakistan Engineering Council | Whether a public searchable constructor register exists, current categories and limits |
| PPRA (EPADS) | Whether supplier registers or award notices are public |
| NAVTTC and TEVTA | Certificate verification, any public list of certified workers |
| DRAP and provincial drug control | Whether licensed pharmacy lists are public |
| PNRA | Format and contents of licensed radiation facility lists |
| TDAP | Status and reuse terms of the exporters directory |
| Pakistan Bar Council, ICAP, ICMAP | Member directory use and consent routes |
| SECP | Written terms for manual look-ups and any licensed data route |
| Chambers (FPCCI, LCCI, KCCI, RCCI) and trade associations, ABAD | Partnership and member directory terms. These were not researched in depth. |
| Housing society managements | Pilot partnership |
| Other countries: Brazil Ministry of Health (DATASUS), KMPDC, NCA Kenya, Dubai Municipality, Saudi Contractors Authority, India's National Medical Commission, Indonesia's Ministry of Health | CNES and register licence and terms, data formats, fields and update frequency |

### Still not researched at all

- Schools, lawyers and accountants in countries other than Pakistan.
- Trade and skills registers outside Pakistan.
- Chamber and business-registry terms in most countries.
- Personal-data rules in the Gulf, Nigeria, Kenya, Bangladesh, Indonesia, Brazil and others.
- Any Pakistan-specific buyer price for any list (see `Which lists pay.md`).
