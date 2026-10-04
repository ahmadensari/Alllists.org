# Launch-Market Selection for AllLists.org: Evidence-Based Comparison of 12 Candidate Markets

**Research date:** 2026-10-04. **Method caveat (read first):** WebFetch was blocked by the egress proxy for community.openstreetmap.org, giscienceblog.uni-heidelberg.de, ncbi.nlm.nih.gov, nber.org, arxiv.org, yelp-ir.com and stripe.com. Almost every cited finding below therefore comes from web-search result summaries, not from reading the full page. Treat each as "reported by the search summary of this source". Primary pages (SEC filings, NSE investor presentation, DLA Piper, ICO) were surfaced in search but not opened. Scores in the matrix are my judgement, not published data. Figures not in a source are marked UNVERIFIED. Currencies are given as reported (INR, USD); USD conversions are my approximations and marked "approx".

## 1. Local-business-data quality: where is coverage of small and informal businesses weakest, and where would a contributor-built verified list have the biggest edge?

### Takeaway
No source I could reach publishes a country-by-country POI completeness or freshness index for small and informal businesses across the candidate markets. The evidence is indirect: OSM completeness is highly uneven, the best open studies are from Germany and Canada, and Overture and Foursquare volumes are growing fastest in India and Indonesia. The data-gap edge is probably largest in Nigeria/Kenya, Pakistan, India (informal long tail) and Indonesia, and smallest in the US and UK. That ranking is an inference with low-to-medium confidence, and it needs a direct sampling test (see section 7).

### Cited Findings
- A 2017 PLoS ONE study estimated OSM road completeness for every country and concluded the world's user-generated road map is "more than 80% complete". This is roads, not POIs, so it is a weak proxy for business coverage. — [PMC5552279 (Barrington-Leigh and Millard-Ball, 2017)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5552279/)
- A 2023 study of OSM POI quality for travel-demand models used surveyed ground truth from 49 areas in Germany and found OSM POI completeness depends on the POI category. — [Heidelberg library record, "Quality assessment of OpenStreetMap's points of interest with large-scale real data"](https://heibib.ub.uni-heidelberg.de/search/Record/1896226124)
- An analysis of Canadian OSM POI data found completeness ranged from 7% to 81%, and fast-food/restaurant chains from 33% to 51%. This is from a 2014 mailing-list post, so it is dated and not peer-reviewed. — [OSM-talk, June 2014](https://lists.openstreetmap.org/pipermail/talk/2014-June/069952.html)
- A summary of the OSM-completeness literature says many robust completeness methods cover limited areas, mostly developed countries where ground-truth data exists, and that some areas are complete while others are incomplete or untouched. — [Search summary of the SotM 2020 academic track, building completeness](https://pretalx.com/state-of-the-map-2020-academic-track/talk/YHEMFS)
- Overture Maps held 72M+ places as of January 2026. Foursquare OS Places held 106M+ places as of December 2025. A vendor benchmark (SafeGraph, a commercial competitor, so potentially biased) says free datasets have narrowed the volume gap with paid ones but not commercial-grade completeness, freshness or support. — [SafeGraph vs OSM benchmark (2026)](https://www.safegraph.com/?p=947)
- Foursquare's release notes and docs show it has expanded ingestion of Overture data for France, Germany, Serbia, South Korea, Indonesia, Finland, Chile and Bulgaria, and that India and Indonesia are among the top countries by volume of newly created POIs. Open-data coverage in these two is therefore improving quickly. — [FSQ OS Places release notes](https://docs.foursquare.com/data-products/docs/fsq-os-places-release-notes)
- Overture documentation says data quality varies by region and some categories are sparse. — [Overture Places guide](https://docs.overturemaps.org/guides/places/)
- A "global comparison of restaurants in OpenStreetMap and Overture Places" exists on the OSM community forum and an HeiGIT "OSM completeness with Overture data" analysis exists, but both were blocked, so I have no country-level figures from them. — [OSM community thread](https://community.openstreetmap.org/t/a-global-comparison-of-restaurants-in-openstreetmap-and-overture-places/120475); [HeiGIT](https://heigit.org/?p=33507)
- Google Maps accuracy: a marketing-vendor page claims phone-number accuracy of 85-90%, address 92%+ and website URL 80-85%. It is a vendor claim with no stated method, and it is not country-specific. — [mapsleads.co](https://www.mapsleads.co/blog/google-maps-data-accuracy)
- Fake and falsely "closed" Google listings are documented problems. Google's own blog discusses spammy closed-listing labels. — [Google Maps blog, 2011](https://maps.googleblog.com/2011/09/combatting-spammy-closed-listing-labels.html)
- SME online presence is low in several candidate markets but the data is old. In India only 32% of SMBs used Google's digital tools (maps and search listing) around 2017, and earlier data showed under 5-6% of 51M Indian SMEs had an online presence in 2015. In Indonesia fewer than 10% of small businesses were online per Google Asia Pacific leadership in 2013. — [The Ken, 2017](https://the-ken.com/google-indias-2017-focus/); [PYMNTS, 2015](https://www.pymnts.com/news/2015/google-targets-20-million-indian-smbs-on-the-net-by-2017/); [Jakarta Post, 2013](https://www.thejakartapost.com/news/2013/04/24/more-asian-smes-go-online-expand)
- Business-population scale: India's Udyam and Udyam Assist registrations (the latter built for street vendors and household units without PAN or GST) crossed 7.83 crore (78.3M) by 28 Feb 2026 and 8.7 crore by June 2026. Indonesia had about 66M MSMEs in 2023 (databoks, citing government data). SMEDA estimated about 3.25M MSMEs in Pakistan (undated estimate, probably older; SMEDA's own annual report is cited but not read). — [IBEF](https://www.ibef.org/news/over-7-83-crore-enterprises-registered-on-udyam-platforms-indicating-strong-msme-formalisation-growth); [Databoks](https://databoks.katadata.co.id/en/finance/statistics/670d149c779b0/number-of-indonesian-msmes-2018-2023); [SMEDA/PIDE](https://file.pide.org.pk/uploads/sme-sector-in-pakistan.pdf)
- China: Qichacha (largest company lookup, over 320M companies per its description) and Tianyancha/Aiqicha repackage official register data; the top map brands are Baidu Maps then Gaode (Amap); a listing on Baidu Maps costs about 2,500 yuan per year per business per a marketing-agency blog (unverified vendor claim). — [companydata.com China](https://companydata.com/b2b-data-provider-comparisons/china/); [Nanjing Marketing Group](https://nanjingmarketinggroup.com/blog/how-can-baidu-maps-help-my-business)
- WhatsApp is the main business-customer channel in India and Brazil (about 80% of small businesses use it in both per a vendor stats blog; 96% in Brazil per the same blog, unverified). Informal businesses there may exist on WhatsApp Business rather than on Maps. — [wapikit](https://www.wapikit.com/blog/global-whatsapp-business-statistics-2025)

### Inferences
- Where open datasets are densest (US, UK, Germany, France), a contributor list competes with Google, Overture, Foursquare and commercial vendors (ZoomInfo, Cognism, Infobel) and has a thin edge. Verified phone and WhatsApp numbers for informal shops are the likely edge anywhere, but the edge is largest where businesses are not on Maps at all.
- Candidate ranking for data-gap edge (high to low): Nigeria/Kenya, Pakistan, India and Indonesia, Brazil and Mexico, Gulf (many SMEs are formal and listed, but informal trades and expat-run shops are not), China (not scorable by an outsider), UK/US/Germany/France.
- The caveat for India and Indonesia: Overture and Foursquare volumes are growing fastest there, so the gap is closing, and "present on Maps" does not mean "has a verified, contactable phone". The edge shifts from "existence" to "verified contact, owner name, products, WhatsApp, freshness".
- Buyers value verified, current contact data for the specific trade and locality (hardware suppliers in Lahore, pharmacies in Pune), which is what hierarchical street-to-city lists deliver. Completeness of "all POIs" matters less than completeness within a niche.

### Gaps
- No country-level POI completeness or freshness index for Nigeria, Kenya, Pakistan, India, Indonesia, Brazil, Mexico or the Gulf could be retrieved. The OSM-versus-Overture restaurant comparison and HeiGIT analysis were blocked.
- No academic study found on Google Maps listing staleness by country (only anecdotes and vendor claims).
- SME online-presence statistics are 2013-2017, so the current share of businesses on Google Business Profile is UNVERIFIED for every country.
- No source found for Nigeria SME online presence.

## 2. Willingness and ability to pay: B2B data spend, lead-gen spend, and ARPU of listing and lead products

### Takeaway
Listing and lead products in emerging markets monetise at roughly 2-10 times less per paying customer than Western equivalents, but they are real businesses at scale. Justdial has about 631k paid campaigns at roughly INR 19k per campaign per year (approx US$220), and IndiaMART has 221k paying suppliers at INR 67k annualised (approx US$770). Yelp earns about US$1.39B from advertising, and ZoomInfo US$1.25B from enterprise data subscriptions at a much higher price point. The US and UK are paper winners on willingness to pay; India is the strongest emerging-market proof that SMEs pay for leads.

### Cited Findings
- Justdial FY26 (year to 31 March 2026): operating revenue INR 12,139 million, up 6.3%; 631,530 active paid campaigns at end of Q4 FY26. Average pricing per paid campaign was INR 4,825 in Q1 FY26 (up 2.3% QoQ); the search summary does not state the unit (monthly, quarterly or other). — [Investywise Q4 FY26 results](https://www.investywise.com/just-dial-q4-fy26-financial-results/); [ICICI Direct Q1 FY26 note](https://www.icicidirect.com/mailcontent/idirect_justdial_q1fy26.pdf); [NSE investor presentation, Apr 2026](https://nsearchives.nseindia.com/corporate/chintan_13042026222656_Investor_Presentation.pdf)
- IndiaMART: Q3 FY26 had 221,000 paying suppliers (up 3% YoY, net -1,000 in the quarter) and annualised revenue per paying supplier of INR 67,000 (up 6% YoY); Q3 collections INR 426 crore (up 17%); FY26 consolidated revenue from operations INR 1,569 crore (up 13%), standalone EBITDA INR 520 crore at a 36% margin. — [Angel One, Q3 FY26](https://oga-prod.angelone.in/news/stocks/indiamart-q3-fy26-earnings-results-revenue-grows-13-percent-on-strong-collections-and-cash-position); [AlphaStreet Q2 FY26](https://alphastreet.com/india/india-mart-q2-fy26-earnings-results)
- Yelp FY2025: net revenue US$1.46B (a record). Services advertising revenue was a record US$948M (up 8%) and Restaurants, Retail and Other (RR&O) advertising US$444M (down 6%). Total paying advertising locations fell 3% while average revenue per location reached an annual record (the figure itself was not in the summary). — [Yelp IR press release, 12 Feb 2026](https://www.yelp-ir.com/news/press-releases/news-release-details/2026/Yelp-Delivers-Record-Net-Revenue-in-2025-Accelerating-Investment-in-AI-Transformation/default.aspx); [10-K](https://www.sec.gov/Archives/edgar/data/1345016/000134501626000019/yelp-20251231.htm)
- ZoomInfo FY2025: GAAP revenue US$1,249.5M (up 3%); 1,921 customers with ACV of US$100k or more (up 54), and those customers are over 50% of ACV. Growth has stalled, which is a caution for the pure "contact database" category in the US. — [ZoomInfo/BusinessWire, 9 Feb 2026](https://www.businesswire.com/news/home/20260209677262/en/ZoomInfo-Announces-Fourth-Quarter-and-Full-Year-2025-Financial-Results/)
- Market sizing from research-vendor reports (low reliability): lead-generation software market US$7.16B in 2025 with North America at 38.8% share and Asia-Pacific the fastest-growing region; B2B lead-generation services market US$8.46B in 2025, projected US$15B by 2035 (5.9% CAGR). — [SNS Insider](https://www.snsinsider.com/reports/lead-generation-software-market-10616/segmentation); [WiseGuy Reports](https://www.wiseguyreports.com/reports/b2b-lead-generation-services-market)
- Western SMB software spend (vendor-blog statistics, unverified method): average US$4,830 per employee per year in 2025; small businesses about US$4,700 per employee; average cost per lead about US$198; B2B SaaS CPL US$100-300. — [Stealth Agents](https://stealthagents.com/research/smb-saas-spending-statistics-2026); [Mails.ai](https://blog.mails.ai/posts/average-lead-generation-cost-2025-industry-channel-breakdown); [SaaS Hero](https://www.saashero.net/google-ppc/b2b-lead-gen-cost-2025/)
- Pakistan: millions of SMEs, only a few thousand accept digital payments, and the sector is predominantly cash-based (PYMNTS framing). — [PYMNTS TV](https://tv.pymnts.com/detail/video/6372137421112/with-a-larger-population-than-brazil-pakistan-s-newly-digital-smbs-offer-huge-opportunity)

### Inferences
- Computed from the cited numbers: Justdial FY26 revenue of INR 12,139M divided by 631,530 campaigns gives about INR 19,200 per campaign per year (approx US$220 at about INR 87/USD, an assumed rate). This is a rough "ARPA", not a reported one. It suggests the INR 4,825 figure is a quarterly price, not a monthly one (UNVERIFIED).
- IndiaMART's ARPU is about 3.5 times Justdial's because it sells to B2B manufacturers and traders who value export and wholesale leads. For AllLists, whose buyers are suppliers, distributors and sales teams, the IndiaMART price point (about US$800/year) is the more relevant emerging-market ceiling.
- Lists sold to buyers outside the list's country are not capped by the local SME price. A US/UK/Gulf importer pays Western-level budgets (hundreds to thousands of USD) for verified supplier or distributor lists in Pakistan or India. This decoupling of buyer market from data market is the main structural insight for sequencing.
- ZoomInfo's flat growth and enterprise price point show the Western B2B-data market is mature and dominated by incumbents; a newcomer cannot win on breadth there.

### Gaps
- No reliable B2B data spend per SMB for Indonesia, Brazil, Mexico, Nigeria, Kenya, Gulf, Pakistan or China.
- No Yelp average revenue per advertising location (the 10-K was surfaced but not opened). No ARPU for Sulekha, TradeIndia, Alibaba/1688 (China), Infobel, Dun & Bradstreet or Cognism.
- FX rates are my assumption; verify before use in any pricing model.

## 3. Regulatory burden for selling business contact data and sending outreach

### Takeaway
No market has a clean "business contact data is exempt" rule. The lightest regimes for B2B email are the US (CAN-SPAM, no consent for email, but TCPA for texts and calls) and the UK (corporate subscribers need no consent, but sole traders do). The heaviest are Germany (UWG s.7 requires consent for B2B email) and China (PIPL has no business-contact carve-out, plus cross-border limits). India, Brazil, Indonesia, Mexico, Gulf and Nigeria all now have consent-centred laws that were recently notified or enforced, which makes "message campaigns to businesses" the riskiest product line; selling lists is less risky than sending messages.

### Cited Findings
- **EU/Germany:** GDPR legitimate interest lets providers collect, store and enrich B2B contact data; UWG s.7(2) treats email advertising without prior express consent as "unreasonable harassment" regardless of whether the recipient is a consumer or a business; Germany is described as the strictest EU market for B2B cold email. — [Overloop](https://overloop.com/blog/b2b-cold-email-germany-gdpr-compliance); [Cognism](https://www.cognism.com/blog/data-providers-germany); [Prospeo](https://prospeo.io/s/gdpr-cold-email). These are vendor and law-firm-adjacent blogs; the statute text itself was not read.
- **France:** not specifically researched; no source retrieved (UNVERIFIED).
- **UK:** PECR distinguishes corporate subscribers (companies and LLPs, no prior consent required for marketing email) from individual subscribers (including sole traders and some partnerships, consent or soft opt-in needed). — [ICO B2B marketing guidance](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/business-to-business-marketing/)
- **US:** CAN-SPAM has no B2B exemption and no prior-consent requirement; it requires accurate headers, a physical address, and an opt-out honoured within 10 business days. TCPA applies equally to B2B and B2C calls and texts: autodialed or prerecorded marketing calls and texts to wireless numbers need prior express written consent. — [GDPRLocal](https://gdprlocal.com/?p=774); [Wipfli](https://www.wipfli.com/insights/articles/does-tcpa-apply-to-b2b-marketing-key-rules); [DNC.com](https://www.dnc.com/faq/are-b2b-calls-exempt-tcpa-regulations). State privacy laws were not researched (UNVERIFIED).
- **China:** PIPL has no express carve-out for business contact information, so B2B data that identifies individuals can be caught; separate consent is needed for processing and cross-border transfer; transfer out of China needs a security assessment, certification or standard contract. — [MoFo FAQ](https://www.mofo.com/resources/insights/211025-china-personal-information-protection-law-faqs); [Linklaters](https://www.linklaters.com/en/insights/blogs/digilinks/2023/january/china---at-a-glance-summary-of-the-new-data-transfer-regime)
- **India:** DPDP Act enacted Aug 2023; DPDP Rules notified 14 Nov 2025 with a 12-18 month phased compliance window; marketing consent must be free, specific, informed, unambiguous and as easy to withdraw as to give; the TRAI Do-Not-Call layer applies to calls and SMS on top. DLA Piper's India page covers this. — [KPMG on DPDP Rules 2025](https://assets.kpmg.com/content/dam/kpmgsites/in/pdf/2025/11/dpdp-rules-2025-guidance-to-dpdp-act-implementation.pdf); [Mondaq](https://www.mondaq.com/india/privacy-protection/1742050/indias-digital-personal-data-protection-law-implications-for-global-businesses)
- **Brazil:** LGPD in force, ANPD actively investigating, fines capped at BRL 50M per infraction, no clear B2B/B2C distinction. — [Barbieri Advogados 2026 guide](https://barbieriadvogados.com/en/?p=8824); [Altitude Marketing](https://altitudemarketing.com/blog/lgpd-b2b-marketers/)
- **Indonesia:** PDP Law's two-year transition ended 17 Oct 2024; as of Dec 2024 the data protection authority was not yet established and implementing regulations were pending (current 2026 status not retrieved). — [DLA Piper Indonesia](https://www.dlapiperdataprotection.com/?c=ID&t=law); [Captain Compliance](https://captaincompliance.com/education/indonesia-pdpl/)
- **Mexico:** a new LFPDPPP was approved 20 March 2025 and took effect 21 March 2025, replacing the 2010 law, with broader personal-data definition, stricter privacy notices and higher fines, plus specialised courts. — [Hunton](https://www.hunton.com/privacy-and-cybersecurity-law-blog/mexico-overhauls-federal-data-protection-law); [Greenberg Traurig](https://gtlaw.com/en/insights/2025/3/nueva-ley-general-proteccion-de-datos)
- **UAE:** Federal PDPL (Decree-Law 45/2021) exists but sources conflict on whether Executive Regulations have been issued (several say still pending in 2026; others cite a 2023 cabinet decision), so the status is unclear. TDRA's Mobile Spam Policy (2020) requires opt-in consent for electronic marketing, and cold-calling fines of up to AED 150,000 applied from 27 Aug 2024. — [ConsentStack](https://consentstack.io/regulations/uae-pdpl); [Gulf Business](https://gulfbusiness.com/en/2024/telecoms/cold-callers-uae-dhs150k-fines); [Tamimi](https://turtl.tamimi.com/story/law-update-issue-348-tmt/page/13)
- **Saudi Arabia:** PDPL fully enforceable from 14 Sept 2024 (SDAIA); consent must be obtained before marketing and be withdrawable. — [Clyde & Co](https://www.clydeco.com/en/insights/2024/09/saudi-arabia-s-personal-data-protection-law-become); [Tamimi](https://turtl.tamimi.com/story/law-update-issue-367-saudi-arabia-and-competition/page/11)
- **Nigeria:** NDPA 2023 requires consent for direct marketing; the NDPC issued the GAID on 20 March 2025, effective Sept 2025. — [LawPavilion](https://blog.lawpavilion.com/ndp-act-2023-gaid-2025-a-comprehensive-guide-to-nigerias-new-data-protection-landscape); [KPMG Nigeria](https://assets.kpmg.com/content/dam/kpmg/ng/pdf/2025/05/Review%20of%20the%20NDPA%20General%20Application%20and%20Implementation%20Directive%20(GAID)%202025.pdf)
- **Kenya:** Data Protection Act 2019 exists but I retrieved no source (UNVERIFIED). **Pakistan:** personal-data-protection bill status and PECA/PTA messaging rules were not researched; no source retrieved (UNVERIFIED).

### Inferences
- Regulatory risk differs by product line. Selling lists of publicly available business details (name, address, category, general business phone) is lower risk than selling named individuals' mobile numbers, and sending outreach to those numbers is the highest risk everywhere. A launch that sells lists and lets buyers run their own outreach (with compliance warnings and suppression handling) is much lighter than AllLists sending campaigns itself.
- Contributor payment per verified entry plus verification workflows can double as consent/provenance records, which is a regulatory asset in DPDP, LGPD and PDPL markets (inference).
- Proposed regulatory burden score (5 = light): US 3 (TCPA), UK 3, Pakistan 3 (unverified), Brazil 3, Indonesia 3, Mexico 3, India 2 (new DPDP plus TRAI DND), Gulf 2, Nigeria/Kenya 2, France 2 (unverified), Germany 1, China 1.

### Gaps
- DLA Piper's Data Protection Laws of the World was found via search but its country pages were not opened; statute-level B2B treatment under DPDP, LGPD, PDP, PDPL (UAE/KSA), NDPA, Kenya DPA and Pakistan is therefore unconfirmed.
- US state privacy laws (CCPA/CPRA and others) and how they treat B2B contact data were not researched.
- France (CNIL position on B2B prospecting) not researched.
- No legal advice: a local-counsel review is needed in any chosen market.

## 4. Payments and payouts: collecting from buyers and paying many small contributors

### Takeaway
Collection from buyers is easy in the US/UK/EU and workable in Brazil (Pix), India (UPI, from background knowledge), Nigeria/Kenya (Paystack, M-Pesa), and hard in China and Pakistan. Paying many small contributors is the harder half. Pakistan has no PayPal and an unclear Stripe position; Wise's Pakistan position is restricted; local wallets (Easypaisa, JazzCash) are large. Per-contributor payouts need a local-rail partner in each market.

### Cited Findings
- Stripe's country coverage was not retrievable (stripe.com blocked). A search summary claims Stripe Connect lists India, Indonesia, Nigeria, Kenya and Pakistan, but also that India and Indonesia are "preview" markets and that Nigeria, Kenya, Ghana, South Africa and Cote d'Ivoire run on Paystack (a Stripe company since 2020). The Pakistan claim conflicts with widely-known facts and is UNVERIFIED. — [Search summary of Stripe docs/third-party pages](https://docs.stripe.com/changelog/clover/2026-02-25/cross-border-payouts-new-countries); [StartupOwl](https://startupowl.com/setup/stripe-unsupported-countries)
- Stripe cross-border payouts were listed as US-only in older Stripe docs; a Feb 2026 changelog adds new countries (details not read). — [Stripe changelog](https://docs.stripe.com/changelog/clover/2026-02-25/cross-border-payouts-new-countries)
- Brazil: Pix is projected at 44% of online transaction value in 2025 (above credit cards at 41%) and accounts for 51% of B2B transaction value per a trade-press summary; Stripe added Pix via EBANX on 11 Aug 2025; Mercado Pago handles Pix at 0% fee. — [Olhar Digital](https://olhardigital.com.br/2024/09/10/internet-e-redes-sociais/pix-deve-superar-credito-no-e-commerce-brasileiro-em-2025/); [EBANX press release](https://business.ebanx.com/en/press-room/press-releases/stripe-users-can-now-accept-pix-in-brazil-via-ebanx); [Payments Journal](https://www.paymentsjournal.com/stripe-adds-pix-payments-through-ebanx-integration/)
- Pakistan: retail payment transactions reached 9.1B in FY2024-25 (up 38% YoY) with digital channels at 88% of retail transactions; Easypaisa had 55M+ registered users and 20M monthly actives (Dec 2025); JazzCash 40M+ registered users; Easypaisa received a digital retail bank licence in Jan 2025. — [Business Recorder](https://www.brecorder.com/news/amp/598517); [Digital Pakistan](https://digitalpakistan.pk/?p=1553)
- Pakistan: PayPal is still not officially available; a SIFC initiative lets 10,000 freelancers get paid through a third-party mediator. Wise has stopped giving new Pakistani-address accounts full features; a Wise freelancer-account rollout was announced but details are inconsistent. — [Profit/Pakistan Today fact-check, Jan 2024](https://profit.pakistantoday.com.pk/2024/01/06/fact-check-paypal-is-not-coming-to-pakistan); [TechJuice](https://www.techjuice.pk/is-paypal-really-available-in-pakistan-false-rumors-debunked-heres-what-you-need-to-know/); [Wise Pakistan](https://wise.com/pk/blog/receive-international-payments-in-pakistan)
- Nigeria/Kenya: Flutterwave suits multi-country payouts (about 1% plus fixed fee, instant to T+1); Paystack handles Nigeria payouts at T+1; M-Pesa settles near-instantly to T+1 with a KES 250,000 per-transaction cap; Wise re-enabled NGN payouts for UK customers. — [Kolonell, cross-border vendor payouts](https://kolonell.com/en/blog/cross-border-vendor-payouts-flutterwave-paystack-2026); [Kolonell, M-Pesa limits](https://kolonell.com/en/blog/mpesa-settlement-times-limits-kenya-2026); [Condia, Wise Nigeria](https://thecondia.com/wise-local-payouts-nigeria/)
- India (UPI), Indonesia (QRIS), China (Alipay/WeChat Pay), Mexico (SPEI/OXXO), UAE/KSA (Stripe/Tap/mada): searches did not return reliable pages for these. UNVERIFIED in this session. The following statements come from background knowledge only: UPI is the dominant domestic instant rail in India; QRIS is Indonesia's national QR standard; Alipay/WeChat Pay merchant onboarding for foreign firms normally needs a Chinese entity or a licensed intermediary.

### Inferences
- A two-sided payment design avoids most blockers: collect from buyers in a well-served market (USD/GBP/EUR through Stripe or Paddle-style merchant-of-record) and pay contributors in their own country through a payout aggregator (Wise Platform, Payoneer, Flutterwave, local wallets). This favours "foreign buyer, local contributor" models in Pakistan, Nigeria and Kenya, which is the same decoupling as in section 2.
- India is the easiest emerging market for collecting from SMEs at small ticket sizes, which matters because AllLists wants subscriptions and per-campaign payments from small buyers; Pakistan is the hardest for collecting (low card penetration, no PayPal) but workable for wallets.
- Marketplace money-handling (holding funds, paying out revenue share) may trigger e-money or marketplace-payment licensing; this was not researched. A licensed payout partner is the safer route.

### Gaps
- Stripe, Adyen, Mangopay and PayPal availability tables could not be fetched; per-country Stripe status for Pakistan, India, Indonesia and the Gulf is unconfirmed.
- No verified fee schedules for UPI, QRIS, Alipay, WeChat Pay or Raast.
- Tax withholding and 1099-style reporting for contributor payouts in each country not researched.

## 5. Contributor supply cost: gig earnings, whether per-entry payouts motivate, and where crowd work is already common

### Takeaway
Crowd and micro-task workers in South Asia and Africa earn very little per hour, so a per-entry payout at US$0.05-0.20 can motivate part-time contributors there, and it will not in the US/EU/UK. The supply base is large in India, Pakistan, Nigeria, Kenya and Indonesia, which the World Bank identifies as the main sources of online-gig traffic from lower-income countries. Whether enough contributors would work for a revenue share on unproven lists is untested, and the 50/40/30 share per verified entry is paid only if lists sell.

### Cited Findings
- World Bank-based report: Nigeria, Kenya and South Africa accounted for 80.6% of internet traffic to online gig platforms from Sub-Saharan Africa; around a fifth of visitors to gig platforms are from low and lower-middle-income countries, driven by India, Indonesia, Nigeria, Pakistan, the Philippines and Ukraine. — [BusinessDay](https://businessday.ng/news/article/nigeria-others-account-for-81-gig-economy-online-traffic-world-bank/)
- Research on drivers in India, Indonesia and Kenya found platform work yields higher monthly net earnings than casual low-skill work, with comparable or lower hourly earnings. — [NBER w34680](https://www.nber.org/papers/w34680); [IDinsight](https://www.idinsight.org/publication/wheels-of-work-a-cross-country-look-at-digital-driving-gigs-in-india-indonesia-and-kenya/)
- ADB comparative-wage study on low-skilled platform and nonplatform workers in India; a separate summary says microtask platforms lead to lower wages and more precarious conditions in India. — [ADB](https://www.adb.org/publications/from-platforms-to-paychecks-comparative-insights-into-wages-of-low-skilled-platform-and-nonplatform-workers-in-india)
- An ILO survey of nearly 3,200 workers on five micro-task platforms found the majority make relatively low earnings because of oversupply and weak regulation; a cross-country crowdworker study covers demographics. — [ILO gigwork (via Oxford OII)](https://www.oii.ox.ac.uk/publications/gigwork.pdf); [arXiv 1812.05948](https://arxiv.org/pdf/1812.05948)
- Data-labelling pay: US companies say US$7-15 per hour; Malaysia about US$2.50 per hour; Kenyan labelling workers for an OpenAI vendor were reported to earn under US$2 per hour (TIME report). — [HPCwire/TIME summary](https://www.hpcwire.com/bigdatawire/tag/sama/); [AIPressRoom](https://aipressroom.beehiiv.com/p/millions-of-workers-are-training-ai-models-for-pennies)
- Crowdsourced mapping is established in Indonesia, Nigeria and Kenya: HOT has paid mappers in Indonesia, funded micro-grants and mapathons in Nigeria, and State of the Map was held in Nairobi in 2024; commercial firms also pay OSM mappers (Apple, Facebook, Amazon cited). — [OSM wiki, HOT Awards 2024](https://wiki.openstreetmap.org/wiki/Humanitarian_OSM_Team/Working_groups/Community/Humanitarian_Open_Mapping_Awards_2024); [OSM blog on organised editing](https://blog.openstreetmap.org/2017/09/22/dwg-survey-on-organised-editing/)

### Inferences
- The right comparison for contributors is the opportunity cost of an hour. At typical micro-task rates of roughly US$1-3 per hour in lower-income countries (from the cited ranges), a verified entry that takes 3-5 minutes needs about US$0.10-0.25 expected value to compete. AllLists' revenue-share model delivers that only once lists sell repeatedly, so a small fixed per-entry floor (funded from founder capital or buyer prepayments) is likely needed to recruit the first contributors.
- Supply is cheapest and most plentiful in Pakistan, India, Nigeria, Kenya and Indonesia; moderately priced in Brazil and Mexico; expensive in the Gulf (labour is expat and wages are higher) and unworkable at revenue-share scale in the US, UK, Germany, France.
- Revenue-share is a weak motivator without early sales. The strongest drivers are likely trust in payouts, ease of payout rails (section 4) and local social structures (students, shop-association leaders, mapping communities).

### Gaps
- No data on typical earnings per verified business entry or on contributor churn in any directory crowdsourcing model (Justdial and Sulekha field sales force economics were not found).
- No country-specific average gig or micro-task hourly wage table could be retrieved for all candidate markets; the figures above are examples, not a series.
- No evidence on contributor fraud rates (fake entries), which could dominate cost-to-verify.

## 6. Competition intensity and customer acquisition cost for a new directory or lead product

### Takeaway
Every candidate market has strong incumbents in listings (Google Maps and Business Profile everywhere except China) and, in India and China, strong local players (Justdial, IndiaMART, Qichacha, Baidu/Amap). I found no published CAC for a new directory or lead product in any market. Competition is lightest in Nigeria/Kenya and Pakistan, heaviest in the US and China.

### Cited Findings
- India: Justdial with 631,530 paid campaigns and IndiaMART with 221,000 paying suppliers are scaled incumbents with growing collections (IndiaMART collections +17% in Q3 FY26; Justdial revenue +6.3% in FY26). — [Investywise](https://www.investywise.com/just-dial-q4-fy26-financial-results/); [Angel One](https://oga-prod.angelone.in/news/stocks/indiamart-q3-fy26-earnings-results-revenue-grows-13-percent-on-strong-collections-and-cash-position)
- China: enterprise lookup is dominated by Qichacha, Tianyancha, Aiqicha and Qixinbao; maps by Baidu then Gaode. — [companydata.com](https://companydata.com/b2b-data-provider-comparisons/china/)
- US: Yelp lost 3% of paying locations in 2025 despite record revenue; its RR&O segment ad revenue fell 6%, which shows pressure on generic local-listing products. ZoomInfo grew 3%. — [Yelp IR](https://www.yelp-ir.com/news/press-releases/news-release-details/2026/Yelp-Delivers-Record-Net-Revenue-in-2025-Accelerating-Investment-in-AI-Transformation/default.aspx); [ZoomInfo](https://www.businesswire.com/news/home/20260209677262/en/ZoomInfo-Announces-Fourth-Quarter-and-Full-Year-2025-Financial-Results/)
- Tools that scrape Google Maps for B2B leads already exist (e.g., CariLeads for Indonesia); Callbox and Infobel sell lead and directory services in Indonesia and Brazil. Scraped Maps data is a low-cost substitute for list buyers. — [CariLeads on Product Hunt](https://www.producthunt.com/@carileads); [Callbox Brazil](https://www.callboxinc.com/lead-generation-services-brazil/); [Infobel](https://www.infobelpro.com/html-sitemap)
- Western B2B lead cost benchmarks: roughly US$100-300 per B2B SaaS lead; about US$198 average lead cost (vendor blogs, UNVERIFIED method). — [SaaS Hero](https://www.saashero.net/google-ppc/b2b-lead-gen-cost-2025/); [Mails.ai](https://blog.mails.ai/posts/average-lead-generation-cost-2025-industry-channel-breakdown)
- Germany's Bundeskartellamt opened a case on Google Maps Platform (B7-25/22), indicating regulatory attention to Google's dominance in maps data in the EU. — [Bundeskartellamt](https://bundeskartellamt.de/SharedDocs/Entscheidung/EN/Entscheidungen/Missbrauchsaufsicht/2025/B7-25-22_GMP.pdf)

### Inferences
- Because a contributor-built list sells to a niche buyer, the cheapest acquisition path is the contributor's own network, trade associations and WhatsApp groups. A paid-ads funnel at Western CPLs (US$100-300) would not fit a low-capital founder.
- Competing head-on with Justdial or IndiaMART as a consumer-facing directory is not advisable; selling lists to buyers they do not serve (importers abroad, FMCG distributors, tool vendors) is the open lane.
- Proposed competition score (5 = weak competition): Nigeria/Kenya 4, Pakistan 4, Brazil 3, Indonesia 3, Mexico 3, Gulf 3, India 2, UK 2, Germany 2, France 2, US 1, China 1.

### Gaps
- No CAC data for any directory, lead-gen marketplace or list vendor in any candidate market; CAC remains the largest unmeasured variable.
- No verified competitor mapping for Nigeria, Kenya, Mexico, Gulf and Pakistan directories (e.g., Jumia/BusinessList.ng, Yellow Pages variants).

## 7. Scoring matrix, biggest uncertainties, recommended sequence and low-cost experiments

### Takeaway
On paper the highest-potential markets (US, UK, Germany) rank 2nd-4th only when willingness to pay is weighted heavily, and they lose on data gap, contributor cost and competition. On a balanced weighting India ranks first, Pakistan second, with the US/UK and Brazil/Nigeria-Kenya clustered next. The evidence therefore does not support starting in the US, EU or China. Recommended path: use a Pakistan-plus-India supply base to build lists, and sell first to buyers in India and, in parallel, to foreign buyers (UK/US/Gulf) who want verified South-Asian suppliers. Treat the scores as hypotheses to test, not conclusions.

### Cited Findings
- No new cited findings in this section; it applies the evidence from sections 1-6. The inputs are cited there.

### Inferences
**Criteria and weights (sum 100).** Score 1-5, higher is better for AllLists.

| # | Criterion | Weight | What 5 means | Main evidence (section) |
|---|---|---|---|---|
| 1 | Data-gap / contributor edge | 20 | Small and informal businesses poorly covered; verified lists clearly add value | Sec 1 (indirect, low confidence) |
| 2 | Willingness and ability to pay | 20 | Buyers pay US$ hundreds-thousands/year for lists/leads | Sec 2 (Justdial, IndiaMART, Yelp, ZoomInfo) |
| 3 | Regulatory lightness | 15 | B2B list sales and outreach easy | Sec 3 |
| 4 | Payments and payouts | 15 | Easy to collect and pay many small contributors | Sec 4 |
| 5 | Contributor supply cost | 10 | Plentiful, motivated, cheap contributors | Sec 5 |
| 6 | Competition / CAC (lightness) | 10 | Weak incumbents, cheap acquisition | Sec 6 |
| 7 | Founder feasibility | 10 | Language, culture, ops by non-technical founder with low capital | My judgement (founder-fit assumed: South Asian networks, English, Urdu/Hindi) |

**Scores and weighted totals (out of 100; computed as sum of weight times score divided by 5).**

| Market | Data gap (20) | WTP (20) | Reg (15) | Pay (15) | Supply (10) | Comp (10) | Feasib. (10) | **Total** |
|---|---|---|---|---|---|---|---|---|
| India | 4 | 3 | 2 | 4* | 4 | 2 | 4 | **66** |
| Pakistan | 4 | 1 | 3* | 2 | 5 | 4 | 5 | **63** |
| United States | 2 | 5 | 3 | 5 | 1 | 1 | 3 | **62** |
| United Kingdom | 2 | 4 | 3 | 5 | 1 | 2 | 4 | **62** |
| Brazil | 3 | 3 | 3 | 4 | 3 | 3 | 2 | **61** |
| Nigeria/Kenya | 5 | 1 | 2 | 3 | 4 | 4 | 3 | **61** |
| Indonesia | 4 | 2 | 3 | 3 | 4 | 3 | 2 | **60** |
| Mexico | 3 | 3 | 3 | 3 | 3 | 3 | 2 | **58** |
| Gulf (UAE/KSA) | 3 | 3* | 2 | 4 | 2 | 3 | 3 | **58** |
| France | 2 | 4 | 2* | 4 | 1 | 2 | 2 | **52** |
| Germany | 2 | 4 | 1 | 4 | 1 | 2 | 2 | **49** |
| China | 3 | 3 | 1 | 1 | 2 | 1 | 1 | **38** |

`*` = score rests on background knowledge or unverified evidence (India payments/UPI, Pakistan regulation, Gulf WTP, France regulation). Mexico, Indonesia and Gulf scores have the thinnest evidence base.

**Evidence behind key scores.**
- India WTP 3: Justdial about INR 19k and IndiaMART INR 67k per paying customer per year (sec 2) means real but modest ARPU. Regulation 2: DPDP Rules phase in over 12-18 months from Nov 2025 and TRAI DND applies. Competition 2: two listed incumbents. Supply 4: large gig base, low micro-task wages (sec 5).
- Pakistan WTP 1: cash-based SMEs, few accept digital payments (sec 2). Payments 2: PayPal absent, Wise limited, but wallets are large (sec 4). Supply 5 and Feasibility 5: cheapest labour and founder's existing study (assumption).
- US/UK WTP 5/4: ZoomInfo and Yelp scale (sec 2). Supply 1: contributors cannot be motivated by revenue share at low per-entry values (sec 5). Competition 1/2: ZoomInfo, Yelp, Google, Overture, Foursquare (sec 1, 6).
- Germany regulation 1: UWG s.7(2) bars unsolicited B2B email without consent (sec 3). China 1 across regulation, payments, feasibility: PIPL, local-entity requirements, incumbents (sec 3, 4, 6).
- Nigeria/Kenya data gap 5 but WTP 1: the largest likely coverage gap but I found no evidence of SME spend on lists; payments rely on Paystack/Flutterwave/M-Pesa (sec 4).

**Sensitivity (same scores, different weights).**
- Willingness-to-pay-heavy (WTP 30, data gap 15, reg 10, pay 15, supply 5, comp 10, feas 15): US 69, UK 68, India 66, Brazil 60, Gulf 60, Pakistan 58.
- Data-gap-heavy (data gap 30, WTP 10, reg 10, pay 10, supply 15, comp 10, feas 15): Pakistan 74, Nigeria/Kenya 71, India 70, Indonesia 64, Brazil 59.
- India is first or third in all three weightings; China and Germany are last in all. The US/UK win only if willingness to pay dominates the weighting and the data-gap, supply and competition penalties are discounted.

**Biggest uncertainties (rank by impact).**
1. Whether any buyer segment will pay for a contributor list when Google Maps scraping tools are cheap and open datasets are growing. No demand test exists.
2. Real data-gap size per country: no country-level small-business POI completeness index was retrievable; scores rest on proxies.
3. CAC and sales-cycle for list products: no data found for any market.
4. Contributor motivation and fraud under a revenue-share model, with no payout data.
5. Legal treatment of selling named-individual contact data (DPDP, LGPD, PDPL, NDPA, PDP) and of hosting outreach campaigns; DLA Piper pages not read.
6. Payout rails for a foreign marketplace: Stripe/Wise availability by country, and e-money licensing exposure.
7. FX and price assumptions (US$220 and US$770 per year approximate ARPU).

**Recommended sequence (hypothesis).**
1. **Beachhead: India, with Pakistan as a supply and cost lab.** India has the best balanced score, a proven SME lead market (Justdial, IndiaMART), the largest informal business population (8.7 crore Udyam/Udyam Assist registrations), cheap contributors, UPI collection and an English-friendly business culture. Start with one trade and a handful of cities where verified contact data has clear buyer demand (for example, wholesale or industrial supply in a few clusters), not a general directory. Pakistan stays in play because it is already studied, has the cheapest supply and the least competition, but its local willingness to pay and payments are weak, so use it for building lists to sell to buyers elsewhere, including India-based and diaspora buyers.
2. **Second market: UK (or Gulf) as a buyer market, not a data market.** Sell the India/Pakistan lists to UK and US importers, sourcing agents and distributors, who pay Western budgets, collect through Stripe, and sit in a light-regulation regime for B2B email to limited companies (UK corporate subscribers). The second data market to open after that is Nigeria/Kenya or Indonesia, depending on early results, because they have the largest likely data gap but unproven spend.
3. **Avoid early:** China (PIPL, local-entity payment rails, strong incumbents), Germany and France (consent-based B2B outreach, high contributor cost, strong open and commercial data), the US as a data market (highest competition and contributor cost; fine as a later buyer market), Gulf as a data market (expensive supply; uncertain PDPL; revisit as a buyer market), Mexico and Brazil until language and local legal partners are in place.
4. **Do not begin with paid message campaigns** anywhere; start with list sales and subscriptions where buyers do their own outreach.

**Low-cost experiment 1: India (4-6 weeks, target spend a few hundred US dollars, plus a small fixed contributor floor; figures indicative, not researched).**
- Pick one niche and 2-3 city clusters. Recruit 5-10 contributors through colleges, trade associations and WhatsApp groups. Pay a fixed micro-fee per verified entry (for example INR 5-10, my assumption) so the first week does not depend on sales.
- Build 500-1,000 verified entries with phone check, photo or WhatsApp confirmation, and date-stamp. Measure verification cost per entry, fraud rate, and decay (call-back test after 30 days).
- Compare against Google Maps, Justdial and Overture for the same niche and area: share of businesses missing, wrong phones, closed shops. This yields the first data-gap measurement.
- Pre-sell: offer 20-30 targeted buyers (distributors, tool vendors, B2B sales teams) a sample and a paid list at INR 2,000-10,000 (my assumption, bracketed by Justdial and IndiaMART ARPU). Success criterion: at least 3-5 paid orders or signed pre-orders, and verified-entry cost under 30% of list price.

**Low-cost experiment 2: UK/US buyer pilot using the Pakistan/India lists (4 weeks, near-zero cost).**
- Take the same lists (or a Pakistan equivalent for a niche such as textiles, surgical goods, sports goods or rice exporters) and approach 30-50 UK/US importers or sourcing agents through LinkedIn and trade directories, in a manner compliant with PECR (corporate subscribers) and CAN-SPAM; no automated texts or calls.
- Charge US$50-200 for a pilot list (my assumption), collect via Stripe or invoice, and pay contributors through Wise or a local wallet. Measure conversion, willingness to pay and which fields buyers value (WhatsApp, owner name, product catalogue).
- Success criterion: at least 3 paying buyers at above US$50, and a payout cycle completed to at least 5 contributors in under 7 days.

**Decision rule.** Move to the next stage only if (a) the data-gap test shows at least 20-30% of the verified businesses are missing or wrong on Google Maps/Justdial (a threshold I propose, not a published standard), and (b) the buyer test converts at least 5-10% of contacted buyers (my assumption). If (a) fails, drop the niche or country; if (b) fails, change the buyer segment before changing the market.

### Gaps
- All thresholds, prices and spend figures in the experiments are my assumptions, not researched benchmarks.
- The matrix inherits all the gaps of sections 1-6; Mexico, Indonesia, Gulf, France and Kenya have the least evidence.
- Founder-fit scoring assumes South Asian language and network advantages; confirm with the founder.
