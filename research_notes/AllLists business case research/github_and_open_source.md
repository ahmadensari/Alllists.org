# GitHub and Open-Source Components for AllLists.org (hierarchical, contributor-built business-list marketplace)

Method and verification notes (read first):
- All dates are relative to 2026-10-04 (research date). Stars, forks, description, archived flag and `updated_at` were read directly from the GitHub search API (via the GitHub MCP tool) on 2026-10-04. Note `updated_at` is NOT last-commit date. Where I give a last-commit ("pushed_at") date, it is from the API's `pushed_at` field. For repos in the second and third batches, I verified only "pushed after 2026-04-04" (batch 2) or nothing beyond `updated_at` (batch 3); those are labelled.
- Licences were verified in one of two ways: (a) GitHub's detected licence returned in the repo object or via a `license:` filter query, or (b) by reading the LICENSE file directly. Anything labelled "licence not verified" is not confirmed; I did not guess. GitHub licence detection missed several repos (e.g. Medusa, Chatwoot, Mautic), so absence from a filter result is not evidence of a licence.
- Several non-GitHub sites (docs.overturemaps.org, gadm.org, opendatacommons.org, download.geonames.org, huggingface.co) were blocked by the network proxy, so data-licence facts rest on web-search snippets and are flagged as secondary-source. Re-check primary licence pages before relying on them legally.
- Direct GitHub API access via `gh` was denied for repos outside the session allow-list; the MCP search tool worked.

## 1. Business directory and marketplace platforms: base or reference?

### Takeaway
None of the directory or marketplace platforms is a good base for a Python/PostgreSQL + Next.js/Astro stack. The WordPress directory plugins (HivePress, GeoDirectory) are tiny on GitHub, GPL-licensed PHP and cannot model a street-to-world hierarchy with per-entry revenue shares. Saleor (BSD-3, Python) and Medusa (MIT with an Enterprise carve-out) are the only credible architecture references, for order/payment/payout patterns rather than for directories.

### Cited Findings
- Saleor: Python headless commerce API, about 23.4k stars, 6.1k forks, not archived, `updated_at` 2026-10-04; BSD-3-Clause per GitHub licence filter; pushed after 2026-04-04 — [saleor/saleor](https://github.com/saleor/saleor)
- Medusa: TypeScript commerce framework, about 36.6k stars, `updated_at` 2026-10-04, pushed after 2026-04-04 — [medusajs/medusa](https://github.com/medusajs/medusa)
- Medusa licence: MIT, but "Except for the Enterprise Edition materials identified in ENTERPRISE-LICENSE.md" (read directly from the LICENSE file) — [Medusa LICENSE](https://raw.githubusercontent.com/medusajs/medusa/develop/LICENSE)
- Sharetribe Go: repo describes itself as "old source-available marketplace software... no longer actively maintained"; Ruby, about 2.4k stars. "Source-available" signals a non-OSI licence (exact licence not verified) — [sharetribe/sharetribe](https://github.com/sharetribe/sharetribe)
- Sharetribe Web Template: JavaScript client starter, about 67 stars, pushed after 2026-04-04; licence not verified — [sharetribe/web-template](https://github.com/sharetribe/web-template)
- HivePress: WordPress/PHP directory plugin, only about 69 stars, 47 open issues; GPL-3.0 per GitHub licence filter; pushed after 2026-04-04 — [hivepress/hivepress](https://github.com/hivepress/hivepress)
- GeoDirectory: WordPress directory plugin, about 46 stars on GitHub, `updated_at` 2026-04-27 (older than the others); licence not verified (it appeared under neither the BSD-3 nor GPL-2.0 filters) — [GeoDirectory/geodirectory](https://github.com/GeoDirectory/geodirectory)
- Directorist: searched under `Directorist/Directorist` and `sovware/directorist`; neither repo was returned by the GitHub search, so no stats or licence were obtained.
- Wagtail (Django CMS): about 20.5k stars, BSD-3-Clause per filter, `updated_at` 2026-10-04 — [wagtail/wagtail](https://github.com/wagtail/wagtail)
- Django: about 91.3k stars, BSD-3-Clause per filter, `updated_at` 2026-10-04 — [django/django](https://github.com/django/django)

### Inferences
- WordPress plugins would force PHP/WordPress/MySQL and GPL derivative-work obligations on any theme/plugin code you ship; this conflicts with the stated Python/PostgreSQL + Next.js/Astro direction. Treat as UI/feature inspiration only (listing cards, claim-listing flows).
- Sharetribe's hosted-backend model (from general knowledge, not verified this session) and "source-available" licence make it unsuitable as a base for a product whose core asset is its own hierarchical dataset.
- Saleor/Medusa are product-checkout engines; AllLists sells access to lists, not SKUs. Useful as reference for payments webhooks, order state machines, and plugin architecture; adopting either wholesale adds more complexity than it removes.
- Build the directory core (hierarchy, entries, contributions, access grants) as a small custom Django or FastAPI app. Django's admin would give a non-technical owner a moderation UI almost for free (inference; not tested).

### Gaps
- Directorist and Sharetribe web-template licences and stats not obtained.
- No search was made for a Python-native open-source directory project (e.g. a Django business directory) with real traction; I found none in the searches run, but the search was narrow.

## 2. Geography and hierarchy (GeoNames, GADM, OSM, geocoders, PostGIS, Overture, Foursquare, tree patterns)

### Takeaway
Use GeoNames (CC-BY-4.0) plus OSM-derived admin boundaries as the seed hierarchy, keep OSM-derived geometry in a separate, ODbL-aware layer, and avoid GADM, which is non-commercial only. Overture Places (CDLA-Permissive-2.0) and Foursquare OS Places (Apache-2.0) are the only large open POI sets with licences friendly to a commercial, partly closed product. Nominatim is GPL-3.0 but is run as a service, Photon is Apache-2.0, libpostal is MIT.

### Cited Findings
- GeoNames data is licensed under Creative Commons Attribution 4.0; the only condition is to credit GeoNames and its sources; contains 25 million+ names — [GeoNames about](https://geonames.org/about.html); [Creative Commons wiki on GeoNames](https://wiki.creativecommons.org/wiki/GeoNames) (secondary, via search snippet)
- GADM: data "can be used for non-commercial purposes only... not allowed to redistribute... or use for commercial purposes, without prior consent" — [GADM licence text mirror](https://mitra.stanford.edu/kundaje/marinovg/oak/papers/2021_COVID_BG-2/2021-03-08-figures/BGR_adm/license.txt); see also [OSM legal-talk thread on GADM licence](https://lists.openstreetmap.org/pipermail/legal-talk/2015-August/008179.html) (primary gadm.org page was blocked)
- ODbL: a "Derivative Database" that is Publicly Used triggers share-alike; a "Collective Database" (independent databases assembled together) does not, and share-alike applies only to the OSM-derived parts; publicly used Produced Works make the underlying derivative database "Publicly Used" — [OSM Collective Database Guideline](https://wiki.openstreetmap.org/wiki/Proposed_Metadata_Guideline); [OSMF Licence and Legal FAQ](https://osmfoundation.org/wiki/Licence_and_Legal_FAQ)
- Overture Places theme: 64 million+ points, licensed CDLA-Permissive-2.0; Overture uses CDLA-Permissive-2.0 "unless derived from sources requiring different licenses, such as OpenStreetMap data licensed under ODbL v1.0" — [Overture Places guide](https://docs.overturemaps.org/guides/places); [Overture FAQ](https://overturemaps.org/about/faq/) (search snippets)
- Overture Addresses theme first released July (2024) with about 200 million address records across 14 countries — [Overture address theme post](https://overturemaps.org/blog/2024/introducing-overture-maps-address-theme/) (snippet; Pakistan coverage not confirmed)
- Foursquare Open Source Places: 100 million+ POIs, about 22 core attributes, updated monthly, Apache-2.0, free for commercial use, Parquet on S3 — [Foursquare announcement](https://foursquare.com/?p=44932); [OSM community thread](https://community.openstreetmap.org/t/foursquare-releases-100m-poi-dataset-under-apache-2-0/121883)
- Overture `data` repo (code/schema, not the data itself): about 1.2k stars, MIT per filter, `updated_at` 2026-10-02 — [OvertureMaps/data](https://github.com/OvertureMaps/data)
- Nominatim: about 4.5k stars, GPL-3.0, last push 2026-09-30, Python — [osm-search/Nominatim](https://github.com/osm-search/Nominatim)
- Photon (Komoot): about 3.1k stars, Apache-2.0, last push 2026-09-24, Java, Elasticsearch-based — [komoot/photon](https://github.com/komoot/photon)
- Pelias: about 3.6k stars, MIT, last push 2026-07-24, 234 open issues, Elasticsearch-based — [pelias/pelias](https://github.com/pelias/pelias)
- libpostal: about 4.9k stars, MIT, last push 2026-05-13, 299 open issues — [openvenues/libpostal](https://github.com/openvenues/libpostal)
- PostGIS (GitHub mirror): about 2.2k stars, GPL-2.0 per filter, `updated_at` 2026-10-04 — [postgis/postgis](https://github.com/postgis/postgis)
- django-treebeard (tree storage for Django: materialised path, nested sets, adjacency list): about 1.2k stars, `updated_at` 2026-10-02; licence not verified — [django-treebeard/django-treebeard](https://github.com/django-treebeard/django-treebeard)
- Pakistan's administrative structure per one data vendor: provinces/autonomous territories, districts, about 596 tehsils and 6,000+ union councils — [GeoPostcodes Pakistan](https://www.geopostcodes.com/country/pakistan/administrative-divisions/) (commercial vendor page, treat as indicative)
- OCHA is cited as a source of official Pakistan admin-boundary data (country, province, district, tehsil) — [pkmapr R package manual](https://cran.r-project.org/web/packages/pkmapr/refman/pkmapr.html) (secondary)

### Inferences
- Geocoders (Nominatim, Photon, Pelias) are useful mainly for normalising contributor-entered addresses to a node in the tree and for place search; they are not needed for MVP if you let contributors pick from a pre-seeded tree. Nominatim's GPL-3.0 applies to its code, which you would run as a separate service, not link into your app (my reading; confirm with counsel). OSM data used by any of them remains ODbL.
- A cautious licensing architecture: keep ODbL-derived data (OSM boundaries, OSM-derived Overture places) in a clearly separate table/layer with attribution, and do not merge it row-by-row into your proprietary contributor lists, so that your own contributed data is a Collective Database rather than a Derivative Database. This is an interpretation of the ODbL guidance above, not legal advice.
- For the hierarchy itself, three standard PostgreSQL options are the `ltree` extension (path column, fast subtree queries), a closure table (explicit ancestor/descendant rows), and adjacency list with recursive CTEs. Given a fixed, shallow 8-level hierarchy that rarely changes, `ltree` or a simple adjacency list plus a denormalised ancestor-ids array is likely enough. This comes from general PostgreSQL knowledge; I did not fetch documentation in this session.
- Pakistan's real hierarchy (province, division, district, tehsil, union council) is more granular than the vendor page lists; the user's "division" level exists in Pakistan's administration but I did not confirm the OSM `admin_level` mapping for each.
- Foursquare OS Places and Overture Places could pre-seed (or be used to cross-check) entries per city, but their Pakistan coverage and quality are unverified and are likely thin outside major cities.

### Gaps
- OSM Pakistan admin-boundary completeness and `admin_level` mapping: the wiki search returned no relevant page.
- Pakistan coverage and quality of Overture Places/Addresses and FSQ OS Places not measured.
- GeoNames Pakistan admin2/postal code coverage not confirmed (download.geonames.org was blocked).
- Licences of django-treebeard, python-stdnum, and other tree libraries not verified.
- PostgreSQL ltree/closure-table guidance not sourced.

## 3. Deduplication and entity resolution

### Takeaway
Use rapidfuzz plus python-phonenumbers as the first line of dedup (normalise phone to E.164, fuzzy-match names), and keep Splink (MIT, very active) as the upgrade path for probabilistic record linkage. libpostal is useful but heavyweight and Pakistani addresses are informal. dedupe (MIT) is less recently maintained; recordlinkage is the weakest on activity.

### Cited Findings
- Splink: probabilistic record linkage with multiple SQL backends (DuckDB, Spark), about 2.5k stars, MIT, last push 2026-09-30, 218 open issues — [moj-analytical-services/splink](https://github.com/moj-analytical-services/splink)
- dedupe: about 4.5k stars, MIT, last push 2025-07-29 (about 14 months before research date), 92 open issues — [dedupeio/dedupe](https://github.com/dedupeio/dedupe)
- RapidFuzz: about 4.2k stars, MIT, last push 2026-09-28 — [rapidfuzz/RapidFuzz](https://github.com/rapidfuzz/RapidFuzz)
- python-phonenumbers (port of Google's libphonenumber): about 3.8k stars, Apache-2.0, last push 2026-09-24, only 11 open issues — [daviddrysdale/python-phonenumbers](https://github.com/daviddrysdale/python-phonenumbers)
- recordlinkage: about 1.1k stars, BSD-3-Clause per filter; it was NOT among repos pushed after 2026-04-04 (so last push is older than about 6 months), 65 open issues — [J535D165/recordlinkage](https://github.com/J535D165/recordlinkage)
- libpostal: see section 2 (MIT, push 2026-05-13, topics include deduplication, record-linkage) — [openvenues/libpostal](https://github.com/openvenues/libpostal)
- python-stdnum (validates standard numbers, e.g. national ID formats): about 600 stars, `updated_at` 2026-09-30; licence not verified — [arthurdejong/python-stdnum](https://github.com/arthurdejong/python-stdnum)

### Inferences
- Practical pipeline: normalise (strip, case-fold, Urdu/English transliteration if needed), parse phone with phonenumbers into E.164 (strongest exact key), blocking on city plus phone or name prefix, rapidfuzz scoring for name/address, and a human-review queue for the middle band. Splink becomes worthwhile once you have hundreds of thousands of rows and want calibrated match probabilities.
- Contributor-submitted duplicates are mostly same business, different spelling, shop-number variants, so phone number is likely the best dedup key; this is a hypothesis to test on real imports, not a finding.
- libpostal's address parser is trained on global data; its accuracy on Pakistani informal addresses (landmarks, "near X chowk") is unverified and I would not make it a dependency for MVP.

### Gaps
- No benchmark of these tools on Pakistani business names/addresses (Roman Urdu spelling variance).
- Exact recordlinkage last-commit date and dedupe maintenance trajectory not examined beyond the dates above.

## 4. Data import, cleaning and validation

### Takeaway
Pydantic (validation models) plus Polars or pandas (bulk cleaning) is a sufficient, well-maintained stack for CSV/Excel imports. Frictionless is a reasonable optional schema/validation layer; Great Expectations could not be checked.

### Cited Findings
- Pydantic: about 28.9k stars, MIT per filter, `updated_at` 2026-10-04, 591 open issues — [pydantic/pydantic](https://github.com/pydantic/pydantic)
- Polars: about 39.9k stars, MIT per filter, `updated_at` 2026-10-04, 2,930 open issues — [pola-rs/polars](https://github.com/pola-rs/polars)
- Frictionless-py: about 844 stars, MIT per filter, `updated_at` 2026-09-26, 247 open issues — [frictionlessdata/frictionless-py](https://github.com/frictionlessdata/frictionless-py)
- FastAPI (which builds on Pydantic): about 102.8k stars, MIT per filter, `updated_at` 2026-10-04 — [fastapi/fastapi](https://github.com/fastapi/fastapi)

### Inferences
- Import flow suggestion: upload to staging table, row-level Pydantic validation with per-row error report returned to the contributor, phone/geo normalisation, dedupe check, then promote to entries. Excel parsing libraries (openpyxl etc.) were not researched.
- Frictionless adds a declarative schema per upload template, but with 247 open issues and a small star count, plain Pydantic models are lower risk for MVP.

### Gaps
- Great Expectations: `great-expectations/great_expectations` was not returned by the GitHub search, so no stats or licence were obtained.
- pandas, openpyxl, pyexcel and CSV sniffing libraries not checked.

## 5. Ledgers and revenue splitting; Pakistani payment gateways

### Takeaway
No open-source ledger is clearly the right adoption for MVP. Blnk (Go, Apache-2.0, Postgres-backed) and TigerBeetle (Apache-2.0, very high-scale) are the credible options if you want a ready-made double-entry engine; for a small team on Python/PostgreSQL the lowest-risk path is a minimal append-only double-entry table design that you own, using Blnk as a design reference. Pakistan-specific gateway tooling is thin and mostly unofficial.

### Cited Findings
- Blnk: Go, "open-source ledger and financial core", topics include double-entry, postgres-ledger, reconciliation, wallets; about 545 stars, 7 open issues, Apache-2.0 per filter, `updated_at` 2026-10-04, pushed after 2026-04-04 — [blnkfinance/blnk](https://github.com/blnkfinance/blnk)
- TigerBeetle: Zig, "financial transactions database", about 17.1k stars, Apache-2.0 per filter, `updated_at` 2026-10-04 — [tigerbeetle/tigerbeetle](https://github.com/tigerbeetle/tigerbeetle)
- Formance (`formancehq/stack`): Go, "Open Source Infrastructure for the Financial Internet", about 527 stars; licence not verified (my attempt to read its files was denied) — [formancehq/stack](https://github.com/formancehq/stack)
- Medici: Node.js + Mongoose double-entry, about 360 stars, MIT per filter, `updated_at` 2026-09-24 — [flash-oss/medici](https://github.com/flash-oss/medici)
- Beancount: Python plain-text double-entry accounting, about 6.1k stars, GPL-2.0 per filter, `updated_at` 2026-10-04 — [beancount/beancount](https://github.com/beancount/beancount)
- django-money: about 1.8k stars, repo is ARCHIVED on GitHub (read-only), so not a safe new dependency — [django-money/django-money](https://github.com/django-money/django-money)
- Unofficial JazzCash PHP library exists (`zfhassaan/jazzcash`, on Packagist); a WooCommerce plugin supports Safepay hosted checkout with cards plus Easypaisa and JazzCash wallets in PKR — [zfhassaan/jazzcash](https://github.com/zfhassaan/jazzcash); [Safepay WooCommerce gateway listing](https://ecosire.com/apps/woocommerce/woo-safepay-pk-gateway)
- A third-party "pakistan payments stack" AI skill discusses JazzCash/Easypaisa/PSP integration, PKR billing, webhook reliability and reconciliation; low-quality secondary content, listed only for completeness — [Tessl registry entry](https://tessl.io/registry/skills/github/administrakt0r/AI-Agents-Safe-Coding-Skills/pakistan-payments-stack--pakistan-payments-stack)

### Inferences
- Medici (MongoDB) and Beancount (text files, GPL) do not fit a Postgres web app; use as conceptual references only.
- Revenue share design: one `ledger_entry` table (account_from, account_to, amount in integer paisa, currency, idempotency key, reference to purchase and to entry-contribution), immutable rows, balances derived or cached; payouts as a separate state machine. Store money as integer minor units rather than relying on an archived money library; `py-moneyed` or `Decimal` are alternatives I did not verify.
- Whether the platform may hold contributor balances and pay out in Pakistan may carry regulatory implications (payment-service licensing); this is outside the scope of what I researched and needs a Pakistani legal opinion.
- Safepay or similar aggregators that already support cards plus local wallets are the pragmatic collection route; I did not verify their APIs, fees, or payout/split support, so confirm marketplace-split capability with the provider.

### Gaps
- Official developer documentation for JazzCash, Easypaisa, Safepay, PayFast not reached (searches returned only third-party items); marketplace payout/split capabilities unknown.
- Formance licence and current product status not verified.
- No Python double-entry library (e.g. django-ledger, python-accounting) was evaluated.

## 6. Web stack: frameworks, auth, search, UI, i18n

### Takeaway
Django (BSD-3) with a Next.js or Astro front end is well supported; FastAPI (MIT) is the lighter alternative. For search start with PostgreSQL full-text/trigram and graduate to Meilisearch (MIT, 59k stars) only when needed; Typesense is GPL-3.0 and OpenSearch is heavy. No UI-kit or Urdu/RTL research was done.

### Cited Findings
- Next.js: about 143k stars, MIT per filter, `updated_at` 2026-10-04 — [vercel/next.js](https://github.com/vercel/next.js)
- Astro: about 63k stars, `updated_at` 2026-10-04; licence not verified by filter — [withastro/astro](https://github.com/withastro/astro)
- Django: about 91.3k stars, BSD-3 per filter — [django/django](https://github.com/django/django)
- FastAPI: about 102.8k stars, MIT per filter — [fastapi/fastapi](https://github.com/fastapi/fastapi)
- Meilisearch: about 59.5k stars; Community LICENSE-MIT file (Copyright Meili SAS) read directly; repo may contain separately licensed enterprise components (not verified), pushed after 2026-04-04 — [meilisearch/meilisearch](https://github.com/meilisearch/meilisearch); [LICENSE-MIT](https://raw.githubusercontent.com/meilisearch/meilisearch/main/LICENSE-MIT)
- Typesense: about 26.6k stars, GPL-3.0 per filter, `updated_at` 2026-10-04, 911 open issues — [typesense/typesense](https://github.com/typesense/typesense)
- OpenSearch: about 13.8k stars, Apache-2.0 per filter, 3,208 open issues — [opensearch-project/OpenSearch](https://github.com/opensearch-project/OpenSearch)
- Supabase (Postgres platform with auth, PostgREST): about 111k stars, `updated_at` 2026-10-04; licence not verified by filter — [supabase/supabase](https://github.com/supabase/supabase)
- pgvector: about 23.2k stars, `updated_at` 2026-10-04; licence not verified — [pgvector/pgvector](https://github.com/pgvector/pgvector)
- MapLibre GL JS (open map rendering): about 11.8k stars, `updated_at` 2026-10-04; licence not verified — [maplibre/maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js)
- PMTiles and Tippecanoe (serverless vector tiles from boundaries): about 3.1k stars each, active in October 2026; licences not verified — [protomaps/PMTiles](https://github.com/protomaps/PMTiles); [mapbox/tippecanoe](https://github.com/mapbox/tippecanoe)

### Inferences
- Because SEO is central (one indexable page per geography node), server-rendered pages via Next.js or Astro (static + incremental rendering for tens of thousands of city/district pages) fit. Astro is likely the lighter choice for mostly-read pages; Next.js has the larger ecosystem for authenticated dashboards (inference).
- Meilisearch's typo tolerance and facets suit "restaurants in Gulberg"-style search; PostgreSQL `pg_trgm` plus full-text should be enough for MVP and avoids another service (general knowledge, unverified here).
- Typesense's GPL-3.0 is acceptable when run as an unmodified separate service, but Meilisearch's MIT licence is simpler for a commercial product.
- A map of admin boundaries could be served with PMTiles + MapLibre cheaply, but only with ODbL-compliant attribution if the geometry is OSM-derived.

### Gaps
- Auth libraries (django-allauth, Auth.js, better-auth, authlib) not researched.
- Tailwind UI kits (shadcn/ui, DaisyUI, Flowbite) not researched.
- Urdu/RTL i18n tooling (Django i18n, next-intl, Tailwind RTL plugins) and Urdu fonts not researched.
- Licences of Astro, Supabase, MapLibre, pgvector not confirmed.

## 7. Messaging and outreach

### Takeaway
For compliant campaigns use the official WhatsApp Business Cloud API (paid per template message) and a self-hosted email sender; listmonk is the strongest open-source campaign manager but is AGPL-3.0. Unofficial WhatsApp libraries (Baileys, whatsapp-web.js) violate WhatsApp's ToS and carry real ban risk; do not build a commercial campaign product on them.

### Cited Findings
- listmonk: Go, newsletter/mailing-list manager, topics include sms-gateway and transactional-emails, about 23.7k stars, AGPL-3.0 per filter, `updated_at` 2026-10-04, 119 open issues — [knadh/listmonk](https://github.com/knadh/listmonk)
- Postal: Ruby mail delivery platform, about 16.8k stars, MIT per filter, `updated_at` 2026-10-04 — [postalserver/postal](https://github.com/postalserver/postal)
- Mautic: PHP marketing automation, about 10.7k stars, GPL-3 (read directly from LICENSE.txt), `updated_at` 2026-10-04 — [mautic/mautic](https://github.com/mautic/mautic); [LICENSE.txt](https://raw.githubusercontent.com/mautic/mautic/7.x/LICENSE.txt)
- Chatwoot: Ruby omnichannel support desk (topic whatsapp), about 37.5k stars, 1,538 open issues; MIT with a separately licensed `enterprise/` directory (read directly) — [chatwoot/chatwoot](https://github.com/chatwoot/chatwoot); [LICENSE](https://raw.githubusercontent.com/chatwoot/chatwoot/develop/LICENSE)
- Baileys (WhatsApp Web socket library): about 11.2k stars, MIT per filter, `updated_at` 2026-10-04; marked reverse-engineering — [WhiskeySockets/Baileys](https://github.com/WhiskeySockets/Baileys)
- WhatsApp ToS prohibits non-personal, bulk and automated messaging on the consumer app and use of unofficial/modified clients; whatsapp-web.js and Baileys automate the consumer app and "by design violate the ToS" with non-deterministic ban risk; the strongest ban signals are messaging strangers and block/report rate; the official Business/Cloud API is the zero-ToS-risk route — [Dragapp analysis](https://www.dragapp.com/blog/whatsapp-mcp-server/); [Zylos research](https://zylos.ai/research/2026-01-26-whatsapp-api-automation) (secondary sources; confirm against WhatsApp's own terms)
- WhatsApp Business Platform moved to per-message pricing on 2025-07-01, charged per delivered template (marketing, utility, authentication); Pakistan utility and authentication rates rose on 2026-04-01; marketing rates range from $0.0109 (Turkey) to $0.1597 (Netherlands) by country — [Meta pricing docs](https://developers.facebook.com/docs/whatsapp/pricing) (via search snippet; Pakistan marketing rate not retrieved)

### Inferences
- Selling "message campaigns" to businesses listed in the directory means contacting people who did not opt in. Both WhatsApp Business policy and email anti-spam rules generally require opt-in; build an opt-in/consent table and unsubscribe handling first, and consider restricting campaigns to contacts who have opted in or to the buyer's own customers (inference; legal review needed).
- listmonk (AGPL-3.0) can be deployed unmodified as a separate service with API integration, which is the usual low-risk pattern, but any modification served to users triggers AGPL source-sharing (my reading of AGPL; confirm with counsel). Postal (MIT) is a safer licence if you want to embed or modify; it is an SMTP delivery server, not a campaign manager.
- Official WhatsApp Cloud API costs are per delivered template, so campaign pricing should pass through Meta's per-country rate plus a margin; check Pakistan's current marketing rate before pricing.

### Gaps
- Pakistan marketing-template rate not retrieved.
- No open-source tool specific to WhatsApp Cloud API opt-in management was verified.
- Pakistan SMS gateway tooling and PTA/PECA rules on bulk messaging not researched.
- Meta's own ToS pages not fetched directly (only secondary summaries).

## 8. Anti-fraud, moderation, rate limiting, anti-scraping, audit logging

### Takeaway
Small, well-maintained Python libraries cover rate limiting and brute-force protection; ALTCHA is an MIT, privacy-friendly CAPTCHA alternative to Cloudflare Turnstile. Audit logging was not verified.

### Cited Findings
- ALTCHA: self-hosted proof-of-work CAPTCHA alternative, about 2.8k stars, MIT per filter, `updated_at` 2026-10-04, 0 open issues — [altcha-org/altcha](https://github.com/altcha-org/altcha)
- django-axes: failed-login tracking, about 1.7k stars, MIT per filter, `updated_at` 2026-10-02 — [jazzband/django-axes](https://github.com/jazzband/django-axes)
- Flask-Limiter: about 1.2k stars, MIT per filter, `updated_at` 2026-10-02, 7 open issues — [alisaifee/flask-limiter](https://github.com/alisaifee/flask-limiter)
- django-ratelimit: cache-based rate limiting, about 1.1k stars, `updated_at` 2026-09-16; licence not verified — [jsocol/django-ratelimit](https://github.com/jsocol/django-ratelimit)
- django-model-utils: about 2.8k stars, BSD-3 per filter, `updated_at` 2026-10-04 — [jazzband/django-model-utils](https://github.com/jazzband/django-model-utils)
- django-simple-history (audit trail): searched as `jazzband/django-simple-history`; not returned by the GitHub search, so no data.

### Inferences
- Anti-scraping for a data-resale product is mostly about per-user quotas, signed/expiring access grants, pagination caps, watermarking exports (e.g. seeded canary rows) and rate limits keyed on account not IP; libraries above cover the rate-limit piece only.
- For audit logging, a Postgres append-only `audit_event` table written in the same transaction as changes is simple and sufficient; Django admin log or simple-history are options but unverified here.
- Jazzband projects are community-maintained; Jazzband's sunsetting status was not checked, so confirm project health before depending on django-axes.

### Gaps
- Cloudflare Turnstile terms and alternatives (hCaptcha, mCaptcha, Cap) not compared.
- Moderation tooling (spam classification, contributor reputation) not researched.
- Audit-log libraries (django-auditlog, simple-history, pgaudit) not verified.

## 9. Deployment

### Takeaway
For a non-technical owner, Coolify (Apache-2.0, 62.6k stars) is the most active self-hosted PaaS, with Dokku (MIT) as the leaner option and CapRover as another; Caddy gives automatic HTTPS without certbot. For Postgres backups, pgBackRest, WAL-G and restic are all active. Cloud Run vs Compute Engine was not researched.

### Cited Findings
- Coolify: self-hostable PaaS (Vercel/Heroku alternative), PHP/Laravel, about 62.6k stars, Apache-2.0 per filter, 736 open issues, pushed after 2026-04-04 — [coollabsio/coolify](https://github.com/coollabsio/coolify)
- Dokku: Docker-powered PaaS, about 32.2k stars, MIT per filter, only 31 open issues, pushed after 2026-04-04 — [dokku/dokku](https://github.com/dokku/dokku)
- CapRover: Docker+nginx PaaS, about 15.2k stars, `updated_at` 2026-10-04, pushed after 2026-04-04; licence not verified — [caprover/caprover](https://github.com/caprover/caprover)
- Caddy: web server with automatic HTTPS, about 76.5k stars, Apache-2.0 per filter, pushed after 2026-04-04 — [caddyserver/caddy](https://github.com/caddyserver/caddy)
- pgBackRest: PostgreSQL backup/restore with S3/GCS/Azure support, incremental/differential, about 4.4k stars, pushed after 2026-04-04; licence not verified — [pgbackrest/pgbackrest](https://github.com/pgbackrest/pgbackrest)
- WAL-G: about 4.3k stars, pushed/updated 2026-10-04; licence not verified — [wal-g/wal-g](https://github.com/wal-g/wal-g)
- restic: general backup, about 36.4k stars, `updated_at` 2026-10-04; licence not verified — [restic/restic](https://github.com/restic/restic)

### Inferences
- A single VM (Compute Engine or any VPS) running Coolify or Dokku with Caddy, PostgreSQL, and nightly pgBackRest/restic backups to object storage is the simplest operable setup for a non-technical owner; Coolify's web UI is the main advantage, though its 736 open issues suggest churn. Cloud Run would suit stateless web containers but needs a managed Postgres (extra cost); neither claim was verified against pricing.
- Self-hosting inside Pakistan vs abroad (latency, data-protection) not considered.

### Gaps
- Google Cloud Run vs Compute Engine pricing and fit: not researched.
- Licences for CapRover, pgBackRest, WAL-G, restic not verified.
- Managed Postgres options (Cloud SQL, Neon, Supabase) not compared.

## 10. Ranked shortlist and minimum set to adopt first

### Takeaway
Adopt first (all permissive, active, verified): Django (or FastAPI) + PostgreSQL/PostGIS, Pydantic, Polars, python-phonenumbers, RapidFuzz, GeoNames (CC-BY) as the geography seed, Next.js or Astro for SEO pages, Caddy plus Coolify or Dokku for deployment, and ALTCHA plus a rate-limit library. Defer Splink, a ledger engine (Blnk/TigerBeetle), Meilisearch, geocoders and campaign tools until there is proven need.

### Cited Findings
- Tier 1 (adopt for MVP; licence verified permissive or standard, active):
  - python-phonenumbers (Apache-2.0, push 2026-09-24) — [repo](https://github.com/daviddrysdale/python-phonenumbers)
  - RapidFuzz (MIT, push 2026-09-28) — [repo](https://github.com/rapidfuzz/RapidFuzz)
  - Pydantic (MIT) and Polars (MIT), both updated 2026-10-04 — [pydantic](https://github.com/pydantic/pydantic); [polars](https://github.com/pola-rs/polars)
  - Django (BSD-3) or FastAPI (MIT) — [django](https://github.com/django/django); [fastapi](https://github.com/fastapi/fastapi)
  - Next.js (MIT) or Astro (licence not verified) — [next.js](https://github.com/vercel/next.js); [astro](https://github.com/withastro/astro)
  - Caddy (Apache-2.0) and Coolify (Apache-2.0) or Dokku (MIT) — [caddy](https://github.com/caddyserver/caddy); [coolify](https://github.com/coollabsio/coolify); [dokku](https://github.com/dokku/dokku)
  - ALTCHA (MIT), Flask-Limiter (MIT) or django-ratelimit (licence unverified), django-axes (MIT) — [altcha](https://github.com/altcha-org/altcha); [flask-limiter](https://github.com/alisaifee/flask-limiter); [django-axes](https://github.com/jazzband/django-axes)
  - GeoNames (CC-BY-4.0) as hierarchy seed — [GeoNames](https://geonames.org/about.html)
- Tier 2 (adopt when volume or features require it):
  - Splink (MIT, push 2026-09-30) — [repo](https://github.com/moj-analytical-services/splink)
  - PostGIS (GPL-2.0 extension) for spatial queries — [repo](https://github.com/postgis/postgis)
  - Meilisearch (MIT) — [repo](https://github.com/meilisearch/meilisearch)
  - Blnk (Apache-2.0) as ledger or as design reference; TigerBeetle (Apache-2.0) at high scale — [blnk](https://github.com/blnkfinance/blnk); [tigerbeetle](https://github.com/tigerbeetle/tigerbeetle)
  - Foursquare OS Places (Apache-2.0) and Overture Places (CDLA-Permissive-2.0) as optional POI seeds — [Foursquare](https://foursquare.com/?p=44932); [Overture](https://docs.overturemaps.org/guides/places)
  - pgBackRest or restic for backups (licences unverified) — [pgbackrest](https://github.com/pgbackrest/pgbackrest); [restic](https://github.com/restic/restic)
  - Official WhatsApp Cloud API for campaigns (paid per delivered template) — [Meta pricing](https://developers.facebook.com/docs/whatsapp/pricing)
- Licence flags for a commercial, partly closed-data product:
  - AGPL-3.0: listmonk — [repo](https://github.com/knadh/listmonk)
  - GPL-3.0: Nominatim, Mautic, Typesense, HivePress — [Nominatim](https://github.com/osm-search/Nominatim); [Mautic LICENSE](https://raw.githubusercontent.com/mautic/mautic/7.x/LICENSE.txt); [Typesense](https://github.com/typesense/typesense); [HivePress](https://github.com/hivepress/hivepress)
  - GPL-2.0: Beancount, PostGIS — [Beancount](https://github.com/beancount/beancount); [PostGIS](https://github.com/postgis/postgis)
  - Open-core with enterprise carve-outs: Medusa, Chatwoot — [Medusa LICENSE](https://raw.githubusercontent.com/medusajs/medusa/develop/LICENSE); [Chatwoot LICENSE](https://raw.githubusercontent.com/chatwoot/chatwoot/develop/LICENSE)
  - Data: ODbL (OSM and OSM-derived Overture content, share-alike on derivative databases); GADM non-commercial only — [OSM Collective Database Guideline](https://wiki.openstreetmap.org/wiki/Proposed_Metadata_Guideline); [GADM licence text mirror](https://mitra.stanford.edu/kundaje/marinovg/oak/papers/2021_COVID_BG-2/2021-03-08-figures/BGR_adm/license.txt)
  - Not safe as new dependencies: unofficial WhatsApp libraries (ToS) — [Dragapp analysis](https://www.dragapp.com/blog/whatsapp-mcp-server/); django-money (archived) — [repo](https://github.com/django-money/django-money)

### Inferences
- Recommended minimum first set: (1) Django + PostgreSQL (+ PostGIS later), with `ltree` or adjacency-list hierarchy seeded from GeoNames; (2) Pydantic + Polars for CSV/Excel imports; (3) python-phonenumbers + RapidFuzz for dedupe; (4) Next.js or Astro for server-rendered geography pages; (5) Caddy + Coolify (or Dokku) on one VM with PostgreSQL backups; (6) ALTCHA + rate limiting + a hand-built append-only audit table; (7) an in-house, Postgres-based double-entry ledger table with integer paisa amounts, deferring Blnk/TigerBeetle.
- Components that do not need to be adopted at launch: Splink, Meilisearch, geocoders, listmonk/Mautic/Chatwoot, any WhatsApp library. Campaign delivery can be a manual or API-based Cloud API integration once the opt-in model is designed.
- Everything in Tier 1 is permissively licensed, so none forces open-sourcing your own code; the main legal risk sits in data (ODbL layer) and in outbound messaging consent, not in code licences.

### Gaps
- Several Tier 1/2 licences are unverified (Astro, django-ratelimit, pgBackRest, restic); confirm in the repos before final adoption.
- Last-commit dates were not individually confirmed for batch 3 repos (Django, Next.js, Astro, FastAPI, Pydantic etc.); they showed `updated_at` within the last days, which suggests but does not prove active commits.
- No coverage of Pakistan-specific commercial concerns (data protection law, payment licensing, PTA messaging rules), Urdu/RTL tooling, Tailwind UI kits, or Cloud Run vs Compute Engine economics.
