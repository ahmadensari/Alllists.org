# Official registers of service providers in AllLists's other priority markets (UAE, Saudi Arabia, Turkey, Egypt, Nigeria, Kenya, Bangladesh, Indonesia, Brazil, Philippines; India as benchmark)

Research date: 2026-10-05. Method note: only WebSearch snippets were usable. Every WebFetch to official sites (bmdc.org.bd, nca.go.ke, kmpdc.go.ke, en.prothomalo.com, capitalfm.africa) was blocked by the egress proxy, so no official page could be opened and no register's fields, record counts or terms of use were read directly from the source. Search snippets are often undated. Anything below that rests on a snippet only is flagged "(snippet only)". Planning research, not legal advice. Items I know from background knowledge but could not source are listed under Gaps, not under Cited Findings.

## 1. Health: which regulators and registers identify doctors, hospitals and clinics, and are they public?

### Takeaway
Most health regulators in these markets run a free lookup of a single practitioner or facility, queried by ID or name. In the sources found, only Brazil (CNES via DATASUS monthly files) and India (IMR, 1.4M+ doctors) show evidence of bulk or browsable data. The facility-level sources most likely to be bulk-usable are Brazil's CNES, Indonesia's SATUSEHAT master facility index (access terms unverified) and Turkey's open-data portal (coverage unverified). For the UAE, Saudi Arabia, Nigeria and Egypt, the evidence found describes verification lookups, not downloadable lists.

### Cited Findings

**UAE**
- DHA runs "Sheryan", a public professional register at sheryan.dha.gov.ae, where a professional can be searched and checked by ID. Third-party sites (zavis.ai) republish Sheryan-derived doctor profiles with specialty and licence type. Third-party mirror sites are not an official source. — [zavis.ai example listing](https://www.zavis.ai/find-a-doctor/family-medicine/namrah-shafiq-63728716) (snippet only; the Sheryan description comes from an aggregator summary, not from DHA)
- DOH Abu Dhabi licenses doctors, nurses, dentists, pharmacists and allied health professionals, and applications go through TAMM using UAE PASS. DOH also runs a Health Workforce Management System. — [Bayut explainer](https://www.bayut.com/mybayut/all-about-doh-license/); [DOH HWMS FAQs](https://www.doh.gov.ae/en/covid-19/Health-Workforce-Management-System/HWMS%20FAQs) (snippet only). I found no evidence of a DOH public searchable register or bulk file.
- MOHAP licenses professionals, with applications through the MOHAP site and UAE PASS, and licence transfer is possible from DHA or DOH using their licence numbers. Credential primary-source verification is outsourced to DataFlow. — [MOHAP transfer-licence page](https://mohap.gov.ae/en/w/transfer-license-from-dha/doh); [DataFlow-MOHAP](https://dataflowgroup.com/verification-services/healthcare/ministry-of-health-and-prevention). I found no MOHAP public register in these results.

**Saudi Arabia**
- SCFHS offers an instant "verify practitioner registration" service, queried by national ID, Iqama, passport or SCFHS file number. Mumaris is the licensing portal. — [SCFHS service page (snippet)](https://scfhs.org.sa/en/node/1992); [SCFHS practitioner page](https://scfhs.org.sa/en/practitioner?page=13). Lookup requires an identifier, so it is a verification service and not a browsable directory, based on the snippet.

**Nigeria**
- MDCN maintains a Master Register and has told practitioners to update their website accounts to keep it current. Primary-source verification goes through DataFlow, and MDCN publishes registrar@mdcn.gov.ng. — [MDCN primary source verification](https://mdcn.gov.ng/page/services/primary-source-verification); [Nairametrics (snippet)](https://nairametrics.com/?p=496740). I found no evidence of a public name-search register.
- NHIA (established by the NHIA Act 2022) has accredited facilities, but the search found no centralised public list. — [Nairametrics on NHIA](https://nairametrics.com/2025/04/18/nhia-begins-nationwide-free-caesarean-sections-in-over-100-hospitals/); [BusinessDay on NHIA delisting](https://stg18326.businessday.ng/health/article/nhia-delists-suspends-10-health-facilities-sanctions-47-hmos-over-poor-service/)
- The UK government publishes a Nigeria "List of Medical Facilities" for its citizens. It is a secondary, non-comprehensive list. — [GOV.UK](https://www.gov.uk/government/publications/nigeria-list-of-medical-facilitiespractitioners/nigeria-list-of-medical-facilities)

**Kenya**
- KMPDC registers and licenses all practitioners and all health institutions (public, private, mission hospitals, medical and dental centres and clinics, nursing and maternity homes). Its site lets the public search a practitioner (registered and licensed for the current year) and a health facility (registered and licensed for the current year). — [KMPDC site (snippet)](https://kmpdc.go.ke/?p=134)
- KMPDC registers are split into: general/dental practitioners, senior registrar, specialists, community oral health workers, interns, foreign practitioners, health facilities and medical camps. Annual licence renewals are applied for through osp.kmpdc.go.ke. — [KMPDC (snippet)](https://kmpdc.go.ke/?p=2174); [KMPDC automation notice, 2020-01-17](https://kmpdc.go.ke/2020/01/17/kmpdc-embarks-on-automation-of-online-licensing-processes/)
- Counts and bulk-download terms were not found.

**Bangladesh**
- BMDC runs a verification portal at verify.bmdc.org.bd (search moved there from www.bmdc.org.bd/view-doctor). A search summary cites 134,568 registered physicians, 14,323 dentists and 2,918 medical assistants. The date of those figures was not given. — [BMDC view-doctor page (search result)](https://www.bmdc.org.bd/view-doctor) (snippet only)
- BMDC's president said about 36,000 physicians practise without renewed registration. BMDC does not know how many registered with fake documents or practise with no registration. Article date not shown in the snippet. — [Prothom Alo](https://en.prothomalo.com/bangladesh/jkx47oy065)
- A third-party platform, ePharma, lists 38,000+ active doctor chambers across all 64 districts, drawn from a stated "137,000-doctor master database". This is a commercial private dataset, not an official source. — [ePharma](https://epharma.com.bd/en/doctors/speciality/gynaecologist) (snippet only)

**India (benchmark)**
- NMC's Indian Medical Register (IMR) is publicly searchable by name, qualification, registration year, number or State Medical Council. It lists 1.4M+ registered doctors with registration number, council, qualification, university, address and year. The data is described as current to 2021 (with gaps for Karnataka, Arunachal and Delhi). — [NMC IMR](https://nmc.org.in/information-desk/indian-medical-register); [NMC page](https://www.nmc.org.in/?p=191) (snippet only)
- NMC has started a National Medical Register (NMR) that will replace IMR and show name, ID, registration number, place of work, qualifications and specialty. — [Careers360](https://news.careers360.com/nmc-begins-registration-of-mbbs-doctors-licensed-medical-practitioners-on-national-medical-register-nmr-portal/amp)
- Third-party Apify actors scrape the NMC register. This shows the data is scrapeable, but it is not evidence that scraping is permitted. — [Apify NMC actor](https://apify.com/whoareyouanas/nmc-doctor-lookup)

**Brazil**
- CNES (Cadastro Nacional de Estabelecimentos de Saúde), run by the Ministry of Health through DATASUS, holds monthly snapshots of establishments, professionals, beds and equipment. DATASUS publishes 13 file types, one file per type, state and month, in .dbc format, covering 2005-2024. R packages (healthbR, microdatasus) read these from the DATASUS FTP. — [healthbR CNES vignette](https://cloud.r-project.org/web/packages/healthbR/vignettes/cnes-health-facilities.html); [microdatasus manual](https://archive.linux.duke.edu/cran/web/packages/microdatasus/refman/microdatasus.html)
- The CFM portal shows physician name, CRM number, state and specialty. More than 400,000 physicians are registered with the CFM. — [CFM portal news](https://portal.cfm.org.br/noticias/medicos-devem-ter-atencao-com-divulgacao-de-dados-na-internet/); [CFM](https://portal.cfm.org.br/noticias/mais-11-125-medicos-efetuaram-o-recadastramento-nacional/) (snippet only). CFM Resolution 2.309/2022 governs CFM data handling and LGPD (Brazil's data-protection law). — [CFM Res. 2309/2022](https://sistemas.cfm.org.br/normas/arquivos/resolucoes/BR/2022/2309_2022.pdf). I did not read it, so its content is unverified.

**Indonesia**
- Ministry of Health's SATUSEHAT, launched July 2022, has a Master Sarana Index (MSI) for health facilities covering 35 facility types. It is compiled from SISDMK (health workforce), SIRS/RS Online (hospitals), SIMADA (pharmaceuticals) and other systems. More than 60,000 facilities are involved: 10,000+ primary care, 17,000 private clinics, 3,000 hospitals, 1,000 laboratories and 30,000+ pharmacies. — [Kemenkes SATUSEHAT](https://kemkes.go.id/id/satusehat-platform-layanan-kesehatan-digital-indonesia); [GovInsider](https://govinsider.asia/indo-en/article/ata-riwayat-kesehatan-di-dalam-genggaman). Whether MSI is public was not stated. The results said nothing on KKI or STR registers.

**Philippines**
- PRC's LERIS verification (verification.prc.gov.ph) is free. It verifies exam ratings, and licences by name or by licence number, and returns name, profession and registration status. — [PRC verification portal](https://verification.prc.gov.ph/); [FilipiKnow](https://filipiknow.net/prc-verification/)

**Turkey**
- The Ministry of Health has an open-data portal at acikveri.saglik.gov.tr. I did not verify whether it lists hospitals or clinics with names and addresses. — [Search summary citing the portal](https://github.com/ozancanozdemir/Turkiye-deki-Acik-Veri-Portallari-Open-Data-Portals-in-Turkey-)
- e-Nabız (the personal health record) communicates with more than 30,000 health facilities. It is a patient system and is not a provider directory. — [NTV](https://www.ntv.com.tr/saglik/e-nabiz-en-iyi-saglik-uygulamasi-secildi,ZUVUw0otaEats5RJdknh6Q)
- OCHA/HDX hosts a "Turkey Healthsites" dataset. — [HDX mirror](https://opendata.com.pk/dataset/https-data-humdata-org-dataset-turkey-healthsites). The dataset is from the Healthsites.io project (OpenStreetMap-derived) and not an official register. Its licence was not checked.

**Egypt**
- The Egyptian Medical Syndicate has 230,000+ registered members and helps the Ministry of Health license physicians. — [Wikipedia](https://en.wikipedia.org/wiki/Egyptian_Medical_Syndicate) (secondary source). No public searchable register was found.
- GAHAR accredits healthcare facilities. No public directory was found. — [Amwal Al Ghad](https://en.amwalalghad.com/?p=217523)

### Inferences
- The UAE, Saudi, Nigerian, Egyptian and (probably) Bangladeshi and Philippine registers are check-one-record tools. Bootstrapping a list from them means either per-name verification of candidates sourced elsewhere (a verification badge) or scraping, whose legality is unresolved.
- Brazil is the one country with documented official bulk facility data. Indonesia's MSI and Turkey's open-data portal are the next best leads for facility lists.
- India's IMR is the model for a public, fielded doctor register, but its data is stale (to 2021).
- Kenya's KMPDC has public search of both practitioners and facilities with annual licence status. That makes it the best African source for eye hospitals and clinics, subject to terms.
- Third-party scrapes (zavis, ePharma, Apify) show demand and data shape, but they carry their own terms and personal-data risk. They are not clean sources.

### Gaps
- Whether Sheryan (DHA), DOH or MOHAP expose facility directories or open-data feeds. Not found.
- SCFHS registry fields, count and API or partnership route. Not found beyond the lookup description.
- Nigeria: MDCN public name search and counts; MDCN facility registration and NHIA facility list. Not found.
- Kenya: register counts and downloadable lists. Official pages blocked.
- Bangladesh: BMDC fields (the snippet shows none), and whether the 134,568 figure is current. Page blocked.
- Indonesia KKI/STR registers, and whether SATUSEHAT facility data is public. Not found.
- Brazil: CNES dataset licence, and the CFM and CRM search terms. Not read.
- Turkey: contents of acikveri.saglik.gov.tr. Egypt: any official register. Not found.
- Also not covered: Saudi MoH facility list, Philippines DOH facility licensing (LTO) lists, Dubai DHA facility directory and eye-specialist filtering.

## 2. Contractors and engineers

### Takeaway
Contractor and engineer regulators with public lookups appear in Kenya (NCA, EBK), Nigeria (COREN, CORBON), Saudi Arabia (Contractors Authority, Council of Engineers), Dubai (Municipality registered-contractor data) and the Philippines (PRC for engineers). The Dubai Municipality contractor register is the only one I found that is described as published as data on a government site. Contractor classification lists are the strongest contractor sources, and counts are large (Saudi, about 142,000; Kenya, 18,000 at one point).

### Cited Findings
- **UAE (Dubai):** Dubai Municipality publishes "Consultants, Contractors and Suppliers Data", with a database of registered engineering consultancy offices and one of registered contracting companies. — [Dubai Municipality data page](https://www.dm.gov.ae/municipality-business/consultants-contractors-and-suppliers-data/) (snippet only). A new Dubai law (2025) has the Municipality maintain a unified register of all contractors, linked to the "Invest in Dubai" platform, and run an integrated system for contractor classification, technical competency certificates and code-of-conduct enforcement. — [Fenwick Elliott, 2025](https://www.fenwickelliott.com/knowledge-hub/annual-review/ar-2025/industry-update-regulating-contractor-activities-in-dubai/); [Enterprise AM, 2025-07-14](https://enterpriseam.com/uae/2025/07/14/new-dubai-law-creates-regulatory-body-compliance-system-for-contractors/). Whether the new register is public is not stated.
- **Saudi Arabia:** one source reports about 142 thousand contractors registered with the Saudi Contractors Authority and about 4 thousand with the Ministry of Municipal and Rural Affairs. The date was not stated. — [Muqawil classification page (snippet)](https://muqawil.org/en/contractor-classification/info). The September 2025 amendments to contractor classification rules are covered by [Lexis, 2025-09-11](https://www.lexis.ae/2025/09/11/ksa-updates-contractor-classification-rules-with-new-project-division-criteria/). The Saudi Council of Engineers requires all practising engineers to register (Article 27 of its bylaw) and has an accreditation e-services portal. An older Argaam report says SCE licensed 5,300 engineering offices and companies. — [SCE accreditation](https://www.saudieng.sa/English/Eservices/Accreditation); [Argaam](https://www.argaam.com/en/article/articledetail/id/1620857). No public engineer directory was confirmed.
- **Nigeria:** COREN has a public verification portal that takes a COREN number (practitioner R-numbers, firm EF-numbers). — [COREN verification](https://portal.coren.gov.ng/verification). CORBON (builders) has a public verification portal at bumap.corbon.gov.ng searchable by name, membership number, licence ID or QR code. One snippet says its register includes 88 building contracting companies and 63 consulting firms (undated, and the figure looks low). CORBON has also launched a register for building technicians and craftsmen. — [CORBON licence search](https://bumap.corbon.gov.ng/search/); [CORBON about](https://corbon.gov.ng/aboutUs); [NAN](https://nannews.ng/corbon-unveils-register-for-building-technicians-craftsmen/)
- **Kenya:** NCA registers contractors in eight categories (NCA 1 to NCA 8) across building, civil (roads, water) and specialist (mechanical and electrical) classes. Its site has a "Search Registered Contractors" feature. NCA 1 is unlimited contract value and NCA 8 is up to KES 10 million. — [NCA](https://www.nca.go.ke/local-contractors); [ConstructionKenya](https://www.constructionkenya.com/2623/nca-kenya-registration-requirements/). NCA said it had registered 18,000 contractors and accredited over 150,000 construction workers and site supervisors (undated snippet). — [Capital FM](https://capitalfm.africa/nca-registers-18000-contractors/); [Construction Review](https://constructionreviewonline.com/national-construction-authority-says-18000-contractors-in-kenya-registered/). In January 2026 NCA warned thousands of contractors face de-registration for unpaid fees, so many registered entries may be inactive. — [Capital FM, 2026-01](https://www.capitalfm.co.ke/news/2026/01/thousands-of-contractors-face-de-registration-over-unpaid-fees-nca-warns/); [AllAfrica, 2026-01-28](https://allafrica.com/stories/202601280029.html). EBK registers engineers and consulting firms (fees KES 2,000 processing, 30,000 registration, 30,000 annual licence for local firms). An online searchable EBK list was not found. — [Kenyans.co.ke](https://www.kenyans.co.ke/news/42261-engineers-board-kenya-how-register-engineer-kenya)
- **Bangladesh:** the search found the Board of Professional Engineers Bangladesh (BPERB, established 11 January 2001), which keeps a National Database of Licensed Engineers, and IEB as the professional body. It found no entity named "BEC", no PWD or RAJUK enlistment register, and no confirmation of public search. — [Wikipedia, Professional Engineers of Bangladesh](https://en.wikipedia.org/wiki/Professional_Engineers_of_Bangladesh) (secondary)
- **Indonesia:** construction business certificates (SBU) are issued by accredited LSBU bodies under LPJK. Workers need SKK competency certificates from LSPs licensed by the Ministry of PUPR, and assessors need BNSP certificates. — [izin.co.id](https://izin.co.id/blog/berapa-lama-pembuatan-sbujk/); [LSP Pertakonas](https://lsp-pertakonas.co.id/halaman/apa-itu-skk). Whether a public SIKI search exists was not confirmed.
- **Philippines:** PRC LERIS covers licensed engineers by name or number, and a private guide explains how to check engineers and contractors. — [PRC](https://verification.prc.gov.ph/); [Aedo](https://aedoconstruction.com/blog/verify-engineer-contractor-license-philippines/) (private, snippet only)

### Inferences
- Contractor registers are large (Saudi about 142k, Kenya 18k) and tiered by capacity, which makes them good raw material for "contractors" lists. Kenyan lists need an active-licence filter.
- Dubai Municipality's published contractor database and the new unified register are the strongest UAE lead.
- Nigerian COREN and CORBON lookups are identifier-driven, so they work for verification, and bulk use needs an agreement.
- Because Brazil's CREA, Turkey's contractor registry, Egypt's contractors union and others returned nothing, those markets need a separate pass.

### Gaps
- Brazil CREA/Confea public search and terms; Turkey contractor registry (including YETK and the Ministry of Environment, Urbanisation and Climate Change); Egypt contractors federation (not found).
- Saudi Contractors Authority register fields and search method (Muqawil platform), and any SCE public directory.
- NCA register fields, EBK online search, Bangladesh PWD enlistment and BPERB database access, Indonesia SIKI search and counts, Dubai DM database format (PDF, table or searchable). None confirmed.

## 3. Skilled trades and vocational certification (plumbers, electricians)

### Takeaway
For trades the search found few public registers. India (NSDC), Indonesia (BNSP/LSP) and Nigeria (CORBON technician register) have named schemes, and Bangladesh's NSDA certification is under fraud-prevention reform. For the others (UAE and Saudi trade testing, Kenya NITA, Nigeria NDE/trade testing) I found nothing citable. A trades list at launch likely has to come from licensed companies (contractor and MEP licences) and not from individual tradespeople.

### Cited Findings
- **Nigeria:** CORBON launched a register of building technicians and craftsmen. — [NAN](https://nannews.ng/corbon-unveils-register-for-building-technicians-craftsmen/) (undated snippet)
- **Kenya:** NCA accredits construction workers and site supervisors (over 150,000 per its executive director). This is the nearest Kenyan trades register found, and NITA was not found. — [Capital FM](https://capitalfm.africa/nca-registers-18000-contractors/)
- **Bangladesh:** in February 2026 the Chief Adviser ordered action against forged skill certificates, and NSDA (set up 2018) is driving a unified, standardised certification system. — [Bangladesh Monitor](https://bangladeshmonitor.com.bd/en/chief-adviser-orders-action-to-curb-fake-skill-certificates); [TBS News](https://www.tbsnews.net/node/1355096). No public NSDA register of certified workers was found.
- **India:** NSDC Digital provides a digital wallet and credential verification. — [NSDC Digital](https://nsdcindia.org/digital); [WES-NSDC partnership, 2024-08-27](https://www.globenewswire.com/news-release/2024/08/27/2936412/0/en/World-Education-Services-and-the-National-Skill-Development-Corporation-Partner-On-Enhancing-Digital-Verification-of-Academic-Records-from-India.html). It is a verification tool for learners and employers, and I found no evidence of a public worker directory.
- **Indonesia:** workers must hold SKK competency certificates from licensed LSPs, with BNSP certifying assessors. — [LSP Pertakonas](https://lsp-pertakonas.co.id/halaman/apa-itu-skk)
- **Dubai:** the new contractor law covers technical competency certificates through Dubai Municipality's system. — [Fenwick Elliott](https://www.fenwickelliott.com/knowledge-hub/annual-review/ar-2025/industry-update-regulating-contractor-activities-in-dubai/)

### Inferences
- Individual plumbers and electricians are rarely in public registers. Where listed (CORBON technicians, NCA accredited workers, SKK holders), the lists are small relative to the informal workforce or not searchable.
- Fraudulent certificates (Bangladesh) argue for treating certificate numbers as unverified claims, even when held.

### Gaps
- UAE and Saudi trade-testing bodies (including Saudi TVTC), Kenya NITA, Nigeria NDE, India Skill India register and Philippines TESDA registers. Nothing citable was found.
- Whether any of the above exposes a searchable public lookup, a count, or an API.

## 4. Business registries and chambers (companies, licences, terms)

### Takeaway
Little was verified here. Nigeria's CAC has a free public search that replaced a paid one. Dubai's contractor register is tied to the "Invest in Dubai" platform. India has a formal open-data licence (GODL-India). No chamber directory terms were found.

### Cited Findings
- **Nigeria:** CAC has a public search portal that replaced the old paid search of NGN 500. Historical search reports cost NGN 20,000 to 30,000 and certified copies NGN 5,000 per extract. Fee points come from commentary pieces. — [Techpoint](https://techpoint.africa/general/cac-public-search/); [AFSIC](https://www.afsic.net/overview-of-cac-registration-costs-in-nigeria/)
- **India:** Government Open Data Licence India (GODL-India), gazetted February 2017, allows lawful commercial and non-commercial use, adaptation and derivative works of shareable non-sensitive government data. The Open Government Data Platform has run since 2012 under NDSAP (March 2012). — [Wikipedia on NDSAP/GODL](https://www.wikipedia.org/wiki/GODL); [CIS India](https://cis-india.org/openness/public-consultation-for-the-first-draft-of-government-open-data-use-license-india-announced). Whether MCA company master data falls under it was not found.
- **UAE:** the Dubai unified contractor register links to "Invest in Dubai". — [Enterprise AM](https://enterpriseam.com/uae/2025/07/14/new-dubai-law-creates-regulatory-body-compliance-system-for-contractors/)

### Inferences
- A free public company search (CAC) is for lookups, and bulk extraction would normally need a data agreement. This needs checking per country.

### Gaps
- Not found at all: UAE economic-department licence search terms (DET Dubai, ADDED), Saudi Ministry of Commerce commercial register and Monsha'at, Turkey MERSIS/TOBB, Egypt GAFI/commercial register, Kenya BRS (eCitizen), Bangladesh RJSC, Indonesia AHU/OSS (NIB), Brazil CNPJ (Receita Federal open data), Philippines SEC/DTI, India MCA terms, and all chamber-of-commerce directory terms. These are the largest holes in this note.

## 5. Which registers are public, searchable, downloadable or restricted; personal data and partnership

### Takeaway
Classification from evidence found: bulk or file-based (Brazil CNES; India IMR is browsable); public single-record or filtered lookups (Kenya KMPDC and NCA, Bangladesh BMDC, Philippines PRC, Nigeria COREN and CORBON, Saudi SCFHS); and unclear or restricted (DOH, MOHAP, MDCN, Egypt). Terms of reuse were not read for any register.

### Cited Findings
- Brazil's CNES monthly files are downloadable in bulk, and a restricted-access area exists for each health manager. — [healthbR vignette](https://cloud.r-project.org/web/packages/healthbR/vignettes/cnes-health-facilities.html); [SES-MT PDF](https://www.saude.mt.gov.br/storage/old/files/0143-[8429-210213-SES-MT].pdf) (snippet only)
- Brazil CFM publishes name, CRM, state and specialty (restricted field set), and the CFM warns doctors about data disclosure on the internet. — [CFM portal](https://portal.cfm.org.br/noticias/medicos-devem-ter-atencao-com-divulgacao-de-dados-na-internet/) (snippet only)
- India's GODL-India permits commercial reuse of non-sensitive open data, but IMR's own terms were not found. — [Wikipedia](https://www.wikipedia.org/wiki/GODL)
- Saudi SCFHS lookups need a national ID, Iqama, passport or file number. — [SCFHS](https://scfhs.org.sa/en/node/1992)
- Credential verification in the UAE, Nigeria and Kenya-linked cases is via DataFlow (private vendor), which is a verification service for applicants. — [MDCN PSV](https://mdcn.gov.ng/page/services/primary-source-verification); [DataFlow-MOHAP](https://dataflowgroup.com/verification-services/healthcare/ministry-of-health-and-prevention)

### Inferences
- Where a register requires an ID number to query, bulk listing needs either an official data-sharing arrangement or scraping, and scraping risks breaching site terms and data-protection law (Brazil LGPD explicitly; others unverified).
- Practical approach: approach regulators for a partnership, using the verified-status badge as the value offered, and start with bulk-friendly Brazil and open-licensed India data.
- Languages and scripts (Arabic, Turkish, Bangla, Bahasa, Portuguese) were not documented in sources, but local-script names will matter. Transliteration needs are unverified.

### Gaps
- Terms of use, robots restrictions, API availability, personal-data rules (UAE PDPL, Saudi PDPL, Nigeria NDPA, Kenya DPA, Bangladesh, Indonesia PDP Law, Brazil LGPD, Philippines DPA, Turkey KVKK, Egypt PDPL) were not researched in sources.
- How to partner or request data was found for none of the regulators.

## 6. Ranked table of most usable official sources and what to bootstrap first

### Takeaway
Ranking is my judgment from the evidence above, not a sourced fact. Rank reflects: public searchability, evidence of bulk availability, evidence of record count and field richness, and verification status. Nothing was confirmed on reuse terms, so every rank is provisional.

### Cited Findings
Evidence basis for the table is in sections 1 to 5. No new facts here.

### Inferences
| Rank | Country | Source | Provider type | Evidence of access | Counts found | First list types |
|---|---|---|---|---|---|---|
| 1 | Brazil | CNES (DATASUS) | Hospitals, clinics, professionals | Monthly bulk files, 13 types | Not found | Eye hospitals/clinics (by CNES service type, unverified) |
| 2 | Kenya | KMPDC practitioner and facility search | Doctors, hospitals, clinics | Public search, annual licence status | Not found | Eye hospitals, specialists (specialists register) |
| 3 | Kenya | NCA contractor search | Contractors | Public search, 8 tiers | 18,000 (undated, possibly stale) | Contractors by class (needs active-licence filter) |
| 4 | India | NMC IMR / NMR | Doctors | Public search, fields documented | 1.4M+ (data to 2021) | Eye doctors benchmark |
| 5 | UAE | Dubai Municipality contractor and consultant database | Contractors, engineering offices | Published on government site (format unverified) | Not found | Contractors in Dubai |
| 6 | Saudi Arabia | Contractors Authority classification | Contractors | Public status unconfirmed | about 142k (single report, undated) | Contractors (if access obtainable) |
| 7 | Indonesia | SATUSEHAT facility index | Hospitals, clinics, pharmacies | Public access unconfirmed | 60,000+ facilities | Hospitals and clinics |
| 8 | Nigeria | COREN and CORBON verification portals | Engineers, builders, technicians | Per-ID lookup | CORBON snippet looks low | Verification badges; contractors via agreement |
| 9 | Bangladesh | BMDC verify portal | Doctors, dentists | Public portal, figures from search summary | 134,568 physicians (undated) | Verification badge for eye doctors |
| 10 | Philippines | PRC LERIS | Professionals incl. engineers | Free lookup by name or number | Not found | Verification only |
| 11 | Saudi/UAE | SCFHS, DHA Sheryan | Doctors | Per-ID lookup | Not found | Verification only |
| 12 | Turkey/Egypt | MoH open data / Medical Syndicate | Facilities / doctors | Unverified | Syndicate 230,000+ members | Needs more research |

First list types to bootstrap: eye hospitals and clinics in Brazil (CNES), Kenya (KMPDC) and, if access is confirmed, Indonesia; contractors in Kenya (NCA) and Dubai; eye doctors in India (IMR benchmark). Plumbers, electricians and schools had no usable official source found in these markets, and schools were not researched at all.

### Gaps
- Schools (ministry of education registers in every country) were not searched. The assignment asked for them, and this note does not cover them.
- Lawyers and accountants (bar associations, ICAI-type bodies, Saudi SOCPA, Nigeria ICAN and NBA, Kenya LSK/ICPAK, etc.) were not searched.
- The table needs a second pass using direct access to official pages, which this environment blocked.
