# Group 1: Local directories and maps - list types seen (research, 2026-10-05)

Scope: platforms 1 to 11 in `00_platform_inventory.md`.

Method and limits (read first):
- Only WebSearch snippets were usable. WebFetch and curl to the platforms' own sites (yelp.com, docs.developer.yelp.com, martech.zone, justdial.com, sulekha.com) were blocked by the egress proxy (EGRESS_BLOCKED / 403). Full category trees could therefore NOT be read directly.
- The WebSearch budget for the session ran out (200 of 200) after about 28 of my own searches, before I could cover Apple Business Connect categories, Facebook category count, and Yelp sub-category examples. These are gaps (section 4).
- Labels: VERIFIED-SNIPPET = figure appears in a search snippet from the named URL, dated where the snippet gave a date. UNVERIFIED = single secondary source, or undated, or from my background knowledge with no URL this session. Anything tagged "(background)" has no URL and must be checked before use.
- Search snippets are model-summarised text, not page text. Treat every number as needing a click-through before it goes in a public document.

---

## 1. Per-platform findings

### 1. Google Maps / Google Business Profile (GBP)
- What it is: Google's place and business listing layer behind Maps and Search. Business owners claim a profile and choose categories.
- Organisation: by place (every profile is a pinned location) and by category (one primary plus up to 9 additional). Source for 1 + 9: https://daltonluka.com/blog/google-my-business-categories (secondary, 2026).
- Category count: 4,046 categories as at 9 May 2026 (https://daltonluka.com/blog/google-my-business-categories, UNVERIFIED: single secondary). 4,098 US categories as at 23 Oct 2024 (shown in the same search result set; sources included https://martech.zone/google-business-profile-category-list/ and https://classification.codes/classifications/industry/gmb, UNVERIFIED: could not attribute the figure to one page). Google adds and retires categories often.
- Primary-category examples named in results: restaurant, cafe, supermarket, pharmacy, hairdresser, dentist, veterinarian, lawyer, financial advisor, real estate agent, gas station, auto repair shop, gym, electronics store, clothing store, hospital, childcare, school (https://www.cyberoptik.net/blog/google-business-profile-categories/ and https://uberall.com/en-us/resources/blog/google-categories-and-attributes, UNVERIFIED).
- Size of some categories (counts of businesses): Gas station 195,051 (8th most popular), Bakery 101,543 (37th), Pharmacy 81,108 (55th). Source https://www.openwebninja.com/blog/top-google-maps-categories, undated, UNVERIFIED.
- Secondary-category example: restaurant gets pizzeria, catering, takeaway restaurant, vegan restaurant (https://uberall.com/en-us/resources/blog/google-categories-and-attributes, UNVERIFIED).
- Top-level groups: GBP has no public top-level tree in the sources found; the category list is flat and searchable. (UNVERIFIED conclusion from absence.)
- Paid / most commercial: Google Local Services Ads (LSA) are pay-per-lead and limited to defined verticals, grouped as Home, Business, Health, Learning, Care, Wellness, Beauty, Automotive (https://business.google.com/us/ad-solutions/local-service-ads/). Named LSA job types:
  - Home (Google Verified badge): appliance repair, carpenter, carpet cleaning, countertop pro, drain expert, electrician, fencing, flooring, foundations, garage door, general contractor, handyman, home inspector, insulation, home security, home theater, house cleaning, HVAC, junk removal, landscaper, lawn care, locksmith, moving, painter, pest control, plumber, pool cleaning, pool contractor, roofing, sewage, siding, snow removal, solar, tree services, water damage restoration, window cleaning, window repair.
  - Business (Google Screened badge): lawyers by speciality (bankruptcy, business, contract, criminal, disability, DUI, estate, family, immigration, IP, labor, litigation, malpractice, personal injury, real estate, tax, traffic), financial planner, real estate agent, tax specialist, storage, cellphone and laptop repair.
  - Source: https://techwyse.com/?p=51770 and the Google LSA page above (UNVERIFIED for the full list: snippet only; LSA list is per country).
- Entry fields unique to a category: not captured (gap). Background (no URL): GBP has category-specific attributes and features such as hotel amenities, restaurant menus and reservations, healthcare provider fields, and service lists.

### 2. Justdial (India)
- What it is: India's largest local search and listing business; phone, app and web.
- Organisation: by city and locality plus category plus keyword. Search by location, category and keywords (https://yespress.io/justdial.md, UNVERIFIED).
- Scale: about 32.8 million listings as at 30 June 2022 (https://alphastreet.com/india/just-dial-research-tear-sheet-q1-fy-2023/); earlier figure 27.7 million (https://www.klazify.com / https://vizologi.com/business-strategy-canvas/justdial-business-model-canvas/, undated, UNVERIFIED). Total number of categories: NOT FOUND in any source.
- Category names seen on its search surface: Restaurants, Hotels, Beauty Spa, Home Decor, Education, Rent & Hire, Hospitals, Contractors, Pet Shops, PG/Hostels, Estate Agent, Dentists, Gym, Consultants, Event Organisers, Driving Schools, Packers & Movers, Courier Service (https://apify.com/themineworks/justdial-business and similar scraper pages, UNVERIFIED: tertiary).
- Other services: flower delivery, doctor appointment, laundry pickup, grocery shopping, pharmacy supplies (https://yespress.io/justdial.md, UNVERIFIED). JD Mart (B2B portal), JD Business, JD Omni (same source).
- Paid: free basic listing; paid tiers Platinum, Gold, Silver, weekly / monthly / quarterly / annual; pricing varies by business category, geography and package type (https://vizologi.com/business-strategy-canvas/justdial-business-model-canvas/ and https://www.outlookbusiness.com/markets/feature/wait-dont-justdial-379, UNVERIFIED). 5.61 lakh active paid campaigns in Q2 FY24 (https://inc42.com/?p=421600, snippet cites Q2 FY24).
- Which categories are most commercial: not stated in sources (gap). Background (no URL): healthcare, real estate, education and home services are widely described as high-spend.

### 3. Sulekha (India)
- What it is: local services classifieds and lead marketplace; founded 1998 (https://yourstory.com/companies/sulekha).
- Organisation: by city and by service category.
- Category counts, inconsistent across dates: 800+ categories across 40+ cities (https://bwdisrupt.com/article/sulekha-catering-to-over-40-cities-across-800-plus-categories-in-local-service-market-99824); roughly 1,200 categories (same search result set, UNVERIFIED, undated); 200 categories and 50,000 professionals in about 40 cities (https://www.impactonnet.com/interview/sulekha-is-the-airbnb-of-digital-expert-service-providers-6740.html, UNVERIFIED, undated).
- Top-level groups: three spheres (Home Improvement, Life Improvement, Self Improvement) divided into six categories (https://www.businessinsider.in/all-services-are-just-one-touch-away/amp_articleshow/49904920.cms, UNVERIFIED, dated about 2015). Also described as Home Services, Education (coaching and training), Lifestyle (events and entertainment) (https://bwdisrupt.com/... as above).
- Sub-categories named: carpenters, brokers, pest control, packers and movers, interior decorators, modular kitchens, consultants, lawyers, GST tax specialists, graphic designers, caterers, wedding planners, decorators, overseas admissions counsellors, tutors, test-preparation specialists, computer training, coaching and tuition, property, rentals, domestic workers (https://www.thenewsminute.com/atom/bengaluru-leads-online-searches-domestic-workers-sulekha-unlock-10-128726).
- Paid: leads sold to verified service providers; the markhub24 piece describes a "verified service provider model" (https://www.markhub24.com/post/sulekha-s-verified-service-provider-model-from-digital-classifieds-to-intelligent-matchmaking, not read, UNVERIFIED).

### 4. Yelp
- What it is: US-origin reviews and local business platform.
- Organisation: by place plus category plus attributes (search filters). Yelp's own engineering blog describes a hierarchical category system (https://engineeringblog.yelp.com/2015/09/automatically-categorizing-yelp-businesses.html).
- Counts: "more than 1,500 different categories", list growing, official Yelp page (https://business.yelp.com/resources/articles/yelp-category-list/ and https://blog.yelp.com/businesses/yelp_category_list/, undated, VERIFIED-SNIPPET on count only). Another result set gave 22 primary, 498 secondary, 178 tertiary categories (https://engineeringblog.yelp.com/2015/09/automatically-categorizing-yelp-businesses.html, dated 2015, UNVERIFIED, probably out of date).
- Groups named on Yelp's own page: Entertainment (arcades, art galleries, casinos, cinema, museums, music venues); Beauty & Personal Care (barbers, day spas, hair salons, nail salons); Home Services (contractors, electricians, plumbing, landscaping, HVAC, handyman); Travel & Lodging (hotels, B&Bs, campgrounds, car rental, tours, resorts); Shopping & Retail (antiques, electronics, clothing, books, music, home and garden); Automotive (car repair, gas stations, car wash, tire shops, towing); Restaurants & Food (cuisine types); Health & Medical (doctors, dentists, acupuncture, alternative medicine); Financial Services (banks, insurance, tax, mortgage lenders); Nightlife (bars, lounges, clubs); Pets & Animals (pet services, shelters, grooming). Source: https://business.yelp.com/resources/articles/yelp-category-list/ (search summary, VERIFIED-SNIPPET).
- Machine-readable list: Yelp Fusion all-category list and Categories API give alias, title, parent and country availability (https://www.yelp.com/developers/documentation/v3/all_category_list, https://docs.developer.yelp.com/docs/resources-categories). Not read (blocked).
- Paid / commercial: Yelp advertising is cost-per-click; one law firm reported a $500 monthly budget and average $12.50 CPC for personal injury on Yelp (https://jurisdigital.com/guides/yelp-advertising-reviews-effective-for-lawyers/, UNVERIFIED single anecdote). Legal is the highest-CPC industry in search advertising generally (https://www.webfx.com/blog/ppc/businesses-with-the-highest-cost-per-click/, undated).
- Unique entry fields: not captured. Background (no URL): restaurants carry menus, price band and wait-list; home-service categories support Request a Quote.

### 5. Yellow Pages (US/Canada) and Yell (UK)
- What they are: legacy print-to-web directories organised by heading (category) and place.
- Yell: UK directory launched 1996, over 2.9 million businesses (https://www.wmtips.com/technologies/business-listings/yell/, undated, UNVERIFIED). Uses "most popular category" menus such as "days and nights out" and "gifts and shopping" (https://www.marketingweek.com/yell-com-to-offer-business-listings-search-for-mobiles/). Total heading count NOT FOUND.
- Yellow Pages US: popular headings named: Restaurants, Physicians & Surgeons, Automobile Parts, Automobile Repairing & Service, Pizza, Automobile Dealers, Beauty Salons, Attorneys/Lawyers, Dentists, Hospitals (https://www.localseoguide.com/iyp-seo-rankings-2009-part-ii-which-yellow-pages-sites-should-you-use-for-which-categories/, dated 2009, UNVERIFIED). Consumer browse groups: Automotive Services, Restaurants, Healthcare Providers, Home Improvement (same search result set, UNVERIFIED).
- Paid: sponsored links and enhanced listings (https://www.ukbusinessforums.co.uk/threads/yell-sponsored-link-worth-it.118062/post-933981, forum anecdotes only; which headings cost most NOT FOUND).

### 6. Bing Places and Apple Business Connect
- Bing Places: owner picks a primary and additional categories from Bing's own taxonomy (https://skills.sh/garrettjsmith/localseoskills/bing-places, UNVERIFIED). Category count NOT FOUND.
- Apple Business Connect: Apple "significantly increased the number of top-level categories and subcategories" to match Maps search behaviour (https://impressivemagazine.com/apple-business-connect-categories-and-attributes/amp/, UNVERIFIED). Three types of categories exist (primary, additional; count of four additional shown in the UI; partners can add more through the API) (https://support.apple.com/guide/apple-business-connect/intro-abcb205640e7/web, snippet only). Counts and names NOT FOUND.
- Both are free claim-and-edit layers; no paid categories seen.

### 7. Foursquare / Swarm
- What it is: venue database and check-in app, now mostly a places-data business.
- Organisation: by place and a hierarchical category tree.
- Counts: proprietary taxonomy of 1,000+ categories, hierarchy up to six levels (https://docs.foursquare.com/data-products/docs/places-categories-faqs, undated, VERIFIED-SNIPPET).
- 10 top-level categories: Arts and Entertainment; Business and Professional Services; Community and Government; Dining and Drinking; Event; Health and Medicine; Landmarks and Outdoors; Retail; Sports and Recreation; Travel and Transportation (https://docs.foursquare.com/developer/docs/pilgrim-categories, undated, VERIFIED-SNIPPET; the older Pilgrim tree, may differ from the current Places taxonomy).
- Noteworthy: "Event" and "Community and Government" are top-level groups, so one-off happenings and public bodies sit in the same tree as shops.

### 8. Facebook Pages and Instagram business profiles
- What it is: social profiles, not a directory, but Pages carry a category and location and are used as business listings.
- Page types: Local Business or Place; Company, Organization or Institution; Brand or Product; Artist, Band or Public Figure; Entertainment; Cause or Community (https://gosmallbiz.com/facebook-business-page-types-explained/). The same results say Facebook now uses a search-based category system with "thousands" of options (UNVERIFIED, no count).
- Categories seen by name in results: Bakery, Cake Shop, Furniture Store (https://socialrails.com/blog/facebook-business-page-categories, UNVERIFIED).
- Organisation: by account topic, with an optional place; no list pages.
- Unique to this platform: people-type categories (public figure, artist, band) and Cause or Community sit next to businesses.

### 9. Tripadvisor
- What it is: travel reviews and booking.
- Top listing types: Hotels, Things to Do (attractions, tours, cruises, classes), Restaurants, Vacation Rentals, plus airlines and flights (https://www.tripadvisor.com/pages/service_en.html). Hotels, restaurants, airlines, landmarks, places of interest and tour operators are listed free of charge; bookable vacation rentals only under a commercial licence; bookable tours and activities only where suppliers contract with Tripadvisor (same page).
- Attraction rules: must be of tourist interest, family-friendly, with official name and permanent address, open to the public on a regular schedule (same page).
- Attraction sub-types seen on listing pages: art galleries, shopping malls, specialty and gift shops, waterfalls, historic walking areas, nature and wildlife areas, spas, universities and schools, historical and heritage tours, art museums, casinos (https://www.tripadvisor.co.uk/Attractions-g43983-Activities-Ripley_Mississippi.html, UNVERIFIED).
- Awards categories (Travellers' Choice Best of the Best): Amusements & Water Parks, Bucket List, Cultural & Historic, Family-Friendly, Food & Drink, Nature & Outdoors, Sailing & Day Cruises, Water Sports (https://tripadvisor.mediaroom.com/Travellers-Choice-Best-of-the-Best-Things-To-Do-2025).
- Scale: 1 billion reviews; several million accommodations, restaurants, experiences, airlines, cruises (https://everythingmoney.com/company-info/TRIP/1/metrics, UNVERIFIED, undated). 1,083,397 European restaurants in a Kaggle dataset (https://baselight.app/u/kaggle/dataset/stefanoleone992_tripadvisor_european_restaurants, historical).
- Notable: inclusion rule "of interest to tourists" means Tripadvisor is deliberately a visitor list, and also hosts a "Cruises" and "Flights" layer.

### 10. Hotfrog, Cylex, Europages
- Hotfrog: 27 country directories (https://uberall.com/en-us/directories/hotfrog) and "38 countries", 69M businesses claim (https://www.yext.com/integrations/publishers/hotfrog); the two figures conflict, both UNVERIFIED. Free listing; category count NOT FOUND.
- Cylex: 78 categories (https://blog.hubspot.de/marketing/branchenverzeichnisse, UNVERIFIED); over 5.1 million entries in Germany (same, UNVERIFIED). Category names seen on town pages: Service & Dienstleistung, Baudienstleistungen, Baumarkte, Haus & Garten, Sport & Freizeit, Restaurant & Cafe (https://web2.cylex.de/zens and similar town pages). Organised by town (Germany) and category.
- Europages: B2B supplier directory with 26 business sectors, 3M+ suppliers, 45 countries (https://globaledge.msu.edu/global-resources/resource/1275 and https://www.fdcapital.co.uk/?p=557, undated, UNVERIFIED). Organised by sector and country; suppliers, not shops.

### 11. Yellow Pages Pakistan and other Pakistani directories
- yellowpages.com.pk: browse by category, search by keyword or city; fields: name, contact name, telephone, website, services, address, city (https://opendata.com.pk/dataset/yellow-pages-of-pakistan; https://apify.com/crawlerbros/yellow-pages-pk-scraper.md). Dataset holds about 67,000 businesses, undated (same opendata link, UNVERIFIED).
- b2c.com.pk: free-to-register directory, "Yellow Pages of Pakistan", search by category, keyword, location (https://medium.com/@b2cbacklinks/b2c-com-pk-8aaf78a85fd7, UNVERIFIED, promotional).
- Category tree of any Pakistani directory: NOT FOUND (gap). Citation-source lists for Pakistan: https://loganix.com/citation-building-lists/pakistan/ and https://www.wmtips.com/technologies/business-listings/country/pk/. The latter claims GBP has 58.6% share of listing platforms in Pakistan in 2026 (UNVERIFIED, odd metric).
- Pakistan-specific vertical finders (Marham, Zameen, Daraz) belong to Groups 4 and 5, not examined here.

---

## 2. Master table of distinct list types seen

Scale: HL = hyper-local (street / neighbourhood), C = city, N = national, G = global. "F/I" = firm or individual. Evidence column is what a source showed; "none" means no paid evidence found.

| List type | Platforms (evidence) | F/I | Natural scale | Paid or free evidence |
|---|---|---|---|---|
| Restaurants, cafes, takeaways (by cuisine) | GBP, Yelp, Justdial, Tripadvisor, Yell, Foursquare (Dining and Drinking), Facebook | F | C | Free listing; paid ads on Yelp/Justdial |
| Bars, nightlife, clubs | Yelp, Foursquare, Tripadvisor | F | C | Yelp ads |
| Hotels, B&Bs, campgrounds, resorts | Tripadvisor, Yelp, Google, Justdial (Hotels) | F | C to G | Tripadvisor listed free; bookings commercial |
| Vacation rentals | Tripadvisor | F or I (hosts) | C to G | Commercial licence only |
| Tours, cruises, activities | Tripadvisor, Yelp (Tours) | F | C to G | Bookable only via contract |
| Attractions, sights, museums, galleries | Tripadvisor, Foursquare, Yelp | F (or public body) | C to G | Free |
| Gas stations | GBP, Yelp (Automotive) | F | HL | GBP shows 195,051 (UNVERIFIED) |
| Car repair, car wash, tyres, towing, car rental | Yelp, GBP, Yellow Pages, Justdial | F | C | Ads |
| Driving schools | Justdial | F | C | Paid tiers |
| Doctors, dentists, hospitals, clinics | GBP, Yelp, Justdial, Yellow Pages | F and I | C | Ads; dentist categories on Justdial |
| Alternative medicine, acupuncture | Yelp | I and F | C | Not shown |
| Pharmacies | GBP (81,108, UNVERIFIED), Justdial (pharmacy supplies) | F | HL | Free |
| Beauty salons, barbers, nail salons, spas | Yelp, GBP, Justdial, Yellow Pages | F and I | HL to C | Ads |
| Gyms, yoga, personal training | Justdial, GBP LSA (Wellness) | F and I | HL | LSA pay-per-lead |
| Schools, universities, coaching, tuition, test prep | GBP, Justdial, Sulekha, Tripadvisor (universities as attractions) | F and I | C | Sulekha leads |
| Tutors and trainers (computer training) | Sulekha, GBP LSA (tutoring) | I and F | C | LSA, Sulekha leads |
| Childcare, preschool | GBP LSA | F and I | HL | LSA |
| Pets: vets, grooming, shelters, shops | Yelp, Justdial, GBP LSA | F | C | Not shown |
| Home services: plumbers, electricians, HVAC, painters, roofers, cleaners, pest control, locksmiths, movers | Yelp, GBP LSA, Sulekha, Justdial | F and I | C | LSA pay-per-lead; Yelp ads |
| Contractors, carpenters, interior decorators, modular kitchens | Sulekha, Justdial, Yelp | F and I | C | Leads |
| Packers and movers, courier | Justdial, Sulekha, GBP LSA | F | C | Paid tiers |
| Lawyers by speciality | GBP LSA, Yelp, Sulekha, Yellow Pages | F and I | C | Highest CPC of any industry (webfx) |
| Accountants, tax specialists, GST, financial planners | GBP LSA, Sulekha, Yelp | F and I | C | LSA |
| Banks, insurance, mortgage lenders | Yelp (Financial Services), Foursquare | F | C | Not shown |
| Real estate agents, brokers | GBP LSA, Sulekha, Justdial | F and I | C | LSA |
| Property rentals, PG/hostels | Sulekha, Justdial | F and I | HL to C | Leads |
| Wedding and event planners, caterers, decorators, photographers | Sulekha, Justdial | F and I | C | Leads |
| Shops: clothing, electronics, books, music, home and garden, antiques, furniture, bakery, cake shops | Yelp, Facebook, GBP | F | HL | Free |
| Cellphone and laptop repair | GBP LSA | F | HL | LSA |
| Storage | GBP LSA | F | C | LSA |
| Flower delivery, laundry pickup, grocery delivery | Justdial | F | C | Not shown |
| Cinemas, music venues, casinos, arcades | Yelp, Tripadvisor | F | C | Not shown |
| Government and community bodies | Foursquare (Community and Government) | F (public) | C to N | Free |
| One-off events | Foursquare (Event) | event, not a firm | HL to C | Not shown |
| Landmarks and outdoors | Foursquare, Tripadvisor | place, not a firm | HL to G | Free |
| Public figures, artists, bands | Facebook | I | N to G | Free |
| Causes and communities | Facebook | group | HL to G | Free |
| Brands and products | Facebook | F | N to G | Free |
| B2B suppliers by sector | Europages (26 sectors), JD Mart | F | N to G | Not shown |
| Local firms by town and trade (Germany) | Cylex | F | HL to C | Not shown |
| Travel-adjacent: flights, airlines | Tripadvisor | F | G | Listed free |
| Editorial "best of" lists | Yelp Top 100 Local Businesses, Tripadvisor Travellers' Choice (https://www.yelp.com/article/top-100-local-businesses-2025) | F | N | Awards, free |

---

## 3. List types here that are NOT in the seed set

Seed-set exclusions as supplied by the founder: petrol pumps, schools, beauty parlours, bakeries, mobile stores, mobile repair, spare parts, furniture, pharmacies, doctors, nurses, lawyers, bookshops, hardware, MRI machines, plumbers, Quran tutors, factories. Reading the instruction as "which of my findings are outside this seed set", the wording is ambiguous; I cover both: (a) evidence for seed items, and (b) types outside it.

(a) Seed items with evidence on these platforms:
- Petrol pumps: GBP "Gas station" 195,051 (https://www.openwebninja.com/blog/top-google-maps-categories, UNVERIFIED); Yelp Automotive "gas stations" (https://business.yelp.com/resources/articles/yelp-category-list/).
- Schools: GBP "school" (https://www.cyberoptik.net/blog/google-business-profile-categories/); Tripadvisor lists universities and schools as attractions.
- Beauty parlours: Yelp hair salons, nail salons, day spas; GBP hairdresser; Justdial Beauty Spa; Yellow Pages Beauty Salons.
- Bakeries: GBP Bakery 101,543 (UNVERIFIED); Facebook Bakery and Cake Shop.
- Mobile stores and mobile repair: GBP LSA "Cellphone and laptop repair" only (https://techwyse.com/?p=51770). No source for mobile stores here.
- Spare parts: Yellow Pages "Automobile Parts" (https://www.localseoguide.com/iyp-seo-rankings-2009-part-ii-which-yellow-pages-sites-should-you-use-for-which-categories/, 2009).
- Furniture: Facebook "Furniture Store" (https://socialrails.com/blog/facebook-business-page-categories).
- Pharmacies: GBP Pharmacy 81,108 (UNVERIFIED); Justdial pharmacy supplies.
- Doctors: Yelp Health & Medical, Justdial Hospitals/Dentists, Yellow Pages Physicians & Surgeons, GBP LSA primary care.
- Nurses: NOT FOUND on any platform here.
- Lawyers: GBP LSA (17+ specialities), Yelp, Sulekha, Yellow Pages Attorneys.
- Bookshops: Yelp Shopping "books".
- Hardware: no direct source here.
- MRI machines: NOT FOUND (equipment lists are a B2B-platform matter).
- Plumbers: GBP LSA, Yelp Home Services (plumbing).
- Quran tutors: NOT FOUND directly; nearest are Sulekha tutors and test-prep, GBP LSA tutoring.
- Factories: NOT FOUND in local directories; closest is Europages B2B suppliers.

(b) List types seen here that are outside the seed set (candidates to add to the catalogue):
1. Hotels, B&Bs, resorts, campgrounds (Tripadvisor, Yelp).
2. Vacation rentals (Tripadvisor) - hosts are often individuals.
3. Tours, cruises, classes and activities (Tripadvisor).
4. Attractions, landmarks, museums, galleries, waterfalls, walking areas (Tripadvisor, Foursquare).
5. Restaurants and cafes by cuisine, and nightlife (all platforms).
6. Cinemas, arcades, casinos, music venues (Yelp, Tripadvisor).
7. Driving schools (Justdial).
8. Packers and movers, courier services (Justdial, Sulekha).
9. Wedding planners, caterers, event organisers, decorators (Sulekha, Justdial).
10. PG/hostels and property rentals (Justdial, Sulekha).
11. Pest control, locksmith, junk removal, solar, tree services, water damage restoration, snow removal, pool cleaning, home inspector, garage door, fencing (GBP LSA).
12. Pet services, grooming, shelters (Yelp, Justdial).
13. Gyms, yoga studios, personal trainers (Justdial, GBP LSA).
14. Domestic workers (Sulekha, https://www.thenewsminute.com/atom/bengaluru-leads-online-searches-domestic-workers-sulekha-unlock-10-128726).
15. Overseas admissions counsellors, GST and tax specialists, graphic designers, interior decorators, modular kitchens (Sulekha).
16. Financial services: banks, insurance, tax, mortgage lenders (Yelp).
17. Government and community bodies, and one-off events (Foursquare top-level groups).
18. Public figures, artists, bands, causes and communities, brands (Facebook).
19. Storage (GBP LSA).
20. Flower delivery, laundry pickup, grocery delivery (Justdial).
21. B2B suppliers by sector (Europages).

---

## 4. Gaps

- Full category trees were not read for any platform; every platform's own page was blocked. A later pass should obtain: Yelp categories.json (via the Fusion Categories API page), Foursquare category CSV, the GBP gcid list, Facebook's category list, and Apple Business Connect categories.
- Counts missing: Justdial categories, Yell headings, Yellow Pages US headings, Bing Places categories, Apple categories, Facebook category count, Hotfrog categories, every Pakistani directory's categories.
- Entry fields unique to a category were not sourced for any platform; only background knowledge exists (flagged above as background).
- Paid categories: only Justdial (tiers vary by category, no list), Google LSA (named verticals) and Yelp CPC (one anecdote) have evidence. No price list by category was found.
- Pakistan: no tree, no counts. The 67,000-business figure and the 58.6% share are undated and weakly sourced. Marham, Zameen and Daraz were not examined here.
- Nurses, MRI machines, hardware stores, Quran tutors and factories had no direct hits in local directories. The Quran-tutor and MRI types are likely to be found on Group 3 and Group 4 platforms.
- Conflicting figures (Sulekha 200 vs 800+ vs about 1,200 categories; Hotfrog 27 vs 38 countries; Yelp 1,500+ vs 22/498/178 hierarchy) are listed side by side; undated, none resolved.
- Which of the seed set items a "not in seed set" test should use: I read the founder's list as the exclusion list; the lead should confirm.
