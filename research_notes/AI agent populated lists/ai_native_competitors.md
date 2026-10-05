# AI-native and automation-based competitors and precedents for AI-populated business/local directories (research as of 5 Oct 2026)

Method note: research done via web search snippets; many primary pages (linuxfoundation.org, overturemaps.org, docs.overturemaps.org, sacra.com, cleanlist.ai, blog.opencorporates.com) were blocked by the egress proxy and could not be opened, so figures from them are search-snippet-level and flagged where relevant. Revenue figures labelled "Sacra estimate" are third-party estimates, not company-reported. Vendor pricing comparisons come from competitor/affiliate blogs and should be treated as indicative.

## 1. AI-native data and lead companies: what they collect, how, and price

### Takeaway
The market has split into (a) workflow/orchestration layers that resell many data providers (Clay), (b) legacy contact databases moving to AI features (ZoomInfo, Apollo, Cognism, Lusha), (c) cheap collection infrastructure (Apify, Outscraper, Firecrawl, Bright Data, Exa) where raw local-business scraping costs roughly $1-6 per 1,000 records. Money and valuation are accumulating in orchestration and AI-infrastructure layers, not in raw listings.

### Cited Findings
- Clay: Sacra estimates ARR of $150M in May 2026, up from $108M at end of 2025; company expected ~$200M in the current quarter and possibly ~$240M by fiscal year end (estimate/guidance as reported by Sacra and secondary press) — [Sacra](https://sacra.com/research/clay-crosses-150m-year/); [Sacra profile](https://sacra.com/c/clay/)
- Clay valuation: $5B in January 2026 (after a $55M employee tender led by DST), then a $115M Series D at $7.1B led by Wellington, with a16z, Sequoia, CapitalG, Meritech, DST and others participating — [Verdict](https://www.verdict.co.uk/newsletters/clay-completes-series-d); [AI Weekly](https://aiweekly.co/alerts/ai-sales-startup-clay-in-talks-for-wellington-led-round-at-7b-pre-money-up-from-5b-in-january)
- Clay pricing (2026): Free (100 Data Credits + 500 Actions/mo), Launch $185/mo (2,500 Data Credits, 15,000 Actions), Growth $495/mo (6,000 Data Credits, 40,000 Actions), custom Enterprise; two-credit system since March 2026; top-ups carry a ~50% premium — [Zeliq](https://www.zeliq.com/blog/clay-pricing); [Amplemarket](https://www.amplemarket.com/blog/how-much-does-clay-really-cost) (competitor blogs; search summary)
- Clay waterfall enrichment reportedly burns 10-25 credits per row; enriching 1,000 contacts with email, phone and company data reportedly uses 15,000-25,000 credits — [Zeliq](https://www.zeliq.com/blog/clay-pricing) (secondary, competitor source)
- ZoomInfo: full-year 2025 GAAP revenue $1,249.5M, up 3% YoY (growth has stalled to low single digits); launched GTM Studio workspace — [ZoomInfo/BusinessWire](https://www.businesswire.com/news/home/20260209677262/en/ZoomInfo-Announces-Fourth-Quarter-and-Full-Year-2025-Financial-Results/)
- ZoomInfo pricing (third-party): Professional from about $14,995/yr with 5,000 credits, Enterprise $45,000+; reported average spend $42,034/yr SMB and $164,064/yr enterprise — [Relevance AI comparison](https://marketplace.relevanceai.com/compare/zoominfo-alternatives); [CostBench](https://www.costbench.com/compare/cognism-vs-zoominfo/) (unverified vendor-comparison data)
- Cognism: about $22K+/yr, SMB average ~$25,009/yr; Lusha: free to ~$69.90/user/mo, SMB average ~$9,049/yr; Seamless.AI basic about $147/mo — [Spendhound](https://spendhound.com/marketplace/cognism-pricing); [Cognism blog](https://www.cognism.com/blog/lusha-vs-zoominfo) (vendor-authored; treat cautiously)
- Apollo.io: valued at $1.6B after Aug 2023 Series D (Bain Capital Ventures); Sacra estimate of $150M ARR at end of May 2025; Apollo said in May 2026 revenue has grown more than 5x since Aug 2023; plans Free, $49, $79, $119 per user/mo (annual), unified credit pool — [Sacra](https://sacra.com/c/apollo/); [11x guide](https://www.11x.ai/guides/apollo-io-pricing)
- Outscraper (Google Maps scraper): free to 500 records, then $3 per 1,000 records up to 100,000, cheaper above; full lead profile with email finding, verification and enrichment about $14 per 1,000 — [SyncGTM review](https://syncgtm.com/blog/outscraper-review-2026); [Datarade](https://datarade.ai/data-providers/outscraper)
- Apify Marketplace Google Maps actors price in the range $1-6 per 1,000 places: official pay-per-event actor $4 per 1,000 plus per-place event fees; third-party actors at $1.00, $2.50, $5.00 and $6.00 per 1,000 — [Apify](https://apify.com/lp/scrape-google-maps); [Apify actor $1/1k](https://apify.com/fancyboeing/my-actor); [Apify help](https://help.apify.com/en/articles/10774732-google-maps-scraper-is-going-to-pay-per-event-pricing)
- Bright Data datasets: charged per record or subscription; Google datasets from $250 for 100K records (about $0.0025/record) as a one-time purchase; one source says full business-record datasets with enrichment run $2,000-10,000+ — [Bright Data pricing docs](https://docs.brightdata.com/products/marketplace/pricing); [Bright Data Google dataset](https://brightdata.com/products/datasets/google) (the $2,000-10,000 figure comes from a competitor blog and is unverified)
- Phantombuster: Start $69/mo ($56 annual), Grow $159 ($128), Scale $439 ($352); priced by execution hours, not records — [Phantombuster](https://phantombuster.com/blog/ai-automation/phantombuster-pricing-explained)
- Firecrawl (AI web-scraping API): Scrape/Crawl/Map cost 1 credit per page, free tier 1,000 credits/mo; $14.5M Series A led by Nexus Venture Partners in 2025; a scoop reports a further $82M raise (August 2026; not confirmed by primary source) — [eesel](https://www.eesel.ai/blog/firecrawl-pricing); [Unite.ai](https://www.unite.ai/firecrawl-raises-14-5-million-series-a-to-power-the-future-of-ai-web-crawling/); [RuntimeWire scoop](https://runtimewire.com/article/scoop-firecrawl-raises-82m-after-its-14-5m-series-a-warm-up)
- Exa (AI search API): $85M Series B at $700M (Benchmark, Sept 2025); Sacra estimate $10M annualised revenue in Sept 2025 (~11x YoY); reported $250M raise at $2.2B valuation led by a16z in May 2026 — [Sacra](https://sacra.com/research/exa-at-10m-growing-11x-yoy); [Bloomberg Law](https://news.bgov.com/antitrust/andreessen-backed-ai-search-startup-exa-valued-at-2-2-billion)
- Newer "AI SDR" startups (e.g. AiSDR, $3M seed with Y Combinator) focus on outreach automation, not on building local-business datasets — [Flyer One](https://flyerone.vc/post/why-f1v-invested-in-aisdr)

### Inferences
- Raw local-business scraping is a commodity at about $0.001-0.006 per record; value is captured when records are verified, enriched with emails/phones and embedded in workflow (Clay at $185-495/mo; ZoomInfo/Cognism at $15-45K+/yr).
- Capital is flowing to orchestration (Clay) and agent-infrastructure (Exa, Firecrawl) layers. An AI-populated directory competes on the data layer, where the lowest-cost providers sit.

### Gaps
- I found no reliable evidence of a funded startup specifically using agents to build a consumer-facing local-business directory; the search surfaced AI-SDR and enrichment tools only. Could not verify Perplexity, Seamless.AI, Lusha, Cognism revenue or funding.
- Seamless.AI, Lusha and Cognism pricing comes only from competitor/aggregator pages; official pricing pages not opened.
- Sacra pages could not be opened directly; ARR figures are estimates from search snippets.

## 2. Map and place data producers: how freely available is baseline small-business data?

### Takeaway
Open baseline POI data is now large and permissively licensed: Overture (CDLA Permissive 2.0, about 64M places, 50 members), Foursquare OS Places (100M+ POIs, Apache 2.0, monthly), and OSM. Google's Places API remains costly ($32-40 per 1,000 calls) and its terms bar lead-list building. The cheap commodity layer is basic name/address/category/coordinates; contacts and verified attributes are not covered well.

### Cited Findings
- Overture Maps Foundation was founded in December 2022 by AWS, Meta, Microsoft and TomTom; Places theme has more than 64 million point features, licensed CDLA Permissive 2.0, distributed as GeoParquet — [Overture Places Guide](https://docs.overturemaps.org/guides/places); [Linux Foundation release](https://linuxfoundation.org/press/overture-maps-foundation-releases-first-open-map-dataset)
- April 2026 release source breakdown (features by source): Meta 59,413,511 (CDLA-P-2.0), Microsoft 7,261,643, Foursquare 6,749,057 (Apache-2.0), AllThePlaces 1,749,242 (CC0-1.0), plus others (counts overlap, so the total is not the sum) — [Overture Places Guide / release data via search](https://docs.overturemaps.org/guides/places)
- Overture reached 50 members (nearly double its 2024 count), adding Grab, Uber, Samsara, Fresno County and UC Santa Cruz; Meta, TomTom, Tripadvisor and Uber contribute live signals (foot traffic, ratings, pickups/drop-offs) to the June 2026 Places update — [Linux Foundation](https://www.linuxfoundation.org/press/overture-maps-foundation-reaches-50-members-as-industry-converges-on-open-data-to-ground-ai)
- May 2026: BrightQuery joined as a POI provider, adding 250,000+ new US places, with millions more expected — [Linux Foundation](https://www.linuxfoundation.org/press/brightquery-joins-overture-maps-foundation-to-expand-open-places-data-coverage)
- Overture roadmap (2026 member summit): Places Connect launching in H2, ML-based quality model in Q3, revamped places taxonomy on quarterly cadence; a Places+Imagery Task Force (early 2026) uses street-level imagery to improve POI geolocation, which "opens the door to AI native places data" — [Overture summit blog](https://overturemaps.org/blog/2026/inside-the-2026-overture-member-summit-the-road-ahead/); [Overture summit schedule](https://overturesummit2026.sched.com/list/descriptions/company/Intermediate)
- Overture uses ML validation/conflation and a confidence score; GERS assigns each feature a persistent 128-bit ID; Microsoft-sourced points carry confidence 0.6 — [LWN](https://lwn.net/Articles/995992); [dev.to analysis](https://dev.to/krschap/exploring-overture-map-data-2l49)
- Foursquare Open Source Places: 100M+ POIs in 200+ countries, 20+ core attributes (name, address, coordinates, website, social handles, category), monthly updates, Apache 2.0, commercial use allowed, Parquet on S3 (launched Nov 2024) — [Foursquare blog](https://foursquare.com/resources/blog/products/foursquare-open-source-places-a-new-foundational-dataset-for-the-geospatial-community/); [OSM community](https://community.openstreetmap.org/t/foursquare-releases-100m-poi-dataset-under-apache-2-0/121883)
- Google Places API (New): Pro $32 per 1,000, Enterprise $35, Enterprise + Atmosphere $40; free usage caps per SKU (10,000 Essentials, 5,000 Pro, 1,000 Enterprise) replaced the $200 monthly credit in March 2025 — [openplacesapi.com](https://openplacesapi.com/blog/google-places-api-pricing); [Google FAQ](https://developers.google.com/maps/billing-and-pricing/faq)
- Google Maps terms prohibit bulk extraction, caching and building lead lists or substitute directories; Google sued SerpApi in Dec 2025 (motion to dismiss filed Feb 2026, hearing set May 2026; outcome not found) — [ConductAtlas](https://conductatlas.com/platform/google-maps/google-maps-platform-terms-of-service/no-scraping-or-content-extraction/); [Proxyway](https://proxyway.com/news/google-sues-serpapi)
- Meta's RapiD / MapWithAI (AI-suggested roads and Microsoft building footprints for OSM mappers): no new releases since Dec 2024 as Meta's effort moved into Overture — [OSM wiki: RapiD](https://wiki.OpenStreetMap.org/wiki/RapiD); [OSM wiki: Meta](https://wiki.openstreetmap.org/wiki/Meta)

### Inferences
- A free, legal baseline of ~100M POIs exists; AllLists should license Overture/FSQ rather than spend agent compute rebuilding name/address/coordinates.
- Overture's and Meta's own AI/ML direction means baseline freshness and quality will keep improving for free, eroding any moat on "AI-built basic listings".

### Gaps
- Could not open Overture pages; release cadence (monthly), total place count for latest release, and exact member list not verified beyond snippets.
- Apple Maps, Amazon Location, HERE and TomTom pricing/licence terms not researched.
- Coverage quality in South Asia, Africa, and informal-economy businesses in Overture/FSQ not verified.

## 3. Directory and listing sites using AI generation

### Takeaway
Evidence favours incumbents using AI as a layer on existing proprietary content, while thin AI-generated or programmatic directories face severe Google penalties. Incumbents report modest growth (Yelp +4%, Tripadvisor +3%) and are licensing content to AI platforms.

### Cited Findings
- Google's August 2026 spam update targeted scaled AI content and low-value programmatic SEO; case studies describe sites losing rankings for 200,000+ queries and one with 1.5M+ indexed URLs losing many; thin-pattern sites lost 50-80% of traffic; recovery typically takes at least several months after fixes — [GSQi](https://gsqi.com/marketing-blog/august-2026-google-spam-update-case-studies/); [Seoteric](https://www.seoteric.com/googles-august-2026-spam-update-impact-and-recovery-guidance/)
- A named case of a 22,000-AI-page penalty was surfaced (details not verified) — [Tailride](https://tailride.so/blog/google-penalty-22000-ai-pages)
- G2 reportedly lost about 80% of organic traffic by late 2025, with Reddit ranking for most comparison queries it once owned (secondary report) — [QuickSEO](https://quickseo.ai/blog/programmatic-seo-stats-2026-is-pseo-still-viable-in-the-ai-search-era)
- Google 2026 spam policy defines scaled content abuse to include generative AI pages with no added value and scraped feeds — [Seoteric](https://www.seoteric.com/googles-august-2026-spam-update-impact-and-recovery-guidance/)
- Google connected Gemini to Google Business Profile on 10 June 2026 so owners can update hours, respond to reviews and analyse performance via chat; Business Profile now serves as structured data for local pack and AI answers — [PPC Land](https://ppc.land/gemini-now-manages-your-google-business-profile-with-a-single-tap/); [Whitespark](https://whitespark.ca/blog/23-local-developments-you-need-to-know-about-from-q2-2026/)
- Yelp: 2025 net revenue $1.46B (+4%); Yelp Assistant requests for quotes up more than 400% YoY (about 5% of all RAQ projects); agreement with OpenAI to supply local content; acquired Hatch — [Yelp/BusinessWire](https://www.businesswire.com/news/home/20260212812443/en/Yelp-Delivers-Record-Net-Revenue-in-2025-Accelerating-Investment-in-AI-Transformation/)
- Tripadvisor: 2025 revenue $1.9B (+3%); shipped an AI-native MVP in Q4 2025 with higher engagement than its prior assistant — [PhocusWire](https://www.phocuswire.com/tripadvisor-q4-2025-earnings)
- Justdial: 54.7M listings and 182.4M quarterly unique visitors in Q4 FY26 (to 31 March 2026); uses AI to qualify enquiries — [Business News Today](https://business-news-today.com/just-dial-q3-fy26-results-net-profit-falls-10-2-amid-strong-ai-execution-rs-5703cr-cash-cushion-and-campaign-growth/); [Inc42](https://inc42.com/buzz/justdial-q1-profit-rises-13-yoy-to-inr-160-cr)
- Swiggy integrated ChatGPT, Claude and Gemini as ordering channels from 28 Jan 2026 — [Angel One news](https://oga-prod.angelone.in/news/stocks/swiggy-integrates-chatgpt-gemini-and-other-ai-tools-for-food-and-grocery-delivery)

### Inferences
- AI-written profiles at scale without owner/user-generated or verified content carry real search-visibility risk; listings must be differentiated by owner-claimed and verified facts.
- Incumbent local platforms are positioning as structured data sources for AI assistants; an independent directory may find distribution via being cited by AI agents rather than by classic SEO.

### Gaps
- No named, reliable AI-generated local directory with disclosed traffic and revenue outcomes found; the "programmatic SEO" evidence is general case studies, not directory-specific.
- Yelp AI and Tripadvisor AI details beyond earnings summaries not verified; Zomato AI listing features not found.

## 4. Public-sector and open data agents could use legally

### Takeaway
Registry data is the most legally clean source but varies hugely: UK is open and free; India MCA master data is on the open data portal; Pakistan SECP basic search is free but bulk reuse terms are unclear; Delaware prohibits mining; OpenCorporates is share-alike unless paid. Registries cover legal entities, not informal local businesses.

### Cited Findings
- UK Companies House: free monthly snapshot of live companies (CSV ZIPs, available within 5 working days of month end), at no charge since June 2012; Open Government Licence not confirmed in the snippet — [GOV.UK data products](https://www.gov.uk/guidance/companies-house-data-products); [data.gov.uk](https://www.data.gov.uk/dataset/companies-house-free-company-data-product)
- Companies House API default limit 600 requests per 5 minutes; higher limits by request — [Companies House developer guidelines](https://developer-specs.company-information.service.gov.uk/guides/rateLimiting)
- India MCA company master data (CIN, name, registration date, status, class, capital): about 3.67M companies on OGD India (data.gov.in) in CSV, governed by the Government Open Data License India — [AIKosh dataset](https://aikosh.indiaai.gov.in/home/datasets/details/company_master_data.html); [Apify actor listing](https://apify.com/nexgendata/mca-company-registry)
- Pakistan SECP: basic search (name/number, status, address, officers) free; certified extracts PKR 200-3,000 (~USD 0.70-10.50); data-sharing MoUs with government bodies under PRMI — [LemReveal](https://lemreveal.com/how-to/is-registry-free/pakistan); [SECP PRMI press release](https://www.secp.gov.pk/wp-content/uploads/2025/08/Press-Release-SECP-Integrates-with-key-organizations-for-Data-Sharing-under-Pakistan-Regulatory-Modernization-Initiative-PRMI.pdf) (bulk-reuse licence not found)
- US: Delaware offers no API or bulk download, "strictly prohibits mining data" and warns against automated tools; several other states publish full registries on Socrata portals as public domain or commercially licensable — [Kyckr](https://kyckr.com/guides-and-reports/delaware-company-registry); [DEV Community](https://dev.to/bradju/124-million-us-business-registrations-are-sitting-on-state-open-data-portals-free-3h1n); [OpenCorporates blog](https://blog.opencorporates.com/2025/09/15/sourcing-data-directly-from-us-state-registries) (not opened)
- OpenCorporates: data under share-alike Open Database Licence; share-alike API keys free with evidence of good use and contributing back; commercial API from £2,250/yr (500 calls/mo), £6,600 (2,500 calls/mo), £12,000 (5,000 calls/mo), Enterprise custom — [OpenCorporates terms](https://opencorporates.com/terms-of-use-2/); [OpenCorporates pricing](https://opencorporates.com/pricing/); [Zephira summary](https://zephira.ai/opencorporates-pricing-explained-2026-plans-api-limits-licensing-and-what-it-means-in-production/)
- China: Qichacha is the largest company-lookup platform (200M+ entities, reportedly heading for a stock listing); Tianyancha (Tencent-backed, since 2014) crawls and cross-validates public filings into an ownership graph with a developer API — [Deepline](https://deepline.com/gtm-stack/providers/tianyancha); [CompanyData.com](https://companydata.com/b2b-data-provider-comparisons/china/)

### Inferences
- Registry data gives a legal baseline for formal companies; Qichacha/Tianyancha show registry aggregation can itself be a large business, but via processing and graph/compliance value rather than raw access.
- OpenCorporates' share-alike ODbL terms make it unsuitable for a proprietary layer unless paying.

### Gaps
- EU register access, OpenCorporates coverage counts, Companies House exact licence text, and SECP/MCA terms for commercial scraping not verified.
- No data on legal limits of automated scraping of Qichacha sources.

## 5. Defensibility: what stays valuable when anyone can run agents

### Takeaway
Evidence suggests value shifts from collection to verification, freshness and workflow. Contact data decays ~3%/month, so freshness and verification are ongoing costs that raw scrapes lack. I found no solid analogue study; the case for the moat is mostly inference.

### Cited Findings
- Verified B2B contact data median price: $34.29 per 1,000 emails (pricing pages reviewed Sept 2026), range $13.00-$435.29 (33.5x spread); contact data decays ~3% a month (~30% a year) — [Cleanlist](https://www.cleanlist.ai/blog/2026-09-07-what-b2b-contact-data-costs) (vendor blog, not opened)
- Developer analysis claims the prospect data an AI agent needs now costs more than the inference, and data prices are not falling like inference — [DEV Community](https://dev.to/threadotter/i-priced-enrichment-for-an-ai-agent-at-scale-the-data-costs-more-than-the-inference-290f) (single practitioner source)
- Clay's model (resell many providers through waterfalls) reached an estimated $150M ARR, showing value in orchestration/workflow over owning data — [Sacra](https://sacra.com/research/clay-crosses-150m-year/)
- Yelp keeps growing (+4%, $1.46B) and signed with OpenAI, suggesting reviews/claimed-business relationships retain value even as AI answers proliferate — [Yelp/BusinessWire](https://www.businesswire.com/news/home/20260212812443/en/Yelp-Delivers-Record-Net-Revenue-in-2025-Accelerating-Investment-in-AI-Transformation/)
- Overture members contribute proprietary live signals (foot traffic, ratings, pickups) to keep data current, i.e. even open baselines rely on non-public signals — [Linux Foundation](https://www.linuxfoundation.org/press/overture-maps-foundation-reaches-50-members-as-industry-converges-on-open-data-to-ground-ai)

### Inferences
- Defensible assets for AllLists: owner-claimed profiles, verified contacts with timestamps, contributor community, outreach/response data and demand statistics that no scraper can reproduce. Agent-collected baseline is not defensible.
- Price-comparison and review-scraping analogues were not found in my research; the claim that these became commoditised is untested here.

### Gaps
- No primary evidence on analogues (price comparison, review aggregation, lead-list scraping) and how margins moved; no data on claimed-profile conversion rates or owner-verification costs.
- Could not verify that contributor communities or claimed profiles resist AI-agent substitution in emerging markets.

## 6. Pricing pressure: falling collection costs and what buyers still pay for

### Takeaway
Raw record collection prices are near zero ($0.001-0.006 per record at scraping marketplaces; Bright Data ~$0.0025). Buyers continue to pay for verified, enriched, deliverable contacts ($13-435 per 1,000 verified emails; $15K-165K per year for ZoomInfo-class platforms).

### Cited Findings
- Scraper marketplaces: Apify $1-6 per 1,000 places; Outscraper $3 per 1,000 (about $14 enriched); Bright Data about $0.0025/record — see Section 1 sources
- Verified-email median $34.29 per 1,000, range $13-435 — [Cleanlist](https://www.cleanlist.ai/blog/2026-09-07-what-b2b-contact-data-costs)
- Google Places API $32-40 per 1,000 calls vs scraping at $1-6 per 1,000 — [openplacesapi.com](https://openplacesapi.com/blog/google-places-api-pricing); [Apify](https://apify.com/lp/scrape-google-maps)
- ZoomInfo growth slowed to +3% (2025) while newer orchestration vendors (Clay, Exa) grew rapidly — [BusinessWire](https://www.businesswire.com/news/home/20260209677262/en/ZoomInfo-Announces-Fourth-Quarter-and-Full-Year-2025-Financial-Results/); [Sacra](https://sacra.com/research/clay-crosses-150m-year/)
- Clay's credit model costs 10-25 credits per waterfall row; users pay a 50% premium for top-ups — [Zeliq](https://www.zeliq.com/blog/clay-pricing)

### Inferences
- A directory selling bulk lists of basic local-business data would price against a $1-6 per 1,000 floor; revenue must come from verification, enrichment and outreach delivery.
- Pricing shift from per-seat to per-credit/action suggests buyers pay for outcomes (verified contact, delivered message).

### Gaps
- No time series of list prices over time showing the actual decline; ZoomInfo/Cognism list prices are third-party reports only.

## 7. Strategic options for AllLists

### Takeaway
The research supports a hybrid: license free baselines (Overture, FSQ OS Places, registries), use agents only as a cheap draft/enrichment layer, and compete on owner-claimed/verified data, freshness guarantees and outreach delivery. These are inferences from the findings above, not sourced claims.

### Cited Findings
- Baseline POI data: Overture (CDLA-P-2.0, 64M+ places) and Foursquare OS Places (Apache 2.0, 100M+) are free for commercial use — [Overture Places Guide](https://docs.overturemaps.org/guides/places); [Foursquare](https://foursquare.com/resources/blog/products/foursquare-open-source-places-a-new-foundational-dataset-for-the-geospatial-community/)
- Scraping Google Maps content carries ToS and litigation risk — [ConductAtlas](https://conductatlas.com/platform/google-maps/google-maps-platform-terms-of-service/no-scraping-or-content-extraction/); [Proxyway](https://proxyway.com/news/google-sues-serpapi)
- Scaled AI content without added value risks large traffic loss — [GSQi](https://gsqi.com/marketing-blog/august-2026-google-spam-update-case-studies/)
- Google is giving owners AI-chat tools to manage Business Profiles, lowering the cost of owner-maintained data and raising the bar for rival directories — [PPC Land](https://ppc.land/gemini-now-manages-your-google-business-profile-with-a-single-tap/)

### Inferences
- Option A (recommended by evidence): baseline from Overture/FSQ/registries plus agent drafts, with human contributors and owners verifying and a visible "verified/claimed" badge; do not publish unverified agent pages as indexable at scale.
- Option B: sell outreach delivery and response data (proprietary signals) rather than lists.
- Avoid depending on Google Places data or scraping it for resale.
- Overture's quarterly taxonomy and ML quality roadmap, plus Places Connect, may offer a channel for contributing back; evaluate fit.

### Gaps
- No cost model for owner verification or contributor incentives; no evidence found on AllLists's target geographies' coverage in open data.
- Overture Places Connect scope and licensing for contributors not verified.
