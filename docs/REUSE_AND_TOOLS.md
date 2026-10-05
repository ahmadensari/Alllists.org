# Open code, data and tools we can reuse

Planning note for the coding phase. No code is written yet. Licence status is graded:

- **Seen** means a search result this session states it. Still check the repository's licence file before use.
- **Memory** means it is from my background knowledge and was not checked this session.

Last updated: 2026-10-05.

## Headline finding

No strong open-source business-directory platform turned up. What the search returned was commercial PHP scripts and WordPress-style plugins (for example Listeo and phpListings, both paid), and one small directory-aggregator project under Apache-2.0. Our data model (place tree, verification levels, per-field provenance, revenue ledger) is specific, so build that core ourselves and reuse components around it.

Two licence rules to keep in mind:
1. **Code licence is not data licence.** Open data has its own terms (OpenStreetMap is share-alike, Overture mostly permissive). Our decision A3 is: code open, list data under terms.
2. **Copyleft code needs care.** GPL and AGPL code can require us to publish our changes if we copy or modify it. Using it as a separate service or database is usually different from copying it into our code. Ask counsel before copying any GPL or AGPL code.

## 1. Data we can load

| Source | What it gives | Licence | Status |
|---|---|---|---|
| Overture Maps places | Tens of millions of places, a schema and a new category taxonomy | Mostly permissive, per-record licence | Seen (see earlier reports) |
| Foursquare Open Source Places | 100 million or more places, 1,000+ categories | Apache 2.0 | Seen (earlier reports) |
| OpenStreetMap | Shops and facilities by volunteers | ODbL, share-alike | Seen (earlier reports); keep as a separate layer |
| Wikidata, GeoNames | Places, institutions, public figures | Open licences | Memory |
| Government registers and open-data portals | Facilities, schools, companies | Differs by body | See `reports/Service provider sources.md` |

## 2. Code and components

| Need | Candidate | Licence | Status | How we would use it | Caution |
|---|---|---|---|---|---|
| Place and category schema | Overture schema (Pydantic models, official GitHub repository) and its categories CSV | Open (check repo) | Seen that the code is on GitHub | Borrow the place structure and taxonomy as a starting point for our concept table | Our own crosswalk still needed |
| Load Overture data | `overturemaps-py`, the official command-line tool | Open (check repo) | Seen | Download by region and convert formats | |
| Duplicate detection | Splink (Ministry of Justice, Python, links tens of millions of records) | Free and open source; exact licence not confirmed | Seen (open source); licence Memory | Core of our merge pipeline | Needs tuning for Urdu and transliteration |
| Duplicate detection (alternatives) | `dedupe`, `recordlinkage` | Memory | Memory | Smaller datasets, easier to learn | |
| Address parsing | libpostal | MIT | Memory | Normalise addresses worldwide | Large model; weak on informal addresses such as "Adyala Road, near X" |
| Geocoding | Pelias | MIT | Seen | Self-hosted address search | Heavy to run; start with a hosted service if terms allow |
| Geocoding | Photon | Apache 2.0 | Seen | Lighter geocoder on OpenStreetMap data | |
| Geocoding | Nominatim | GPL | Memory | OpenStreetMap's own geocoder | Check GPL fit |
| Geocoding | Mimirsbrunn | AGPL-3.0 | Seen | Avoid for now | AGPL |
| Database and maps | PostgreSQL, PostGIS | PostgreSQL licence, GPL | Memory | Our core store | |
| Hex-grid areas | H3 | Apache 2.0 | Memory | Optional area roll-ups | |
| Backend framework | Django (admin, auth, migrations) | BSD | Memory | Back office and moderation screens almost free | Decision pending (Q-S9) |
| Backend framework (alternatives) | Flask or FastAPI | BSD, MIT | Memory | The draft we already prepared | |
| Login | django-allauth | MIT | Memory | Social sign-in including ORCID | |
| Search | Postgres full text first. Later Meilisearch (MIT, with some BUSL-licensed parts), Typesense (GPL-3) or OpenSearch (Apache 2.0) | As stated | Seen | Add only after a measured limit | Check which parts of Meilisearch are BUSL |
| Money ledger | Formance Ledger (programmable double-entry, MIT) | MIT | Seen | Could run as a separate ledger service | Adds a service to operate; a simple Postgres ledger may be enough early |
| Money ledger | TigerBeetle (open-source financial transactions database) | Open | Seen | Only if volume demands it | Overkill early |
| Money ledger | django-ledger (double-entry accounting for Django) | Not stated | Seen (existence); licence unknown | Reference for ledger design | Built for bookkeeping, not per-sale revenue sharing |
| Marketplace parts (vendors, commissions, payouts) | Saleor (BSD-3, Python), Medusa (MIT, TypeScript), Mercur (marketplace on Medusa, MIT core with separately licensed enterprise modules) | As stated | Seen | Study how they model vendors, commissions and payouts | We sell data access, not goods; do not adopt a whole shop platform |
| Support and messaging inbox | Chatwoot (MIT; handles WhatsApp Business API, email, SMS) | MIT | Seen | Reply inbox for outreach responses | Needs official WhatsApp Business API access |
| Email campaigns | listmonk (AGPL-3.0, Go, single binary with Postgres) | AGPL-3.0 | Seen | Run as a separate service for email outreach | AGPL; do not copy its code into ours |
| Front end | Next.js or Astro, Tailwind | MIT | Memory | Server-rendered, search-friendly pages | |
| Content pages | Wagtail (BSD, Django) | Memory | Memory | If we want an editorial layer | |
| Security scanning | Dependabot, secret scanning (GitHub), OWASP guides | | Memory | Free checks in CI | |

## 3. Things to avoid

- Unofficial WhatsApp libraries that mimic WhatsApp Web. They break WhatsApp's terms and can get numbers banned. Use the official Business API through a provider (Memory).
- Copying code from commercial directory scripts or marketplaces with unclear licences.
- Copying GPL or AGPL code into our repository before counsel agrees.
- Scraped Google Maps, Facebook or Baidu data, already classed red in `reports/AI agent populated lists.md`.

## 4. What the tools in this session can do for us

| Capability | Use |
|---|---|
| Subagents (parallel researchers and writers) | Research rounds like the ones already done; later code review and test writing |
| Workflow tool | Large multi-agent jobs. It only runs when the owner asks for it in their own words, for example "use a workflow" |
| Web search | Verify licences and facts; limited by the search allowance per agent and blocked from many official sites |
| GitHub tools | Read and write this repository, pull requests and checks. More repositories can be attached to a session with `add_repo`, then cloned to read or study |
| Skills | `security-review`, `code-review`, `simplify` for the coding phase; `deep-research` for research; `docx`, `pdf`, `xlsx`, `pptx` for files; `session-start-hook` to prepare test and lint runs; `skill-creator` to package our own repeatable steps |
| Documents, artifacts and mind maps | Share reports and pages privately; a mind map of the place tree and list families could help the founder see the structure |
| Scheduled routines | Recurring checks, such as re-running source checks or watching a pull request |

Limits: the network proxy blocks many official sites, so facts from them cannot be read directly; no production hosting is available from here; GitHub access is limited to the attached repository plus any added with `add_repo`.

## 5. Suggested next steps (research only, until the owner asks for code)

1. Attach and read the repositories for Overture schema, Splink and one marketplace platform (Saleor or Medusa) to confirm licences and see what is reusable.
2. Confirm each shortlisted licence from its repository file.
3. Decide the stack (Q-S9) before choosing among the alternatives above.
