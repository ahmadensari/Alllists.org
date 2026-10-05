# Which business lists and databases buyers actually pay for (list purchase and data licensing)

Research date: 2026-10-05. Method note: WebSearch only; WebFetch was blocked by the egress proxy for prospeo.io, postcardmania.com, leadgenius.com, bolddata.nl, niir.org, datarade.ai and mediapost.com, so no vendor page could be opened and verified. Every price below comes from search-result summaries (snippets), not from a page read in full. Treat all vendor and aggregator prices as SECONDARY and unverified. Many snippets carried no date; where undated this is stated. Search-result summaries did not always say which URL a figure came from; where that is the case it is flagged.

## 1. Best-selling list categories and which industries are most requested

### Takeaway
The commercial B2B data market is dominated by contact and leads data for sales prospecting, sold as subscriptions (ZoomInfo, Apollo, Lusha, Cognism) or credits, and by firmographic/risk data (D&B). Healthcare professional data is the single most visibly segmented vertical on Datarade. I found NO verified marketplace sales rankings by industry, so "best-selling by industry" is inferred from catalogue breadth, not from sales data.

### Cited Findings
- ZoomInfo FY2025 GAAP revenue was $1,249.5 million (+3% YoY); over 35,000 companies are customers; 1,921 customers pay $100,000+ ACV (more than 50% of total ACV); net revenue retention was 90% at 31 Dec 2025 (press-release figures as summarised by search; 10-K FY2025 exists at the SEC link but was not opened). Revenue is "substantially all" subscriptions; pricing is based on functionality, users and records under management; about 53% of contracts (by annualised value) are multi-year. — [ZoomInfo FY2025 10-K](https://www.sec.gov/Archives/edgar/data/1794515/000179451526000012/zi-20251231.htm); [ZoomInfo Q4/FY2025 results](https://www.businesswire.com/news/home/20260209677262/en)
- Dun & Bradstreet FY2024 revenue was $2,381.7 million (+2.9%); Data Cloud covers nearly 600 million organisations; about 215,000 customers worldwide at 31 Dec 2024. FY2025 D&B figures were not found (the FY2025 D&B material appears only as exhibits to Cannae's 10-K, not opened). — [D&B FY2024 10-K](https://www.sec.gov/Archives/edgar/data/1799208/000179920825000012/dnb-20241231.htm)
- Datarade describes itself as the largest external data marketplace: 2,000+ providers, 600+ categories, over 100k businesses per month comparing providers (self-reported, secondary). Top B2B categories on its site include B2B contact and leads data, B2B marketing data and company/firmographic data; healthcare professionals (HCP) data has its own sub-category tree (healthcare contact data, HCP data, physician databases, doctors datasets). — [Datarade B2B data](https://datarade.ai/data-categories/b2b-data/providers); [Datarade HCP category](https://datarade.ai/data-categories/healthcare-provider-hcp-data); [Datarade physician databases](https://datarade.ai/search/products/physician-databases)
- Datarade healthcare listings seen: Hagimo US Medical Providers (about 6.6M providers with contact, credentials, specialties); MedicoReach "Doctors Data" (948,000+ verified contacts) and Dentists Database; DataCaptive 120,520 verified dentist emails and phones (USA); CarePrecise (physician, hospital, clinic, practice-group databases, monthly updates). — [Hagimo](https://datarade.ai/data-products/hagimo-us-medical-providers-6-6m-providers-contact-credentials-specialties-more-hagimo); [MedicoReach doctors](https://datarade.ai/data-products/doctors-data-more-than-948-000-verified-contacts-of-doctors-medicoreach); [DataCaptive dentists](https://www.datarade.ai/data-products/more-than-120-520-verified-emails-and-phone-numbers-of-dentis-datacaptive); [CarePrecise](https://datarade.ai/data-providers/careprecise)
- BoldData claims Datarade's #1 company-data provider spot (vendor-reported) and sells country company databases, including about 401,000 UAE companies and India category lists (chemists, pharmaceuticals). — [BoldData on Datarade](https://bolddata.nl/en/bolddata-fastest-growing-loved-b2b-data-provider); [BoldData UAE product](https://datarade.ai/data-products/list-of-400k-companies-in-united-arab-emirates-bolddata); [BoldData India chemists](https://bolddata.nl/en/companies/india/chemists-india)
- Experian says its business lists cover more than 14 million US businesses (consumer lists 245 million consumers, 110 million households); Experian Small Business is pay-per-record with no subscription (vendor claim). — [Experian small business lists FAQ](https://experian.com/small-business/small-business-marketing-lists-faqs)
- B2B lists are most often compiled/selected by SIC code, with selects for employee size, sales volume, new businesses (list-broker blog, secondary). — [Postalytics list-broker content](https://www.postalytics.com/?p=3121)
- Indian and Gulf vendors sell generic "directory" databases by category, including chemists/medical stores, doctors, restaurants, boutiques, salons, nursing homes, diagnostic centres (NIIR-type directories); UAE vendors sell directories by sector (medical, industrial, oil & gas, logistics, product finder) — see section 2 for prices. — [NIIR directory listing](https://niir.org/books/database/directory-database-list-chemists-medical-store-nursing-home-maternity-diagnostic-centre-pathology-labs-fashion-studio-boutique-tailors-beauty-parlours-spa-salon-restaurants-bar-lounge/z,,a,7e,0,a/index.html)

### Inferences
- Healthcare professionals is the one vertical that clearly has its own dedicated commercial sub-market and multiple specialist vendors; that is a demand signal (several vendors would not exist otherwise), but not a measured sales rank.
- ZoomInfo's customer count (35,000) and Data Axle/D&B scale show the paying base is mostly sales teams buying subscriptions for decision-maker contacts, not buyers of one-off static lists of local SMEs.

### Gaps
- No verified sales rankings or "top sellers by industry" from Datarade, AWS Data Exchange, Snowflake Marketplace, Data Axle, or SalesGenie (pages blocked or not surfaced).
- No data found on Lusha, Apollo, AeroLeads, Europages or SalesGenie category popularity.
- Dentists, hospitals, pharmacies, lawyers, accountants, real estate, contractors, restaurants, hotels, manufacturers, schools, farms, auto dealers, NGOs: no per-category sales data located; only that vendors list them.

## 2. Price per record / per list by category and data depth

### Takeaway
Prices span roughly four orders of magnitude: public-registry-derived records at $0.002 to $0.02 each, bulk "commodity" lists at $0.0002 to $0.05, name+address+phone lists at about $0.05 to $0.5, and verified decision-maker or healthcare contacts at about $0.15 to $2+ per record (subscription or credit). Premium (physician, executive) data commands higher rates mainly when verified and updated. Most real-world list brokers do not publish prices. All figures are secondary unless stated.

### Cited Findings
Generic business data
- Data Axle API: about $50 to $75 per 1,000 business records ($0.05 to $0.075 per record); for 50,000+ contacts $0.05 to $0.07; pricing otherwise "contact sales"; extras (email validation, setup, updates) said to add 30% to 50%. Source is a ZoomInfo-owned competitor blog and Fullenrich/Prospeo blogs (competitor/aggregator, low reliability). — [ZoomInfo "Data Axle pricing" (competitor)](https://pipeline.zoominfo.com/sales/data-axle-pricing); [Fullenrich Data Axle pricing](https://fullenrich.com/content/data-axle-pricing); [Prospeo business mailing lists](https://prospeo.io/s/business-mailing-lists)
- Historic list-rental benchmarks (per thousand, "M"): B2B lists typically $175/M to $300/M; large business email lists averaged $190/M (that is $0.175 to $0.30 per record; per use/rental, not ownership). Date not shown in snippet; the MediaPost article ("B2B Email List Rental Prices Take A Dip", ID 328735) appears to date from about 2019 (unverified). — [MediaPost](https://www.mediapost.com/publications/article/328735/b2b-email-list-rental-prices-take-a-dip.html)
- An older Chief Marketer broker survey (undated, likely 2000s; low relevance for current prices) listed top-selling B2B email lists: Business E-mail Network (17.5M universe) at $300/M with industry, employee count and title selects; Decisionmaker Management Marketplace (2.38M emails) at $425/M; HR.com master file (172,350) at $400/M. — [Chief Marketer](https://chiefmarketer.com/the-brokers-lowdown-on-e-mail-lists)
- Experian business lists: price depends on database type, selections and record count, quoted in order flow; no published rate. — [Experian FAQ](https://experian.com/small-business/small-business-marketing-lists-faqs)
- Datarade listings (provider-set "starting" prices): Leads XL from $0.05 per record; Metric Central US business and contact database from GBP 0.50 per record; Metric Central worldwide database from GBP 1 per record; one targeted B2B marketing data product from USD 100 per 5,000 records ($0.02 per record). — [Leads XL](https://datarade.ai/data-providers/leads-xl); [Metric Central US](https://datarade.ai/data-products/us-business-contact-database-list-metric-central); [Metric Central worldwide](https://datarade.ai/data-products/worldwide-business-contact-database-list-metric-central); [Targeted B2B marketing data](https://datarade.ai/data-products/targeted-b2b-marketing-data-for-telemarketing-and-email-marke-b2b-email-databases)
- Credit-based B2B contact data self-serve: roughly $0.20 to $2.00+ per contact reveal; platform seat licences commonly five figures per year per team (LeadGenius vendor blog, 2026, secondary). — [LeadGenius pricing guide](https://www.leadgenius.com/resources/how-much-does-b2b-contact-data-cost-a-2026-pricing-guide)
- Subscription tools (2026, review-blog figures, secondary): Cognism contracts about $22,000 to $40,000 per year, median about $36,000; ZoomInfo $15,000 to $45,000+ per year; Apollo $49 and $79 per user per month (annual billing); Lusha $37.45 to $259.95 per month promotional (list $49.90, $69.90, $399.90), with 1 credit per verified email and 5 per phone; ZoomInfo extra credit packs $2,000 to $5,000. — [Emelia/Cognism pricing](https://emelia.io/hub/cognism-pricing); [Datalane Lusha](https://www.datalane.com/post/lusha-pricing); [Zeliq Apollo](https://www.zeliq.com/blog/apolloio-pricing); [Cloudnuro ZoomInfo](https://www.cloudnuro.ai/blog/zoominfo-pricing-guide); [Prospeo Cognism](https://prospeo.io/s/cognism-pricing)

Healthcare and professional categories
- Arkansas Medical Board (a government primary source) sells a mailing list of 15,091 MD/DO records for $250.00 (about $0.017 per record, name and address from licensing; date of price not shown). — [Arkansas Medical Board](https://armedicalboard.adh.arkansas.gov/Public/PurchaseMailingList.aspx)
- UpLead: US dentist email list of 12,147 verified contacts for $1,999 one-time (about $0.16 per record; vendor page, date not shown). — [UpLead dentist list](https://www.uplead.com/dentist-email-list)
- Tomba: dental clinic contacts from $8.90 per 1,000 valid emails (about $0.009 per record; low-end, verification included); FullEnrich dentist contacts "from $29" pay-per-found contact. — [Tomba](https://tomba.io/e/dental-clinic-email-list); [FullEnrich](https://fullenrich.com/email-list/dentist-email-list)
- A datahub.io-hosted listing claims physician emails around $0.00016 each in a 2.5M-contact list, and a $439 healthcare package (788k physicians with 17k emails, plus hospitals, dentists, chiropractors, pharma companies). Very low reliability (lead-gen listing, likely scraped/low-verification data; note only 17k of 788k physician records had email). — [datahub.io Doctors Email Address List](https://datahub.io/@leadsbluecom/mailinglists/Doctors+Email+Address+List)
- Apify scrapers of public NPI and CMS data: $2 per 1,000 (NPPES NPI registry scrape), $3 per 1,000 (normalised NPPES), $20 per 1,000 (Medicare provider records, 2.8M+ clinicians), $150 per 1,000 (CMS Open Payments Pro, pharma-to-physician payments enriched with specialty and address). Shows that name/NPI/practice-address physician data derived from government sources is a near-commodity ($0.002 to $0.02) and value is added only by enrichment (payments, prescribing, verified email). — [NPI Registry Scraper](https://apify.com/cblu/npi-healthcare-providers-scraper); [Medicare Provider Records](https://apify.com/nexgendata/medicare-provider-intelligence); [Normalized NPPES](https://apify.com/overlookdata/npimcp-search); [CMS Open Payments Pro](https://apify.com/nexgendata/cms-open-payments-physician-intelligence-pro)
- AMA Physician Masterfile: AMA licenses to "Database Licensees" (for example Medical Marketing Service, MMS) which resell; cost depends on records, data set and identification; schedule not found. AMA earned more than $44 million from database products in 2005 (about 16% of its budget), largely from pairing physician identity with prescribing data for pharma (older figure, from advocacy source PNHP). — [J-PAL admin data catalogue on AMA Masterfile](https://www.povertyactionlab.org/admindatacatalog/american-medical-association-physician-masterfile); [PNHP](https://pnhp.org/news/prescription-mining-raises-millions-for-doctors-group/)

India
- India chemists/medical store directories: GBP/INR figures seen: INR 999 (one chemists/medical stores database; vendor not identified in snippet); INR 3,700 (about US $150) for a database of chemists, medical stores, pharmacy, druggists (NIIR-type listing); INR 4,366 (about US $150) for another chemists database; INR 6,490 (about US $200) for a Doctors in India directory. One collection had 8,800+ chemist records; another 42,949 chemist companies. For scale, at INR 3,700 for 8,800 records the price is about INR 0.42 per record. Fields: name, address, phone, sometimes email. Prices are for static one-off lists (date not shown). — [NIIR directory](https://niir.org/books/database/directory-database-list-chemists-medical-store-nursing-home-maternity-diagnostic-centre-pathology-labs-fashion-studio-boutique-tailors-beauty-parlours-spa-salon-restaurants-bar-lounge/z,,a,7e,0,a/index.html); [Entrepreneur India database](https://www.entrepreneurindia.co/database/534/download-pdf); [BoldData India chemists](https://bolddata.nl/en/companies/india/chemists-india); [CompanyData India chemists](https://companydata.com/india/chemists-india/)

UAE and Gulf
- UAE business directory (Excel, about 320,000 companies; name, phone, fax, PO box, email, website, activity) AED 1,000; UAE plus free-zone directory (about 360,000) AED 1,500; UAE mobile database (about 300,000 contacts) AED 5,000; UAE directory with contact names and emails (40,000 top companies) AED 3,000; Dubai Industrial Directory AED 500; Dubai Medical Directory AED 1,000; sector directories (oil and gas, logistics, product finder) AED 1,000 each. CAUTION: the search summary did not attribute this to one specific URL; vendor and date unverified. — search summary for query "UAE business database buy companies list price AED" (no single URL confirmed); comparator: [BoldData UAE database](https://acc.bolddata.nl/en/database/uae-dubai)
- BoldData UAE (about 401,000 companies): licences from EUR 425 one-off, or EUR 7,500 per year (vendor, date not shown). — [BoldData UAE database](https://acc.bolddata.nl/en/database/uae-dubai); [Datarade BoldData UAE](https://datarade.ai/data-products/list-of-400k-companies-in-united-arab-emirates-bolddata)

Europe and exporters
- Kompass: 35 million companies in 70+ countries; data is sold via "Export Credits" and Kompass Files; official prices not found. Third-party Apify scrapers of Kompass sell at $2.49 per 1,000 companies and $9.99 per 1,000 "verified exporter leads". Shows exporter data is demanded, and that scraping undercuts the vendor (and may breach Kompass terms). — [Kompass special conditions](https://fr.kompass.com/l/special-conditions); [Kompass Scraper](https://apify.com/crawloop/kompass-scraper); [Kompass Exporter Scraper](https://apify.com/logiover/kompass-exporter-scraper)

### Inferences
- Price ladder by depth (approximate, mixed currencies and years): public-registry name and address $0.002 to $0.02; commercial compiled name, address, phone $0.02 to $0.075 (Data Axle API), rented lists $0.175 to $0.43 per use; verified email plus phone or decision-maker $0.15 to $2+.
- The only strong "premium vs commodity" evidence is indirect: physician core identity data is cheap (government-sourced); price rises with enrichment (verified email, payments, prescribing) and with human-verified contact depth. Lawyers/accountants/executives: no price evidence found.
- India and UAE static list vendors charge about US $15 to $270 for whole-country sector files (INR 999 to 6,490; AED 500 to 5,000), i.e. very low ticket prices; list-as-file is a low-value product in these markets unless updated, verified or niche.

### Gaps
- No price evidence for lawyers, accountants, real estate agents, contractors, restaurants and hotels, schools, farms, auto dealers, importers or exporters from established brokers (SalesGenie, Data Axle, InfoUSA, Experian rate cards not accessible).
- No Lusha or AeroLeads per-record list prices, no D&B list price, no Snowflake/AWS Data Exchange price points found.
- Dates missing on most snippets; INR/AED price pages could not be opened.

## 3. Who buys which lists and why

### Takeaway
The best-evidenced buyer segments are sales teams (software, services) buying decision-maker contacts, and pharma buying physician-level data. Evidence for the other specific pairings (POS vendors, insurers, distributors, recruiters, franchisors) is largely absent from sources I could retrieve.

### Cited Findings
- ZoomInfo's customer base is "go-to-market" teams; more than half of its ACV comes from customers paying $100,000+; products are sales intelligence subscriptions. — [ZoomInfo FY2025 results](https://www.businesswire.com/news/home/20260209677262/en)
- Pharma buys physician identity data from the AMA licensees and pairs it with prescribing data; the AMA Masterfile therefore underpins pharma sales targeting (older and advocacy-sourced). — [PNHP](https://pnhp.org/news/prescription-mining-raises-millions-for-doctors-group/)
- CMS Open Payments (Sunshine Act pharma-to-physician payments) data enriched with NPI specialty and address is sold at $150 per 1,000 rows via Apify, implying demand from pharma/medical-device compliance, competitive intelligence and sales (inference; vendor does not state buyers). — [CMS Open Payments Pro](https://apify.com/nexgendata/cms-open-payments-physician-intelligence-pro)
- List brokers describe B2B lists being bought for direct mail, telemarketing and email, selected by SIC, headcount, sales volume and new-business status (secondary). — [Postalytics](https://www.postalytics.com/?p=3121)
- Datarade says B2B data providers serve marketers and sales teams running account-based marketing with intent, firmographic and technographic data (Datarade, secondary). — [Datarade B2B marketing data](https://datarade.ai/data-categories/b2b-marketing-data/providers)

### Inferences
- Exporter and importer data on Kompass-type platforms implies buyers are trade and sourcing teams; not confirmed in sources.
- Buyer-use pairings in the brief (POS vendors to small businesses, insurers to SMEs, distributors to retailers, recruiters, franchisors, political/NGO outreach, real-estate marketers) are plausible but I found no cited evidence.

### Gaps
- No evidence located on buyer mix by vertical from Data Axle, D&B, or Datarade. No press coverage of specific data buyers found.

## 4. Retailer and outlet census data (FMCG and pharma distribution)

### Takeaway
Outlet universe data is sold by NielsenIQ and Kantar-type auditors as part of expensive syndicated retail-measurement subscriptions, not as cheap lists; I found no public price. India's scale (millions of kirana outlets) is the opportunity, but the data buyers are multinationals buying through audits. No Retail Cloud or local audit vendor prices were found.

### Cited Findings
- NielsenIQ publishes "universe information" (its estimate of each country's retail trade universe) and "Market at a Glance" reports; Retail Measurement Service covers offline markets; NIQ expanded FMCG e-commerce measurement in Southeast Asia/Indonesia. Prices not shown. — [NIQ Market at a Glance guide](https://develop.nielseniq.com/global/en/wp-content/uploads/sites/4/2021/02/using-the-market-at-a-glance-reports.pdf); [NIQ SEA e-commerce expansion](https://www.barchart.com/story/news/36152159/niq-expands-fmcg-e-commerce-measurement-across-southeast-asia); [ESOMAR retail in emerging markets](https://ana.esomar.org/documents/retail-in-emerging-markets-)
- NIQ shopper-trend reports are sold via a shop; prices not extracted. — [NIQ shop](https://shop.nielseniq.com/shopper-trends/)
- India: "over 12 million retail outlets"; kirana stores estimated 15 to 20 million and about 90% of FMCG retail sales (search-summary figures; figures conflict internally and the underlying source was not identified). — [Statista India kirana](https://fr.statista.com/statistics/1223851/india-share-of-open-kirana-stores/); [DealStreetAsia on kiranas](https://dealstreetasia.com/stories/startups-mncs-kirana-stores-204355)
- InfobelPRO lists 8.2 million retail company records in India (from Ministry of Corporate Affairs registry data); GapMaps sells POI/GIS data for India; Datarade has a "retail sales data India" category. Prices not found. — [InfobelPRO India retail](https://www.infobelpro.com/companies/india/retail); [Datarade retail sales data India](https://datarade.ai/search/products/retail-sales-data-india)

### Inferences
- The outlet-census gap is real in emerging markets (unorganised retail is not in registries), and the buyer (FMCG/pharma distribution) already pays an auditor; a crowd-built, cheaper outlet list could be positioned against audits, but this is a hypothesis without price evidence.

### Gaps
- No price for NielsenIQ, Kantar, Retail Cloud-type or local retail-audit vendors; no outlet counts by channel (grocery, pharmacy, general store, wholesale) from a primary source; Kantar and Retail Cloud were not surfaced at all.

## 5. Demand signals (searched lists, SEO volumes, rankings)

### Takeaway
I found no usable keyword-volume data for "X email list" or "list of X in Y" queries and no marketplace sales rankings. The only signals are indirect: how many vendors publish SEO landing pages for "[profession] email list" (dentists, physicians, pediatric dentists, orthodontists) and the breadth of Datarade healthcare supply.

### Cited Findings
- Multiple vendors run dedicated "[profession] email list" landing pages for dentists, pediatric dentists, physicians and orthodontists (Saleshandy, UpLead, FullEnrich, Tomba, MedicoReach, DataCaptive) — an indicator that these are search terms worth ranking for. — [Saleshandy dentist list](https://saleshandy.com/dentist-email-list); [Saleshandy physicians list](https://saleshandy.com/physicians-email-list); [Tomba orthodontist list](https://tomba.io/e/orthodontist-email-list)
- General topic searches for professions are large (US: "dentist" about 1.22 million monthly, "dentists" about 1.5 million), but these are consumer-intent terms, not list-purchase intent (aggregator data; date not shown). — [seodata.dev dentist](https://www.seodata.dev/keyword/dentist)

### Inferences
- Profession-specific "email list" pages across many vendors point to healthcare (dentists, physicians) and then other professionals as the most commercially contested list queries.

### Gaps
- No keyword volumes for "doctors email list", "list of hospitals in [city]", "importers email list", etc. (SEO tools not accessible). Recommend checking Ahrefs, Semrush or Google Keyword Planner directly.
- No marketplace sales rankings (Datarade, AWS, Snowflake).

## 6. Licensing and legal sensitivity

### Takeaway
Healthcare practitioner data and sole-trader contact details carry the heaviest legal friction. Under UK/EU rules, sole traders and some partnerships are treated as individuals, so cold email needs consent; corporate-address B2B email can rely on legitimate interest. In the US, CAN-SPAM has no opt-in but purchased mobile numbers for texting are risky under TCPA. Physician identity data via AMA is a licensed product.

### Cited Findings
- UK/EU: sole traders and partnerships are treated as individual subscribers under PECR and UK GDPR; consent is required for direct marketing; their email addresses are personal data. Corporate B2B email can rely on legitimate interest with low privacy impact (compliance-advice blogs, secondary; not primary regulator text). — [GDPRLocal B2B](https://gdprlocal.com/b2b-gdpr/); [Privasee](https://privasee.io/post/gdpr-compliance-for-b2b-marketing); [Beswicks](https://www.beswicks.com/can-i-rely-on-legitimate-interest-for-b2b-marketing/); [Recruitment Network](https://therecruitmentnetwork.com/learn/news/key-differences-between-b2b-and-b2c-when-it-comes-to-gdpr)
- US CAN-SPAM: no recipient consent required, but sender must honour opt-outs; buying lists risks including opted-out and illegally harvested addresses. — [Pepperdine compliance summary](https://community.pepperdine.edu/imc/resources/email/law-regulation-compliance.htm)
- US TCPA: marketing texts to purchased mobile numbers without prior express written consent are unlawful; statutory damages $500 to $1,500 per message (vendor blogs, secondary). — [Tatango](https://www.tatango.com/blog/can-you-buy-mobile-phone-numbers-for-text-message-marketing/); [Instantly TCPA](https://instantly.ai/blog/2025-tcpa-checklist-compliant-cold-email-sms/)
- Physician data: AMA Physician Masterfile is licensed only through approved licensees; state boards sell their own licensee lists (Arkansas example, $250 for 15,091 records) with purchase terms. — [AMA Masterfile via J-PAL](https://www.povertyactionlab.org/admindatacatalog/american-medical-association-physician-masterfile); [Arkansas Medical Board](https://armedicalboard.adh.arkansas.gov/Public/PurchaseMailingList.aspx)
- US NPI registry data is public and scraped/resold at $2 to $20 per 1,000 (see section 2), meaning the base physician list has no licensing barrier; the AMA Masterfile specialty/ID layer does.

### Inferences
- For AllLists, safest to list organisations (hospitals, pharmacies, companies, schools) with business phone and generic business email, and to avoid sole-trader personal contact details and personal mobile numbers, especially for UK/EU subjects. Lawyers, accountants, doctors in the Gulf and India: no regulatory source found (UAE data law, India DPDP Act 2023 not researched here); must be checked before launch.

### Gaps
- No primary regulator text (ICO, EU, FTC) retrieved; India DPDP Act and UAE PDPL implications not researched; lawyer-directory licensing rules not researched.

## 7. Conclusion for AllLists: ranked shortlist of list types where buyers pay for the list itself

### Takeaway
Ranking below combines price evidence (where any), breadth of buyers and legal risk. Evidence strength is weak to moderate throughout: most prices are vendor-listed "from" prices, not realised sales. The static-list-as-file market is low ticket (tens to low hundreds of USD per country file in India and the Gulf); higher money is in subscriptions and enriched, verified, updated data.

### Cited Findings and Ranked List
Ranking is my judgement; underlying data cited in the sections above.
1. Healthcare organisations and practitioners (hospitals, clinics, pharmacies, dentists, doctors), with verified phone and email. Highest evidence of dedicated vendors and highest price anywhere in the evidence (Open Payments enriched $0.15 per record; UpLead dentist list $1,999 for 12,147; Indian doctor directory about US $200); buyers: pharma, device, healthcare marketers. Evidence: moderate. Legal risk: highest for named individuals; lower for organisation-level (hospital, pharmacy) lists.
2. Decision-maker contacts at companies (verified email, title). Largest buyer breadth (ZoomInfo 35,000 customers; Cognism $22,000 to $40,000 per year; credits $0.20 to $2+). But the market is dominated by large subscription incumbents; a new list entrant competes on price (Data Axle API at $0.05 to $0.075). Evidence: strong for market size, weak for a small vendor winning.
3. Importers and exporters, and manufacturers/distributors (trade partner lists). Kompass-type exporter data is demanded (scrapers selling at $9.99 per 1,000 exporter leads); buyers are exporters, sourcing teams. Evidence: weak to moderate; no list-broker price located.
4. Country company databases by sector (UAE, India, other emerging markets). Established low-ticket market (AED 500 to 5,000; INR 999 to 6,490; BoldData UAE EUR 425 one-off) with many sellers; buyer breadth wide but willingness to pay per file is low and quality sensitive. Evidence: moderate for existence of demand, price low.
5. Retail outlet census (pharmacy, grocery, general trade, wholesale). Potentially high value to FMCG/pharma distributors but currently sold inside expensive audit subscriptions (NIQ); no price evidence. Evidence: weak (no prices). Possibly the largest underserved niche for emerging markets.
6. New-business and local small-business lists (SIC-selected, US-type mailing lists). Mature commodity at $175 to $300 per thousand rental historically; price pressure from free and scraped sources. Evidence: moderate; low differentiation.
7. Professionals (lawyers, accountants, real estate agents) and other verticals (schools, farms, auto dealers, NGOs, restaurants, hotels). Vendors list them but no price or demand evidence was found. Evidence: very weak.

### Inferences
- Where the buyer pays for the list itself (rather than a platform), the evidence points to: niche-verified healthcare and trade lists first; and generic country-level company files last in value.
- A free, open directory like AllLists will compete with free government sources (NPI, state boards, Open Payments, company registries) where the base data is near-zero priced, so value must come from enrichment, verification, freshness, or hard-to-get coverage (unregistered outlets, informal sector).

### Gaps
- Single biggest gap: real transaction or ranking data. Suggest: pull Datarade provider pages for the shortlisted categories (blocked here), buy a small sample from two Indian/Gulf vendors, check Google Keyword Planner/Ahrefs for "[X] email list", "[X] database in [country]", and obtain NIQ/Kantar quotes for outlet universe data.
- All prices are secondary; none were verified on a primary page. Datarade, BoldData, NIIR and Prospeo pages could not be opened.
