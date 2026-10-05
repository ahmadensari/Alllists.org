# AI Agent Data Collection for Business Directory Lists: Feasibility, Accuracy, Cost, Verification

Research date: 2026-10-05. Method note: WebSearch worked. WebFetch was blocked by the egress proxy for arxiv.org, docs.firecrawl.dev, twilio.com, foursquare.com, docs.overturemaps.org and hosted-files.sched.co, so almost every figure below comes from search-result summaries of the cited pages, not from reading the primary page. Treat all numbers as "reported by search snippet, primary page not read" unless stated. Vendor prices change often and should be re-checked. All cost-per-record and cost-per-million figures in the "Inferences" subsections are my own estimates with stated assumptions, not published numbers.

## 1. Accuracy: what benchmarks and studies say about LLM/agent extraction and business-data quality

### Takeaway
LLMs extract fields from a page that actually contains them very well (F1 ~0.95+ in a controlled study, hallucination ~3%), and LLM entity matching reaches ~95-99% F1 on clean benchmarks. The weak points are (a) agents navigating the live web end to end, where success is far from perfect and decays on long tasks, and (b) the underlying source data (Overture/OSM/Foursquare), where staleness and location error are the main defects. I found no published benchmark measuring agent-collected small-business records (name, address, phone, hours, size) against ground truth, so agent-vs-Google/OSM accuracy for this exact task is unmeasured in the sources I could reach.

### Cited Findings
- NEXT-EVAL (arXiv 2505.17125, 2025): with "Flat JSON" input, Gemini-2.5-pro-preview reached precision 0.9939, recall 0.9392, F1 0.9567 and hallucination rate 0.0305 on web data-record extraction; input format (flat JSON vs slimmed HTML vs hierarchical JSON) materially changed accuracy. This is extraction from a page that contains the data, not discovery. — [NEXT-EVAL](https://arxiv.org/html/2505.17125v1)
- When a field is absent from the page, LLMs may generate plausible values such as phone numbers that were not listed (practitioner write-up, not a measured rate). — [webscraping.ai FAQ on LLM hallucination](https://webscraping.ai/faq/scraping-with-llms/what-is-llm-hallucination-and-how-can-i-prevent-it-in-web-scraping)
- A 2025 study benchmarked Llama-3, Llama-4, DeepSeek-R1 and ChatGPT-4.1 on detecting errors in personal contact information and found LLMs outperformed classical error-detection tools Raha and Baran (no business-directory-specific rate found in snippet). — [HPI / arXiv 2406.08246 listing](https://www.arxiv.org/pdf/2406.08246)
- Entity matching with LLMs: on OpenSanctions Pairs, off-the-shelf LLMs beat a 91.33% F1 rule-based production baseline, reaching 98.95% F1 (GPT-4o) and 98.23% with a local 14B open model; GPT-4 product matching F1 was 95.78% (Abt-Buy), 85.21% (Amazon-Google, few-shot), 89.61% (WDC Products). Entity matching on names/addresses of small businesses was not specifically benchmarked in what I found. — [OpenSanctions Pairs, arXiv 2603.11051](https://arxiv.org/html/2603.11051); [Match, Compare, or Select?](https://arxiv.org/pdf/2405.16884)
- BrowseComp (OpenAI, 1,266 hard multi-hop browsing questions): GPT-4o with browsing 1.9% (0.6% without), o1 ~10%, Deep Research 51.5% at launch (2025). A leaderboard aggregator reports GPT-5.5 Pro 90.1%, GPT-5.4 Pro 89.3%, Claude Mythos 5 88% as of 2026-07-06 (aggregator; not verified against a primary leaderboard). BrowseComp tests finding one obscure fact, not enumerating many records. — [OpenAI BrowseComp](https://openai.com/index/browsecomp/); [Moonlight review](https://themoonlight.io/review/browsecomp-a-simple-yet-challenging-benchmark-for-browsing-agents); [BenchLM](https://benchlm.ai/benchmarks/browse-comp)
- WebArena: best single agent reported 61.7% (IBM CUGA, Feb 2025) vs 78% human; success rose from 14% to ~60% in two years. — [WebArena search summary / NeurIPS](https://neurips.cc/virtual/2023/79176) (the 61.7% figure came from the search summary, source page not identified precisely)
- WebVoyager: claimed ~90% by some agents, but "An Illusion of Progress?" (Online-Mind2Web, 300 tasks on 136 sites, human-evaluated) found WebVoyager has shortcut tasks (a Google-search-only agent solves up to 51%) and LLM-judge agreement with humans is low; on Online-Mind2Web, agents scored well below their WebVoyager claims. — [arXiv 2504.01382](https://arxiv.org/pdf/2504.01382)
- Long-horizon decay: arithmetic of compounding (99% per step over 100 steps is ~37%; 95% per step over 20 steps is ~36%), and one 2026 study reports Pass@1 dropping from 76.3% on short tasks to 52.1% on very long tasks, a super-linear decline. — [Long-Horizon Task Mirage, arXiv 2604.11978](https://arxiv.org/pdf/2604.11978); [buildmvpfast](https://www.buildmvpfast.com/blog/why-long-horizon-ai-agents-fail-compounding-error-memory-2026)
- Overture Places accuracy tied to confidence score: places with confidence >=0.6 showed 81.2% accuracy, >=0.9 showed 95% (Overture Summit 2026 slide, via search summary). Main defects: wrong location for correct places, outdated records for incorrect ones. — [Overture Summit 2026 deck](https://hosted-files.sched.co/overturesummit2026/39/Places%20Surge%20Headliner.pdf) (not fetched; via search summary)
- Overture Places composition as of April 2026: >64M places; Meta 59,413,511, Microsoft 7,261,643, Foursquare 6,749,057, AllThePlaces 1,749,242, plus smaller sources (counts are source features before conflation). — [Overture Places guide](https://docs.overturemaps.org/guides/places)
- Foursquare's improved "Closed" model identified almost 700,000 new permanently closed US restaurants; precision and recall up ~20% in the US. — [Foursquare blog](https://foursquare.com/resources/blog/news/fsq-places-introducing-our-improved-closed-model)
- OSM POI completeness is category- and place-dependent: German retail completeness 42-100% by district; Canadian shop completeness 7-81%, major chains 33-51%; strong Global North bias in contributors. — [AGILE-GISS 2021](https://agile-giss.copernicus.org/articles/2/20/2021/agile-giss-2-20-2021.pdf); [OSM wiki Completeness](https://wiki.openstreetmap.org/wiki/Completeness); [SotM 2022](https://2022.stateofthemap.org/sessions/GPMSLW/)
- Google Maps accuracy for small businesses: no independent quantitative study found. — see Gaps.

### Inferences
- Real error budget for an agent pipeline = discovery error (missed or wrong entity) + extraction error (~3-5% when the page has the data) + staleness of the source page. Extraction is the smallest component; entity identity (is this the same shop as the OSM node?) and "page is out of date" dominate.
- Do not give agents long free-form browsing tasks. Per-step reliability compounding means short, checkpointed, single-record jobs (search, fetch 2-4 pages, extract to schema, cite the evidence span) are far more reliable than "research the whole city".
- Requiring every extracted phone/address to be quoted verbatim from the fetched text (and rejecting values not found as a substring) is a cheap guard against the fabricated-phone-number failure mode.
- Overture's own self-reported figures (81% at >=0.6, 95% at >=0.9) suggest even the best open POI base is ~5-20% wrong depending on the threshold, so agents seeded from it start with that baseline.

### Gaps
- No peer-reviewed or vendor-published accuracy number for agent-collected small-business directory records (phone, hours, size) was found.
- No measured hallucination rate specifically on phone numbers or opening hours.
- No independent accuracy study of Google Places for small businesses, nor of Foursquare/OSM phone and hours fields; Overture's own accuracy slide not read directly.
- Accuracy of "size" (employees / floor area) fields: nothing found; likely the least reliable field.

## 2. Cost: per page, per record, verification, geocoding, estimate per million records

### Takeaway
Raw LLM extraction is cheap (about half a cent to 2 cents per page at current Haiku/Sonnet list prices); search calls, anti-bot proxies, retries and verification dominate, and human review dominates everything if more than a few percent of records are checked. A plausible agent-plus-verification cost is order of $0.03-$0.30 per record (estimate), versus $0.70-$1.64 per task for a full browser agent as billed by Browser Use Cloud.

### Cited Findings
- Claude API list prices (2026): Haiku 4.5 $1/$5, Sonnet 4.6 $3/$15, Opus 4.7 $5/$25 per million input/output tokens; prompt caching up to 90% off, Batch API 50% off. — [MetaCTO](https://metacto.com/blogs/anthropic-api-pricing-a-full-breakdown-of-costs-and-integration); [Price Per Token](https://pricepertoken.com/pricing-page/model/anthropic-claude-opus-4.7)
- Search APIs (per 1,000): Exa $7 search; Brave $5 (with $5 monthly free credit); SerpAPI plan-based, entry tier $25 per 1,000 searches ($75 for 5,000); Tavily ~$8/1k at research depth. — [DEV Community 7 cheapest search APIs](https://dev.to/team_metabees_4b5127db951/7-cheapest-web-search-apis-for-ai-agents-in-2026-ranked-76m); [apicostcalc](https://apicostcalc.com/ru/blog/exa-vs-tavily-vs-serper-vs-brave-web-search-api-cost.html); [techstackups](https://techstackups.com/comparisons/best-serp-api-comparison-serpapi-exa-tavily/)
- Firecrawl: Scrape/Crawl/Map 1 credit per page; JSON/LLM extraction +4 to +5 credits (5 credits per extract call in some descriptions); Enhanced/Stealth proxy +4 credits (5 total) for Cloudflare-protected sites; JSON plus Enhanced = 9 credits per page. Plan dollar prices not captured (primary page blocked). — [Firecrawl billing docs](https://docs.firecrawl.dev/billing); [eesel](https://www.eesel.ai/blog/firecrawl-pricing); [ScrapeGraphAI](https://scrapegraphai.com/blog/firecrawl-pricing)
- Browser Use Cloud: $0.01 task initialisation plus per-step model cost from $0.002 (Browser Use LLM) to $0.10 (Claude Opus 4.5); typical tasks $0.70-$1.64 depending on agent version; V4 completed 76% of "difficult real-world" tasks (vendor benchmark); one trade-press piece reports a vendor claim of 3 cents per successful task (vendor claim, unverified). — [Browser Use pricing](https://docs.browser-use.com/cloud/pricing); [Models and pricing](https://docs.cloud.browser-use.com/get-started/models-and-pricing); [RuntimeWire](https://runtimewire.com/article/browser-use-cloud-v4-luna-web-agent-cost)
- Twilio Lookup Line Type Intelligence $0.008 per request (Basic lookup cheaper/free tier not captured). — [Twilio Lookup pricing](https://www.twilio.com/en-us/lookup/pricing)
- ZeroBounce email verification: pay-as-you-go from $39 for 2,000 credits; $0.0138/credit at 5,000; ~$19.50 per 1,000 at small tier; 10k $129; 100k $649 (about $0.0065/credit). NumVerify pricing not found. — [tlinky review](https://tlinky.com/zerobounce-review/); [Emelia pricing hub](https://emelia.io/hub/zerobounce-pricing)
- Google Places (New): Text Search / Nearby Search $32 per 1,000 (first 100k/month, Pro SKU) falling to $2.40 per 1,000 above 5M; Place Details Essentials $5, Pro $17, Enterprise $20 per 1,000; free monthly caps since 2025-03-01 of 10k (Essentials), 5k (Pro), 1k (Enterprise). Storing/caching Google data is restricted by its terms (not verified in snippet). — [Woosmap pricing breakdown](https://www.woosmap.com/blog/google-places-api-pricing); [Google pricing page](https://developers.google.com/maps/billing-and-pricing/pricing)
- Geocoding: Google Geocoding $5 per 1,000 (10k free/month); Mapbox temporary geocoding $0.75 per 1,000 at 100k-500k/month falling to $0.45 at 1-5M, permanent (storable) $5 per 1,000, free 100k/month; HERE ~$0.50-0.75 per 1,000 at volume; public Nominatim max 1 request/second and not for bulk; Pelias (MIT) and Nominatim (GPL-2.0) can be self-hosted, Pelias runnable on 8 cores/16GB for European data. — [CSV2GEO comparison](https://csv2geo.com/blog/geocoding-api-pricing-compared-real-cost-2026); [Nominatim usage policy](https://operations.osmfoundation.org/policies/nominatim/); [OpenCage on self-hosting](https://opencagedata.com/alternatives/self-hosting-nominatim.md)
- Cloudflare: from 2026-09-15 default settings block Training and Agent category crawlers (and mixed-use crawlers, ~36% of crawler traffic) on ad-carrying pages; Search crawlers still allowed; pay-per-crawl / pay-per-use being introduced. This raises cost and failure rate for agentic fetching. — [chudi.dev](https://chudi.dev/blog/cloudflare-block-ai-crawlers-september-15); [letsdatascience](https://letsdatascience.com/news/cloudflare-gives-publishers-control-over-ai-crawlers-3f1384fa)
- Human annotation economics: LLM-first labelling with human review of low-confidence items reported 50-96% cost reduction in classification-type tasks; but showing annotators LLM labels did not speed them up and introduced anchoring bias. — [Toloka](https://toloka.ai/blog/llms-and-humans-for-data-labeling/); [Hands-on tutorial arXiv 2411.04637](https://arxiv.org/html/2411.04637v3)

### Inferences (ESTIMATES, assumptions labelled)
- Per page, LLM extraction only: assume ~5,000 input tokens of cleaned markdown and ~300 output tokens. Haiku 4.5: 5,000 x $1/M + 300 x $5/M = ~$0.0065. Sonnet 4.6: ~$0.0195. Batch API halves these. Assume 10,000 input tokens for messy pages: ~$0.012 (Haiku) / ~$0.035 (Sonnet).
- Per record, pipeline A ("search + fetch + extract", no browser agent): 1 search ($0.005-0.008) + 3 pages x ($0.0065 extraction + $0.001-0.01 fetch/proxy, depending on self-hosted vs Firecrawl-style credits) + 1.5x retry factor = roughly $0.03-$0.06 with Haiku-class model, $0.10-$0.25 with Sonnet-class on 5 heavier pages. Browser-agent pipeline B using Browser Use Cloud at published task prices: $0.70-$1.64 per task, which is 10-50x pipeline A.
- Automated verification add-on per record: phone line-type lookup $0.008 + geocode $0.0005-$0.005 (self-host Pelias/Nominatim near zero, plus infrastructure) + email check $0.0065-$0.02 where an email exists = about $0.01-$0.035.
- Human audit add-on: unknown wage and minutes, so assumption: 1-3 minutes per record at $3-$15/hour gives ~$0.05-$0.75 per record reviewed. A 5% sample costs $0.003-$0.04 per record; 100% review costs $0.05-$0.75 per record, i.e. equal to or greater than all automation combined.
- Rough cost per million records (ESTIMATE): fully automated A with Haiku, Overture/OSM seed for discovery, Crawl4AI self-hosted: ~$30k-$60k per million plus verification ~$10k-$35k = ~$40k-$95k. Sonnet-class heavier pages: ~$100k-$250k plus verification. Browser-agent pipeline B: ~$0.7M-$1.6M. Add 5% human sampling: +$3k-$40k; add 100% human review: +$50k-$750k. Excludes engineering, proxies for hard sites, storage, and re-crawling for freshness (multiply by number of refresh cycles per year).
- Seeding from Overture/OSM (free, ~64M+ places) and using agents only to fill gaps (phone, hours, website) is far cheaper than discovering entities by agent; discovery by search alone costs an order of magnitude more per usable record.
- Google Places as a data source at $17-$32 per 1,000 calls ($17k-$32k per million records at base tier) is within the same order of magnitude as agent extraction, but its terms probably restrict storing data in your own directory (check before relying on it).

### Gaps
- Primary pricing pages (Firecrawl, Twilio, Exa, Tavily, Brave) not fetched; Firecrawl plan dollars per credit not captured; Apify per-result actor prices, Perplexity API, OpenAI/Claude web-search-tool per-search fees, NumVerify and Twilio Basic lookup prices not found.
- No published per-record cost from a real agent-built directory pipeline was found.
- Residential proxy / CAPTCHA-solving costs not researched.

## 3. Tooling: frameworks, licences, maturity, failure modes

### Takeaway
Mature, free building blocks exist for each stage (Overture/OSM for seeding, Crawl4AI or Scrapy+Playwright for fetching, LLM for extraction, Pelias/Nominatim for geocoding). Managed APIs (Firecrawl, Exa, Browser Use Cloud) trade money for less engineering. The recurring failure modes are bot blocking (now policy-level at Cloudflare), JS-heavy sites, rate limits, and benchmark-to-production gaps.

### Cited Findings
- Crawl4AI: Apache-2.0 licence, free self-hosted Python library, no credit meter; Firecrawl: AGPL-3.0 server with managed cloud, free tier and paid plans; GitHub stars reported ~135k (Firecrawl) vs ~69k (Crawl4AI) at time of the comparison page (date not shown). — [OpenAlternative compare](https://openalternative.co/compare/crawl4ai/vs/firecrawl); [Apify blog](https://blog.apify.com/crawl4ai-vs-firecrawl/)
- Pelias is MIT-licensed (Elasticsearch-based); Nominatim is GPL-2.0 (PostgreSQL). — [OpenCage](https://opencagedata.com/alternatives/self-hosting-nominatim.md); [pyPelias](https://pypi.org/project/pyPelias/)
- Overture Maps places theme is free on S3 and Azure Blob; sources include Meta, Microsoft, Foursquare, AllThePlaces and smaller providers; each place has a 0-1 confidence score. — [Overture Places guide](https://docs.overturemaps.org/guides/places); [DVRPC catalog](https://catalog.dvrpc.org/dataset/overture-maps-places)
- Firecrawl needs paid "Enhanced/Stealth" mode (5 credits per page) for sites protected by Cloudflare-type bot defences. — [eesel](https://www.eesel.ai/blog/firecrawl-pricing)
- Cloudflare's default AI-crawler blocking (from 2026-09-15) targets Training, Agent and mixed-use crawlers on ad-carrying pages. — [chudi.dev](https://chudi.dev/blog/cloudflare-block-ai-crawlers-september-15)
- Search-API cost and benchmark claims for Exa/Tavily/Brave/Parallel exist; one vendor (Parallel) published a BrowseComp comparison of 6 search APIs (vendor-authored, not read). — [Parallel](https://parallel.ai/articles/best-ai-search-for-agents.md)
- Browser Use: cloud agent versions V2-V4; vendor reports V4 76% on its own difficult-task set, +9 points over V3 and +22 over V2. — [Browser Use docs](https://docs.browser-use.com/cloud/choosing-an-agent)
- WebVoyager-style scores overstate reliability; use human-evaluated sets such as Online-Mind2Web. — [arXiv 2504.01382](https://arxiv.org/pdf/2504.01382)

### Inferences
- Likely stack for a founder: Overture/OSM extract (seed) + search API (Brave/Exa) for the website/profile URL + Crawl4AI/Playwright fetch + Haiku/Sonnet-class extraction with JSON schema + Pelias geocode + libphonenumber and line-type lookup. LangGraph or a plain queue is adequate orchestration; per-record jobs are embarrassingly parallel and need no multi-hour agent loop.
- Licence note: AGPL-3.0 Firecrawl self-hosting is fine for internal use, but modifying and offering it as a network service triggers source-sharing obligations; Crawl4AI (Apache-2.0) avoids that.
- Scraping Google Maps/Facebook/Instagram is the highest-yield source for small shops without websites, but also the one most likely to violate terms of service and be blocked; I did not research legal position (outside scope).

### Gaps
- Licences and maturity for Browser Use (open-source library), Playwright, Scrapy, LangGraph, Apify actors, Exa, Perplexity API, Claude/OpenAI web-search and computer-use tools, Common Crawl not verified in this pass (only Crawl4AI, Firecrawl, Pelias, Nominatim, Overture covered).
- No quantitative failure-rate data for blocking by site type or region.
- Legal/ToS and robots.txt position of agent crawling not researched.

## 4. Verification: how to check agent-collected entries and how much human checking is needed

### Takeaway
Cheap automated checks (cross-source agreement, verbatim-evidence match, website liveness, phone format and line-type lookup, geocode-vs-address consistency, Overture-style confidence scoring) can screen most records, but they verify consistency, not truth; true verification (phone call, owner claim code, field visit, street imagery) costs more per record, so use statistical sampling to estimate residual error.

### Cited Findings
- Overture uses a confidence score built from multiple signals, refreshed weekly, and is adding street-level imagery to confirm place existence and improve location; accuracy rose from 81.2% (>=0.6) to 95% (>=0.9). — [Overture Summit 2026 deck](https://hosted-files.sched.co/overturesummit2026/39/Places%20Surge%20Headliner.pdf) (via search summary)
- Foursquare's closed-business model identified ~700k newly closed US restaurants and improved precision/recall ~20% in the US, i.e. a model-based closure signal works at scale. — [Foursquare blog](https://foursquare.com/resources/blog/news/fsq-places-introducing-our-improved-closed-model)
- Twilio Lookup Line Type Intelligence ($0.008) distinguishes mobile, landline, fixed VoIP, non-fixed VoIP, toll-free; it validates the number's type and carrier but does not confirm the business owns it. — [Twilio Lookup pricing](https://www.twilio.com/en-us/lookup/pricing)
- ZeroBounce email verification costs ~$0.0065-$0.02 per address; confirms deliverability, not ownership. — [tlinky](https://tlinky.com/zerobounce-review/)
- LLM judges and annotators are "unreliable as independent annotators"; humans shown model suggestions show anchoring/automation bias; the ACT approach has the LLM flag the most suspicious items for human review. — [Hands-on tutorial arXiv 2411.04637](https://arxiv.org/html/2411.04637v3); [ACT, NeurIPS 2025](https://neurips.cc/virtual/2025/poster/117727)
- WebVoyager's LLM-as-judge agreement with humans is low, so automated verification of agent output by another LLM should itself be audited. — [arXiv 2504.01382](https://arxiv.org/pdf/2504.01382)
- Owner claim by WhatsApp/SMS code and phone-call verification: no cost or effectiveness data found for these in the sources reached.

### Inferences
- Layered scheme (estimate of design, not published evidence): (1) require evidence quote and source URL per field; (2) two independent sources agreeing on name+phone or name+address raises confidence; (3) website liveness and phone line-type check; (4) geocode and compare to address, flag mismatch with Overture/OSM point beyond ~100-200 m; (5) LLM-judge second pass; (6) route low-confidence and disagreement cases to humans; (7) random audit of auto-accepted records.
- Sample sizes (standard binomial calculation, not from a source): to estimate a batch's error rate to +/-5 percentage points at 95% confidence needs ~385 audited records; +/-2 points needs ~2,400; +/-1 point ~9,600 (worst-case p=0.5; fewer when error rate is small). Audit per country/category/language stratum, since error varies strongly by region.
- Owner-claim by code to a listed phone number is both verification and a freshness mechanism; it costs one SMS/WhatsApp message (cents) and shifts review labour to owners, but only works for businesses that find and care about the directory.

### Gaps
- No empirical study giving "x% human review yields y% precision" for business directories; the figures above are generic statistics, not domain evidence.
- Cost and response rates for phone-call or WhatsApp verification not found; WhatsApp Business messaging prices not researched.

## 5. Freshness: staleness and closure rates; how agents can maintain data

### Takeaway
Small-business data goes stale quickly: general business-population closure is ~7-9% per year, concentrated retail/food/service sectors ~11% in one market, and vendors cite ~20% of new businesses closing within a year and up to ~22% annual decay of small-business records. Maintenance means continuous re-verification, so refresh cost recurs every cycle.

### Cited Findings
- SBA (2018) reported ~7-9% of all US businesses closed per year since 1990; one market analysis put the six small-business-heavy sectors (manufacturing, wholesale, retail, food service, accommodation, services) at 11.08% closure and the overall rate at 8.64% (from 9.04%); "by some estimates" 20% of new businesses close within a year. — [Infobel / SafeGraph / SBA summaries via search](https://www.infobelpro.com/en/blog/data-decay-why-it-matters-across-business-consumer-and-poi-data); [Herald Corp](https://biz.heraldcorp.com/article/10792649)
- Vendor claim that small-business data decays up to 22% every year (marketing source, primary study not identified). — [Enigma](https://enigma.io/resources/blog/how-data-decay-can-spoil-your-small-business-database); [Moorfields](https://moorfieldscr.com/media-centre/business-insights/smes-struggle-with-business-data-decay)
- POI datasets updated only annually or quarterly decay as businesses relocate, change addresses, new construction occurs. — [SafeGraph](https://www.safegraph.com/blog/the-importance-of-reliable-accurate-and-timely-open-and-close-metadata-for-pois)
- Overture refreshes confidence signals weekly; Foursquare uses models to detect closures. — [Overture Summit 2026 deck](https://hosted-files.sched.co/overturesummit2026/39/Places%20Surge%20Headliner.pdf); [Foursquare blog](https://foursquare.com/resources/blog/news/fsq-places-introducing-our-improved-closed-model)

### Inferences
- If 8-11% of businesses close per year and more change phone/hours/address, a directory without maintenance falls to roughly 80-90% existence accuracy after one year (simple arithmetic from the cited closure rate, excluding field changes), and phone/hours fields decay faster.
- Tiered refresh (estimate): re-crawl high-traffic or high-churn categories (restaurants, retail) every 3-6 months, others yearly; use cheap signals (website HTTP status, domain expiry, Google/OSM change feeds, owner-claim pings) to trigger deeper agent re-checks. Refresh cost per cycle equals roughly the verification-only cost per record, so annual refresh multiplies the per-million figures in section 2 by cycles per year.
- Closure rates by category (e.g. restaurants vs pharmacies) from a primary dataset: not obtained.

### Gaps
- Category-specific closure and field-change rates from primary sources (e.g. Yelp/Google/Foursquare studies) not found; figures are US-centric and from secondary summaries.
- No data for non-US countries.

## 6. Coverage limits: languages, scripts, informal businesses, where agents cannot find data

### Takeaway
Agents can only find what has a web footprint. Informal shops with no website, social page or map listing are invisible to web research, and LLM performance is lower in low-resource languages and scripts, so coverage will be sharply uneven by region.

### Cited Findings
- OSM contributions are heavily biased to the Global North; completeness varies 7-81% for shops in Canada and 42-100% by district in Germany, so many Global South places are likely far less mapped (no direct Global South POI figure found). — [SotM 2022](https://2022.stateofthemap.org/sessions/GPMSLW/); [AGILE-GISS 2021](https://agile-giss.copernicus.org/articles/2/20/2021/agile-giss-2-20-2021.pdf)
- Google Maps lets businesses list address, hours, phone and photo with no website; but Street View covers only 13 African countries, little of Central America, Asia and the Middle East; informal settlements and unnamed streets complicate addressing; Sri Lanka cited as having minimal Google Maps data. — [Google Maps Kenya launch, Geospatial World](https://geospatialworld.net/news/google-maps-launched-in-kenya); [ArchDaily](https://www.archdaily.com/983526/whatsapp:/send); [Univ. of Moratuwa](https://dl.lib.uom.lk/items/04250010-1c47-49d9-a6c2-492a73030a4e)
- Language gap: GPT-4 scored F1 89.1% in English vs 76.4% in Urdu on question answering (UQuAD1.0 vs SQuAD2.0); UrduMMLU (26,431 questions) shows significant performance disparities across 30 models; X-WebAgentBench shows even GPT-4o with cross-lingual techniques fails to reach satisfactory results on multilingual web-agent tasks. — [Urdu NLP benchmark arXiv 2405.15453](https://arxiv.org/html/2405.15453v1); [UrduMMLU](https://themodelwire.com/article/urdummlu-a-massive-multitask-benchmark-for-urdu-language-understanding-01KTJH9K6B51TXV4ATAXBMA2SQ); [X-WebAgentBench via arXiv 2502.16961](https://arxiv.org/abs/2502.16961v1)
- No data found on Hindi, Chinese, Cyrillic or Arabic business-extraction accuracy, nor transliteration/geocoding accuracy for Arabic- or Urdu-script addresses.

### Inferences
- Expect coverage to be strongest where business listings, delivery apps, Facebook/Instagram pages and Google Maps are widely used, and weakest for neighbourhood shops, markets, home businesses and rural places. For those, the data source is people on the ground (owners, community contributors, field surveys), not web agents.
- Cross-script matching (the same shop spelled in Urdu script, Latin transliteration and English) is a likely entity-resolution failure mode; the 13-point English-Urdu gap in one QA task hints at the order of degradation, not a direct measure for this task.
- Countries where messaging apps (WhatsApp, Telegram, WeChat, LINE) hold the business presence are partly or fully outside crawlable web; agents there need platform-specific access that is often against terms of service.

### Gaps
- No quantitative estimate of the share of small shops with any web presence by country.
- No evidence on Chinese platform data (Baidu/Amap/Dianping), Indian (Justdial) or Arabic-region coverage by agents.
- Street-level geocoding quality for non-Latin addresses not found.

## 7. Human-in-the-loop: agents draft, humans verify

### Takeaway
Evidence from annotation research supports "LLM drafts, humans review the uncertain subset" as a large cost saver (reported 50-96% in classification-type labelling), but humans reviewing LLM suggestions are subject to anchoring and do not necessarily go faster, and no study I found measures this for business-directory records.

### Cited Findings
- Confidence-selective review (humans relabel only lowest-confidence items) reported 50-96% cost reductions in labelling tasks; industry claims of up to 50% lower cost versus manual-only. — [Toloka](https://toloka.ai/blog/llms-and-humans-for-data-labeling/); [RiseUp Labs](https://riseuplabs.com/what-is-ai-assisted-data-labeling/)
- Presenting LLM-generated labels raises annotator confidence but not speed, and creates anchoring bias; LLMs are effective assistants but unreliable independent annotators. — [Hands-on tutorial arXiv 2411.04637](https://arxiv.org/html/2411.04637v3); [MEGAnno+](https://arxiv.org/html/2402.18050v1)
- ACT pipeline: LLM annotates and also judges, humans review only the most suspicious cases. — [NeurIPS 2025 poster](https://neurips.cc/virtual/2025/poster/117727)
- Double Triangle Annotation (arXiv 2605.25781, 2026) proposes a scalable human-in-the-loop framework for high-precision document annotation (details not read). — [arXiv 2605.25781](https://arxiv.org/pdf/2605.25781)

### Inferences
- Suggested design (estimate, not measured): agents produce a draft with field-level evidence and confidence; auto-accept only high-confidence multi-source agreement; humans (local-language, ideally local residents) review low-confidence and disagreement cases blind to the model's answer where feasible (to limit anchoring), plus a random audit of auto-accepted records to measure real precision per region; owner claims later replace human review for high-value listings.
- Human cost is most efficient when concentrated on local knowledge tasks agents cannot do (is this shop real, is the phone answered, correct local-script spelling, closing status), not on re-doing web lookups.
- Local volunteers or paid local micro-taskers are the only route for informal shops; web agents then help only with deduplication, geocoding and formatting.

### Gaps
- No study comparing cost and quality of fully manual vs agent-draft vs fully automatic collection for business listings.
- No cost data for local-language crowd verification by country.
- Whether Yelp, Foursquare, Google Local Guides or Overture use human sampling audits and what rates they use: not found.

## 8. Overall feasibility judgment for "agents fill every list in every region"

### Takeaway
Feasible at modest cost for discovery and enrichment of businesses that already have a web or map presence (est. tens of thousands of dollars per million records for automation, before human review), but not for the full long tail: informal and offline businesses, low-resource languages, and fields like opening hours and size cannot be verified from the web alone, and unmaintained data decays by roughly a tenth or more per year.

### Cited Findings
- See sections 1-7; key anchors: Overture 95% accuracy only at confidence >=0.9 (81.2% at >=0.6); LLM extraction F1 ~0.957 on pages that contain the data; business closure ~7-11% per year; agent success degrades with task length; Cloudflare blocking agents by default from 2026-09-15.

### Inferences
- A defensible plan: seed from Overture/OSM, enrich with short per-record agent jobs, verify with automated checks plus stratified human audits, publish confidence/last-verified dates, let owners claim and correct, and budget recurring refresh. Treat "every list in every region" as a staged rollout by region and language, measured by audit-based precision, not a single global run.
- Opening hours and size are the least supported fields: no accuracy evidence was found, and they are often absent from web pages. Consider making them optional or owner-supplied.

### Gaps
- Entire evidence base is secondary (search summaries) because primary pages were blocked; numbers should be re-verified before external use.
- No direct measurement of an agent-populated directory exists in what I found; the largest uncertainty is real-world precision of agent-collected phone and address data by region.
