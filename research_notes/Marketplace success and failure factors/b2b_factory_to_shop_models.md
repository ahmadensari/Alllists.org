# B2B factory/brand-to-small-shop models: cases, economics, leakage, demand data, and a lighter-weight alternative

Research caveats (read first): WebFetch was blocked by the egress proxy for sacra.com, resolvepay.com, propakistani.pk, scmp.com and entrackr.com, so almost everything below comes from WebSearch result summaries, not from full-page reads. Figures from aggregators, vendor blogs and AI-generated "template" sites are marked (unverified). Where two sources conflict, both are listed. Nothing here comes from primary filings except the Alibaba SEC 6-K/20-F snippets. Search date: October 2026.

## 1. Models and cases: which won, which failed, funding raised and outcome

### Takeaway
Horizontal "brand-to-independent-retailer" wholesale marketplaces consolidate into one winner per region (Faire in the US, Ankorstore in Europe). Others were shut down (Tundra) or absorbed (Handshake), and the loss-making Indian and Pakistani models that owned inventory, credit and delivery (Udaan, Retailo, Jugnu, Dastgyr, Bazaar) cut staff, shut distribution or retrenched after raising large sums. Winners are asset-light software and payments layers over brand-owned fulfilment. Losers tried to replace the distributor's physical logistics and credit function with venture capital.

### Cited Findings

**Winners / survivors (Western wholesale marketplaces)**
- Faire: a headline said it raised $400M at a $12.4B valuation (Nov 2021), and another headline said $260M at $7B (year not shown in the snippet, likely 2022, unverified). Aggregator data puts a Nov 2025 valuation at $5.2B, a 10.4x multiple on about $500M revenue, led by WCM Investment Management with Baillie Gifford and True North (unverified). Total disclosed capital is about $1.7B (aggregator, unverified). — [Retail TouchPoints (2021)](https://retailtouchpoints.com/topics/inventory-merchandising/400-million-funding-round-pushes-wholesale-marketplace-faires-value-to-12-4b); [DTNext](https://www.dtnext.in/news/business/online-wholesale-marketplace-faire-raises-usd-260-mln-valued-at-usd-7-bln); [multiples.vc](https://multiples.vc/private-comps/faire)
- Faire scale (aggregator-sourced, unverified): "700,000+ independent retailers and 100,000+ brands" in late 2025; "$6.8B GMV 2025" is flagged by the same source as varying between sources. — [Sacra chat summary](https://sacra.com/chat/h/adf545c3-1917-4574-9616-2afe6062efc1)
- Ankorstore (France): €250M Series C in Jan 2022 led by Bond and Tiger Global, with Eurazeo and Coatue, at €1.75B valuation (TechCrunch's headline calls it a $2B valuation, two years after launch). It cited 200,000 retailers and 15,000 brands across Europe and sales up 950% 2020 to 2021. — [TechCrunch (2022)](https://techcrunch.com/2022/01/09/ankorstore-reaches-2-billion-valuation-two-years-after-launching-its-wholesale-marketplace); [FashionUnited (2022)](https://fashionunited.uk/news/business/ankorstore-raises-250-million-euros-in-series-c-funding-round/2022011060488)
- Ankorstore handled logistics for about €350M GMV in 2025 (snippet is ambiguous about whether this is total GMV or only the logistics-handled part, unverified). — [Garnet Marketplace profile](https://garnetmarketplace.com/marketplaces/ankorstore.html)
- Orderchamp (Amsterdam, founded 2019): about $20M (EUR 16.6M) Series A in May 2021 led by Prime Ventures (with henQ and angels). At the time it reported 1,800+ active brands and 30,000+ retailers across NL, BE, DE, FR and LU. Current status (2024 to 2026) not found. — [Tech.eu (2021)](https://tech.eu/2021/05/06/amsterdam-based-e-commerce-platform-orderchamp-raises-20-million-seeks-to-sew-up-european-market); [EU-Startups (2021)](https://www.eu-startups.com/2021/05/dutch-wholesale-marketplace-orderchamp-raises-e16-6-million-to-expand-further-across-europe/)

**Failures / absorbed (US)**
- Tundra: raised about $38M (Emergence, Redpoint), reached 30,000+ retailers, and announced in July 2023 it was shutting its marketplace. Tundra blamed Faire's "anticompetitive conduct, unfair policies, and punitive enforcement of exclusive arrangements" and claimed Faire holds about 90% of online wholesale marketplaces. Faire counter-sued the same day, alleging unauthorised computer access. — [Resolve Pay blog (vendor with an interest in the topic)](https://resolvepay.com/blog/tundra-shut-down); [Business of Home (2023)](https://businessofhome.com/articles/inside-the-lawsuit-between-b2b-digital-marketplaces-faire-and-tundra); [Digital Commerce 360 (2023)](https://www.digitalcommerce360.com/2023/09/11/faire-tundra-lawsuit-b2b-marketplaces/)
- The court dismissed Tundra's antitrust claims in Feb 2024 on market definition and later dismissed them with prejudice (2025). — [Paul Weiss (law firm for Faire)](https://www.paulweiss.com/insights/client-news/faire-wholesale-wins-dismissal-with-prejudice-of-monopolization-claims); [Bloomberg Law](https://news.bloomberglaw.com/antitrust/faire-wholesale-again-escapes-antitrust-claims-brought-by-rival)
- Handshake: Shopify "quietly acquired" it in 2019. It was folded into Shopify's B2B wholesale tooling. Price not found in the snippet. — [TechCrunch (2019)](https://techcrunch.com/2019/05/23/shopify-quietly-acquired-handshake-an-e-commerce-platform-for-b2b-wholesale-purchasing/amp/)

**India**
- Udaan: GMV was Rs 9,900 cr in FY22, Rs 5,609 cr in FY23 and Rs 5,707 cr in FY24 (+1.7%). Net loss was Rs 2,076 cr in FY23 and Rs 1,674 cr in FY24. Valuation fell more than 59%, from $3.2B at peak to $1.3B. Management claimed EBITDA burn cut 40% a year and group EBITDA profitability within about 18 months (a company claim). It raised Rs 300 cr in debt (Lighthouse Canton, Stride, InnoVen, Trifecta). — [Entrackr (FY24)](https://entrackr.com/fintrackr/udaans-growth-stalls-mid-flight-losses-down-19-in-fy24-7452166); [Entrackr (debt)](https://entrackr.com/news/udaan-raises-rs-300-cr-debt-from-lighthouse-canton-and-others-7367717)
- Udaan also closed a $114M Series G, bought ShopKirana to push profitability and an FMCG focus, and a headline reports a $160M raise and "streamlining for public market debut" (details not verified; the date is unclear). — [Inc42 Series G](https://inc42.com/?p=516452); [Inc42 ShopKirana](https://inc42.com/?p=523483); [Parsers.vc](https://parsers.vc/news/260716-udaan-secures-160-million--streamlines-for)
- Ninjacart (fresh produce, so only partly comparable): FY24 gross revenue Rs 2,002.7 cr (+74%) with adjusted loss Rs 259.6 cr (down 20%). Its $145M round from Walmart and Flipkart valued it above $800M (2021). A 2024 raise of $60M at about Rs 5,850 cr valuation is from weaker sources (unverified). — [Entrackr](https://entrackr.com/fintrackr/ninjacart-claims-rs-2002-cr-in-gross-revenue-for-fy24-7372513); [Inc42 (Flipkart round)](https://inc42.com/?p=271151); [Clay dossier](https://clay.com/dossier/ninjacart-funding)
- Meesho (a reseller-led social-commerce marketplace, not a factory-to-shop model): zero seller commission on most categories, monetised through logistics fees, ads and services. FY25 operating revenue was Rs 9,390 cr on NMV of about Rs 30,000 cr, an effective "take" of about 31% that is mostly shipping and so not comparable to a commission (aggregator figures, unverified). Its IPO opened 3 Dec 2025 to raise about Rs 5,421 cr at about $5.8B. — [Zerodha Daily Brief](https://thedailybrief.zerodha.com/p/inside-meeshos-ipo); [Entrepreneur India](https://india.entrepreneur.com/en-in/news-and-trends/meesho-ipo-to-open-on-december-3-key-things-to-know/500210)

**Pakistan**
- Jugnu: shut core operations in July 2023, a year after raising $22.5M, pivoting away from self-managed fulfilment and logistics to a "tech-platform play". — [ProPakistani (2023)](https://propakistani.pk/2023/07/16/jugnu-shuts-down-its-core-operations-a-year-after-raising-22-5-million/)
- Retailo (Riyadh-based, active in Saudi, Pakistan and the UAE): $2.3M pre-seed, $6.7M seed, $36M Series A in Feb 2022 ($29M equity, $7M debt), about $45M in total, and it bought UAE's DXBUY. One summary says it shut distribution operations in Oct 2023, but I found no direct article confirming this and a second search found no shutdown news (conflict, unverified). — [AgFunder News (2022)](https://agfundernews.com/retailo-raises-36m-series-a-funding-from-agfunder-graphene-others); [Gulf News](https://gulfnews.com/business/corporate-news/retailo-further-strengthens-presence-in-mena-by-acquiring-uaes-dxbuy-1.1650613162301); [Profit/Pakistan Today](https://profit.pakistantoday.com.pk/?p=161891)
- Dastgyr: $37M Series A in June 2022 (the largest Pakistani Series A reported; Bloomberg). Layoffs: one search summary says about 85% of staff, another says 50-60% of over 500 staff (conflict). — [Bloomberg (2022)](https://www.bloomberg.com/news/articles/2022-06-14/pakistan-e-commerce-startup-raises-record-37-million-series-a); [Profit/Pakistan Today](https://profit.pakistantoday.com.pk/?p=160497)
- Bazaar Technologies: $30M Series A in Aug 2021 (Defy, Wavemaker), then a $70M Series B led by Dragoneer and Tiger Global (year not shown in the snippet, unverified), for more than $100M in total. It claims 1M+ merchants, 500+ towns and 200+ brands. It laid off about 600 and wiped out its Lahore field force, but said its core B2B retail arm would continue. — [TechCrunch (2021)](https://techcrunch.com/2021/08/23/pakistans-b2b-marketplace-and-digital-ledger-platform-bazaar-raises-30-million); [Gulf News](https://gulfnews.com/business/retail/pakistans-ecommerce-startup-bazaar-raises-70m-in-funding-1.86460830); [Profit/Pakistan Today](https://profit.pakistantoday.com.pk/?p=161891)
- Combined, Jugnu, Retailo and Dastgyr raised $161.4M (per the press summary). — [Profit/Pakistan Today](https://profit.pakistantoday.com.pk/?p=161891)

**China and Africa**
- Alibaba 1688.com (domestic wholesale) had 990,000+ paying members at 31 Mar 2021, and value-added services were over 50% of its revenue in the 12 months to that date. Alibaba.com is the international wholesale platform, with buyers in about 190 countries in FY2020. — [Alibaba 6-K FY2021 (SEC)](https://www.sec.gov/Archives/edgar/data/1577552/000110465921096324/a21-17183_36k.pdf); [Alibaba 20-F FY2020 (SEC)](https://www.sec.gov/Archives/edgar/data/1577552/000110465920082409/baba-20200331x20f.htm)
- Ling Shou Tong (LST): a Taobao-Tmall (TTG) project that began inside 1688. It connected FMCG brands and their distributors to small retailers via an app, with next-day restock from city warehouses or two-day restock from regional warehouses and POS tools, and aimed to digitise China's roughly 6M convenience stores. A 2018 Coresight briefing described it as a way for Alibaba to strengthen distribution, last-mile and local-market knowledge. Alibaba announced it would "temporarily halt operations" on 30 Mar 2024 for "business adjustments", while saying it was not merging with 1688. — [SCMP (2024)](https://www.scmp.com/tech/article/3256426/alibaba-suspends-operations-lst-platform-consolidation-moves-continue-apace); [Coresight (2018)](https://coresight.com/research/china-tech-briefings-ling-shou-tong-alibaba-leverages-independent-convenience-stores-to-gain-a-competitive-advantage-in-new-retail); [Flourish Ventures Digital Corner Shop report (2022)](https://digitalcornershop.flourishventures.com/global-report)
- Jumia: the searches returned only its 2019 exits from Tanzania and Cameroon and a 6% Kenya layoff (all consumer e-commerce). I found no reliable source on a Jumia B2B product (gap). — [Citizen Digital (2019)](https://www.citizen.digital/article/jumia-shuts-operations-tanzania-305851)

**Big-tech B2B**
- Amazon Business launched in 2015, passed $1B in its first year and $25B by 2021, and is above $35B in annual sales with 8M+ customers. — [Modern Distribution Management](https://www.mdm.com/news/ecommerce/marketplaces/now-10-years-in-amazon-business-surpasses-8m-customers/); [Manufacturing.net](https://www.manufacturing.net/e-commerce/news/22948384/amazon-business-accounts-for-over-35b-in-annual-sales-company-says)

### Inferences
- Pattern: winners (Faire, Ankorstore, IndiaMART, Meesho) let the supplier keep the physical logistics, or push the cost onto it, and monetise through payments and credit, software, ads or leads. Losers or retrenchers (Udaan, Jugnu, Retailo, Dastgyr, Bazaar, LST) owned warehouses, field forces, delivery fleets and credit book exposure. This follows from the dates and outcomes above, but no source states it as a general rule.
- Faire's valuation went from $12.4B (2021) to about $5.2B (2025, unverified), so even the category winner re-rated sharply. The market is large but not high-margin software.
- Tundra's failure shows second place is not viable in a two-sided wholesale network where exclusivity and network effects favour the incumbent. A new entrant should not copy a horizontal marketplace head-on. (Faire denied the allegations and the court dismissed the claims, so the exclusivity allegation is unproven.)
- LST's pause, despite Alibaba's resources, suggests that even with deep logistics, a brand-distributor-retailer ordering layer was not worth operating on Alibaba's economics. The reasons are not public.

### Gaps
- Faire's audited revenue, GAAP take rate and retailer cohort retention: Faire is private and Sacra was blocked. The "68% repeat-retailer retention", "take rate 16.5% to 19%" and "$2.8B Faire Direct GMV" figures came only from an AI-generated aggregator summary and are not used as facts.
- Whether Orderchamp is still operating, and its later funding.
- Tundra's and Handshake's exact acquisition or exit economics, and Jumia B2B.
- Primary confirmation of Retailo's status after 2023 and the Dastgyr layoff percentage.
- Walmart/Costco wholesale: the searches returned no usable material on small-shop wholesale programmes. Taobao Xiaodian / Tmall Xiaodian: nothing specific found beyond the LST descriptions above.

## 2. What distributors do that factories cannot easily replace; take rates; credit risk and logistics handling

### Takeaway
Distributors sell a bundle: stocking, small-lot breaking, weekly sales visits, unsecured credit, collections and compliance. One analysis values that bundle at about 11.5% of the retail price against a typical 5-6% distributor margin, so the distributor is cheap for what it does. Platforms that succeed charge about 15-19% (Faire) or a subscription (IndiaMART) and take credit risk onto their balance sheet or through partners, not by pretending credit does not matter.

### Cited Findings
- Services such as inventory stocking, small-order dispatch and unsecured zero-interest retailer credit are valued at about 11.5% of the final merchandise price, against the 5-6% margin distributors typically take. This comes from the MIT-linked Supply Chain Management Review piece on e-B2B in India's fragmented retail (the snippet's attribution of 11.5% to the article is not confirmed). — [SCMR](https://www.scmr.com/article/e_b2b_distribution_strategies_for_fragmented_retail_environments_saving_ind)
- India has about 12M kirana stores, which place small orders, deal with many exclusive distributors and carry many brands, so cost-to-serve is high. Distributors visit kiranas about once a week. — [Kirana Club guide](https://kirana.club/resources/fmcg-distribution-india-guide); [Kotak Neo](https://www.kotakneo.com/investing-guide/insights/fmcg-distributor-disruption-quick-commerce/)
- Retailer margin expectations quoted by a Kirana Club summary: 5-10% for strong national brands, 10-18% for regional brands, 18-25%+ for new brands entering new states. Distributor prices give retailers margins of about 10-12%, against up to about 20% on app prices (practitioner source, unverified). — [Kirana Club margins](https://kirana.club/resources/fmcg-distributor-kirana-margins)
- Distributors relieve brands of compliance complexity and have been able to organise boycotts against brands that go direct (a WARC headline on traditional distributors suspending brand boycotts). — [WARC](https://www.warc.com/content/feed/indias-traditional-distributors-suspend-brand-boycotts/en-GB/5125); [The Ken, "HUL, ITC and the direct-reach quandary"](https://the-ken.com/tradetricks/hul-itc-and-the-direct-reach-quandary/)
- Faire fees: 15% commission on marketplace orders plus $10 on a retailer's first order; reorders carry 15% with no flat fee; Faire Direct (brand-invited retailers) is 0% commission with only payment processing of 1.9-3.5% depending on payout speed and a $0.30 payment fee. Effective cost is about 19% with processing included. — [Craftybase fee guide](https://craftybase.com/blog/how-to-sell-on-faire-wholesale-guide); [Wholesale Helper](https://wholesalehelper.io/blog/selling-on-faire-vs-having-your-own-store/); [EightX analysis](https://eightx.co/blog/faire-wholesale-take-rate-margin-impact) (third-party, not Faire's own help pages)
- Faire credit model: retailers get Net 60 terms once approved. Faire pays the brand within about 1-7 days of shipment and absorbs retailer default and fraud losses, so the commission includes a risk transfer. (Source is a trade-credit vendor's blog and may be biased.) — [Resolve Pay](https://resolvepay.com/blog/faire-net-60)
- Faire also lets retailers test a new brand with 60 days before payment, so the platform earns only if merchandise sells through. — [Retail TouchPoints](https://retailtouchpoints.com/topics/inventory-merchandising/400-million-funding-round-pushes-wholesale-marketplace-faires-value-to-12-4b)
- Udaan's cost lines (employee benefits -35%, logistics and packaging -17%, outsourced manpower -39% in FY24) show how much of a self-operated model is physical cost. — [Entrackr](https://entrackr.com/fintrackr/udaans-growth-stalls-mid-flight-losses-down-19-in-fy24-7452166)
- Meesho's FY25 revenue is mostly shipping and logistics fees paid by suppliers (aggregator figures, unverified). — [Zerodha Daily Brief](https://thedailybrief.zerodha.com/p/inside-meeshos-ipo)
- 1688: value-added services accounted for over 50% of revenue, so even a listing marketplace monetises services and not commission. — [Alibaba 6-K (SEC)](https://www.sec.gov/Archives/edgar/data/1577552/000110465921096324/a21-17183_36k.pdf)

### Inferences
- Take rate plus risk: 15% on a brand's wholesale price is a large margin for a brand (typical wholesale margin is only 50% of retail, so a brand is giving away roughly a third of its gross profit on a Faire-sourced order). Marketplaces justify it as customer acquisition, which is why the 0% Faire Direct tier exists.
- Credit is the part a factory-direct link struggles most to replace, because the factory has no local collections capability. Whoever underwrites small-shop credit (the platform, a fintech partner or a distributor) captures the margin. Udaan and Faire's Net 60 are both credit-heavy designs, but Faire shifts the cost to a priced commission on higher-ticket goods, whereas FMCG/grocery operates at far thinner margins.
- Pakistan's collapses came with exactly this combination: low-ticket FMCG, owned logistics, credit exposure and thin margins.

### Gaps
- Faire's actual credit-loss rate and Udaan's credit-book or NBFC loss rates.
- Primary-source distributor margin data by country; most figures are practitioner blogs.
- Time-to-cash cycles for factory-direct vs distributor-supplied small shops.

## 3. Disintermediation and leakage: how factory-shop pairs avoid the platform and what mitigations work

### Takeaway
Leakage is real and is the structural weakness of lead or listing marketplaces (Alibaba sellers offer discounts for off-platform wire transfers). The mitigations that appear to work are those that make staying on-platform worth more than the commission: payment protection, net terms, financing and software tools. Faire's 0% Faire Direct tier turns the leakage problem into an acquisition channel.

### Cited Findings
- Alibaba: sellers commonly offer about a 3% discount if the buyer wires directly to their bank account. This loses Trade Assurance protection (escrow, on-time shipment and quality coverage). Off-platform payments are described as the most common way importers lose money. Alibaba itself publishes a "stay on platform" guide. — [Shopappy](https://shopappy.com/ecommerce/alibaba/trade-assurance); [Alibaba Reads](https://reads.alibaba.com/stay-on-platform-stay-protected-a-practical-guide-to-secure-your-trading-on-alibaba-com/); [JingSourcing](https://jingsourcing.com/is-alibaba-safe-legit/) (importer blogs, not official data)
- Faire Direct: brands invite existing accounts through a personal link at 0% commission, so Faire collects only payment fees. Faire holds the credit and payment function that brands cannot easily replicate. — [Wholesale Helper](https://wholesalehelper.io/blog/selling-on-faire-vs-having-your-own-store/); [Craftybase](https://craftybase.com/blog/how-to-sell-on-faire-wholesale-guide)
- Faire is also described as net-60-plus-brand-paid-upfront, giving both sides a reason to transact on-platform. — [Resolve Pay](https://resolvepay.com/blog/faire-net-60)
- Tundra alleged Faire used exclusivity arrangements to stop brands and retailers multi-homing; the court dismissed the antitrust claims. — [Business of Home](https://businessofhome.com/articles/inside-the-lawsuit-between-b2b-digital-marketplaces-faire-and-tundra); [Paul Weiss](https://www.paulweiss.com/insights/client-news/faire-wholesale-wins-dismissal-with-prejudice-of-monopolization-claims)
- Faire's "Faire Direct repeat-brand order frequency +18%" and "retention 68%" claims came from an aggregator summary (unverified). — [Sacra chat](https://sacra.com/chat/h/adf545c3-1917-4574-9616-2afe6062efc1)
- Shopify acquired Handshake (2019). That puts wholesale ordering inside a merchant's own store tooling, where there is no matching fee. — [TechCrunch (2019)](https://techcrunch.com/2019/05/23/shopify-quietly-acquired-handshake-an-e-commerce-platform-for-b2b-wholesale-purchasing/amp/)

### Inferences
- Where goods are standardised and repeat (FMCG, spare parts), the buyer-seller pair needs the platform only for discovery, so the commission becomes untenable after the first order. Faire's response (0% on referred accounts, 15% on discovered ones) is a price-discrimination design that separates the two cases.
- Leakage is lowest when the platform provides something that cannot be copied off-platform: working capital, dispute protection, consolidated multi-brand shipping, and a single retailer ordering workflow. It is highest for single-brand lead generation.
- IndiaMART's subscription model (below) avoids transaction leakage by charging for leads and visibility, not for completed orders. That is the main structural alternative to commission.

### Gaps
- No quantified leakage or take-rate-erosion rates for any platform.
- No evidence found on RFQ-specific leakage on Alibaba.

## 4. Demand-signal and RFQ models: IndiaMART's lead model, Alibaba RFQ, sample programmes, retail audit data

### Takeaway
IndiaMART shows that a leads-and-visibility subscription sold to suppliers can be a very profitable, cash-collecting business without handling goods, payments or credit. Retail measurement is a large paid category, but small-shop demand data is still sold mainly to brands and distributors, and startups there are small.

### Cited Findings
- IndiaMART FY25 (year to March 2025): consolidated revenue about Rs 1,388 cr (+16%), standalone EBITDA about Rs 513 cr (39% margin), net profit Rs 181 cr, cash and investments about Rs 2,885 cr. Paying subscribers were about 2.17 lakh (+16.7%) with ARPU about Rs 65,590 (+11%). Platinum and gold subscribers were about 50% of customers and about 75% of revenue. Standalone collections were Rs 1,526 cr (+9%) and deferred revenue Rs 1,678 cr. Unique business enquiries were 27M (+10%) and storefronts 8.4M. — [Entrepreneur India](https://india.entrepreneur.com/news-and-trends/indiamart-closes-fy25-with-a-net-profit-of-inr-181-crore/490851); [My Domicile Substack](https://mydomicile.substack.com/p/indiamart-fy25-the-cash-machine-built); [IndiaMART Q2 FY25 release](https://corporate.indiamart.com/2024/10/19/indiamart-intermesh-limited-announces-strong-q2fy25-results-with-18-revenue-growth) (note: the Entrepreneur figure is net profit Rs 181 cr, but the figure differs by definition between sources, so treat as approximate)
- IndiaMART revenue comes mainly from supplier subscriptions that give visibility and buyer leads, plus pay-per-lead, RFQ access and advertising. — [Garnet Marketplace profile](https://garnetmarketplace.com/marketplaces/indiamart.html); [IndiaMART call transcript](https://financialfilings.com/filings/indiamart-intermesh-limited/call-transcript/2025/42419886/)
- Kirana data: kirana stores are cited as about 90% of FMCG retail sales in India. Startups and multinationals are racing to collect kirana data (DealStreetAsia). SnapBizz connected about 1,400 kiranas to distributors and brands; Retail Pulse sells AI-based store insights; 1K Kirana ran about 1,000 stores. — [DealStreetAsia](https://www.dealstreetasia.com/?p=204355); [Retail Pulse](https://portfolio.joinef.com/companies/retail-pulse); [Inc42](https://inc42.com/features/the-battle-for-indias-kirana-stores-has-begun/)
- NielsenIQ sells syndicated retail-measurement and panel data on multi-year subscriptions to CPG makers and retailers in 90+ countries. Pricing is not public. One aggregator estimated revenue at "$8.3B", which looks wrong for NIQ as I remember it (roughly mid-single-digit billions) and I do not use it. — [Koji comparison](https://www.koji.so/blog/nielseniq-vs-circana-vs-numerator-2026); [RFP.wiki](https://www.rfp.wiki/vendors/nielseniq)
- Faire's model includes a test-the-brand window (Net 60) that works as a sell-through sample programme for retailers, with brand data on the platform. — [Retail TouchPoints](https://retailtouchpoints.com/topics/inventory-merchandising/400-million-funding-round-pushes-wholesale-marketplace-faires-value-to-12-4b)

### Inferences
- IndiaMART's economics (about 39% EBITDA margin, advance billing, no inventory) are the sharpest contrast to Udaan (loss of about Rs 1,674 cr on about Rs 5,700 cr GMV). That contrast is the single strongest argument for a "lighter" model.
- IndiaMART's model works because buyers are intent-rich (searching to buy), and suppliers can measure lead value. A lead product for small shops needs the same property, which is hard when buyers are fragmented, low-ticket and often not online.
- What brands pay for demand data is observable only from NIQ's contract model; I found no verified price points.

### Gaps
- Alibaba RFQ specifics (volume, conversion, pricing); IndiaMART's lead conversion rates.
- What FMCG brands pay for kirana-level audit or sell-through data; no price list found.
- Evidence on product-testing or sample programmes as a business in their own right.

## 5. Evidence on whether direct-to-retailer ordering actually reduces cost, and in which categories

### Takeaway
Evidence is thin and mostly anecdotal. Direct models reduce price only when the platform can match the distributor's service bundle cheaply, which has mostly not happened in low-ticket, high-frequency categories (FMCG/grocery). Categories with higher margins, longer shelf life and lower delivery frequency (gift, home, beauty, stationery, specialty food, sold by independent brands) fit marketplaces better.

### Cited Findings
- Distributor services (stocking, small-lot dispatch, unsecured credit) valued at 11.5% of final price against a 5-6% distributor margin, which means direct models cannot undercut the distributor on cost unless they cut services or pass credit off. — [SCMR](https://www.scmr.com/article/e_b2b_distribution_strategies_for_fragmented_retail_environments_saving_ind)
- Retailer margins on app-based direct ordering reached up to about 20% against about 10-12% through distributors (practitioner source). — [Kirana Club margins](https://kirana.club/resources/fmcg-distributor-kirana-margins)
- Faire and Ankorstore categories (aggregator/press): home about a third of Ankorstore's brands, then grocery, fashion, beauty and children's products. — [FashionUnited (2022)](https://fashionunited.uk/news/business/ankorstore-raises-250-million-euros-in-series-c-funding-round/2022011060488)
- Udaan's GMV fell about 42% from FY22 to FY23 when it cut discounts and costs, then was flat, suggesting much of the early GMV was subsidised. — [Entrackr](https://entrackr.com/fintrackr/udaans-growth-stalls-mid-flight-losses-down-19-in-fy24-7452166) (inference; the cause is my reading, not stated)
- Pakistan's FMCG-led B2B plays (Jugnu, Retailo, Dastgyr, Bazaar) all retrenched within about 18 months of large raises, in an FX and inflation shock. — [Profit/Pakistan Today](https://profit.pakistantoday.com.pk/?p=161891); [ProPakistani](https://propakistani.pk/2023/07/16/jugnu-shuts-down-its-core-operations-a-year-after-raising-22-5-million/)
- Amazon Business grew to $35B+ largely in supplies and industrial categories (office, facility, MRO) serving institutions, not mom-and-pop FMCG. — [MDM](https://www.mdm.com/news/ecommerce/marketplaces/now-10-years-in-amazon-business-surpasses-8m-customers/)
- Alibaba 1688 has about 990,000 paying members, mostly factory and wholesaler suppliers selling to Chinese small traders. This is a listing and services business, so cost savings come from price transparency, not delivery. — [Alibaba 6-K (SEC)](https://www.sec.gov/Archives/edgar/data/1577552/000110465921096324/a21-17183_36k.pdf)

### Inferences
- Category fit (my judgement, mostly unverified): the evidence is weakest for hardware, spare parts, bakery supplies and mobile accessories because I found nothing on them. By inference from the above, mobile accessories, beauty and gift categories (high margin, light, tolerant of parcel shipping) look better for a direct model than bakery supplies or FMCG staples (perishable or heavy, high frequency, thin margin).
- Cost reduction accrues mainly from price transparency and a wider assortment, not from cutting the distributor's logistics.

### Gaps
- No controlled study or primary data comparing landed cost by channel for hardware, spare parts, bakery supplies or mobile accessories.
- MIT e-B2B kirana study findings were not retrievable beyond its title.
- No Walmart or Costco small-retailer wholesale data found.

## 6. What a lighter-weight model looks like versus a full marketplace

### Takeaway
The evidence favours asset-light layers: paid leads or RFQ (IndiaMART), payment and credit (Faire's core), and software and data, with logistics and collections done by partners. The big losses came from owning fulfilment and credit. A founder should test a narrow, single-category lead or RFQ and data product before taking any inventory or credit risk.

### Cited Findings
- IndiaMART shows a leads, RFQ and storefront subscription at about 39% standalone EBITDA margin with advance billing (Rs 1,678 cr deferred revenue). — [Entrepreneur India](https://india.entrepreneur.com/news-and-trends/indiamart-closes-fy25-with-a-net-profit-of-inr-181-crore/490851); [My Domicile](https://mydomicile.substack.com/p/indiamart-fy25-the-cash-machine-built)
- Jugnu moved away from self-managed fulfilment to a tech-platform model after shutting core ops; Bazaar said its B2B retail arm continued after cutting new verticals; Udaan bought ShopKirana and shifted to an FMCG focus for profitability. — [ProPakistani](https://propakistani.pk/2023/07/16/jugnu-shuts-down-its-core-operations-a-year-after-raising-22-5-million/); [Profit/Pakistan Today](https://profit.pakistantoday.com.pk/?p=161891); [Inc42](https://inc42.com/?p=523483)
- Ankorstore's model handles logistics for part of its GMV while brands ship the rest (snippet, unverified). — [Garnet Marketplace](https://garnetmarketplace.com/marketplaces/ankorstore.html)
- Faire Direct and Shopify-Handshake show that brand-owned relationships plus payment and ordering software can be monetised at 0-3.5% instead of 15-19%. — [Wholesale Helper](https://wholesalehelper.io/blog/selling-on-faire-vs-having-your-own-store/); [TechCrunch (2019)](https://techcrunch.com/2019/05/23/shopify-quietly-acquired-handshake-an-e-commerce-platform-for-b2b-wholesale-purchasing/amp/)
- Kirana data businesses (SnapBizz, Retail Pulse) exist but are small, mostly selling to distributors and brands. — [DealStreetAsia](https://www.dealstreetasia.com/?p=204355)

### Inferences
- A lighter ladder, in order of capital need, derived from the cases above:
  1. Demand intelligence and RFQ: collect small-shop orders and requests in one category, sell leads or reports to factories on subscription (IndiaMART logic, Retail Pulse/SnapBizz logic). Risk: low leakage concern, but lead quality must be proven.
  2. Add partner payments and escrow-style protection, to reduce leakage (Trade Assurance logic).
  3. Add partner-underwritten credit (a fintech or distributor-financed Net terms) once repeat order data exists, without holding the book.
  4. Only then add partner logistics, then consider owning anything.
- "Reverse Alibaba" has two readings. A listing/leads marketplace is Alibaba/IndiaMART, which is profitable but crowded. A managed supply-chain marketplace is Udaan/LST/Pakistan, which burned capital. The note's cases support the first as lower-risk and the second as risky without a very high-margin category.
- Faire's narrow positioning (independent brands to independent shops) is a "specialised Amazon for targeted shops" that worked, but it took about $1.7B (unverified) and has been re-rated. Founders should assume incumbent defence in any category where a winner already exists.

### Gaps
- Unit economics (CAC, order frequency, contribution margin per order) for any lighter-weight model are not publicly available.
- No verified case of a pure RFQ or demand-data business serving small shops at scale in Pakistan or emerging markets.
- I found no evidence on how factories in categories like hardware, spare parts, or mobile accessories actually behave when offered direct small-shop ordering.
