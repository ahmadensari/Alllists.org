# Google, search engines and AI-agent-populated directories (search-ranking risk and opportunity)

Research date: 2026-10-05. Method note: every primary-source domain I tried to fetch (developers.google.com, developers.google.cn, searchengineland.com, seroundtable.com, searchenginejournal.com, sistrix.com, ahrefs.com, web.archive.org) was blocked by the network proxy. All findings below therefore come from web-search result summaries (which quote or paraphrase those pages) and could not be checked against the full pages. Where a result came from a low-authority SEO blog (many 2026 "programmatic SEO is dead" posts), it is flagged as such. Treat all percentage figures from blogs as unverified.

## 1. What Google's written policies say (scaled content abuse, site reputation abuse, AI content, helpful content, 2025-2026 updates)

### Takeaway
Google penalises low-value mass production, not AI use as such. The March 2024 "scaled content abuse" policy applies "no matter" whether pages are made by automation, humans or both, and the test is whether many pages exist "for the primary purpose of manipulating Search rankings and not helping users". A directory of auto-collected pages is not banned in principle, but it is exactly the shape of site the policy was written to catch if pages are thin, unoriginal or near-duplicate.

### Cited Findings
- Policy definition (announced 5 March 2024; quoted via search results of Google's blog and Search Engine Land/SERoundtable): "Scaled content abuse is when many pages are generated for the primary purpose of manipulating Search rankings and not helping users. This abusive practice is typically focused on creating large amounts of unoriginal content that provides little to no value to users, no matter how it's created." — [Google Search Central blog, March 2024](https://developers.google.com/search/blog/2024/03/core-update-spam-policies) (full page not fetched; quote from search-result extract)
- Examples given in the policy include using generative AI tools to generate many pages without adding value, scraping feeds/search results, and stitching together content from different web pages without adding value (paraphrased in search extract: "using AI-generated text, scraping feeds, and pasting together content from other web pages") — [Google blog, Mar 2024](https://developers.google.com/search/blog/2024/03/core-update-spam-policies); also [Aspiration Marketing summary](https://blog.aspiration.marketing/en/googles-new-update-targets-low-quality-content)
- Method of creation is explicitly irrelevant: the policy lets Google "take action on scaled content abuse as needed, whether the content is produced through automation, human efforts, or some combination of human and automated processes", and it "builds on" the earlier "automatically generated content" spam policy — [Google blog, Mar 2024](https://developers.google.com/search/blog/2024/03/core-update-spam-policies); also reported at [SERoundtable, March 2024](https://www.seroundtable.com/google-march-2024-spam-updates-37002.html)
- Google's stated long-standing position (as paraphrased in the same search results): "use of automation, including generative AI, is spam if the primary purpose is manipulating ranking in Search results". The March 2024 text was framed as the same principle "expanded to account for more sophisticated scaled content creation methods where it isn't always clear whether low quality content was created purely through automation" — [Google blog, Mar 2024](https://developers.google.com/search/blog/2024/03/core-update-spam-policies)
- Google claimed the March 2024 core update plus spam policies would together reduce low-quality, unoriginal content in results by 40% (Google's own estimate; later reports cite 45% achieved) — [Google blog, Mar 2024](https://developers.google.com/search/blog/2024/03/core-update-spam-policies); "45%" cited in secondary source [Sistrix/pSEO roundup via search result](https://www.airops.com/blog/hidden-dangers-of-programmatic-seo) (secondary, unverified)
- Consequence: "Sites that violate spam policies may rank lower in results or not appear in results at all" — [Aspiration Marketing summary of Google blog](https://blog.aspiration.marketing/en/googles-new-update-targets-low-quality-content). Enforcement was both algorithmic and manual action.
- Site reputation abuse: original wording, "the practice of publishing third-party pages on a site in an attempt to abuse search rankings by taking advantage of the host site's ranking signals". Enforcement via manual actions began May 2024 (Forbes Advisor and CNN Underscored reported hit) — [Wordtracker summary](https://app.wordtracker.com/blog/seo/google-tightens-site-reputation-abuse-policy)
- Updated 19 Nov 2024: Google said "no amount of first-party involvement alters the fundamental third-party nature of the content or the unfair, exploitative nature of attempting to take advantage of the host's sites ranking signals" — i.e. oversight/white-label/licensing does not exempt third-party content — [Google blog, Updating our site reputation abuse policy (Nov 2024)](https://developers.google.com/search/blog/2024/11/site-reputation-abuse); [Search Engine Land](https://searchengineland.com/google-site-reputation-abuse-policy-now-includes-first-party-involvement-or-oversight-of-content-448432)
- Relevance to a directory: site reputation abuse concerns hosting third-party content (e.g. coupon/review sections) on an authoritative domain. A directory that publishes its own AI-collected data is first-party, so this policy matters mainly if you later add user-submitted or sponsored sections that are hosted for ranking benefit. Inference, not a Google statement.
- Helpful Content system: merged into core ranking in the March 2024 core update; it is no longer "a single system with a single classifier" but incorporated into core ranking systems — [GSQI (Glenn Gabe) on March 2024 core update](https://www.gsqi.com/marketing-blog/google-march-2024-core-update-helpful-content-system/) and secondary summaries via search. Before the merge (mid-2023) the system applied a site-wide signal so low-value content in one section could suppress unrelated pages — secondary source, [ProfileTree/Pi-Datametrics via search](https://pi-datametrics.com/blog/what-is-googles-helpful-content-system/).
- Doorway abuse (older policy, still current): pages "created to rank highly for specific search queries" that "lead users to multiple similar pages in search results where each result ends up taking the user to essentially the same destination". John Mueller warned against ~1,300 city landing pages built to rank for "keyword + city", calling that doorway behaviour — [Local Search Forum thread quoting Mueller](https://localsearchforum.com/threads/google-city-landing-pages-can-be-doorway-pages-against-guidelines.55438/latest) (forum; date not confirmed)
- Google guidance page "Google Search's Guidance on Generative AI Content on Your Website" exists at developers.google.com/search/docs/fundamentals/using-gen-ai-content (listed in search results; text not retrievable). Per search extracts it reiterates that using AI is not itself a violation, but generating many pages without adding value may violate the scaled content abuse policy — [Google guidance page](https://developers.google.com/search/docs/fundamentals/using-gen-ai-content) (not read; extract only)
- Quality Rater Guidelines were updated (Jan 2025) so raters can rate pages whose main content is created with automated/generative AI tools with little effort or originality as lowest quality — [PPC Land summary](https://ppc.land/google-updates-quality-rater-guidelines-with-ai-content-evaluation-criteria/); [SEOZoom](https://www.seozoom.com/?p=27852). Raters do not directly change rankings; they evaluate systems.
- 2026 updates confirmed by Search Engine Land headlines and Google Search Status Dashboard listings: March 2026 spam update began 24 March 2026, completed in 19h30m ([SEL](https://searchengineland.com/google-releases-march-2026-spam-update-472411), [Google status](https://status.search.google.com/incidents/VbnSXAH4SmEcxPtx4YSD)); March 2026 core update ran 27 March to 8 April 2026 (12 days 4 hours) and was the first core update of 2026 ([SEL rollout complete](https://searchengineland.com/google-march-2026-core-update-rollout-is-now-complete-473883), [Google status](https://status.search.google.com/incidents/7eTbAa2jWdToLkraZj5y)); a May 2026 core update followed ([SEJ headline](https://www.searchenginejournal.com/google-confirms-may-2026-core-update-is-now-rolling-out/575589/)); spam updates in June and an August 2026 spam update started 18 August 2026 (secondary: [Coalition Technologies](https://coalitiontechnologies.com/blog/google-august-2026-spam-update)). A further core update was only predicted (not confirmed) for Q4 2026.
- Google described the March 2026 core update as "a regular update designed to better surface relevant, satisfying content for searchers from all types of sites" — [Search Engine Land via search extract](https://searchengineland.com/google-march-2026-core-update-rolling-out-now-472759). I found no evidence of a new written scaled-content policy rewrite in 2026; the policy text appears unchanged since March 2024 (not verified against the live page).
- Claims that March 2026 caused "60-90% overnight losses" for AI-page sites come only from SEO-agency blogs (e.g. [Digital Applied](https://www.digitalapplied.com/blog/scaled-content-abuse-google-march-update-ai-pages-decimated), [1ClickReport](https://www.1clickreport.com/blog/google-may-2026-core-update-programmatic-seo-dead)) with no named sites or methodology; unverified and likely marketing.

### Inferences
- The operative test is purpose and value per page, not provenance. A directory where each page carries distinct, verified facts (name, address, hours, fuel types, coordinates, verification date) has a defensible position; pages that differ only by place name and a templated AI paragraph are the policy's archetype.
- Because the Helpful Content signal was folded into core ranking (site-wide quality assessment), a large share of weak pages can depress good pages. Quality control of the whole index matters more than the best pages.
- Use of AI agents to collect data is not the risk; the risk is publishing unverified, sparse or duplicated output at scale.

### Gaps
- Could not read the live Google spam-policies page, gen-AI guidance page or its "last updated" dates; the quotes above are from search-result extracts. Re-verify wording before quoting publicly.
- No confirmed 2025-2026 Google blog post changing scaled content policy text found; "Google November 2025 helpful content refresh" mentioned by a blog is unverified (Google no longer has a separate HCU).
- Google's doorway-abuse exact current wording not retrieved.

## 2. Evidence and case studies (winners, losers, directory-type sites)

### Takeaway
Named large losers are mostly review/affiliate and comparison sites, not pure directories. The big place/listing sites (Tripadvisor, Yelp, Zillow, Glassdoor) survived the spam policies because their pages hold unique user-generated and first-party data, but they now lose traffic to AI Overviews, not to spam enforcement. Evidence on AI-agent-populated directories specifically is thin and anecdotal.

### Cited Findings
- HouseFresh (independent product review site) reported losing about 95% of Google traffic after September 2023 Helpful Content update (~4,000 daily visitors to ~200 per one summary); a recovery was reported by its editor Gisele Navarro on 11 October 2025 — [PPC Land](https://ppc.land/housefresh-achieves-notable-traffic-recovery-after-google-algorithm-impacts-2/); [AFP via Malay Mail, 2 July 2024](https://www.malaymail.com/news/tech-gadgets/2024/07/02/google-is-broken-how-an-algorithm-tweak-cost-livelihoods/142493). Note this is a human-written site that lost, i.e. the update was not AI-detection.
- Sistrix IndexWatch "SEO losers in Google US search 2024": product-review/affiliate publishers including Lifewire, Newegg, Good Housekeeping and CNET saw visibility declines through 2024 — [Sistrix](https://www.sistrix.com/blog/indexwatch-seo-losers-in-google-us-search-2024/) (via search extract; figures not retrieved).
- G2 (software review site with 100,000+ programmatic pages) reportedly lost about 80% of organic traffic by late 2025, with Reddit ranking for most of the comparison queries it used to own — secondary source only ([AirOps](https://www.airops.com/blog/hidden-dangers-of-programmatic-seo)); unverified, no SEC statement found. Cause is plausibly a mix of content/UGC competition, not necessarily a penalty.
- ZoomInfo programmatic collapse and a 73% "HCU algorithmic penalty" drop appear in blog roundups with no dates or methodology — unverified ([AirOps](https://www.airops.com/blog/hidden-dangers-of-programmatic-seo), [quickseo.ai](https://quickseo.ai/blog/programmatic-seo-stats-2026-is-pseo-still-viable-in-the-ai-search-era)).
- Tripadvisor: CEO Matt Goldberg told investors of "ongoing declines in flyby visitors to our site due to the changing search landscape and the rise of AI overviews"; the CFO said SEO matters to legacy businesses but is expected to produce under 10% of strategic "Experience" gross booking volume by end of 2026 — [Skift, 12 Feb 2026](https://skift.com/2026/02/12/tripadvisor-sees-traffic-decline-from-ai-overviews-considers-strategic-alternatives-again/). One secondary source cites monthly visits down from 146-169M (early 2023) to ~120M (Feb 2025) — [CO/AI](https://getcoai.com/news/tripadvisor-pivots-to-daily-app-as-google-ai-threatens-search-traffic/) (unverified). No SEC filing text confirmed.
- Programmatic "winners" cited in roundups: Zapier (25,000-70,000 integration pages; ~6.3M monthly visits claimed), Tripadvisor (millions of pages), Yelp, Zillow, Glassdoor (millions), Canva, Wise (1.7M programmatic pages and ~54M monthly organic visits in one source; another says ~14,888 pages / 4.67M visits for currency pages, so figures conflict) — [Bullet.so](https://bullet.so/blog/best-programmatic-seo-examples/), [SEOmatic](https://seomatic.ai/blog/programmatic-seo-examples), [AirOps](https://www.airops.com/blog/hidden-dangers-of-programmatic-seo), [Upgrowth](https://upgrowth.in/how-wise-programmatic-seo-drives-over-90m-monthly-organic-traffic/). All are third-party traffic estimates (Semrush/Similarweb-type), not company statements. Nomad List: search yielded no usable evidence.
- Common pattern attributed to winners: repeatable keyword pattern, a structured dataset that differs per page, and a template that answers the query for each variation — [Security Boulevard, Nov 2025](https://securityboulevard.com/2025/11/the-programmatic-seo-paradox-why-your-fear-of-creating-thousands-of-pages-is-both-valid-and-obsolete/) (opinion).
- Directory-type anecdotes: a directory with 2,499 vendor listings across Beirut, Dubai, Riyadh, Doha, Cairo and Casablanca had 591 programmatic landing pages and 1,182 sitemap URLs, with Google indexing one page — [DEV Community](https://dev.to/bcrypto/i-have-591-pages-google-indexed-one-heres-how-im-debugging-it-5cel) (single-author anecdote, unverified). Thirty programmatic city pages: zero indexed after six months, status "Discovered - currently not indexed" — [DEV Community](https://dev.to/dylanmerigaud/i-built-30-programmatic-pages-google-indexed-zero-2h6f) (anecdote).
- SEJ reported a site deindexed by Google for programmatic SEO that later "bounced back" (title only; details not retrievable) — [SEJ](https://www.searchenginejournal.com/why-website-deindexed-by-google-for-programmatic-seo-bounced-back/552179/). GSQI published a case of a site removed from Google before a delayed manual action — [GSQI](https://www.gsqi.com/marketing-blog/deindexed-and-delayed-manual-action-case-study/) (not read).
- Zero evidence found of Yellow Pages-type or Zillow-style sites penalised under scaled content abuse; absence of evidence in search results, not proof.

### Inferences
- Winners combine unique/first-party or UGC data, brand demand (people search the brand), strong link profiles, and per-page depth. Losers are low-differentiation, affiliate-monetised, thin or derivative pages on weak domains.
- A new, brand-less, link-less directory populated by agents sits far closer to the losers' profile on authority, and so must compensate with verified data depth and page-level usefulness.
- Even successful directories face a second threat: AI Overviews and answer engines removing the click (Tripadvisor).

### Gaps
- No reliable per-site traffic-loss numbers with dates from Sistrix/Semrush/Ahrefs pages (blocked). No SEC/IR statements located for Yelp, Glassdoor (Recruit Holdings), Zillow or G2 on spam-policy impact.
- No documented case study of a fully AI-agent-populated local directory ranking or being penalised at scale with traceable data.

## 3. Thin and empty pages: soft 404, doorway, indexing limits, noindex, crawl budget

### Takeaway
Google does not publish a cap on indexed pages from a template site; it indexes what it judges worth indexing, and near-empty template pages typically end up in "Discovered/Crawled - currently not indexed" (a quiet filter) before any spam action. Crawl budget formally matters at 1M+ pages, and soft 404s waste it.

### Cited Findings
- Google's crawl-budget guide targets sites with 1 million+ unique pages and weekly changes, 10,000+ pages with daily changes, or sites with a large share of URLs classed "Discovered - currently not indexed" — [Google crawl budget docs](https://developers.google.com/crawling/docs/crawl-budget) (via search extract).
- Crawl budget = crawl capacity limit + crawl demand; "Soft 404 pages will continue to be crawled, and waste your budget"; use robots.txt to block unimportant pages, and keep sitemaps current — [Google crawl budget docs](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget) (via search extract).
- Programmatic template guidance that these pages become doorways "when only the placeholder changes" while they are legitimate when each page carries real local data and differences — [WPReset article](https://wpreset.com/programmatic-location-pages-without-doorway-risks/) (secondary, low authority).
- Reported Search Console statuses for programmatic sites ("Discovered - currently not indexed", "Crawled - currently not indexed") are quality/priority filters rather than penalties — [DEV Community case](https://dev.to/dylanmerigaud/i-built-30-programmatic-pages-google-indexed-zero-2h6f) (anecdote consistent with Google docs).
- A 50,000-page long-tail AI programme reported pages being deindexed and traffic dropping overnight; sites that kept the templated playbook through March 2024 reportedly lost 40-90% of indexed pages — [Digital Applied](https://www.digitalapplied.com/blog/scaled-content-abuse-google-march-update-ai-pages-decimated), [AirOps](https://www.airops.com/blog/hidden-dangers-of-programmatic-seo) (blog-level, unverified).

### Inferences
- Practical rule: only put into the sitemap and leave indexable the pages that meet a minimum content threshold (e.g. a non-zero verified count of places with real fields); noindex or exclude empty or one-item category-place combinations until populated. This follows Google's soft-404/doorway logic but is my recommendation, not a quoted Google rule.
- A "petrol pumps in Islamabad" page with real list entries, map, hours, last-verified date has a purpose; "petrol pumps in [tiny village]" with zero entries is a soft-404 / doorway candidate. Return a real 404 or noindex rather than an empty page.
- Staged rollout (index a few thousand strongest pages, expand as indexing rate proves healthy) limits site-wide quality dilution.

### Gaps
- No Google-stated numeric limit on indexed template pages exists in what I found. Could not fetch Google's soft-404 / noindex documentation. Google's recommendation on noindex for low-content pages was not retrieved verbatim.

## 4. Unique data as a moat

### Takeaway
Evidence is consistent but indirect: successful programmatic sites attribute their results to proprietary or structured per-page data and are explicit that copied/aggregated content is what gets filtered. I found no controlled study isolating "first-party data" as a ranking factor.

### Cited Findings
- Policy language lists as abusive "scraping feeds" and pasting together content from other pages, i.e. aggregation without added value — [Google blog, Mar 2024](https://developers.google.com/search/blog/2024/03/core-update-spam-policies).
- March 2026 coverage (blog-level) says aggregator sites adding no context beyond scraped source data were one of three patterns hit — [Digital Applied](https://www.digitalapplied.com/blog/scaled-content-abuse-google-march-update-ai-pages-decimated) (unverified).
- Sites that survived are described as having "a structured dataset that differentiates each page" — [Security Boulevard](https://securityboulevard.com/2025/11/the-programmatic-seo-paradox-why-your-fear-of-creating-thousands-of-pages-is-both-valid-and-obsolete/); Wise (exchange-rate data, own pricing) and Zapier (real integration data) are repeatedly used as examples — [Bullet.so](https://bullet.so/blog/best-programmatic-seo-examples/).
- Quality-rater guidance penalises AI-made main content with little originality or effort — [PPC Land, Jan 2025](https://ppc.land/google-updates-quality-rater-guidelines-with-ai-content-evaluation-criteria/).

### Inferences
- For an agent-gathered directory, the moat is verification: timestamped, source-cited, human- or field-verified records, plus data that no scraper has (pump fuel availability, prices, photos, contributor reports). The raw agent output alone is replicable, so is not a moat.
- Links are a likely second prong (original datasets, rankings, press); no sourced figure found on link yield from proprietary data.

### Gaps
- No peer-reviewed or large-sample (Ahrefs/Semrush/Sistrix) study found that quantifies ranking or link benefit of proprietary data. Search for "information gain" patent commentary not done.

## 5. Measuring early: Search Console, indexing, time-to-rank, sandbox

### Takeaway
Google has never confirmed a "sandbox"; new sites are quick to index but slow to rank for competitive terms. Early signals are indexing ratio and impressions on long-tail queries, not clicks.

### Cited Findings
- Sandbox "has never been officially confirmed by Google"; new sites are easy to index but hard to rank — [Ahrefs, Google Sandbox article](https://ahrefs.com/blog/google-sandbox/) (via search extract; study data not retrieved).
- Indexing: pages can be crawled within hours of submission and indexed within a day or two for some sites — [Ahrefs via search extract](https://ahrefs.com/blog/google-sandbox/). Estimates for ranking range from 4-6 weeks (one expert) to 6-12 months (other SEO blogs) — [Seatext](https://seatext.com/blog/why-is-my-new-website-taking-6-months-to-rank-on-google) (low authority). I did not find a rigorous sourced benchmark; the Ahrefs "Sandbox 2.0" / large-sample time-to-rank studies were not retrievable.
- Search Console statuses to monitor on large template sites: "Discovered - currently not indexed", "Crawled - currently not indexed", Soft 404 (flagged in Page Indexing report) — [Google crawl budget docs](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget).
- Anecdote: 30 city pages not indexed after six months and a directory with 1 of 591 landing pages indexed show the risk of a new/low-authority domain — [DEV 30 pages](https://dev.to/dylanmerigaud/i-built-30-programmatic-pages-google-indexed-zero-2h6f), [DEV 591 pages](https://dev.to/bcrypto/i-have-591-pages-google-indexed-one-heres-how-im-debugging-it-5cel).

### Inferences
- Suggested early dashboard (my recommendation): indexed/submitted ratio per template; share of pages with at least one impression after 30/60/90 days; impressions on branded vs non-branded; average position for "category + city" queries; crawl stats (Search Console Settings > Crawl stats). Treat a low indexed ratio on a sampled batch as the earliest warning, before traffic.
- Plan for roughly several months before meaningful non-brand traffic; do not read a flat first 4-8 weeks as failure or as a penalty.

### Gaps
- No credible sourced distribution of "days to first traffic" for new domains (Ahrefs, Semrush and Sistrix pages blocked). Do not cite the 4-6 week or 6-12 month figures as benchmarks.

## 6. Other search engines (Bing, Baidu, Yandex, Naver)

### Takeaway
Only Bing's guidance was confirmed as explicit about AI-generated content at scale (quality and oversight, not method). Baidu, Yandex and Naver had no retrievable AI-content-policy text; assume quality/duplication rules, but this is unverified.

### Cited Findings
- Bing Webmaster Guidelines: large-scale automatically generated content produced without oversight, quality control or editorial review "often lacks usefulness, accuracy, and originality" and "may be excluded from indexing" — [Bing Webmaster Guidelines](http://www.bing.com/webmasters/help/webmaster-guidelines-30fba23a) (via search extract). Bing allows AI content that meets its quality/originality standards — [Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/2349276/does-bing-allow-ai-content-to-be-used-in-the-websi).
- Bing rewrote its guidelines to add Generative Engine Optimization (GEO) and expanded AI-abuse definitions; it also offers an "AI Performance" report in Webmaster Tools — [SEJ](https://www.searchenginejournal.com/bing-adds-geo-to-official-guidelines-expands-ai-abuse-definitions/568442/), [Bing AI Performance](https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c). Date of the rewrite not confirmed (appears 2026).
- Naver: an "Authority-aware Generative Retriever (AuthGR)" is reported to evaluate author credibility and demote low-quality or machine-generated content; about 70% of Naver AI Briefing results rely on user-generated content (blogs, cafes) — [Bizhankook (via search)](https://en.bizhankook.com/articles/29309.html) (low confidence, translated Korean media).
- Baidu: sources say it punishes duplicate content harshly and favours quality; no AI-content-specific policy found — [BrightEdge glossary](https://www.brightedge.com/glossary/world-search-engines) (generic). Baidu 20-F FY2025 exists on SEC but was not read — [SEC](https://www.sec.gov/Archives/edgar/data/1329099/000119312526109289/d38065d20f.htm).
- Yandex: described as emphasising content quality and link quality; no AI-content policy found — [BrightEdge glossary](https://www.brightedge.com/glossary/world-search-engines).

### Inferences
- A Google-compliant, high-quality directory should also meet Bing's stated bar. IndexNow (supported by Bing and Yandex) is an easy way to push new URLs (from the IndexNow Wikipedia entry in results; not verified further).
- For China, Baidu indexing also depends on ICP licensing and hosting (my background knowledge, not sourced here); do not rely on Google-style assumptions.

### Gaps
- No primary documentation for Baidu (Webmaster Platform quality guidelines, "Baidu Search Resource Platform"), Yandex Webmaster guidance on AI content, or Naver Search Advisor on AI content was retrieved. Needs a direct check or a native-language source.

## Unverified items from background knowledge (not found in this session's sources; do not cite without checking)
- Google's February 2023 Search Central statement that appropriate use of AI is not against guidelines, and the "who, how and why" framing of helpful content.
- Google's official recommendation that noindex is appropriate for pages not intended for search, and its stated view that soft 404s should return real 404/410 status.
- Mueller's statements that there is no fixed page count limit and that "Discovered - currently not indexed" often reflects perceived site quality.
