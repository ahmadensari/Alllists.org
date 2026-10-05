# Name, place-by-place navigation and automatic location

Three owner requests of 2026-10-05, answered in one note. Prototype changes for the second and third are built (`prototype/alllists-prototype.html`: home, place pages, widen steps). Grades: **S** search summary of a source, **M** measured here, **I** my judgement.

Last updated: 2026-10-05.

## 1. The name

### What I could and could not check

- GoDaddy and the registry lookup services are blocked from this environment, so I could not read GoDaddy's availability or prices.
- I used a weaker test: whether a name resolves in the internet's address book (DNS). **TAKEN** means it resolves or has name servers, so it is registered. **free?** means no record was found. A registered name with no records also shows free?, and a free name can still be on sale at a premium price. So every free? must be confirmed on GoDaddy before you rely on it (M, limited).
- Trademarks and social media handles were not searched in registries. A web search found no product named "AllLists" or "All Lists" (S, weak).

### Findings for your four options

| Name | .com | .org | .net | .io | .app | .pk | My view |
|---|---|---|---|---|---|---|---|
| **AllLists** | TAKEN (points to a parking address that looks like a domain for sale) | TAKEN (points to a Google Cloud address; may be yours, please check) | free? | free? | free? | free? | Best meaning of the four: everything, everywhere. Easy to say and write in Urdu. The .com may have to be bought |
| **Listall** | TAKEN | free? | unclear | free? | TAKEN | free? | Same idea, weaker. A product called ListAll may exist (not checked) |
| **Yellow Lists** | free? | free? | free? | free? | free? | free? | Not recommended. It borrows from "Yellow Pages", which is a registered mark in the UK, Canada and Australia though called generic in the US (S). It sounds like the old print directory, and it narrows the idea to business listings |
| **Listings** | TAKEN | TAKEN | TAKEN | TAKEN | TAKEN | TAKEN | Not winnable. A common word, taken everywhere, and impossible to rank for |

### Other names tested (DNS signal only)

| Name | Idea | .com | .org | Note |
|---|---|---|---|---|
| ListAtlas | An atlas of lists; fits the world-to-street drill-down | TAKEN | free? | Also free? on .net, .io, .app, .pk. Pronounceable, easy in Urdu ("ایٹلس") |
| WorldLists | Says the global scope | TAKEN | free? | Descriptive |
| Fehrist | Urdu and Hindi for "list" or "index" (فہرست); the Arabic form is Fihrist, the title of a famous tenth-century catalogue of books | TAKEN | free? | Strong local meaning, harder for English speakers to spell. Fihrist, Fehrist and Fahrist all occur |
| Fehristan | "Land of lists" | free? | free? | Memorable, but "-istan" suggests one region |
| EveryListed | Every business is on a list | free? | free? | Descriptive, longer |
| WorldOfLists | Global | free? | free? | Long |
| ListOsphere, Listaverse | Coined | free? | free? | Needs explaining |
| BazaarLists, MohallaLists | Local flavour | free? | free? | Narrows the idea to markets or neighbourhoods |

### Recommendation

1. **Keep AllLists as the working name.** It says the whole idea in two words, it is easy in English and Urdu, and nothing found conflicts with it (weak evidence).
2. **Secure the domain in this order:** check who owns alllists.org (the repository uses it), then ask GoDaddy for the price of alllists.com through its buy service, then register alllists.app or alllists.io and alllists.pk as protection, and consider alllists.net.
3. **If alllists.com is too dear, the strongest alternative is ListAtlas**, because the world-to-street drill-down is the product. Keep Fehrist (فہرست) as an Urdu brand line, for example "AllLists, فہرست".
4. **Before buying anything:** confirm each free? on GoDaddy, search the Pakistan, US, UK and EU trademark registers, and check @alllists on Facebook, Instagram, X, TikTok, YouTube and LinkedIn. A lawyer's hour on the trademark is worth it.

Open decision Q-S19.

## 2. Navigation: world, then country, then down until the list is reached

The owner's logic: start at the world page, then the country page, then the next, then the next, until the list is reached. This is the place tree already decided (C10), made into pages.

| Level | Example | The page shows |
|---|---|---|
| World | Global | Countries, with counts, and the lists that exist worldwide |
| Country | Pakistan | Regions, and country-wide lists |
| Region | Punjab | Cities |
| City | Sialkot | Areas, and the lists in this city |
| Area | Paris Road | The lists on this road |
| List | Surgical instrument makers in Sialkot | The entries |

Rules:
1. Every level is a page built from the same template. A page shows the places inside it and the lists here, each with a count that rolls up from below.
2. Breadcrumbs let you step back up one level or jump to any ancestor.
3. Addresses follow the tree, for example `/pk/punjab/sialkot/surgical-instrument-makers`, so search engines and people can read them.
4. A list that has no entries yet still exists (C11). It shows the empty state, which is the contributor funnel.
5. You can also reach a list without walking the tree: search, or the near-you shortcut below.

Built in the prototype: home, place pages for world, country, region, city and area, and list pages reached from them, with clickable breadcrumbs.

## 3. Automatic location: lists near you, widen on request

The owner's logic: find where the person is, show lists in their town, city and region first, let them widen the search, let them search country-wide lists whether or not one exists, then apply the payment policy.

### How the place is found

| Method | What it gives | Needs | Notes |
|---|---|---|---|
| Guess from the connection (IP address) at the network edge | Country, usually region and city | Nothing from the user | Cloudflare adds country, city, region and coordinates as request headers; city-level needs a setting turned on (S). A free MaxMind GeoLite2 database also works under its licence, which requires attribution and forbids using it to identify individuals (S). Mobile networks and VPNs often point to the wrong city |
| The browser's location | A precise point | The user's permission | A button, "Use my exact location", never an automatic prompt |
| The user picks a place | Exact | One tap | Always available, and the fallback if the guess is wrong |

The page says plainly what was guessed ("We think you are in Sialkot. This is a guess from your connection and is not stored.") and offers "Change place". The address is not stored. Counsel should confirm the wording for each country, because an IP address can count as personal data.

### Rules that keep pages fast and search-friendly

1. **The address of every list page is the same for everyone.** The page is cached and the same for search engines. Location never changes the content at an address.
2. **The near-you part is separate.** It is a small piece loaded after the page, or added at the edge, so the main page stays cacheable.
3. **No automatic redirect by location.** Offer a banner link instead.
4. **If the guess fails, fall back to the country, then to the world,** never to an empty page.

### The widen steps

Your place, then region, then country, then world. Each step shows its count. The prototype's home page and list page both have the four steps.

### Search and the payment policy

- Searching looks for list types at the current step. If no list matches, the page says so and offers "Start this list", because every list exists everywhere but is empty until someone adds entries.
- Wider than your own place, the working reading of the payment decisions applies: a preview of names is free, and the full list, statistics and enquiry tools are for subscribers. The prototype shows the first five names at country level and a panel naming the full list and count.
- The exact rule (where free ends) is still the open question in the decision log (CP3, CP4).

Open decision Q-S20.
