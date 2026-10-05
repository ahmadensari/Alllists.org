# Gulf states and wider Middle East as launch markets for AllLists.org

Scope: UAE, Saudi Arabia, Qatar, Kuwait, Oman, Bahrain, Egypt, Jordan, Iraq, Lebanon, Turkey. Research date: 2026-10-05. Planning research, not legal advice.

Method and reliability warning for the report writer: this note rests almost entirely on web-search result summaries. Direct page fetches were blocked by the network egress proxy for thenationalnews.com, morganlewis.com, businessdataguide.com, turtl.tamimi.com, dubaichamber.com, mediaoffice.ae, clydeco.com and docs.overturemaps.org. No primary page (chamber, ministry, regulator, law firm) could be read in full. Many sources are law-firm-style or SEO/aggregator blogs; these are flagged "(aggregator)" where the quality is low. Several important questions (country-by-country map completeness for Arabic small businesses; chamber terms of use; prices actually paid for lists) returned no usable evidence and are listed under Gaps rather than guessed. Nothing below should be treated as verified legal position.

## 1. Data gap evidence: how complete and current are Google Maps, OSM, Overture and Foursquare for small businesses (especially Arabic script and migrant-run trades)?

### Takeaway
I found no study or count that measures small-business completeness on Google Maps, OSM, Overture or Foursquare in any of the 11 countries, so the "data gap" thesis is currently an inference, not a measured fact. Overture's places layer is dominated by Meta (about 59m of about 64m+ places globally) with Foursquare a small contributor, and the only Gulf-specific counts found are very small (28,637 places in a Riyadh Region dataset).

### Cited Findings
- Overture places theme contains more than 64 million point features; as of April 2026 the source counts were Meta 59,413,511, Microsoft 7,261,643, Foursquare 6,749,057, AllThePlaces 1,749,242, PinMeTo 147,902, DAC 166,108 (global, not Gulf-specific) — [Overture Summit 2026 slides via search](https://hosted-files.sched.co/overturesummit2026/39/Places%20Surge%20Headliner.pdf); [Overture Places Guide](https://docs.overturemaps.org/guides/places)
- A third-party "Riyadh Region" places extract on Source Cooperative holds 28,637 places (area-of-interest records); the source and the extraction date were not verified — [Source Cooperative tabaqat/riyadh-places](https://source.coop/tabaqat/riyadh-places)
- Overture's October 2024 release added more than 30,000 km of TomTom road features in Saudi Arabia (roads, not places; indicates Overture investing in KSA but says nothing on business coverage) — [Overture October release preview](https://docs.overturemaps.org/blog/2024/10/21/preview-october-release/)
- An academic assessment of OSM data exists for Abu Dhabi city (UAE University); I could only see the title, not the findings — [UAEU research record](https://research.uaeu.ac.ae/en/publications/assessment-of-openstreetmap-osm-data-the-case-of-abu-dhabi-city-u/fingerprints/)
- Google Maps in Kuwait, Bahrain, Qatar, Algeria and Libya was built "in large part" by user edits via the (now retired) Map Maker, per a 2011 report, i.e. user-generated rather than systematic business coverage — [Geospatial World](https://geospatialworld.net/news/google-maps-now-in-middle-east-north-africa/) (2011; very dated)
- Transliteration is a documented data-quality problem: one name can appear in many Latin spellings ("Jumeirah" cited with up to five), dialect variants and no universal Arabic transliteration standard; one practitioner source reports about 10 percent of geocodes lost to truncated long Arabic address strings, and that small POI and road names in Arabic can be hard to verify online or are absent — [UN GEGN toponymy papers](https://unstats.un.org/unsd/ungegn/sessions/4th_session_2025/documents/GEGN.2_2025_142_CRP142_presentation_Oman.pdf); [OSM community thread on Arabic names](https://community-cdn.openstreetmap.org/t/arabic-names/82299/12) (practitioner anecdote, not a measured study)
- Informality as a proxy for invisibility: roughly 84 percent of Iraqi MSMEs operate informally, about 56 percent of Egyptian workers are informal, and the unofficial sector is about 26 percent of Jordan's economy — [UNCTAD/etradeforall and related snippets](https://etradeforall.org/fr/node/15168); [Friedrich Naumann Foundation Jordan MSME paper](https://www.freiheit.org/sites/default/files/import/2019-12/20979-publicationsocio-economicreformsandjordansforeignpolicyschmidmsmes.pdf) (snippet-level, years vary)

### Inferences
- Because Meta supplies most Overture places and Meta's places derive from Facebook Pages, businesses without a Facebook Page (many informal Iraqi, Egyptian, Lebanese and migrant-run shops) are likely under-covered; this is an inference, not tested.
- Formal licensed firms in the UAE and KSA (over 1 million licences each, see section 2) are the likeliest to be already on Google Maps; the data gap there is more likely to be in currency, verified contact (owner WhatsApp), Arabic/English name pairing and trade-category detail than in raw presence. Needs a sampling test (see Gaps).
- Informal-economy countries (Iraq, Egypt, Jordan, Lebanon) probably have the largest raw coverage gaps but the weakest buyer budgets and payment rails.

### Gaps
- No published completeness study found for Google Maps, OSM, Foursquare or Overture for any of the 11 countries. Recommended: a 100-business street-walk or registry-sample test in Deira/Karama (Dubai), Sharjah Industrial Area, Riyadh Batha, Cairo, Istanbul Bayrampasa, measuring presence, correct Arabic name, phone, WhatsApp, hours.
- No evidence on Arabic-script name accuracy per platform; no counts for migrant-run trades (groceries/baqalas, repair, laundry, trading firms) on any platform.
- Foursquare's current Gulf footprint unknown (Foursquare's global open-source places data feeds Overture, but no per-country numbers found).
- Overture per-country place counts for UAE/KSA/others were not found (docs page could not be fetched).

## 2. Existing data holders: chambers, registries, licence portals, free zones, associations (what is public, terms, reuse limits)

### Takeaway
Registries are large and digitised in the UAE, KSA and Turkey, but public bulk reuse is unclear everywhere: Saudi Arabia offers a paid/controlled API gateway (Wathq) and announced free commercial-registration data for the business sector, and the Dubai Chamber has a directory of 245,000+ members plus an open-data page whose terms I could not read. No evidence found of permissive bulk-reuse licences for business contact data.

### Cited Findings
- UAE: more than 1.4 million licensed businesses, about 760,000 new companies between September 2021 and 2025 (+118.7 percent vs mid-2021) — [UAE business-licence news summary via search](https://cairoscene.com/buzz/dubai-accounts-for-59-of-uae-business-licences-in-q1-2025) (secondary; ministry figure not seen)
- Dubai holds 59 percent of UAE commercial licences as of March 2025, approaching 990,000 licences across economic departments and licence-issuing authorities; about 19,000 of about 40,000 national new licences in Q1 2025 were in Dubai — [CairoScene, 2025-04](https://cairoscene.com/Buzz/Dubai-Accounts-for-59-of-UAE-Business-Licences-in-Q1-2025)
- Dubai Chambers directory: "more than 245,000 businesses with a DCCI membership" (date uncertain; Gulf News article is old) and the directory is described as a registry of member companies — [Gulf News: DCCI unveils commercial directory](https://gulfnews.com/business/dcci-unveils-commercial-directory-1.295227). Dubai Chamber operates an "open data" page — [Dubai Chamber open data](https://dubaichamber.com/en/open-data) (contents and terms not readable; blocked)
- Dubai: a 2025 Executive Council resolution eased free-zone firms operating on the mainland — [Reed Smith](https://www.reedsmith.com/our-insights/blogs/viewpoints/102l0qt/new-era-for-free-zone-mainland-integration-dubais-executive-council-resolution/)
- Saudi Arabia: single national Commercial Register run by Ministry of Commerce via the Saudi Business Center; the new Commercial Register Law applies from 3 April 2025 (one unified registration, sub-registers abolished, annual electronic confirmation instead of renewal) — [Business Data Guide, Saudi Arabia](https://businessdataguide.com/blog/jurisdictions/saudi-arabia-company-search-guide) (aggregator; page not fetched)
- Wathq (developer.wathq.sa) is a government-backed API gateway for verified data from accredited government entities; Ministry of Commerce announced it would provide commercial registration data free for the business sector to support SMEs and e-commerce (date of announcement not seen) — [Wathq overview, Noqta](https://noqta.tn/en/blog/maroof-wathq-api-business-verification-saudi-2026); [Ministry of Commerce news item](https://mc.gov.sa/en/mediacenter/News/Pages/12-05-19-02.aspx)
- Saudi SMEs: more than 1.8 million SMEs in 2025 (earlier figure 1.3 million at end of 2023) — [Arab News on Monsha'at](https://arab.news/gfjy8); SME lending SR420.7 billion at end Q2 2025, up 37 percent year on year — [Arab News/SAMA](https://www.arabnews.pk/node/2585794)
- Turkey: Trade Registry Gazette is a public database updated daily by TOBB; all transactions through MERSIS; 1,336,321 legal entities in the trade registry as of May 2026 per an open-data aggregator — [Sayari Learn](https://learn.sayari.com/turkish-trade-registry-gazette/); [Infoproff Turkey](https://www.infoproff.com/en/open-data/turkey/247/business-register-in-turkey) (aggregator)
- Iraq launched an online company-registration portal cutting registration from 35 steps to 5; 2,981 entrepreneurs registered in the first year — [UNCTAD](https://unctad.org/news/iraq-online-portal-opens-doors-women-business)

### Inferences
- The UAE has a three-layer structure (each emirate's economic department, free zone authorities, chambers), so no single registry covers all; a contributor-plus-agent model that reconciles them could add value but each source's terms need checking before any bulk ingest.
- Saudi Wathq is the most explicit "official verification API" and could serve as a verification oracle for contributors (checking CR numbers) rather than as a bulk list source, subject to access terms.

### Gaps
- Terms of use and reuse limits for Dubai Chamber, Abu Dhabi Chamber, Sharjah Chamber, Federation of Saudi Chambers, Qatar Chamber, Kuwait Chamber, Egyptian Federation of Chambers: none obtained (sites blocked or search returned no terms).
- Wathq pricing and licence terms, UAE DED/DET public search terms, Qatar MOCI, Egypt GAFI registry access: not found.
- Free-zone directories (DMCC, JAFZA, DAFZA, SAIF, etc.), trade associations: not researched in depth; no sources found in this session.
- Jordan, Lebanon, Kuwait, Oman, Bahrain registry openness: not found.

## 3. Buyers and budgets: who would pay, price evidence, B2B marketplace performance

### Takeaway
Evidence of prices is thin and mostly from vendor marketing: qualified B2B leads in the UAE are quoted at AED 1,200-3,500 (enterprise SaaS), and bulk UAE email lists sell around USD 850 for about 250k contacts, which implies a low price floor for raw lists and a high value for verified, qualified outreach. Government-backed B2B marketplace Tradeling reports 200,000+ registered business customers, showing platform demand exists but also that a state-backed player occupies the "SME buyer" slot.

### Cited Findings
- Cost per qualified lead in the UAE: enterprise SaaS AED 1,200 to 3,500; financial-services or government leads can exceed AED 8,000 (agency marketing content, not audited) — [Upgrowth, Dubai B2B lead generation channels](https://upgrowth.in/dubai-b2b-lead-generation-channels/)
- Agency pricing: outbound (LinkedIn/email) pipeline building AED 5,000-12,000 per month; full lead-gen retainer AED 10,000-25,000 per month; paid ads management AED 3,000-7,000 per month plus spend — [Upgrowth](https://upgrowth.in/dubai-b2b-lead-generation-channels/); [Salesbox UAE lead gen list](https://salesbox.ai/blog/top-lead-gen-companies-uae-2026)
- A UAE business email list of about 250,000 contacts is listed for about USD 850 one-time — [DataHub listing](https://datahub.io/@datalists/b2b/UAE-Business-Email-List-Database) (commodity list seller; quality and legality unverified)
- Tradeling: one source claims 50,000+ business buyers and 120,000 sellers across 14 categories; another states 200,000+ registered business customers and about 3 million requests per day; month-on-month revenue growth about 35 percent (self-reported, undated, inconsistent between sources) — [Images Retail ME](https://www.imagesretailme.com/tradeling-strengthens-uaes-reputation-as-a-global-trade-hub/); [Gulf News on Tradeling](https://gulfnews.com/business/retail/dubai-owned-b2b-marketplace-tradeling-is-out-to-win-the-percentage-game-1.85940538)
- January 2026: Dubai Department of Economy and Tourism and Dubai Chambers partnered with Tradeling (page not readable; only headline seen) — [Dubai Media Office](https://mediaoffice.ae/en/news/2026/january/26-01/det-and-dubai-chambers-partner-with-tradeling)
- Pakistan to UAE: exports USD 1.92 billion (2025 annual) and USD 1.424 billion in Jul-Feb FY2025-26; to Saudi Arabia about USD 692 million (2025) and USD 687 million in FY2025-26 vs USD 724 million prior year — [Trading Economics/APP via search](https://jp.tradingeconomics.com/pakistan/exports-annual); [ProPakistani, Saudis lower imports from Pakistan](https://propakistani.pk/2026/08/17/saudis-lower-imports-from-pakistan/) (summary mixes two different periods; treat with care)
- Noon is a consumer marketplace (about USD 1.37 billion GMV cited by a blog); no data found on a separate "Noon Business"; no data found for Amazon Business UAE/KSA, Dubizzle B2B, Alibaba GCC, or Yellow Pages UAE performance — [Virtuzone ecommerce blog](https://virtuzone.com/blog/ecommerce-industry-uae/)
- Saudi SME financing is growing fast (SR420.7 billion at Q2 2025), pointing to banks/fintechs as SME-targeting buyers — [Arab News/SAMA](https://www.arabnews.pk/node/2585794)

### Inferences
- Likeliest paying buyers: (a) importers and distributors who need verified downstream retailer/wholesaler lists with WhatsApp contacts; (b) exporters from Pakistan, India, China, Turkey seeking Gulf buyers; (c) SME-focused fintech, POS and software vendors. Telcos and banks pay more per lead but need compliance and procurement cycles. None of these buyer classes has been validated with interviews or price quotes.
- The lead-price anchor (AED 1,200+ per qualified enterprise lead vs about USD 0.003 per record in commodity lists) suggests AllLists should sell outcomes (verified, responded contacts, delivered outreach) rather than raw records, consistent with its platform-delivered model.
- Tradeling, with government backing and a Dubai DET/Chambers tie-up, is a potential partner or competitor, not a gap.

### Gaps
- No evidence of actual transaction prices for business lists in KSA, Qatar, Kuwait, Oman, Bahrain, Egypt, Jordan, Iraq, Lebanon, Turkey.
- No performance data (conversion, retention) for Dubizzle B2B, Yellow Pages UAE/Dubai Yellow Pages, Noon Business, Amazon Business, Alibaba.
- No data on free-zone or government budgets for business-data products.
- Willingness to pay of Pakistani/Indian/Chinese/Turkish exporters: no survey found.

## 4. The migrant-trader angle: diasporas, language, WhatsApp, community networks; Pakistan/India-to-Gulf bridge

### Takeaway
Gulf South Asian communities are huge, WhatsApp is the dominant business channel, and Dubai's Deira/Bur Dubai re-export trade is run largely by Indian (and other South Asian) trader networks, so a Gulf-based, WhatsApp-first, multilingual (Arabic, English, Urdu, Hindi, Malayalam) list product has a plausible bridge role. Hard numbers on migrant-run shop counts and WhatsApp-led discovery are missing.

### Cited Findings
- About 2 million Pakistanis live in the UAE, mostly Dubai and the Northern Emirates; nearly half of the Pakistani diaspora is in the Gulf — [Khaleej Times on Pakistani remittances](https://www.khaleejtimes.com/business/overseas-pakistanis-send-record-416-billion-remittances-saudi-uae-lead); [Digital Pakistan](https://digitalpakistan.pk/pakistan-remittances-2025-the-38-billion-lifeline-explained-simply/) (diaspora count from secondary source, date unclear)
- Pakistani remittances rose 8.6 percent to USD 41.6 billion in FY2025-26; Saudi Arabia USD 9.78 billion, UAE USD 8.80 billion — [Khaleej Times](https://www.khaleejtimes.com/business/overseas-pakistanis-send-record-416-billion-remittances-saudi-uae-lead)
- 151,000+ Pakistani workers went to Gulf countries in Q1 2025 — [Arab News](https://arab.news/pp4hf)
- Dubai wholesale shops in Bur Dubai and Deira receive Chinese fabrics re-exported via Jebel Ali; Indian diaspora networks in China and Dubai mediate many transnational trade deals (academic piece) — [NUS Middle East Institute Insight 188](https://mei.nus.edu.sg/publication/insight-188-china-dubai-textile-trade-through-indian-connections/)
- Over 90 percent of UAE smartphone users open WhatsApp daily; WhatsApp is the preferred channel for high-intent and service-driven business interactions (vendor blog claims) — [QuickReply UAE WhatsApp](https://www.quickreply.ai/ae/whatsapp-business-api); [Gulf News on WhatsApp calls and business](https://gulfnews.com/business/unblocking-whatapp-calls-will-be-a-boost-for-business-say-executives-1.67675336)
- Indian trader warehouses in Dubai: "over 55,000 new commercial licences in 2024" in Dubai, with a growing Indian-trader share (aggregator; unverified) — [Dubai South BH](https://dubaisouthbh.com/moving-to-dubai/indian-traders-opening-a-dubai-warehouse-operation)

### Inferences
- A corridor product ("verified Gulf buyers for Pakistani/Indian exporters" and the reverse) fits the data: remittance and trade flows are large, and exporters at home cannot see Gulf shop-level demand. This is inference only.
- Discovery in these communities is likely word-of-mouth, WhatsApp groups and Facebook pages rather than Google Maps; this would raise the value of contributor-led collection but also raises consent issues (see section 5).

### Gaps
- No count of South Asian-owned shops, baqalas, laundries or repair shops in the UAE, KSA, Qatar, Kuwait, Oman or Bahrain.
- No study of WhatsApp-group-based B2B discovery among migrant traders.
- Pakistan/India-specific exporter pain-point evidence (e.g., TDAP, FPCCI or EEPC statements) not found.
- Qatar, Kuwait, Oman, Bahrain diaspora sizes not retrieved.

## 5. Law and compliance

### Takeaway
All Gulf countries except possibly Kuwait now have a general data-protection law with marketing-consent provisions, and the UAE actively enforces telemarketing rules (DNCR, fines, licences). B2B outreach is not clearly exempt in most Gulf regimes (Turkey is the exception: tradesmen and merchants can receive commercial messages without prior consent). Scraping Google Maps content for lead lists is prohibited by Google's terms. All of this needs local counsel before launch.

### Cited Findings
UAE
- Federal Decree-Law 45 of 2021 (PDPL) has been in force since 2 January 2022; sources conflict on Executive Regulations: one says as of August 2026 they remain unissued, another says they have been issued with compliance by 1 January 2027 — [Primerus UAE data privacy note](https://www.primerus.com/sites/default/files/2026-03/UAE%20Data%20Privacy%20Law.pdf); [UAE data protection law 2026 guide (aggregator)](https://bshsoft.com/uae-data-protection-law-2026-guide); [ConsentStack](https://consentstack.io/regulations/uae-pdpl). Status is unresolved; check the UAE Data Office.
- TDRA's Do Not Call Registry launched September 2022; registered numbers cannot be contacted for marketing calls, SMS and emails, even with prior consent — [Gulf News DNCR explainer](https://gulfnews.com/living-in-uae/telephone-internet/how-to-block-telemarketing-calls-in-the-uae--all-you-need-to-know-about-the-do-not-call-registry-1.1667573547539); [Virgin Mobile UAE DNCR](https://virginmobile.ae/dncr/)
- Telemarketing regulations (adopted 2024): prior approval from authority needed to telemarket, calls only 9am-6pm, personal numbers may not be used for marketing; covers calls and marketing SMS/social-app messages to consumers — [Morgan Lewis](https://www.morganlewis.com/ru/blogs/sourcingatmorganlewis/2024/07/telemarketing-in-an-evolving-legal-landscape-uae-adopts-regulations-on-telemarketing-activities); [Nukta on fines up to AED 150k](https://nukta.com/up-to-aed-150k-fines-new-uae-regulations-target-unwanted-telemarketing-calls); [UAE Ministry of Economy/WAM](https://www.wam.ae/en/article/143d7h5-ministry-economy-reviews-regulatory-legislation)
- Enforcement as of June 2026: 3,301 violations against individuals, AED 19.19 million fines, 9,433 numbers cut; AED 5,000 first fine rising to AED 50,000 and 12-month service ban — [The National, 2026-08-06](https://thenationalnews.com/news/uae/2026/08/06/dh19-million-in-fines-issued-and-9400-numbers-disconnected-for-telemarketing-violations); [Khaleej Times](https://www.khaleejtimes.com/uae/tdra-uae-telemarketing-violations-fines-numbers-cut)
- UAE e-commerce platform setup: trade licence required for online sellers (fines up to AED 50,000 otherwise); a "portal/marketplace" licence exists for platforms connecting buyers and sellers and is open to foreigners; most free zones allow 100 percent foreign ownership of e-commerce activities — [Meydan Free Zone](https://www.meydanfz.ae/relocation-dubai-us/ecommerce-business-setup-dubai-american-entrepreneurs); [UpperSetup](https://uppersetup.com/en/article/e-commerce-in-the-uae-how-to-launch-a-business-in-2026) (aggregators)

Saudi Arabia
- Marketing communications governed by PDPL and its Regulations, the CST Regulations for Curbing SPAM Messages and Calls, and the E-Commerce Law; PDPL requires prior, freely given, documented consent for marketing with simple opt-out; fines up to SAR 5 million, doubled for repeats; SDAIA violation-review committees active — [Al Tamimi, marketing consent in Saudi Arabia](https://turtl.tamimi.com/story/law-update-issue-367-saudi-arabia-and-competition/page/11); [Clyde & Co on PDPL consultation, 2025-05](https://www.clydeco.com/en/insights/2025/05/saudi-arabia-new-pdp-law-consultation); [Captain Compliance on PDPL anniversary](https://captaincompliance.com/?p=9828)
- SDAIA issued a third public consultation on PDPL Implementing Regulation amendments in April 2025 — [Clyde & Co](https://www.clydeco.com/en/insights/2025/05/saudi-arabia-new-pdp-law-consultation)
- Foreign e-commerce: MISA licence needed for foreign-owned operating entity; one source says no specific licence is required for a foreign company selling online without local presence but E-Commerce Law duties apply (sources differ) — [Healy Consultants](https://www.healyconsultants.com/saudi-arabia-company-registration/e-commerce-business/); [Al Tamimi, cross-border e-commerce licensing in the GCC](https://www.tamimi.com/law-update/technology-media-telecommunications-august-2021/articles/cross-border-e-commerce-in-the-gcc-a-licensing-perspective/)

Qatar
- PDPPL (Law 13 of 2016) prohibits direct electronic marketing communications without prior consent, requires sender identification and an opt-out route; enforced by NCGAA/NCSA, with guidelines issued January 2021 — [Mondaq](https://www.mondaq.com/privacy-protection/544052/new-national-privacy-law-in-qatar); [Securiti](https://securiti.ai/qatar-personal-data-protection-law/)

Oman, Bahrain, Kuwait
- Oman PDPL: Royal Decree 6/2022, in force 13 February 2023 — [CMS Oman guide](https://cms.law/en/int/expert-guides/cms-expert-guide-to-data-protection-and-cyber-security-laws/oman); Bahrain PDPL: Law 30 of 2018, in force 1 August 2019, with a right to object to direct marketing — [Clyde & Co Bahrain infographic](https://www.clydeco.com/uploads/Files/Bahrain_Data_Protection_Infographic.pdf); Kuwait: Data Privacy Protection Regulation (CITRA Decision 42/2021) — [Kennedys GCC overview](https://kennedyslaw.com/thought-leadership/article/an-overview-of-personal-data-protection-laws-in-the-member-states-of-the-cooperation-council-for-the-arab-states-of-the-gulf-gulf-cooperation-council-gcc)

Egypt
- Executive Regulations to Law 151 of 2020 issued by Ministerial Decision 816/2025 on 1 November 2025, starting a one-year compliance period; they cover consent, licensing, cross-border transfers and direct electronic marketing; a licence from the Personal Data Protection Center (valid 3 years) is needed for activities including electronic marketing — [CMS](https://cms.law/en/are/legal-updates/egypt-s-pdpl-executive-regulations-issued-one-year-compliance-countdown-begins); [Al Tamimi](https://www.tamimi.com/law_update_articles/from-policy-to-practice-egypt-issues-executive-regulations-of-the-personal-data-protection-law/); [Clyde & Co, 2026-01](https://www.clydeco.com/fr/insights/2026/01/egypt-regulatory-update-on-data-privacy)

Turkey
- Commercial electronic messages governed by Law 6563 (ETK) plus KVKK (Law 6698); consents must be recorded in the national IYS system; B2C opt-in; messages to tradesmen and merchants (esnaf and tacir) may be sent without prior consent, opt-out honoured within 3 business days — [Moroglu Arseven](https://www.morogluarseven.com/news-and-publications/turkey-introduces-centralised-system-for-recording-approvals-about-commercial-electronic-messages); [Egressif](https://egressif.io/resources/compliance/turkey-kvkk-etk); [Makdos on IYS](https://makdos.com/en/blog/iys-message-management-system/842707/iys-for-small-businesses-what-to-get-right-in-turkiye/)

Scraping and platform rules
- Google Maps Platform terms prohibit scraping, bulk export, caching beyond 30 days (place IDs exempt), and creating mailing or telemarketing lists from Maps content — [Google Maps Platform service terms](https://cloud.google.com/maps-platform/terms/maps-service-terms/index-20231025); [Thunderbit summary](https://thunderbit.com/blog/is-scraping-google-maps-legal); [OpenPlacesAPI caching comparison](https://openplacesapi.com/blog/can-you-store-places-api-results)
- WhatsApp Business pricing in UAE (vendor figures): marketing AED 1.20-1.45 per conversation, utility AED 0.15-0.20, authentication AED 0.30-0.40; service messages free in the 24-hour window; Meta's pricing model has changed over time, so verify — [ChatDaddy](https://chatdaddy.tech/blog/whatsapp-business-api-uae); [QuickReply](https://www.quickreply.ai/ae/whatsapp-business-api)

### Inferences
- A platform that sends outreach on behalf of buyers is likely a "controller" or joint controller for recipient data and, in the UAE, probably needs a TDRA telemarketing approval for SMS/call campaigns to consumers; whether sole-proprietor shop owners count as "consumers" under DNCR is untested (open legal question).
- Turkey's merchant exemption makes it the legally easiest B2B cold-outreach market in the set; the UAE and KSA need opt-in or legitimate-interest analysis per message type.
- Using official registry data (Wathq, MERSIS) and owner-verified contributor data is safer than Google-derived data; Google Maps content must not feed the lists.
- Owner-submitted and contributor-verified data with explicit consent and a clear opt-out matches the consent language in the PDPL regimes (UAE, KSA, Qatar, Egypt).

### Gaps
- Primary texts and regulator guidance not read; law-firm notes read only as search snippets.
- Whether UAE PDPL and the TDRA telemarketing rules apply to B2B or sole-trader recipients not established.
- DIFC (DIFC Law 5 of 2020) and ADGM data-protection regimes: no source found in this session.
- Kuwait CITRA regulation details, Jordan's Personal Data Protection Law (2023), Iraq and Lebanon data law status, Saudi CST spam-rule specifics (B2B treatment, opt-out requirements): not found.
- Egypt marketing licence specifics (whether B2B lists need a licence) not confirmed.
- Foreign-company platform licensing in Qatar, Kuwait, Oman, Bahrain, Egypt, Turkey not researched.

## 6. Payments: local gateways, Mada, Apple Pay, Stripe, payouts to contributors, VAT on digital services

### Takeaway
Card acceptance is well served: Stripe operates natively for UAE and Saudi Arabian businesses, and Tap Payments, PayTabs, Telr and MyFatoorah cover Mada, Apple Pay and local wallets across the GCC. The harder parts (not resolved here) are paying contributors abroad and VAT/tax position.

### Cited Findings
- Stripe: supports UAE-registered businesses at 2.9% + 30 cents with AED settlement and T+5 payouts, and is available in Saudi Arabia on the same headline pricing with SAR settlement (secondary directory pricing; confirm with Stripe) — [LearnWithHasan UAE gateways](https://learnwithhasan.com/payment-gateways/country/united-arab-emirates/); [LearnWithHasan Saudi gateways](https://learnwithhasan.com/payment-gateways/country/saudi-arabia/)
- Tap Payments: Mada at 1 percent capped at SAR 200, Apple Pay over Mada, STC Pay, SAR settlement; received a Central Bank of the UAE retail payment services licence in April 2025, completing approvals across all six GCC markets — [CMARIX Saudi gateway guide, 2026](https://www.cmarix.com/blog/best-payment-gateways-in-saudi-arabia/); [Tap Payments profile](https://learnwithhasan.com/payment-gateways/tap-payments/)
- PayTabs: SAMA-certified, supports Mada, wallets, bank transfer and BNPL, next-day SAR settlement; Telr popular with UAE SMEs; comparison of PayTabs, Telr, MyFatoorah — [CodingClave comparison 2026](https://codingclave.com/blog/paytabs-vs-telr-vs-myfatoorah-uae-gulf-2026); [Ziina on Stripe alternatives](https://ziina.com/blog/stripe-alternatives-for-small-to-medium-sized-businesses)
- UAE VAT is 5 percent from 1 January 2018; non-resident providers of electronic services to consumers must register (no threshold) via the FTA EmaraTax portal; B2B supplies to UAE VAT-registered customers use the reverse charge — [VATCalc UAE e-services](https://www.vatcalc.com/uae/uae-value-added-tax-on-non-resident-digital-services/); [Farahat & Co](https://farahatco.com/blog/vat-treatment-supply-electronic-services-uae)
- UAE, Saudi Arabia, Bahrain and Oman tax non-resident digital services (Saudi rate and rules not confirmed in the search results) — [Kintsugi Middle East guide](https://trykintsugi.com/sales-tax-guides/middle-east)

### Inferences
- A UAE free-zone or mainland entity with Stripe or Tap would give AED/SAR acceptance, Mada and Apple Pay; this also simplifies VAT registration and local invoicing, at the cost of entity setup.
- Because buyers are businesses, a UAE entity with B2B reverse-charge invoicing keeps VAT simple for UAE buyers; B2C-like micro-shop buyers would trigger 5 percent output VAT.

### Gaps
- Cross-border payouts to contributors in Pakistan, India, Egypt, etc. (Stripe Connect availability, Wise, local rails, UAE exchange houses): no sources found.
- Saudi VAT 15 percent and ZATCA e-invoicing application to a foreign platform: not confirmed with a source.
- Payment details for Qatar, Kuwait, Oman, Bahrain, Egypt, Jordan, Iraq, Lebanon, Turkey (Iyzico, Paymob, KNET, Benefit etc.) not researched; Iraq and Lebanon likely have severe card/banking constraints (unverified).
- Merchant-of-record or marketplace payout regulation (CBUAE) not researched.

## 7. Agent feasibility: Arabic extraction, web presence of small businesses, Google Maps dominance, scraping restrictions

### Takeaway
Scraping Google Maps is contractually prohibited and cannot legally underpin a list product; Overture/OSM are open alternatives with limited small-business depth; the web presence of migrant-run small trades is likely thin and WhatsApp/Facebook/Instagram-centred. I found no measured benchmark of Arabic LLM extraction quality for business pages.

### Cited Findings
- Google Maps Platform terms ban bulk extraction and list-building from Maps content (see section 5) — [Google Maps Platform service terms](https://cloud.google.com/maps-platform/terms/maps-service-terms/index-20231025)
- Overture places are open data built mainly from Meta (59.4m features), Microsoft (7.3m) and Foursquare (6.7m) as of April 2026 — [Overture Summit 2026 slides](https://hosted-files.sched.co/overturesummit2026/39/Places%20Surge%20Headliner.pdf)
- Arabic place names show high transliteration variance and lacking standards, hurting matching and geocoding — [UN GEGN](https://unstats.un.org/unsd/ungegn/sessions/4th_session_2025/documents/GEGN.2_2025_142_CRP142_presentation_Oman.pdf)
- WhatsApp Business app (free) and API are widely used by UAE SMEs; the API requires approved templates and verified business identities — [SleekFlow UAE guide](https://phrase-marketing.sleekflow.io/blog/how-to-set-up-a-whatsapp-business-account-in-uae); [Wetarseel](https://wetarseel.ai/whatsapp-business-api-for-abu-dhabi-pricing-use-cases-best-providers-2026/)

### Inferences
- Agent drafting should seed from registries (Wathq, MERSIS, emirate licence searches where terms allow), Overture/OSM and owner-supplied data, with human or owner verification to reconcile Arabic/English name pairs; this matches the stated "AI drafts, owners verify" design.
- Where the web footprint is thin (street-level shops), the verification step by owners and contributors is the actual product, which supports starting where contributor density is high (Dubai/Sharjah South Asian trade districts).

### Gaps
- No benchmark of Arabic extraction accuracy on small-business sites or social profiles; no data on share of small businesses with a website versus social-only presence per country.
- robots.txt and ToS of the registries and chamber directories not checked.
- Terms for Meta/Facebook page data reuse not researched.

## 8. Recommendation: best one or two entry points

### Takeaway
Provisional recommendation (evidence is limited and needs validation): Wedge 1 is the UAE (Dubai plus Sharjah/Northern Emirates) with a trade-corridor focus on South Asian-run wholesale, trading and distribution firms, sold to Pakistani/Indian exporters and UAE importers/distributors; Wedge 2 is Turkey as the legally easiest B2B outreach market and a supply-side exporter into the Gulf, or alternatively Saudi Arabia (verification via Wathq, 1.8 million SMEs) as the second-phase scale market. Iraq, Lebanon, Egypt and Jordan have the largest likely data gaps but weak evidence of budgets and payments.

### Cited Findings
- UAE: 1.4 million+ licensed businesses; Dubai about 990,000 licences; Tradeling reaches 200,000+ registered business customers; Stripe/Tap operate natively; free-zone e-commerce/portal licences open to foreign owners; active enforcement of telemarketing rules (see sections 2, 3, 5, 6)
- Pakistan-UAE exports USD 1.92 billion (2025), about 2 million Pakistanis in the UAE; UAE-Pakistan remittances USD 8.80 billion (see section 4)
- Turkey: 1.34 million legal entities (May 2026) and a merchants exemption from consent for commercial messages (see sections 2, 5)
- Saudi Arabia: 1.8 million SMEs, SR420.7 billion SME lending, official Wathq API, PDPL enforcement already active (see sections 2, 5)

### Inferences
- UAE rationale: highest density of South Asian trader networks, English/Arabic/Urdu business, WhatsApp-first norms, easiest entity and payments setup, large licensed base, and a visible buyer set (importers, distributors, exporters, fintech/POS). Main risks: higher per-record competition (many lead-list vendors and agencies), DNCR/telemarketing enforcement, and the state-backed Tradeling.
- Corridor design: start with one trade (e.g. grocery/FMCG wholesale or auto-parts/repair, or textiles in Deira/Bur Dubai) and one buyer (Pakistani or Indian exporter seeking UAE distributors), selling verified lists with owner-confirmed WhatsApp numbers and delivery of a buyer-approved first message.
- Turkey as a second wedge: Turkish exporters selling into the Gulf are buyers; Turkish merchants are legally reachable for B2B messages (subject to IYS and ETK specifics); lists could be bilingual Turkish/Arabic. Unvalidated: Gulf-side demand from Turkish exporters and local payment/tax setup.
- Saudi Arabia is likely the better second market after the UAE because of scale and Wathq verification, but heavier compliance (PDPL penalties up to SAR 5 million, CST spam rules, MISA licensing) argues for entering after UAE learnings.
- Do not lead with Egypt (new data-protection licensing of electronic marketing in 2025-26), Iraq or Lebanon (informality, payments); these are better as contributor-supply markets later than as buyer markets.

### Gaps and unknowns that most affect the decision
- Measured completeness of Google/OSM/Overture in Deira, Karama, Sharjah, Riyadh and Istanbul districts (single most valuable test).
- Real willingness to pay and price points from 10-20 importer/exporter interviews.
- Whether UAE telemarketing and DNCR rules cover B2B/sole-trader recipients and platform-sent WhatsApp outreach (needs UAE counsel).
- Terms of use of UAE emirate registries and Wathq for verification at scale.
- Contributor payout rails for Pakistan/India/Egypt.
- Whether the UAE PDPL Executive Regulations are in force (sources conflict).
- DIFC/ADGM, Kuwait, Jordan, Iraq, Lebanon legal positions; Qatar/Kuwait/Oman/Bahrain market structure.
