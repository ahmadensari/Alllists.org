# Global professional talent list (data scientists as the example): sources, legal limits, economics

Research date: 2026-10-05. Planning research, not legal advice.

Method and limits: web search worked. Direct page fetching was blocked by the network proxy for docs.github.com, kaggle.com, linkedin.com, news.linkedin.com, info.orcid.org, semanticscholar.org, gdpr-info.eu, cppa.ca.gov and proskauer.com. So platform terms are reported from search-result excerpts and secondary summaries, not read in full. Items marked UNVERIFIED rest on aggregator or vendor-blog sources, or on my background knowledge with no source retrieved in this session. Vendor pricing in third-party blogs is often SEO content and may be stale; treat it as indicative ranges only. No clause below has been checked against the live terms page.

## 1. Established sources: what is public, reuse terms, API

### Takeaway
Research-identity sources (ORCID public data file, OpenAlex) are the only sources found with explicitly open reuse terms (CC0). Platform sources (GitHub, Kaggle, Upwork, Hugging Face, Google Scholar) allow limited API or browsing use but restrict scraping, bulk collection or resale of personal data, and GitHub explicitly forbids selling user data to recruiters. A global list should therefore link to these sources through user consent rather than harvest them.

### Cited Findings
- ORCID: an annual Public Data File of all public data on claimed or created records is released under CC0 1.0, with no conditions on access or use. The same guidance says not to use emails for junk or unsolicited bulk mail, and to give people an opt-out if emails are used commercially. Record holders choose visibility (Everyone, Trusted parties, Only me), so only data set to "Everyone" is in the file. — [ORCID public data file / use policy (search excerpt)](https://info.orcid.org/public-data-file-use-policy); [ORCID public data file](https://info.orcid.org/orcid-public-data-file/)
- ORCID Public API use is covered by ORCID's Terms and Conditions of Use and Privacy Policy. — [ORCID terms of use](https://info.orcid.org/terms-of-use/)
- ORCID Trust Markers show which data was asserted by ORCID member organisations (institutions, publishers, funders). That makes ORCID a ready-made verification signal for researchers. — [ORCID public data file](https://info.orcid.org/orcid-public-data-file/)
- OpenAlex: the full dataset is a CC0 snapshot on a public AWS S3 bucket, with no account or key needed for bulk access. Since 13 Feb 2026 the API needs a free key and uses usage-based pricing. Reported free allowance is about $0.10/day with no key and about $1/day with a free key. Single-record lookups are free, and list/filter calls cost on the order of $0.0001 each. — [CASRAI summary of OpenAlex API keys and pricing](https://casrai.org/news/openalex-api-keys-mandatory-usage-based-pricing-2026) (secondary source, UNVERIFIED against openalex.org docs); docs index: [OpenAlex authentication](https://developers.openalex.org/api-reference/authentication.md)
- Semantic Scholar API: governed by an API License Agreement with AI2. Use is "at will" and AI2 can terminate it at any time without notice. An API key gives an introductory 1 request per second on all endpoints. Unauthenticated use shares a pool, reported as 1000 requests per second across all users. — [Semantic Scholar API licence page](https://semanticscholar.org/product/api/license) (search excerpt; full clauses on commercial use not read); [CASRAI guide](https://www.casrai.org/guides/semantic-scholar-api)
- Google Scholar: no official API. Excerpts say its terms prohibit automated queries, robots.txt has `Disallow: /scholar`, and IPs that query too fast are blocked. — [Search summary incl. R-bloggers on Scholar blocking](https://www.r-bloggers.com/google-scholar-still-sucks/) (secondary, UNVERIFIED against Google's current terms)
- GitHub: excerpts of the Acceptable Use Policies say you may not use the API to download data or content "for spamming purposes, including for the purposes of selling GitHub users' personal information, such as to recruiters, headhunters, and job boards." Scraping is tolerated for some uses, but user personal information may only be used for the purpose it was given. — [GitHub Acceptable Use Policies](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies) (search excerpt, page itself blocked); [GitHub blog on the terms change](https://github.blog/news-insights/the-library/new-github-terms-of-service)
- Kaggle: Terms of Use are a binding contract (version effective 4 Oct 2024 per search result). Scraper vendors sell Kaggle profile scrapers (name, join date, followers, title, location, bio), but I could not read what the terms say about automated access or reuse of profile data. Kaggle's official API rate limits for profiles were not found. — [Kaggle terms](https://kaggle.com/terms) (page blocked, UNVERIFIED clauses); [Crawlbase Kaggle scraping cookbook](https://crawlbase.com/cookbook/kaggle)
- Kaggle rank as a verification signal: a recruiting blog reports 23M+ users, 612 Grandmasters and 2,973 Masters, "verified through competition performance." — [Pin: find data science talent on Kaggle](https://www.pin.com/blog/find-data-science-talent-kaggle) (vendor blog, counts UNVERIFIED and likely dated)
- Kaggle ran a job board from 2014 to 2022 and then shut it down. — [Pin blog above](https://www.pin.com/blog/find-data-science-talent-kaggle) (secondary, UNVERIFIED). A Harvard case on Kaggle's early crowd model also exists: [Harvard D3 "Kaggle's Krowd Woes"](https://d3.harvard.edu/platform-digit/submission/3-kaggles-krowd-woes/index.html)
- Hugging Face: Hub APIs are rate-limited in 5-minute windows, with higher limits for PRO, Team and Enterprise. The Content Policy is incorporated into the Terms and covers privacy violations such as publishing others' personal information. Hugging Face has no dedicated public jobs board per a forum thread. — [HF rate limits](https://huggingface.co/docs/hub/en/rate-limits); [HF Content Policy](https://huggingface.co/content-policy); [HF forum: is there a jobs board?](https://discuss.huggingface.co/t/is-there-a-jobs-board/39711)
- Upwork: terms prohibit robots, spiders and scrapers without express written permission. Its API and MCP terms are reported to bar using the official surface to "enumerate or continuously monitor Upwork's available content corpus." — [ConductAtlas Upwork terms summary](https://conductatlas.com/platform/upwork/upwork-terms-of-service/prohibition-on-building-competing-services-using-upwork/); [UpHunt on Upwork scraping 2026](https://uphunt.io/blog/upwork-job-scraper-2026) (secondary, UNVERIFIED against upwork.com)
- Stack Overflow discontinued Stack Overflow Jobs and Developer Story on 31 March 2022, after the Prosus acquisition (reported at $1.8B, June 2021), judging talent acquisition not strategic. — [Hackajob on end of Stack Overflow Jobs](https://blog.hackajob.com/the-end-of-stack-overflow-jobs-heres-what-it-means-for-you/); [Dice](https://dice.com/career-advice/stack-overflow-jobs-and-developer-stories-ending-by-march-2022)

### Inferences
- Sources split into three tiers. (a) Open data, CC0: ORCID public file, OpenAlex. (b) API-licensed, conditional: Semantic Scholar, GitHub API, Hugging Face API, Upwork API. (c) Closed to bulk reuse: Google Scholar, LinkedIn, Upwork pages. Only tier (a) is safe for bulk ingestion, and it covers researchers only.
- For practitioner talent (Kaggle, GitHub, Hugging Face), the safe route is the person linking their own profile and confirming it, using their own OAuth or a code in their bio, then reading public data via the official API on their behalf. Whether each platform's terms allow this still needs checking.
- Two marketplace exits (Kaggle Jobs, Stack Overflow Jobs) suggest large developer communities struggled to turn talent access into a core business. Possible reasons (focus, low willingness to pay, matching difficulty) are not established by the sources found.
- Papers with Code, DBLP, conference speaker lists, university directories, ACM/IEEE/INFORMS and local societies, Toptal, Fiverr, Freelancer and open-source foundations were not researched here for lack of tool budget. They should be checked individually before any ingestion.

### Gaps
- Primary-text confirmation of Kaggle, GitHub, Hugging Face, Upwork and Semantic Scholar terms (pages blocked).
- Papers with Code (now folded into Hugging Face per my background knowledge, UNVERIFIED), DBLP licence (believed CC0, UNVERIFIED), professional associations' member-directory terms, Toptal/Fiverr/Freelancer API terms: not searched.
- Kaggle API user-profile endpoints and limits.

## 2. Off limits: LinkedIn, scraping law, personal-data rules, consent alternatives

### Takeaway
Scraping logged-out public data is not a federal crime in the US, but contract claims succeeded against hiQ. hiQ ended with a $500,000 judgment, a permanent injunction and deletion of data and code. In the EU and UK, a scraped list of people needs an Article 14 notice within one month. Regulators have fined firms that skipped it on "disproportionate effort" grounds, and a California registry now lets residents force deletion by data brokers.

### Cited Findings
- hiQ v. LinkedIn: in a November 2022 summary judgment order the N.D. Cal. court held that user-agreement provisions banning scraping and fake profiles were enforceable in a breach-of-contract claim, and that hiQ's scraping and fake profiles violated them. On 6 Dec 2022 the parties filed a stipulated consent judgment: $500,000 damages to LinkedIn, a permanent injunction against scraping or accessing LinkedIn in violation of the User Agreement, no fake accounts, and no using LinkedIn to build a commercial service without permission. hiQ also had to delete all source code, data and algorithms derived from the scraping. — [National Law Review](https://www.natlawreview.com/article/linkedin-s-data-scraping-battle-hiq-labs-ends-with-proposed-judgment); [Proskauer New Media Law blog](https://newmedialaw.proskauer.com/2022/12/08/hiq-and-linkedin-reach-proposed-settlement-in-landmark-scraping-case/); [ZwillGen](https://www.zwillgen.com/alternative-data/hiq-v-linkedin-wrapped-up-web-scraping-lessons-learned/)
- The earlier Ninth Circuit rulings (2019 and 2022) that scraping public pages is probably not "without authorization" under the CFAA are not in the excerpts retrieved. UNVERIFIED here, from background knowledge. The LinkedIn User Agreement clause on bots and scraping could not be read (linkedin.com blocked), so I do not quote it. Later cases (for example Meta v. Bright Data, 2024) were not searched. UNVERIFIED.
- GDPR Art. 14: where data is not obtained from the person, they must be informed within a reasonable period and at the latest within one month, or at first contact. UK ICO recruitment guidance says sourcing on professional networks can serve a legitimate interest, but a legitimate interests assessment is required and the interest cannot override the candidate's rights. — [TechGDPR on recruitment](https://techgdpr.com/blog/understanding-gdpr-compliance-in-recruitment/); [ICO recruitment guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/employment/recruitment-and-selection/data-protection-and-recruitment/) (search excerpt)
- Bisnode (Poland, UODO, 2019): fine of about EUR 220,000 for not giving Art. 14 notices to scraped business-owner records. Bisnode had emails for few of about 5.7 million people and called the cost of postal notice disproportionate (about EUR 7.7M for postage). UODO held notification was neither impossible nor disproportionate and ordered Bisnode to contact them. — [Blake Morgan](https://www.blakemorgan.co.uk/digital-marketing-agency-bisnode-fined-by-the-polish-dpa-for-failing-to-be-transparent-with-data-subjects/); [IAPP](https://iapp.org/news/a/polands-dpa-issues-first-gdpr-fine/)
- Clearview AI: CNIL fined it EUR 20M in Oct 2022 for scraping public sources and social media, and ordered it to stop and delete. It is biometric data, so a harsher case than professional profiles. — [Sophos](https://www.sophos.com/en-us/blog/zut-alors-raclage-crapuleux-clearview-ai-in-20-more-trouble-in-france)
- US/California: the CCPA exemptions for employee and B2B contact data expired on 1 Jan 2023, so CCPA/CPRA now applies in full to job applicant and business-contact data of California residents of covered businesses. "Publicly available" is narrow and tied largely to government records. — [Steptoe on the extensions](https://www.steptoe.com/en/news-publications/cyberblog/california-extends-exemptions-from-ccpa-for-b2b-and-employee-information.html); [Privacy Law Map](https://privacylawmap.com/blog/ccpa-exemptions-guide-who-is-exempt) (secondary)
- California Delete Act: the CPPA's DROP platform lets a resident send one deletion request to all registered data brokers. From 1 Aug 2026 more than 600 registered brokers must process DROP requests, accessing it at least every 45 days. SB 361 is reported to have doubled the daily fine for failing to register from $100 to $200. More than 300,000 Californians had signed up by spring 2026 per one report. — [TrustArc](https://trustarc.com/resource/california-delete-act-drop-platform-data-brokers/); [Malwarebytes, Aug 2026](https://www.malwarebytes.com/blog/news/2026/08/californians-can-tell-data-brokers-to-drop-their-informatio); [CPPA DROP page](https://cppa.ca.gov/data_brokers); [Alston & Bird](https://www.alstonprivacy.com/drop-is-coming-due-what-californias-delete-act-means-for-data-brokers-in-august/) (secondary; fee figure UNVERIFIED)
- Platform contracts bind beyond law: GitHub bars selling user data to recruiters (see section 1), and ORCID asks for opt-out where email is used commercially.

### Inferences
- Even where scraping is not a crime, a list built from scraped platform data risks (i) breach-of-contract claims and account bans, (ii) GDPR Art. 14 notice duty for every EU/UK person, plausibly at a cost that makes the model uneconomic, (iii) California data-broker registration if AllLists sells data about people it has no direct relationship with, and DROP deletions every 45 days.
- Whether a consent-only, self-registered directory counts as a "data broker" under California law depends on the first-party-relationship test. I did not verify this. Counsel should confirm.
- Consent-based alternatives: self-registration, "Sign in with ORCID", OAuth to GitHub/Kaggle/Hugging Face to prove ownership, opt-in profile visibility, and recruiter contact routed through the platform. All keep AllLists in a first-party role and avoid Art. 14.

### Gaps
- Other jurisdictions' people-search and recruiting-database rules (Vermont, Texas, Oregon broker laws; Brazil LGPD; India DPDP Act; Canada) not searched.
- Xing and similar terms not searched.
- Primary text of LinkedIn's User Agreement and of GDPR Art. 14(5) exemptions (page blocked); CJEU or EDPB views on "public data" reuse not searched.
- Developments in LinkedIn enforcement after 2022 (for example suits against scraper vendors) not searched.

## 3. Economics: what buyers pay

### Takeaway
Recruiters pay about $100 to $300 per seat per month for entry-level sourcing tools and roughly $8,000 to $15,000 per seat per year for LinkedIn Recruiter Corporate. Contact-data vendors (ZoomInfo, Apollo) sell on credits or contracts of $15,000 or more per year. Marketplaces monetise through take rates: Upwork about 18.7%, Fiverr about 27.7%, and Toptal through an undisclosed client markup.

### Cited Findings
- LinkedIn Recruiter Lite: reported at $170/month on annual billing or $270/month monthly, with seats 2 to 5 at $270 each. Recruiter Corporate is "contact sales." Third parties report about $8,000 to $12,000 per seat per year (Vendr data) and buyer reports of $8,999 to $15,000, with 2026 renewals at $10,000 to $12,960 after a price increase. — [Dover, June 2026](https://www.dover.com/blog/linkedin-recruiter-lite-vs-professional); [Pin LinkedIn Recruiter pricing 2026](https://www.pin.com/blog/linkedin-recruiter-pricing-2026/); [GoPerfect](https://www.goperfect.com/blog/linkedin-recruiter-pricing-plans-and-costs-for-hiring-teams-in-2026) (vendor and recruiter blogs, UNVERIFIED against LinkedIn)
- LinkedIn revenue: aggregator pages say LinkedIn revenue is above $18B a year, with Talent Solutions at about $7.8B (43%), and that agentic hiring products passed a $450M annual run rate, in a quarter where LinkedIn revenue grew 12% (Q3 FY26). These figures come from secondary pages. I could not retrieve Microsoft's 10-K or LinkedIn's own release. — [LinkedIn Q3 FY26 highlights](https://news.linkedin.com/2026/Q3-Earnings-Highlights) (page listed, not fetched); [Fueler](https://fueler.io/blog/linkedin-in-usage-revenue-valuation-growth-statistics) (aggregator); [ThinkInsights](https://thinkinsights.net/strategy/linkedins-professional-network-business-model) (aggregator). Treat all as UNVERIFIED.
- SeekOut: entry plan Recruit Core at $149/user/month annual ($179 monthly); higher tiers and API access are custom quoted. — [FabricHQ](https://fabrichq.ai/blogs/seekout-pricing); [Noon](https://www.noon.ai/blog/articles/250-seekout-pricing-2026)
- hireEZ: no flat published rate. Solo plans reported from $494/month, and third-party estimates of $169, $199 and $250+ per user per month. — [GoPerfect hireEZ pricing](https://www.goperfect.com/blog/hireez-pricing-in-2026-plans-costs-and-how-it-compares)
- Gem: custom pricing keyed to company headcount. Entelo: quote-based at roughly $5,000 to $10,000 per seat per year. Findem: no price found. — [Dupple](https://dupple.com/learn/best-ai-sourcing-tools); [FabricHQ hireEZ](https://fabrichq.ai/blogs/hireez-pricing)
- Juicebox (PeopleGPT): Starter $99/seat/month annual ($119 monthly), Growth $179 annual ($199 monthly), custom Business plan. Agents add $199/agent/month. Contact credits capped at 500/month (Starter) and 1,500/month (Growth). — [Paraform on Juicebox](https://www.paraform.com/insights/juicebox-ai-pricing); [HeroHunt](https://www.herohunt.ai/blog/juicebox-pricing-2026-cost-and-alternatives/)
- ZoomInfo: contracts reported from about $14,995/year with a three-seat minimum, median signed about $33,500/year, SMB average about $48,524 and enterprise average about $166,802. Apollo: Basic $49, Professional $79, Organization $119 per seat/month on annual billing, with 2,500, 4,000 and 6,000 credits per seat/month. A verified email costs 1 credit and a phone number 8. — [SpendHound](https://www.spendhound.com/blog/zoominfo-pricing); [Valley on Apollo](https://www.joinvalley.co/blog/apollo-pricing-and-credits-explained-2026) (third-party, UNVERIFIED)
- Upwork FY2025 (10-K): marketplace revenue $682.9M (+3%), marketplace take rate 18.7% (18.0% in 2024), total revenue about $787.8M, about 785,000 active clients. Freelancer fee moved on 1 May 2025 from 20/10/5% tiers to a variable 0 to 15%. — [Upwork 10-K FY2025 (SEC)](https://www.sec.gov/Archives/edgar/data/1627475/000162747526000012/upwk-20251231.htm) (numbers via search excerpt of the filing); [Golance on Upwork fees](https://golance.com/blogs/upwork-fees-explained-2026)
- Fiverr FY2025: revenue $430.9M (+10.1%), 3.1M annual active buyers (down 13.6%), spend per buyer $342, blended take rate 27.7%. Freelancer commission is a flat 20%. — [Kavout on Fiverr FY2025](https://www.kavout.com/market-lens/what-does-fiverr-s-q4-and-full-year-2025-report-really-tell-us) (secondary; check against Fiverr's 20-F); [WebsiteRating on Fiverr fees](https://websiterating.com/blog/productivity/fiverr-fees-explained)
- Toptal: freelancers keep their negotiated rate and Toptal takes an undisclosed client markup. Third-party estimates put it at 40 to 60%. Clients pay $60 to $250+/hour. — [The Frontend Company on Toptal pricing](https://www.thefrontendcompany.com/posts/toptal-pricing) (UNVERIFIED estimate, not from Toptal)
- Buyers: recruiters, startups and staffing firms are the named buyers in vendor material. Universities and governments as buyers of talent lists were not evidenced in any source found.
- Hired: a search result says Vettery acquired Hired when it was set to wind down. I could not confirm dates or later history. — [Global Venturing](https://globalventuring.com/vettery-settles-hired-acquisition) (UNVERIFIED)

### Inferences
- The price ladder is: contact credits at a few dollars or less; $100 to $250 per seat per month for tools with AI search; $8,000 to $15,000 per seat per year for LinkedIn's full Recruiter. The price reflects the size of the searchable pool (LinkedIn) rather than the quality of any single record.
- Marketplaces earn by taking 10 to 28% of billings on placed work, not by selling lists. A list that routes hires through its own platform could earn on this basis, but only with payment flow. Fiverr's falling buyer count shows marketplace demand is not guaranteed.
- Kaggle Jobs and Stack Overflow Jobs closing suggests a pure job board on a developer community is hard to sustain.

### Gaps
- Primary Microsoft 10-K segment figures for LinkedIn and Talent Solutions; LinkedIn's own product pricing pages.
- Gem and Findem price points; per-contact prices for individual (not company) data across vendors; Toptal's actual margin.
- Recruiter-community pricing from Hired, Hackajob, Wellfound, Turing, Deel or similar.
- Buyer segments such as universities and governments: no data found.
- Kaggle or Hugging Face recruiting products with prices: none found.

## 4. Value of a niche, consent-based list versus scraped data

### Takeaway
Little hard evidence on pricing was found. Diversity-focused AI and data science groups (Black in AI, Women in AI directories, AIAI) monetise through sponsor and recruiter access, with conferences and events as the channel, not through per-record list sales.

### Cited Findings
- Black in AI: first event at NeurIPS 2017. At its annual conference, participants are connected to AI research teams at large firms recruiting talent. Leading sponsors fund travel grants. Email and Facebook group communities of about 800 and 1,200 members were reported (dated figures). — [Wikipedia: Black in AI](https://wikipedia.com/wiki/Black_in_AI); [TPInsights](https://tpinsights.com/the-private-group-pushing-black-tech-talent-into-ai-jobs/)
- Alliance for Inclusive AI (AIAI, Berkeley-based) lists corporate sponsors and used a fundraising deck to fund mentorship and training. — [AIAI fundraising deck (2020)](https://aiai.berkeley.edu/wp-content/uploads/2020/09/AIAI-Fundraising-Deck.-CB.pdf)
- Re-Work published a "Top Women in AI" directory (2020). — [Re-Work blog](https://blog.re-work.co/top-women-in-ai-2020-directory/). The Alan Turing Institute (Southampton) launched a Women in Data Science and AI hub as a community resource, not a paid service. — [Southampton/Turing](https://www.southampton.ac.uk/the-alan-turing-institute/news/2019/10/women-in-data-science-and-ai.page)
- Kaggle claims its rankings verify skills by performance. — [Pin](https://www.pin.com/blog/find-data-science-talent-kaggle) (vendor blog)
- ORCID Trust Markers and the CC0 public file show that verified, opt-in researcher identity is already available at no cost. — [ORCID](https://info.orcid.org/orcid-public-data-file/)

### Inferences
- The advantage of a consent list is that records carry current availability, rates and a contact route the person chose, which scraped records lack. Scraped data has freshness and legal-notice problems (section 2). I found no source comparing reply rates or price per contact for consented versus scraped data, so this is reasoning, not evidence.
- The niche directories found do not run as self-funding list businesses. They are community, event or sponsor models. The only direct evidence of buyer willingness to pay is for large search tools (section 3).
- A narrow, verified pool (for example Kaggle Masters and Grandmasters, a few thousand people per the Pin figure) is small enough that per-seat subscription revenue would be limited. Success-fee or intro-fee models are likelier.

### Gaps
- No pricing, revenue or buyer data for named niche directories (Women in Tech, regional AI directories, Black in AI).
- No data on response rates for opt-in versus scraped outreach.

## 5. Global versus local

### Takeaway
No source found compares global and local lists directly. For remote professions the evidence points to skill, availability and rate as the matching dimensions, with verification by competition rank, publications or portfolio.

### Cited Findings
- Upwork and Fiverr, the main remote-talent marketplaces, price on take rate rather than geography. Freelancer rates are negotiated per person, and Toptal clients pay $60 to $250+/hour by role. — [Upwork 10-K FY2025](https://www.sec.gov/Archives/edgar/data/1627475/000162747526000012/upwk-20251231.htm); [The Frontend Company](https://www.thefrontendcompany.com/posts/toptal-pricing)
- Available verification signals: Kaggle competition tiers (Pin), ORCID Trust Markers, and OpenAlex/Semantic Scholar publication records (section 1).

### Inferences
- A remote buyer filters on skills, rate and time zone overlap, not country. A global list needs rate and availability fields that go stale quickly, so it needs a re-confirmation cycle (for example a 90-day check-in). This is an assumption.
- Local lists matter where law, language or in-person work applies (public-sector, regulated sectors, translators for local certification). Global suits data scientists, software engineers, designers and researchers.
- Legal exposure is global: a worldwide list has EU/UK, California and other privacy-law subjects from day one.

### Gaps
- No data on remote-hiring geography, rate dispersion across countries, or time-zone filters in recruiter tools.
- No source on verification practice in translators or designers (certifications, portfolios).

## 6. Conclusion for AllLists

### Takeaway
A consent-based global data scientist list is viable if it is built on self-registration with proof-of-ownership links (ORCID, GitHub, Kaggle, Hugging Face), tiered verification, and paid access for buyers. It stays outside LinkedIn-style scraping risk and the Art. 14 and data-broker regimes. Revenue is plausible from a seat subscription priced at the low end of recruiter tools or from placement and intro fees. Demand evidence is still thin.

### Cited Findings
- (Evidence base for the design is in sections 1 to 5; no further citations here.)

### Inferences
Design (my proposal, not sourced):
- Entry: self-registration with email, and optional "Sign in with ORCID". The person chooses visibility, rates, availability and contact preference. Profiles can be deleted at any time.
- Verification levels:
  - L0, email-verified, self-declared.
  - L1, linked accounts proven by OAuth or a code in the profile (GitHub, Kaggle, Hugging Face, ORCID), with public stats pulled via official APIs for the linked user only.
  - L2, evidence-backed claims: Kaggle Master or Grandmaster tier, ORCID Trust Markers or OpenAlex-matched publications, merged open-source work.
  - L3, human or test review (portfolio check, short skills assessment, reference), for paid placement.
- Data sources: use CC0 data (ORCID public file, OpenAlex) only to seed claim-your-profile pages for researchers. That case has more legal risk, because creating a page about someone without consent would raise Art. 14 duties. Safer: use these sources only to match data after a person registers.
- Buyers and prices (price points anchored to section 3, adoption unproven): recruiters, startups and small staffing firms at roughly $100 to $250 per seat per month (similar to Juicebox, SeekOut Core, hireEZ low tiers); teams at several thousand dollars per year; optional intro fee or success fee per hire (marketplace take rates of 10 to 28% give a ceiling for reference). Universities and governments (research hiring, challenge sponsors) are possible but unevidenced. Sponsor revenue from challenges and events is the niche-directory model.
- Contact route: the platform mediates contact. Buyers do not receive bulk exports, which also fits GitHub's and ORCID's anti-spam terms.
- Legal risks for counsel to review: (1) GDPR/UK GDPR controller duties even on consent (withdrawal, access, retention, international transfers); (2) whether California data-broker registration applies; (3) platform terms on API use for a commercial directory (GitHub, Kaggle, Hugging Face, Semantic Scholar all need reading in full); (4) discrimination and bias rules if rates or ranks are used for filtering; (5) fake profiles and rank spoofing; (6) email deliverability and anti-spam law (CAN-SPAM, PECR, CASL).
- Other professions: the same approach fits software engineers (GitHub), researchers (ORCID, OpenAlex) and designers or translators (portfolio, certification) if a free, API-readable proof source exists. Where no proof source exists, verification falls back to L0 or L3 review, and the list loses its main advantage over general marketplaces such as Upwork. Data science and research have the strongest proof signals found in this research.

### Gaps
- Willingness-to-pay by real buyers for a small consented list: no survey or comparable found. A pilot or buyer interviews would be needed.
- Counsel review of every legal point above.
- The sources not yet checked (section 1 gaps) should be completed before launch.
