# AllLists should sell verified lists first

AllLists has a plausible but unproven business case. It is strongest as a narrow, data-only product: one trade, in a few cities where small businesses are poorly covered by existing data. Verified lists would be sold one-off, then refreshed by subscription. The industry it descends from is shrinking, but businesses still pay for visibility and leads. US print Yellow Pages advertising fell from **$14.2B in 2005 to $8.6B in 2011** ([Search Engine Land](https://searchengineland.com/are-yellow-pages-toast-four-years-later-we-review-ad-value-116199/comment-page-1)), yet Justdial earns about **Rs 1,214 crore a year** ([Investywise](https://www.investywise.com/just-dial-q4-fy26-financial-results/)), Yelp **$1.46B** ([Yelp IR](https://www.yelp-ir.com/news/press-releases/news-release-details/2026/Yelp-Delivers-Record-Net-Revenue-in-2025-Accelerating-Investment-in-AI-Transformation/default.aspx)) and ZoomInfo **$1.25B** ([BusinessWire](https://www.businesswire.com/news/home/20260209677262/en)). The central problem is price. Bulk business records sell for cents (about $0.02 to $1.30 each on marketplaces, with US vendors near $0.05 to $0.075), while intent-qualified leads sell for tens of dollars. A 50%, 40% or 30% contributor share of a few cents pays a fraction of a cent per sale, so a pure revenue-share model cannot recruit contributors in rich countries and is thin even in poor ones. The evidence therefore does not support starting in the US, EU or China as a data market. Those are better treated as buyer markets: they have the money, but contributors cost $18 an hour or more, free open datasets already cover chains and big cities, and the legal and licensing barriers are highest. The recommendation is to build supply in South Asia, where contributors cost roughly $1 to $3 an hour, and to sell to buyers who pay more, including exporters, importers and sales teams abroad. Launch full-list sales first, then subscriptions. Defer paid message campaigns, which carry the heaviest legal exposure, until the data product has paying customers. Nearly every figure here comes from search-result summaries of primary documents that could not be opened, there is no customer-acquisition-cost data for any directory, and no one has yet tested whether anybody will pay for a contributor-built list. Spend a few hundred dollars and six weeks on experiments before building more software.

## The recommendation on one page

| Decision | Recommendation | Confidence | Main reason |
|---|---|---|---|
| Where to start | Build the lists in Pakistan (and India only if the legal entity and payments allow it). Sell to buyers there and abroad (UK, US, Gulf). | Medium-low | Cheapest contributors, thinnest data, lightest competition. Selling locally is weak because willingness to pay is low. |
| Where not to start | China, Germany, then France and the US as data markets. | Medium-high on China and Germany, medium on the US | China requires a licensed local operator. Germany bans B2B cold email without consent. The US has the highest contributor cost, the strongest incumbents and the most legal risk. |
| Who pays | Business buyers: distributors, exporters, importers, sales teams. Listed shops are not the main customer. | Medium | Directories that depended on listed businesses paying for ads shrank. Micro-businesses have thin budgets. |
| First product | One niche's verified list (one-time sale with a free sample), then a subscription for fresh updates. | Medium | Highest price per entry, no messaging law exposure, simplest to build. |
| Contributor pay | A small fixed fee per verified entry plus revenue share. Do not rely on revenue share alone. | Medium-high | Revenue share on cent-level prices cannot motivate people to start. |
| Defer | Paid message campaigns, ads, shop-promotion upsells, automated payouts. | High | Highest legal risk, unproven demand, hardest to build. |
| Legal posture | Business data only (shop name, address, category, main phone). Named-owner data comes later and only after counsel advises. No scraping of Google or Yelp. | High | Regulators fine data brokers that compile personal data, and Google's terms bar bulk extraction. |
| Technology | Small custom Python and PostgreSQL app with open-source parts. Do not adopt a directory or marketplace platform. | Medium-high | No existing platform models a hierarchy with per-entry revenue shares. |
| Claude tooling | Start with read-only reviewer agents and Anthropic's own plugins. Add database, deployment and payment tools last. | Medium-high | Least privilege. Everything in the stack can be installed in stages. |
| Next 30 days | Rotate the secrets committed to the repo, run the desk checks and two small pilots (section 7). | High | Cheap tests can kill the idea before major spending. |

One urgent housekeeping item sits outside the business case. The repository README states that `app.yaml` and `backend/config.py` contain committed secrets, and `app.yaml` visibly holds a database URL with a password and an application secret key. Rotate them now and remove them from git history.

## How much to trust the numbers

No figure in this report has been checked by us against a filing, statute or vendor price page. The research team's web-fetch tool was blocked for nearly every primary domain (SEC, NSE, BusinessWire, law-firm sites, regulator sites), so almost every figure comes from a search-result summary that quotes a primary document. The exceptions are GitHub repository statistics and a few licence files, which the researchers read directly through the GitHub tool on 4 October 2026, and queries of the official MCP registry API. Status tags in the tables mean the following.

| Tag | Meaning |
|---|---|
| R | Reported: a search summary quotes a company filing, press release, regulator or statute. Primary not opened. Re-check before publishing. |
| S | Secondary: vendor blogs (including competitors), aggregators, consumer sites or single-source articles. Treat as indicative. |
| P | Primary-read: GitHub API data, LICENSE files or MCP registry data read directly (tooling section only). |
| I | Inference: arithmetic or judgement by the research notes or by this report, with inputs stated. Not a fact about the world. |

Where the notes disagree with each other or with the project's own README, the conflict is shown below rather than quietly resolved.

| Topic | Conflict | How this report treats it |
|---|---|---|
| Contributor share "50% → 40% → 30%" | The research notes read it as a share that falls as lists merge upward (street, city, country). The project README says it steps down by date phase and is locked per entry at creation, with 30% as the mature rate. | Both readings are used. The mature 30% appears in both. Confirm the intended rule (open questions). |
| Thryv SaaS share of revenue | Company wording says "over 62%". The notes' division ($461.0M / $785.0M) gives 58.7%. | Use 59% as a computed figure and note the discrepancy. |
| Thryv client counts | 230,000 total clients versus 100,000 SaaS plus 171,000 Marketing Services (sums to 271,000). | Not used. |
| Sensis sale price | About A$260M ([CMO](https://www.cmo.com.au/article/686617/sensis-australia-yellow-pages-sold-us-software-company-260m)) versus a A$250M headline ([Business News Australia](https://www.businessnewsaus.com.au/articles/us-software-company-buys-sensis-from-telstra-for--250m.html)). | "About A$250-260M". |
| Justdial "Rs 4,825 per paid campaign" | The unit (monthly, quarterly) is undefined in the sources. Dividing revenue by campaigns gives about Rs 19,200 a year. | Use the computed Rs 19,200 and label it I. |
| Pakistan retail outlets | About 0.65 million (location-data vendor), about 0.8 million (a startup's target market), about 1.2 million (an academic paper of unknown date). No official census figure. | Use 0.65 to 1.2 million as a range. |
| Open POI dataset sizes | Overture Places is reported at 64M+, 72M+ and 100M+ depending on release. Foursquare OS Places at 104.5M and 106M+. | Use "roughly 70M+" and "roughly 105M". |
| Dun & Bradstreet take-private | One note says it closed around September 2025, another says August 2025. | Say "2025". |
| EU digital ad spend 2024 | EUR 118.9bn versus EUR 84.2bn from the same IAB report family. | Not used for sizing. |
| Stripe in Pakistan | Sources conflict. Most say Pakistan-registered businesses are not supported. One summary lists it. Stripe's own page was blocked. | Treat as not supported until verified. |
| Gumroad minimum payout | A rise from $10 to $100 in March 2026 is reported, but one source says verified accounts stay at $10. | Cited only as an example of payout-floor changes. |
| Pakistan mobile users | 194 million cellular connections (DataReportal) versus 205.5 to 225.75 million (PTA-based press). | Use the lower figure and note multiple SIMs per person. |

## Directories shrank, but businesses still pay for visibility and leads

### Legacy yellow pages died of leverage and a single medium

The legacy industry is a case study in how not to be dependent. It was a sales organisation with a publishing asset. At its AT&T-era peak, a national sales force of nearly **5,000** sold listings in **1,250** directory titles ([Hacienda Business Park](https://hacienda.org/ho-network/ho-nw-2007-08-att-welcomes-yellow-pages)). Advertisers paid for space per book per heading, and a large field force renewed them each year. When search moved online, the firms' debt, sized to peak print cash flow, turned decline into insolvency. Dex Media's Chapter 11 eliminated about **$1.8B** of debt ([MarketScreener](https://www.marketscreener.com/quote/stock/THRYV-HOLDINGS-INC-111065703/news/Dex-Media-Inc-Emerged-from-Bankruptcy-35386994/)). Yell's parent entered administration in November 2013 after a £2.3bn Spanish acquisition ([Management Today](https://www.managementtoday.co.uk/big-yellow-book-closes-hibu-handed-creditors/article/1193051)). Canada's Yellow Pages Group restructured about C$1.5B of debt in 2012 (a search summary of Globe and Mail and Stockchase coverage, so unverified).

| Business | Latest reported figure | What it shows | Status |
|---|---|---|---|
| Thryv (US, ex-Dex) | FY2025 revenue **$785.0M** (-4.7%), SaaS **$461.0M** (+34.2%); monthly revenue per client $356 for SaaS versus $108 for legacy marketing services ([10-K](https://www.sec.gov/Archives/edgar/data/1556739/000155673926000013/thry-20251231.htm)). Agreed in September 2026 to sell its print directories for **$142M** ([Globe and Mail](https://www.theglobeandmail.com/investing/markets/stocks/THRY-Q/pressreleases/4609948/thryv-sells-print-directories-to-accelerate-saas-transition/)). | The survivor sells a software bundle to the same small-business base. SaaS growth slowed to +5% in Q1 2026 ([Thryv](https://investor.thryv.com/news/news-details/2026/Thryv-Grows-SaaS-Revenue-in-First-Quarter-2026-Exceeds-Total-Company-Revenue-and-EBITDA-Guidance/default.aspx)), partly because the Keap acquisition is now in the base. | R |
| Yellow Pages Ltd (Canada) | FY2025 revenue **C$198.9M** (-7.4%), net income C$18.1M; 2018 sales were C$818M ([release](https://www.newswire.ca/news-releases/yellow-pages-limited-reports-fourth-quarter-and-full-year-2025-financial-and-operating-results-and-declares-a-cash-dividend-1--801984504.html), [Globe and Mail](https://beta.theglobeandmail.com/globe-investor/investment-ideas/yellow-pages-left-out-of-high-yield-rally-as-ad-revenue-drops/article34321514/)) | A shrinking but profitable cash-yielding reseller (about 81% digital). Revenue is down about 76% since 2018 (computed). | R, I |
| Solocal / PagesJaunes (France) | FY2024 revenue **EUR 334.5M** (-7%), 1.2 million managed business profiles ([release](https://webdisclosure.com/press-release/solocal-epa-local-2024-financial-results-lF1KoFeMGC8)) | France's largest local-business vendor still earns hundreds of millions selling visibility, but it is shrinking. | R |
| Yell / Hibu (UK) | Ended print in 2019 and became a digital services company ([Localogy](https://www.localogy.com/?p=19710)). No reliable current financials. | Digital transition survived only after a debt reset. | R |
| Jamals (Pakistan) | Founded 1983, printed Karachi directory from 1984, now also CD and web (self-description, [Jamals](https://jamals.com/)). No public financials. | The only legacy Pakistani brand found. Online portals (b2c.com.pk and others) are free to list with paid upgrades. | S |

The practical lessons are three. First, the asset that mattered was the category taxonomy and the customer relationship, not the books. Second, long, auto-renewing advertising contracts with hard-to-measure results generated heavy complaints and churn (anecdotal reviews of DexYP and Hibu). Third, the one working pivot, Thryv's, sold a software workflow (website, reviews, CRM, marketing) rather than a "better directory". A directory is a distribution channel, not the durable product. The research notes also record no source on how legacy firms collected and verified data, so the field methodology is unknown beyond "paid canvassers and renewal calls" (general industry knowledge, unverified).

### Justdial and IndiaMART prove that Indian small businesses pay, at modest prices

Justdial is the best-documented modern Yellow Pages. In FY26 (to March 2026) it reported operating revenue of **Rs 1,213.9 crore** (+6.3%), operating EBITDA of **Rs 357.5 crore** and **631,530 active paid campaigns** ([Investywise](https://www.investywise.com/just-dial-q4-fy26-financial-results/), [Outlook Business](https://www.outlookbusiness.com/corporate/just-dial-q4-results-operating-revenue-hits-307-cr-profit-dips-on-treasury-drag)). Reported net profit is flattered by treasury income: total pre-tax profit (Rs 616.2 crore) is about double operating pre-tax profit (Rs 303.4 crore). Reliance Retail bought 40.95% in 2021 for Rs 3,497 crore ([Reliance](https://www.ril.com/sites/default/files/2023-01/Media-Release-RRVL-16072021.pdf)). Dividing revenue by campaigns gives roughly **Rs 19,200 a year (about US$220 at an assumed Rs 87 per dollar)** per paying business (I). With 48.8 million listings in FY25 ([Business Standard](https://www.business-standard.com/companies/news/just-dial-fy25-net-profit-up-61-to-rs-584-crore-revenue-rises-9-5-125041900159_1.html)), only about 1.3% of listings pay (I, mixed years). The model is a large on-ground sales force (10,472 sales staff in 250+ cities, undated, per a [Trendlyne summary](https://trendlyne.com/research-reports/stock/704/JUSTDIAL/just-dial-ltd/)) selling annual ranking packages. The only documented data-collection method is from 2010, when Justdial paid resellers **Rs 15 per new unique record** plus Rs 5 for a photo and phoned businesses to verify ([Medianama](https://www.medianama.com/2010/07/223-justdials-reseller-program-data-collection-but-more-about-sales/)). That is a useful precedent for a fixed per-record bounty, though it is 16 years old.

IndiaMART is the closer analogue for AllLists' B2B buyers. It had about **221,000 paying suppliers**, each worth about **Rs 67,000 a year (about $770, I)**, in Q3 FY26 ([Angel One](https://oga-prod.angelone.in/news/stocks/indiamart-q3-fy26-earnings-results-revenue-grows-13-percent-on-strong-collections-and-cash-position)). About 2.6% of its storefronts pay (I). Third-party pricing sources put its Maximiser annual plan at Rs 60,000 with leads at **Rs 24 each**, falling to Rs 16 on a three-year plan ([Refrens](https://www.refrens.com/grow/detailed-overview-and-analysis-of-all-indiamart-packages/), S, unverified against the company). Both firms show the same funnel: a huge free base, a 1 to 3% paying tail and a human sales force doing the conversion. Neither discloses customer-acquisition cost.

### Yelp, Angi and Thumbtack show where local-lead money concentrates

Yelp's 2025 revenue of **$1.46B** split into Services advertising of **$948M** (+8%) and Restaurants, Retail and Other advertising of **$444M** (-6%), with paying locations down 3% ([Yelp IR](https://www.yelp-ir.com/news/press-releases/news-release-details/2026/Yelp-Delivers-Record-Net-Revenue-in-2025-Accelerating-Investment-in-AI-Transformation/default.aspx)). Angi's revenue fell 13% to **$1,030.5M** ([10-K](https://www.sec.gov/Archives/edgar/data/1705110/000170511026000011/angi-20251231.htm)). Nextdoor earned $257.6M and still lost $54.2M ([Nextdoor](https://www.businesswire.com/news/home/20260218233855/en/nextdoor-reports-fourth-quarter-and-full-year-2025-results/)). The reading is that listings monetise where one customer is worth hundreds of dollars (home services, professional services) and poorly for small shops and restaurants. Lead prices in the US run at **$10 to $100+ on Thumbtack** ([LeadCapture](https://leadcapture.io/blog/thumbtack-lead-cost/), S) and about **$53 on average for Google Local Services Ads** across 888 contractors ([Enrich Labs](https://www.enrichlabs.ai/blog/local-services-ads-complete-guide-2026), S). Pakistan-specific benchmarks for any of these do not exist in the notes. Google Business Profile is reportedly the leading listing platform in Pakistan at 58.6% share (a low-reliability tracker, S).

### B2B data vendors sell cheap records and expensive subscriptions, and the incumbent is leaking

ZoomInfo's FY2025 revenue was **$1,249.5M** (+3%) with net revenue retention of **90%**, up from 87% ([BusinessWire](https://www.businesswire.com/news/home/20260209677262/en)). Retention below 100% at the market leader means the seat-and-credit model loses customers faster than it expands them. Dun & Bradstreet earned $2.38B in 2024 and was taken private at a $7.7B enterprise value ([PE Professional](https://peprofessional.com/2025/09/clearlake-closes-take-private-dun-bradstreet/)). Pricing falls into clear bands.

| Product | Price | Status |
|---|---|---|
| Marketplace records (Datarade listings) | About $0.02 to GBP 1 (about $1.30) per record, a 50-times range; Leads XL from $0.05 ([Leads XL](https://datarade.ai/data-providers/leads-xl), [Metric Central](https://datarade.ai/data-products/us-business-contact-database-list-metric-central)) | S |
| Data Axle (US) | About $50 to $75 per 1,000 business records, or $0.05 to $0.075 each, per a competitor's blog ([ZoomInfo Pipeline](https://pipeline.zoominfo.com/sales/data-axle-pricing)). Salesgenie subscription from $99 a month. | S |
| Apollo | $49, $79 or $119 per user per month on annual billing, with credit caps ([Zeliq](https://www.zeliq.com/blog/apolloio-pricing)) | S |
| ZoomInfo | Entry about $15,000 a year; median contract about $33,500 ([Hackceleration, citing Vendr](https://hackceleration.com/labs/zoominfo-pricing)) | S |
| Cognism | From about $22,000 a year ([Overloop](https://overloop.com/blog/cognism-pricing)) | S |
| SafeGraph US places | $150,000 for a 12-month licence ([AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-q7xzrn4dwruym)) | R |

Two points matter for AllLists. First, no vendor in the notes sells per-territory or per-street lists, and the research found no per-territory price anywhere, so street-level granularity has no price anchor. Second, **no global vendor covers Pakistan or Bangladesh well** (one blog, [SyncGTM](https://syncgtm.com/blog/best-b2b-database-south-asia), S), and Nielsen closed its Pakistani retail audit in 2020 ([Profit](https://profit.pakistantoday.com.pk/2020/10/01/nielsen-shutters-retail-intelligence-operations-in-pakistan)). That is a real gap, but no price for the field-survey alternatives was found, so willingness to pay cannot be sized.

### Free open datasets cap the price of generic place lists at zero

Overture Places (roughly 70 million places, CDLA-Permissive-2.0 licence) and Foursquare Open Source Places (roughly 105 million, Apache-2.0, monthly updates) are free for commercial use ([Overture](https://docs.overturemaps.org/guides/places), [ClickHouse docs](https://clickhouse.com/docs/getting-started/example-datasets/foursquare-places)). SafeGraph sells a similar US dataset for $150,000, so buyers pay for curation, freshness and support, not coverage. OpenStreetMap is licensed under the ODbL, which forces share-alike on a combined "derivative database" ([OSMF](https://osmfoundation.org/wiki/Licence_and_Legal_FAQ)). AllLists should keep OSM-derived rows separate. A vendor page counts 653,308 retail locations in Pakistan ([xmap.ai](https://www.xmap.ai/location-intelligence-reports/retail--shopping-locations-in-pakistan), S). Compared with a roughly 1.2 million outlet estimate, open and commercial point-of-interest data may cover about half of Pakistani retail, skewed to urban and modern trade (I, from two unverified numbers). The small kiryana shops are the likely gap. Nobody has measured it, and the cheapest first experiment is to query the free Overture and Foursquare files for Pakistan.

### Contributor-built data has precedent, but it was paid in credits, not cash

Jigsaw is the closest precedent. It was a crowdsourced business-contact marketplace with **1.4 million contributors** and 22 million contacts. Contributors earned access to more records by keeping data accurate. Salesforce bought it in 2010 for about **$142M** ([TechCrunch](https://techcrunch.com/2010/04/21/salesforce-buys-jigsaw-for-142m-in-cash-plus-earn-out)), and all Data.com products were deleted by July 2020 ([Traction Complete](https://tractioncomplete.com/?p=1281)). The reason for the shutdown is not established. The pattern across crowd-data programmes is that the biggest crowds are paid in status and perks, not cash. Google Local Guides, Waze, Mapillary and OSM mostly pay in points, badges or hardware (2016-era programme details, [TechCrunch](https://techcrunch.com/?p=1502573)), and only task apps such as Premise and Field Agent pay cash per task, with GPS and photo evidence to control fraud. Fraud is a standing risk: Google removed or blocked about **12 million fake business profiles in 2023** ([CBS News](https://www.cbsnews.com/news/google-maps-fake-listings-lawsuit-scams/)), and Medium suspended about **1.7%** of its revenue-share writers for suspected fraud ([Nieman Lab](https://www.niemanlab.org/reading/medium-suspended-1-7-of-its-rev-share-writer-accounts-over-suspected-fraudulent-activity/)).

Revenue-share rates in creator platforms also put AllLists' plan in context.

| Platform | Platform take | Notes | Status |
|---|---|---|---|
| Gumroad | 10% + $0.50 direct, 30% on its Discover marketplace | Payout floor changes reported | S ([Dodo Payments](https://dodopayments.com/blogs/gumroad-fees-explained)) |
| Patreon | 10% for new creators | | R ([Patreon](https://support.patreon.com/hc/en-us/articles/36426991446797)) |
| Udemy | 3% own link, 75% paid-ads sales, 63% organic marketplace sales | Funds held about 60 to 90 days; $25 minimum | R ([SEC exhibit](https://sec.gov/Archives/edgar/data/1607939/000160793923000181/exhibit991-xinstructorle.htm)) |
| Shopify apps | 0% on the first $1M, then 15% | | R ([Shopify](https://shopify.dev/docs/apps/launch/distribution/revenue-share)) |
| YouTube | 45% on long-form (creators keep 55%) | Gated by audience thresholds | S ([Kapwing](https://www.kapwing.com/resources/monetize-youtube-shorts/)) |
| Quora | Paid people to ask questions, then ended the English programme in 2022 | Bootstrap-then-stop | R ([TechCrunch](https://techcrunch.com/2022/08/18/quora-shutting-down-english-version-partner-program/)) |

Platforms take 10 to 15% where creators bring their own audience and 30% or more where the platform supplies the demand. AllLists' plan leaves the platform 50 to 70%, which matches Udemy's 63% on organic sales where the platform supplies the buyers. That is defensible only if AllLists really supplies the buyers, the verification and the merging. The mature 30% share will look stingy to contributors who see their entries sold. Quora's logic (pay to seed supply, then stop) points toward time-limited bounties instead of permanent revenue share.

## Evidence favours South Asian supply with richer buyers abroad

### The founder's instinct is half right

The wish to start "where the potential is high, even EU, USA or China" is right about money and wrong about fit. The money is real: about **36.2 million US small businesses** ([SBA](https://advocacy.sba.gov/2026/02/03/advocacy-releases-frequently-asked-questions-about-small-businesses-2026/)), **$171B** of US local advertising in 2025 ([BIA](https://bia.com/press-releases/bia-estimates-local-ad-revenue-to-reach-171b-in-2025-core-spending-up-6-1/)), about 26 million EU SMEs ([Statista via Eurostat](https://www.statista.com/statistics/878412/number-of-SMBs-in-europe-by-size)) and about 127 million individual businesses in China ([China Daily HK](https://www.chinadailyhk.com/hk/article/614784)). But a contributor-built list needs cheap, plentiful contributors, thin existing data and permission to sell, and the rich markets fail those tests. In the US a data-entry keyer earns a median **$18.17 an hour** ([BLS](https://www.bls.gov/oes/2023/May/oes439021.htm), vintage uncertain). Crowd workers on MTurk earned a median of about $2 an hour in a 2018 study ([Hara et al.](https://arxiv.org/pdf/1712.05796)). Cents per record cannot compete with the former, though they can with the latter. Growth in the generic-contact-data category is stalling (ZoomInfo +3%) and the free baseline keeps improving.

### Scoring 12 markets: no clear winner, but clear losers

The research notes score 12 markets on seven weighted criteria. The scores are the researcher's judgement, not published data, and the gap between the top eight is smaller than the uncertainty.

| Market | Weighted score (of 100) | Strongest factor | Weakest factor |
|---|---|---|---|
| India | **66** | Proven SME lead market, UPI collection (background knowledge), cheap contributors | Two scaled incumbents, new consent law |
| Pakistan | 63 | Cheapest supply, lightest competition, thin existing data | Low local willingness to pay, weak payment rails |
| United States | 62 | Highest willingness to pay, easy collection | Contributor cost, incumbents, free data |
| United Kingdom | 62 | Buyer budgets, light B2B email rules for companies | Contributor cost |
| Brazil | 61 | Pix payments | Language, local counsel needed |
| Nigeria / Kenya | 61 | Likely largest data gap | No evidence of spend |
| Indonesia | 60 | Large informal base | Thin evidence |
| Mexico, Gulf | 58 | | Thin evidence, expensive labour in the Gulf |
| France | 52 | Permissive B2B email rule | Contributor cost |
| Germany | 49 | Largest EU buyer pool | Consent needed for B2B email |
| China | **38** | Largest business base | Licensing, mapping, payouts, free substitutes |

Changing the weights changes the winner. With willingness to pay weighted heavily, the US scores 69 and the UK 68 against India at 66. With the data gap weighted heavily, Pakistan scores 74 and Nigeria/Kenya 71. India is first or third in all three weightings, and China and Germany are last in all. The defensible conclusion is that there is no decisive winner, China and Germany are poor starting points, and the high-potential rich markets belong on the buyer side.

### Why not the US

The US has the largest budgets but the weakest case for a contributor model. Baseline place data is free (Overture, Google, Yelp), and per-record prices are **$0.05 to $0.075** ([ZoomInfo Pipeline](https://pipeline.zoominfo.com/sales/data-axle-pricing), S). Legal exposure is highest. TCPA class actions roughly doubled in the first half of 2025 (1,052 versus 539, [TCPAWorld](https://tcpaworld.com/2025/07/25/midyear-litigation-report-tcpa-class-actions-up-staggering-95-2-from-2024-previously-the-highest-year-on-record/)). California is the only comprehensive privacy state without a business-contact exemption ([California Lawyers Association](https://calawyers.org/privacy-law/hr-employee-data-b2b-data-to-come-within-scope-of-ccpa-on-january-1-2023/)). Several states require data-broker registration (section 4). The plausible US niches are untested hypotheses: new-business alerts (record 5.67 million applications in 2025, [Census](https://www.census.gov/econ/bfs/pdf/historic/bfs_2025m12.pdf)) and trades suppliers. The US is a buyer market for lists made elsewhere.

### Why not the EU, and where it could work later

The EU has a large buyer pool, with France's Solocal still selling hundreds of millions of euros of local visibility. But minimum wages run from EUR 551 in Bulgaria to EUR 2,704 in Luxembourg, and EUR 2,161 in Germany ([Euronews](https://euronews.com/business/2025/08/08/which-nations-have-the-highest-and-lowest-minimum-wages-across-europe)). Regulators actively fine contact-data compilers. France's regulator (CNIL) fined KASPR EUR 240,000 for collecting LinkedIn contact data ([CNIL](https://www.cnil.fr/en/data-scraping-kaspr-fined-eu240000)), and Italy's regulator reportedly fined Lusha EUR 2 million ([Captain Compliance](https://captaincompliance.com/education/italian-garante-hits-us-data-broker-lusha-with-e2-million-fine-and-processing-ban/), single secondary source). Germany requires prior consent for B2B email. If AllLists ever enters the EU, France is the most promising by the notes' judgement (permissive B2B opt-out rule, one language, a large local market), starting with registry-verifiable trades. That is untested.

### Why not China

The notes find China the poorest starting point, with moderate confidence on regulation and low confidence on market data. Foreign equity in value-added telecom services is capped at 50% under the 2024 negative list ([Rajah & Tann](https://www.rajahtannasia.com/viewpoints/regional-round-up-china-q4-2024-year-in-review-edition/)), and a foreign company cannot hold the commercial ICP licence itself ([China Briefing](https://www.china-briefing.com/news/china-internet-business-licenses-foreign-companies/)). Showing or labelling maps may require a surveying and mapping licence ([Zhonglun](https://en.zhonglun.com/research/articles/54675.html)). The 2026 Cybersecurity Law amendments raise fines to RMB 500,000 and in severe cases RMB 10 million ([Latham](https://www.lw.com/en/insights/Chinas-Cybersecurity-Law-Amendments-Increase-Penalties-Broaden-Extraterritorial-Enforcement)). The competition is formidable and free. Amap offers free certified listings for small shops ([KrASIA](https://amp.kr-asia.com/alibabas-map-app-rolls-out-listings-for-mom-and-pop-shops)), Baidu researchers published automated POI verification from street-view imagery ([arXiv](https://arxiv.org/pdf/2411.18073)), and Meituan lost RMB 23.4bn in 2025 on subsidy competition ([Tiger Brokers](https://www.itiger.com/news/1144025335), S). Paying contributors in China from abroad hits foreign-exchange rules and 20 to 40% withholding on labour income ([MS Advisory](https://msadvisory.com/withholding-tax-in-china/), S). A realistic China path is offshore only: sell Chinese-supplier lists to foreign buyers, or a later partner-led entry.

### India and Pakistan: what they offer and where they fall short

India has the best-proven small-business spending, **7.83 crore** registered micro-enterprises by February 2026 ([IBEF](https://www.ibef.org/news/over-7-83-crore-enterprises-registered-on-udyam-platforms-indicating-strong-msme-formalisation-growth)), and strong incumbents. The notes advise against competing head-on with Justdial or IndiaMART as a consumer directory. The open lane is lists for buyers they do not serve. Pakistan has about 241.5 million people ([Gulf News](https://gulfnews.com/world/asia/pakistan/pakistans-population-soars-to-241-million-1.97390516)), **117 million internet users** at end-2025 and 194 million cellular connections ([DataReportal](https://datareportal.com/reports/digital-2026-pakistan)). However, only 29% used mobile internet in 2024 despite 68% smartphone ownership ([GSMA](https://www.gsma.com/about-us/regions/asia-pacific/wp-content/uploads/2025/07/Unlocking-Pakistan-digital-future-FINAL.pdf)). Shops outside cities are therefore often not online, so field collection is needed, which suits a contributor model. Pakistan's well-funded B2B shop apps largely failed (Jugnu shut core operations in July 2023, [ProPakistani](https://propakistani.pk/2023/07/16/jugnu-shuts-down-its-core-operations-a-year-after-raising-22-5-million/); Jugnu, Retailo and Dastgyr together raised $161.4M, [Profit](https://profit.pakistantoday.com.pk/?p=161891)). They failed on inventory, logistics and field-force costs, and shops kept buying from traditional distributors. An information-only directory avoids that cost but has not yet shown anyone will pay.

| Pakistan factor | Finding | Status |
|---|---|---|
| Retail outlets | 0.65 to 1.2 million; no official census | S |
| Hierarchy | 4 provinces, 37 divisions, about 169 to 173 districts; about 596 tehsils (vendor) | S |
| Local willingness to pay | Cash-based SMEs; only a few thousand accept digital payments | S |
| Collecting money | Stripe and PayPal not available to Pakistan-registered firms; licensed local gateways exist (PayFast, Safepay) ([ProPakistani](https://propakistani.pk/2021/05/25/payfast-becomes-first-pakistani-payment-gateway-to-get-commercial-license-from-sbp/)) | R, S |
| Paying contributors | Easypaisa and JazzCash wallets via aggregators (PKR 50 to 500,000 per transaction, [PayerMax](https://docs.payermax.com/en/202506-version/disbursement/payment-method-list/southeast-asia/pakistan.html)); Payoneer charges 3% on withdrawals ([Profit](https://profit.pakistantoday.com.pk/2025/05/03/payoneer-slaps-3-withdrawal-fee-on-pakistani-users-sparking-backlash-among-freelancers)) | R, S |

### Where this synthesis departs from the notes

The notes recommend India as the beachhead with Pakistan as a supply lab. This report agrees with the scoring logic but flags a question the notes did not research. The repository design (Pakistani administrative divisions, Urdu right-to-left support) suggests a Pakistan-based founder. Whether such a founder can lawfully and practically sell to Indian buyers, pay Indian contributors or hold an Indian entity, and the reverse, was not examined. Do not assume India is open until counsel has answered. The lowest-risk test does not depend on India: build a Pakistani niche list and sell it to buyers in the UK, US or Gulf. The notes' scoring also assumes South Asian language and network advantages that the founder should confirm.

## Cents per record versus dollars per lead decides everything

### The price gap is hundreds to thousands of times

A record is a fact about a business (name, phone, address). A lead is a buyer's expressed intent to purchase. The market prices them very differently.

| Item | Price | Status |
|---|---|---|
| Bulk record, US vendors | $0.05 to $0.075 | S |
| Bulk record, marketplaces | $0.02 to about $1.30 | S |
| Verified-by-phone premium mobile record | Premium tier (Cognism "Diamond Data"); no per-record price found | S |
| Lead, India (IndiaMART plans) | Rs 16 to 24 (about $0.18 to $0.28 at Rs 87 per dollar) | S, I |
| Lead, US (Thumbtack, Angi, Google LSA) | About $10 to $100+; Google average about $53 to $63 | S |

Comparing typical US leads ($25 to $75) with typical records ($0.05 to $0.075) gives a gap of roughly 330 to 1,500 times (I). The research note's own summary says "500 to 1,000 times". The two worlds are separated by intent. A home-service lead might close into a job worth hundreds or thousands of dollars. A bulk record is a fact that a buyer can re-collect. AllLists' business is either cheap bulk lists, with thin per-record revenue to share, or products closer to lead economics.

### What a revenue share pays per sale

The notes assume that verifying one entry takes three to five minutes (an assumption, not measured). The table converts price into contributor pay using the notes' sourced price inputs and my arithmetic.

| Scenario (I) | Gross price per entry sold | Contributor share | Contributor gets per sale |
|---|---|---|---|
| US vendor record price, street-level entry | $0.05 to $0.075 | 50% | $0.025 to $0.0375 |
| Same, mature phase | $0.05 to $0.075 | 30% | $0.015 to $0.0225 |
| Bulk Indian list: Rs 2,000 to 10,000 for 500 to 1,000 entries | Rs 2 to 20 (about $0.02 to $0.23) | 50% | Rs 1 to 10 |

What contributors need depends on where they live.

| Contributor location | Opportunity cost | Pay needed per entry (3 to 5 minutes) | Sales needed at $0.025 per sale (50% of $0.05) | Sales needed at $0.015 (30% of $0.05) |
|---|---|---|---|---|
| Low-income country | About $1 to $3 an hour (MTurk median about $2, Kenyan labelling under $2, [HPCwire](https://www.hpcwire.com/bigdatawire/tag/sama/), S) | About $0.05 to $0.25 | About 2 to 10 | About 3 to 17 |
| United States | $18.17 an hour (BLS) | About $0.91 at 3 minutes | About 36 | About 61 |

For US contributors, earning the median wage needs roughly **24 to 36 sales of each entry** at the 50% share and US record prices (the US note's own figure for $0.05 to $0.075). So per-entry revenue share cannot pay wages in rich countries. In South Asia it can work only if the same entry is sold repeatedly or priced higher. Revenue share is also paid late and only if lists sell, so recruits carry the sales risk. MTurk's closure on 30 September 2026 ([The Next Web](https://thenextweb.com/news/amazon-mechanical-turk-closing-september-2026)) is a reminder that task workers depend on platform stability, and Udemy and Shopify cut or rolled back payout terms. A published payout rulebook with notice periods is a trust asset.

### Micro-payout costs eat small payments

Payment fees compound the problem. Stripe Connect Express in the US is priced at $2 per active account per month plus 0.25% and $0.25 per payout ([Dupple](https://dupple.com/learn/best-marketplace-transactability-platforms-2026), S), so a $2 payout loses over 12% to the fixed fee alone (I). Payoneer takes 3% on Pakistani withdrawals. The remedy is batching, monthly payouts and a minimum balance (the notes suggest a floor around PKR 1,000 to 2,500, their own estimate), as Udemy does with a $25 floor and a 60-to-90-day hold. Holding contributor balances may trigger payment or e-money licensing in Pakistan and the EU. That was not researched and needs counsel.

### What the gap implies for products and for the revenue-share model

First, the model should not be "everything is shared by entry at cent-level prices". It needs a fixed per-entry floor to recruit contributors, funded by buyer pre-payments or founder capital. The notes suggest INR 5 to 10 per verified entry as a starting assumption, not a researched benchmark. Second, entry value must rise above generic-record prices by adding what free data lacks: a verified phone or WhatsApp number, owner name where lawful, a freshness date, a trade category and an exclusive local territory. Cognism's premium tier sells phone-verified mobiles checked in the last 90 days; the free datasets are the price ceiling for anything less. Third, repeat sales matter. The hierarchy can multiply sales of the same entry (street, city, country lists), but only if merged lists do not carry volume discounts that cut the per-entry price, an open question given that merged lists are platform-priced.

Fourth, and most important, the intermediate products map onto the price ladder.

| Product | Price per entry (I) | Legal exposure | Build effort | Recommended order |
|---|---|---|---|---|
| Full list, one-time snapshot | Highest per entry | Low if business data only | Low | **1st** |
| Subscription (live territory and category access, watermarked exports) | Lower recurring | Low to medium | Medium | **2nd** |
| Shop claims and paid promotion | Justdial/IndiaMART model; only about 1 to 3% of listings pay | Low | Medium; needs sales effort | 3rd |
| Paid message campaigns | Closest to lead economics; price unknown for Pakistan | **High** | High | **Last** |

Messaging is the product with the best price per entry and the worst risk. The README's design (messages go only to opted-in shops, buyers never see contact data, frequency caps, one-tap opt-out) is the right way to build it, and the notes' recommendation is to pre-sell lists and subscriptions first. If AllLists later sells message delivery, use the official WhatsApp Business Cloud API, which charges per delivered template (marketing rates range from $0.0109 in Turkey to $0.1597 in the Netherlands; the Pakistan marketing rate was not found, [Meta](https://developers.facebook.com/docs/whatsapp/pricing)), and price campaigns as Meta's rate plus a margin. Anti-fraud basics apply from day one. The README already says self-listed entries and unverified imports earn nothing, which is consistent with how Medium and Google fight fake supply.

### Platform economics are unmeasured

The notes find no customer-acquisition cost for any directory, list vendor or lead marketplace in any market. Western software benchmarks are not a substitute: one vendor-blog figure puts the tolerable acquisition cost for a $99-a-month subscription at about $600 to $1,200 given a 6 to 12 month payback (I, ignoring churn and margin). That is reachable only through referrals, trade associations and contributor-led selling, not paid ads at Western lead prices of $100 to $300. This is the largest unmeasured variable in the business case.

## Messaging is the legal minefield; lists are manageable

The legal picture is consistent across markets. Selling lists of public business details (shop name, address, category, main line) is lower risk than selling named individuals' mobile numbers, and sending messages to those numbers is the highest risk everywhere (notes' inference). This section is research, not legal advice. Every row needs a local lawyer.

| Area | Pakistan | India | US | UK / EU | China |
|---|---|---|---|---|---|
| Messaging | PECA s.25 requires an unsubscribe option for direct marketing, fine Rs 50,000 up to Rs 1M (secondary summary, [Scribd](https://www.scribd.com/presentation/890995014/offences)); PTA bulk-SMS rules ([PTA](https://www.pta.gov.pk/en/media-center/single-media/pta-issues-regulations-for-unsolicited-and-obnoxious-communications)); WhatsApp requires opt-in ([Meta](https://developers.facebook.com/documentation/business-messaging/whatsapp/getting-opt-in)) | DPDP consent rules plus the TRAI do-not-call layer | CAN-SPAM covers B2B email, up to $53,088 per email; TCPA needs written consent for autodialled calls and texts | UK: companies need no prior consent, sole traders do ([ICO](https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/business-to-business-marketing/)); Germany needs consent; France is opt-out ([donneespersonnelles.fr](https://donneespersonnelles.fr/prospection-commerciale-rgpd)); Spain needs consent | Consent required, no promotional sends 19:00 to 08:00, telecom licence |
| Personal data | No data protection law enacted as of May 2026; the bill has stalled since 2018 ([Recordinglaw](https://www.recordinglaw.com/world-laws/world-data-privacy-laws/pakistan-data-privacy-laws/)) | DPDP Rules notified 14 Nov 2025, 12 to 18 month phase-in ([KPMG](https://assets.kpmg.com/content/dam/kpmgsites/in/pdf/2025/11/dpdp-rules-2025-guidance-to-dpdp-act-implementation.pdf)) | CCPA covers business contacts in California; data-broker laws in California, Texas, Oregon and Vermont; California DROP deletion system live for brokers from 1 Aug 2026 ([CPPA](https://privacy.ca.gov/drop-for-data-brokers/)) | GDPR applies to named individuals at businesses; fines up to EUR 20M or 4% of turnover; reselling lists without a consent and notice chain was fined in Italy ([EDPB](https://www.edpb.europa.eu/news/telemarketing-the-italian-sa-imposes-fines-of-3-million-eu-on-an-energy-company-and-eu-850-000_en)) | PIPL has no business-contact carve-out; sole-trader (getihu) phones are personal data; cross-border limits |
| Database rights | Copyright covers only the compilation, not underlying data; no sui generis right found ([Pakistan Law](https://pakistanlaw.com/Copyright_Ordinance_1962.php)) | Not researched | None for facts (Feist, [summary](https://en.wikipedia.org/wiki/Feist_Publications,_Inc._v._Rural_Telephone_Service_Co.)) | EU database right protects makers who invest substantially in verifying data; cumulative extraction of small parts can infringe (Innoweb, [SCL](https://www.scl.org/2984-database-right-innoweb-v-wegener-cjeu-judgment/)); contract can bind users of unprotected databases (Ryanair, [Haerting](https://haerting.de/en/insights/vertragliche-beschraenkung-der-rechte-der-benutzer-einer-datenbank-hier-screen-scraping-von-flugangeboten/)) | Not researched |
| Platform work | Not researched | Not researched | Contributors paid as contractors: 1099-NEC threshold rises to $2,000 for 2026 payments ([NATP](https://www.natptax.com/news-insights/blog/form-1099-filing-changes-under-the-new-2-000-threshold/)) | EU Platform Work Directive transposition deadline 2 Dec 2026; presumption of employment where a platform directs and controls work ([LexisNexis](https://www.lexisnexis.com/en-gb/legal/guidance/the-eu-platform-work-directive)) | Labour income withholding 20 to 40% |
| Tax reporting | 2% sales tax on digital payments collected via banks and gateways (FY2025-26); 5% withholding on creator payments proposed for FY2026-27, final form unverified ([Accountability Lab](https://pakistan.accountabilitylab.org/the-fy-2025-26-budget-and-its-impact-on-pakistans-it-ites-sector/), [Daily Pakistan](https://en.dailypakistan.com.pk/12-Jun-2026/budget-2026-youtube-tiktok-earnings-to-be-taxed-in-pakistan-under-new-proposal)); contributor payout withholding not researched | Not researched | Stripe collects tax IDs at $600 if 1099 is enabled ([Stripe docs](https://docs.stripe.com/connect/required-verification-information-taxes)); 1099-K threshold back to $20,000 and 200 transactions ([CPA Practice Advisor](https://www.cpapracticeadvisor.com/2026/02/18/2026-tax-filing-and-form-1099-k-know-the-new-rules-this-tax-season/178331/)); sales-tax nexus around $100,000 or 200 transactions | EU DAC7 reporting of seller income unless under 30 activities and EUR 2,000 a year ([Belastingdienst](https://www.belastingdienst.nl/wps/wcm/connect/en/business/content/information-for-sellers-dac7)); B2B VAT reverse charge | Fapiao and withholding obligations; local entity likely needed |

### What the regulatory picture implies for design

The tightest constraint is not the law of any single country but the combination of three features: AllLists compiles contact data, sells it to others and pays individuals for providing it. That makes the platform a controller or joint controller of personal data under GDPR-style regimes and a probable data broker in several US states. Contributors who import third-party lists (Kompass, registries with licence terms) expose the platform to database-right claims, so the README's contributor warranty and takedown process are required, not optional. The notes note that EU database rights could protect AllLists' own merged list only if it can show substantial investment, while US law gives no copyright protection to facts, so protection must come from contracts, planted trace records (the README plans watermarking) and access controls. On platform work, contributors who choose what to add, face no quotas and may stop at any time sit at lower risk. A platform-set step-down scale could be argued to be control, so employment counsel should review it per country.

Pakistan is lighter than the EU or US on personal-data law today because no general data protection law has been enacted, but this is a window, not a safe harbour. The bill would create a regulator and fines up to Rs 25 million, and PECA and PTA rules already restrict bulk marketing. The notes found no source on how Pakistani law treats collecting and selling business (non-personal) contact data, and that question needs a Pakistani lawyer first. One more caution on scraping: Meta v. Bright Data found logged-off scraping of public data lawful ([Quinn Emanuel](https://www.quinnemanuel.com/the-firm/news-events/client-alert-what-does-the-meta-v-bright-data-summary-judgment-ruling-mean-for-web-scraping/)), but Google Maps terms reportedly prohibit bulk extraction and lead lists ([ConductAtlas](https://conductatlas.com/platform/google-maps/google-maps-platform-terms-of-service/no-scraping-or-content-extraction/), S). The README's "do not copy from Google Maps" rule is correct.

## A boring open-source stack is enough to start

### What the platform must do

For a non-technical founder, the technical requirements reduce to ten jobs: a place tree from street to world; list import from spreadsheets with column mapping; duplicate detection; verification records for every entry (source, contributor, date, status); a revenue ledger that records who earns what from each sale; payments in and payouts out; public pages that search engines can index; Urdu (right-to-left), Roman Urdu search and English; abuse controls (rate limits, bot checks, audit log); and watermarked, rate-limited exports. The repository holds an early Flask prototype that does not run end to end, according to its README, with a missing database module, no login endpoint and a failing CI workflow. The README's own MVP scope (import a list, geography tree, indexable pages, manual payment, watermarked export, ledger, simple login) is a sensible first slice.

### Recommended components

All repository statistics below were read directly from GitHub on 4 October 2026 (P). "Updated" is not "last commit".

| Job | Pick | Licence | Notes |
|---|---|---|---|
| Web framework | Django ([repo](https://github.com/django/django), 91.3k stars) or keep Flask/FastAPI ([FastAPI](https://github.com/fastapi/fastapi), 102.8k stars) | BSD-3 / MIT | Django's admin gives a non-technical owner a moderation screen almost free (inference). |
| Database | PostgreSQL; `ltree` or a plain adjacency list for the tree; PostGIS later | PostGIS GPL-2.0 extension | A fixed, shallow 8-level hierarchy needs no exotic tree library. |
| Place seed | GeoNames ([about](https://geonames.org/about.html)), CC-BY 4.0 | CC-BY | **Avoid GADM**, which is non-commercial only. |
| Import and validation | Pydantic ([repo](https://github.com/pydantic/pydantic)) and Polars ([repo](https://github.com/pola-rs/polars)) | MIT | Return a per-row error report to the contributor. |
| Deduplication | python-phonenumbers ([repo](https://github.com/daviddrysdale/python-phonenumbers)) and RapidFuzz ([repo](https://github.com/rapidfuzz/RapidFuzz)) | Apache-2.0 / MIT | Normalise phones to E.164; phone is the likely best key (hypothesis). Splink ([repo](https://github.com/moj-analytical-services/splink), MIT) later. |
| Public pages | Next.js ([repo](https://github.com/vercel/next.js), MIT) or Astro ([repo](https://github.com/withastro/astro), licence not verified) | | Server-rendered pages for indexing. Keep thin lists `noindex`, as the README says. |
| Hosting | One VM with Caddy and Coolify ([repo](https://github.com/coollabsio/coolify), Apache-2.0) or Dokku ([repo](https://github.com/dokku/dokku), MIT), nightly backups | | Matches the README's plan to avoid Kubernetes until there is traffic. |
| Abuse controls | ALTCHA ([repo](https://github.com/altcha-org/altcha), MIT), django-axes ([repo](https://github.com/jazzband/django-axes), MIT), and a rate limiter | | The notes list Flask-Limiter, which is Flask-specific; with Django use django-ratelimit (licence unverified). |
| Revenue ledger | A small in-house append-only double-entry table in Postgres, amounts in integer paisa | | Use Blnk ([repo](https://github.com/blnkfinance/blnk), Apache-2.0) as a design reference; defer TigerBeetle. `django-money` is archived. |
| Search | PostgreSQL full-text and `pg_trgm` first; Meilisearch ([repo](https://github.com/meilisearch/meilisearch), MIT) later | | Roman Urdu spelling variants need testing. |

Optional free data seeds are Overture Places (CDLA-Permissive-2.0) and Foursquare OS Places (Apache-2.0). Keep any OSM-derived rows in a separate layer with attribution so AllLists' own contributor data stays a "collective database" and not a share-alike derivative (the notes' reading of ODbL guidance, not legal advice).

### What not to adopt

The WordPress directory plugins (HivePress with 69 GitHub stars, GeoDirectory with 46) are small, GPL-licensed PHP and cannot model a hierarchy with per-entry revenue shares. Saleor and Medusa are product-checkout engines; they are useful as references for payment webhooks and order states but add more complexity than they remove for a list marketplace. Sharetribe Go is described as no longer maintained and source-available. For campaigns, listmonk is AGPL-3.0, so deploy it only as an unmodified separate service. Unofficial WhatsApp libraries such as Baileys (11.2k stars) are by design in breach of WhatsApp's terms, with ban risk ([Dragapp](https://www.dragapp.com/blog/whatsapp-mcp-server/), S). The official Cloud API is the only safe route.

Payments need one honest note. Pakistan-registered firms cannot use Stripe directly or PayPal, and the notes found conflicting information on Stripe. Collection for a Pakistani company should go through a licensed local gateway (PayFast, Safepay). Payouts to contributors can use Easypaisa, JazzCash or bank transfers via an aggregator. The README's plan to record payments manually at first is a reasonable way to avoid committing to a gateway before the pilot results.

## Install Claude helpers in five stages, read-only first

Nothing has been installed. The goal is to give a non-technical founder help with review, testing and data quality without handing a program the keys to the business. Two risks drive the staging. Third-party tool servers run with your credentials and read untrusted content: a marketplace of listings written by strangers is a realistic path for prompt injection (hostile text inside a listing telling the assistant what to do). And supply-chain quality varies. Anthropic's own SQLite server carried an SQL injection flaw that was forked over 5,000 times before it was archived ([The Register](https://www.theregister.com/2025/06/25/anthropic_sql_injection_flaw_unfixed/)). Claude Code's own documentation warns that servers that fetch external content expose you to prompt injection ([Claude Code docs](https://code.claude.com/docs/en/mcp)). Last-commit dates and licence files could not be verified directly for most of these tools. Registry `updatedAt` dates were used instead (P), and everything should be re-checked at install time.

| Stage | When | Install | Permissions and risks |
|---|---|---|---|
| 1 | Now; no credentials | Project reviewer agents in `.claude/agents/` (code-reviewer, security-reviewer, data-quality-auditor, Urdu-English copy checker) with read-only tools ([docs](https://code.claude.com/docs/en/sub-agents)). Use the built-in `/security-review`. Add Anthropic's `code-review` and `security-guidance` plugins from `claude-plugins-official`. | Agents you write yourself carry no third-party code. The `code-review` plugin is flagged "privileged" in the plugin directory, so read its command file first. `security-guidance` function was not verified. Anthropic says it does not control what plugins contain. |
| 2 | When the app runs locally | `frontend-design` and `webapp-testing` skills; Playwright MCP (Microsoft, Apache-2.0), pinned version, headless, local and staging only | Playwright's own docs say it is not a security boundary. Never log in to personal accounts in it. |
| 3 | When code is in GitHub | GitHub MCP (GitHub, MIT) with a fine-grained token limited to this repository and `--read-only` at first. This session already exposes GitHub tools. | Store tokens in environment variables. Branch protection on main. No merge or delete rights for agents. Review any `.mcp.json` or `.claude/` change in every pull request. |
| 4 | When real data exists | Postgres MCP Pro in restricted mode (Crystal DBA, MIT, community) or Google's MCP Toolbox (Apache-2.0), against a development copy with a read-only database role. The `xlsx` skill (source-available licence) for owner spreadsheets. Context7 for library docs (data passes through Upstash). | Never write access, never production. Treat all database text as untrusted. An AWS postgres MCP vulnerability was reported (single summary, unverified). |
| 5 | After the payment and hosting decisions | `gcloud` or Cloud Run MCP (Google; gcloud MCP is preview and unsupported) using service-account impersonation with narrow roles; Cloudflare MCP with a DNS-only token; Sentry MCP once Sentry exists; Stripe plugin only if a Stripe account is possible | Prefer human-run deploy commands for a non-technical owner. Do not install Stripe tools until Pakistan eligibility is resolved. WhatsApp sending belongs in application code, not an assistant tool. |

Avoid unofficial WhatsApp bridges, archived Anthropic reference servers (SQLite, PostgreSQL, Puppeteer, Google Maps, Slack and their forks), unvetted registry entries from third-party hosts, any database server with write access to production, and any tool given broad cloud Owner rights. Registry presence is not a safety signal, because anyone can publish; check that the namespace matches the vendor's real organisation. One rule is worth repeating: never combine private-data access, untrusted content and an outbound channel (for example database plus web fetch plus WhatsApp) in one session. The owner's connected claude.ai services (Indeed, MindMap AI, RankedIn) are unrelated to build and deploy work.

## Six cheap experiments can confirm or kill the idea in six weeks

### The risks that matter most

| Risk | Why it matters | Evidence | Mitigation |
|---|---|---|---|
| Nobody pays for a contributor list | Scraping tools and free open data are cheap substitutes | No demand test exists (notes) | Pre-sell before building |
| Revenue share too small to attract contributors | Cents per sale; contributors carry sales risk | Section 3 arithmetic | Fixed per-entry floor; non-cash recognition; time-limited bounties |
| Fake entries and contributor fraud | Medium and Google both fight it | 1.7% suspensions; 12 million fake profiles | No pay until verified; GPS and photo; second-contributor review; clawback right |
| Messaging law and WhatsApp bans | Highest-exposure product | Sections 3 and 4 | Defer; opt-in only; official API |
| Cannot pay contributors cheaply | Micro-payout fees, Pakistan rails, possible licensing | Section 3 | Batch payouts; local wallets; counsel |
| Two-sided cold start | Contributors need buyers, buyers need coverage | Notes' main GTM risk | One niche, a few cities |
| Incumbents and free data erode value | Overture, FSQ, Google, Justdial, IndiaMART | Section 1 | Sell verified freshness and niche depth, not "a list of shops" |
| Founder-market fit and cross-border limits | India-Pakistan commerce not researched | Section 2 | Confirm before committing to India |
| Existing code and secrets | README admits broken build and committed secrets | README | Rotate secrets; rebuild MVP scope |

### Open questions for the founder and counsel

First, what exactly does "50% → 40% → 30%" mean: a fall by merge level, by time phase locked per entry (as the README says), or both? The answer changes contributor economics sharply. Second, where is the founder and the legal entity based, and can it trade with and pay people in India? Third, who is the first paying buyer in the founder's network (an exporter, a distributor, an FMCG sales head)? Fourth, can AllLists lawfully hold contributor balances and pay out in Pakistan without a payment licence? Fifth, how do Pakistani law and PECA treat collecting and selling business contact data, and do sole proprietors' numbers count as personal data? Sixth, what do merged lists cost buyers: is there a volume discount that undercuts per-entry revenue? Seventh, can AllLists buy outlet-census data from audit firms (SurveyAuto, Ipsos) as a price benchmark?

### The experiments

All budgets and thresholds below are the research notes' assumptions or this report's, not researched benchmarks.

| # | Experiment | Duration and cost | What to measure | Pass if |
|---|---|---|---|---|
| 1 | Desk test: query the free Overture and Foursquare files for Pakistan counts by city and category | 1 to 2 days, free | Open-data coverage versus the 0.65 to 1.2 million outlet range | A clear gap in your chosen niche and cities |
| 2 | Data-gap sample: verify 200 to 500 shops in one trade and area by phone, photo or WhatsApp, then compare with Google Maps, Justdial and Overture | 2 to 3 weeks, small contributor fees | Share missing or wrong; verification cost per entry; call-back after 30 days for decay | At least 20 to 30% missing or wrong (proposed threshold) |
| 3 | Buyer pre-sale: show a sample to 20 to 30 buyers (distributors, tool vendors, sales teams) and offer a paid list at INR 2,000 to 10,000 | 4 weeks, near zero | Orders or signed pre-orders | 3 to 5 paid orders and verification cost under 30% of list price |
| 4 | Foreign-buyer pilot: offer a $50 to $200 Pakistani niche list to 30 to 50 UK and US importers or sourcing agents by LinkedIn and trade directories, no automated texts or calls | 4 weeks, near zero | Conversion; which fields buyers value (WhatsApp, owner name, catalogue) | At least 3 buyers paying over $50 and 5 contributors paid in under 7 days |
| 5 | Contributor motivation: two groups of 5 to 10 recruits, one with a fixed fee per verified entry plus share, one share only | 3 to 4 weeks | Entries per week, fraud rate, retention | Fixed-fee group clearly outproduces; fraud under control |
| 6 | Payout rails and legal check: test PKR wallet payouts via an aggregator; one hour with a Pakistani lawyer on PECA, data and balances | 1 to 2 weeks, small fees | Cost per payout, time to arrive, licensing answer | Payouts clear for under about 5% cost |

The notes propose a decision rule that this report adopts. Move to the next stage only if the data-gap test finds at least 20 to 30% of verified businesses missing or wrong elsewhere, and the buyer test converts at least 5 to 10% of contacted buyers. If the data gap fails, drop that niche or country. If the buyer test fails, change the buyer segment before changing the market.

## Conclusion

The research changes the founder's question from "which big market first?" to "which product has a price that can pay people?". The surprising result is that the market with the most potential and the market with the best fit are different, and the bridge between them is the buyer: a Pakistani or Indian contributor, a UK or Gulf buyer, and a list priced above the free-data ceiling. That decoupling of where data is made from where it is sold is the one structural idea in the evidence that survives scrutiny. It also explains why the US and EU belong in the plan as customers, not as launch sites, and why China belongs outside it for now.

Two uncomfortable facts should shape the next move. First, the 50/40/30 revenue share is generous in percentage terms but meaningless in cents, so the first decision to make is the per-entry floor and the repeat-sale mechanism, not the percentage. Second, the strongest precedent, Jigsaw, scaled and sold but its product was eventually deleted, and it paid contributors in access, not cash. The business is real only if verified, fresh, niche data commands lead-like prices from buyers who cannot get it free, and the six experiments above will show whether that is true before more code is written.
