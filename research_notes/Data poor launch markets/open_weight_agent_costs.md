# Open-weight and low-cost AI agent networks for web research on local businesses: real cost, capability and risk (tests the claim "AI agents are free, run from laptops, cost close to nothing")

Research date: 2026-10-05. All prices are as reported on the date stated or as of search-result retrieval in late Sept to early Oct 2026. Many pricing figures come from third-party aggregators because the official DeepSeek, OpenRouter and Puter pages were blocked by the network egress proxy (see Gaps). Where aggregators disagree, the conflict is stated. Items labelled "Estimate" are my own arithmetic from the cited inputs and the stated assumptions, not sourced facts.

Headline verdict (inference, supported by the sections below): The claim is true only for one layer, which is LLM token cost for page-level extraction. Tokens for extraction cost roughly $0.0003 to $0.02 per record (Estimate). That is real and small. The claim fails for the rest of the pipeline: proxies and unblocking, search or places APIs, human review, verification, engineering time, legal review, and security hardening. Together these plausibly cost 5x to 100x more per record than the model tokens (Estimate). "Free" also does not hold for agentic browsing, where token use per record is roughly 10x to 15x higher than extraction-only (Estimate).

---

## 1. Model costs: API prices, cache discounts, free tiers, self-hosting, laptop throughput

### Takeaway
Cheap Chinese open-weight APIs (DeepSeek V4 Flash, Qwen Flash tiers) are about 7x to 70x cheaper per input token than Claude Haiku 4.5 or Sonnet 5.5, and GPT-5 nano is in the same bracket. Cheap means cents per hundred records, not free. A laptop can run a small model (Qwen3 8B class) at roughly 50 to 80 generated tokens per second on high-end Apple silicon, which supports a few thousand extraction-only records per day (Estimate), not "an army".

### Cited Findings

**Frontier and mid-tier comparators (primary source, fetched 2026-10-05)**
- Anthropic official pricing page lists Claude Sonnet 5.5 at $2 input / $10 output per MTok, cache hits $0.20/MTok. Claude Sonnet 5 is also $2/$10. The introductory price became the standard price and the planned 1 Sept 2026 rise to $3/$15 will not occur. Claude Sonnet 4.6 is $3/$15. Claude Haiku 4.5 is $1/$5, cache read $0.10/MTok. — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- Anthropic Batch API gives 50% off input and output (Haiku 4.5 batch $0.50/$2.50; Sonnet 5.5 batch $1/$5). Cache hits are 0.1x base input for most models, and the discounts stack. — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- Claude models 4.7 and later use a tokenizer that produces about 30% more tokens for the same text, which raises effective cost versus the headline rate (applies to Sonnet 5.5 but not Haiku 4.5 or Sonnet 4.6 per the page). — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- Anthropic web search tool costs $10 per 1,000 searches plus tokens; web fetch has no extra charge beyond tokens. An average 10 kB web page is about 2,500 tokens, a 100 kB page about 25,000 tokens. — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- Anthropic's own worked example: 10,000 support tickets of about 3,700 tokens on Haiku 4.5 cost about $37 (about $0.0037 per item). — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- Anthropic data residency: US-only inference carries a 1.1x multiplier on Claude 4.6 and later. — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)

**OpenAI small tier (aggregator, as of 2026-09-15)**
- GPT-5 nano: $0.05 input / $0.40 output per MTok. GPT-5.4 nano: $0.20 / $1.25. — [anotherwrapper GPT-5 nano](https://anotherwrapper.com/tools/llm-pricing/gpt-5-nano-2025-08-07), search summary of [intuitionlabs](https://intuitionlabs.ai/articles/chatgpt-api-pricing-2026-token-costs-limits). A GPT-5 mini price was not retrieved (Gap).

**DeepSeek (aggregators only; official page blocked)**
- DeepSeek V4 Flash: about $0.13 to $0.14 input (cache miss), $0.28 output per MTok, 1M-token context, 384K max output. — [SiliconFlow V4 pricing blog](https://www.siliconflow.com/blog/deepseek-v4-api-pricing-pro-flash), [zenmux](https://zenmux.ai/blog/deepseek-v4-flash-api-pricing)
- V4 Flash cache-hit input: $0.028/MTok per SiliconFlow summary; contradicted by another aggregator listing $0.0028/MTok (10x lower). Either way a cache hit is stated to be a small fraction of a miss. — [SiliconFlow](https://www.siliconflow.com/blog/deepseek-v4-api-pricing-pro-flash); contradicted by [morphllm DeepSeek API](https://www.morphllm.com/deepseek-api)
- V4 Pro: about $1.60 input / $3.135 output; cache hit $0.135 (SiliconFlow figures); search summary says a 75% promotional discount applied until 2026-05-31 15:59 UTC, after which it becomes one quarter of original, but the post-promo price was not confirmed. Another aggregator lists $1.74/$3.48 for "V4-Pro-Max". Treat the Pro price as unresolved. — [SiliconFlow](https://www.siliconflow.com/blog/deepseek-v4-api-pricing-pro-flash), [anotherwrapper compare](https://anotherwrapper.com/tools/llm-pricing/qwen3-32b/deepseek-v4-pro-max)
- DeepSeek has no permanent free tier on the official API; new accounts get trial credits only. — [SiliconFlow](https://www.siliconflow.com/blog/deepseek-v4-api-pricing-pro-flash)

**Qwen (Alibaba Cloud Model Studio, via aggregators)**
- Qwen3.7-Plus $0.40/$1.60 per MTok (tiered up to $1.20/$4.80 above 256K input); Qwen3.8-Flash $0.15/$0.47; Qwen3.7-Flash $0.03/$0.13 (tiered $0.20/$0.80 above 256K). — [Puter Qwen pricing via search summary](https://developer.puter.com/tutorials/qwen-api-pricing/), [eesel Qwen pricing](https://eesel.ai/blog/qwen-pricing)
- Free quota: new accounts get 1M tokens per eligible model for 90 days on the Singapore international endpoint, pooled across most Qwen models. — [Puter/eesel via search summary](https://developer.puter.com/tutorials/qwen-api-pricing/)

**Kimi and GLM (OpenRouter prices via aggregator, as of 2026-09-15)**
- Kimi K2-Instruct-0905: $0.60 input / $2.50 output per MTok; Kimi K2 Base $0.57/$2.30. — [anotherwrapper Kimi K2-Instruct-0905](https://anotherwrapper.com/llm-pricing/kimi-k2-instruct-0905), [Kimi K2 Base](https://anotherwrapper.com/llm-pricing/kimi-k2-base)
- GLM-5.1 about $1.40 / $4.40 per MTok; GLM-5.3 reported as similar. — [anotherwrapper GLM comparison](https://anotherwrapper.com/tools/llm-pricing/glm-5.1/kimi-k2-instruct-0905), [gradually.ai](https://www.gradually.ai/en/llm-comparison/kimi-k2.6-vs-glm-5.3/)
- Newer Kimi (K2.6, K3) exist, but I did not retrieve their prices (Gap).

**Llama-hosted and US hosts**
- Together AI ($0.20 to $0.90/MTok) and Fireworks AI ($0.18 to $3.00/MTok) are described as cheapest for open-source models with US data residency. No per-model Llama price retrieved. — [morphllm LLM API pricing via search summary](https://www.morphllm.com/llm-api-pricing)
- Qwen3 32B quoted at $0.10/$0.44; DeepSeek-V4-Flash-0423 at $0.10/$0.20 on an aggregator comparison. — [anotherwrapper compare](https://anotherwrapper.com/tools/llm-pricing/qwen3-32b/deepseek-v4-pro-max)

**Self-hosting: laptop throughput and GPU rental**
- Qwen3 8B at Q4_K_M with llama.cpp: about 83 tokens/s on MacBook Pro M4 Max 64 or 128GB (82.6), about 62 tok/s on M4 Max 36GB, about 53 tok/s on M3 Max 64GB; decode speed is memory-bandwidth-bound. These are top-end laptops, not typical ones. — [willitrunai Qwen3 8B on M4 Max](https://willitrunai.com/es/can-run/qwen-3-8b-on-m4-max-96gb)
- GPU rental: RTX 4090 about $0.34 to $0.69/hr (RunPod community vs secure) and $0.34 to $0.50/hr (Vast.ai); H100 80GB about $1.99 to $2.89/hr on RunPod and about $0.90 to $1.87/hr on Vast.ai. — [spheron RunPod vs Vast](https://www.spheron.network/blog/runpod-vs-vastai-2026/), [RunPod pricing](https://www.runpod.io/gpu-cloud/pricing)

### Inferences
- Per-record token cost (Estimate). Assumptions: extraction-only pipeline (crawler converts page to markdown, LLM returns JSON): about 6,000 input and 500 output tokens per business; agentic browsing: about 80,000 input (about 10 steps with growing context, no caching) and 3,000 output tokens. Single pass, no retries, list price (no cache or batch discount), prices from the findings above.

| Model (price used) | Extraction per record | Per 1M records | Agentic per record | Per 1M records |
|---|---|---|---|---|
| Qwen3.7-Flash ($0.03/$0.13) | $0.00025 | about $250 | $0.0028 | about $2,800 |
| GPT-5 nano ($0.05/$0.40) | $0.0005 | about $500 | $0.0052 | about $5,200 |
| DeepSeek V4 Flash ($0.14/$0.28) | $0.0010 | about $980 | $0.012 | about $12,000 |
| Kimi K2-0905 ($0.60/$2.50) | $0.0049 | about $4,900 | $0.056 | about $55,500 |
| Claude Haiku 4.5 ($1/$5) | $0.0085 | about $8,500 | $0.095 | about $95,000 |
| Claude Sonnet 5.5 ($2/$10) | $0.017 | about $17,000 | $0.19 | about $190,000 |

- Retries, validation passes and failed pages plausibly multiply these by 1.3x to 2x (assumption). Cache hits and Batch (Anthropic 50%) can cut input costs materially if the system prompt and schema dominate input, which they do not when pages dominate.
- Even on the cheapest rows, the model share of total per-record cost is small once proxies and review are included (see section 4).
- Laptop economics (Estimate). Assumptions: Qwen3 8B Q4 at about 60 to 80 tok/s decode on a high-end MacBook; 500 output tokens plus prefill of 6,000 input tokens; prefill speed was not sourced, so I assume about 10 to 15 seconds per record end to end. That yields about 5,000 to 8,500 records per day running 24 hours, which is 120 to 200 days per million records on one laptop. Agentic browsing with a small local model (80K+ tokens of context, multi-step) is plausibly 3 to 5 minutes per record, so about 300 to 500 records per day (Estimate, low confidence). Electricity at an assumed 60 to 100 W continuous and $0.15/kWh is roughly $0.2 to $0.4/day, which is negligible; the real constraint is time, thermal limits and a laptop that cannot be used for anything else.
- Rented GPU (Estimate): a 4090 at $0.34 to $0.69/hr costs $8 to $17 per day. Whether batching (vLLM) on one GPU gives 10x to 50x laptop throughput was not sourced; plausible, but unverified here.
- "Free tier" is a trial, not a pipeline: DeepSeek none, Alibaba 1M tokens per model for 90 days (which is roughly 160 extraction records at 6.5K tokens each if the whole million were used, arithmetic Estimate). Rate limits for free tiers were not retrieved.

### Gaps
- Official DeepSeek pricing page, OpenRouter, Together, Fireworks, Moonshot and Zhipu pricing pages could not be fetched (egress blocked or not attempted); all non-Anthropic prices are aggregator-reported.
- Cache-hit price for V4 Flash conflicts between sources (10x difference); V4 Pro post-promo price unconfirmed.
- No GPT-5 mini price, no current Llama-4-hosted per-model price, no Kimi K3 or GLM-5.2 price retrieved.
- Free-tier rate limits (requests per minute) for all providers not retrieved.
- Local prefill throughput and vLLM batched throughput not sourced; laptop records/day is an estimate.

---

## 2. Capability and reliability: benchmarks, extraction quality, multilingual performance, error compounding

### Takeaway
Top open-weight models now score at or near frontier closed models on agentic web benchmarks (vendor and aggregator numbers), and structured extraction from clean input is accurate with small models. But the evidence is weakest exactly where this project lives: multi-step, multilingual (Urdu, Bengali, Arabic) local-business research on messy sites. Per-step reliability compounds geometrically, so long agent runs fail much more often than benchmark headlines suggest.

### Cited Findings
- Kimi K3 (Moonshot, open-weight) listed #1 on BrowseComp at 91.2% as of 2026-09-09 per an aggregator leaderboard; scores for DeepSeek, GLM and Qwen on BrowseComp were not given in the retrieved results. BrowseComp measures hard multi-step web research puzzles, not local-business data extraction. — [anotherwrapper BrowseComp](https://anotherwrapper.com/tools/llm-pricing/evals/browsecomp), [benchlm best open source LLM](https://www.benchlm.ai/blog/posts/best-open-source-llm)
- Qwen-UI-Agent 27B technical report claims a 73.6% success rate, above Claude Opus 4.8 at 71.9% and GPT-5.5 at 69.5%; the retrieved snippet does not say which benchmark (it appeared in a WebArena-related search) and it is a self-reported vendor result. — [Qwen-UI-Agent Technical Report, arXiv 2607.28227](https://arxiv.org/pdf/2607.28227)
- A 9B supervised-fine-tuned model is reported as the best open-weight SFT result on full WebArena, nearly 2x the prior Go-Browse result, and beats GPT-4o on 4 of 5 benchmarks. — [Structured Distillation of Web Agent Capabilities, arXiv 2604.07776](https://arxiv.org/pdf/2604.07776)
- WebArena described as a reproducible 812-task benchmark across four web applications; these are synthetic sites, not live local-business sites with anti-bot defences. — [benchmarkingagents.com WebArena](https://benchmarkingagents.com/webarena)
- Extraction input format dominates quality: in NEXT-EVAL, flat JSON input let LLMs reach F1 0.9567 with minimal hallucination, while Gemini-2.5-pro-preview with Slimmed HTML input scored F1 0.1014 with a 0.9146 hallucination rate (and F1 0.4048 / hallucination 0.5976 with hierarchical JSON). — [NEXT-EVAL, arXiv 2505.17125](https://arxiv.org/pdf/2505.17125)
- ScrapeGraphAI-100k (93,695 real extraction events, multilingual): a 1.7B model trained on a subset narrows the gap to 30B baselines, which supports cheap small-model extraction when fine-tuned. — [ScrapeGraphAI-100k, arXiv 2602.15189](https://arxiv.org/html/2602.15189)
- Error compounding: task success follows a geometric law in a per-step reliability parameter that "saturates well below 1"; on agentic tasks every model tested fell from near-perfect to near zero within sixteen steps in one study; agents struggle to detect and recover from early errors. Agents near 100% on minutes-long tasks drop below 10% on multi-hour tasks (a secondary summary). — [Beyond the Leaderboard, arXiv 2607.05775](https://arxiv.org/pdf/2607.05775), [tianpan.co long-horizon gap](https://tianpan.co/blog/2026/04/10/long-horizon-evaluation-gap-agent-benchmarks), [How Fast Do Agents Rot, arXiv 2609.01660](https://www.alphaxiv.org/abs/2609.01660)
- Multilingual evidence: English consistently outperforms low-resource languages across tasks; LLaMA-3-70B reached 94.73% average accuracy on an Urdu benchmark (UrduBench, translated MGSM, MATH-500, CommonSenseQA, OpenBookQA), comparable to Gemma-3-27B-PT; this tests reasoning and QA, not entity extraction from Urdu business pages. — [UrduBench, arXiv 2601.21000](https://arxiv.org/pdf/2601.21000), [Do LLMs Speak All Languages Equally, arXiv 2408.02237](https://arxiv.org/html/2408.02237v1)
- Urdu-specific adaptation exists (UrduLLaMA 1.0 from Llama-3.1-8B with 128M Urdu tokens and LoRA), implying base small models needed adaptation to be useful. — [search summary of Urdu benchmark papers](https://arxiv.org/html/2410.13153v1)

### Inferences
- Illustrative compounding arithmetic (Estimate): at 95% per-step reliability a 20-step run succeeds about 36% of the time (0.95^20); at 99% it is about 82%. For a 10-step browse per business, a 95% per-step agent yields about 60% clean runs. So agentic browsing needs checkpoints, schema validation and retries, which multiplies token cost, which weakens the "near zero cost" claim.
- Design implication: separate deterministic crawling (Scrapy, Crawl4AI) from a short single-shot LLM extraction step. This keeps step counts to 1 to 3 and avoids most compounding. Benchmarks overstate agentic reliability for live local-business sites.
- Hallucination on weak input formats (0.91 in NEXT-EVAL) shows that, for business records, fabricated phone numbers or addresses are the key quality risk, so each extracted field needs source-text grounding or verification.
- For Urdu, Arabic, Bengali, Hindi and Chinese: Chinese is a core strength of Qwen, DeepSeek, Kimi and GLM (inference from provenance, not from a retrieved benchmark). For South Asian languages evidence is thin; test each model on a held-out sample before committing.

### Gaps
- No retrieved benchmark for Bengali, Arabic, or Hindi on entity or contact-field extraction; no tokenization-cost comparison (tokens per word in Urdu or Bengali versus English), which affects cost because non-Latin scripts typically use more tokens. This is not sourced here.
- No retrieved real-world head-to-head of DeepSeek V4 Flash vs Haiku 4.5 vs GPT-5 nano on local-business extraction F1.
- BrowseComp scores for DeepSeek V4, GLM and Qwen not retrieved; all leaderboard numbers are aggregator or vendor reported, not independently verified. Date-stamped scores from the aggregator leaderboard (2026-09-09) may already be stale.

---

## 3. Open-source agent frameworks and "agent armies": stars, licences, maturity, failure modes, proven scale

### Takeaway
There is no shortage of popular frameworks, but the proven large-scale data collection tools are the classical crawlers (Scrapy) and the LLM-ready crawlers (Crawl4AI, Firecrawl). Multi-agent "role-play" frameworks (CrewAI, MetaGPT, AutoGen) have large star counts but I found no evidence of them powering million-record collection pipelines. Stars are not maturity, and two of the browser-agent tools use AGPL.

### Cited Findings
Stars, licence and activity as read from GitHub pages on 2026-10-05 (page-view figures; latest-commit dates were mostly not displayed).

| Project | Stars | Licence | Notes |
|---|---|---|---|
| Firecrawl | 189k | AGPL-3.0 core; MIT SDKs/UI | 6,469 commits; cloud adds enterprise features beyond self-hosted core — [GitHub](https://github.com/firecrawl/firecrawl) |
| Browser Use | 117.2k | MIT | 10,333 commits; hosted cloud API plus local library; 31 browser actions — [GitHub](https://github.com/browser-use/browser-use) |
| OpenHands | 90k | MIT | Release 1.24.0; positioned as developer control centre for coding agents, not a scraper — [GitHub](https://github.com/OpenHands/OpenHands) |
| Crawl4AI | 84.8k | Apache-2.0 | Release v0.9.4 on 2026-09-23; markdown generation, CSS/XPath/LLM extraction, deep crawl, Docker, MCP — [GitHub](https://github.com/unclecode/crawl4ai) |
| MetaGPT | 70.7k | MIT | README news items dated early 2025 only — [GitHub](https://github.com/FoundationAgents/MetaGPT) |
| Scrapy | 64.6k | BSD-3-Clause | Maintained by Zyte plus community; Python 3.11+ — [GitHub](https://github.com/scrapy/scrapy) |
| AutoGen | 61.3k | CC-BY-4.0 and MIT | In maintenance mode, community-managed, no new features; Microsoft Agent Framework is the successor — [GitHub](https://github.com/microsoft/autogen) |
| CrewAI | 59.4k | MIT | Page showed "latest release v0.102.0" which looks stale (possible cached page); verify before relying on it — [GitHub](https://github.com/crewAIInc/crewAI) |
| OpenManus | 58.5k | MIT | 535 commits; 246 open issues; from MetaGPT contributors; uses Browser Use — [GitHub](https://github.com/FoundationAgents/OpenManus) |
| LangGraph | 42.7k | MIT | Durable, stateful agent orchestration by LangChain Inc — [GitHub](https://github.com/langchain-ai/langgraph) |
| Agno | 42.6k | Apache-2.0 | Agent platform, 100+ integrations — [GitHub](https://github.com/agno-agi/agno) |
| smolagents | 29.7k | Apache-2.0 | README warns LocalPythonExecutor has no security boundary and should not run untrusted code — [GitHub](https://github.com/huggingface/smolagents) |
| Skyvern | 23.1k | AGPL-3.0 | LLM plus computer-vision browser workflows; 6,940 commits — [GitHub](https://github.com/Skyvern-AI/skyvern) |

- Crawl4AI and Firecrawl describe themselves as pipelines that turn websites into LLM-ready markdown, with LLM-schema extraction; Browser Use, Skyvern and OpenManus are browser-driving agents. — repo READMEs above.
- Security-relevant framework failure mode: smolagents warns its local Python executor is not safe for untrusted code. — [smolagents](https://github.com/huggingface/smolagents)
- Scale evidence I did find: ScrapeGraphAI-100k records about 93,695 real LLM extraction events from the ScrapeGraphAI library in Q2 to Q3 2025 across domains and languages, which shows the extraction pattern is used in practice at the 100k-event scale, but it is a dataset paper rather than a cost or accuracy audit of a production directory. — [arXiv 2602.15189](https://arxiv.org/html/2602.15189)

### Inferences
- Stars are inflated by hype cycles (OpenClaw-style projects accrue stars faster than security review; see section 6). Use release cadence, open issue counts and the existence of paid cloud versions as maturity signals instead.
- Licence risk: Firecrawl (AGPL-3.0 core) and Skyvern (AGPL-3.0) require source disclosure of network-served modifications; for an internal data pipeline this is usually manageable, but legal should check if any service exposes the code. MIT, Apache or BSD options (Crawl4AI, Scrapy, Browser Use, smolagents) avoid this.
- AutoGen being in maintenance mode makes it a poor foundation for a new build.
- A sensible stack for this task (inference): Scrapy or Crawl4AI for fetching, a single LLM call for extraction, and a thin orchestrator. A multi-agent "army" adds coordination tokens and failure modes without improving extraction on listing-type pages.

### Gaps
- No named public case study found of CrewAI, MetaGPT, AutoGen, OpenManus or Browser Use producing a large (100k+ records) verified business dataset with published cost and accuracy.
- Last-commit dates and release dates were not displayed for most repos; CrewAI release number looks stale; Scrapy, LangGraph, Agno, smolagents, MetaGPT release dates not retrieved.
- Zyte or Firecrawl customer case studies on enrichment pipelines not retrieved.

---

## 4. Non-model costs that remain, with an itemised cost-per-verified-record model

### Takeaway
Proxies, search or places data, human review and verification dominate cost once tokens are cheap. My itemised estimate gives about $0.03 to $0.20 per verified record on web-scraping routes (Estimate), i.e. about $30k to $200k per million records before engineering and legal. If the Google Places API is used instead of scraping, API fees alone are about $0.05 to $0.08 per record at list price and Google's terms restrict storage.

### Cited Findings
- Bright Data residential proxies about $4.00/GB pay-as-you-go (promo against $8.00/GB list), committed tiers about $2.50 to $3.50/GB; another source lists about $8.40/GB pay-as-you-go falling to about $3.00/GB committed. Oxylabs about $6 to $8/GB. — [use-apify Bright Data pricing](https://use-apify.com/blog/bright-data-pricing-guide-2026), [DEV cheapest residential proxies](https://dev.to/ethan_walker995/cheapest-residential-proxy-providers-in-2026-price-per-gb-comparison-38g3), [costbench Oxylabs vs Bright Data](https://costbench.com/compare/bright-data-vs-oxylabs/)
- Bright Data Web Unlocker about $3 per 1,000 successful responses; scraper APIs from about $0.75 per 1,000 records. — [hackceleration Bright Data pricing](https://www.hackceleration.com/labs/bright-data-pricing), [use-apify](https://use-apify.com/blog/bright-data-pricing-guide-2026)
- CAPTCHA solving: 2Captcha about $0.50 to $1 per 1,000 image CAPTCHAs, about $2.99 per 1,000 reCAPTCHA v2/hCaptcha; CapSolver from $0.80 per 1,000; Anti-Captcha $1.98. — [AIMultiple CAPTCHA services](https://research.aimultiple.com/captcha-solving-services), [hasdata](https://hasdata.com/blog/captcha-solving)
- Search APIs: Serper about $1 per 1,000 Google SERP calls; Brave Search API $5 per 1,000 (with $5/month credit). Anthropic web search $10 per 1,000. — [apicostcalc comparison](https://apicostcalc.com/web-search-api-cost-calculator.html), [keenable](https://select.keenable.ai/r/web-search-api-providers-2026-comparison/nk_VX3yEg0e9P0ufQdwS9g), [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- Google Places API: Text Search about $32 per 1,000 for the first 100,000 per month (falling to $2.40 above 5M); Place Details about $17 per 1,000 (Pro) to $20 (Enterprise) and $35 to $40 per 1,000 when ratings, hours, reviews or photos are requested. — [Woosmap Google Places pricing](https://www.woosmap.com/blog/google-places-api-pricing), [Google Maps Platform pricing](https://developers.google.com/maps/billing-and-pricing/pricing)
- Google Maps terms prohibit scraping Google Maps content and storing content for more than 30 days (bulk downloading, copying names, addresses, reviews). — [ConductAtlas Google Maps Platform ToS](https://conductatlas.com/platform/google-maps/google-maps-platform-terms-of-service/no-scraping-or-content-extraction/), [Thunderbit](https://thunderbit.com/blog/is-scraping-google-maps-legal)
- Anthropic Managed Agents: $0.08 per session-hour runtime plus tokens (for comparison with self-run infrastructure). — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)

### Inferences
Itemised cost-per-verified-record model (all Estimate; per attempted business record; assumptions listed):

| Line | Assumption | Low | High |
|---|---|---|---|
| LLM tokens, extraction | 6K in / 0.5K out; Qwen Flash to Haiku 4.5 prices; 1.3x to 2x retries | $0.0003 | $0.017 |
| LLM tokens, agentic browsing (if used instead) | 80K in / 3K out; DeepSeek V4 Flash to Haiku 4.5 | $0.012 | $0.19 |
| Residential proxy bandwidth | 4 page loads at about 1.5 MB each (6 MB) with images/JS; $2.50 to $8/GB; lower if images blocked and datacenter IPs suffice | $0.015 | $0.05 |
| Unblocker alternative | 4 requests at $0.75 to $3 per 1,000 | $0.003 | $0.012 |
| Search API | 1 to 2 queries per record at $1 to $5 per 1,000 | $0.001 | $0.010 |
| CAPTCHA | 5% to 10% of requests need solving at $0.8 to $3 per 1,000 | $0.0001 | $0.001 |
| Human review | 5% of records reviewed at 2 minutes each, at $5 to $15/hour | $0.008 | $0.025 |
| Phone/email verification | No sourced price; allowance only | $0.00 | $0.05 |
| Compute/electricity/hosting | Laptop near zero; cloud box or GPU rental $8 to $17/day amortised over 5k to 50k records/day | $0.0002 | $0.003 |
| Per attempted record, scraping route | Sum of non-agentic lines | about $0.03 | about $0.12 |
| Per verified record | Divide by an assumed 50% to 70% pass rate | about $0.04 | about $0.20 |

- Per million verified records: about $40k to $200k in variable cost (Estimate), versus the "model cost only" figure of about $250 to $17,000 per million attempted extraction-only calls. So model tokens are roughly 1% to 15% of total cost depending on model choice (Estimate).
- Fixed costs not in the table: engineering time (build, selectors, monitoring, schema, QA, plausibly several person-weeks to months; no sourced figure), legal review (GDPR, ToS, no sourced figure), de-duplication, geocoding (Google geocoding price not retrieved; Nominatim/OSM is a free alternative but has usage limits, unverified here), storage (negligible for text records).
- If the Google Places API is used instead: Text Search ($32/1,000) plus Details ($17 to $40/1,000) is about $0.05 to $0.07 per record at list price (Estimate from cited prices), which exceeds the entire LLM bill, and the 30-day storage restriction in Google's terms conflicts with building a persistent directory.
- Datacenter proxies and polite crawling of small business sites (often simple, unprotected) could cut the proxy line sharply; the share of small-business sites with anti-bot protection was not found.

### Gaps
- No sourced prices for phone or email verification services, geocoding, or human review labour rates in specific launch markets (the $5 to $15/hour range is an assumption).
- Official Bright Data, Oxylabs and ScraperAPI pages not fetched; prices are aggregator-reported and differ between sources.
- Share of local-business sites needing proxies or CAPTCHAs unknown; average page weight is an assumption.
- No sourced engineering or legal review cost figures.

---

## 5. Throughput and scale: records per day, blocking, time to one million records

### Takeaway
On a single laptop with a local model, extraction-only throughput is in the low thousands to about eight thousand records per day (Estimate); agentic browsing is hundreds per day. A modest cloud setup with API models is limited by crawl concurrency and blocking, not by the model, and could reach one million records in days to weeks (Estimate).

### Cited Findings
- Local decode speed on high-end laptops about 53 to 83 tok/s for Qwen3 8B Q4 (see section 1). — [willitrunai](https://willitrunai.com/es/can-run/qwen-3-8b-on-m4-max-96gb)
- GPU rental about $0.34 to $2.89/hr depending on card and provider. — [spheron](https://www.spheron.network/blog/runpod-vs-vastai-2026/)
- Web Unlocker is billed per successful response, which implies block rates are borne by the provider rather than the buyer. — [hackceleration](https://www.hackceleration.com/labs/bright-data-pricing)
- No retrieved source gives provider API rate limits (DeepSeek, Alibaba free tier, Moonshot, OpenRouter) or published blocking rates for local-business sites.

### Inferences (all Estimate)
- Laptop, local small model, extraction-only: about 10 to 15 s per record, single stream, 24h: about 5,800 to 8,600 records/day; 1M records takes about 115 to 175 days. With a more typical laptop (slower than M4 Max) or daytime use only, expect 1,000 to 3,000/day, so 1M takes about a year or more.
- Laptop, local model, agentic browsing: about 300 to 500 records/day; 1M takes 5 to 9 years. This directly undercuts "laptops can run an army".
- Cloud box with API model and Crawl4AI/Scrapy: assume 50 concurrent browser sessions at about 20 s per record (4 page loads plus one LLM call): about 2.5 records/s, about 216,000 per day, so about 5 days per million, before blocking and retries. Realistically 2x to 5x slower with blocking, JS-heavy pages and retries: about 10 to 25 days per million. Bandwidth and proxy cost scale linearly (see section 4).
- Rate limits: model APIs generally scale by account tier and concurrency, but exact limits were not found; target-site rate limiting and IP blocking will bind first for repeated hits on large directory sites, whereas many independent small-business domains parallelise well.
- For the pilot, throughput should be measured, not assumed.

### Gaps
- Provider rate limits (requests/min, tokens/min) for DeepSeek, Qwen, Kimi, GLM, OpenRouter not retrieved.
- No measured crawl/block-rate data for local-business websites in target markets.
- No sourced vLLM or batched GPU throughput for the models discussed.

---

## 6. Security and compliance risks

### Takeaway
Running unvetted agent code with web and file access is a proven attack surface: the OpenClaw skills registry had hundreds of malicious entries, and indirect prompt injection works against commercial AI browsers today. Sending data to DeepSeek's own API means processing in China with no enterprise DPA (per secondary sources); self-hosting open weights or using US/EU hosts avoids that transfer but leaves GDPR scraping risk and provider and website terms.

### Cited Findings
**Supply chain and prompt injection**
- OpenClaw (self-hosted AI assistant, formerly Clawdbot/Moltbot): Koi Security's January 2026 audit of 2,857 ClawHub skills found 341 malicious, 335 from one campaign ("ClawHavoc") using fake prerequisites to install the Atomic Stealer macOS infostealer; counts later rose to over 1,184 by Feb 16 per one report, with Bitdefender placing it nearer 900 of an expanded 10,700-skill registry. Infostealer malware stole OpenClaw agent configs and gateway tokens. — [incidentdatabase.ai](https://incidentdatabase.ai/reports/6951/), [insiderllm ClawHub alert](https://insiderllm.com/guides/clawhub-malware-alert/), [bastion.tech](https://bastion.tech/blog/openclaw-infostealer-ai-agent-security-crisis), [ClawdPwned, ICLR 2026](https://iclr.cc/virtual/2026/10016269)
- OWASP ranks prompt injection first in its LLM Top 10 (LLM01:2025); indirect injection via web content is the class most often seen in real exploits. — [Aurascape summary of OWASP](https://aurascape.ai/answers/ai-browser-prompt-injection/)
- LayerX Security (2026-06-24) disclosed "BioShocking", an indirect prompt injection class that compromised six AI browsers and extensions, including products from OpenAI, Anthropic and Perplexity, enabling credential theft. — [CSA research note](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-browser-prompt-injection-20260630-csa-s/)
- Zscaler found hidden prompts, SEO manipulation and fake trust signals targeting agents that browse the open web; InjecAgent measured data-stealing attacks succeeding about 60% of the time without defences. — [Let's Data Science on Zscaler](https://letsdatascience.com/news/zscaler-finds-prompt-injection-campaigns-targeting-ai-agents-b88d1490), [Aurascape](https://aurascape.ai/answers/ai-browser-prompt-injection/)
- smolagents' LocalPythonExecutor has no security boundary. — [smolagents](https://github.com/huggingface/smolagents)

**DeepSeek and data residency**
- Italy's Garante ordered DeepSeek to block its chatbot in January 2025 and moved to remove its apps from app stores; Germany's data protection commissioner (June 2025) asked Apple and Google to delist the app citing illegal transfer of personal data outside the EU; app-store bans in South Korea, government-device bans in the Netherlands and Australia. — [Jurist](https://www.jurist.org/news/2025/06/germany-data-commissioner-orders-apple-and-google-to-remove-deepseek-over-data-concerns), [Malay Mail](https://www.malaymail.com/news/tech-gadgets/2025/06/29/global-scrutiny-grows-as-nations-curb-access-to-deepseek-amid-surveillance-and-misinformation-concerns/182027), [Introl](https://introl.com/blog/deepseek-government-bans-spreading-worldwide-2026)
- At least 17 US states have government-device bans; Texas first on 2025-01-31; federal agencies including Commerce and the Navy ban it on government devices. These target government devices and contractors; a secondary source says no US law stops private companies from API use as of 2026-04-24. — [BGR](https://www.bgr.com/2014815/deepseek-illegal-us-states/), [deepseekai.guide US restrictions](https://deepseekai.guide/news/deepseek-us-restrictions/) (low-authority aggregator, not verified against primary law)
- Secondary sources state the DeepSeek API sends prompts to servers in China under Chinese law, uses inputs for training by default with an opt-out, and offers no enterprise DPA, BAA, or EU/US residency. — [Sonomos](https://sonomos.ai/blog/is-deepseek-safe-gdpr-hipaa-2026/), [deepseekai.guide privacy](https://deepseekai.guide/guides/deepseek-privacy/) (not checked against DeepSeek's own policy, which was not fetchable)

**Scraping law and terms**
- Dutch DPA position: private-sector scraping will almost always violate GDPR for lack of a legal basis when personal data is involved; legitimate interest is the only realistic basis and requires a three-part test; public availability alone does not justify scraping; commercial interest weakens legitimate interest. — [Hogan Lovells](https://www.hlc.com/en/publications/dutch-dpa-issues-guidelines-on-data-scraping_1), [Pinsent Masons](https://www.pinsentmasons.com/out-law/news/dutch-web-scraping-guidance-warn-businesses-gdpr-breach-risk)
- Clearview AI fines for scraping: EUR 20M (Hellenic DPA) and EUR 30.5M (Dutch DPA) (face images, special category data, so an extreme case). — [EDPB](https://www.edpb.europa.eu/news/national-news/2022/hellenic-dpa-fines-clearview-ai-20-million-euros_en), [BankInfoSecurity](https://www.bankinfosecurity.net/dutch-agency-fines-clearview-ai-30m-euros-for-data-scraping-a-26205)
- Google Maps Platform terms bar scraping and caching Maps content beyond 30 days. — [ConductAtlas](https://conductatlas.com/platform/google-maps/google-maps-platform-terms-of-service/no-scraping-or-content-extraction/)

### Inferences
- Business records are mixed: company names, addresses and generic phone numbers are lower risk than sole-trader names, personal mobile numbers, emails and reviewer names, which are personal data under GDPR if EU persons are involved. Launch markets outside the EU have different regimes (not researched).
- Controls that match the risks: run agents in a disposable container or VM with no access to personal files or credentials; use scoped, low-limit API keys; no access to logged-in browser profiles; allow-list outbound domains where possible; do not install third-party skills or tools without code review and pinning; treat all page content as untrusted and constrain the LLM to schema-only output without tool calls on extraction passes.
- Data-residency: if any personal data is in the prompts, use open weights hosted by the team, or a US/EU host (Together, Fireworks) or Anthropic with `inference_geo`, rather than the DeepSeek first-party API. Using the open-weight DeepSeek model through a third-party host is a different risk from calling DeepSeek's own endpoint (inference; DeepSeek's terms not retrieved).

### Gaps
- DeepSeek, Moonshot, Alibaba and Zhipu terms of use on scraping or data-collection use cases not retrieved; likewise Anthropic and OpenAI usage policies on automated data collection.
- Primary-source confirmation for DeepSeek privacy policy details and current US federal law (secondary sources only).
- Non-EU data-protection regimes in target launch markets (for example Pakistan, Bangladesh, India) not researched.
- Primary pages for Koi/Bitdefender counts not fetched; counts vary between reports.
- No sourced security audits of Crawl4AI, Firecrawl, Browser Use, Skyvern or the other listed frameworks specifically.

---

## 7. Realistic recommendation and a small, measurable pilot

### Takeaway
Treat the claim as "model tokens are nearly free; everything else is not". Near-zero-cost parts: single-shot LLM extraction, normalisation, translation and dedup suggestions. Paid or human parts: unblocking, discovery via search or places data, verification, spot review, legal, security, and engineering. Test with a 1,000 to 2,000 record pilot and measure cost, accuracy and throughput per stage.

### Cited Findings
(Recommendations rest on the findings in sections 1 to 6; no additional sources.)
- Anthropic's own worked support-ticket example (about $0.0037 per item on Haiku 4.5) shows extraction-scale tasks cost fractions of a cent per item for tokens. — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- NEXT-EVAL shows input format drives accuracy and hallucination far more than model choice. — [arXiv 2505.17125](https://arxiv.org/pdf/2505.17125)

### Inferences
**Near-zero cost (with open-weight or cheap models)**
- Single-call extraction from cleaned markdown or flat JSON: about $0.0003 to $0.005 per record (Estimate) with Qwen Flash, GPT-5 nano, DeepSeek V4 Flash or Kimi.
- Classification, categorisation, language detection, translation or transliteration of names and categories, address normalisation, dedup candidate generation.
- Local small models (Qwen3 8B class) for high-volume low-stakes steps if accuracy on the target languages is proven.

**Needs paid services or humans**
- Fetching reliably: proxies or unblockers where sites block, plus CAPTCHA solving.
- Discovery of businesses: search APIs (about $1 to $5 per 1,000) or places data (about $50 to $80 per 1,000 records at Google list price, with licence limits).
- Verification: phone and email checks, spot human review (5% sample estimated at about $0.01 to $0.03 per record), and a human sign-off on quality targets.
- Legal review (GDPR and local law, site terms, API terms) and security setup.
- Engineering time, which is the largest unpriced item in the "free" claim.

**Pilot design (Estimate-based targets; adjust)**
1. Sample: 1,000 to 2,000 businesses across at least two launch markets and languages (Urdu, Bengali, Arabic, Hindi if relevant), including some with no website, some with JS-heavy or blocked sites, and some with only social pages.
2. Gold set: 300 records hand-verified by humans (name, category, address, phone, hours, website, language), to compute field-level precision and recall.
3. Arms (same input, same schema): (a) Scrapy or Crawl4AI plus single LLM call with DeepSeek V4 Flash; (b) same with Qwen3.7-Flash or GPT-5 nano; (c) same with Haiku 4.5 (quality ceiling); (d) local Qwen3 8B on a laptop; (e) optionally an agentic browser (Browser Use) arm on a 200-record subset to measure compounding.
4. Instrument per record: input and output tokens, dollars, proxy MB and cost, retries, block or CAPTCHA rate, wall-clock seconds, pass or fail on schema validation, and whether each field is grounded in source text.
5. Metrics and decision thresholds: field-level precision at or above 95% for contact fields after validation; hallucinated-field rate under 2%; verified-record yield; fully loaded cost per verified record (including human minutes and engineer hours logged); records per day per machine at a defined concurrency.
6. Security and compliance checks in the pilot: run in a sandbox with throwaway credentials; pin dependencies; no third-party skills; log all outbound requests; test a canary prompt-injection page to see if the agent obeys it; record what personal data (if any) enters prompts, and which provider region processes it.
7. Output: a one-page table of cost per verified record by arm and stage, so the claim "near zero" can be accepted or rejected on measured numbers.

### Gaps
- Pilot thresholds (95% precision, 2% hallucination) are my suggested targets, not sourced standards.
- Market-specific constraints for the target launch markets (site quality, language mix, legal regime, labour rates) were not researched in this note.

---

## Source quality notes for the report writer
- Strongest sources: Anthropic pricing page (primary, fetched live), GitHub repo pages (primary, page-view figures), arXiv papers (peer-unreviewed preprints; vendor reports self-reported).
- Weak or secondary: all non-Anthropic API prices (aggregators such as anotherwrapper, SiliconFlow, morphllm, costbench, use-apify), DeepSeek privacy and US-ban summaries (deepseekai.guide, Sonomos), Google Maps ToS summaries (ConductAtlas, Thunderbit). Conflicts noted inline.
- Blocked by the egress proxy: api-docs.deepseek.com, developer.puter.com, openrouter.ai. A GitHub API call via `gh` was refused for these repos, so GitHub web pages were fetched instead; last-commit dates were mostly not shown.
- Several search results returned summary text produced by the search tool; figures cited from them are only as reliable as the linked pages, which I could not all open.
