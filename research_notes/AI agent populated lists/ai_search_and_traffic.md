# How AI is changing search traffic and web discovery: implications for a new directory site (notes as of 2026-10-05)

Method caveat: WebFetch was blocked by the egress proxy for pewresearch.org, ahrefs.com, seranking.com, sec.gov and digitalapplied.com. Every figure below therefore comes from WebSearch result summaries and not from reading the primary page. Where a primary study is cited through an aggregator or trade site, this is flagged. Several 2026 items come from low-authority blogs or vendor posts and are marked "unverified". Nothing here has been checked against the original filings or studies.

## 1. Zero-click and AI answers: evidence on click-through rates (Google AI Overviews/AI Mode, ChatGPT, Perplexity, Copilot)

### Takeaway
Independent datasets agree that AI Overviews (AIOs) reduce clicks to organic results, with estimates from about 35% to about 60% lower CTR for the top result. Google says total click volume is "relatively stable" and publishes no data to support that. Being cited inside the AI answer is associated with materially higher CTR than not being cited.

### Cited Findings
- Pew Research (900 US adults, 68,879 Google searches, browsing data from April 7-17, 2025): users clicked a traditional result in 8% of visits when an AI summary appeared versus 15% when none appeared. They clicked a link inside the AI summary in about 1% of visits. They ended the browsing session after 26% of AI-summary pages versus 16% of traditional pages. The finding is described as directional. Pewresearch.org could not be fetched, so this is via an aggregator. — [AI Weekly summary of Pew](https://aiweekly.co/alerts/pew-ai-summaries-cut-google-click-throughs-to-8-from-15)
- Ahrefs (first study, 300,000 keywords, March 2024 vs March 2025): an AIO was associated with a 34.5% lower average CTR for the top-ranking page versus similar informational keywords with no AIO. For AIO keywords, position-1 CTR fell from 0.073 to 0.026. — [Ahrefs blog via search result](https://ahrefs.com/blog/ai-overviews-reduce-clicks/) and [EngageWeb summary](https://www.engageweb.co.uk/blog/study-finds-ai-overviews-decrease-clicks-by-34-5)
- Ahrefs (updated study, December 2023 to December 2025): the AIO-associated drop in top-page CTR is now reported as 58%, with position-1 CTR for AIO keywords falling from 0.073 to 0.016. This figure comes from search-result text and a press-release syndication; the original page was not read. — [Ahrefs update](https://ahrefs.com/blog/ai-overviews-reduce-clicks-update/?pp=iaqb); [syndicated release dated 2026-05-19](https://stocks.observer-reporter.com/observerreporter/article/bizwire-2026-5-19-new-research-googles-ai-overviews-now-cost-websites-58-of-their-clicks)
- Seer Interactive (3,119 informational queries, 42 client organisations, 25.1M organic impressions, June 2024 to September 2025): organic CTR on AIO queries fell from 1.76% to 0.61%. Paid CTR fell from 19.7% to 6.34%. Brands cited in the AIO got 1.2% organic CTR and 11.05% paid CTR, versus 0.52% and 4.14% when not cited. — [Seer Interactive study](https://seerinteractive.com/insights/aio-impact-on-google-ctr-september-2025-update); [PPC Land summary](https://ppc.land/google-ai-overviews-reduce-organic-ctr-61-paid-traffic-68/)
- Similarweb: zero-click share of news-related searches rose from 56% to 69% between May 2024 and May 2025. Organic visits to news sites fell from a peak above 2.3 billion (mid-2024) to under 1.7 billion (May 2025). Note that this covers news searches, not directories. — [Search Engine Roundtable](https://www.seroundtable.com/similarweb-google-zero-click-search-growth-39706.html)
- Google's position: Liz Reid (VP, Head of Search) has said "total organic click volume from Google Search to websites has been relatively stable year-over-year" and that "quality clicks" (users who do not quickly click back) are slightly up. Reid has repeated this in later appearances without supporting figures. — [TechWyse on Reid/Bloomberg](https://www.techwyse.com/news/search-news/google-liz-reid-bounce-clicks-ai-overviews-traffic-data); [TechCrunch 2025-08-06](https://techcrunch.com/2025/08/06/google-denies-ai-search-features-are-killing-website-traffic/)
- A randomized field experiment found a 39.8% decrease in organic clicks when AIOs are shown. It found no significant difference in click-quality measures (time on site, quick return to results). I could not identify the authors or venue from the snippet, so treat this as unverified. — [summary in a search snippet, Jamie McKaye post](https://jamiemckaye.com/bounce-click-defence-google-measurement-problem/)
- AIO prevalence: roughly 43-48% of Google queries per Similarweb/Semrush-based reporting. BrightEdge measured about 48% in February 2026, and Conductor measured 25.11% across 21.9M searches. The two vendor datasets disagree because their methods differ. — [Relevant Audience roundup](https://www.relevantaudience.com/geo/ai-overviews-half-of-google-queries/)
- AIO query-intent mix is shifting: informational queries were 91.3% of AIO triggers in January 2025 and 57.1% by October 2025, while navigational AIOs rose from 0.74% to 10.33% (secondary roundup, unverified). — [SLT Creative stats roundup](https://sltcreative.com/ai-seo-statistics)
- Local and directory queries: Whitespark and related studies report AIOs on 68% of local searches overall. Informational local queries get an AIO about 92% of the time with a Local Pack only about 6% of the time. For "trade plus town" queries, the map pack still appears about 90%+ of the time and AIOs only about 15%. — [Whitespark case study](https://whitespark.ca/blog/case-study-the-prevalence-of-ai-overviews-in-local-search/); [Search Engine Journal](https://www.searchenginejournal.com/ai-overviews-now-answer-most-local-searches-how-to-get-your-business-cited/); [Whito UK summary](https://whito.co.uk/research/uk-local-search-data/). The 68% and 15% figures are not reconciled across sources.
- Tripadvisor attributes revenue decline to Google AIO erosion of organic traffic (see section 3).

### Inferences
- The studies measure different things (position-1 CTR, all-organic CTR, session endings). The consistent direction is a click drop when an AIO is present, and the range is wide. A planning assumption of roughly 30-60% fewer organic clicks on informational queries that trigger an AIO is supported. Navigational and "trade plus town" queries with map packs are less exposed.
- Citation inside the AIO is associated with about 2x organic CTR (Seer), but this is correlation, and cited brands are likely already stronger.
- A directory built on informational "what/best/how" pages is the most exposed type. Pages that match the transactional "service plus place" pattern, where the map pack dominates, face competition from Google Business Profile instead of from AIOs.

### Gaps
- I found no data on Perplexity, Copilot or ChatGPT click-through rates to cited sources. Referral volumes are in section 2.
- No primary data on AI Mode CTR specifically, only AIO studies.
- Google's own "stable clicks" claim has no published numbers.
- Pew, Ahrefs, Seer and Similarweb primary pages were not read. Figures rely on search-result text.

## 2. Referral traffic from AI assistants, how AI picks sources, and GEO evidence

### Takeaway
AI referral traffic is growing fast from a tiny base (about 0.3% of all website traffic in 2026), with ChatGPT supplying about three quarters of it. Conversion quality estimates range from about 2x to 23x organic, depending on methodology. Evidence on what makes content get cited is thin. The one academic study (Princeton GEO) found that statistics, quotations and source citations help, and keyword stuffing does not.

### Cited Findings
- SE Ranking (2026 study, sample size not confirmed): AI platforms account for 0.32% of all website traffic in 2026, versus 0.24% in 2025 and 0.02% in 2024, which they call 16x growth. Within AI referrals, ChatGPT was 74.78%, Gemini 11.56%, Perplexity 7.23%, Copilot 3.51% and Claude 2.62%. ChatGPT's share fell from 79.74% in 2025 even though its traffic grew about 27% year over year. — [SE Ranking study via search result](https://seranking.com/blog/ai-traffic-research-study/)
- A different study reported ChatGPT sending 92.4% of measurable LLM referral traffic, so share depends heavily on how referrers are classified. — [SEO-Day](https://www.seo-day.de/news/article/chatgpt-commands-92-of-ai-referral-traffic-heres-what-677?lang=en)
- Conversion: Ahrefs (June 2025, one B2B SaaS site) found AI search was 0.5% of traffic but 12.1% of signups, which they call 23x. Semrush (2026) reports AI visitors 4.4x as valuable as organic. Similarweb (2026) reports 11.4% versus 5.3% conversion (2.15x). The differences come from methodology and sample (one site versus cross-industry versus panel). These come through secondary writeups. — [PPC Land on Ahrefs](https://ppc.land/ahrefs-study-finds-ai-search-visitors-convert-23x-higher-than-organic-traffic/); [Ecorpit comparison](https://ecorpit.com/ai-search-conversion-rate-23x-studies-geo-budget-2026/)
- Zillow (Q1 2026 call, company claim): consumers using Zillow's AI mode spend more than 3x as long, view more than 2x as many homes and contact an agent at nearly 3x the rate. This is on-platform behaviour, not external AI referral. — [RISMedia Q1 2026 recap](https://ace.rismedia.com/2026/05/07/zillow-q1-2026-earnings-call-recap/)
- Source selection for local queries in ChatGPT: BrightLocal found business websites were 58% of sources, business mentions 27% and directories 15%. In one study Yelp appeared in 80% of local answers, and Tripadvisor had 10,227 citations. A UK study found Reddit the most-cited source (10 of 18 answers) with Yell, Yelp and Facebook cited zero times. Results conflict by country, query type and date. — [BrightLocal ChatGPT sources](https://www.brightlocal.com/research/uncovering-chatgpt-search-sources/); [BrightLocal directory sources](https://www.brightlocal.com/resources/ai-directory-sources/); [Whito UK AI citation study](https://whito.co.uk/research/ai-citation-sources-uk-study/)
- BrightLocal LCRS 2026: share of consumers using AI tools such as ChatGPT to find or evaluate local businesses rose from 6% to 45% in one year, making AI the third most-used route after Google and Facebook. Treat as a survey claim. Also: only about 35% of small businesses have a Google Business Profile. — [Search Engine Journal local AI](https://www.searchenginejournal.com/ai-overviews-now-answer-most-local-searches-how-to-get-your-business-cited/)
- Princeton GEO paper (arXiv 2311.09735, 10,000 queries, nine methods): adding statistics, quotations and cited sources raised visibility in generative-engine answers by up to about 40%, and lower-ranked sites gained up to 115% for some methods. Keyword stuffing gave near-zero or negative results, and an authoritative tone did not help. This tested a research generative engine and not Google or ChatGPT in production. — [arXiv GEO paper](https://ar5iv.labs.arxiv.org/html/2311.09735)
- llms.txt: Originality.ai counted 4,088 files (June 2025) rising to 36,120 (May 2026) across 3M+ sites. Ahrefs server-log data on 137,000 domains found 97% of llms.txt files got zero requests in May 2026. Google says it does not use llms.txt, and OpenAI, Anthropic and Meta have not adopted it (per ppc.land summary). — [PPC Land adoption](https://ppc.land/llms-txt-adoption-rises-8-8x-but-97-of-files-get-zero-ai-requests/); [PPC Land stall](https://ppc.land/llms-txt-adoption-stalls-as-major-ai-platforms-ignore-proposed-standard/)
- A claim that "schema.org LocalBusiness markup increases AI citation" was not found in any solid source in my searches. No reliable controlled evidence.

### Inferences
- AI referrals are a small channel for a new site (well under 1% of traffic for the average site), but higher-intent. They matter more as a brand and citation channel than as raw volume.
- Evidence favours information-rich pages: statistics, named sources, structured facts. That fits a data-rich directory. Structured data and llms.txt are cheap, but the evidence they cause citation is weak to absent.
- Which directories get cited varies by country and query. Do not assume Yelp-style dominance outside the US.

### Gaps
- No reliable evidence on how Gemini, Claude or Perplexity weigh schema.org or freshness.
- Sample sizes and methodology for SE Ranking, Semrush and Similarweb AI-traffic studies not confirmed.
- No emerging-market AI referral data found.

## 3. Effects on directory and review sites, investor statements, and licensing

### Takeaway
Results are mixed. Tripadvisor, Stack Overflow, Wikipedia and Zillow report traffic erosion linked to AI. Yelp reports stable or improving traffic and monetises through an OpenAI licensing deal. The sites that fare best are US-centric incumbents with logged-in users, apps and brand search.

### Cited Findings
- Yelp: Q2 2026 (reported 2026-08-06) shows year-over-year improvements in app installs and page views. Management says Google algorithm changes favouring user-generated content were a tailwind for organic search. CEO Jeremy Stoppelman said Yelp ratings and reviews have begun "powering ChatGPT's local experience." H1 2026 net revenue was $737.0M, up 1%. — [Yelp Q2 2026 press release (BusinessWire)](https://secure.businesswire.com/news/home/20260806543061/en/Yelp-Reports-Second-Quarter-2026-Results); [Yelp Q2 2026 call transcript (Webull)](https://www.webull.com/news/15397963795538944); [Yelp 10-Q FY2026](https://www.sec.gov/Archives/edgar/data/0001345016/000134501626000066/yelp-20260630.htm) (not read)
- Yelp-OpenAI deal (Axios exclusive, 2026-07-23): ChatGPT gets Yelp reviews, ratings, photos and business details for local queries, with Yelp branding and links. Reported scale is 330M cumulative reviews and 8M+ business listings. Financial terms undisclosed, non-exclusive, and Yelp plans to bring its Request-a-Quote feature into ChatGPT. Yelp already supplies data to Apple Maps and Yahoo. Yelp's 2025 net revenue was $1.46B and "other revenue" (including data licensing) grew 17%. — [Axios](https://axios.com/2026/07/23/yelp-reviews-chatgpt-geo-partnership); [Search Engine Land](https://searchengineland.com/openai-yelp-deal-483326); [TechWyse](https://www.techwyse.com/news/platform-updates/yelp-openai-licensing-deal-chatgpt-local-reviews)
- Tripadvisor: February 2026 reporting says AI Overviews and other search changes are cutting "flyby" traffic, and the company again explored strategic alternatives. The CFO said under 10% of Experiences gross booking volume is expected to come from free organic search by end of 2026. Q2 2026 (August) revenue was $441.9M (down about 7%). "Hotels and Other" fell from $208M to $163.3M, which is attributed to AIO effects on organic traffic (commentary from a secondary source). — [Skift 2026-02-12](https://skift.com/2026/02/12/tripadvisor-sees-traffic-decline-from-ai-overviews-considers-strategic-alternatives-again/); [Webull Q2 2026](https://www.webull.com/news/15417915579606016); [Travelers Today](https://www.travelerstoday.com/articles/60777/20260807/tripadvisors-hotel-search-falls-21-percent-while-viator-keeps-growing.htm)
- Zillow: Q1 2026 traffic to apps and sites fell 3% year over year to 220M average monthly unique users, a third consecutive quarter of decline. Q2 2026 traffic fell 2%. Revenue grew 18% to $708M in Q1. — [RISMedia](https://ace.rismedia.com/2026/05/07/zillow-q1-2026-earnings-call-recap/); [Real Estate News](https://www.realestatenews.com/2026/08/05/zillow-beats-q2-forecasts-with-18-spike-in-revenue); [Online Marketplaces](https://www.onlinemarketplaces.com/articles/zillow-q1-2026-revenue-up-18-but-q2-outlook-drags-shares-lower/)
- Wikipedia: Wikimedia Foundation reported human pageviews down roughly 8% year over year after reclassifying bot traffic (data to August 2025). Marshall Miller attributes this to AI search and social video, with Wikipedia content used in answers. — [Search Engine Journal](https://www.searchenginejournal.com/wikipedia-traffic-down-as-ai-answers-rise/558803/); [Storyboard18](https://www.storyboard18.com/amp/digital/wikipedia-reports-8-fall-in-human-traffic-amid-rise-of-ai-search-and-social-video-82806.htm)
- Stack Overflow: question volume has collapsed. Sources disagree on figures (a 75% drop from 2014 to late 2025, versus claims of about 3,862 questions in December 2024, versus a KuCoin item claiming 1,304 in July 2026 and a 99% drop from 2014). The 1,304 figure is unverified, from a crypto news site, and inconsistent with the other sources. Decline began about 2020 and accelerated after ChatGPT (November 2022). — [Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/are-llms-making-stackoverflow-irrelevant); [Eden AI](https://www.edenai.co/post/what-ai-did-to-stack-overflow-and-what-replaces-developer); [KuCoin (unverified)](https://www.kucoin.com/news/flash/stack-overflow-s-monthly-questions-drop-to-1-304-in-july-2026-down-99-from-2014)
- Reddit: Google licence about $60M per year (signed February 2024) and OpenAI about $70M per year (May 2024), both reported as up for renewal in 2026, with Reddit reportedly seeking usage-based fees because AIOs cut referral traffic. Wells Fargo estimate of about $550M combined after renegotiation versus about $130M now. Renewal status is from press reports and not confirmed. — [Search Engine Land](https://searchengineland.com/reddit-google-ai-content-licensing-deal-437782); [The Decoder](https://the-decoder.com/reddit-signs-60-million-annual-training-data-deal-with-google/); [AI Weekly](https://aiweekly.co/alerts/reddit-weighs-cutting-google-ai-access-as-60m-deal-expires); [TIKR](https://www.tikr.com/blog/reddit-stock-fell-8-in-a-day-on-a-google-licensing-report-heres-where-the-stock-could-go-in-2026)

### Inferences
- Logged-in, app-heavy and brand-search-heavy sites (Yelp, Zillow) are more resilient than sites living on informational generic queries (Tripadvisor "flyby", Stack Overflow, Wikipedia). A new directory has no brand or app, so it resembles the exposed group.
- The deals that pay (Reddit, Yelp) involve sites with hundreds of millions of items and massive proprietary or user-generated corpora. They are not a template for a startup.

### Gaps
- Not found: Glassdoor (Recruit Holdings), Quora, and Yellow Pages-type sites (Yellow Pages Group, Thryv, Yell). The search returned nothing usable for Glassdoor.
- No verified Yelp organic traffic percentages. SEC pages were not readable.
- Licensing fees for Yelp-OpenAI, Stack Overflow, Shutterstock and news publishers were not retrieved.

## 4. Opportunity: data licensing, pay-per-crawl, llms.txt, MCP and agentic commerce

### Takeaway
Licensing money is concentrated in very large corpora. For a small directory the realistic AI-era routes are being cited, offering a structured API or MCP server, and joining marketplace-style micropayment schemes. All of those are early and unproven. Cloudflare's pay-per-crawl is live but is being redesigned toward pay-per-use.

### Cited Findings
- Cloudflare pay-per-crawl: introduced July 1, 2025 in private beta. Publishers can allow, charge or block crawlers, with charged requests receiving HTTP 402 "Payment Required." Payment uses the x402 protocol with stablecoins. Cloudflare reports more than 1 billion 402 responses per day. Early adopters named include Condé Nast, Time, AP, BuzzFeed, Reddit, Pinterest and Stack Overflow. On July 1, 2026 Cloudflare proposed shifting to "pay per use," paying publishers when content appears in an answer. — [PPC Land on Cloudflare pay per use](https://ppc.land/cloudflare-stops-charging-ai-per-crawl-and-starts-paying-per-answer/); [Leadgen Economy](https://www.leadgen-economy.com/blog/cloudflare-ai-crawl-control-publisher-economics/); [eWeek](https://www.eweek.com/de/news/cloudflare-expands-ai-crawler-control/). Secondary sources only, no figures on payments actually made were found.
- Crawl-to-referral imbalance (Cloudflare Radar): in 2025 Google about 9.4:1, OpenAI about 1,600:1, Anthropic about 70,900:1. A Q1 2026 analysis of Cloudflare Radar data reports Googlebot about 5:1, OpenAI about 1,300:1 and Anthropic about 24,000:1. — [PPC Land](https://ppc.land/cloudflare-exposes-ai-crawlers-hitting-sites-50000-times-per-visitor/); [Digital Applied (August 2026, not fetched)](https://www.digitalapplied.com/blog/ai-crawl-economics-pay-per-crawl-referral-data-2026)
- MCP (Model Context Protocol, Anthropic, November 2024) is described as supported across Claude, ChatGPT, Gemini and Copilot. Commerce vendors (Microsoft Dynamics 365, Zoovu, Logicbroker) are shipping MCP servers so agents can query catalogues, inventory and prices. I found nothing specific on a directory-style MCP server making money. — [Microsoft Learn commerce MCP](https://learn.microsoft.com/en-us/dynamics365/commerce/commerce-mcp); [Zoovu release 2025-12-11](https://www.businesswire.com/news/home/20251211046138/en/Zoovu-Launches-MCP-Server-to-Give-AI-Agents-the-Product-Intelligence-Required-for-Agentic-Commerce)
- llms.txt: see section 2. It has no demonstrated benefit.
- Yelp's Request-a-Quote inside ChatGPT is a concrete example of an AI-native lead channel, from the deal described in section 3.

### Inferences
- A small directory cannot expect licence revenue. Possible value is in being a cleaner, fresher, structured source in a niche or region that big sources cover badly.
- An MCP server or open API is cheap to build and fits the "AI agent populated lists" theme, but demand and payment are unproven.

### Gaps
- Not retrieved: Stack Overflow, Shutterstock and news-publisher licensing amounts and terms; Google's agent-payments protocol and ChatGPT Instant Checkout details (the search returned nothing); evidence of any small-site licensing deal.
- No evidence found that "verified local data" is bought by AI shopping systems.

## 5. Local search: Google Business Profile, Apple, Bing, Meta, and how a new directory earns visibility

### Takeaway
Local intent queries still resolve mostly through map packs, and Google Business Profile (GBP) is the core data source. AI assistants are becoming a third route for consumers. Evidence on exact "share of local queries ending in Maps" was not found.

### Cited Findings
- Map packs still appear on about 90%+ of "trade plus town" queries and AIOs on about 15% of them. Informational local queries are the opposite, with AIOs on about 92% and a Local Pack about 6%. — [Whitespark](https://whitespark.ca/blog/case-study-the-prevalence-of-ai-overviews-in-local-search/); [Search Engine Journal](https://www.searchenginejournal.com/ai-overviews-now-answer-most-local-searches-how-to-get-your-business-cited/)
- GBP signals are roughly a third of local-pack ranking weight, per the BrightLocal/Whitespark-based summary. — [Search Engine Journal](https://www.searchenginejournal.com/ai-overviews-now-answer-most-local-searches-how-to-get-your-business-cited/)
- BrightLocal: 45% of consumers used AI tools for local business discovery (up from 6%), third after Google and Facebook. 74% ignore reviews older than three months. — [Search Engine Journal](https://www.searchenginejournal.com/ai-overviews-now-answer-most-local-searches-how-to-get-your-business-cited/)
- Yelp already supplies data to Apple Maps and Yahoo, a sign that Apple and others buy review and listing data. — [Search Engine Land](https://searchengineland.com/openai-yelp-deal-483326)
- Google's spam policies treat scaled low-value pages as scaled content abuse, and this was a major focus of the March 2026 spam update. Programmatic pages are acceptable if each answers a distinct need with material beyond template substitution. There were also June and August 2026 spam updates (June's coverage was about home services). — [Bulkbase on scaled content abuse](https://bulkbase.ai/seo/scaled-content-abuse-googles-policy-enforcement-how-to-stay-compliant-in-2026); [Digital Shift Media on June 2026](https://digitalshiftmedia.com/search-intelligence/google-june-2026-spam-update-home-services/); [Vizup on August 2026](https://www.tryvizup.com/blog/august-spam-update)

### Inferences
- A directory cannot rank in the Maps pack without being the business. Its local visibility comes from organic listings below the pack and from being cited in AI answers.
- A mass-generated directory is at policy risk unless each page carries distinct verified data.

### Gaps
- No data found on Apple Business Connect, Bing Places or Meta local share.
- No source for the percentage of local queries ending in Maps clicks.
- Primary Google policy page was not read.

## 6. Alternative audience channels not dependent on Google

### Takeaway
Little hard evidence was retrieved. WhatsApp is building its own business directory, which is both a channel and a competitor in emerging markets.

### Cited Findings
- WhatsApp has tested and rolled out an in-app business directory (Discover > Businesses), first in São Paulo, Brazil, with reporting of availability in Brazil, Colombia, Indonesia, Mexico and the UK, and India and Indonesia flagged as next. Dates and scale not confirmed. — [Android Central](https://androidcentral.com/whatsapp-pilots-app-business-directory); [Geo TV](https://www.geo.tv/latest/370728-whatsapp-rollsout-new-business-directory-to-promote-e-commerce); [Man's World India](https://www.mansworldindia.com/tech/whatsapp-begins-testing-a-yellow-pages-style-business-directory)
- A third-party "DigiDirectory" project lists WhatsApp-enabled businesses in India, South Africa, Kenya, Malaysia and UAE, which shows demand for discovery layers on top of WhatsApp. This is a hobby project and not evidence of traffic. — [Peerlist](https://peerlist.io/galib/project/digidirectory)

### Inferences
- In emerging markets with WhatsApp-first commerce, a directory that exports to or links with WhatsApp may reach users Google does not.

### Gaps
- Nothing retrieved on TikTok, YouTube or Instagram search discovery share, Telegram, community outreach or marketplace channels, or emerging-market evidence with figures. Needs separate research.

## 7. Time and effort for a new domain to gain organic traffic at scale; examples

### Takeaway
Only anecdotal case studies were found. None are verified directory timelines at scale, and the Semrush "212% average" claim is not interpretable for a brand-new domain.

### Cited Findings
- OpenAlternative (programmatic directory) is described as reaching about 70,000 visitors per month, mostly organic, on pages generated from listing data. Timeline not given in the snippet. — [Dirstarter](https://dirstarter.com/blog/programmatic-seo-directory-websites)
- guiltychef.com (recipe directory) reportedly gets about 11,000 monthly organic visits from 160 pages. Self-reported. — [Dirstarter](https://dirstarter.com/blog/programmatic-seo-directory-websites)
- Flexafit (existing brand, not a new domain) reports organic traffic 4x within 6 months after launching 450+ programmatic pages. Vendor case study. — [SyncGTM](https://syncgtm.com/case-studies/flexafit)
- "Programmatic SEO boosts organic traffic 212% in the first year (Semrush 2025)" appears in a low-authority blog. Unverified, and it measures growth from an existing base. — [SGEO blog](https://www.sgeo.it.com/blog/seo-booster-sgeo-it-com/unlocking-growth-how-programmatic-seo-can-transform-your-content-strategy-in-2026)

### Inferences
- Indie-hacker directories in tech niches have reached tens of thousands of visits per month, but I found no verified timeline, and survivorship bias is likely. Google's scaled-content enforcement in 2026 raises the bar for thin directories.

### Gaps
- No verified case with dates for a new local or business directory reaching scale, and no data on the typical sandbox period. Needs a dedicated search (for example Ahrefs/Semrush case studies of Yelp-like or Yellow-Pages-like launches and country-specific directories).
