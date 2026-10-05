# Data sources AI agents could use to find business information, and what is permitted for each

Research date: 5 October 2026. Planning research, not legal advice; counsel is essential before any bulk ingestion or resale, especially for Google, Meta, China and personal-data (GDPR / Pakistan / India / Gulf) questions.

Method caveat: the research environment blocked direct fetching of most primary pages (developers.google.com, docs.overturemaps.org, gov.uk, lbs.qq.com, osmfoundation.org, fbm.com, dubaichamber.com were all "egress blocked"). The two Google terms pages that did load were truncated. Most findings below therefore come from search-result excerpts of primary pages or from law-firm and third-party summaries. Each is flagged as "primary excerpt via search" or "secondary". Quotes marked "via search excerpt" were not read in full context and must be re-checked against the live page before anyone relies on them. Items I could not source are in Gaps, not in findings.

## 0. Overall classification (green / amber / red) for the founder

### Takeaway
Green: open datasets whose licences allow commercial reuse with attribution (Foursquare OS Places, Overture Places records with CC0 / Apache-2.0 / CDLA-Permissive-2.0 sources, Wikidata, GeoNames) and owner-submitted data collected with explicit consent. Amber: OSM / ODbL-derived data, government registers (licence and personal-data limits vary by country), chamber and association directories (only with a written agreement), and a business's own website contact page (only via a per-record, documented decision). Red: bulk collection or resale from Google Maps / Places content, Facebook (outside official APIs), Baidu / Amap / Tencent maps, and marketplaces whose terms forbid compiling directories (Alibaba, and likely Justdial, IndiaMART, Daraz and OLX, which I could not verify).

### Cited Findings
Classification table (my synthesis; evidence in sections 1-9):

| Source | Class | One-line reason |
|---|---|---|
| Google Maps Platform / Places API data stored in own resale database | RED | Terms bar scraping, bulk download, storing content outside the Services; lat/lng cache limited to 30 days (sec. 1) |
| Scraping Google Maps (SerpApi-style) | RED | Contract breach plus live DMCA 1201 litigation by Google (sec. 1) |
| Facebook Pages scraped | RED | Meta terms forbid automated collection without permission; court win for Bright Data covers only logged-off, public data and contract claims (sec. 2) |
| Meta official APIs (Page Public Content Access, Business Discovery) | AMBER | Permitted only inside app review and platform terms; not designed for directory building (sec. 2) |
| Baidu / Amap / Tencent | RED for a foreign resale product | Chinese mapping law and licensing; terms not verified (sec. 3) |
| Chamber / association directories | AMBER | Typical terms ban scraping and mailing-list use; reuse needs written permission or member opt-in (sec. 4) |
| Government registers | AMBER (varies from GREEN to RED by country) | UK and India open licences vs thin or restricted registers elsewhere (sec. 5) |
| Foursquare OS Places | GREEN | Apache 2.0 (sec. 6) |
| Overture Places | GREEN to AMBER by record | Multi-licence per record since Sept 2025 (sec. 6) |
| OpenStreetMap / ODbL | AMBER | Share-alike for derivative databases (sec. 6) |
| Wikidata, GeoNames | GREEN | CC0 and CC BY 4.0 (sec. 6) |
| Business's own website | AMBER | Public, but terms, robots.txt and privacy law apply per record (sec. 7) |
| Marketplaces | RED | Compilation bans (sec. 7) |
| Owner submissions and claims | GREEN | Consent is the cleanest legal basis (sec. 8) |

### Inferences
- The only sources that are both scalable and clean today are open datasets (Foursquare, Overture non-ODbL records, Wikidata, GeoNames) plus consented owner submissions.
- Google, Meta and Chinese map data should be treated as "look up and link, never copy into the resale database."

### Gaps
- No court has, to my knowledge in these results, ruled on scraping Google Maps specifically (see sec. 1).

## 1. Google Maps Platform / Places API: caching, storage, bulk export, lead lists, scraping law, licensing routes

### Takeaway
Google's terms allow only temporary caching of Places lat/lng (30 consecutive days) and indefinite storage of Place IDs. They prohibit exporting, scraping, bulk downloading or copying and saving business names, so a resale database built from Places or Maps content is outside the standard licence. I found no public commercial licence that permits building a resale database; Places Insights offers only aggregated counts.

### Cited Findings
- Service-specific terms (versions back to 2020 are consistent): customer may "temporarily cache latitude (lat) and longitude (lng) values from the Places API for up to 30 consecutive calendar days," then must delete them; Place ID (place_id) values may be cached in line with the Places API policies — [Google Maps Platform Service Specific Terms, 22 May 2024 version](https://cloud.google.com/maps-platform/terms/maps-service-terms/index-20240522); [1 May 2025 archive](https://cloud.google.com/archive/maps-platform/terms/maps-service-terms-20250501) (via search excerpt; pages truncated when fetched, so the live current version was not read).
- Place IDs are exempt from the caching restriction, but Google recommends refreshing IDs older than 12 months, and a refresh via Place Details request is free — [Google Place ID docs](https://developers.google.com/maps/documentation/places/web-service/place-id) (via search excerpt).
- Section 3.2.3 "Restrictions Against Misusing the Services", quoted via search excerpt: "Customer will not export, extract, or otherwise scrape Google Maps Content for use outside the Services," with examples "(i) pre-fetch, index, store, reshare, or rehost Google Maps Content outside of the Services; (ii) bulk download Google Maps Content; or (iii) copy and save business names, addresses, or user reviews" — [Google Maps Platform Terms of Service](https://cloud.google.com/maps-platform/terms); [EEA terms, 4 June 2025](https://cloud.google.com/archive/terms/maps-platform/eea-20250604) (secondary excerpt; full clause not verified in context).
- Third-party summaries say the terms also bar using Maps content to create or augment a business listings database, mailing list or telemarketing list; I could not verify that exact wording against Google's text — [Thunderbit summary](https://thunderbit.com/blog/is-scraping-google-maps-legal) (secondary, a scraping vendor with a commercial interest).
- Pricing since 1 March 2025: Essentials / Pro / Enterprise categories, with the old USD 200 monthly credit replaced by a free monthly usage threshold per Core Services SKU — [Google pricing overview](https://developers.google.com/maps/billing/overview/) and [March 2025 changes](https://developers.google.com/maps/billing-and-pricing/march-2025). Per-SKU prices were not captured.
- Places Insights (BigQuery) provides aggregated counts and density of POIs by attributes (type, ratings, hours, accessibility), not record-level exports — [Places Insights overview](https://developers.google.com/maps/documentation/placesinsights/overview).
- Google LLC v. SerpApi LLC, N.D. Cal., case 5:25-cv-10826, filed 19 December 2025: DMCA anti-circumvention claims over SerpApi's alleged circumvention of "SearchGuard" to scrape and resell Search results; Google alleges SerpApi requests grew "as much as 25,000%" in two years — [IPWatchdog, 26 Dec 2025](https://ipwatchdog.com/2025/12/26/google-sues-serpapi-parasitic-scraping-circumvention-protection-measures/); [Search Engine Journal](https://www.searchenginejournal.com/google-files-dmca-suit-targeting-serpapis-serp-scraping/563847/). A search summary reported that Judge Yvonne Gonzalez Rogers dismissed the claims with leave to amend (21 days, to show authorisation from copyright owners). I could not retrieve the order or date; treat as unverified and check the docket.
- The SerpApi case concerns Google Search results, not Maps/Places specifically. I found no reported court decision on scraping Google Maps itself. Commentary says breach of terms is not a US crime but creates civil contract risk, plus account and IP bans — [Cufinder](https://cufinder.io/blog/local-business-database/is-scraping-google-maps-legal/) (secondary vendor blog).
- Google Business Profile APIs have separate terms: Business Profile Additional Terms, Business Profile API Policies and Google APIs ToS, in that order of precedence — [Business Profile API terms](https://developers.google.com/my-business/content/terms).

### Inferences
- An agent may call Places to find or verify a business and keep the Place ID (plus own-collected data) but should not persist Google names, addresses, phones, ratings or reviews, and should delete coordinates after 30 days.
- Because Google has chosen to sue scrapers under the DMCA rather than only contract, any agent that evades bot protection on Maps carries extra risk beyond ToS breach.
- A resale or lead-list product cannot be built on Places content under the published terms. An enterprise negotiated licence is the only conceivable route; none was found publicly.

### Gaps
- Full current text of section 3.2.3 and any lead-list or "database" clause; Places API Policies page (blocked).
- Whether Google offers any bespoke commercial data licence for resale (no public evidence found).
- Status and outcome of Google v. SerpApi after the reported dismissal.
- Per-SKU Places prices in 2026.

## 2. Facebook / Meta: scraping terms, official APIs, Meta v. Bright Data, WhatsApp directory

### Takeaway
Meta's terms forbid automated data collection without permission, and its official APIs for reading other Pages and businesses are gated by app review and business verification. A federal court held that logged-off scraping of public data did not breach Meta's contract, but that ruling is narrow, so Facebook is red for an agent-driven bulk pipeline.

### Cited Findings
- Meta terms (via third-party compilation): "You may not access or collect data from our Products using automated means (without our prior permission) or attempt to access data you do not have permission to access"; permitted automated collection must follow Meta's Automated Data Collection Terms, and permission can be revoked — [ConductAtlas record of Meta Terms of Service](https://conductatlas.com/platform/meta/meta-terms-of-service/automated-data-collection-restrictions/) (secondary; confirm at facebook.com/terms). Meta Platform Terms are at [developers.facebook.com/terms](https://developers.facebook.com/terms).
- Meta Platforms v. Bright Data (N.D. Cal., Judge Edward Chen): summary judgment for Bright Data on breach of contract; the court said Meta's terms govern "your use" of Meta's products and that Bright Data "did not 'use' Facebook and Instagram when it engaged in public logged-off scraping"; only a tortious interference claim remained — [MediaPost](https://www.mediapost.com/publications/article/392920/judge-sides-against-meta-in-battle-over-scraping-p.html); [Lowenstein client alert, 15 Feb 2024](https://www.lowenstein.com/news-insights/publications/client-alerts/meta-v-bright-data-ruling-has-important-implications-for-webscraping-activities-by-investment-advisers-im). Meta later abandoned the suit — [MediaPost](https://www.mediapost.com/publications/article/393996/None) (headline only; details not read), so no appellate precedent exists.
- Instagram Business Discovery lets an app read profile info and media of other business or creator profiles. It requires a Facebook account administering a Page linked to an Instagram Business account, and cannot reach non-business accounts — [Meta Instagram API getting started](https://developers.facebook.com/docs/instagram-api/getting-started/) and [Meta developer blog 2018](https://developers.facebook.com/blog/post/2018/01/30/instagram-graph-api-updates/) (via search excerpt).
- Reading Pages you do not manage requires the "Page Public Content Access" feature, with app review and business verification — [bundle.social Graph API guide, Aug 2026](https://bundle.social/blog/facebook-graph-api) (secondary; Meta's own page for this feature was not retrieved).
- WhatsApp: at Conversations (London, 3 June 2026) Meta announced Business Discovery, letting users find businesses by name, phone number or shared contact card inside WhatsApp, rolling out market by market — [AIChat summary](https://www.aichat.com/blog/meta-conversations-2026-announcements); [Kanal](https://getkanal.com/blog/whatsapp-business-search-get-found). An in-app business directory (browse by category) was reported for Brazil, the UK, Indonesia, Mexico and Colombia — [AOL/Reuters-style report](https://www.aol.com/news/whatsapp-broadens-app-business-directory-170207670.html) (secondary, undated in excerpt). No evidence found of a public API for reading the directory.

### Inferences
- The Bright Data decision does not help an agent that logs in, uses accounts, or sells data in ways raising other claims (privacy, tortious interference). It also does not address GDPR or other privacy law.
- WhatsApp Business Discovery is a distribution channel for listed businesses (a place to be found), not a data source for Alllists.

### Gaps
- Meta's own current text of the Automated Data Collection Terms and of Page Public Content Access limits (rate limits, permitted purposes).
- Why and when Meta dropped the Bright Data case, and whether other Meta scraping suits changed the picture in 2025-26.

## 3. Baidu Maps and Chinese map services (Amap/Gaode, Tencent Maps)

### Takeaway
I could not retrieve Baidu or Amap developer terms. Chinese law requires licences for publishing digital maps, GCJ-02 coordinate offsetting, in-country storage of map data and approval for exporting it, so Chinese map data is red for a foreign-run resale database unless a local licensed partner is involved.

### Cited Findings
- China mandates the GCJ-02 coordinate system for publicly available digital maps; the Surveying and Mapping Law dates from 2002, revised 2013 and 2017; map publishers need a licence from the surveying and mapping administration; Baidu, Gaode and Tencent all use GCJ-02 or variants — [Wikipedia, Restrictions on geographic data in China](https://en.wikipedia.org/wiki/Restrictions_on_geographic_data_in_China) (secondary).
- Foreign firms wanting to provide mapping and surveying services must use joint ventures or local partners; map data must be stored in China and exporting map data needs government approval — [Zhonglun Law, Regulation on Digital Maps in China](https://en.zhonglun.com/research/articles/52416.html) (law-firm commentary via search excerpt, date not captured).
- Tencent publishes a separate overseas map-service SDK agreement — [Tencent Map overseas terms](https://lbs.qq.com/OverseasMapServiceAgreement/OverseasMapService/OverseasMapServiceAgreement) (URL appeared in search results; content could not be fetched).

### Inferences
- If Alllists ever covers China, the lawful route is local business-registry data or a licensed Chinese partner, not scraping or storing Baidu/Amap/Tencent POIs.

### Gaps
- Baidu Maps Open Platform service terms on storage, caching, bulk use and overseas use (searches returned nothing).
- Amap (Gaode) terms; any 2023 amendments to the Surveying and Mapping Law (my search returned only the 2002/2013/2017 history).
- Whether foreign users can obtain Baidu API keys at all.

## 4. Chambers of commerce and trade associations

### Takeaway
Chamber directories are published "for information", and typical terms prohibit scraping, bulk use and mailing-list creation without written permission. Some chambers do release member lists to third parties, so partnership (written data-sharing agreement plus member opt-in) is the route; scraping is not.

### Cited Findings
- Example chamber and association directory terms: transmitting or sharing data outside the platform prohibited; directory contents may not be used for bulk communications, direct mail, e-blasts or mailing lists for commercial purposes; unauthorised "use, reproduction, scraping, harvesting, or redistribution ... for commercial purposes" prohibited without prior written permission — [Edinburgh Chamber directory usage policy](https://www.edinburghchamber.co.uk/?p=18690); [Ossining Chamber terms](https://www.ossiningchamber.org/terms/); [Council on Foundations Member Directory Policy](https://cof.org/content/member-directory-policy-appropriate-use) (search excerpts; exact clause-to-site mapping not verified).
- Some chambers do share: Glasgow Chamber's membership terms say members' details may be made available to third parties as part of a mailing list, with an opt-out — [Glasgow Chamber terms](https://glasgowchamberofcommerce.com/about-us/terms-and-conditions-of-membership/).
- Lahore Chamber (LCCI) launched a classified directory of trade and industry with counts such as 4,017 manufacturers and 4,119 exporters (date not captured; likely old) — [Business Recorder](https://www.brecorder.com/news/519895) (listed in search results; claim from search excerpt).
- Dubai Chambers' directory covers companies affiliated by membership — [Wikipedia, Dubai Chambers](https://en.wikipedia.org/wiki/Dubai_Chambers); the chamber has an open-data page — [dubaichamber.com/en/open-data](https://dubaichamber.com/en/open-data) (exists per search; content and licence not read).

### Inferences
- A partnership model (chamber supplies or co-collects listings, members opt in, chamber gets a member benefit such as free enhanced listings or a co-branded directory) fits the terms better than any scraping approach; written agreement needed because members, not just chambers, own their contact data.
- The Glasgow example shows chambers regard member lists as a revenue or service asset, which supports offering them something of value.

### Gaps
- FPCCI and KCCI directory terms; whether any Pakistani chamber sells or licenses data.
- Dubai Chambers open-data licence terms; Gulf chambers' policies.
- Whether members consented to reuse (no evidence found for any chamber).

## 5. Government registries and open data portals

### Takeaway
Registers range from open (UK Companies House snapshot, India MCA data on the OGD portal under GODL) to thin, free-to-search-only (Pakistan SECP, Nigeria CAC). Open-licensed registers are usable with attribution, but director and address fields can be personal data.

### Cited Findings
- UK Companies House: since June 2012 a subset of register fields has been available as a free monthly "snapshot" bulk download on an open basis, plus free accounts data (XBRL); the company snapshot covers live companies with type, registered office address, SIC nature of business, status, filing dates — [Companies House data products](https://www.gov.uk/guidance/companies-house-data-products) (via search excerpt; page not fetchable); [Open Knowledge Index](https://2014.index.okfn.org/place/united-kingdom/companies). Commentary notes some data for the smallest companies is effectively personal data, with junk-mail concerns — [OKFN Index](https://2015.index.okfn.org/place/united-kingdom/companies/2013/).
- India: Government Open Data Licence (GODL-India) notified 13 February 2017, allowing commercial and non-commercial use of OGD datasets with attribution — [Atlas data portals summary](https://atlas.co/data-portals/data-gov-in/). MCA company master data (CIN, name, registration date, status, class, capital) is listed on the OGD platform, about 3.67 million companies — [AIKosh dataset page](https://aikosh.indiaai.gov.in/home/datasets/details/company_master_data.html) (secondary; check licence on the dataset's own page).
- Pakistan SECP: free company search by name, registration number or CUIN returns name, incorporation date, kind, registered office address, jurisdiction, status — [Lemreveal](https://lemreveal.com/how-to/is-registry-free/pakistan) (secondary vendor); a 2015 Open Knowledge assessment found only names and website links openly available — [OKFN 2015](https://2015.index.okfn.org/place/pakistan/companies/) (old). No open bulk licence found.
- Nigeria CAC: free public search limited to name and registration number confirmation; no directors, shareholders, beneficial owners, addresses or filings in the public register — [YouVerify guide](https://youverify.co/blog/business-registry-verification-africa-kyb-cac-cipc-company-registries); third-party scrapers of CAC exist on Apify (not a licence).
- Kenya: Business Registration Service is custodian of company records under the Companies Act 2015 — same YouVerify source; bulk/licence terms not found.

### Inferences
- Registers establish that a business exists (legal name, ID, status) and are a good verification layer, but rarely give contacts, categories or maps. Use them to confirm, not to populate listings.
- Where a register includes sole-trader or director details, treat as personal data requiring a legal basis (see sec. 9).

### Gaps
- Companies House exact licence wording and API terms (OGL v3 is my expectation but I did not verify it).
- UAE, Saudi and Kenyan portals' licences; Pakistan SECP bulk access terms; Pakistan's data protection law status in 2026.

## 6. Open map datasets: OSM, Overture, Foursquare OS Places, Wikidata, GeoNames

### Takeaway
Foursquare OS Places (Apache 2.0), Wikidata (CC0) and GeoNames (CC BY 4.0) are usable for a commercial product with attribution duties. Overture Places is now licensed per record, and OSM-derived data brings ODbL share-alike obligations that must be tracked per record.

### Cited Findings
- Foursquare OS Places: 100M+ places, 22 core attributes, updated monthly, Apache 2.0, commercial use allowed, Parquet on S3 (about 10.6 GB) — [Foursquare blog](https://foursquare.com/resources/blog/products/foursquare-open-source-places-a-new-foundational-dataset-for-the-geospatial-community/); [Simon Willison, 20 Nov 2024](https://simonwillison.net/2024/Nov/20/foursquare-open-source-places).
- Overture Places: since September 2025 a multi-licence dataset, with each place's licence set by its source property. As of April 2026 sources include AllThePlaces (CC0-1.0), Foursquare (Apache-2.0), DAC, Krick, Microsoft, PinMeTo, RenderSEO and Meta (CDLA-Permissive-2.0); Meta supplies over 59 million features, Microsoft over 7 million — [Overture release notes](https://docs.overturemaps.org/blog/2026/04/15/release-notes/) and [Sept 2025 notes](https://docs.overturemaps.org/blog/2025/09/24/release-notes/) (via search excerpt). The `categories` property is deprecated, to be removed in the September 2026 release, replaced by `basic_category` and `taxonomy`.
- Overture says it prefers CDLA-Permissive 2.0 but several themes derived from OSM carry ODbL, forming a "Derivative Database" — [Overture FAQ](https://overturemaps.org/about/faq/); [Linux Foundation release](https://linuxfoundation.org/press/overture-maps-foundation-releases-first-open-map-dataset). Attribution page lists sources and licences by theme (not fetched).
- ODbL definitions: "Derivative Database" includes extracting or re-utilising a substantial part of the contents in a new database; "Collective Database" (unmodified database in a collection of independent databases) is not derivative; a "Produced Work" results from using contents. Share-alike applies when you publicly use a derivative database, and recipients of a Produced Work may request the derivative database — [OSM wiki, ODbL 1.0 text](https://wiki.openstreetmap.org/wiki/OSMFJ/ODbL/1.0/text); [OSMF Licence and Legal FAQ](https://osmfoundation.org/wiki/Licence_and_Legal_FAQ) (search excerpts).
- Wikidata is CC0; GeoNames is CC BY 4.0 with attribution method left to the user — [Creative Commons wiki, GeoNames](https://wiki.creativecommons.org/wiki/GeoNames).

### Inferences
- Pitfall: merging OSM-derived records with Apache / CDLA / CC0 records into one table can make the merged table an ODbL derivative database. Keep source and licence per record, and keep the ODbL layer separable (a "collective" arrangement) unless the founder accepts share-alike.
- Overture's per-record licence means a Places extract is not uniformly CDLA; the agent must filter by the `sources` licence field.
- These datasets are weakest exactly in the data-poor launch markets (sparse and uneven coverage in Pakistan, Africa), so they are a seed and a dedupe layer, not a complete directory.

### Gaps
- Overture attribution page text and exact ODbL attribution wording (blocked).
- OSM geocoding-community guidance on whether storing geocoder results triggers share-alike (not verified).
- Per-country POI coverage figures for Pakistan, Gulf and Kenya.
- Whether CDLA-Permissive 2.0 carries any attribution duty beyond notice (not read).

## 7. Business websites, social pages and marketplaces (robots.txt, ToS, per-record permission)

### Takeaway
A business's own public contact page is the most legitimate web source, but legality depends on the site's terms, robots.txt, database-right and privacy law, so it is amber and should be handled per record. Marketplaces generally forbid compilation, so red.

### Cited Findings
- US: Ninth Circuit (hiQ v. LinkedIn, 2022, after Van Buren) found it likely that accessing publicly available data from a system that permits public access is not "without authorization" under the CFAA — [White & Case](https://www.whitecase.com/insight-our-thinking/web-scraping-website-terms-and-cfaa-hiqs-preliminary-injunction-affirmed-again); [Proskauer](https://www.proskauer.com/insights/get-pdf/24942). This addresses only the CFAA, not contract, copyright or privacy.
- EU: in Ryanair v. PR Aviation, CJEU held that where the Database Directive does not apply, site operators may restrict scraping through contract terms — [Pinsent Masons](https://www.pinsentmasons.com/out-law/news/website-operators-can-prohibit-screen-scraping-of-unprotected-data-via-terms-and-conditions-says-eu-court-in-ryanair-case); [Osborne Clarke](https://marketinglaw.osborneclarke.com/media-and-ip/could-ryanair-control-use-of-its-flight-data-by-pr-aviation-without-database-right/).
- Alibaba.com terms reportedly prohibit systematic retrieval of content to build a database or directory without written permission, by robots or manual means — search summary only, underlying page not identified; confirm at alibaba.com terms.
- India: no statute explicitly permits or prohibits scraping; exposure sits under the IT Act and Copyright Act, depending on method — [Lawrato](https://lawrato.com/indian-kanoon/civil-law/is-web-scraping-legal-in-india-what-a-business-can-and-cannot-collect-3192); [Advocate Gandhi](https://advocategandhi.com/data-scraping-in-india-legal-perspectives-risks-and-regulatory-framework-explained/). IndiaMART and JD Mart were reported to be in a copyright dispute over listings — [Inc42](https://inc42.com/?p=232997) (date not captured). A July 2026 Indian law-firm article on collecting public business data from Google Maps, Justdial and IndiaMART exists but could not be read — [Sudhir Rao](https://sudhirrao.com/insights/legal-collect-public-business-data-google-maps-justdial-indi).
- Many Justdial, IndiaMART and Daraz scrapers are sold on Apify and ScrapingBee, which shows they are technically scrapable, not that it is permitted — [Apify Justdial](https://apify.com/themineworks/justdial-business); [ScrapingBee Daraz](https://www.scrapingbee.com/scrapers-v2/daraz-api).

### Inferences
- "Business-published, per-record permission" pattern: fetch only the contact or about page of the business's own site, honour robots.txt and noindex, record the decision, keep only fields the business itself publishes as a business contact (not named individuals' personal data), and give an easy removal route.
- Because Ryanair-type contract claims survive outside the US, a US CFAA result is not a safe harbour for Pakistan, the Gulf, Kenya or the EU.

### Gaps
- Actual ToS text for Daraz, OLX, Justdial, IndiaMART, Amazon (not retrieved).
- Pakistan and Gulf law on scraping and database protection.
- Whether robots.txt carries legal force in any launch market (no source found).

## 8. Owner submissions and claims

### Takeaway
Owner-submitted, verified and consented data is the cleanest source: the data subject supplies it and grants the licence. Established platforms use verification codes and claim flows that Alllists can copy.

### Cited Findings
- Google Business Profile verification methods include video, live video call, phone or text code, email and postcard code (code mailed to the address) — [Google support, Verify your business](https://support.google.com/business/answer/7107242).
- Yelp: click "Unclaimed" on the page, enter business email and phone, and confirm by email or phone — [Network Solutions help](https://www.networksolutions.com/help/article/how-do-i-claim-my-yelp-page) (secondary).
- Foursquare: search for the venue in the business portal, confirm it is the right listing and click Claim — [Foursquare support](https://support.foursquare.com/hc/en-us/articles/23646714300444-Claiming-a-listing).
- Research reports claiming a profile on review platforms can have unintended effects on reviews — [FIU Business, 2026](https://business.fiu.edu/news/2026/claiming-your-business-page-on-review-platforms-can-have-unintended-effects-on-customer-reviews-study-shows.html) (relevant to product design, not licensing).

### Inferences
- WhatsApp or SMS claim flow: send a one-time code to the phone number in the record (proves control of that number), capture explicit consent language (publish this data in the directory, to users and AI agents, and share via API; can withdraw at any time), store the consent text and timestamp. WhatsApp is the dominant channel in the likely launch markets; Meta's business messaging policies and template-message rules need checking before using it for outbound claim invitations (cold outreach rules not researched here).
- A claim flow can also convert scraped-from-open-source records into permissioned records, raising their class from amber to green.

### Gaps
- Meta WhatsApp Business messaging policy on unsolicited claim invitations; local SMS and anti-spam rules (Pakistan PTA, UAE TDRA, Kenya, India TRAI/DND).
- Recommended consent wording needs counsel review.

## 9. Personal-data overlay and what a compliant source registry should record

### Takeaway
"Public" does not mean lawfully reusable, because privacy regulators have fined scrapers of public data. A per-record source registry is the control that lets the founder show provenance, licence and consent.

### Cited Findings
- Regulators found Clearview AI's "legitimate interest" argument for scraping public images insufficient: Dutch DPA fined EUR 30.5 million, French CNIL EUR 20 million (maximum), UK ICO issued a GBP 17 million notice of intent — [Privacy Bootcamp](https://www.privacybootcamp.com/Resources/Article/clearview-ai-fine-when-publicly-available-becomes-unlawfully-processed); [Techdirt](https://www.techdirt.com/2022/10/24/french-government-hits-clearview-with-the-maximum-fine-for-gdpr-violations/); [IAPP](https://iapp.org/news/b/ico-hits-clearview-ai-with-17m-gbp-fine-notice). Clearview involved biometric photos, a far more sensitive category than business contact data, so it shows the principle, not a direct analogue.

### Inferences
- Minimum fields per record (my recommendation, not a sourced standard): source name and URL; source type and licence (SPDX-style: Apache-2.0, CC0-1.0, CDLA-Permissive-2.0, ODbL-1.0, owner-consent, chamber-agreement-ID); licence version and attribution string; collection date and agent run ID; robots.txt result and ToS check date (allow / deny / not applicable); consent record (text version, timestamp, channel, verification code outcome); per-field provenance for merged records; personal-data flag (sole trader or named individual); retention or delete-by date (for example 30 days for any Google lat/lng, if ever used); share-alike flag for ODbL-derived fields; takedown and removal log.
- Enforce at the agent boundary: allow-list of sources by class; agents refuse red sources by default.

### Gaps
- Pakistan, UAE, Saudi, Kenya, Nigeria and India personal-data law status and applicability to business directories (not researched here; India DPDP Act and Gulf laws need counsel).

