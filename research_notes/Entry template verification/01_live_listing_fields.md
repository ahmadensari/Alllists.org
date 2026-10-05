# Entry template verification 01: fields on live listings (research date 2026-10-05)

Scope: checks the add-on tables and the "must-have for launch" table in `research_notes/Service provider sources/entry_attributes_by_list_type.md` (the "earlier draft") against live evidence for ten list-type groups. Planning research, not legal advice.

## Method and evidence rules (read first)

- 35 WebSearch calls (standard mode), about 3 to 4 per group. WebFetch was tried twice (marham.pk, oladoc.com) and both returned EGRESS_BLOCKED, so no profile page was opened and read directly. Every "confirmed" field therefore rests on what the search tool's result summary says about the URLs it returned. That is better than inference but weaker than reading five real profiles. The earlier draft's own next step (open 5 real profiles per type and tick fields off) is still needed.
- Page dates: result pages do not show publication dates. Every citation below is "retrieved 2026-10-05, page date not shown" unless a date is stated in the text. Because of that, all price, fee, count and limit figures are marked UNVERIFIED as to currency.
- Evidence grades:
  - **P** = the cited URL is on the platform's own domain (or the regulator's own document) and the summary names the field.
  - **S** = secondary source (blog, scraper tool description, hotel-tech or marketing page). Weaker.
  - **UNVERIFIED** = single-sourced, or only S-grade, or undated and time-sensitive. Fields with two or more independent sources are marked "2+ src".
- "Draft" means the earlier draft. "Missed" means found on a live source but absent from the draft.
- Draft structure gap found: the draft has no add-on table for **real estate agents** or **hotels** (it has talent/professionals instead, which is outside this task's ten groups). Sections 8 and 9 below are new templates, built only from the evidence found.

---

## 1. Doctors (Practo, Marham, Oladoc, Zocdoc)

Practo itself returned no result in any search (the Practo query surfaced only Oladoc pages), so nothing here is Practo-confirmed.

### Confirmed by a cited source
| Field | Platform and source | Grade |
|---|---|---|
| PMDC verified status shown on profile | Oladoc [Dr Khadija Sadia](https://oladoc.com/pakistan/lahore/dr/general-physician/khadija-sadia/3894986) (summary: "PMDC-verified doctors"); Marham [Dr Muhammad Hamza](https://www.marham.pk/doctors/rawalpindi/general-surgeon/dr-muhammad-hamza) (summary: "PMDC verification status") | P, 2 platforms (2+ src). Shown as a verified flag; whether the PMDC number itself is displayed was not confirmed |
| Years of experience (e.g. 20 years, 1 year) | Oladoc [Yasmeen Qadir](https://oladoc.com/pakistan/dera-ghazi-khan/dr/general-physician/yasmeen-qadir/3818327); Marham profiles | P, 2+ src |
| Consultation fee in PKR (e.g. Rs 1,000; Rs 3,000), fee can differ by location/service | Oladoc pages above; Marham profiles | P, 2+ src |
| Qualifications (MBBS, FCPS etc.) and specialty | Oladoc, Marham | P, 2+ src |
| Practice locations with timings; multiple hospitals/clinics per doctor | Marham (summary: "in-clinic appointments at multiple hospitals", "hospital timings") | P, UNVERIFIED (single platform) |
| Video consultation option | Oladoc (Video Consultation button), Marham [online-consultation pages](https://www.marham.pk/online-consultation/general-practitioner/lahore/dr-samra-zahid-32004) | P, 2+ src |
| Patient reviews with sub-scores: patient satisfaction, diagnosis rating, clinic environment rating | Marham profile summary | P, UNVERIFIED (single platform) |
| Average wait time and "time to patient" metrics | Marham profile summary | P, UNVERIFIED (single platform) |
| Services offered list | Oladoc summary | P, UNVERIFIED |
| Insurance accepted, with insurer/plan check by patient | Zocdoc [profile example](https://www.zocdoc.com/doctor/chelsea-batista-md-824071) | P, UNVERIFIED (single platform) |
| Languages spoken | Zocdoc profiles | P, UNVERIFIED |
| Board certification in "Education and background" | Zocdoc profiles | P, UNVERIFIED |
| Accepting new patients flag; earliest availability; online booking | Zocdoc profiles | P, UNVERIFIED |
| Gender, NPI number, practice names, popular visit reasons, office locations | Zocdoc profiles | P, UNVERIFIED |
| schema.org: `isAcceptingNewPatients` and `healthPlanNetworkId` sit on MedicalOrganization (Physician is a medical organization type) | [metacpan SemanticWeb::Schema::MedicalOrganization](https://v1.metacpan.org/pod/SemanticWeb::Schema::MedicalOrganization) (mirror of schema.org) | S |

### In the draft with no source support (keep as inference)
Hospital affiliation/visiting privileges as a separate verified field; memberships (CPSP, OSP, PMA); awards/publications; licence expiry date; telemedicine licence/platform; gender as a patient filter on Pakistani platforms (confirmed only on Zocdoc); conditions treated list; separate doctor mobile vs reception number (no evidence either way; nothing seen of doctor mobiles on pages); Practo "years of experience derived from registration" (Practo not seen).

### Found but missed by the draft
Marham-style experience-quality metrics (wait time, patient satisfaction/diagnosis/environment sub-ratings); fee per location (fee belongs to the doctor-location pair, not the doctor); video-consultation as a separate mode and fee; "services offered" list distinct from specialty; Zocdoc board certification and "visit reasons" taxonomy.

### Revised launch must-have (10)
1. Name and title; 2. specialty and qualifications (degree, institution); 3. PMDC (or national regulator) number plus verified flag and check date; 4. years of experience (derived, not self-claimed, where regulator gives first registration); 5. practice location(s), each with days/times; 6. consultation fee per location with currency and fee date; 7. appointment mode (in-person, video, phone); 8. languages; 9. gender (self-declared, optional filter); 10. insurance/panel (where applicable). Reviews, wait-time metrics, board certification and accepting-new-patients move to "later".

---

## 2. Hospitals and eye hospitals

Practo and Oladoc hospital pages did not surface. Evidence is weak here.

### Confirmed
| Field | Source | Grade |
|---|---|---|
| Address, operating hours (08:00 to 23:00), OPD timings by weekday and Saturday, doctor count (82) | [HealthWire, Al-Shifa Trust Eye Hospital](https://healthwire.pk/hospitals/rawalpindi/al-shifa-trust-eye-hospital-16293) | S, UNVERIFIED (single, figures undated) |
| Per-speciality department pages (e.g. cornea) with OPD timings | [Al-Shifa speciality pages](https://alshifaeye.org/speciality-departments.php?%2F=cornea) | P (hospital's own site), UNVERIFIED |
| Accreditation recorded as a registry with **scope of accreditation**: clinical services, diagnostics (2D echo, ECG, EEG, X-ray, endoscopy), support services (ambulance), lab disciplines, pharmacy, allied health | [NABH accredited-hospital PDFs](https://portal.nabh.co/Documents/AccreditedList/Hospitals/H-2024-1397_5th%20Edition.pdf) and others on portal.nabh.co | P (accreditor's own documents). India only; edition "5th" stated, per-document dates not shown |
| Eye-hospital history/chain structure (established 1958; branches in several cities) | [Graana blog on Amanat Eye Hospital](https://www.graana.com/blog/amanat-eye-hospital-eye-care-in-pakistan/amp/) | S, UNVERIFIED |
| schema.org Hospital/MedicalClinic: `availableService` (MedicalProcedure, MedicalTest, MedicalTherapy), `medicalSpecialty`, `isAcceptingNewPatients`, `healthPlanNetworkId` | [metacpan MedicalClinic](https://metacpan.org/release/RRWO/SemanticWeb-Schema-v22.0.0/view/lib/SemanticWeb/Schema/MedicalClinic.pm), [Google schema Hospital reference](https://developers.google.cn/gmail/markup/reference/types/Hospital?hl=en) | S, 2 mirrors (2+ src) |
| Oladoc eye-specialist listing shows fee (Rs 900) and procedures (glaucoma surgery, laser, LASIK) as services | [Oladoc eye specialist](https://oladoc.com/pakistan/wah-cantt/dr/eye-specialist/muhammad-akmal-khan/746480) | P, UNVERIFIED. Procedure list yes; procedure price not shown in results |

### Draft items with no source support (keep as inference)
Bed counts by ward; procedure price ranges (cataract, LASIK) on hospital pages (not found on any returned page); equipment list; licence number with provincial commission; charity/zakat; PNRA licence; insurance panel list on hospital pages; complaints record.

### Missed by the draft
Accreditation **scope** (what departments/services the accreditation covers) rather than just "accredited yes/no"; per-department OPD timings; doctor count as a listing statistic (derived from roster links); schema.org `availableService` as the structured home for procedures and tests.

### Revised launch must-have (9)
1. Facility type; 2. ownership; 3. licence/registration number with issuer and validity; 4. departments/specialties (each with own OPD timings where known); 5. emergency 24x7 flag; 6. overall hours and OPD hours; 7. accreditation body plus scope plus expiry; 8. doctor roster link or count; 9. insurance/panel list (self-declared at launch). Equipment list and price ranges move to "later" (no live evidence they are standard fields).

---

## 3. Diagnostic labs and imaging centres with test prices

### Confirmed
| Field | Source | Grade |
|---|---|---|
| Per-test pages with price, discounted price and discount % (e.g. Chughtai Free PSA Rs 9,360 after 20% off Rs 11,700; Executive Profile (C) Rs 18,400 after 20% off Rs 23,000) | [InstaCare Chughtai pages](https://instacare.pk/book-tests/lab/chughtai-lab-11081/free-psa) | S (aggregator), UNVERIFIED (prices undated) |
| Per-test pages on Oladoc with platform discount and free home sample (e.g. fasting glucose Rs 900, 10% off; Basic Health Screen Rs 2,950 to 4,500) | [Oladoc fasting glucose](https://oladoc.com/labs/test/fasting-glucose), [Basic Health Screen](https://oladoc.com/labs/test/basic-health-screen-fasting) | P, UNVERIFIED (prices undated) |
| Fasting requirement stated per test (e.g. "8-12 hrs fasting" in test name) | Oladoc [GTT page](https://oladoc.com/labs/test/gtt-5-hrs-11-fl-tubes-required8-12-hrs-fasting); [Husaini Labs](https://husaini.org/lab-test-price-in-karachi/) ("fasting requirements clearly listed on every test detail page") | P, 2+ src |
| Home sample collection (free on Oladoc; Husaini: within 60 minutes in Karachi) | Oladoc, Husaini | P, 2+ src |
| Online report access, SMS when report is ready, 24/7 | Chughtai (summary via press piece and InstaCare) | S, UNVERIFIED |
| Number of branches/collection points (Chughtai 300+; Husaini 30+ Karachi branches) | [Mammoth Times press release](https://business.mammothtimes.com/mammothtimes/article/globeprwire-2025-10-12-top-medical-laboratories-in-pakistan), Husaini | S, UNVERIFIED (promotional) |
| Lab certification shown (PNAC certified) | Husaini page header | P, UNVERIFIED (single) |
| Number of tests in catalogue (800+) | Husaini | P, UNVERIFIED |
| Sample-transportation fee as a priced line item (Rs 230) | [Oladoc Aga Khan lab pages](https://oladoc.com/labs/agha-khan-lab), [sample transportation](https://oladoc.com/labs/test/sample-transportation-only) | P, UNVERIFIED |
| Imaging price depends on contrast and field strength (1.5T cheaper, 3T dearer); contrast adds a separate charge; radiologist report included; same-day reports | Indian centre pages: [Ace Imaging](https://aceimaging.in/mri-scan-price/), [Shalby](https://www.shalby.org/mri-scan-cost-in-india/), [CION](https://www.cioncancerclinics.com/mri-scan/mri-brain-scan-cost-in-hyderabad/) | S, 3 sources but all India marketing pages (2+ src, India only). No Pakistani imaging price page found |

### Draft items with no source support
Equipment make/model/slice count/install year; open/closed bore; radiation licence (PNRA/AERB) shown on listings; package prices (packages seen, e.g. Executive Profile, so this is actually supported but only on lab pages, not imaging); referral requirement; machine downtime notices; patient-safety (implant) info; named radiologist; second opinion.

### Missed by the draft
Original price vs discounted price and discount source (lab vs platform); fasting/preparation as a per-test field; sample type is expected but not confirmed; **branch/collection-point count and per-branch hours** (chain structure); per-test pages that exist per lab (lab x test price matrix); sample transport fee; contrast as a price modifier; catalogue size.

### Revised launch must-have (10)
1. Centre type (lab, collection point, imaging, hospital department); 2. modalities (for imaging) or discipline list (for labs); 3. test/scan catalogue entries with list price, discounted price if any, currency, price date; 4. fasting/preparation note per test; 5. home sample collection flag and areas; 6. report delivery (online, turnaround); 7. accreditation (PNAC, ISO 15189, CAP) with body and ID; 8. regulatory licence (radiation, where applicable); 9. hours incl. 24x7; 10. field strength (MRI) and contrast surcharge (MRI/CT). Equipment make/model, radiologist roster and downtime move to "later".

---

## 4. Plumbers, electricians, mobile repair

Mobile repair: no search was spent on it; nothing is confirmed. Gap.

### Confirmed
| Field | Source | Grade |
|---|---|---|
| Fixed, pre-booking prices on service pages; locality-level pages (e.g. Mumbai Kurla, Pune Sant Nagar) | [Urban Company Mumbai electricians Kurla](https://urbancompany.com/mumbai-electricians-kurla), [Delhi plumbers Janakpuri](https://www.urbancompany.com/delhi-ncr-plumbers-pocket-d-1a-janakpuri-new-delhi) | P, 2+ src |
| Visit/consultation charge (Rs 99 + 18% GST minimum if no service availed) | Urban Company electrician pages | P, UNVERIFIED (figure undated, single platform) |
| Service guarantee (up to 30 days) and damage protection up to Rs 10,000 ("UC Promise"), not applicable on cash payment | Urban Company pages | P, UNVERIFIED |
| Professionals described as trained, experienced, background-verified, police-verified; mandatory training before taking bookings | Urban Company pages; [Lapaas business-model article](https://voice.lapaas.com/startup/urban-company/business-model/) | P + S (2+ src) |
| Rating and review count on the service (e.g. 4.75, 18K reviews) | Urban Company | P, UNVERIFIED |
| Thumbtack pro profile: services selected, specialties, experience/certifications/years in business, licences, reviews, photos (3 to 5 minimum), ~30-second intro video, website link, background-check badge (free, under 5 minutes) | [Thumbtack Pro Center](https://pro-center.thumbtack.com/stories/profile-101), [Thumbtack community](https://community.thumbtack.com/discussion/comment/7476/) | P, 2 pages (2+ src) |
| TaskRabbit Tasker profile: Elite Tasker flag, star rating, number of tasks done in category, photos from past tasks, skills and experience, tools, vehicles, hourly minimums | [TaskRabbit support: which Tasker is best](https://support.taskrabbit.com/hc/articles/360050012971) | P |
| TaskRabbit onboarding: SSN-based identity check and criminal background check (US) | [Gerald guide](https://joingerald.com/learn/work--income/taskers-guide) and other S pages | S, 2+ src |
| Justdial record fields (as seen by a scraper description): name, phone, address, locality, city, category, rating, rating count, geo-coordinates, postal code, verified status, listing URL | [Apify Justdial scraper](https://apify.com/themineworks/justdial-business) | S, UNVERIFIED. Free listings rank on pages 3 to 10 (same source) |

### Draft items with no source support
Years of experience and jobs completed (Thumbtack says "years in business", TaskRabbit shows tasks-in-category; "repeat-customer share" not seen); police/character verification on Thumbtack/TaskRabbit (UC only); parts-supply policy; tools/vehicles for plumbers (tools and vehicles confirmed only for TaskRabbit); reference contacts; insurance; cancellation/no-show rate; Urban Company onboarding document list (Aadhaar etc. not found); mobile repair fields.

### Missed by the draft
Pre-booking fixed price per service (UC) vs hourly rate and minimums (TaskRabbit); guarantee/warranty period as a displayed field (30 days UC); damage protection cap; tasks completed **per category** rather than total; intro video; badge types (Elite Tasker, background-check badge); locality-level listing pages (SEO unit); training completion.

### Revised launch must-have (10)
1. Display name (first name plus initial option) and photo; 2. trade(s) and services offered; 3. service area (localities or radius); 4. price per service (fixed or starting) or hourly rate with minimum, plus visit charge, currency, price date; 5. availability (hours, same-day/emergency); 6. identity-verified flag and date (no ID number); 7. police/character check flag and date, where done (home-entry trades); 8. years in trade; 9. warranty/guarantee period on work; 10. contact via relay/WhatsApp. Photos, tools, certifications, completed-jobs-by-category move to "later".

---

## 5. Schools and tutors (incl. Quran tutors)

### Confirmed (schools)
| Field | Source | Grade |
|---|---|---|
| Summary rating 1 to 10 built from Test Score, Student Progress, College Readiness, Equity, Advanced Courses sub-ratings | [GreatSchools](https://www.greatschools.org/utah/lehi/2705-Belmont-School/), [Wikipedia GreatSchools](https://en.wikipedia.org/wiki/GreatSchools) | P + S (2+ src). US public schools, derived from state data |
| Student-teacher ratio; teacher tenure and certification; graduation rate; SAT/ACT; AP coursework; demographics | GreatSchools profile summaries | P, UNVERIFIED for exact field list |
| Niche K-12: acceptance rate, student-teacher ratio, SAT/ACT, graduation rate, tuition, boarding costs, school type (private, boarding, all-girls), grade levels, religious affiliation, clubs, sports, student safety and satisfaction surveys | [Niche Oldfields School](https://www.niche.com/k12/oldfields-school-sparks-glencoe-md/), [Niche City of Life Christian Academy](https://www.niche.com/k12/city-of-life-christian-academy-kissimmee-fl/) | P, 2 pages (2+ src) |
| Pakistan (international-school finder doris.school): curriculum (Cambridge IGCSE, O/A level, FBISE Matric/FSc), boys-only vs co-ed, day vs boarding, age range (5 to 18), campuses (3 Karachi campuses), annual tuition ranges (about PKR 812,400 to 2,543,007 depending on curriculum), compare and shortlist tools | [doris.school Karachi Grammar School](https://www.doris.school/schools/pakistan/karachi-grammar-school), [Bay View Academy](https://www.doris.school/schools/pakistan/bay-view-academy) | S (finder), UNVERIFIED (fee figures undated) |

### Confirmed (tutors)
| Field | Source | Grade |
|---|---|---|
| Preply application: bio of strengths, headshot, intro video (up to 2 minutes), digital copy of certificates/diploma, schedule/availability; team review and activation within 3 working days; "Professional Tutor" badge for approved certificates (TEFL, TESOL, CELTA); tutor sets own hourly rate | Preply tutor-guide pages ([Teast](https://teast.co/blog/teach-english-online-preply), [Roaming Vegans](https://roamingvegans.com/?p=1741)) | S only (Preply's own page did not surface), 2+ src |
| Wyzant tutor profile: hourly rate, background-check status (shown even as "No background check"), approved subjects, travel radius (e.g. within 2 miles), lesson type (in-person/online), cancellation notice (e.g. 24 hours), education, bio, schedule | Wyzant profiles [Hoboken](https://www.wyzant.com/Tutors/NJ/Hoboken/10269443/), [Chicago](https://www.wyzant.com/Tutors/IL/Chicago/9956465) | P, 2 profiles (2+ src) |
| Superprof: name, price, rating, review count, badge, response time, lesson type (face-to-face/online/both), geo coordinates, free first lesson flag, webcam flag, level taught, intro video | [Apify Superprof scraper](https://apify.com/abotapi/superprof-tutor-scraper), [Educational App Store](https://www.educationalappstore.com/website/superprof) | S, 2 sources (2+ src) |
| Quran tutors on Superprof state: ijazah certification, Tajweed, recitation, memorisation (Hifz), revision, Nazra, translation, Ashara riwayat/qira'at, Maqamat, ages (kids and adults), years of experience in title | [Superprof ijazah Quran teacher](https://www.superprof.com/ijazah-certified-quran-teacher-for-quran-recitation-quran-memorization-and-quran-revision-learn-quranic-tajweed-ashara-riwayahs.html), [Nazra/Tajweed/Hifz listing](https://www.superprof.co.in/english-learn-quran-online-nazra-tajweed-hifz-and-translation-contact-for-lessons.html) | P (platform pages), 2+ src. Whether the ijazah is verified by Superprof: not evidenced |

### Draft items with no source support
Tutor gender and "students' gender accepted" as profile fields; safeguarding checks and child-protection policy (only Wyzant shows a background-check status, nothing on child protection); parent-in-room policy; results/pass rates for tutors; fees breakdown (admission, annual charges) on Pakistani finders; school registration/recognition (PEIRA, boards) as a displayed field; facilities and admissions deadlines; Pakistani school finder fields beyond doris.school (no Pakistani-local finder surfaced).

### Missed by the draft
School: derived/outcome ratings (growth, equity, college readiness) are US-state-data driven and not replicable in Pakistan at launch; **safety and student-satisfaction survey scores** (Niche); religious affiliation; number of campuses; boarding vs day and boarding cost. Tutor: free first lesson/trial flag (Superprof), response time (Superprof), intro video as an application requirement (Preply), certificate upload with platform-awarded badge (Preply), travel radius (Wyzant), cancellation notice (Wyzant), level taught, approved-subject concept (subjects the platform approved, not self-claimed), background-check status shown even when negative (Wyzant).

### Revised launch must-have (11)
Schools: 1. entity type and registration/recognition body plus ID; 2. grades offered, gender (boys/girls/co-ed), day/boarding; 3. curriculum/board; 4. fee (monthly tuition, plus admission fee if known) with fee year; 5. campuses/address. Tutors: 6. subjects and levels (Quran tutors: Nazra, Tajweed, Hifz, translation, riwayah); 7. mode (online, home, tutor's place) with travel radius; 8. hourly rate and free/paid trial flag; 9. qualifications (degree, ijazah/sanad) with document-checked flag; 10. background-check status and date (shown even when "none"), required for child-facing tutors; 11. cancellation notice. Reviews, results and facilities move to "later".

---

## 6. Manufacturers and exporters

### Confirmed
| Field | Source | Grade |
|---|---|---|
| IndiaMART TrustSEAL: documentary verification of existence, legal status, statutory approvals, affiliations and quality certifications; paid service; separate "TrustSEAL Pro" | [IndiaMART help: TrustSEAL Pro](https://help.indiamart.com/knowledge-base/trustseal-pro/), [markhub24 explainer](https://www.markhub24.com/post/indiamart-trustseal-building-marketplace-credibility-in-india-s-b2b-e-commerce-sector) | P + S (2+ src) |
| Verified-details page lists: company name, business type, established year, director/proprietor name, GSTIN, address, IEC | [IndiaMART TrustSEAL member pages](https://trustseal.indiamart.com/members/vaastu-craft), [Rockland Earthmovers](https://trustseal.indiamart.com/members/rockland-earthmovers) | P, 2 pages (2+ src). Which exact items are verified on each page is as the search summary states |
| IndiaMART exporter data shape: years exporting, export destinations, review rating and count, badges (TrustSEAL, GST Verified, IEC Verified) | [Apify IndiaMART verified exporter directory](https://apify.com/nexgendata/indiamart-verified-exporter-directory) | S, UNVERIFIED |
| Alibaba Verified Supplier: legal existence, production capability and process controls checked; independent inspectors (SGS, TUV Rheinland, Intertek); on-site visit with staff interviews; "Gold Supplier" paid tier; Trade Assurance separate | [Shopappy guide](https://shopappy.com/ecommerce/alibaba/verify-alibaba-supplier), [China Checkup](https://www.chinacheckup.com/blog/alibaba-gold-supplier) | S, 2+ src. Alibaba's own page did not surface |
| Alibaba profile: certifications, years in business, staff count, factory reviews | Shopappy guide | S, UNVERIFIED |
| Alibaba audit assessment dimensions: company overview, production capacity, process management and flow, export situation, export business capacity, development plans | [9696.me explainer](https://9696.me/how-are-alibaba-com-suppliers-verified/) | S, UNVERIFIED. (One result was a university-domain page that looked like scraped content; not relied on.) |
| Made-in-China audit report structure: A General (company overview, human resources); B Foreign trade capacity (export overall situation, export business capacity, supplier management, after-sales service); C R&D capacity; D Management system and product certification; E Production capacity and quality control; badges Diamond Member and Audited Supplier | [made-in-china.com/factory/audits](https://www.made-in-china.com/factory/audits.html) | P, UNVERIFIED (single platform, structure from search summary) |
| Made-in-China data fields include prices and MOQ | [Apify MIC scraper title](https://apify.com/haketa/made-in-china-scraper) | S, UNVERIFIED (title text only) |

### Draft items with no source support
MOQ and sample availability as confirmed Alibaba/IndiaMART fields (MOQ only hinted for MIC via a scraper title); price basis (FOB, EXW); payment terms; lead time; packaging; annual turnover band (note: search flagged that turnover and employee count were **not** prominent on the TrustSEAL page; Alibaba shows staff count); registered vs factory vs warehouse addresses; trade-association membership; ready stock; response rate.

### Missed by the draft
Verification as a **tiered, paid, third-party/on-site product** (document-only TrustSEAL vs on-site inspected Alibaba/MIC) with named inspector; "years exporting" separate from year established; separate "verified" flags per tax ID (GST Verified, IEC Verified); director/proprietor name as a verified field; factory reviews (reviews of the factory, not the product); the audit report's five-part structure as a ready-made capability checklist; OEM/ODM flag inside R&D capacity; "Diamond"/"Gold" paid-tier flags (must not be confused with verification).

### Revised launch must-have (10)
1. Business type (manufacturer, trader, wholesaler, exporter); 2. product categories with HS code; 3. legal/tax IDs with per-ID verified flag (NTN/STRN, GSTIN, IEC, USCC) and check date; 4. registered address and factory address with separate geo; 5. year established and years exporting; 6. export markets/destinations; 7. certifications with body, ID, expiry; 8. verification tier and verifier (none, document, on-site, third-party inspector) with date; 9. production capacity band and workforce band; 10. OEM/ODM flag; MOQ added as optional. Price lists, payment terms and ready stock move to "later".

---

## 7. Contractors and construction firms

### Confirmed
| Field | Source | Grade |
|---|---|---|
| Checkatrade vetting: 12 checks including evidence of qualifications/accreditations (e.g. Gas Safe), outstanding CCJs (credit check), trading history, proof of public liability insurance, ID check, 5 customer references called, face-to-face consultation, minimum 2 years in trade, profile live in as little as 24 hours | [ProBuilder](https://probuildermag.co.uk/?p=44103), [Trade2base comparison](https://www.trade2base.com/blog/rated-people-vs-mybuilder-guide-uk), [Electrician Courses 4U](https://electriciancourses4u.co.uk/?p=5617) | S, 3 sources (2+ src). Checkatrade's own page did not surface |
| Houzz Pro profile: professional category, license number, "Verified License" status, areas served, typical job cost range (e.g. $7,500 to $5 million), awards | [Houzz pro page](https://www.houzz.com/pro/builttoperfection), [Houzz Calvin Cutler Construction](https://www.houzz.com/professionals/general-contractors/calvin-cutler-construction-inc-pfvwus-pf~1891171739) | P, 2 pages (2+ src) |
| Angi Certified/Approved: average rating 3 stars or higher, owner/principal background check passed within last 2 years, state/local licences maintained | [Bob Vila Angi review](https://www.bobvila.com/articles/angi-review), [Angi FAQ](https://www.angi.com/faq) | S + P (2+ src) |
| PEC constructor categories: eight (C-A no limit; C-B up to PKR 3,000 million; C-1 1,800; C-2 800; C-3 400; C-4 150; C-5 50; C-6 20 million); matching operator categories O-A to O-6; annual renewal fee by category (C-A Rs 200,000 down to C-6 Rs 10,000 for Pakistani applicants); late fee 2% per month up to 18%; renewal deadline 31 March | [PPRA-hosted PEC document](https://www.ppra.org.pk/elv/7/38uob15721.pdf), [PEC application documents summary](https://www.slideshare.net/slideshow/constructorsopreratorform/51797384) | P-ish (regulator policy copies), UNVERIFIED: figures come from the 2017 Registration Policy; current values not confirmed. |

### Draft items with no source support
Past projects with client and completion certificate (Checkatrade uses references and photos/testimonials, Houzz uses job cost range; project tables not confirmed); key personnel; plant and equipment list; bonding capacity and audited turnover; litigation/blacklisting; EPADS/PPRA enlistment; defects-liability terms; HSE record; ISO certificates on profile.

### Missed by the draft
Draft listed "C-A to C-6"; sources show **C-B exists between C-A and C-1** and a parallel O-series for operators (UNVERIFIED current); credit-check/CCJ equivalent (financial standing flag); **public liability insurance as verified document with expiry** (Checkatrade core check); minimum years in trade as admission gate; references called by the platform (count, e.g. 5); **typical job cost range** as a buyer field (Houzz); Angi's recency rule on background checks (valid for 2 years); licence status shown as a separate "Verified License" badge distinct from the licence number; awards.

### Revised launch must-have (10)
1. Legal entity type and registration (SECP/NTN); 2. PEC number, category (C-A to C-6 incl. C-B), field(s) of work and validity date; 3. work types; 4. typical project size band (min/max); 5. service/mobilisation area; 6. public liability insurance verified flag with expiry; 7. years trading (derived from registration); 8. three past projects or references with proof link, flagged consented; 9. licence-verified badge with check date; 10. key equipment owned (self-declared). Bonding, financial bands and litigation history move to "later" (no live platform shows them as standard).

---

## 8. Real estate agents (new; the draft has no table)

### Confirmed
| Field | Source | Grade |
|---|---|---|
| Property Finder agent: verified status, broker licence (BRN/RERA), super-agent badge, nationality, languages spoken, year experience began (years of experience), average rating, review count, platform ranking, total active listings, recorded transactions, job title, agency, service areas | [Property Finder agent page](https://www.propertyfinder.ae/en/agent/mehmet-agirman-442151), [Apify Property Finder agent extractor](https://apify.com/axlymxp/propertyfinder-agent-lead-extractor) | P + S (2+ src) |
| Property Finder requires licence number on profile and checks it with RERA and ADRAC | [Property Finder Help Center](https://support.propertyfinder.ae/hc/en-us/articles/25088401552402) | P |
| Zameen agency profile: agency name, properties for sale and for rent, team members with roles (CEO, Director), description, contact phone and WhatsApp; profiles reviewed by Zameen editorial staff | [Zameen Zaamin Properties](https://www.zameen.com/agents/Lahore/Zaamin_Properties_-205117/), [Zameen forum: become an agent](https://www.zameen.com/forum/t/how-to-become-an-agent-in-zameen-com/7520) | P, 2 pages (2+ src) |
| Zameen listing-level verification (blue or green check-mark, reserve button) | [Zameen blog on frauds](https://www.zameen.com/blog/common-property-frauds-to-avoid.html) | P, UNVERIFIED (listing, not agent, verification) |
| Zameen scale statistics (about 6,000 agencies, 500,000 verified listings) | same Zameen pages and [Craft](https://craft.co/zameencom) | S, UNVERIFIED (undated) |

### Not supported
No Zameen agent-licence field was seen; no evidence in this research that Pakistan has a national agent licence like RERA/BRN (not searched).

### Revised launch must-have (9, built only from evidence)
1. Agency name and agent name/role; 2. licence/registration number, issuing body, verified flag (where a regulator exists; otherwise "none"); 3. verification level and date; 4. service areas (localities/societies); 5. listing types handled (sale, rent, commercial); 6. years of experience/year started; 7. languages; 8. active-listings count (derived) and link to listings; 9. phone/WhatsApp contact via relay. Ratings, ranking, transactions and super-agent badge move to "later".

---

## 9. Hotels (new; the draft has no table)

### Confirmed
| Field | Source | Grade |
|---|---|---|
| schema.org LodgingBusiness/Hotel: `checkinTime`, `checkoutTime`, `numberOfRooms`, `petsAllowed`, `starRating` (a Rating whose `author` names the rating body, e.g. HOTREC, DEHOGA, WHR, Hotelstars), `amenityFeature` | [schema.org Hotel mirror](https://meta.schema.org/Hotel), [attic.schema.org/Hotel](https://attic.schema.org/Hotel), [metacpan LodgingBusiness](https://metacpan.org/pod/SemanticWeb::Schema::LodgingBusiness) | S (mirrors of schema.org), 3 mirrors (2+ src) |
| Booking.com extranet property details: photos, room descriptions, amenities (Wi-Fi, AC, pool), house rules, check-in/check-out times, cancellation policy, room types, rates and availability per room type, special offers | [Hostex Extranet guide](https://hostex.io/blog/?p=3079), [Smartorder Extranet guide](https://www.smartorder.ai/resources/blog/booking-com-extranet/) | S, 2 sources (2+ src). Booking.com's own help page did not surface |
| Tripadvisor property setup: full address, phone, email, website, business type (hotel, B&B, vacation rental, resort), number of rooms, maximum occupancy, amenities checklist (Wi-Fi, parking, breakfast, pool, AC, pet-friendly, 24-hour front desk) | [Roommaster](https://www.roommaster.com/blog/how-to-list-hotel-on-tripadvisor), [InnQuest](https://www.innquest.com/blog/how-to-list-a-hotel-on-tripadvisor) | S, 2 sources (2+ src). Tripadvisor's own help page did not surface |

### Not found
Tripadvisor languages spoken, price range and hotel class/style fields (asked, not returned); Booking.com star rating as an extranet field (not shown in results); Google Hotel Center feed fields (a support page was returned but not summarised).

### Revised launch must-have (10, evidence-based)
1. Property type (hotel, guesthouse, resort, serviced apartment); 2. address plus geo; 3. star/class rating with rating body (schema `starRating.author`); 4. number of rooms and room types; 5. check-in and check-out times; 6. amenities checklist (Wi-Fi, parking, breakfast, pool, AC, 24-hour front desk, pets); 7. cancellation policy summary; 8. price range or from-price with currency and date; 9. phone, email, website/booking URL; 10. house rules (pets, couples/ID policy where relevant locally). Reviews and photo galleries move to "later".

---

## 10. Pharmacies and petrol pumps

### Confirmed
| Field | Source | Grade |
|---|---|---|
| GBP attributes are driven by primary category; general groups: Service (curbside pick-up, online orders), Access and comfort (wheelchair access, parking, Wi-Fi), Hygiene and safety, Payments (cards, mobile payments) | [Uberall: Google categories and attributes](https://en.uberall.com/en-us/resources/blog/google-categories-and-attributes), [Lumistry checklist](https://lumistry.com/blog/google-business-profile-checklist/) | S, 2 sources (2+ src) |
| Petrol-station attributes: clean restrooms, car wash, electric charging stations; EV charging listed as its own GBP use case | Uberall; [DBA Platform on EV charging GBP](https://dbaplatform.com/blog/how-to-set-up-a-google-business-profile-for-your-ev-charging-station) | S, 2 sources (2+ src) |
| Pharmacy attributes: wheelchair accessibility, drive-through | Uberall | S, UNVERIFIED (single, and it is an example not a full list) |
| "24 hours" shown as an attribute for some categories (supermarket given as example; gas/EV for accessibility 24/7) | Uberall | S, UNVERIFIED |
| Fuel-station directory fields (cardekho, India): address, location, phone, timings, fuel types (petrol, diesel, CNG, LPG), services (tyre inflation, oil check, pollution check, convenience store, air filling), 24-hour operation | [CarDekho fuel stations Bathinda](https://www.cardekho.com/fuel-stations/bathinda) and sister pages | S, UNVERIFIED (note: this is CarDekho, not Justdial) |

### Draft items with no source support
Justdial petrol-pump and pharmacy fields (Justdial pages did not surface for these categories); drug licence number and pharmacist-in-charge as listing fields on any platform; cold chain; controlled-drug licence; fuel price display and last-updated time; fuel brand/marketer (not shown in results; may still be useful); weights-and-measures calibration seal; OGRA/explosives licence; queue/crowd info. These are regulatory-driven additions, justified by law not by platform practice, so keep as inference.

### Missed by the draft
Hygiene and safety attribute group (GBP); drive-through as a pharmacy/fuel service flag; EV charging as a first-class service (with connector/charger types, to be sourced); pollution check (PUC) service at pumps (India context); the principle that the **available attribute set changes with primary category** (already in draft) now has two secondary sources.

### Revised launch must-have (9)
1. Hours with 24x7 flag; 2. brand/chain; 3. services/fuel types (petrol, diesel, CNG, LPG, EV charging) as checklist; 4. payment methods; 5. accessibility (wheelchair) and restroom/prayer facilities; 6. pharmacy: home delivery and drive-through flags; 7. pharmacy: drug licence number and pharmacist-in-charge registration (inference, regulator-driven, keep because it is the only strong trust field); 8. pump: ancillary services (air, car wash, tyre, ATM, store); 9. phone. Live fuel price and stock data move to "later".

---

## Consolidated table: newly confirmed or newly discovered fields

Mark: C = confirmed in the draft but now source-backed; N = new field the draft missed. All rows are retrieved 2026-10-05, page date not shown.

| # | List type | Field | C/N | Evidence | Grade |
|---|---|---|---|---|---|
| 1 | Doctors | PMDC verified flag on profile | C | Oladoc, Marham | P, 2+ src |
| 2 | Doctors | Years of experience, fee in PKR per location | C | Oladoc, Marham | P, 2+ src |
| 3 | Doctors | Video-consultation mode | C | Oladoc, Marham | P, 2+ src |
| 4 | Doctors | Wait time and patient-satisfaction/diagnosis/environment sub-ratings | N | Marham | P, UNVERIFIED |
| 5 | Doctors | Board certification; visit reasons; accepting new patients; earliest availability | N | Zocdoc | P, UNVERIFIED |
| 6 | Hospitals | Accreditation scope (services/departments covered) | N | NABH PDFs | P (India) |
| 7 | Hospitals | Per-department OPD timings; doctor count | N | HealthWire, Al-Shifa | S/P, UNVERIFIED |
| 8 | Hospitals/Doctors | schema.org `availableService`, `medicalSpecialty`, `isAcceptingNewPatients`, `healthPlanNetworkId` | C | schema mirrors | S, 2+ src |
| 9 | Labs | List price, discounted price, discount % per test | N | InstaCare, Oladoc | S/P, UNVERIFIED prices |
| 10 | Labs | Fasting/preparation per test | C (as prep) | Oladoc, Husaini | P, 2+ src |
| 11 | Labs | Home sample collection (free on Oladoc), sample transport fee | C/N | Oladoc, Husaini | P, 2+ src (fee single) |
| 12 | Labs | Branch/collection-point count; PNAC certification; online report + SMS | N | Chughtai, Husaini | S/P, UNVERIFIED |
| 13 | Imaging | Contrast surcharge; field strength as price driver; report included | C | Indian centre pages | S, 2+ src (India only) |
| 14 | Trades | Fixed pre-booking price per service; visit charge; locality-level pages | C/N | Urban Company | P, 2+ src |
| 15 | Trades | Service guarantee period (30 days); damage cover cap | N | Urban Company | P, UNVERIFIED |
| 16 | Trades | Background-check badge, licences, intro video, 3 to 5 photos | C/N | Thumbtack | P, 2+ src |
| 17 | Trades | Tasks done per category, Elite flag, tools, vehicles, hourly minimum | N | TaskRabbit | P |
| 18 | Schools | Safety and satisfaction survey scores; religious affiliation; boarding cost | N | Niche | P, 2+ src |
| 19 | Schools | Curriculum, boys/co-ed, day/boarding, campuses, tuition range (Pakistan) | C | doris.school | S, UNVERIFIED fees |
| 20 | Tutors | Background-check status shown even when negative; travel radius; cancellation notice; approved subjects | N | Wyzant | P, 2+ src |
| 21 | Tutors | Free first lesson, response time, webcam flag, level taught, intro video | N | Superprof | S, 2+ src |
| 22 | Tutors | Certificate upload with platform badge; intro video required (<=2 min); review before activation | N | Preply | S, 2+ src |
| 23 | Quran tutors | Ijazah, Tajweed, Hifz, Nazra, translation, riwayat/qira'at, Maqamat, age groups | C | Superprof | P, 2+ src |
| 24 | Suppliers | Tiered verification (document vs on-site/third-party) with named inspector | N | IndiaMART, Alibaba, MIC | P/S, 2+ src |
| 25 | Suppliers | Per-ID verified flags (GST Verified, IEC Verified), director/proprietor name, years exporting, export destinations | N | IndiaMART | P/S, 2+ src |
| 26 | Suppliers | Five-part audit structure (overview/HR, foreign trade, R&D, management/certification, production/QC) | N | Made-in-China | P, UNVERIFIED |
| 27 | Contractors | Insurance proof, credit/CCJ check, references called (5), min 2 years in trade | N | Checkatrade | S, 2+ src |
| 28 | Contractors | Typical job cost range; Verified License badge; areas served | N | Houzz | P, 2+ src |
| 29 | Contractors | Background check valid 2 years; rating >= 3 stars | N | Angi | S/P, 2+ src |
| 30 | Contractors | PEC C-B category and O-series; cost limits and renewal rules | C/N | PEC 2017 policy copies | UNVERIFIED (2017) |
| 31 | Real estate | BRN/RERA licence checked with regulator; nationality; languages; super-agent; transactions | N | Property Finder | P + S, 2+ src |
| 32 | Real estate | Agency team roles; sale/rent counts; editorial review | N | Zameen | P, 2+ src |
| 33 | Hotels | checkin/checkout time, numberOfRooms, petsAllowed, starRating with rating body, amenityFeature | N | schema.org mirrors | S, 2+ src |
| 34 | Hotels | Property type, max occupancy, amenities checklist, cancellation policy, room types, house rules | N | Tripadvisor, Booking.com | S, 2+ src |
| 35 | Pharmacy/pumps | Hygiene and safety group, drive-through, EV charging, restrooms, car wash | N | GBP via Uberall, DBA | S, 2+ src |
| 36 | Pumps | Fuel types and ancillary services (tyre, oil check, PUC, store) | C | CarDekho | S, UNVERIFIED |

---

## Gaps

- **No page opened.** WebFetch to marham.pk and oladoc.com was blocked, so all confirmation is via search-result summaries. Redo with 5 live profiles per type, ideally in a browser session, to tick fields and read exact labels (for example whether Marham shows the PMDC number or only a badge).
- **Practo, Justdial, Zameen agent-profile page, Booking.com and Tripadvisor help-centre pages, Checkatrade's own pages, Alibaba's own pages and Preply's own pages did not surface.** Their entries rely on third-party descriptions (grade S).
- **Mobile repair:** no search made. Nothing confirmed.
- **Urban Company onboarding documents** (Aadhaar, police verification procedure, training length) not found; only the headline claims. **TaskRabbit** onboarding is US-specific (SSN).
- **Justdial fields for pharmacies and petrol pumps** and **Justdial free-listing form** not confirmed; drug licence and pharmacist registration as listing fields are not seen on any platform.
- **Pakistani-specific:** no Pakistani school finder with fee tables, PEIRA/board recognition fields, Pakistani imaging price pages or Pakistani real-estate-agent licensing evidence found. Pakistani prices in this note (Oladoc, InstaCare, doris.school) are undated and must not be reused as current.
- **PEC figures** come from 2017-era policy copies; current categories, limits and fees unconfirmed. The earlier repo note said "C-A to C-6"; sources suggest C-B also exists.
- **Hospital price lists and equipment lists** were not found as standard fields on any hospital listing, so the draft's "price ranges and equipment" rows stay inference.
- **Eye-hospital-specific fields** (retina/cornea sub-specialty centres, OPD by sub-specialty) seen only on one hospital's own site.
- **Counts and statistics** (Zameen 6,000 agencies, Chughtai 300+ points, Husaini 800+ tests) are promotional and undated: UNVERIFIED.
- **Legal/consent** questions unchanged from the earlier draft (health, child safeguarding, ID data); none were researched here.
