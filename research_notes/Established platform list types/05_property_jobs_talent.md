# Group 5: property, vehicles, classifieds, jobs, talent networks (platforms 36 to 44)

Researched 2026-10-05 for AllLists.org. Method: about 30 WebSearch queries (the session search cap was then reached, so a few follow-ups were not run). WebFetch was tried once (rozee.pk) and blocked by the egress proxy. Findings rely on search snippets, so single-source or undated figures are marked UNVERIFIED. Items marked "(background)" come from general knowledge, not from a fetched source, and are also UNVERIFIED.

## 1. Per-platform findings

### 36. Property portals (Zillow, Rightmove, Zameen, Property Finder, Bayut)

**Zameen (PK)**
- Top-level taxonomy is Homes, Plots, Commercial.
  - Homes: houses, flats, upper portion, lower portion, farm houses, rooms.
  - Plots: residential plots, commercial plots, agricultural land.
  - Commercial: offices, shops, warehouses, factories, buildings, other commercial.
  - Source: https://help.zameen.com/hc/en-us/articles/5644114679837-What-are-different-property-types
- Entities are listings, agents or agencies, developers or projects, and society or plot maps.
  - Agent pages are organised by city, e.g. https://www.zameen.com/agents/Karachi/Adnan_Associates_Builders_And_Realtors-194231/
  - Agency names often include "Builders And Realtors", so builders and agents overlap.
- Plot Finder shows the on-ground location of over 1.2 million houses and plots (2019 launch, UNVERIFIED as current): https://propakistani.pk/2019/11/22/zameen-com-launches-new-plot-finder-tool-to-facilitate-online-plot-searching/
- Scale (undated, UNVERIFIED): 14,500 registered agents, 1,000 developers, and about 500,000 new listings a month. Agents estimate 70% of PK transactions start on Zameen. Sources: https://restofworld.org/2021/how-zameen-dominated-pakistans-real-estate-market/ and https://app.dealroom.co/companies/zameen_com
- Payment: agents and developers pay for listings, advertising and lead generation. The packages themselves were not verified.

**Bayut (UAE)**
- Listings are apartments, villas, offices, shops and other residential or commercial types, across all seven emirates.
- It claims more than 1,200 agencies and keeps a brokers and agents directory. Source: https://bayut.com/about/
- Verification products: TruCheck (listing verification), TruBroker (agent recognition), TruEstimate (valuation), and Dubai Transactions data from the Dubai Land Department.
- Payment: agencies and brokers (the exact model was not verified).

**Property Finder (UAE)**
- Search entity types are property, project, agent, agency and location. Properties are residential or commercial, for sale or rent: apartments, houses, offices and plots.
- One scraper listing counts 15,705 agents (UNVERIFIED, third-party scraper page): https://apify.com/drramerets/propertyfinder-agents
- Agent profile fields:
  - licence number, languages, nationality
  - super agent status, verification status
  - listing counts (residential and commercial, sale and rent)
  - ratings and reviews, WhatsApp response time, claimed deals
  - Source: https://apify.com/xtracto/propertyfinder-dubai-leads
- Payment: agents pay for listings (the exact model was not verified).

**Rightmove (UK)**
- Subscription model for property professionals: estate agents, lettings agents and new-home builders. Rightmove's report puts agency-related revenue at 72%, new-homes developers at 18%, and commercial, data and overseas at 10% (for 2024).
- 16,591 agency branches at 30 June 2026. Average revenue per advertiser (ARPA) was GBP 1,636 a month in H1 2026, and new-homes advertisers paid GBP 2,247 a month. Source: https://www.estateagenttoday.co.uk/breaking-news/2026/08/if-agents-hate-rightmove-why-do-more-join-and-pay-higher-fees/
- Search types seen in listings: houses, bungalows, flats and park homes (https://www.rightmove.co.uk/press-centre/?p=859). Land, retirement, shared ownership, student, commercial and overseas are UNVERIFIED (background).
- Agents are listed per branch, so the natural unit is the branch.

**Zillow (US)**
- Segments are Residential, Mortgages, Rentals and Other. Brands include Zillow, Trulia, StreetEasy, HotPads and Zillow New Construction.
- The Professional Directory (2008 launch) has 6 categories: Property Managers, Real Estate Agents, Real Estate Services, Photographers, Home Inspectors, Home Improvement. It is open to stagers, lenders, contractors, landscapers and architects.
  - https://zillow.mediaroom.com/2008-10-02-Zillow-Professional-Directory-Connects-Consumers-With-Local-Professionals
  - Per-city pages such as https://www.zillow.com/professionals/home-inspector-reviews/gilbert-az/
- Payment: Premier Agent advertising is bought by ZIP code. The top three ranked agents in a ZIP code get Agent Finder placement. Rentals also sell advertising and tools to landlords and property managers. Source: https://bstrategyhub.com/how-does-zillow-make-money/ (secondary source).

### 37. Vehicles (PakWheels, Autotrader, CarGurus)

**PakWheels (PK)**
- Covers cars, bikes and auto parts or accessories, with 200,000+ vehicles for sale and 3 million+ buyers a month (undated app-store claim, UNVERIFIED).
- Filter dimensions: city, make, model, transmission, CC, body type, generation, colour, registration city.
- Curated lists: Japanese, hybrid, imported, luxury, automatic, 1000cc, sports and modified cars. Source: https://apps.apple.com/us/app/-/id739776365
- Dealer directories by vehicle type and city, e.g. https://www.pakwheels.com/used-bikes/dealers/lahore/2952556
- Payment (background, UNVERIFIED): paid and featured ads, dealer packages.

**Autotrader UK**
- Advertising packages and fees vary by vehicle type (cars, vans and others). Retailers choose private or trade seller status and a price band. Retailers pay monthly package fees, and admin-fee configuration is documented. Sources: https://help.autotrader.co.uk/hc/en-gb/articles/9084202545437 and https://www.nfda-uk.co.uk/press-room/newsletter/2021/7/auto-trader-announces-admin-fee-changes-for-dealers-adverts-on-its-marketplace
- More than 50 million cross-platform visits a month (https://en.wikipedia.org/wiki/Autotrader_Group, undated).
- Bikes, caravans, plant and farm categories were not confirmed (background). Gumtree does confirm them for classifieds.

**CarGurus (US)**
- Dealers get Basic Listing (free) or paid Enhanced and Featured listings. Subscriptions are about 90% of revenue.
- Year-end 2017: 27,670 dealers (25,122 US, 2,548 international), and average annual revenue per US subscribing dealer of USD 12,055. More recently about 24,500 dealers (UNVERIFIED, undated). Source: https://investors.cargurus.com/node/6966

### 38. General classifieds (OLX, Craigslist, Gumtree, Facebook Marketplace)

**OLX Pakistan**
- Categories include:
  - Mobiles: phones, accessories, tablets, smart watches, mobile numbers.
  - Vehicles: cars, car accessories, spare parts, car care, rickshaw and chingchi, buses/vans/trucks, tractors and trailers, oil and lubricants, boats.
  - Property for sale: land and plots, houses, apartments, shops/offices/commercial, portions.
  - Property for rent.
  - Electronics and home appliances.
  - Kids.
  - Jobs.
  - Business, Industrial and Agriculture: food and restaurants, trade and industrial machinery, medical and pharma, business for sale, construction and heavy machinery, agriculture.
  - Services: tuitions and academies, home and office repair, car rental, domestic help, web development, drivers and taxi.
  - Animals: livestock, pet food, pigeons and other animals.
- Location hierarchy runs down to neighbourhood level, for example `olx.com.pk/basti-samlan_g4664/livestock_c1960`.
- Scale: 40,000+ listings a day across 14 categories, 950,000+ daily users, 12,000 mobile ads a day, and about 100,000 live vehicle ads (undated press, UNVERIFIED). Sources: https://profit.pakistantoday.com.pk/2017/04/17/olx-simple-easy-fast and https://www.olx.com.pk/jobs_c4
- Payment (background): featured ads and business packages.

**Craigslist**
- Sections: community, services, discussion forums, housing, jobs, for sale, gigs, resumes, wanted.
- Housing: apartments, rooms and shares, sublets, vacation rentals.
- Jobs are split by sector (accounting, admin, healthcare, sales, tech, and others).
- Services are split into automotive, beauty, computer, legal and so on.
- Organised strictly by city site. Source: secondary guides only, e.g. https://z28.zyxware.com/blog/craigslist-metrowest-boston (UNVERIFIED). Fee categories were not searched; paid categories are jobs and some housing in some cities (background, UNVERIFIED).

**Gumtree (UK)**
- Top-level: for sale, cars-vans-motorbikes, flats-houses (property), jobs, pets, community, services, business-services.
- Vehicles: cars, motorbikes and scooters, vans, campervans and motorhomes, caravans, trucks, plant and tractors, parts.
- Property: for sale, to rent, to share, to swap, commercial, parking and garage.
- Services (17 groups): business and office, childcare, clothing, computers and telecoms, entertainment, finance and legal, food and drink, goods suppliers, health and beauty, motoring, pets, property and maintenance, tradesmen and construction, transport, travel, tuition, weddings.
- Source: https://www.gumtree.com/termsofuse2020 and category pages.

**Facebook Marketplace**
- Categories: Vehicles, Property Rentals, Home Sales, Apparel, Electronics, Home Goods, Toys, Musical Instruments, Health and Beauty, Garden and Outdoor, Sports, Home Improvement, Family and Baby, Free Stuff.
- Listing is free. Shipped orders carry a 10% fee with a USD 0.80 minimum (from 15 April 2024). Local pickup is free. Source: https://litcommerce.com/blog/facebook-marketplace-fees/ and https://www.inventorysource.com/does-facebook-marketplace-charge-fees/
- Cars and rentals face stricter rules (2022): https://www.ecommercebytes.com/2022/09/29/facebook-marketplace-cracks-down-on-cars-and-rental-listings/

### 39. Job boards (Indeed, Naukri, Rozee.pk, Glassdoor)

**Rozee.pk (PK)**
- Search dimensions: experience, job title, skills, career level, gender, functional area, company, city.
- Functional areas: accounts/finance, admin operations, bank operations, business development, corporate affairs, creative design, consultant, engineering, education and training, graphic design, health care, HR, legal, field operations, management consulting, M&E.
- Industries: sales and marketing, software and web, accounting and finance, customer service, distribution and logistics, healthcare, civil engineering, retail.
- Cities: Lahore, Karachi, Islamabad, Rawalpindi, Faisalabad, Multan, Gujranwala, Quetta, Peshawar, Sialkot, Hyderabad.
- Pages: https://www.rozee.pk/jobs-by-functional-area and https://www.rozee.pk/EN/jobs-by-industry. Both were seen in the search index only, because the fetch was blocked.
- 70,000+ registered employers and 5 million+ registered professionals (undated, UNVERIFIED).
- Data-science and ML titles appear as individual job pages, e.g. https://www.rozee.pk/computer-house-ml-engineer-jobs-1867467
- Payment: employer job postings and CV access (background).

**Naukri (India)**
- Browse by category (IT, sales, marketing, data science, HR, engineering), city, skill, designation, and company type (unicorn, MNC, startup, product, internet). Matching uses functional area, department, role and industry.
- Data science is a top-level category, so it is a first-class list.
- Source: https://www.naukri.com/blog/naukri-jobspeak-report/amp. Pricing was not found (search cap).

**Indeed**
- Organic posts are free. Sponsored jobs are pay-per-click, up to USD 5+ a click in competitive markets. Resume database access costs roughly USD 120 to 300 a month for 30 to 100 contacts. Source: https://www.pin.com/blog/indeed-pricing (third-party, UNVERIFIED).
- Also hosts company pages with reviews and salaries, and a CV database. Available in 60 countries and 28 languages.
- Job category tree: UNVERIFIED (not retrieved).

**Glassdoor**
- Company-centred lists: reviews, salaries (high or low confidence by data points), interviews, benefits, CEO approval.
- 33 million reviews and insights covering about 700,000 companies (undated, UNVERIFIED).
- Enhanced Profile starts at USD 8,000 for 12 months. Source: https://vator.tv/?p=32708 (old article) and https://www.selecthub.com/p/recruiting-software/glassdoor-for-employers/

### 40. LinkedIn

- 1.2 billion members, USD 17.81 billion revenue in Microsoft FY2025 (https://news.linkedin.com/2025/Q4FY25_Earnings_Highlights and secondary stats pages).
- Skills Graph: about 39,000 skills (earlier figure 41,000), 26 languages, 374,000 aliases, 200,000+ links between skills, with skill type and ID per entry. https://engineering.linkedin.com/blog/2023/Building-maintaining-the-skills-taxonomy-that-powers-LinkedIns-Skills-Graph
- Entity types: person profile, Company Page, University Page, Showcase Page, Product Page, Service Page, and Group. Source: https://www.linkedin.com/help/lms/answer/a727893
- Services Marketplace: freelancers list services free across about 250 categories (accounting, consulting, IT, software and others). It is organised by service, location and language. Source: https://itpro.com/business-strategy/careers-training/361383/linkedin-rolls-out-service-marketplace-globally. The 250 count comes from a secondary source, UNVERIFIED.
- Payment:
  - Premium Career about USD 29.99 a month.
  - Premium Business about USD 59.99, Sales about USD 79.99, Hiring about USD 119.95.
  - Recruiter Lite about USD 170 a month. Corporate seats are about USD 835 to 1,080 a month (UNVERIFIED, third-party).
  - Source: https://www.subscriptioninsider.com/article-type/news/linkedin-streamlines-premium-subscription-plans-raises-prices
  - Also ads, job posts and Sales Navigator (background).

### 41. Research and developer talent (GitHub, Kaggle, ORCID, ResearchGate, Google Scholar)

**GitHub**
- 180 million+ developers, 630 million repositories, 36 million new developers in the year. India overtook the US in contributor count. Source: https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/
- Lists by language, topic, collection and sponsorship (background, UNVERIFIED). Talent is not organised as a directory. Profiles are discoverable via search by location and language.
- Payment: Teams and Enterprise seats, Sponsors (background).

**Kaggle**
- 23.29 million accounts at 2 April 2025, of whom 2,973 are Masters and 612 are Grandmasters. Source: https://en.wikipedia.org/wiki/Kaggle
- Five tiers (Novice, Contributor, Expert, Master, Grandmaster), earned in four tracks: Competitions, Datasets, Notebooks, Discussions.
- This is the clearest verified ranking-based list of data scientists. Rank is evidence-based. Recruiters use it as a talent pool (https://www.pin.com/blog/find-data-science-talent-kaggle).
- Jobs board: UNVERIFIED.

**ORCID**
- 10.5 million active users and 1,500+ member organisations in 69 countries at end 2025 (earlier sources cite 14.7 million issued iDs, 2022). Source: https://aaf.edu.au/wp-content/uploads/ORCID-YIR-2025-v3.pdf
- Individuals are free. Organisations pay: USD 1,490 (startups) to USD 29,855 (large commercial), and USD 4,775 for non-profit and government (2026). Source: https://info.orcid.org/membership
- The natural entry key is the person's iD, with affiliations and works attached.

**ResearchGate**
- 25 million+ members, mostly medicine and biology, with research interests that members follow (https://en.wikipedia.org/wiki/ResearchGate). Pricing not found.

**Google Scholar**
- Profiles carry free-text interest labels that act as list keys. Google Scholar Metrics lists the top 100 publications by language and by broad area, then subcategory, ranked by h5-index. Source: https://scholar.google.com/intl/en/scholar/metrics.html. Free.

### 42. Creative talent (Behance, Dribbble)

**Behance**
- 56 million+ members (December 2024), 8.8 million published projects, 11,500 uploads a day (https://en.wikipedia.org/wiki/Behance).
- Hire page filters by location, creative field, tools and school.
- Creative field taxonomy is long, about 70 fields, including: advertising, animation, architecture, branding, character design, cinematography, fashion, furniture design, game design, graphic design, illustration, industrial design, interior design, jewelry design, landscape design, motion graphics, music, packaging, photography, product design, programming, UI/UX, web development. Source: https://help.behance.net/hc/en-us/articles/204484044-Guide-Discover-Creative-Work-on-Behance
- Also 100+ galleries and a Featured Freelancers badge.
- Free for creators. Employer job posts are paid (details UNVERIFIED).

**Dribbble**
- Pro designer plans: USD 8 a month or USD 48 a year, and USD 99 a month for the agency plan.
- Employers pay USD 150 a month for a Job Board listing, or USD 300 a month for a Hiring Suite. Source: https://help.dribbble.com/en/articles/11062025-dribbble-pricing-and-payment-terms
- Discovery tags: UI/UX, branding, illustration, animation, print, product design, typography, web design. Designers carry skill, location and availability filters.

### 43. Company and people databases (Crunchbase, Apollo, ZoomInfo)

- **Crunchbase**: covers companies, investors, funding rounds, people, IPOs and acquisitions.
  - May 2019: 760,590 organisations, 121,509 investors, 263,426 funding rounds, 890,429 people. Now 3 million+ companies (UNVERIFIED).
  - Sources: https://research.unipd.it/handle/11577/3341496 and https://apify.com/themineworks/crunchbase-companies
  - Pricing not retrieved.
- **Apollo**: 275 million contacts and 73 million companies. Free plan has 100 credits. Paid plans run USD 49 to 119 per user per month, billed annually, with credits. Source: https://www.artisan.co/blog/apollo-io-review (third-party, UNVERIFIED).
- **ZoomInfo**: claims 265 million to 420 million contacts and 100 million to 145 million companies (estimates vary). Annual contracts of USD 15,000 to 40,000 are required. Source: https://bouncezero.io/zoominfo-review-2026 (UNVERIFIED).
- All three sell filtered lists: company or contact lists by industry, size, location, technology used, funding stage and buying intent. Lists are the product.

### 44. Daraz and Amazon

- **Daraz (PK)**: more than 10 million products across 100 categories, 5 million+ monthly app users (undated, UNVERIFIED). Sellers pay a category-based commission (see "Daraz University" for the table). Source: https://www.daraz.pk/sell/ and https://vizologi.com/business-strategy-canvas/darazpk-business-model-canvas/
- **Amazon**: tens of thousands of browse nodes (July 2025). Electronics was 38% of 2025 sales. Referral fees range from 8% to 45% and most categories are 15%, with a USD 0.30 per-item minimum on most. Sources: https://feedonomics.com/blog/amazon-category-taxonomy/ and https://www.amzadvisers.com/amazon-referral-fees-optimization/
- **Amazon Home Services**: about 700 services in 41 US states, with partners such as TaskRabbit. Categories are assembly, cleaning, home theater, home improvement, computers and electronics, yard and outdoors, business and commercial, smart home. Source: https://www.retaildive.com/news/amazon-launches-professional-services-marketplace/380848 (2015 article, programme status UNVERIFIED).
- **Amazon Business**: 8 million+ business customers and USD 35 billion annualised sales (2025). Source: https://www.marketplacepulse.com/articles/amazons-35-billion-b2b-marketplace

## 2. Master table of distinct list types

Scale legend: HL = hyper-local (neighbourhood), City, Nat = national, Glob = global.
Payment evidence: Y = payment seen in a cited source, Y? = single or secondary source, bg = background only, none = no payment seen.

| # | List type | Platforms | Individual or firm | Natural scale | Payment evidence |
|---|---|---|---|---|---|
| 1 | Property for sale (houses, flats, plots, land) | Zameen, Zillow, Rightmove, Bayut, PF, OLX, Gumtree | Both | City to Nat | Y (Rightmove subscriptions) |
| 2 | Property for rent, to share, to swap | Zillow Rentals, Rightmove, OLX, Gumtree, Craigslist, FB | Both | City | Y (Zillow Rentals ads) |
| 3 | Commercial property (offices, shops, warehouses, factories) | Zameen, Bayut, PF, Gumtree, OLX | Firm | City | Y? |
| 4 | New-build developments and projects | Rightmove, PF, Zillow New Construction, Zameen | Firm | City to Nat | Y (GBP 2,247 a month) |
| 5 | Housing societies and plot maps | Zameen | Firm | City | Y? |
| 6 | Real estate agents and agencies | All five property portals | Both | City | Y |
| 7 | Property developers and builders | Zameen (1,000), Rightmove | Firm | City to Nat | Y? |
| 8 | Property managers and landlords | Zillow | Both | City | Y |
| 9 | Home inspectors | Zillow | Both | HL to City | Y? |
| 10 | Real estate photographers | Zillow | Individual | City | none seen |
| 11 | Home improvement pros, contractors, landscapers, architects, stagers | Zillow, Gumtree, Craigslist, OLX | Both | HL to City | Y? |
| 12 | Mortgage lenders and brokers | Zillow | Firm | Nat | Y |
| 13 | Parking and garage spaces | Gumtree | Both | HL | bg |
| 14 | Used cars | PakWheels, Autotrader, CarGurus, OLX, Gumtree, FB | Both | City to Nat | Y |
| 15 | New cars | PakWheels, Autotrader | Firm | Nat | bg |
| 16 | Bikes, scooters | PakWheels, Gumtree, OLX | Both | City | bg |
| 17 | Vans, trucks, buses, plant, tractors | Gumtree, OLX | Both | City to Nat | bg |
| 18 | Caravans, campervans, boats | Gumtree, OLX | Both | Nat | bg |
| 19 | Car dealers | PakWheels, CarGurus, Autotrader | Firm | City | Y (CarGurus, Autotrader) |
| 20 | Auto parts and accessories | PakWheels, OLX, Gumtree | Both | City | bg |
| 21 | Curated vehicle lists (hybrid, imported, luxury) | PakWheels | n/a | Nat | none |
| 22 | General for-sale classifieds (furniture, electronics, appliances, clothing) | OLX, Craigslist, Gumtree, FB | Individual mostly | HL to City | Y (FB shipping fee 10%) |
| 23 | Mobile phones and accessories | OLX, Daraz | Both | City | bg |
| 24 | Livestock, pets, pigeons | OLX, Gumtree | Both | HL | bg |
| 25 | Business for sale | OLX | Firm | Nat | bg |
| 26 | Industrial and agricultural machinery | OLX | Both | Nat | bg |
| 27 | Tuition and academies | OLX, Gumtree | Both | City | bg |
| 28 | Local services (repair, domestic help, drivers, rental, weddings, childcare, beauty) | OLX, Gumtree, Craigslist | Both | HL to City | bg |
| 29 | Professional services (legal, finance, computer, business) | Gumtree, Craigslist, LinkedIn | Both | City to Glob | Y? |
| 30 | Community: events, groups, lost/found, travel partners | Craigslist, Gumtree | Individual | HL | none |
| 31 | Jobs by functional area or industry | Indeed, Naukri, Rozee, Craigslist | Firm | City to Nat | Y (Indeed PPC) |
| 32 | Jobs by city | Rozee, Naukri | Firm | City | Y |
| 33 | Jobs by company type (startup, MNC, unicorn) | Naukri | Firm | Nat | Y? |
| 34 | Employers and company profiles with reviews | Glassdoor, Indeed, Naukri | Firm | Nat to Glob | Y (USD 8,000+) |
| 35 | Salary lists by role and company | Glassdoor, Indeed | Firm/role | Nat | none direct |
| 36 | Resumes and candidate database | Indeed, Naukri, Rozee, Craigslist | Individual | Nat | Y (Indeed USD 120 to 300 a month) |
| 37 | Professional profiles tagged by skill | LinkedIn, Rozee | Individual | Glob | Y (Recruiter) |
| 38 | Skill taxonomy as list key (about 39,000 skills) | LinkedIn | n/a | Glob | Y (via Recruiter) |
| 39 | Freelance services by category (about 250) | LinkedIn, Behance | Both | Glob | Y? |
| 40 | Company, school and product pages | LinkedIn | Firm | Glob | Y |
| 41 | Developers (by language, topic, location) | GitHub | Individual | Glob | bg |
| 42 | Data scientists ranked by tier | Kaggle | Individual | Glob | none seen |
| 43 | Researchers by iD, interest, institution | ORCID, ResearchGate, Google Scholar | Individual | Glob | Y (ORCID org fees) |
| 44 | Journals and publications ranked by h5 | Google Scholar Metrics | Firm | Glob | none |
| 45 | Creative professionals by field (about 70) | Behance, Dribbble | Individual | Glob | Y (Dribbble) |
| 46 | Design job listings | Dribbble | Firm | Glob | Y (USD 150 a month) |
| 47 | Companies and investors by industry, funding | Crunchbase | Firm | Glob | Y? |
| 48 | Sales prospects and contacts by filter | Apollo, ZoomInfo | Individual and firm | Glob | Y (USD 15,000+ a year) |
| 49 | Product catalogues by category | Daraz, Amazon | Product | Nat | Y (commission 8% to 45%) |
| 50 | Third-party sellers and stores | Daraz, Amazon | Firm | Nat | Y |
| 51 | Home services bundle (assembly, cleaning, yard) | Amazon Home Services | Both | City | Y? |
| 52 | B2B suppliers and procurement | Amazon Business | Firm | Nat | Y? |

## 3. List types not in the seed set

Existing seeds: petrol pumps, schools, beauty parlours, bakeries, mobile stores, mobile repair, spare parts, furniture, pharmacies, doctors, nurses, lawyers, bookshops, hardware, MRI machines, plumbers, Quran tutors, factories.

New candidates, with the strongest first:
1. **Real estate agents and agencies** (rows 6, 7). Priority, because the founder named them. Zameen, Property Finder and Bayut all run city-based agent directories.
2. **Builders, contractors and developers** (rows 7, 11). Zameen has "Builders and Realtors" and 1,000 developers. Zillow has home-improvement pros, landscapers and architects. Gumtree has "Tradesmen & Construction".
3. **Data scientists, ML engineers, data analysts, data engineers** (rows 36, 37, 42). Priority, because the founder named it. See section 4 for the structure.
4. **Software developers by language and location** (row 41).
5. **Researchers and academics** (row 43).
6. **Designers and creatives** (row 45).
7. **Freelancers by service category** (row 39).
8. **Employers by industry** (row 34).
9. **Used car dealers** and **motorbike dealers** (row 19).
10. **Car rental, taxi and driver services** (OLX services).
11. **Livestock and pet sellers** (row 24).
12. **Industrial and agricultural machinery sellers**, plus **construction and heavy machinery** (row 26).
13. **Real estate photographers**, **home inspectors**, **stagers**, **property managers** (rows 8 to 10).
14. **Housing societies and developments** (rows 4, 5).
15. **Mobile numbers** (a OLX sub-category; likely out of scope).
16. **Parking and garage spaces**.
17. **Companies by industry, with funding and technology** (rows 47, 48).
18. **Mortgage lenders and brokers**.
19. **Boats, tractors, rickshaws, campervans** (vehicle sub-types).
20. **Journals** (row 44).

## 4. Gaps and caveats

- **Data science structure**
  - No platform publishes a clean sub-role taxonomy. Naukri makes "Data Science" a top-level category, LinkedIn tags people by skill, and Kaggle ranks people by tier in four tracks.
  - Role splits found were secondary only: data scientist, data analyst, data engineer, ML engineer, BI analyst, research scientist, MLOps. Source: https://datatalks.club/podwiki/wiki/data-roles/ (UNVERIFIED).
  - Dimensions seen on platforms: skill, tier, city, experience.
  - Open question: how to list data scientists globally without a place. Candidate keys are skill, tier or institution, plus country of residence.
- **Not retrieved** (search cap or blocked pages):
  - Craigslist paid categories (jobs, housing in some cities, cars by dealer). Treat as UNVERIFIED.
  - Autotrader listing and retailer counts.
  - PakWheels dealer and pricing detail.
  - Naukri and Rozee employer pricing.
  - Indeed's official category tree.
  - Crunchbase tiers.
  - Daraz seller counts.
  - Rightmove's complete property-type filters (land, retirement, shared ownership, student, commercial, overseas).
  - Zameen listing packages.
  - Bayut and Property Finder fee levels.
- **Source quality**: many numbers come from scraper pages, review blogs and press snippets, and several are undated. Treat them as order-of-magnitude only.
- **Contractors**: the platforms here host them only as sub-lists (Zillow Home Improvement, Gumtree Tradesmen and Construction, OLX Home and Office Repair). Dedicated contractor marketplaces (Angi, Houzz, Urban Company) belong to Group 3 and should be cross-referenced.
- **Not verified in this group**: whether any platform charges a per-entry fee for talent lists. In the evidence, individuals list free (LinkedIn, Behance, GitHub, ORCID, Scholar). Payment comes from the buyer side: recruiters, employers, advertisers, agents and sellers.
