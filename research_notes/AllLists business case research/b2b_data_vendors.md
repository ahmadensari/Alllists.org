# B2B contact-data and lead-list vendors, data marketplaces, and open map/places datasets (research as of Oct 2026)

Method note: WebSearch returned summarised snippets. Most WebFetch calls were blocked by the egress proxy (sec.gov, businesswire, profit.pakistantoday, syncgtm, leadgenius, tbsnews, ft.lk, docs.overturemaps.org, captaincompliance), so primary documents (10-Ks, vendor pricing pages) were NOT read in full. Figures below come from search-result summaries of the cited pages. Anything labelled "unverified" rests on a single secondary/vendor-blog source. Currency is stated per item; most vendor prices are USD and 2026.

## 1. Scale, revenue, pricing models and retention of the vendors (ZoomInfo, Apollo, D&B, Cognism, Lusha, Seamless.AI, Foursquare, SafeGraph, Overture, marketplaces)

### Takeaway
Incumbent contact-data vendors sell annual subscriptions (per seat plus credits or export quotas) at roughly USD 15k to 60k/year for ZoomInfo-class tools, and USD 0.03 to 1 per record in marketplace-style list sales. Net revenue retention at the largest vendor (ZoomInfo) is below 100% (90% in 2025), meaning the incumbent model is leaky. Places/POI data is licensed at much higher flat annual fees (SafeGraph USD 150k/yr for US-wide) while near-equivalent open datasets are free.

### Cited Findings
- ZoomInfo FY2025 GAAP revenue was USD 1,249.5 million, up 3% year on year; net revenue retention was 90% at 31 Dec 2025 versus 87% at 31 Dec 2024; customers with at least USD 100k ACV numbered 1,921 (1,867 in 2024, 1,820 in 2023) and made up over 50% of total ACV — [ZoomInfo FY2025 results (search summary of BusinessWire/10-K)](https://www.businesswire.com/news/home/20260209677262/en); 10-K at [SEC EDGAR](https://www.sec.gov/Archives/edgar/data/1794515/000179451526000012/zi-20251231.htm) (not opened directly)
- ZoomInfo does not publish prices; reseller estimates put the entry "Professional" plan near USD 14,995/year, sold via sales rep, annual billing, 3-seat minimum; extra seats roughly USD 3,000 to 8,000/year — [Cognism/ZoomInfo pricing roundup via search](https://cognism.com/zoominfo-pricing); [Reply.io](https://reply.io/blog/zoominfo-pricing/) (competitor/reseller blogs, treat as estimates)
- Vendr (contract-indexing platform) reports a median ZoomInfo contract of about USD 33,500/year across 1,569 verified purchases; typical range USD 15k to 40k, with many teams reaching USD 30k to 60k after adding seats, credits and features — as summarised in search results citing [hackceleration](https://hackceleration.com/labs/zoominfo-pricing) and [Salesmotion](https://salesmotion.io/blog/zoominfo-pricing) (secondary; Vendr page itself not opened)
- Apollo.io 2026 list prices (annual billing, USD per user per month): Free 0 (100 credits/month); Basic 49 (900 credits/user/year); Professional 79 (12,000 credits/user/year); Organization 119. Monthly billing adds about 20% (59/99/149). Credits expire monthly with no rollover; phone reveals and mobile credits are metered separately — [Zeliq](https://www.zeliq.com/blog/apolloio-pricing), [Docket](https://docket.io/resources/research/apollo-pricing), [Bitscale](https://bitscale.ai/blogs/apollo-pricing-a-full-breakdown-of-plans-credits-hidden-costs-2026) (third-party summaries of Apollo's pricing page; not read at apollo.io)
- Seamless.AI: basic package about USD 147/month billed annually with 250 monthly credits per user; G2 reviewers report USD 79 to 299 per user per month on annual contracts; credits are consumed even on failed lookups — [Docket](https://docket.io/resources/research/seamlessai-pricing), [Cognism blog on Seamless pricing](https://www.cognism.com/blog/seamless-ai-pricing) (note Cognism is a competitor)
- Cognism: custom pricing starting around USD 22k+/year; a credit covers a contact record — [Overloop](https://overloop.com/blog/cognism-pricing) (secondary)
- Lusha: Starter plan USD 37.45/month billed annually for 4,800 credits/year; Lusha pricing range stated as Free to about USD 399.90/month in a comparison — [Costbench](https://www.costbench.com/compare/lusha-vs-cognism/), [search roundup](https://www.datanyze.com/blog/lusha-competitors)
- Dun & Bradstreet: taken private by Clearlake Capital in a deal closed around Sept 2025, enterprise value USD 7.7 billion, equity value USD 4.1 billion; 2024 revenue USD 2.38 billion; database of over 500 million business records keyed by D-U-N-S Number — [PE Professional](https://peprofessional.com/2025/09/clearlake-closes-take-private-dun-bradstreet/), [Bloomberg Law](https://news.bloomberglaw.com/bankruptcy-law/clearlake-agrees-deal-to-buy-dun-bradstreet-for-4-1-billion), [Wikipedia](https://en.wikipedia.org/wiki/Dun_%26_Bradstreet) (D&B 10-Qs on EDGAR exist but were not opened)
- Datarade-listed list/record pricing examples (GBP/USD as listed): Metric Central US business contact database from GBP 0.50 per record; worldwide from GBP 1 per record (5% Datarade discount); Leads XL from USD 0.05 per record; a "targeted B2B marketing data" listing from USD 100 per 5,000 records (about USD 0.02/record); Datyle LinkedIn-derived dataset from USD 0.03 per API call — [Metric Central US](https://datarade.ai/data-products/us-business-contact-database-list-metric-central), [Metric Central worldwide](https://datarade.ai/data-products/worldwide-business-contact-database-list-metric-central), [Leads XL](https://datarade.ai/data-providers/leads-xl), [telemarketing listing](https://datarade.ai/data-products/targeted-b2b-marketing-data-for-telemarketing-and-email-marke-b2b-email-databases), [Datyle](https://www.datarade.ai/data-products/linkedin-dataset-worldwide-b2b-contacts-with-email-datyle)
- SafeGraph Places (all US) on AWS Data Exchange: USD 150,000 for a 12-month contract, bound by SafeGraph's EULA, access expires if not renewed — [AWS Marketplace listing](https://aws.amazon.com/marketplace/pp/prodview-q7xzrn4dwruym), [SafeGraph docs](https://docs.safegraph.com/docs/accessing-safegraph-data-in-the-aws-data-exchange)
- Foursquare Open Source Places (FSQ OS Places): about 104.5 million places, 22 core attributes, Parquet on S3 (about 10.6 GB), updated monthly, Apache 2.0, commercial use allowed; GA announced Nov 2024; another source cites 106M+ places in Dec 2025 — [OSM community thread](https://community.openstreetmap.org/t/foursquare-releases-100m-poi-dataset-under-apache-2-0/121883), [ClickHouse docs](https://clickhouse.com/docs/getting-started/example-datasets/foursquare-places), [Simon Willison](https://feeds.simonwillison.net/2024/Nov/20/foursquare-open-source-places)
- Overture Maps Places: about 64M+ (earlier) to 72M+ places (Jan 2026) depending on release; licensed CDLA Permissive 2.0; a Google Earth Engine listing says 100M+ records (conflicting counts, release-dependent) — [Google Earth Engine catalog](https://developers.google.com/earth-engine/datasets/publisher/overture-maps), [Overture STAC](https://stac.overturemaps.org/2026-05-20.0/places/place/collection.json), [OSM community comparison](https://community.openstreetmap.org/t/a-global-comparison-of-restaurants-in-openstreetmap-and-overture-places/120475)
- Marketplaces (Snowflake Marketplace, AWS Data Exchange, Datarade): AWS Data Exchange is a distribution channel where providers set contract prices (example above); Datarade is a listing/brokerage layer where providers quote per-record or per-API-call prices. I found NO verified marketplace take-rate, Snowflake Marketplace pricing, or Datarade revenue figures.

### Inferences
- ZoomInfo NRR of 87% to 90% (below 100%) with only 3% growth suggests the seat-plus-credit subscription model for contact data faces saturation and churn pressure; a new entrant should not assume expansion revenue.
- Per-record list prices span about USD 0.02 to about USD 1.3 (GBP 1), a 50x range; low-end marketplace sellers are commodity scraped lists, high-end is verified/mobile-validated data.
- The SafeGraph USD 150k/yr US-wide licence versus free FSQ/Overture POI data shows the paid premium is for curation, freshness and support, not raw coverage.

### Gaps
- Revenue/scale for Apollo.io, Cognism, Lusha, Seamless.AI, SafeGraph and Foursquare commercial: not found in sources I could open (private companies; no verified filings).
- ZoomInfo gross margin / D&B 2025 revenue and margins: 10-K/10-Q on SEC EDGAR could not be fetched, so not extracted. ZoomInfo is widely known to have high gross margins but I have no cited number.
- Customer retention/churn for Apollo, Cognism, Lusha, Seamless.AI: not found.
- Snowflake Marketplace and AWS Data Exchange fee structures and Datarade commission: not found.
- Primary vendor pricing pages (apollo.io/pricing, lusha.com/pricing, cognism.com) were not read directly.

## 2. How vendors acquire and verify data; accuracy decay; compliance (GDPR, CCPA, opt-out, lawsuits, fines)

### Takeaway
Vendors combine web crawling, third-party partnerships, user-contributed address-book/email-signature data ("community" networks), and automated plus human verification. Accuracy for emerging-market data is weak, and regulators and plaintiffs are increasingly targeting scraped/contributory models (Lusha EUR 2m fine in Italy, Cognism class action settlement, ZoomInfo CCPA suit).

### Cited Findings
- ZoomInfo data comes from web crawling (machine-learning scan of public information across more than 28 million domains daily: corporate sites, press releases, news, SEC filings, job postings), data partnerships, and user contributions through its free Community Edition, where users contribute contact data and email-signature data (browser extension/integration parses signatures from messages) in exchange for free credits — [Phantombuster explainer](https://phantombuster.com/blog/lead-enrichment/how-does-zoominfo-get-their-data/), [ZoomInfo Atlas data sources](https://atlas.zoominfo.com/data-sources) (search summaries; ZoomInfo states it does not read message bodies)
- ZoomInfo operates a privacy portal (zoominfo.com/privacy-center) for opt-out/removal requests, verification by work email, removal "typically a few business days"; it states CCPA and GDPR compliance — [Datalane](https://www.datalane.com/post/is-zoominfo-legit), [UpLead](https://www.uplead.com/?p=32134) (secondary)
- ZoomInfo was sued by a former partner for alleged CCPA violations — [IAPP](https://iapp.org/news/a/zoominfo-sued-by-former-partner-for-alleged-ccpa-violations/) (details/outcome not read); a LeadGenius post discusses a recent ZoomInfo court ruling — [LeadGenius](https://leadgenius.com/resources/zoominfo-most-recent-court-ruling) (not read; competitor commentary)
- Italy's data protection authority (Garante) fined Lusha Systems EUR 2 million and imposed a processing ban; decision formalised mid-July 2026, announced 27 July 2026; Lusha assembled profiles from data scraped from social networks combined with data bought from other brokers — [Captain Compliance](https://captaincompliance.com/education/italian-garante-hits-us-data-broker-lusha-with-e2-million-fine-and-processing-ban/) (single secondary source via search summary; unverified against Garante's own release)
- Cognism agreed to settle a US class action alleging it displayed contact data to free-trial users; payouts modest (USD 22.50 for a California resident, USD 150 for Alabama); commentary says similar troubles hit ZoomInfo, Apollo and Seamless, and that Apollo and Seamless LinkedIn pages were removed in 2024 over scraping practices — [LeadGenius on Cognism](https://www.leadgenius.com/resources/cognism-class-actions-and-the-shaky-future-of-b2b-data) (LeadGenius is a competitor; claims about LinkedIn page removal unverified)
- Cognism "Diamond Data": mobile numbers a human has phone-verified within the last 90 days; one test of 50 such numbers found a 71% connect rate — [Docket](https://docket.io/resources/research/cognism-alternatives) (secondary/test of limited sample)
- Seamless.AI real-world accuracy per reviewers: email about 70 to 85%, phone about 50 to 70% — [Enrich.so](https://www.enrich.so/blog/seamless-ai-review), [Prospeo](https://prospeo.io/s/seamlessai-reviews) (competitor-run review sites; unverified)

### Inferences
- A product built from publicly visible business listings (shop name, address, category, phone as published) is less exposed than person-level contact data, but business phone numbers of sole proprietors in Pakistan could still be personal data; Pakistan's own data protection law status was not researched here.
- The "verified in last 90 days by phone" tier suggests accuracy decay is managed by re-verification cycles of roughly quarterly frequency at premium vendors; commodity vendors do not document it.

### Gaps
- Vendor-published decay rates (e.g., annual % of B2B data going stale) with a primary source: not found.
- CCPA enforcement actions or GDPR fines against Apollo, ZoomInfo and Seamless.AI: not found as verified items (only references to lawsuits and commentary).
- Outcome, amount and court of the ZoomInfo CCPA suit: not read.
- Apollo's contributory network details (primary source): not found.
- Pakistan data-protection law (PDPA bill) status: not researched.

## 3. Open datasets: OpenStreetMap, Overture Maps, Foursquare OS Places, Wikidata, GeoNames; Pakistan coverage and licence meaning for a commercial resale product

### Takeaway
Overture Places (CDLA-Permissive-2.0) and FSQ OS Places (Apache 2.0) can be freely resold or embedded with minimal obligations; OSM's ODbL imposes attribution plus share-alike on derivative databases, which is the licence to avoid mixing into a proprietary resale list. I could not find any Pakistan-specific coverage statistics for any of them.

### Cited Findings
- OSM (ODbL): commercial use is allowed; attribution to OpenStreetMap required; if you combine OSM data with your own data into a "derivative database", that database must be made available under the same terms to recipients of the database or of Produced Works created from it; there is no requirement to publish it publicly, only to make it available to recipients — [OSMF Licence and Legal FAQ](https://osmfoundation.org/wiki/Licence_and_Legal_FAQ), [OSM wiki Legal Structure](https://wiki.openstreetmap.org/wiki/Open_Data_License/Legal_Structure), [CASRAI ODbL entry](https://www.casrai.org/dictionary/term/open-database-license-odbl)
- ODbL is enforced via copyright, database right and contract, and credit is given to OSM as the database — [OSM talk list on attribution](https://lists.openstreetmap.org/pipermail/talk/2019-September/083269.html)
- Overture Places licence: CDLA Permissive v2.0; component sources include AllThePlaces (CC0-1.0), Foursquare (Apache-2.0), and DAC, Krick, Microsoft, PinMeTo, RenderSEO, Meta (CDLA-Permissive-2.0); source feature counts from about 2.8k to 59.4M as of April 2026 — [Overture Places Guide / release notes](https://docs.overturemaps.org/guides/places), [Overture release page](https://docs.overturemaps.org/release/page/15)
- Overture does not require text attribution or logos on maps/graphics built with its data; it suggests crediting "© Overture Maps Foundation" — [Overture docs via search](https://docs.overturemaps.org/guides/places)
- Overture/OSM relationship: Overture uses OSM for roads/buildings but not POIs; joining CDLA data with OSM may force the result to carry ODbL if it is a derivative database; Overture has said Places can be used as a source for OSM because CDLAv2 is compatible — [OSM community thread](https://community.openstreetmap.org/t/autopopulating-fields-for-new-places-from-overturemaps-data/134376), [OSM POI quality thread](https://community.openstreetmap.org/t/poi-quality-and-usage-any-corporates-contributing/107488)
- Scale: Overture (72M+ places, Jan 2026) and FSQ OS Places (106M+, Dec 2025) — [SafeGraph benchmark post (vendor)](https://www.safegraph.com/?p=947); SafeGraph is a commercial competitor to both, so its quality claims should be treated as marketing.
- Overture POI quality described by an OSM community member as "mediocre" though covering places OSM lacks — [OSM POI quality thread](https://community.openstreetmap.org/t/poi-quality-and-usage-any-corporates-contributing/107488) (opinion)
- Pakistan retail/shopping locations: a commercial location-intelligence page (xmap.ai) counts 653,308+ retail and shopping locations across 19 regions/48 districts, with Punjab 401,927 and Lahore 106,299 — [xmap.ai](https://www.xmap.ai/location-intelligence-reports/retail--shopping-locations-in-pakistan) (source dataset not stated; likely derived from an open or commercial POI set; unverified). Another page cites about 1,200,000 retail outlets in Pakistan (dated July 2026) — [Occupi](https://getoccupi.com/countries/pakistan) (secondary; unverified)

### Inferences
- If open POIs (about 650k tagged retail locations per the xmap figure) are compared to about 1.2M outlets (Occupi figure), open/commercial POI coverage of Pakistani retail may be roughly half the universe, and likely skewed to urban chain/modern-trade shops; small kiryana/general stores are probably the gap. This is an inference from two unverified numbers.
- For a commercial resale list: Overture Places and FSQ OS Places can be ingested and enriched without share-alike; OSM-derived rows should be kept separate (or the ODbL derivative-database obligation accepted). Counsel should confirm.
- Free open POI data sets the practical price ceiling for "generic POI list" products at roughly zero; value must come from verification, phone numbers, owner/contact details, size/category (e.g., FMCG outlet class), and territory structuring.

### Gaps
- Pakistan-specific place counts for OSM, Overture, FSQ, Wikidata and GeoNames: not found. (Could be computed directly by querying the Overture/FSQ Parquet files for country = PK; that would need a dataset query rather than web search.)
- Wikidata and GeoNames licence details (CC0 and CC BY 4.0 respectively, per my general knowledge) were not sourced in this session; unverified here.
- Primary text of the Overture FAQ/licence and the OSMF Licence FAQ were reached only through search summaries, not opened in full.

## 4. Local-list vendors for emerging markets (Pakistan, India, Bangladesh): retailer/shop lists, retail audits, pricing

### Takeaway
Global retail-audit leader Nielsen shut its Pakistan retail measurement service on 30 Sept 2020, and local entrants (SurveyAuto, linked to Dr Umar Saif) and Ipsos moved in; in Bangladesh ex-Nielsen staff formed Insight Metrics. I found no published prices for any retail census/audit or shop-list service in these markets.

### Cited Findings
- Nielsen announced on 30 Sept 2020 it was shutting its Retail Measurement Service in Pakistan, part of global cost-cutting; RMS covered product movement, market share, distribution and price across modern trade and traditional trade (chains, hypermarkets, convenience, independent groceries) — [Profit/Pakistan Today, 1 Oct 2020](https://profit.pakistantoday.com.pk/2020/10/01/nielsen-shutters-retail-intelligence-operations-in-pakistan)
- SurveyAuto positioned as a disruptive-technology alternative after Nielsen's exit; Dr Umar Saif (former PITB chairman) involved; Ipsos Pakistan's managing director said Nielsen was restructuring globally — [Profit, 31 Oct 2020](https://profit.pakistantoday.com.pk/2020/10/31/as-nielsens-dominance-wanes-surveyauto-puts-its-disruptive-tech-to-work/) (article body not opened; details via search summary)
- Bangladesh: former Nielsen employees formed Insight Metrics to continue retail measurement after Nielsen's departure — [TBS News](https://www.tbsnews.net/node/241630) (headline only, not opened)
- Sri Lanka: local competitors took up the mantle after Nielsen's departure (indicates a regional pattern of Nielsen exits) — [Daily FT](https://www.ft.lk/Marketing/Local-competitors-take-up-mantle-following-Nielsen-s-departure/54-715692) (not opened)
- Global B2B databases have thin Pakistan and Bangladesh coverage: "Pakistan and Bangladesh remain coverage gaps for every global provider", with Karachi and Lahore tech sectors underrepresented; India mobile coverage is thin on Lusha, better at Cognism or local vendor EasyLeadz (about USD 30/month for 100 Indian mobile credits) — [SyncGTM South Asia roundup](https://syncgtm.com/blog/best-b2b-database-south-asia), [ModernInbound EasyLeadz vs Lusha](https://moderninbound.com/blog/easyleadz-vs-lusha) (secondary; one blog source)
- A Pakistan-focused FMCG sector document from the State Bank of Pakistan exists on the FMCG sector — [SBP FMCG.pdf](https://www.sbp.org.pk/assets/document/FMCG.pdf) (not opened; no retail outlet counts extracted)

### Inferences
- The Nielsen exit created a gap in trusted outlet-universe data for Pakistani FMCG and distributors; this gap, plus thin global-vendor coverage, supports a local-list product, but the willingness-to-pay cannot be sized from these sources.
- Because I found no published price for audits or shop lists, any price assumption for a Pakistani territory list must be validated by direct quotes (e.g., from SurveyAuto, Ipsos, Kantar, local field-survey firms).

### Gaps
- Prices for retail census/audit services (Nielsen, Kantar, Ipsos, SurveyAuto, Insight Metrics) in Pakistan, India, Bangladesh: not found.
- Retail Cloud type tools (distributor/retailer DMS apps) in Pakistan and any retailer-list sales by them: not found in this session.
- Indian retail-universe vendors (e.g., Bizom, Jumbotail, Udaan-type, Nielsen India outlet universe) and their pricing: not searched.
- Size of Pakistan's retail outlet universe from an authoritative source (census/PBS, Nielsen historic universe figures): only the unverified 1.2M and 653k figures above.

## 5. What buyers actually pay: concrete price points (per contact/record, per seat, per territory)

### Takeaway
Observable buyer price points are: USD 0.02 to about 1.3 per record on marketplaces; USD 49 to 119 per user per month (Apollo) up to USD 15k to 60k/year per team (ZoomInfo); USD 22k+/year (Cognism); and USD 150k/year for a US-wide licensed places dataset (SafeGraph). I found no per-territory price points and nothing specific to Pakistan.

### Cited Findings
- Per record (marketplace): GBP 0.50 US / GBP 1 worldwide (Metric Central), USD 0.05 (Leads XL), about USD 0.02 (USD 100 per 5,000 records), USD 0.03 per API call (Datyle) — see Datarade links in section 1.
- Per seat (subscription): Apollo USD 49/79/119 per user per month annual (Zeliq, Docket); Seamless.AI USD 79 to 299 per user per month reported by G2 reviewers (Docket); Lusha from USD 37.45/month for 4,800 credits/year (Costbench).
- Per team (enterprise): ZoomInfo about USD 15k entry, median about USD 33.5k (Vendr via secondary summaries), extra seats USD 3k to 8k; Cognism USD 22k+ (Overloop).
- Per dataset licence: SafeGraph US Places USD 150,000/12 months (AWS Marketplace listing, link in section 1).
- Free ceiling: FSQ OS Places (Apache 2.0) and Overture Places (CDLA-P 2.0) cost USD 0.

### Inferences
- Implied per-record cost for credit plans: Apollo Basic works out to about USD 49 x 12 / 900 = about USD 0.65 per credit at the stated allocation; Professional about USD 79 x 12 / 12,000 = about USD 0.08 per credit (my arithmetic from the cited list prices; credits are not all equal in value, mobile reveals cost more).
- A territory-list product priced anywhere above the commodity per-record range (USD 0.02 to 0.05) must justify itself with verification (phone-verified, recent) and exclusivity of the data; buyers anchor to the free open POI sets and to cheap marketplace lists.
- For Pakistan, the relevant competitor set is not ZoomInfo/Apollo (poor coverage) but field-survey firms and open POI data.

### Gaps
- Per-territory, per-outlet or per-distributor price points: not found anywhere.
- Any Pakistan-specific price (PKR) for contact or shop lists: not found.
- Enterprise D&B list/data licence price points: not found.
