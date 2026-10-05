# Pakistan: official registries, regulators and bodies that identify service providers (research as of 2026-10-05)

Method note: built from web-search result summaries only. Direct page fetches of pmdc.pk, secp.gov.pk, fbr.gov.pk, os.phc.org.pk, pnra.org, dra.gov.pk and pakistanbarcouncil.org were blocked by the network proxy (EGRESS_BLOCKED), so portal fields, terms of use and live record counts could NOT be verified first-hand. Anything marked [UNVERIFIED] rests on a search snippet or secondary source. Planning research, not legal advice.

## Doctors and dentists: PMDC, CPSP, specialist (ophthalmology) registries

### Takeaway
PMDC is the statutory register for doctors and dentists and offers a public online search, but no bulk download or reuse licence was found, and the one count I found is undated. No national "ophthalmologist register" exists apart from PMDC specialty entries and the Ophthalmological Society of Pakistan (OSP, a voluntary society of about 2,000).

### Cited Findings
- A search summary of PMDC's site reports 366,443 registered practitioners (325,523 medical, 40,920 dental; 161,800 male and 163,723 female medical; 12,782 male and 28,138 female dental). The date of this count was not shown, so treat it as [UNVERIFIED] and undated. — [PMDC](https://pmdc.pk/)
- PMDC provides an online search where a practitioner can be looked up by registration number, full name or father's name, showing licence validity and registered qualifications. This is a lookup of single records, not a documented export. — [PMDC](https://pmdc.pk/)
- A news report says doctors and dentists were given six months to renew PMDC registrations (date and detail not verified). — [The News](https://www.thenews.pk/print/1431533-doctors-dentists-given-six-months-to-renew-pmdc-registrations)
- PMDC homepage carried a notice about "Unrecognized Postgraduate Programs in Medicine & Dentistry", showing PMDC also tracks recognised postgraduate qualifications. — [PMDC](https://pmdc.pk/)
- CPSP (College of Physicians and Surgeons Pakistan) accredits FCPS and MCPS ophthalmology programmes (4-year FCPS/MS; 2-year MCPS/DOMS) at institutions such as SIOVS Hyderabad, Al-Shifa Rawalpindi and Dow Karachi. — [SIOVS prospectus 2026](https://siovs.edu.pk/wp-content/uploads/2026/05/UPDATED-PG-PROSPECTUS-2026.pdf); [Al-Shifa](https://pio.alshifaeye.org/pgt-for-doctors.php)
- The Ophthalmological Society of Pakistan describes itself as having grown to 2,000 qualified ophthalmologists, 13 branches and six subspecialty associations; OSP Lahore has 500+ members and a members page. — [OSP/APAO](https://apaophth.org/?p=644); [OSP Lahore members](https://osplhr.org/osp-lahore/members.html)
- Pakistan Bureau of Statistics has hosted a PDF "Registered Dental Doctor" (2020) — probably aggregate statistics; not examined. — [PBS](https://www.pbs.gov.pk/wp-content/uploads/2020/07/Registered_Dental_Doctor.pdf)

### Inferences
- PMDC name search is suitable for verifying a doctor someone else nominates, or for per-record badges ("PMDC-verified"), not for scraping 366k records; scraping would likely breach site terms (cf. SECP's reaction to scraping below) and involves personal data (name, father's name).
- An "eye doctors" list is best seeded from hospital websites, OSP branch member pages (with permission) and CPSP-accredited training institutions, then verified against PMDC.

### Gaps
- Whether PMDC publishes specialty (ophthalmology) fields in search results, a CSV export, an API, or terms of use: not verified (site blocked).
- Date and methodology of the 366,443 figure.
- CPSP public fellow directory: not found in search; existence unknown.

## Hospitals, clinics, labs, diagnostic centres, pharmacies (healthcare commissions, DRAP, PNRA, IHRA)

### Takeaway
Each province has its own healthcare commission with registration/licensing, but only Punjab (PHC) clearly offers public licence verification and a dashboard; others are partial. Counts of registered facilities are large (Punjab 64k registered, KP about 23k, Sindh about 14k), but licensed totals are much smaller, so "registered" does not mean "inspected and licensed".

### Cited Findings
- Punjab Healthcare Commission (PHC), under the PHC Act 2010, requires all public and private healthcare establishments (allopathic, homeopathic, tibb) to be licensed. Its HCE portal has a licence-number verify page (service to enquire details of a Regular License by number). — [PHC licensing intro](https://os.phc.org.pk/licensingIntro.aspx); [PHC verify](https://os.phc.org.pk/verify.aspx)
- PHC has registered more than 64,000 and licensed over 41,000 healthcare establishments (date not stated in the snippet; [UNVERIFIED] on date). — [Gallup Pakistan PHC dashboard](https://galluppakistandigitalanalytics.com/punjab-healthcare-commission/)
- A third-party "PHC Intelligence Dashboard" (by Gallup Pakistan Digital Analytics) presents facility distribution, licensing status and compliance patterns; unclear whether it is official or what its terms are. — [Gallup dashboard](https://galluppakistandigitalanalytics.com/punjab-healthcare-commission/)
- PHC inspections reportedly passed 18,500 visits, near completion of allopathic HCE coverage (APP report; date not verified). — [APP](https://www.app.com.pk/?p=1201227)
- Sindh Healthcare Commission (SHCC): director said about 100,000 facilities exist, about 14,000 registered, 1,200 on temporary licences, 113 with permanent licences (undated in snippet); another snippet says 132 licensed hospitals; 650 provisional licences; Jan-Jun 2023: 477 registration certificates, 54 provisional, 11 regular. Dawn reported only 3 government and 86 private facilities registered in seven years (older). — [Dawn](https://www.dawn.com/news/amp/1926771); [Business Recorder](https://www.brecorder.com/news/amp/40130061); [Express Tribune, 19 Jul 2026](https://tribune.com.pk/story/2619029/cracks-in-care-healthcentres-fail-shcc-inspections)
- KP Health Care Commission registered 19,612 HCEs April 2022 to April 2025; a later report says 2,574 more in the year for a total of 23,041; since licensing began in 2023, 685 evaluated and 271 given full licences; 5,696 illegal facilities sealed. — [APP](https://www.app.com.pk/?p=982203); [TNN](https://tnnenglish.com/annual-report-shows-sharp-rise-in-crackdown-on-illegal-healthcare-facilities-in-kp)
- Balochistan Healthcare Commission Act was enacted in 2019, covering all public and private healthcare establishments; no registered/licensed count found. — [Balochistan Health Dept PDF](https://health.balochistan.gov.pk/wp-content/uploads/2025/03/2019-2.pdf)
- Islamabad Healthcare Regulatory Authority (IHRA): as of Sept 2021 processed 1,482 establishments, 642 applications, 354 provisionally registered; later notices said no unlicensed facility allowed after June 2022. Current counts not found. — [ProPakistani](https://propakistani.pk/2021/09/20/islamabads-non-licensed-healthcare-facilities-to-be-suspended/); [IHRA](https://ihra.gov.pk/?p=645)
- Sindh and Punjab commissions agreed to collaborate on service delivery systems (news). — [Business Recorder](https://www.brecorder.com/news/amp/40130061)
- DRAP: oversees about 1,380 therapeutic goods manufacturers and about 2,500 importers and distributors; DRAP website has "List of Pharmaceutical Units" and "Registered Drugs Index". Section 14 of the Drugs Act 1976 requires a licence to sell or stock drugs, issued by DRAP or the provincial health department. Retail pharmacy licences are therefore a provincial drug-control matter, and I found no national public list of licensed pharmacies. — [DRAP](https://www.dra.gov.pk/?p=1094); [Wikipedia: DRAP](https://en.wikipedia.org/wiki/Drug_Regulatory_Authority_of_Pakistan)
- PNRA (Pakistan Nuclear Regulatory Authority) regulates radiology, radiotherapy and nuclear medicine, and its site links to lists of licensed X-ray facilities, medical radiation facilities and industrial radiation facilities; total X-ray centre counts not found. Pakistan has 51 nuclear medicine facilities and 49 oncology centres (a CISS journal article). — [PNRA](https://pnra.org/r-safety.html); [CISS](https://www.journal.ciss.org.pk/index.php/ciss-insight/article/download/409/284)
- Open data: opendata.com.pk hosts "Pakistan Health Sites" (name, nature of facility, activities, lat/long; CSV/ZIP), "Pakistan Health Facilities" (government facilities), and PBS "Public health facilities in Pakistan 2021". These are mostly public-sector facilities. — [Pakistan Health Sites](https://opendata.com.pk/dataset/pakistan-health-sites); [Public health facilities 2021](https://opendata.com.pk/dataset/public-health-facilities-in-pakistan-2021)

### Inferences
- Best starting list for "hospitals/clinics/labs" is PHC (Punjab) because licences are verifiable by number; combine with Google Places or hospital sites for addresses, then use PHC as a trust badge.
- Pharmacies and diagnostic centres: no single national register; expect provincial drug inspectorates and per-province healthcare commissions, plus PNRA for X-ray/CT, to be the verification layer rather than a source of bulk lists.
- Gap between registered and licensed counts means "PHC-licensed" is a meaningful quality filter.

### Gaps
- Fields available in PHC verify results, and whether the HCE portal has a browse/list view: not verified (blocked).
- Whether SHCC, KP HCC, BHCC, IHRA publish searchable lists: not found.
- Any dedicated "eye hospitals directory": not found (a gap, and a possible opportunity).
- PNRA list formats and contents: not verified.
- Dates of several counts (PHC 64k/41k, SHCC 14k/113).

## Contractors and engineers (PEC, PPRA, development authorities, ABAD)

### Takeaway
PEC registration is the legal gate for constructors (C-A to C-6) and is widely demanded in tenders; PPRA's EPADS has about 51,000 registered suppliers but is a procurement system, not an open directory. Public searchable contractor lists were not confirmed.

### Cited Findings
- PEC constructor categories and cost limits (from a PEC policy document copy): C-A no limit; C-B up to Rs 3,000m; C-1 up to Rs 1,800m; C-2 Rs 800m; C-3 Rs 400m; C-4 Rs 150m; C-5 Rs 50m; C-6 Rs 20m. Limits are from an older policy (2017 version); may have been revised. — [PEC registration policy 2017 (mirror)](https://n.gst.elementfx.com/dl/registration-policy-2017)
- PEC registered about 1,755 consulting engineers, constructors (figure garbled in source, appears as "7,6251") and 840 operators up to June 2016; roughly 260,000 engineers registered (2016 PEC facts sheet). Both are old; current counts not found. — [Times of Islamabad](https://timesofislamabad.com/19-07-2016/engineers-in-pakistan-pec-facts-and-data-sheet/)
- PEC is the regulator for registration of engineers, contractors and construction companies, and issues no NOC to unregistered companies. — [Graana](https://www.graana.com/blog/a-complete-guide-to-register-a-construction-company-in-pakistan/)
- CDA published a PDF list of contractors (Nov 2012 file name "cdacontractors112012"), showing authorities publish enlistment lists at least occasionally. — [CDA PDF](https://www.cda.gov.pk/Assets/pdf/cdacontractors112012.pdf)
- PPRA e-PADS: free supplier registration; as of FY2024-25 more than 10,000 public agencies and 51,000 suppliers registered; EPADS 2.0 launching with beneficial-ownership verification. — [ADB event material PDF](https://events.development.asia/system/files/materials/2024/09/202409-e-government-procurement-system-e-pak-acquisition-disposal-system-e-pads.pdf); [PhoneWorld](https://www.phoneworld.com.pk/ppra-to-launch-epads-2-0-under-the-vision-of-one-nation-one-system/)
- ABAD (Association of Builders and Developers) formed 1972, affiliated with FPCCI, reported 1,000+ members in 2017. — [Aurora/Dawn](https://aurora.dawn.com/news/1141718); [DevelopmentAid](https://www.developmentaid.org/organizations/view/35859/abad)
- Other contractor bodies exist (Pakistan Contractors Association, Constructors Association of Pakistan, All Pakistan Contractors Association); membership numbers not found. — [Profit](https://profit.pakistantoday.com.pk/?p=51585)

### Inferences
- National contractor list: PEC register (if its online verification supports category/name queries), supplemented by tender award notices (published on EPADS/PPRA, and university/authority PDFs listing enlisted firms). A "contractors at national level" list would at first be PEC category by city, with source/date shown per row.
- CDA/RDA/LDA/PHA lists are scattered PDFs; scrape-and-date approach, or request.

### Gaps
- Whether PEC has a public online searchable constructor register, URL, fields, and current count: search did not surface it; not verified.
- Pakistan Housing Authority, RDA, LDA lists: not found.
- PPRA supplier register public visibility: not confirmed (likely login-gated).

## Skilled trades (NAVTTC, TEVTA, PSDF, Hunarmand, local registers)

### Takeaway
No public national register of individual plumbers, electricians or welders was found. NAVTTC certifies through accredited trade testing centres and licenses assessors, but individual certificates are not published as a directory. Training-programme graduate numbers exist but are held by programmes and are personal data.

### Cited Findings
- NAVTTC runs skills testing through Trade Testing Centres (TTCs), has begun registering TTCs to curb fake certification, and links to the National Vocational Qualification Framework (NVQF). National Assessors are licensed for trades including masonry, steel fixing, painting, tiling, electrician, AC/refrigeration, solar technician, pipe fitter. — [NAVTTC](https://nap.navttc.gov.pk/); [PID](https://pid.gov.pk/site/press_detail/14590)
- TEVTA Punjab: about 220,000 students trained per year in 403 institutes; 590,433 trained 2014-18 (World Bank / Punjab govt sources). Hunarmand Nojawan targets 100,000 additional students a year. — [Punjab ICID](https://icid.punjab.gov.pk/node/71); [World Bank](https://www.worldbank.org/en/results/2018/10/26/pakistan-providing-employable-skills-to-youth-in-punjab-province)
- Punjab Skills Development Programme trained 16,000 graduates July 2015 to August 2018. — [World Bank](https://www.worldbank.org/en/results/2018/10/26/pakistan-providing-employable-skills-to-youth-in-punjab-province)
- Punjab Apprenticeship Act 2021 was launched via TEVTA. — [Punjab govt](https://punjab.gov.pk/node/4465)

### Inferences
- Tradespeople are mostly informal; the credible source for "plumbers in a housing society" is society management, resident referrals and the tradespeople themselves (opt-in, with phone), not a state register. NAVTTC/TEVTA credentials can be an optional self-declared badge verified by certificate number.

### Gaps
- NAVTTC certificate verification portal and any public list of certified workers: not found.
- Overseas Employment Promoters / Protectors of Emigrants lists (a licensed-recruiter register exists in principle): not researched.
- Union council registers of tradespeople: nothing found.

## Lawyers and accountants (bar councils, ICAP, ICMAP, FBR)

### Takeaway
Bar councils maintain rolls (PBC for Supreme Court advocates; provincial councils for others) and some publish PDF lists; ICAP has a member directory; FBR tax practitioners are registered but I found no public list.

### Cited Findings
- Pakistan Bar Council (Legal Practitioners and Bar Councils Act 1973) admits and maintains the roll of Advocates of the Supreme Court, and its site lists "Details of practicing Advocates of Supreme Court" and applications. — [PBC enrolment](https://pakistanbarcouncil.org/enrolment/); [PBC about](https://pakistanbarcouncil.org/about-us/)
- KP Bar Council posts per-district PDF voter lists (advocates lists for bar elections). — [KPBC PDF example](https://kpbarcouncil.com/site/Downloads/a-web-voterlist-folder/SADDA11.pdf)
- ICAP had 10,096 members in 2024 per one source (another snippet says 11,285 active members); it maintains a members directory. — [Wikipedia: ICAP](https://en.wikipedia.org/wiki/Institute_of_Chartered_Accountants_of_Pakistan); [ICAP](https://icap.org.pk/about/who-we-are/)
- ICMAP has over 7,000 members; HQ in Karachi. — [Wikipedia: ICMAP](https://en.wikipedia.org/wiki/Institute_of_Cost_and_Management_Accountants_of_Pakistan)
- Under Section 223 of the Income Tax Ordinance 2001 and Rule 85 of the Income Tax Rules 2002, income tax practitioners enrol with the FBR (application to the Chief Commissioner, RTO). — [ETTC](https://ettc.pk/how-to-become-a-tax-consultant-in-pakistan/); [PKRevenue](https://pkrevenue.com/fbr-unveils-procedure-for-tax-practitioner-registration-in-ty2024/)

### Inferences
- Voter-list PDFs may carry names, enrolment numbers and addresses of individuals; they were published for election purposes, so reuse in a commercial directory is questionable.
- Lawyers and accountants lists are better built opt-in with bar-card or member number verified.

### Gaps
- Total advocate counts (national or provincial): not found.
- Searchable online rolls at Punjab, Sindh, Balochistan bar councils: not found.
- FBR public tax practitioner list: not found.

## Education (provincial registries, PEIRA, HEC, madrasa boards)

### Takeaway
Education is the best-documented sector: PEIRA publishes searchable lists of registered private schools in Islamabad, PEPRIS (PITB) holds Punjab private school registrations, HEC lists recognised universities, and national statistics give totals.

### Cited Findings
- PEIRA regulates private educational institutions in ICT up to higher secondary; its PSMS portal exposes paginated public reports "registered PEIs" and "unregistered PEIs". — [PEIRA](https://www.peira.gov.pk/); [PSMS registered list](https://psms.peira.gov.pk/admin/rpt_registered_peis.php?page=2)
- Punjab: PEPRIS (Private Education Provider Registration and Information System), built by PITB for the School Education Department, launched November 2020; more than 86,000 institutes registered. Public lookup availability not confirmed. — [PITB](https://pitb.gov.pk/node/7552)
- KP ordered action against hundreds of private schools (30 Jul 2026), indicating KP registration enforcement. — [ProPakistani](https://propakistani.pk/2026/07/30/kp-orders-action-against-hundreds-of-private-schools/)
- Pakistan Education Statistics 2023-24: 203,411 institutions, of which 60,904 are private (about 30%); institutions fell 2.10% from 2022-23. Published by the Pakistan Institute of Education (NEMIS/AEPAM). — [State of Children summary](https://stateofchildren.com/pakistan-education-statistics-2023-24/)
- HEC recognises 179 degree-awarding public and private universities and lists campuses (147: 95 public, 52 private); the page is public. Counts are from a search summary, date not shown. — [HEC campuses](https://www.hec.gov.pk/english/universities/Pages/DAIs/HEC-recognized-Campuses.aspx)
- Madrasas: 18,600 registered under the Directorate General of Religious Education (an earlier count was 9,667); estimated 35,000 seminaries nationally; 10 of 15 boards registered with DGRE, and five (Ittehad-e-Tanzeemat-e-Madaris Pakistan, ITMP) register under the Societies Registration Act 1860. Counts vary by source and date. — [Nukta](https://nukta.com/pakistan-president-to-issue-ordinance-to-give-legal-cover-to-over-18000-madrassas); [ISSRA](https://issra.pk/insight/2025/Madrassah-Education-in-Pakistan/insight.html); [Dawn](https://www.dawn.com/news/amp/1622943)

### Inferences
- Schools: seed from PEIRA (Islamabad, public pages) and PEPRIS/NEMIS where accessible; school data are institutional (low personal-data risk).
- Tutors and Quran teachers are informal; no register found.

### Gaps
- Sindh, KP, Balochistan school directories; Punjab School Education Department school list (SIS/PEPRIS) openness: not verified.
- PEIRA terms of use: not verified.
- Quran teaching/tutoring bodies: none found.

## Business and trade (SECP, FBR ATL, SMEDA, TDAP, chambers, trade associations)

### Takeaway
SECP's registry is public for lookups but SECP treats bulk extraction as unauthorised and sells certified data; FBR's Active Taxpayer List is a downloadable public file but is personal/tax data of individuals; TDAP has an exporters directory.

### Cited Findings
- SECP eServices offers free basic company search (name or registration number) without sign-up, showing status, registered address and usually directors. — [Business Data Guide](https://businessdataguide.com/blog/jurisdictions/pakistan-company-search-guide); [LemReveal](https://lemreveal.com/how-to/is-registry-free/pakistan)
- In 2024 SECP said company registry is public information available on payment of fees; after a web-scraping incident, it restricted XML tags, tightened API protection, temporarily suspended company-name search, and said it would pursue legal recourse against those involved; data fields are available under Form-A and Form-29 for a fee. — [SECP](https://www.secp.gov.pk/?p=45425); [Mettis](https://mettisglobal.news/Company-registry-represents-public-information,-SECP-clarifies); [Profit, 24 Mar 2024](https://profit.pakistantoday.com.pk/2024/03/24/secp-data-scrape-is-there-a-silver-lining)
- FBR publishes an Active Taxpayer List as downloadable Excel on fbr.gov.pk, reportedly updated weekly (Mondays) and published annually 1 March; one snippet says it was updated 26 Feb 2026. Fields reported to include names of individuals, companies and AOPs; exact columns not verified. — [FBR ATL](https://www.fbr.gov.pk/download-atl/132041); [ETTC](https://ettc.pk/check-fbr-active-taxpayer-list-atl/)
- TDAP's Pakistan Exporters' Directory (launched 2017; www.pakistanexportersdirectory.gov.pk) searches by HS code, product category and company name. Current status and size not verified. — [ProPakistani](https://propakistani.pk/2017/05/31/online-directory-pakistani-exporters-launched-help-foreign-customers/)
- SMEDA operates an SME Registration Portal (SMERP) and offers free MSME registration; no public member directory found. — [The News](https://www.thenews.pk/print/1424980-smeda-offers-free-registration-for-msmes)
- KCCI had about 17,000 direct members as of 2019; no public member directory found in search. — [Wikipedia: KCCI](https://en.wikipedia.org/wiki/Karachi_Chamber_of_Commerce_%26_Industry)

### Inferences
- SECP: use manual or fee-based/certified access, not scraping, for company lists; companies are a poor proxy for plumbers but fine for contractors, schools run as companies, and pharma distributors.
- FBR ATL: legal to read as published; but taxpayers' CNIC-linked names are personal data. Use only to confirm tax-filer status of a business a user nominates.
- Chambers/trade associations: approach via partnership; they hold members' phones and addresses.

### Gaps
- Chamber directories (FPCCI, LCCI, RCCI, ICCI) and trade associations (petroleum dealers, pharmacists, hoteliers, mobile traders, bakers): not researched in depth; existence and access terms unknown.
- ATL columns and licence/terms of reuse: not verified.

## Housing societies, union councils, data protection and partnering

### Takeaway
Housing societies keep their own vendor/contractor registrations (DHA enlists contractors and suppliers), but I found no public directory of tradespeople; a society manager is the natural partner. Pakistan still has no comprehensive data protection law.

### Cited Findings
- DHA invites contractors registered with PEC and DHA (C-5 and above) and opened vendor/supplier registration (e.g., DHA Quetta), requiring a business licence, tax registration and experience statement; scope includes electrical and plumbing supplies and maintenance services. — [Zameen: DHA Quetta vendor registration](https://www.zameen.com/news/dha-quetta-opens-vendors-suppliers-registration.html)
- Bahria Town Phase schemes are listed with CDA (planning-level information only); no vendor register found. — [CDA](https://cda.gov.pk/housing-schemes/bahria-town-phase-iiiiiv-vi)
- Pakistan has no enacted comprehensive data protection law as of May 2026; the Personal Data Protection Bill/Act 2025 remains a draft (approval delayed March 2025); the Prevention of Electronic Crimes Act 2016 (amended 2025) applies. — [DLA Piper](https://www.dlapiperdataprotection.com/?c=PK); [ARY News](https://arynews.tv/tag/pakistan-it-ministry/)

### Inferences
- A society's manager or welfare committee already holds the best local data (who fixed which house, phone numbers, gate-pass lists); partnership model: society sends an opt-in link to residents/tradespeople, AllLists adds a verified badge, society gets a branded list.
- The draft law's consent-based approach suggests collecting consent and a removal route from the start.

### Gaps
- Bankers Society, Askari, Gulberg, Bahria vendor-registration practices: not found.
- Union council records of tradespeople: nothing found.
- Terms of use for all the above portals: not verified.

## Conclusion: ranked usable sources and bootstrap plan

### Takeaway
The easiest legitimate lists are facilities and institutions (hospitals via PHC, private schools via PEIRA/PEPRIS, universities via HEC), then contractors via PEC, while individual tradespeople must come from opt-in and housing-society partnerships rather than registers.

### Cited Findings
(Ranking is my judgement from the findings above; counts and access as cited in earlier sections.)

| Rank | Source | Public? | Access | Approx. size | Reuse risk | Best first use |
|---|---|---|---|---|---|---|
| 1 | PHC Punjab licence verification (os.phc.org.pk) | Public lookup | Per-licence verify; bulk unclear | >64k registered / >41k licensed [undated] | Medium (check terms) | Verify hospitals/clinics/labs |
| 2 | PEIRA PSMS lists (Islamabad) | Public pages | Browsable pages | Not counted | Low (institutions) | Schools in ICT |
| 3 | HEC recognised universities | Public | List page | 179 universities | Low | Universities |
| 4 | PMDC search | Public lookup | Single-record search | 366k [undated] | Medium-high (personal data) | Verify doctors |
| 5 | PEC register | Not confirmed | Not confirmed | Old 2016 counts only | Medium | Contractors by category |
| 6 | opendata.com.pk health sites | Public | CSV | Public facilities | Low | Government hospitals/BHUs |
| 7 | KP HCC / SHCC / IHRA | Partial | Reports, news | 23k / 14k / small | Medium | Cross-check only |
| 8 | NEMIS/Pakistan Education Statistics | Public | Reports | 60,904 private institutions | Low | Market sizing |
| 9 | FBR ATL | Public download | Excel | Not counted | High (personal tax data) | Verification only |
| 10 | SECP | Public lookup, fee for data | Scraping treated as unauthorised | Not counted | High | Manual lookups only |

### Inferences
Suggested order of building:
1. Eye hospitals and eye doctors (pilot city): start from OSP branch pages, hospital websites and PHC verification; badge "PHC licensed" and "PMDC verified"; no eye hospitals directory was found, so it is a clear gap to fill.
2. Schools: Islamabad from PEIRA, Punjab via PEPRIS if public, plus HEC universities.
3. Contractors: PEC categories C-A to C-6, validated against tender award notices and DHA-style enlistments.
4. Hospitals, labs, diagnostic centres by province using healthcare commission data; pharmacies and radiology via drug inspector and PNRA licensing as verification layers.
5. Plumbers, electricians, AC technicians: opt-in via housing society partners; optional NAVTTC/TEVTA certificate badge.
Approach every body through a formal data-sharing or partnership request; do not scrape SECP, PMDC or portals without written permission.

### Gaps
- Terms of use, fields and bulk-access routes for nearly every portal could not be verified because official sites were blocked; a manual review of each site (and a written enquiry to PHC, PEIRA, PEC, PMDC) is the first next step.
- Chambers, trade associations, union councils, tutoring and Quran teaching bodies, and overseas employment promoters remain unresearched or unfound.
