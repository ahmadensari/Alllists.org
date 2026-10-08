# Pakistan as a launch market for AllLists.org (research notes, as of 5 Oct 2026)

Method and limits (read first): about 30 web searches. Direct page fetches of pbs.gov.pk, pta.gov.pk, brecorder.com, kpcerc.kpitb.gov.pk, poverty-action.org and galluppakistandigitalanalytics.com were blocked by the network proxy, so most figures below come from search-result summaries of those pages, not from the pages themselves. Each claim carries the URL of the search result that surfaced it. Items marked UNVERIFIED come from my background knowledge or a single weak source and must be checked before use. This is planning research, not legal advice. Several of the most important questions (per-city POI coverage in Google Maps/OSM/Overture/Foursquare, named buyer prices, chamber and association terms of use) returned nothing usable, and are listed under Gaps rather than guessed.

## 1. Data gap evidence: completeness and currency of Google Maps, OSM, Overture, Foursquare for Pakistani small businesses

### Takeaway
The size of the target universe is well documented: the 2023 Economic Census counted 7.14 million establishments, of which 3.22 million are wholesale/retail. I found no published, quantified comparison of Pakistani small-business coverage in Google Maps, OSM, Overture or Foursquare against that universe, so "the data is poor" is currently a strong prior, not a measured fact. Measuring it (Overture/OSM counts against census counts, by city and trade) is a cheap first task for the project.

### Cited Findings
- Economic Census 2023 (PBS) recorded 7,142,941 establishments employing 25,344,121 persons. Wholesale and retail trade (incl. motor vehicle/motorcycle repair) is 3,223,227 establishments. Accommodation and food service is 272,147; manufacturing 696,558; information and communication 43,497; financial and insurance 22,264. — [TechJuice/PBS tables via search summary](https://www.techjuice.pk/services-sector-jobs-lead-pakistan-employment-after-new-census/); [PBS Table 1](https://www.pbs.gov.pk/sites/default/files/ec/tables/Table_1.pdf) (page itself not fetched)
- Establishment size: about 7.1 million of 7.14 million establishments have 1 to 50 workers. Only 7,086 have more than 250 workers. — [Gallup Pakistan Digital Analytics summary](https://galluppakistandigitalanalytics.com/2026/03/16/pakistans-economic-reality-7-1-million-businesses-but-almost-all-are-micro-pakistans-economic-census-2023-reveals-something-striking-about-the-structure-of-our-economy/)
- Province split: Punjab about 4.36 million establishments (13.6 million workers); Sindh about 1.38 million (5.7 million workers); KP about 1.00 million (4.0 million workers). Punjab holds 58% of establishments and Sindh 20%. — [Gallup summary](https://galluppakistandigitalanalytics.com/pakistan-economic-census-2023/); [Deccan Herald](https://www.deccanherald.com/amp/story/world%2Fpakistan-has-more-mosques-and-madrassas-compared-to-factories-says-economic-census-3693076)
- The census geo-tagged about 40 million buildings, of which 7.14 million were economic establishments. This is a building-level frame, so it is potentially the best ground truth for validating POI coverage, if the geo-tagged microdata can be obtained (not verified). — [Deccan Herald](https://www.deccanherald.com/amp/story/world%2Fpakistan-has-more-mosques-and-madrassas-compared-to-factories-says-economic-census-3693076)
- FMCG retail universe estimates conflict. One source says about 2 million retail outlets, of which about 800,000 sell FMCG, two-thirds of them kiryana stores. A more recent figure in the same result set is 600k to 730k outlets, 60-65% kiryana. Organised retail is about 5%. — [search summary citing Prime Institute and others](https://primeinstitute.org/wp-content/uploads/2022/09/Modern-Retailing-Prospects-for-Retail-Complexes-in-Pakistan.pdf); a B2B distributor describes its market as "about 800,000 retailers" — [Profit](https://profit.pakistantoday.com.pk/?p=161891)
- The FBR retailer-documentation effort cites an estimated 3.2 to 3.5 million retailers; only about 300,000 file returns (about 92% undocumented per one source). — [ProPakistani 22 Jan 2024](https://propakistani.pk/2024/01/22/fbr-to-unveil-tajir-doost-mobile-app-for-documentation-of-3-2-million-retailers/); [Dawn](https://www.dawn.com/news/amp/1855386). Note the 3.2-3.5 million FBR figure is consistent in scale with the census trade count (3.22 million), but 600k-800k "FMCG outlets" is a narrower definition.
- OSM Pakistan: the OSM wiki says completeness varies by area because of imagery quality and few editors. Many roads are missing on the outskirts of Karachi, in rural areas and in Hyderabad. — [OSM WikiProject Pakistan](https://wiki.openstreetmap.org/wiki/WikiProject_Pakistan). This is road completeness, not POI completeness.
- Local competitor mapping: TPL Maps claims 1.5 million points of interest, built by about 100 IT/GIS staff over 15 years. — [ProPakistani](https://propakistani.pk/2016/09/23/pakistan-made-google-maps-rival-set-expand-three-new-countries/) (2016, and the claim is the vendor's own). 1.5 million POIs is far below the 3.2 million census trade establishments.
- Overture Places has more than 64 million places globally, conflated from Meta and Microsoft data. — [Google Earth Engine catalog entry](https://developers.google.com/earth-engine/datasets/publisher/overture-maps). Overture and OSM building completeness can be assessed with a published HeiGIT pipeline. — [HeiGIT](https://giscienceblog.uni-heidelberg.de/?p=19426). I found no Pakistan-specific Overture places count.
- Pakistan had 69.4 million Facebook users in Aug 2026 (29% of population). Meta is a major Overture places source, so Facebook Page presence is the likely upstream for Overture coverage of Pakistani shops (inference). — [NapoleonCat](https://stats.napoleoncat.com/facebook-users-in-pakistan/2026/06/) (search summary reports August 2026)

### Inferences
- Rough ceiling check: if Overture/OSM hold well under 1 million Pakistani places, they cover under about a third of the 3.2 million census trade establishments. This is arithmetic from the figures above plus an assumed count, so UNVERIFIED until someone downloads the Overture Pakistan extract.
- Best-covered cities are probably Karachi, Lahore, Islamabad/Rawalpindi (restaurants, hotels, clinics, malls, banks). Worst covered are likely kiryana, hardware, spare-parts, mobile-repair and wholesale-market shops in secondary cities and towns. This is a hypothesis from the OSM wiki and the online-presence data, not a measured result.
- The 40-million-building geo-tagged frame means a licensed or negotiated data deal with PBS could be the strongest anchor for "verified at every place", but only if the microdata is accessible.

### Gaps
- No study counting Pakistani POIs by city and category in Google Maps, OSM, Overture or Foursquare was found. Google Places coverage cannot be measured without the API.
- No evidence on Foursquare Pakistan coverage found.
- Karachi/Lahore/Faisalabad etc. census establishment counts by district were not retrievable (PBS blocked).
- Pakistan-specific figures for what share of the census establishments are visible online were not found.

## 2. Existing local data holders: terms and reuse

### Takeaway
The public, bulk-downloadable layers are thin and skewed toward formal firms: SECP company search (free basic profile; 290,041 companies by Mar 2026), the FBR Active Taxpayer List (downloadable Excel, daily updates), and the TDAP Exporters Directory (online, searchable by HS code). Chamber, association and municipal records exist but I found no evidence of public bulk access or reuse licences. The census (PBS) publishes tables, not business-level records. Bulk reuse terms for all of these are UNVERIFIED and need a legal read plus direct outreach.

### Cited Findings
- SECP: official registry on the eServices portal. Basic company profile search is free; certified extracts cost PKR 200 to 3,000. A search returns name, CUIN, incorporation date, kind, registered office address, CRO and status. Foreign users can search without a local ID. — [Business Data Guide](https://businessdataguide.com/blog/jurisdictions/pakistan-company-search-guide). Registered companies totalled 290,041 as of March 2026. — [APP](https://www.app.com.pk/?p=1193171). SECP is moving to a new registry called eZfile. — [SECP press release Feb 2024](https://www.secp.gov.pk/wp-content/uploads/2024/02/Press-Release-Feb-12-SECP-all-set-to-launch-eZfile-a-new-corporate-registry.pdf). SECP registered over 18,000 new companies in early 2026. — [ARY](https://arynews.tv/secp-registers-over-18000-new-companies-in-2026). Terms of use for scraping or bulk reuse: not found. 290k companies is about 4% of 7.14 million establishments, so SECP covers the formal tip only (arithmetic).
- FBR Active Taxpayer List (ATL): a downloadable Excel sheet on fbr.gov.pk Downloads, reportedly updated daily now. — [ICT.edu.pk guide, secondary source](https://www.ict.edu.pk/blogs/active-taxpayer-list-pakistan). It lists filers by name and NTN; it does not appear to carry shop addresses or phone numbers (UNVERIFIED). Only about 300,000 of an estimated 3.5 million retailers file returns. — [Dawn](https://www.dawn.com/news/amp/1855386)
- Tajir Dost scheme: about 64,000 to 70,000 retailers registered, which is low relative to the target. — [Dawn](https://www.dawn.com/news/amp/1855386); [Aaj News: "Just 277 retailers step up"](https://english.aaj.tv/news/amp/330377210). Retailers resist documentation, so shop owners may be wary of any list that looks tax-linked (inference). See also section 4.
- TDAP: an online Pakistan Exporters' Directory, searchable by HS code, product category and company name, grouping firms into large/medium/small by export turnover; firms can add or update their own entry. — [ProPakistani 2017](https://propakistani.pk/2017/05/31/online-directory-pakistani-exporters-launched-help-foreign-customers/). Currency of the data today is unknown. A separate Pakistan Trade Portal exists. — [Pakistan Trade Portal](https://pakistantradeportal.gov.pk/pages/about-us)
- Chambers: FPCCI is in Karachi, and KCCI and LCCI exist, but the search found no downloadable member directories. TDAP and LCCI have signed cooperation on exports. — [Embassy listing](https://pakistanembassy.se/?p=41); [APP](https://www.app.com.pk/?p=1121334)
- PBS: publishes census tables; ownership and microdata terms not confirmed. — [PBS Economic Census report](https://www.pbs.gov.pk/sites/default/files/ec/Economic_Census_Report.pdf)
- DRAP: maintains a registered-drugs database (name, dosage, composition, registration number, holder); any seller or distributor needs a DRAP licence. Retail pharmacy counts were not found. — [DRAP](https://www.dra.gov.pk/?p=34380)

### Inferences
- The public datasets mostly cover registered firms and exporters. Kiryana, repair, hardware and street-market businesses are the invisible majority, consistent with 92% retailer non-filing.
- The best partnership targets are the bodies with member lists and a motive to digitise: trade associations (pharmacy, petroleum dealers, mobile traders, spare parts) and chambers. Their consent would also remove the scraping-rights question.

### Gaps
- No evidence found on bulk reuse terms for SECP, ATL, TDAP, chambers, PTA or municipal licence data.
- PTA publishes no public business data to my knowledge (UNVERIFIED); no search evidence either way.
- Association member counts (petroleum dealers, pharmacists, hoteliers, bakers, mobile traders) not found; SMEDA data not found.

## 3. Buyers and demand

### Takeaway
There is demonstrable demand for retailer-level data and reach: B2B distribution startups and payment providers are building outlet networks. But I found no published prices for outlet data, lead lists or field-force services. The sharpest evidence is that outlet-level digitisation companies raised large funds, and that payment players are chasing merchants.

### Cited Findings
- Bazaar (Karachi) raised a US$6.5 million seed round in Jan 2021. It targeted 800 retailers in Karachi in 2020 and ended with over 10,000. — [ProPakistani 19 Jan 2021](https://propakistani.pk/2021/01/19/pakistani-b2b-e-commerce-startup-raises-6-5-million-in-regions-largest-seed-round/); [Profit](https://profit.pakistantoday.com.pk/2021/01/19/karachi-based-bazaar-technologies-secures-6-5m-in-seed-funding-to-digitise-mom-and-pop-stores)
- Bazaar later raised US$70 million (Gulf News) and then shut two new verticals (mobile phones, pharma) and laid off about 600 people, wiping out its Lahore field force. Field acquisition is expensive and fragile. — [Gulf News](https://gulfnews.com/business/retail/pakistans-ecommerce-startup-bazaar-raises-70m-in-funding-1.86460830); [Profit](https://profit.pakistantoday.com.pk/?p=161891). Bazaar also moved into digital payments. — [Digital Pakistan](https://digitalpakistan.pk/bazaar-technologies-expands-into-digital-payments)
- SnappRetail (kiryana tech) is another comparable. — [TechCrunch 2022](https://techcrunch.com/2022/09/06/snappretail-helps-pakistans-kiryanas-compete-against-supermarkets)
- SBP/Raast: over 2.6 million merchants onboarded or registered an alias by end of Q3 FY26 (March 2026) and 2.5 million QR-enabled merchant locations. Banks and wallets have a clear need to find and activate merchants. — [SBP Payment Systems Review Q3FY26](https://www.sbp.org.pk/psd/pdf/PS-Review-Q3FY26.pdf) (via search summary)
- A national target of 2 million digital merchants was set. — [Profit Aug 2025](https://profit.pakistantoday.com.pk/2025/08/16/pakistan-targets-2-million-digital-merchants-120-million-online-banking-users-15-billion-digital-transactions-by-fy26/)
- Merchandiser pay (a proxy for field-force cost): 80% of Pakistani shelf-stacker/merchandisers earn PKR 22,837 to 84,360 per month gross. — [Paylab](https://paylab.com/pk/salaryinfo/commerce/shelf-stacker-merchandiser?lang=en). This is a salary range, not a per-outlet verification price.

### Inferences
- Likely buyers in rough order of plausibility: (1) fintech/wallet/bank merchant acquirers, (2) FMCG, pharma and B2B distributors needing outlet universe and route lists, (3) POS/software vendors, (4) exporters/importers and overseas buyers using the TDAP directory today, (5) NGOs/government for survey frames. This ranking is judgement, not evidence.
- A route-to-market budget benchmark: if a field visit costs a few hundred PKR, a verified outlet record priced well below that would be attractive. No price data was found to test this.

### Gaps
- No prices found for outlet census, lead lists, or retail audit (NielsenIQ and similar). No named buyer of purchased lists.
- No data on pharma distributor spend or telco/bank spend on merchant mapping.

## 4. Channels and behaviour

### Takeaway
Mobile payments and QR are growing fast, Facebook penetration is high, and WhatsApp is widely used by small sellers, but I found no Pakistan-specific survey of shop WhatsApp Business adoption or willingness to share numbers. Cash remains dominant at the shop level.

### Cited Findings
- Internet users: 117 million at end 2025, 45.6% penetration; 79.9 million social media user identities in Oct 2025 (31.2%). — [DataReportal Digital 2026 Pakistan](https://datareportal.com/reports/digital-2026-pakistan)
- Facebook: 69.4 million users and 53.7 million Messenger users in Aug 2026; LinkedIn 15.1 million. — [NapoleonCat](https://stats.napoleoncat.com/facebook-users-in-pakistan/2026/06/)
- Easypaisa: 55M+ registered and about 18-20M monthly active users. JazzCash: over 60 million registered customers (May 2026), PKR 16.8 trillion processed in year to March 2026 (+56%). — [TechJuice](https://www.techjuice.pk/easypaisa-vs-jazzcash-the-ultimate-mobile-wallet-showdown-in-2025/); [Simpaisa blog](https://www.simpaisa.com/blogs/how-to-accept-jazzcash-payments-on-your-website-step-by-step-2026/) (vendor blog, treat as indicative)
- Raast Q3 FY26: 742 million transactions, PKR 23.27 trillion; P2M transactions 55.9 million; QR merchant transactions 87.3 million. — [SBP PS Review Q3FY26](https://www.sbp.org.pk/psd/pdf/PS-Review-Q3FY26.pdf)
- Digital channels are 88% of retail payment transactions (FY2025) per a Simpaisa summary; however an IPA study states shopkeepers and customers keep choosing cash. — [Simpaisa](https://www.simpaisa.com/blogs/how-to-accept-jazzcash-payments-on-your-website-step-by-step-2026/); [IPA](https://poverty-action.org/why-pakistans-shopkeepers-and-customers-keep-choosing-cash-over-digital-payments) (page not fetched, only the title)
- E-commerce is about 1.3% of retail. SME adoption barriers include trust, payments and logistics. — [PIDE thesis 2019](https://thesis.pide.org.pk/thesis/promoting-e-commerce-exploring-opportunities-for-small-and-medium-enterprises-in-pakistan/) (dated)
- SMS: Jazz bundles around Rs 5 for 1,500 SMS (daily) and Rs 180 for 12,000 SMS (monthly); these are consumer bundles, not bulk-business rates. Telenor business SMS was Rs 1 per SMS in 2012. — [DailyCapital](https://dailycapital.pk/jazz-sms-packages-daily-weekly-monthly/); [ProPakistani 2012](https://propakistani.pk/2012/09/17/telenor-increases-sms-rates-for-postpaid-customers/)
- Retailers are wary of tax documentation: Tajir Dost produced Rs 3 million collected vs a Rs 10 billion target by Sept 2024. — [Dawn](https://www.dawn.com/news/amp/1855386)

### Inferences
- Wallet and Raast QR rails make Rs 200-1,000 micro-payments by shops technically feasible. JazzCash and Easypaisa are the natural collection route, with Raast for bank users.
- WhatsApp is probably the main outreach channel and SMS the fallback, but the WhatsApp Business claim is UNVERIFIED for Pakistan (the 97% figure that surfaced in search is from an Indian MSME survey and must not be used).
- Fear of tax exposure is a trust risk. Listing messages must say clearly that data is not shared with FBR (design inference).

### Gaps
- No Pakistan WhatsApp Business adoption rate for shops; no data on willingness to share numbers; no Urdu/Roman Urdu usage split found.
- No data on wallet fees for small merchants.

## 5. Law and compliance

### Takeaway
Spam is criminalised under PECA 2016 and regulated by PTA's 2009 spam regulations, so platform-delivered outreach must be consent-based and routed through approved bulk-SMS channels or WhatsApp business rules. Pakistan has no enacted data protection law as of May 2026. The payment, tax and company-structure questions (SBP rules for collecting fees and paying contributors abroad) were not resolved by the research and need local counsel.

### Cited Findings
- PECA Amendment Act 2025 was signed by the President on 30 Jan 2025. It adds section 26A (false or fake information) and creates a Social Media Protection and Regulatory Authority. I found nothing indicating it changed the spam provision. — [ARY News](https://arynews.tv/peca-amendment-act-2025-the-key-points/); court challenges and provinces made parties in 2026. — [Express Tribune](https://tribune.com.pk/story/2554524/provinces-made-party-to-case-against-peca-amendments); NCHR report criticised the amendments in Feb 2026. — [Legal500 guide via search](https://www.legal500.com/guides/chapter/pakistan-data-protection-cybersecurity/?export-pdf=)
- PECA 2016 spamming: first offence fine up to Rs 50,000; each subsequent violation fine from Rs 50,000 up to Rs 1 million. — [search extract of PECA text, KP CERC](https://kpcerc.kpitb.gov.pk/node/237). Section numbering conflicts: one source lists spamming as section 25 and spoofing as 26 (SJA index), another as 22 and 23. The 25/26 numbering matches my background knowledge (UNVERIFIED). Check the opt-out and consent exemptions in the statutory text, which I could not read. — [SJA PECA PDF](https://sja.gos.pk/assets/Updated_Laws/The%20Prevention%20of%20Electronic%20Crimes%20Act,%20Rules%20Final%20Index%20(%20Upto%20date%202025).pdf)
- PTA Protection from Spam, Unsolicited, Fraudulent and Obnoxious Communication Regulations 2009: mobile operators may not sell bulk SMS packages unless approved; per-SMS charging; maximum 500 SMS per day per subscription; complaints via short code 9000; a short code can be cancelled immediately if messages go to people who did not opt in. — [Khalid Zafar & Associates](https://khalidzafar.com/?p=2306); [PTA press release](https://www.pta.gov.pk/en/media-center/single-media/pta-issues-regulations-for-unsolicited-and-obnoxious-communications); PTA proposed new anti-spam rules in 2019 including a Do Call/SMS register. — [ProPakistani 2019](https://propakistani.pk/2019/10/25/pta-suggests-new-regulations-to-put-an-end-to-spam-calls-sms/)
- Personal Data Protection Bill: the 2023 draft was reportedly cabinet-approved but not passed by Parliament; further delay reported March 2025; no comprehensive law as of May 2026. It is GDPR-like with fines up to USD 2 million and a proposed National Commission for Personal Data Protection. — [Chambers 2026 guide](https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2026/pakistan); [Recording Law](https://www.recordinglaw.com/world-laws/world-data-privacy-laws/pakistan-data-privacy-laws/); [Arab News](https://arabnews.pk/node/1791371). Sources disagree on whether cabinet approval has happened (one says approved, others say still draft). Treat status as unsettled.
- Tax: the FY2025-26 budget introduced a Digital Presence Proceeds Tax Act with a 5% withholding on payments to digital vendors, but the levy on foreign online purchases was withdrawn retroactively from 1 July 2025 as part of trade talks, and one source says the burden stays on local startups. — [Profit](https://profit.pakistantoday.com.pk/?p=207358); [Arab News](https://www.arabnews.com/node/2610121/amp); [PhoneWorld](https://www.phoneworld.com.pk/pakistan-removes-5-tax-on-foreign-digital-services-keeps-burden-on-local-startups/). Applicability to a marketplace paying contributors is not established.
- Payments: PayPal is unavailable in Pakistan as of 2026; Payoneer and Skrill work; SBP has licensed or piloted local PSPs such as Safepay. — [Jobbers](https://www.jobbers.io/best-ways-to-receive-international-payments-in-pakistan-beyond-paypal/); [Profit](https://profit.pakistantoday.com.pk/?p=95318)

### Inferences
- A safe design is opt-in outreach: business owners claim a listing or consent to receive buyer messages, outreach goes via WhatsApp Business API and approved SMS aggregators, and the platform never cold-blasts scraped numbers. Scraping numbers for cold SMS would risk PECA and PTA violations (not legal advice).
- Absent a data protection law, risk is lower today but a future law is GDPR-like, so build consent records now.
- A Pakistani entity (SECP-registered private limited, FBR-registered) is probably needed to collect rupee fees through wallets and acquirers; paying contributors in Pakistan in PKR via Raast or wallets is simpler than cross-border payouts (inference; SBP rules not verified).

### Gaps
- Not found: SBP PSP/PSO licensing requirements for a marketplace collecting fees; outward remittance rules for paying overseas contributors; GST/withholding treatment of revenue shares; copyright and database rights in Pakistan (the Copyright Ordinance 1962 and its treatment of databases was not researched); the exact statutory text of the PECA spam exemptions; WhatsApp Business API policy for Pakistan.

## 6. Agent feasibility

### Takeaway
Agents can find businesses with an online footprint (Facebook Pages, Google Maps, Daraz, OLX, directories), but a majority of small shops are probably invisible online. Urdu OCR and extraction by frontier LLMs is workable but not perfect.

### Cited Findings
- Facebook reach 29% of the population; Messenger 22.5% (Aug 2026). — [NapoleonCat](https://stats.napoleoncat.com/facebook-users-in-pakistan/2026/06/)
- Urdu Nastaliq OCR: on the Urdu Newspaper Benchmark (829 paragraph images, 9,982 sentences), the best LLM (Gemini 2.5 Pro) reached a word error rate of 0.133; fine-tuning on 500 samples gave a 6.13% WER improvement. LLMs beat traditional OCR. — [arXiv 2505.13943](https://arxiv.org/abs/2505.13943?context=cs); [arXiv 2412.16119](https://arxiv.org/pdf/2412.16119). These are printed newspaper results, not shop signboards or hand-painted boards.
- E-commerce share of retail is 1.3%. — [PIDE](https://thesis.pide.org.pk/thesis/promoting-e-commerce-exploring-opportunities-for-small-and-medium-enterprises-in-pakistan/)

### Inferences
- Digital-visibility share of 3.2 million trade establishments: no measured figure. Using the 600k-800k FMCG outlets as a rough universe, even a high Facebook/Maps presence rate would leave most kiryana invisible. This is a hypothesis to test by sampling.
- Agents are best used for drafts in categories with strong online footprints and for pulling lists from PDFs and directories (including Urdu), with human or owner verification for the rest. Photo-based verification (shopfront images, signboards) should be the main field channel.

### Gaps
- No data on share of shops with Google Maps listings, Facebook Pages or websites. No Roman Urdu extraction benchmark found. No evidence on Google Maps ToS limits for agent use (not researched).

## 7. Suggested first wedge, evidence and unknowns

### Takeaway
Suggested wedge (hypothesis): Karachi or Lahore, one trade where there is both a trade body and a clear B2B buyer, with pharmacies/medical stores (buyers: pharma distributors and fintech merchant acquirers) as the lead candidate and mobile phone/accessory traders or auto spare parts as alternates. Treat this as a testable bet, not a finding.

### Cited Findings (supporting evidence)
- Scale and concentration: Punjab 58% and Sindh 20% of establishments; 3.22 million trade establishments. — [Deccan Herald](https://www.deccanherald.com/amp/story/world%2Fpakistan-has-more-mosques-and-madrassas-compared-to-factories-says-economic-census-3693076); [TechJuice](https://www.techjuice.pk/services-sector-jobs-lead-pakistan-employment-after-new-census/)
- Buyer demand signals: B2B distribution startups (Bazaar, SnappRetail) and Raast merchant targets. — sources in section 3.
- DRAP licensing means pharmacies and distributors are licensed and therefore theoretically listable. — [DRAP](https://www.dra.gov.pk/?p=34380)
- Payment rails: wallets (60M JazzCash registered) and Raast QR. — section 4.

### Inferences
- Why pharmacies: licensed (so verifiable), repeat B2B purchasers, concentrated in clusters, with distributors and pharma companies already paying field forces. Why not kiryana first: largest and least visible, but already contested by funded distributors with field forces.
- Alternative wedge: exporter/importer lists (TDAP directory plus chambers) sold to overseas buyers in USD. It has a smaller local counterpart and easier cross-border payment, but the data gap is weaker because TDAP already publishes a directory.
- Staging: (1) measure the gap with a Karachi/Lahore POI count versus census; (2) approach one trade association for member-list consent; (3) agent drafts plus WhatsApp owner verification; (4) sell to 3 to 5 distributors; (5) collect via Raast/wallet.

### Gaps
- Unknown: outlet counts for pharmacies, spare parts, mobile traders by city; buyer willingness to pay; association cooperation; legal route for fee collection and contributor payouts; owner response rates to WhatsApp verification.
- Unknown whether Pakistan is better than other candidate markets; no comparison was done in this note.
