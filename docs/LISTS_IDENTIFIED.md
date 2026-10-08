# Complete list of the lists identified in research

Compiled 2026-10-06 from the repository's own research. Nothing new was researched. Every row below comes from one of these sources, and the counts are checked against them.

| Part | What it is | Source | Count |
|---|---|---|---|
| 1 | The founder's own seed list (owner-named) | docs/DECISIONS.md section 8, C23, C30 | 31 lines (the log's items, with grouped ones split out) |
| 2 | Service-provider inventory (author's design) | research_notes/Service provider sources | 124 types in 15 groups |
| 3 | Master catalogue from 53 established platforms | reports/Established platform list types.md | 113 list types in 12 families, as the report counts them |
| 4 | Ranked shortlists: 14 seed types, 10 promising groups, 3 first tests, and what to avoid or earn little | reports/Which lists pay.md and the platform report, sections 5 and 6 | see part 4 |
| 5 | List types actually loaded in the software by `seed_taxonomy` | backend/taxonomy/seeds.py | 32 list types in 7 families |

Overlap is deliberate: parts 2 and 3 repeat many of the same types (for example plumbers, schools, hospitals), because they come from two different studies. Most part 1 names also appear in parts 2, 3 or 5; MRI machines with prices, personal lists and some cluster lists are covered only by wider wording.

## Part 1. The founder's seed list (owner-named)

- Petrol pumps
- Schools (on a road, in a city)
- Beauty parlours and salons
- Bakeries
- Mobile stores
- Mobile phone repair services
- Spare parts shops
- Furniture stores
- Medical stores and pharmacies
- Doctors
- Nurses
- Lawyers
- Bookshops
- Hardware shops
- MRI machines with services and prices
- Plumbers and other skill-based lists
- Quran tutors in an area
- Surgical instrument makers in Sialkot
- Football makers in Sialkot
- Fan makers in Gujranwala
- Sanitaryware makers in Gujranwala
- Furniture makers in Faisalabad
- Hotels in Murree
- Eye doctors in a society
- Eye hospitals in a society
- Contractors (national)
- Data scientists (global)
- Factories and suppliers
- Personal lists: books read (private by default)
- Personal lists: belongings (private by default)
- Personal lists: classmates (private by default)

(The decision log groups the personal lists and the Sialkot, Gujranwala, Faisalabad and Murree lists; the lines above split them out. Electricians, tutors and carpenters fall under "other skill-based lists".)

## Part 2. Service-provider inventory (124 types, 15 groups)

Customer: HH household, BIZ business. Form: F firm, I individual, M mixed. Reach: HL hyper-local, CITY, REG region, NAT national, GLOB global. These are the research author's design proposals, not demand data.


### A. Home repair and skilled trades

| # | Type | Examples | Customer | Form | Reach |
|---|---|---|---|---|---|
| A1 | Plumbers | leak repair, bathroom fitting, tank cleaning | HH | I (some F) | HL |
| A2 | Electricians | wiring, fault repair, solar and UPS wiring | HH | I | HL |
| A3 | Carpenters | furniture repair, doors, kitchens | HH | I | HL to CITY |
| A4 | Masons and tile fixers | plaster, tiling, small renovation | HH | I | HL to CITY |
| A5 | AC technicians | install, gas refill, servicing | HH, BIZ | I, F | HL to CITY |
| A6 | Painters | interior, exterior, polishing | HH | I, F | CITY |
| A7 | Welders and fabricators | gates, grills, sheds | HH, BIZ | I, F | CITY |
| A8 | Locksmiths | door, car, safe | HH | I | HL to CITY |
| A9 | Roofing and waterproofing | leak sealing, heat insulation | HH | F | CITY |
| A10 | Pest control and fumigation | termites, cockroaches | HH, BIZ | F | CITY |
| A11 | Water tank and RO plant services | cleaning, filter change | HH, BIZ | F | HL to CITY |
| A12 | Gas, geyser and stove repair | geyser, heater, stove | HH | I | HL |
| A13 | Generator, UPS and solar installers | inverter, panels | HH, BIZ | F | CITY to REG |
| A14 | Handymen / mistri (general) | mixed minor fixes | HH | I | HL |

### B. Appliance and device repair

| # | Type | Examples | Customer | Form | Reach |
|---|---|---|---|---|---|
| B1 | Mobile phone repair | screen, battery, software | HH | F (shops), I | HL to CITY |
| B2 | Laptop and computer repair | hardware, OS install | HH, BIZ | F, I | CITY |
| B3 | Home appliance repair | washing machine, fridge, TV | HH | F, I | HL to CITY |
| B4 | Car mechanics and workshops | tune-up, denting, tyres | HH, BIZ | F | CITY |
| B5 | Motorcycle repair | puncture, engine | HH | F, I | HL |
| B6 | Tyre and battery shops | puncture, replacement | HH | F | HL to CITY |
| B7 | Car wash and detailing | wash, polish | HH | F | HL |
| B8 | Watch, shoe and bag repair | stitching, sole repair | HH | I, F | HL |
| B9 | Camera, printer and photocopier repair | office machines | BIZ, HH | F | CITY |
| B10 | CCTV and security system installers | cameras, alarms | HH, BIZ | F | CITY |

### C. Construction, contracting and property

| # | Type | Examples | Customer | Form | Reach |
|---|---|---|---|---|---|
| C1 | General and civil contractors | roads, buildings, tender work | BIZ, gov | F | NAT |
| C2 | Architects and designers | residential, commercial | HH, BIZ | M | CITY to NAT |
| C3 | Interior designers | home, office fit-out | HH, BIZ | M | CITY |
| C4 | Civil, structural and MEP engineers | design, supervision | BIZ | M | NAT |
| C5 | Quantity surveyors and valuers | cost, property valuation | BIZ, HH | M | NAT |
| C6 | Real estate agents and developers | sales, rentals | HH, BIZ | M | HL to CITY |
| C7 | Building material suppliers | cement, steel, bricks | BIZ, HH | F | CITY to REG |
| C8 | Heavy equipment rental | cranes, excavators | BIZ | F | REG to NAT |
| C9 | Surveyors and land services | boundary, topographic | BIZ, HH | M | REG |

### D. Healthcare

| # | Type | Examples | Customer | Form | Reach |
|---|---|---|---|---|---|
| D1 | General practitioners and clinics | family doctor | HH | M | HL |
| D2 | Eye doctors / ophthalmologists | cataract, LASIK, retina | HH | I | HL to CITY |
| D3 | Eye hospitals | cataract hospitals, optical chains | HH | F | CITY to REG |
| D4 | Dentists | general, orthodontics | HH | M | HL to CITY |
| D5 | Paediatricians | child specialists | HH | I | CITY |
| D6 | Gynaecologists and maternity | obstetrics, IVF | HH | M | CITY |
| D7 | Other specialist doctors | cardiology, neurology, ENT | HH | I | CITY to REG |
| D8 | Hospitals | general, tertiary | HH | F | CITY to REG |
| D9 | Diagnostic labs | blood tests, pathology | HH | F | HL to CITY |
| D10 | MRI, CT and radiology centres | imaging | HH | F | CITY to REG |
| D11 | Pharmacies | retail, 24-hour | HH | F | HL |
| D12 | Physiotherapists and rehab | sports, post-op | HH | M | HL to CITY |
| D13 | Mental health | psychologists, psychiatrists | HH | I | CITY to GLOB |
| D14 | Hakeem and homeopathic | traditional medicine | HH | I | HL to CITY |
| D15 | Veterinary clinics | pets, livestock | HH | M | HL to CITY |
| D16 | Ambulance and blood services | ambulance, blood banks | HH | F | CITY |
| D17 | Opticians and optical shops | spectacles, lenses | HH | F | HL |

### E. Education and tutoring

| # | Type | Examples | Customer | Form | Reach |
|---|---|---|---|---|---|
| E1 | Schools | primary, secondary, Montessori | HH | F | HL to CITY |
| E2 | Colleges and universities | degree, vocational | HH | F | NAT to GLOB |
| E3 | Quran tutors | home tutors, online | HH | I | HL to GLOB |
| E4 | Madrasas and hifz schools | residential, day | HH | F | CITY to REG |
| E5 | Academic tutors | maths, science, O/A levels | HH | I | HL to CITY |
| E6 | Coaching centres and academies | MDCAT, CSS, IELTS | HH | F | CITY |
| E7 | Language teachers | English, Arabic, German | HH | I | CITY to GLOB |
| E8 | Vocational training institutes | TEVTA, NAVTTC courses | HH | F | CITY to REG |
| E9 | Daycare and play groups | child care | HH | F | HL |
| E10 | Driving schools | cars, motorcycles | HH | F | HL to CITY |
| E11 | Music, art and sports coaches | cricket, swimming, gym | HH | I, F | HL to CITY |

### F. Legal, finance and professional services

| # | Type | Examples | Customer | Form | Reach |
|---|---|---|---|---|---|
| F1 | Lawyers | family, property, criminal | HH, BIZ | I, F | CITY to NAT |
| F2 | Corporate and tax lawyers | company, IP, tax | BIZ | F | NAT |
| F3 | Notaries and oath commissioners | attestation | HH, BIZ | I | HL to CITY |
| F4 | Accountants and auditors | bookkeeping, audit | BIZ, HH | F, I | CITY to NAT |
| F5 | Tax consultants | income tax, sales tax | HH, BIZ | I | CITY to NAT |
| F6 | Banks and branches | branches, ATMs | HH, BIZ | F | HL to NAT |
| F7 | Insurance agents | life, motor, health | HH, BIZ | I | CITY |
| F8 | Money changers and remittance | currency, transfer | HH | F | CITY |
| F9 | Loan and microfinance providers | microcredit | HH, BIZ | F | REG to NAT |
| F10 | Management and business consultants | strategy, HR | BIZ | M | NAT to GLOB |
| F11 | Recruitment agencies | local, overseas | BIZ, HH | F | NAT to GLOB |
| F12 | Translators and interpreters | document, certified | HH, BIZ | I | NAT to GLOB |
| F13 | Immigration and visa consultants | study, work visa | HH | F | NAT to GLOB |

### G. IT, data and digital professions

| # | Type | Examples | Customer | Form | Reach |
|---|---|---|---|---|---|
| G1 | Data scientists | ML, analytics | BIZ | I | GLOB |
| G2 | Software developers | web, mobile, backend | BIZ | I, F | GLOB |
| G3 | Software houses and agencies | outsourcing | BIZ | F | NAT to GLOB |
| G4 | Web designers and SEO | websites, marketing | BIZ | I, F | NAT to GLOB |
| G5 | Cybersecurity professionals | pen test, audit | BIZ | M | GLOB |
| G6 | Cloud and DevOps engineers | AWS, Azure | BIZ | I | GLOB |
| G7 | IT support and network installers | LAN, helpdesk | BIZ, HH | F, I | CITY |
| G8 | Freelance digital creatives | design, video, writing | BIZ | I | GLOB |
| G9 | Digital marketing and social media | ads, content | BIZ | I, F | NAT to GLOB |

### H. Beauty, wellness and personal care

| # | Type | Examples | Customer | Form | Reach |
|---|---|---|---|---|---|
| H1 | Beauty parlours | facials, bridal makeup | HH | F, I | HL to CITY |
| H2 | Barbers and salons (men) | haircut | HH | F | HL |
| H3 | Bridal makeup artists | wedding | HH | I | CITY |
| H4 | Spas and massage | wellness | HH | F | CITY |
| H5 | Gyms and fitness | gym, yoga | HH | F | HL |
| H6 | Tailors and boutiques | stitching, bridal | HH | I, F | HL to CITY |
| H7 | Dry cleaners and laundry | pickup | HH | F | HL |
| H8 | Dieticians and nutrition | weight, clinical | HH | I | CITY to GLOB |

### I. Food, retail and daily needs

| # | Type | Examples | Customer | Form | Reach |
|---|---|---|---|---|---|
| I1 | Bakeries | bread, cakes | HH | F | HL |
| I2 | Restaurants and cafes | dine-in | HH | F | HL to CITY |
| I3 | Caterers and cooks | weddings, home cooks | HH, BIZ | F, I | CITY |
| I4 | Grocery and supermarkets | kiryana | HH | F | HL |
| I5 | Petrol pumps | fuel, CNG | HH, BIZ | F | HL to CITY |
| I6 | Water and gas delivery | bottled water, LPG | HH | F | HL |
| I7 | Meat and dairy suppliers | fresh | HH | F | HL |

### J. Transport, logistics and travel

| # | Type | Examples | Customer | Form | Reach |
|---|---|---|---|---|---|
| J1 | Movers and packers | house shifting | HH, BIZ | F | CITY to NAT |
| J2 | Courier and logistics | parcels, freight | BIZ, HH | F | NAT to GLOB |
| J3 | Taxi and ride services | cabs, rent-a-car | HH | F, I | CITY |
| J4 | Truck and goods transporters | freight | BIZ | F | NAT |
| J5 | Travel agents and tour operators | umrah, tours | HH | F | NAT to GLOB |
| J6 | Customs clearing agents | import, export | BIZ | F | NAT |

### K. Events and creative services

| # | Type | Examples | Customer | Form | Reach |
|---|---|---|---|---|---|
| K1 | Wedding halls and marquees | venues | HH | F | CITY |
| K2 | Photographers and videographers | wedding, commercial | HH, BIZ | I, F | CITY to REG |
| K3 | Event planners and decorators | weddings | HH, BIZ | F | CITY |
| K4 | Printing and signage | flex, cards | BIZ, HH | F | CITY |

### L. Public, community and civic

| # | Type | Examples | Customer | Form | Reach |
|---|---|---|---|---|---|
| L1 | Mosques and prayer services | imams, nikah | HH | F, I | HL |
| L2 | NGOs and charities | zakat, welfare | HH | F | CITY to NAT |
| L3 | Police and emergency services | stations, rescue | HH | F | CITY |
| L4 | Government service offices | NADRA, utilities | HH, BIZ | F | CITY to NAT |

### M. Agriculture and rural

| # | Type | Examples | Customer | Form | Reach |
|---|---|---|---|---|---|
| M1 | Agri inputs and seed dealers | fertiliser | BIZ | F | REG |
| M2 | Tractor and farm machinery repair | mechanics | BIZ | I, F | REG |
| M3 | Agronomists and advisers | crop advice | BIZ | I | REG to NAT |

### N. Domestic and household help

| # | Type | Examples | Customer | Form | Reach |
|---|---|---|---|---|---|
| N1 | Maids and cleaners | home cleaning | HH | I, F | HL |
| N2 | Drivers and chauffeurs | personal driver | HH | I | HL to CITY |
| N3 | Gardeners | lawn, plants | HH | I | HL |
| N4 | Security guards and agencies | guards | HH, BIZ | F | CITY |
| N5 | Nannies and elder care | home care | HH | I | HL to CITY |

### O. Specialised business services

| # | Type | Examples | Customer | Form | Reach |
|---|---|---|---|---|---|
| O1 | Engineering consultants (specialised) | oil and gas, power | BIZ | F | NAT to GLOB |
| O2 | Testing and certification labs | ISO, material testing | BIZ | F | NAT |
| O3 | Industrial suppliers and fabricators | machinery | BIZ | F | NAT |
| O4 | Waste and recycling services | scrap, collection | HH, BIZ | F | CITY |

## Part 3. List types seen on 53 established platforms

Columns: who is listed (individual or firm); where the platform report found payment evidence (Strong, Some, None, Unknown); whether the type is in the founder's seed list (Named, Broad = covered only by wider wording, New). Counts come from search snippets and are order of magnitude only.


### Home and trades

| List type | Listed | Payment evidence | Vs founder's seed |
|---|---|---|---|
| Plumbers and electricians | Both | Strong (Angi, UC) | Named (plumbers); Broad |
| Carpenters, painters, handymen, masons, tilers | Both | Some (Angi leads, TaskRabbit rates) | Broad |
| AC and appliance repair | Both | Strong (UC) | Broad |
| Pest control | Both | Strong (UC) | Broad |
| House, deep, sofa and carpet cleaning | Both | Some (Thumbtack, UC) | New |
| Movers, packers, helpers | Both | Strong (Justdial, pay report) | New |
| Roofers, waterproofing, solar, windows, doors, flooring, other LSA home jobs | Firm | Some (Angi leads; Houzz plans UNVERIFIED) | Broad |
| Landscapers, gardeners, tree service | Both | Some | Broad |
| Locksmiths | Both | Some (LSA) | Broad |
| Furniture assembly, TV mounting, junk removal | Individual | Some (TaskRabbit) | New |
| Home inspectors; kitchen, bath and modular-kitchen remodellers | Both | Some (Angi; licence checks weak) | New |
| Housekeepers, domestic workers, home cooks | Individual | Some (Care.com UNVERIFIED) | New |
| Beauty, grooming, massage at home; makeup artists | Individual | Some (UC; about half its value, UNVERIFIED) | New (variant of beauty parlours) |

### Health

| List type | Listed | Payment evidence | Vs founder's seed |
|---|---|---|---|
| Doctors and specialists by specialty | Individual | Strong (Zocdoc fee) | Named |
| Eye doctors and eye care | Both | Some (Zocdoc) | Named |
| Dentists and dental practices | Both | Strong (Zocdoc fee) | Broad |
| Hospitals, clinics, GP surgeries | Firm | Some (Healthgrades) | Named (eye hospitals); Broad |
| Hospitals ranked by specialty or accreditation | Firm | Unknown (rankers) | New |
| Diagnostic and pathology labs with test prices; collection points | Firm | Some (booking margin UNVERIFIED) | New |
| Imaging centres (MRI, CT, X-ray, ultrasound) | Firm | Some (Zocdoc fee; MDSave UNVERIFIED) | Named (MRI) |
| Installed medical machines (MRI, CT, PET) | Equipment | Strong (IMV licences; none in Pakistan) | Named (MRI machines) |
| Used equipment for sale; equipment suppliers and importers | Both | Strong (IndiaMART, Alibaba); DOTmed Some | Broad |
| Pharmacies and medical stores | Firm | Some (1mg margin UNVERIFIED); weak where the shop pays (pay report) | Named |
| Physiotherapists, psychologists, dietitians, audiologists | Individual | Some (Zocdoc) | Broad |
| Nurses, nurse practitioners, physician assistants | Individual | Some (advertisers pay, UNVERIFIED) | Named (nurses) |
| Care homes; mental, sexual-health, pregnancy, vaccination services | Firm | None | New |
| Vets, pet groomers, boarders, walkers, shelters | Both | Some (Thumbtack, Care.com) | New |
| Ambulance and blood banks | Firm | Unknown (none hosts it) | New |

### Education

| List type | Listed | Payment evidence | Vs founder's seed |
|---|---|---|---|
| Schools, with board and district | Firm | Some (Niche school clients); weak for revenue (pay report D) | Named |
| Colleges, universities, courses, exams, rankings, study abroad | Both | Some (leads; Collegedunia UNVERIFIED); QS Unknown | New |
| Coaching centres, vocational and computer training | Firm | Some (leads UNVERIFIED) | New |
| Academic and test-prep tutors | Individual | Some (hourly rates) | Broad |
| Language, music, art and sports teachers | Individual | Some | New |
| Quran tutors (individual) | Individual | Some (marketplace rates) | Named |
| Quran academies (Tajweed, Hifz, Noorani Qaida) | Firm | Some (USD 40 to 120 a month, UNVERIFIED) | New |
| Madrasas by wafaq board | Firm | Unknown (none hosts it) | New |
| Driving schools and instructors | Both | Some (Justdial tiers) | New |
| Daycare, preschools, babysitters, nannies, carers | Both | Some (Care.com UNVERIFIED) | New |

### Construction and property

| List type | Listed | Payment evidence | Vs founder's seed |
|---|---|---|---|
| Property for sale, residential and commercial | Both | Strong (Rightmove) | New |
| Property to rent, share or swap; hostels; parking | Both | Strong (Zillow Rentals ads) | New |
| New-build projects, housing societies, plot maps | Firm | Strong (Rightmove: GBP 2,247 a month) | New |
| Real estate agents, agencies, developers, builders | Both | Strong (Rightmove, Zillow; Dubizzle per pay report) | New (see section 7) |
| Property managers, landlords, photographers, stagers, mortgage lenders | Both | Some (secondary source) | New |
| General contractors, builders, design-build firms | Firm | Some (Houzz UNVERIFIED; Angi leads) | Named |
| Architects; interior designers | Both | Some (Houzz) | New |
| Building-material suppliers | Firm | Strong (IndiaMART) | Broad |
| Heavy and construction machinery, new, used, rental | Both | Strong (IndiaMART); OLX Unknown | Broad |

### Vehicles

| List type | Listed | Payment evidence | Vs founder's seed |
|---|---|---|---|
| Used and new cars, with curated lists (hybrid, imported, luxury) | Both | Strong (CarGurus about 90% of revenue) | New |
| Car and bike dealers | Firm | Strong (CarGurus, Autotrader) | New |
| Bikes, rickshaws, vans, trucks, buses, tractors, caravans, boats | Both | Unknown (OLX, Gumtree) | New |
| Auto parts and accessories | Both | Strong at IndiaMART (B2B); Unknown (PakWheels) | Named (spare parts) |
| Car repair, wash, tyres, towing | Firm | Some (Yelp ads) | Broad |
| Car rental, taxis, drivers | Both | Unknown (OLX) | New |
| Petrol (gas) stations | Firm | None seen | Named |

### Business and trade

| List type | Listed | Payment evidence | Vs founder's seed |
|---|---|---|---|
| Industrial machinery, machine tools, spares | Firm | Strong (IndiaMART, Alibaba, Thomas) | Broad |
| Textile and garment makers and exporters | Firm | Strong (platforms); None (TDAP) | Broad |
| Chemicals, dyes, metals, minerals, ores | Firm | Strong (IndiaMART) | Broad |
| Sialkot cluster: surgical instruments, sports goods, gloves, leather goods | Firm | None seen | Broad |
| Food, agri, FMCG, fertiliser, seeds, farm machinery | Firm | Strong (IndiaMART) | Broad |
| Packaging materials and machines | Firm | Strong (IndiaMART) | Broad |
| Electronics, electrical, appliances, gifts, home products (makers) | Firm | Strong (Alibaba) | Broad |
| Furniture and furniture-hardware makers and wholesalers | Firm | Strong (IndiaMART) | Broad |
| Lab and measuring instruments | Firm | Strong (IndiaMART) | Broad |
| Contract manufacturers and machine shops by process | Firm | Some (placement USD 7,000 to 10,000+, UNVERIFIED) | Broad |
| Certified, women-owned and audited supplier lists (ISO, halal, GOTS) | Firm | Strong (IndiaMART, Alibaba) | New |
| Manufacturers' reps, distributors, wholesalers, wholesale markets | Firm | Some (ThomasNet) | New |
| Importers and buyers; buy leads, RFQs, tenders | Firm | Strong (IndiaMART sells leads) | New |
| Business services: freight, customs, warehousing, printing, IT, testing labs | Firm | Strong (IndiaMART) | New |
| Chambers, associations, trade shows, country pavilions | Firm | None seen (member fee UNVERIFIED); Global Sources Some | Broad |
| Company lists sold as data; prospects by filter | Both | Strong (ZoomInfo; Kompass sells lists) | New |
| Product catalogues and third-party sellers | Product, firm | Strong (Amazon 8% to 45%; Daraz commission) | New |
| Businesses for sale | Firm | Unknown (OLX) | New |

### Professional and talent

| List type | Listed | Payment evidence | Vs founder's seed |
|---|---|---|---|
| Lawyers by speciality | Both | Strong in the US (Yelp, LSA); not shown elsewhere | Named |
| Accountants, tax specialists, financial planners, banks, insurers | Both | Some (LSA); banks Unknown (Yelp) | New |
| Data scientists, analysts, ML engineers | Individual | Strong on the recruiter side (Naukri, LinkedIn); none seen per listing | Named |
| Software, web and app developers | Individual | Some (Upwork, Fiverr) | New |
| Designers, illustrators, writers, translators, video and audio creatives | Individual | Some (Dribbble plans, USD 150 job board) | New |
| Digital marketers, virtual assistants, consultants | Both | Some | New |
| Software, design and marketing agencies; call centres | Firm | Some (UNVERIFIED) | New |
| Researchers and journals | Both | Some (organisations pay ORCID) | New |
| Job vacancies and employers with reviews and salaries | Firm | Strong (Naukri, Indeed); Glassdoor Some | New |
| Candidates, CV databases, profiles by skill | Individual | Strong (Naukri, LinkedIn Recruiter) | New |
| Customer requests (jobs, projects, care jobs) | Request | Some (Bark credits) | New |

### Travel and events

| List type | Listed | Payment evidence | Vs founder's seed |
|---|---|---|---|
| Hotels, B&Bs, resorts, campgrounds | Firm | Some (listed free; bookings commercial) | New |
| Vacation rentals, tours, cruises, flights | Both | Some (licence or contract only) | New |
| Attractions, museums, landmarks, outdoors | Place | None | New |
| Cinemas, arcades, casinos, venues, bars, clubs | Firm | Some (Yelp ads) | New |
| Events, festivals, what's on | Event | Unknown (Foursquare) | New |
| Wedding planners, caterers, DJs, decorators, halls; photographers | Both | Some (lead fees); pay report C | New |

### Retail and food (with beauty and fitness)

| List type | Listed | Payment evidence | Vs founder's seed |
|---|---|---|---|
| Restaurants, cafes, takeaways by cuisine | Firm | Some (ads); earns little (pay report) | New |
| Bakeries and cake shops | Firm | None seen | Named |
| Shops: furniture, books, electronics, clothing, music, home and garden | Firm | None seen | Named (furniture, bookshops) |
| Mobile phones and accessories, new and used | Both | Unknown (OLX, Daraz) | Named (mobile stores; no direct source) |
| Hardware shops | Firm | Unknown (none) | Named |
| Grocery, flower, laundry, delivery | Firm | Unknown (Justdial) | New |
| General for-sale classifieds; livestock, pets, pigeons | Both | Some (Facebook 10% shipping fee) | New |
| Salons, barbers, nail salons, spas, gyms, yoga | Both | Some (ads, LSA); earns little (pay report) | Named (beauty parlours); New |

### Civic and community

| List type | Listed | Payment evidence | Vs founder's seed |
|---|---|---|---|
| Government bodies and public offices | Firm (public) | None | New |
| Causes, communities, NGOs; community notices (lost and found, travel partners) | Group, individual | None seen | New |

### Software and topic lists

| List type | Listed | Payment evidence | Vs founder's seed |
|---|---|---|---|
| Software by category in ranked grids; "alternatives to X"; product launches | Product | Strong (G2, Capterra vendors pay); AlternativeTo Unknown | New |
| AI tools by function | Product | Some (submission USD 47 to 99, UNVERIFIED) | New |
| Websites and web tools by task; mobile apps by country | Product | Unknown (none) | New |
| Developer resource lists ("awesome") | Project | None | New |
| Books, films, TV, music, podcasts, games | Title | Some (Letterboxd plans; Goodreads affiliate) | New |
| Public figures (presidents, ministers, CEOs, judges, award winners); people from a place | Individual | None (Wikipedia) | New |
| Institutions with standard IDs (airports, universities, ports); fact lists, timelines | Institution, fact | None | New |
| Best-of, awards and tested-product lists by place | Firm, product | Some (ads, affiliate, Time Out Market rents) | New |
| Voted Top 10s, playlists, inspiration boards | Item | Some (Ranker ads; revenue UNVERIFIED) | New |

### Personal lists

| List type | Listed | Payment evidence | Vs founder's seed |
|---|---|---|---|
| Wish lists and registries (wedding, baby) | Individual | Some (Amazon commerce margin) | Broad |
| Task lists and templates | Individual | Some (subscriptions; template sales) | Broad |
| Saved places and map layers | Individual | None direct | Broad |
| Watch and reading lists | Individual | Some (Letterboxd) | Named (books read) |
| Alumni and classmates | Individual | Unknown (none) | Named (classmates) |

## Part 4. Rankings from the research

### 14 seed list types (pay report)

| # | Seed list type | Side | Pay grade | Where it is likeliest to pay first | Legal weight |
|---|---|---|---|---|---|
| 1 | Real estate agents and developers | Business pays | A | UAE, Pakistan, Nigeria, Egypt, Brazil, Mexico | Low for firms |
| 2 | Vehicle dealers, car hire, auto-parts sellers | Business pays | B | Pakistan, Nigeria, UAE, Mexico, Brazil, Turkey | Low |
| 3 | Movers and packers, pest control, home repair and trade firms | Business pays | A | India analogues, UAE, Pakistan, Gulf cities | Medium (sole traders) |
| 4 | Clinics, diagnostic centres, dentists, with equipment and dated prices | Business and buyer pay | B | Pakistan, UAE, Saudi (regulated prices) | High for named doctors, medium for facilities |
| 5 | Pharmacies, medical stores and pharma distributors | Buyer pays | B | Pakistan, Egypt, Nigeria, Bangladesh | Low |
| 6 | Industrial machinery and equipment suppliers | Business and buyer pay | B | Turkey, Vietnam, Mexico, Pakistan | Low |
| 7 | Construction materials, hardware, steel and tiles | Business pays | B | Egypt, Pakistan, Nigeria, Saudi, Turkey | Low |
| 8 | Packaging, electrical and electronics suppliers | Business and buyer pay | B | Vietnam, Mexico, Turkey, Pakistan | Low |
| 9 | Manufacturers and exporters by sector (garments, surgical and sports goods, food and agri) | Buyer pays | C | Bangladesh, Pakistan (Sialkot), Vietnam, Kenya, Brazil | Low |
| 10 | Importers and distributors in destination markets | Buyer pays | C | UAE, Turkey, Mexico, Brazil | Low |
| 11 | Mobile phone and electronics distributors and shops | Business pays | C | Pakistan, Nigeria, UAE, Vietnam, Indonesia | Low |
| 12 | Lawyers, accountants, financial and insurance firms | Business pays | A in the US, C elsewhere | Gulf, Brazil, Mexico (firms only) | Medium |
| 13 | Wedding and event vendors | Business pays | C | Large cities in every market | Low |
| 14 | Heavy equipment and crane rental | Business and buyer pay | C (H) | Pakistan, Gulf | Low |

### Ten most promising groups (platform report, section 5)

| Rank | Add | Why it ranks here | Evidence | Pay report |
|---|---|---|---|---|
| 1 | Urgent home and trade firms (movers, pest control, AC and appliance repair, plumbing and electrical firms, cleaning) | Urban Company, Angi, Thumbtack, Justdial and Google host it. Money follows job size. Firms carry less legal weight than individuals | Strong | A; test 2 |
| 2 | Health facilities and equipment (labs, imaging centres, hospitals, clinics, dentists; installed machines; equipment suppliers) | Facility-first avoids named doctors. Zocdoc charges per booking; IMV sells machine data. Pilot default: eye hospitals, then schools, then contractors. No Pakistani buyer shown | Strong in US; weak in PK | B (US), C (PK); test 1 |
| 3 | Manufacturers, exporters, building suppliers by sector and cluster (Sialkot, textiles, leather, agri-food, packaging, chemicals) | IndiaMART and Alibaba earn mainly from paying suppliers. TDAP and chambers are ready registers (decision D21) | Strong for the model; none seen for TDAP | B industrial, C exporters; test 3 |
| 4 | Importers and buy leads | IndiaMART sells leads. LCCI lists 9,396 importers in Lahore alone. Pair with rank 3 | Strong at IndiaMART; unproven in PK | C |
| 5 | Export services (freight, customs agents, packaging, testing labs) | Same buyer as rank 3; firms; low legal weight | Strong (IndiaMART) | Not ranked |
| 6 | Real estate agents, developers, new projects, housing societies | Every property portal hosts it, but portals own the supply. Start where a data gap shows. Not named in `DECISIONS.md` section 8 | Strong | A; C for a new entrant |
| 7 | Vehicle dealers and used-car lists | CarGurus earns about 90% from dealers. PakWheels payment not stated | Strong (US); Unknown (PK) | B |
| 8 | Software, app and AI-tool lists | No place data needed; products, not people. No Pakistani buyer shown | Some | Not covered |
| 9 | Data scientists and other talent | Recruiters pay; individuals list free. Decision: design now, launch after a pilot of about 50 consented people and counsel | Strong (buyer side) | A (professionals) |
| 10 | Colleges, coaching centres, schools by board | Free traffic anchors, not revenue | Some | D for revenue |

### Avoid or delay

| Type | Why | Working rule |
|---|---|---|
| Children: Quran tutors, tutors, babysitters, nannies, daycare, madrasas | Child-facing | Not public until safeguarding and relay-only contact are designed; schools and centres first |
| Health data: patient data, ratings of doctors, mental, sexual-health and pregnancy services | Sensitive; price and ad rules apply | Adopt the health rules before any price is collected; dated prices, no "cheapest" claims, no patient data |
| Named individuals: doctors, nurses, lawyers, plumbers, tutors, domestic workers, candidates | Pakistan had no enacted data law as of May 2026 (pay report) | Consent only; contact through the platform; area only; counsel first |
| Public figures and "people from X" | Named people | Sourced entries only; legal check first |
| Alumni and classmates | Personal | Private by default |
| Copying other platforms' data | Yelp restricts storage; G2, Capterra, Goodreads are not for copying | Use open data; no scraping of Google Maps or Facebook until counsel advises |
| Individual for-sale ads (property, vehicles) | OLX, Zameen, PakWheels own them | List the firms; revisit later |
| Restaurants, shops, attractions as revenue lists | Free everywhere; low ad value (pay report) | Free anchors only |
| Ambulance, blood banks, madrasas | No platform hosts them | Research sources first |

### Three to test first with real buyers

1. Health facilities with equipment and dated prices (Islamabad and Rawalpindi), plus pharmacies in one city.
2. Urgent home and trade-service firms (movers, pest control, repair, plumbing firms) in one city or housing society.
3. Manufacturers, exporters and building-material suppliers in one cluster (for example Sialkot).

### Earn little (free anchors only)

Restaurants, retail shops, groceries, beauty, education leads, cleaning and handyman jobs, bare contact files.

## Part 5. Loaded in the software

Created by `seed_taxonomy`. Natural scale: hyper_local, city, national, global. Flags: individual (named people, consent needed), child (children's services, not public until safeguarding is designed), health, paused (talent list, launch after a pilot).


### Manufacturing and trade

| List type | Natural scale | Flags |
|---|---|---|
| Surgical instrument makers | national | - |

### Health

| List type | Natural scale | Flags |
|---|---|---|
| Doctors | hyper_local | individual, health |
| Eye doctors | hyper_local | individual, health |
| Nurses | hyper_local | individual, health |
| Hospitals | city | health |
| Eye hospitals | hyper_local | health |
| Medical stores and pharmacies | hyper_local | health |
| MRI and imaging centres | city | health |
| Laboratories | city | health |

### Education

| List type | Natural scale | Flags |
|---|---|---|
| Schools | city | - |
| Quran tutors | hyper_local | individual, child |
| Tutors | hyper_local | individual, child |
| Bookshops | city | - |

### Trades and services

| List type | Natural scale | Flags |
|---|---|---|
| Plumbers | hyper_local | individual |
| Electricians | hyper_local | individual |
| Mobile phone repair | hyper_local | - |
| Beauty parlours and salons | hyper_local | - |
| Contractors | national | - |
| Real estate agents | city | - |
| Data scientists | global | individual, paused |

### Manufacturing and trade

| List type | Natural scale | Flags |
|---|---|---|
| Football makers | national | - |
| Fan makers | national | - |
| Sanitaryware makers | national | - |
| Furniture makers | national | - |
| Factories and suppliers | national | - |

### Retail

| List type | Natural scale | Flags |
|---|---|---|
| Bakeries | hyper_local | - |
| Mobile stores | hyper_local | - |
| Spare parts shops | hyper_local | - |
| Furniture stores | city | - |
| Hardware shops | hyper_local | - |

### Hospitality and fuel

| List type | Natural scale | Flags |
|---|---|---|
| Hotels | city | - |
| Petrol pumps | hyper_local | - |
