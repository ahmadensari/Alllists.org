# Group 4: Health and education directories (platforms 30 to 35)

Researched 2026-10-05 using web search snippets only. WebFetch to nhs.uk and zocdoc.com was blocked by the network proxy, so nothing below comes from reading those sites directly. Search-engine summaries were used; every figure is therefore secondary. Marker conventions: **UNVERIFIED** = single source, undated, or from a scraper/aggregator/SEO blog; "(date)" = date given in the source. Counts on company sites are self-reported marketing numbers.

---

## 1. Per-platform findings

### 30. Practo (India)

**Scale (self-reported, various dates):** more than 200,000 doctors, 5,000 diagnostic centres, 10,000 hospitals, 200+ specialties (Vulcan Post, Malaysia launch piece, undated, UNVERIFIED as to date): https://vulcanpost.com/431031/practo-healthcare-platform-malaysia-launch/. An older figure of 1 lakh+ doctors and 70,000 clinics and hospitals appears in YourStory (2014): https://cwv.yourstory.com/2014/08/practo-growth-story.

**List types seen:** doctors by specialty and city; clinics; hospitals; diagnostic centres/labs (launched July 2015, about 4,000 labs in 8 cities at launch, including Thyrocare, SRL, Metropolis, Suburban): https://www.medianama.com/2015/07/223-practo-diagnostic-labs-search/ and https://medicaldialogues.in/practo-launches-diagnostic-centre-search. Lab listings carried accreditation, home pickup, test-wise prices, photos. Search is also by test name, not just by facility.

**Ordering:** proprietary relevance algorithm using location and specialty, patient feedback, appointments booked in last 30 days, availability, recommendations; badges "most booked / recommended" (https://www.noenthuda.com/2014/12/09/practo-and-rating-systems/, 2014, blog; UNVERIFIED as current). Whether payment affects order is not stated in what I found.

**Entry fields (doctor):** photo, qualification, years of experience, clinic location, specialisation/treatments, consultation fee, languages, time slots, reviews, patient stories (same blog plus Practo listing scrapers, e.g. https://apify.com/khadinakbar/practo-doctor-scraper.md, UNVERIFIED).

**Paid:** SaaS subscription for doctors (Practo Ray, Rs 999 and Rs 1,999 per month, per a business-model blog, undated, UNVERIFIED): https://www.perfectiongeeks.com/blogs/practo-business-model-revenue-app. Promoted/sponsored listings and "Prime" visibility plans (same blog, UNVERIFIED). Revenue about USD 29 million FY2024 and EBITDA-positive Q4 FY2024 (same blog, UNVERIFIED; check Dealroom https://dealroom.co/companies/practo/). Critical retrospective: https://futurex.substack.com/p/what-went-wrong-with-practo.

### 31a. Zocdoc (US)

**List types:** providers by specialty and "visit reason"; specialty pages include acupuncturists, allergists, audiologists, cardiologists, chiropractors, **CT scan facilities**, dentists, dermatologists, dietitians, ENT, emergency medicine, endocrinologists, endodontists, eye doctors, family physicians, gastroenterologists, hand surgeons, hearing specialists (https://www.zocdoc.com/insurances/dental via search snippet; https://www.getguru.com/reference/zocdoc-search). Imaging facilities are therefore a list type on a doctor marketplace. Total providers: not found.

**Filters / ordering:** insurance in-network, languages, gender, under-18 patients, availability; ranking factors are patient visit reason, insurance, location and appointment availability (https://www.zocdoc.com/about/how-search-works, snippet only; page not read).

**Paid:** patients free; providers historically paid an annual subscription, then moved to pay-per-booking: one-time fee when a **new patient** books, no subscription, amount varies by specialty and location (https://thepapergown.zocdoc.com/facts/pay-per-booking-fees-explained/; https://d3.harvard.edu/platform-digit/submission/zocdoc-a-two-sided-platform-charging-one-side/). This is the cleanest evidence of "price per lead" in the group.

### 31b. Healthgrades (US)

**Scale:** about 3 million providers (physicians, dentists, hospitals), 40+ specialties; ratings for 28 procedures/diagnoses at 5,000+ hospitals (SEC 10-K from the Health Grades Inc. era; undated figures in aggregator): https://www.sec.gov/Archives/edgar/data/1027915/000136231007000281/c70267e10vk.htm; https://altss.com/profile/healthgradescom (UNVERIFIED). Also urgent care and hospital finders (https://www.getguru.com/reference/healthgrades-search).

**Fields:** board certification, degrees and licences, procedures, hospital affiliations, number of offices, insurance accepted, schedule, patient ratings (communication, office friendliness, wait time).

**Paid:** hospitals must contract with Healthgrades to use its rating badges in advertising (controversy noted in the 10-K-based coverage); enhanced profiles for doctors; pharma/device advertising; reputation-management subscriptions; content licensing (summary from a search aggregator, UNVERIFIED as to current mix). Owned by RVO Health (Red Ventures and Optum) per https://craft.co/healthgrades, UNVERIFIED.

### 31c. Doximity (US)

Directory is built from the NPI database as "stub" profiles that physicians claim for free (https://physicians.utah.edu/doximity; https://trinityhealthma.org/healthcare-professionals/provider-resources/doximity). Claims over 85% of US physicians as members at Q1 2026 (search summary; check https://en.wikipedia.org/wiki/Doximity; investor-sourced, UNVERIFIED). Profiles feed the U.S. News public physician locator. Also covers nurse practitioners and PAs (about 50% claimed, per Utah). **Paid by others, not the listed person:** about 70% of revenue from pharma marketing, about 28% from health systems (recruiting/marketing), small telehealth (https://jnvest.substack.com/p/doximity-docs-deep-dive, https://seekingalpha.com/article/4891767; investor commentary, UNVERIFIED). Lesson: a list can be free to listed individuals and monetised by the buyers who want to reach them. Also has residency programme rankings, salary data (Utah page).

### 32a. Marham (Pakistan)

Founded 2015, Lahore. Self-reported: 16,000+ doctors in 155 cities; 5,000+ hospitals onboard; lab and medicine partners; 10 million users; about 1 million monthly traffic (https://linkedin.com/company/marham; https://www.cbinsights.com/company/marham; undated, UNVERIFIED). Doctors marked **PMDC Verified** (note: the regulator is now called PMC in some sources); profile shows qualifications, years of experience, clinic/hospital, weekly video-consult slots and fee (observed PKR 200, 500, 1,000 for online consults) (https://www.marham.pk/online-consultation/general-practitioner/islamabad/dr-mazhar-ul-haq-malik-32734). Online consultation pages are separate lists from physical-visit pages. URL pattern is /doctors/{city}/{specialty}/{name}. Services beyond doctors: lab tests, medicine ordering. Revenue: consultation fee share and premium features (CB Insights summary, UNVERIFIED).

### 32b. Oladoc (Pakistan)

Founded 2016, Lahore (Abid and Arif Zuberi). Self-reported 25,000+ PMC-verified doctors, 100+ specialities, 15 million patients served (https://propakistani.pk/2024/06/27/zong-4g-and-oladoc-collaborate-to-revolutionize-digital-healthcare-solutions/; https://sarmayacar.com/ventures/oladoc). Earlier: 8,000 doctors in 10 cities (ProPakistani 2022): https://propakistani.pk/2022/01/14/pakistans-oladoc-raises-1-8-million-in-series-a-round/. Services: in-person and video appointments, lab test booking, medicine delivery, surgery booking, corporate wellness. Telecom bundling with Ufone and Zong (distribution channel). Revenue streams listed by data aggregators as commission, subscription SaaS and freemium (https://www.caplight.com/company/oladoc, UNVERIFIED). No source found on ambulance, blood bank or pharmacy directories on either platform. Notably, Chughtai Lab alone claims 300+ collection centres, a blood bank, ambulance and pharmacy (https://chughtailab.com/chughtai-lab/), which shows that these facility types exist in Pakistan but were not found as separate lists on Marham or Oladoc (a gap, see section 4).

### 33a. Doctify (UK and international)

"Healthcare directory powered by verified patient reviews and skill endorsements"; 150,000+ profiles; 6 million patients use it per year (https://www.doctify.com/ie/about/patientfaq, undated, UNVERIFIED). Review verified by mobile number. Search by location, specialism, insurer. List types: specialists, clinics/practices, hospitals, provider groups. Operates country sites (UK, Ireland, Australia, UAE, Saudi). **Paid by providers:** monthly, annual and rolling subscriptions with add-ons, plus sponsored placements (https://www.doctify.com/ie/about/terms-conditions-providers; https://www.doctify.com/en-sa/about/join-doctify/terms-and-conditions). Prices not published.

### 33b. Bupa Finder (UK)

Insurer's directory, not a marketplace: Bupa-recognised consultants (about 21,000), therapists (about 11,000) and hospitals/clinics (about 1,000); also care homes (residential, nursing, dementia), Bupa health centres (physio, assessments), retirement housing, and **dental insurance network practices** (https://www.finder.bupa.co.uk/; https://www.bupa.co.uk/healthcare-professionals/for-your-role/consultants; counts undated, UNVERIFIED). Entry fields: location, experience, qualifications, contact. Membership is gated by the insurer's recognition of the provider, i.e. list = "network". Not paid per listing by providers as far as found; the insurer controls the list.

### 33c. NHS Service Search / Find a service (England)

Free public service. Types: GP surgeries, dentists, pharmacies, opticians, hospitals, urgent care, mental health, sexual health, pregnancy services, vaccination and booking services, back/joint help (https://www.nhs.uk/service-search, via search snippet; page itself not fetched). Fields: address, opening hours, contact details (https://www.rochdale.gov.uk/healthchecks). API documented at https://docs.anysite.io/api-reference/nhs/nhsservicessearch.md (third party, UNVERIFIED). Example of a **government register as base list**, no payment.

### 34. School and college finders

**GreatSchools (US, nonprofit):** 150,000+ public, private and charter K-12 schools; 1-10 rating by state comparison; themed ratings (test scores, student progress, college readiness); data from 50 state education departments and federal sources (https://www.greatschools.org/gk/about/ratings/). Revenue: philanthropy mainly; licensing to real-estate sites (Zillow since 2012, Redfin, Realtor.com, Movoto, Apartments.com) under 20% of revenue (Chalkbeat 2019 via EdSurge): https://edsurge.com/news/2020-04-29-niche-raises-35-million-to-rival-school-directory-review-sites; advertising and tutoring-service ads (https://solutions.greatschools.org/advertising; https://solutions.greatschools.org/advertise-tutoring-services); enterprise K-12 data licence (https://webflow.greatschools.org/k12-data-solutions/enterprise-data-license). Tutoring is an advertiser category, not a list.

**Niche (US, for-profit):** rankings, report cards and profiles for K-12 schools, colleges, neighbourhoods and companies; Best Colleges ranking compares 1,000+ institutions using US Dept of Education data and reviews; sub-lists: public universities, liberal arts, value, by state, by major (https://www.niche.com/about/2027-best-colleges-rankings/). Schools are the paying customers: 1,400+ school clients on annual subscription in 2020; 15,000+ per later description; data licences from USD 5,000 (https://en.wikipedia.org/wiki/Niche_(company); https://edsurge.com/news/2020-04-29-niche-raises-35-million-to-rival-school-directory-review-sites; https://www.niche.com/about/for-k12-schools/). USD 35M Series C in 2020, ARR growth over 100% in 2019 (https://news.crunchbase.com/venture/pittsburgh-based-niche-secures-35m-for-school-search-platform-after-100-arr-growth-in-2019/).

**Shiksha (India, Info Edge):** 60,000+ institutions, 375,000+ courses, 800+ entrance exams, 10 million+ registered students (https://shiksha.com/about; https://craft.co/shikshacom, undated, UNVERIFIED). Separate study-abroad section. Revenue from institute advertising and admission enquiries (lead sale) (https://www.infoedge.in/Businesses/Education). Entry fields: eligibility, fees, placement statistics, rankings, reviews, scholarships, exam dates.

**Collegedunia (India):** 27,000+ colleges, 7,000+ courses, 350+ exams, 200,000+ reviews (YourStory 2014/2016 figures, dated and probably stale): https://yourstory.com/2014/12/collegedunia-secures-funding-reach-1-million-monthly-users-30k-colleges/. Revenue: cost-per-lead, sponsored listings, premium analytics (Vizologi canvas, UNVERIFIED): https://vizologi.com/business-strategy-canvas/collegedunia-business-model-canvas/.

**QS (global):** 2026 subject rankings: 55 subjects in 5 broad areas, 1,900+ universities ranked, 21,000+ entries (https://tools.prnewswire.com/en-us/live/20823/release/20260325EN18335). Ranking = list of institutions per subject; QS revenue from universities (Stars, advertising, data) was **not found** in this research, so I leave it as a gap.

**Government/neutral registers:** England's GIAS lists 65,000+ establishments across 34 establishment types (community, foundation, voluntary aided/controlled, academy converter/sponsor-led, free schools, studio schools, UTCs, special, pupil referral units, independent, sixth form centres, FE colleges, HE institutions, online providers, secure units, nurseries, children's centres) (https://get-information-schools.service.gov.uk/glossary; https://get-information-schools.service.gov.uk/about). A ready taxonomy for school types.

**Pakistan:** 260,000+ schools and about 50 million students; government Matric boards, Cambridge O/A levels, Aga Khan board; 35,000 to 40,000 registered madrasas under five wafaq boards (Wafaq-ul-Madaris Al-Arabia, Tanzeem-ul-Madaris, Al-Salfia, Rabita-ul-Madaris, Al-Shia) (OpenEduCat marketing page, UNVERIFIED): https://openeducat.org/zh/k12-school-management-software-in-pakistan/. EduVision ranks about 25,000 institutions by Matric and Inter results from 19 education boards, by board and by city (https://www.eduvision.edu.pk/ranking/top-matric-schools-in-karachi-medium-category). So the board is a natural list dimension. Tutors and academies in Pakistan are mostly listed on classifieds (OLX Pakistan "Education & Classes", listings by city and neighbourhood for home tuition, Quran Nazra/Tajweed/Hifz, board-specific O/A, Sindh, Aga Khan, Federal) (https://www.olx.com.pk/wapda-colony_g14121/education-classes_c1429/q-tutor) and The Tutors (https://cademy.io/the-tutors). No dedicated Pakistani school/college finder with a visible payment model was found (gap).

**Coaching centres (India):** appear as chain lists (Allen 119 centres, Aakash 175, Narayana IIT 41, FIITJEE 68, Vidyamandir 113, per an SEO article, UNVERIFIED): https://www.freepressjournal.in/education/top-10-jee-coaching-institutes-in-india; also "best NEET coaching in Kota/Jaipur" lists (https://academycheck-website-newari.nuxt.dev/blog/top-neet-coaching-in-kota). List type = coaching centre by exam and city.

### 35. Pharmacy, lab, imaging finders and equipment databases

**Tata 1mg (India):** online pharmacy plus labs; 20,000+ pincodes; own 19 NABL/CAP-accredited labs; 1,200+ phlebotomists; 70+ cities; partner labs include Dr Lal PathLabs, Thyrocare, Pathcare, **Mahajan Imaging** (https://1mg.com/business-partners; https://en.wikipedia.org/wiki/Tata_1mg; marketing page, UNVERIFIED on figures). It also has a franchise "retailstore" shop-locator (https://retailstore.1mg.com/...). Pharmacies here are fulfilment partners, not an open list of independent shops.

**Dr Lal PathLabs (India):** 31 Mar 2025: 298 clinical labs, 6,607 patient service centres, 12,365 pick-up points (company filings): https://nsearchives.nseindia.com/corporate/LALPATHLAB_25042025150015_FINALppt.pdf. Three tiers of lab facility (reference lab, PSC, pick-up point) is a taxonomy the catalogue can borrow. This is a single-brand locator, not a directory.

**Imaging centre finders (US):** MDSave lists 2,000+ imaging and radiology centres with prices (https://www.mdsave.com/location/specialty/imaging-and-radiology); RemakeHealth matches by insurance, shows hours, tests, certification (https://radiologybusiness.com/topics/healthcare-management/medical-practice-management/ahra-2008/new-website-launched-about-imaging-center-information, 2008-era, UNVERIFIED as current). Price transparency is the hook: MRI cash price range USD 351 to 2,804 in one source (undated, UNVERIFIED). Bajaj Finserv Health lists radiology scans by city in India (https://www.bajajfinservhealth.in/lab-tests/chennai/radiology-scans). Pakistan: Islamabad Diagnostic Centre, Medequips etc. appear on supplier lists (https://ensun.io/search/medical-imaging/pakistan, UNVERIFIED).

**Equipment databases and who buys them:**
- **IMV Medical Information Division (US):** census database of 85,000+ pieces of imaging equipment at 12,000+ facilities (CT, MRI, nuclear medicine, fluoro, ultrasound, X-ray), licensable to qualified subscribers with contact and site-specific data; designed so imaging vendors "find customers, verify sales data, locate weak points in competition" (https://itnonline.com/content/comprehensive-database-medical-imaging-equipment, dated July 2020; https://radiologybusiness.com/node/55778). Buyers: equipment vendors (OEMs, service firms, contrast/injector makers). Price not found. This is the strongest evidence of a paid "MRI machines" list.
- **WHO Global Atlas of Medical Devices / OECD:** MRI, CT, PET units per million by country, WHO 2020-21 survey (https://www.who.int/data/gho/data/themes/topics/topic-details/GHO/medical-devices; https://ourworldindata.org/grapher/magnetic-resonance-imaging-mri-units-availability). Free, country-level counts, not per-machine records. Examples: OECD 2011 Japan 46.9, US 31.5 MRI per million (https://www.oecd.org/en/publications/health-at-a-glance-2019_4dd50c09-en/full-report/medical-technologies_ded11d43).
- **India/Pakistan counts:** India about 3.5 MRI per million in 2021 and about 3,500 hospital CT scanners; Pakistan about 80 CT and one MRI per 7.77 million people (JPMA archive, old study, UNVERIFIED): https://www.archive.jpma.org.pk/article-details/1334; GlobalData market note https://www.globaldata.com/media/medical-devices/india-mri-systems-market-to-grow-at-12-cagr-through-2036-forecasts-globaldata/. No public per-machine register for India or Pakistan was found.
- **DOTmed (US marketplace and auction):** buy/sell/refurbish/install used CT, MRI, X-ray etc.; sellers run "WebStores"; auctions with hundreds of lots (https://www.dotmed.com/browse/equipment/imaging/ct/ct-scanner/all/offset/660/). Listing fees not found. Buyers are imaging centres, clinics, hospitals, brokers worldwide.
- **Regulatory:** DRAP (Pakistan) registers medical devices, but the register is backlogged (about 3,000 applications handled) (https://propakistani.pk/2022/11/22/serious-healthcare-crisis-imminent-due-to-roadblocks-in-import-of-surgical-equipment/). US trade guide: https://www.trade.gov/country-commercial-guides/pakistan-healthcare-and-medical-equipment.

**Hospital rankings and accreditation lists (cross-platform):** Newsweek World's Best Specialized Hospitals 2024: 12 specialties, e.g. top 300 for cardiology and oncology, 250 paediatrics, 125 orthopaedics etc. (https://rankings.newsweek.com/worlds-best-specialized-hospitals-2024/orthopedics). U.S. News: 14 specialties plus 23 procedures/conditions (https://www.fiercehealthcare.com/hospitals-health-systems/57-hospitals-get-top-rankings-all-9-specialty-procedures; older edition). JCI and NABH accreditation lists in India (https://apollohospitals.com/clinical-quality-and-outcomes/accreditations). These show that "hospitals by specialty, ranked" and "hospitals by accreditation" are list types.

---

## 2. Master table of distinct health and education list types

Scale key: HL = hyper-local (neighbourhood/town), C = city, N = national, G = global. Payment evidence: P = paid by listed party or buyer with source, F = free/regulatory, ? = not found.

| List type | Platforms | Unit | Priced? (is a price shown) | Natural scale | Evidence of payment |
|---|---|---|---|---|---|
| Doctors by specialty | Practo, Zocdoc, Healthgrades, Doximity, Marham, Oladoc, Doctify | Individual | Often fee shown (Practo, Marham: PKR 200 to 1,000 online) | C (search), N (coverage) | P: Practo Ray, Zocdoc per-new-patient fee, Doctify subscription |
| Specialists/consultants network | Bupa Finder, Doctify | Individual | No | N | Insurer-controlled; Doctify provider subscription |
| Dentists and dental practices | Zocdoc, Healthgrades, NHS, Bupa dental network | Individual and firm | No | HL/C | Zocdoc fee by specialty |
| Hospitals | Practo, Healthgrades, Marham, NHS, Bupa, Doctify | Institution | Procedure ratings, not prices | C/N | P: hospitals pay Healthgrades to use rating badge |
| Hospitals ranked by specialty | Newsweek, U.S. News, Healthgrades | Institution | No | N/G | ? (rankers earn via licences; not verified) |
| Accredited hospitals (JCI, NABH) | accreditors | Institution | No | N/G | ? |
| Clinics and practices | Practo, Doctify, NHS (GP surgeries) | Firm | Fee sometimes | HL/C | P: Practo/Doctify subscriptions |
| Diagnostic labs / pathology | Practo, Marham, Oladoc, 1mg, Lal PathLabs | Firm | Yes, test-wise prices | C | P: lab bookings via partners (1mg, Oladoc); commission, UNVERIFIED |
| Lab test catalogue (test by lab) | Practo, 1mg, Bajaj Finserv Health | Service | Yes | C | P: booking margin, UNVERIFIED |
| Collection centres / pick-up points | Lal PathLabs | Firm outlet | No | HL | Own network |
| Imaging centres (MRI, CT, X-ray, ultrasound) | Zocdoc (CT facilities), MDSave, RemakeHealth, Bajaj | Firm | Yes (MDSave cash prices) | C | P: MDSave sells bookings (UNVERIFIED); Zocdoc fee |
| Pharmacies | NHS, 1mg, Marham/Oladoc (medicine order) | Firm | Drug prices | HL | P: 1mg margin; NHS free |
| Opticians / eye care | NHS, Zocdoc (eye doctors) | Firm and individual | No | HL | ? |
| Sexual health, pregnancy, mental health services | NHS | Service | No | C | F |
| Nursing/dementia care homes, retirement housing | Bupa Finder | Firm | No | C | Bupa-owned operations |
| Physiotherapy/health centres | Bupa Finder | Firm | No | C | Bupa-owned |
| Allied therapists (physio, psychologists) | Bupa (11,000 therapists), Zocdoc (chiropractors, dietitians, audiologists, acupuncturists) | Individual | No | C | Zocdoc fee |
| Nurses and PAs/NPs | Doximity (NPs, PAs) | Individual | No | N | P: Doximity advertisers (pharma, health systems) |
| Medical equipment installed base | IMV, WHO/OECD | Equipment record (IMV), country count (WHO) | IMV licence (price not found) | N (IMV US), G (WHO) | P: IMV licences to vendors; WHO free |
| Used/refurbished equipment for sale | DOTmed | Equipment and seller | Often quote-only | G | P: WebStores/auctions (fee not found) |
| Medical equipment suppliers/importers | Ensun, DRAP lists, trade.gov | Firm | No | N | ? |
| K-12 schools (public, private, charter) | GreatSchools, Niche, GIAS, EduVision | Institution | Ratings; fees on Niche | HL/C | P: Niche school clients; GreatSchools ads/licences |
| School districts | Niche, GreatSchools (attendance zones) | Institution | No | C | P: GreatSchools data licence |
| Schools by board (Matric, Cambridge, Aga Khan) | EduVision (PK) | Institution | No | C/N | ? |
| Colleges and universities | Shiksha, Collegedunia, Niche, QS | Institution | Fees shown | N/G | P: Shiksha ads/leads, Collegedunia CPL, Niche subscriptions |
| Courses/programmes (by subject, level) | Shiksha (375,000+), Collegedunia, QS subject (55) | Programme | Fees shown | N/G | P: same as above |
| Entrance exams | Shiksha (800+), Collegedunia (350+) | Event | No | N | P: lead gen around exams |
| University rankings by subject | QS, Niche | Institution | No | G | ? (QS revenue not found) |
| Study-abroad programmes | Shiksha Study Abroad | Programme | Yes | G | P: leads |
| Coaching centres | Shiksha/Collegedunia/blogs; JD-type directories | Firm | Fees | C | P: leads (UNVERIFIED for coaching) |
| Tutors (home, online, Quran) | OLX Pakistan, The Tutors, GreatSchools tutoring ads | Individual | Hourly/monthly fee | HL | P: classifieds; GreatSchools ads |
| Madrasas (by wafaq board) | none found as consumer list | Institution | No | HL | ? |
| Residency programmes | Doximity | Institution | No | N | P via Doximity's health-system customers |
| Patient reviews / endorsements | Doctify, Healthgrades, Niche, Collegedunia | Content on above | No | n/a | Doctify subscription |

---

## 3. List types not in the seed set

Seed set: petrol pumps, schools, beauty parlours, bakeries, mobile stores, mobile repair, spare parts, furniture, pharmacies, doctors, nurses, lawyers, bookshops, hardware, MRI machines, plumbers, Quran tutors, factories.

New and well evidenced:
1. Hospitals (separate from doctors), and hospitals by specialty or by accreditation.
2. Clinics / GP surgeries / practices.
3. Diagnostic and pathology labs, with a test-wise price list.
4. Imaging centres (CT, MRI, X-ray, ultrasound as facilities, distinct from the machines).
5. Dentists and dental clinics.
6. Opticians and eye hospitals.
7. Physiotherapists and allied therapists (dietitians, audiologists, chiropractors, psychologists).
8. Care homes, nursing homes and retirement housing (Bupa).
9. Mental health, sexual health, pregnancy and vaccination services (NHS).
10. Colleges and universities (distinct from schools), and university programmes/courses.
11. Entrance exams (Shiksha, Collegedunia).
12. Coaching centres/academies and tutor lists beyond Quran (home tutors by board and class).
13. School districts and school-by-board lists.
14. Madrasas by wafaq.
15. Study-abroad programmes.
16. Lab collection centres and sample pick-up points.
17. Used/refurbished medical equipment for sale, medical equipment suppliers/importers, and equipment installed-base records (the existing MRI seed generalises to CT, X-ray, ultrasound, PET).
18. Accredited facilities (JCI, NABH, NABL, CAP) as a cross-cutting list.
19. Residency/training programmes (Doximity).

Not found as lists in this group but implied (UNVERIFIED, from Chughtai's own site only): blood banks, ambulance services, vaccination centres.

---

## 4. Gaps

- NHS and Zocdoc pages could not be read (egress blocked). NHS category list and Zocdoc search ordering are from snippets only.
- No hard counts for Zocdoc providers, Healthgrades facility types beyond doctors and hospitals, and no dated counts for Practo's current doctors, clinics or labs.
- No price points found for Doctify, Practo promoted listings, Niche, Shiksha or Collegedunia lead prices, IMV database licence, DOTmed listing fees, or QS university-side revenue. Treat the payment evidence as direction only.
- No evidence found of ambulance, blood bank, physiotherapy, or nursing home directories on Marham, Oladoc, Practo or Healthgrades. Need a targeted pass (Edhi, Rescue 1122, Red Cross, India's e-RaktKosh, Justdial categories).
- No equipment installed-base register for India or Pakistan. Pakistan MRI/CT counts are from an old JPMA study. A true per-machine "MRI machines" list would have to be built from hospital and imaging-centre submissions, since IMV (US) is the only commercial per-machine census found.
- Pakistan education: no consumer school/college finder with visible monetisation found; EduVision is result-based ranking. No madrasa or Quran-tutor directory found in this group (Group 3 covers tutors).
- Pharmacy finders: no marketplace of independent pharmacies found for India or Pakistan (1mg is partner/franchise; NHS is a register). Pharmacy as an open list of independent shops with local prices is therefore an unproven but unserved slot.
- Many "scale" figures are the platforms' own marketing and are undated; mark UNVERIFIED until confirmed from filings (Info Edge and Doximity file public reports; Dr Lal PathLabs is already from exchange filings).
