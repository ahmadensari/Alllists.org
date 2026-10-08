# 02. Security, anti-scraping, anti-cloning, social linkage, bulk upload

Status legend: BUILT (in code, seen in repo), PARTIAL, NOT BUILT, PLAN (specified in docs/TECHNICAL_PLAN.md only). Priority: P0 before public launch, P1 before paid data or first bulk partner, P2 later.
Web claims marked UNVERIFIED were taken from search snippets or vendor blogs and need counsel or primary-source checking. Dated 2026-10-06.

Repo note: the brief named `backend/core/throttle.py`; it does not exist. Login throttling is `backend/accounts/throttle.py`, quotas and abuse counters are `backend/access/quotas.py`.

## 1. What the repo already has (evidence)

- Login throttle by account (5) and address (20) in 15 min, hashed keys: `backend/accounts/throttle.py`. Address comes from `CF-Connecting-IP` with no check that the request came through Cloudflare (spoofable if origin is reachable directly).
- Quota counters in DB, free names per day (100 account, 40 anon), alarm at 500 fragments/day, hard cap 2000: `backend/access/quotas.py`. Runbook `docs/runbooks/scraper-surge.md`.
- Extracts: staff-made, planted trace entries, `identify_leak`: `backend/analytics/extracts.py`. No user export route (rule R13).
- Canary entries exist for verifier testing: `backend/volunteers/models.py` (CanaryEntry). The plan wants scrape-trace canaries in each large list on the public site too (section 9.3, T1.03, `canary_seeder`): not seen for public pages.
- Security headers and CSP, Permissions-Policy, COOP, default `private, no-store`: `backend/core/middleware.py`. HSTS 30 days, no subdomains, no preload: `backend/config/settings/prod.py`.
- Crypto: encrypted fields, keyed hash, key re-encryption; log scrubber: `backend/core/crypto.py`, `logscrub.py`. DB roles: `dbroles.py`.
- Accounts: TOTP (`accounts/totp.py`), recovery codes, social identities (`accounts/social.py`), optional two-step for all.
- Share channels registry: `backend/catalog/share.py`. No Open Graph or Twitter card tags found in templates or code by grep (needs a template check).
- Fetcher for agents: honest UA, robots respected, SSRF and DNS-rebinding pin, 500 KB and 10 s caps, 2 s per-site interval, stop on first refusal: `backend/agents/fetcher.py`.
- Source gate: red sources blocked, `allowed_uses`, amber needs terms review: `backend/intake/gate.py`.
- Intake: paste/CSV import with declared-rights flag, column mapping (English, Urdu, Roman Urdu), draft entries, duplicate settle, `ImportBatch` and `ImportRow` statuses, audit row per run; dedupe by trigrams, distance and features; open-data loaders with `ExternalRecord` checkpoint: `backend/intake/*`. Whole upload is held in one `raw_text` field and processed in one synchronous function.
- Moderation: reports, suggested edits, `Takedown` with legal basis and due date, erasure, subject access report, consent withdrawal and register: `backend/moderation/*`.
- CI: flake8, bandit, pip-audit in `.github/workflows/python-package.yml`. No `.github/dependabot.yml`. No CodeQL or ZAP seen.
- Runbooks: breach-response, secret-rotation, takedown-request, scraper-surge, restore, deploy-rollback.

## 2. Anti-scraping requirements

| ID | Requirement | Pri | Status | Notes |
|---|---|---|---|---|
| AS-01 | Per-address and per-account daily quotas on detail data, with hard cap and alarm | P0 | BUILT | quotas.py. Add per-minute burst limit; today only daily |
| AS-02 | Edge rate limiting (Cloudflare rules) by path class: list pages, `/_f/` fragments, search, login, forms | P0 | PLAN | Plan 9.3; no config in repo. Keep rules as code (Terraform or documented export) |
| AS-03 | Trust `CF-Connecting-IP` only when the peer is a Cloudflare range or a tunnel/authenticated origin pull | P0 | NOT BUILT | Otherwise quota and throttle keys are forgeable |
| AS-04 | Valuable details served only in private fragments, never in the cached public page | P0 | BUILT (design, R-rules) | Keep a regression test that the public HTML has no contact values |
| AS-05 | Same content to bots and humans for indexable pages (no cloaking) | P0 | PLAN | Decision P5 in plan |
| AS-06 | Bot detection signals: header sanity, no-JS fragment calls without prior page load, known cloud ASNs, request pacing, sequential ID walking | P1 | NOT BUILT | Runbook step 4 expects this analysis by log reading only |
| AS-07 | Challenge (Cloudflare Turnstile, managed mode) on signup, login after failures, contact reveal, report and enquiry forms; not on indexable pages | P1 | NOT BUILT | Decision M4 says CAPTCHA only if abuse appears. Turnstile free reported as unlimited, but free plan lacks per-endpoint policies; one review reports about 33 percent detection (UNVERIFIED) so it is a speed bump, not the defence |
| AS-08 | Honeypot form fields and honeypot links/pages disallowed in robots.txt, hits logged and blocked | P1 | NOT BUILT | Cheap; pairs with AS-09 |
| AS-09 | Trace records: planted fake entries in each large list, per-viewer or per-tier variants where cheap, monitored by `canary_seeder` | P1 | PARTIAL | Extracts have it; public lists do not. Must not be indexable or shown in counts that mislead users; fake phone numbers on reserved test ranges you control, fake business names never real |
| AS-10 | Account-level abuse: new accounts get lower quota; velocity limits on signups per address; disposable email block; link accounts via device hash | P1 | NOT BUILT | Runbook says "look for how accounts were created" with no tooling |
| AS-11 | Graduated response: warn, slow (429 with Retry-After), challenge, block, suspend; every step audited | P1 | PARTIAL | 429 and alarm exist; no slow or challenge tier |
| AS-12 | Terms of use ban automated collection, bulk copying, resale, building competing datasets; state permitted use and licence | P0 | PLAN | Needs counsel. Public logged-out scraping is hard to enforce by contract: Meta v. Bright Data (N.D. Cal.) held ToS governed logged-in "use" only; hiQ v. LinkedIn narrowed CFAA for public pages (both via law-firm summaries, UNVERIFIED, US only). Conclusion: rely on technical controls, logged-in terms (accept at signup), and copyright/database rights, not on CFAA |
| AS-13 | robots.txt and ai.txt style signals: disallow `/_f/`, search, admin; state AI-training policy; honest crawler allow-list (verified Googlebot via reverse DNS) | P1 | PARTIAL | robots rules planned P2.15; AI-crawler policy is an open decision |
| AS-14 | Scraper surge alarm to on-call, auto-block rule suggestions | P1 | PARTIAL | Alarm audit row exists; paging and auto-action not seen |
| AS-15 | Sitemap and publish throttle so a bug or an attacker cannot expose a million pages | P1 | PLAN | `publish_cap_per_week` |

## 3. Anti-cloning requirements

| ID | Requirement | Pri | Status | Notes |
|---|---|---|---|---|
| AC-01 | Canary entries in every list over N rows (name, phone, address unique and registered), with a detector job (search engines, known clone sites, paid-data buyers) | P1 | PARTIAL | See AS-09 |
| AC-02 | Extract watermarking: planted trace entries, per-buyer seed, leak identification | P1 | BUILT | extracts.py; add subtle per-buyer variations (casing, whitespace, field order) as second layer. UNVERIFIED effectiveness against dedupe by cleaners |
| AC-03 | Extract and API licence: per-buyer contract, no resale, audit right, deletion on termination, watermark disclosure policy | P1 | PLAN | Counsel |
| AC-04 | Keyed read API only later, with keys, quotas, watermarking | P2 | PLAN | R31: none at launch |
| AC-05 | Takedown and DMCA-style procedure for AllLists' own content found on clone sites: evidence pack (canary hit, capture, hash), host/registrar/CDN abuse contacts, search engine removal forms | P1 | NOT BUILT | Existing `Takedown` and runbook handle incoming requests about listed entries, not outgoing enforcement. Need a separate outgoing runbook |
| AC-06 | Incoming DMCA and local-law notices (agent registration with US Copyright Office if US users can contribute; counter-notice flow) | P1 | NOT BUILT | Check whether registration is needed given text-only user content. Open decision |
| AC-07 | Copyright and database-right position: facts are weakly protected in US (Feist); EU sui generis database right and UK may help; selection/arrangement and added scores may be protectable | P0 | NOT BUILT | Counsel memo. Affects whether to rely on law at all |
| AC-08 | Own licence per record stored (source, licence, date) so AllLists never claims rights it lacks over open data (Overture, Foursquare, registers) | P0 | BUILT | `Source`, `entry_value_meta` |
| AC-09 | Competitor practice review kept current | P2 | this file | See below |

How comparable sites protect data (all from search snippets, UNVERIFIED, re-check before citing):
- Yelp: terms forbid scraping and data mining; offers a rate-limited Fusion API (about 5,000 calls/day default) and display and storage restrictions; IP bans.
- ZoomInfo: terms forbid unauthorised scraping; CAPTCHAs, IP rate limiting, fingerprinting and behaviour analysis reported; data sold through licensed API and credits; contact data hidden behind paid login. Known to seed trace records (common industry practice among list vendors, UNVERIFIED for ZoomInfo specifically).
- Crunchbase: search results had no confirmed terms text; commonly known to sell API and bulk licences and hide fields behind tiers. UNVERIFIED.
- ThomasNet and Justdial: no usable search results; treat as UNVERIFIED. Pattern to confirm: contact details behind a click or login, paid listing tiers, ToS bans, legal letters. Justdial has litigated against copiers in India (UNVERIFIED, check).
- Common pattern across all: free tier shows little, depth is behind login and quota, contract plus technical limits plus occasional litigation. This matches AllLists plan 9.3.

## 4. Cyber security requirements

| ID | Requirement | Pri | Status | Notes |
|---|---|---|---|---|
| CS-01 | Adopt OWASP ASVS 5.0 (released May 2025, 17 chapters, about 350 requirements; UNVERIFIED count) at L1 for launch and L2 for payment, payout, staff and contact-data areas; keep a checklist mapping each requirement to a test or "not applicable" | P0 | NOT BUILT | Plan lists OWASP risks but no ASVS mapping. Note plan risk table may reference Top 10 only |
| CS-02 | Route-inventory test: every route has a declared access level | P0 | PLAN | Plan section 20 |
| CS-03 | Secrets: none in repo, secret scan with push protection, rotation runbook, key versioning, separate keys per environment | P0 | PARTIAL | Runbook, key re-encryption and GitHub push protection exist; add pre-commit and CI secret scan (gitleaks) so it does not depend on GitHub settings |
| CS-04 | WAF in front: Cloudflare managed rules, OWASP core rule set, origin locked to Cloudflare (tunnel or authenticated origin pulls), no public origin IP | P0 | PLAN | Ties to AS-03 |
| CS-05 | DDoS: Cloudflare proxy, cache on public pages, rate rules, origin autoscale or cap, "under attack" playbook | P0 | PLAN | No runbook found for DDoS (scraper-surge is the nearest). Add one |
| CS-06 | Dependency scanning: pip-audit in CI, Dependabot (pip, GitHub Actions, npm if any), pinned actions, SBOM | P0 | PARTIAL | pip-audit and bandit built; Dependabot file missing; `setup-python@v3` flagged by plan as outdated |
| CS-07 | SAST and DAST: bandit (built), CodeQL or semgrep, ZAP baseline scan against staging each release | P1 | PARTIAL | |
| CS-08 | Pen-test: external test before taking payments or releasing contact data; retest after fixes; annual after | P1 | NOT BUILT | Budget decision |
| CS-09 | Vulnerability disclosure policy: `/.well-known/security.txt`, safe-harbour text, triage SLA; bug bounty later | P1 | NOT BUILT | |
| CS-10 | Breach response: runbook, 72 h GDPR authority notice, PDPL/other country rules, user notice, evidence handling, contacts list, tabletop drill twice a year | P0 | PARTIAL | `docs/runbooks/breach-response.md` exists; per-country notice duties and drill not evidenced |
| CS-11 | Account takeover: Argon2id, throttle (built), staff TOTP (built), optional MFA for all (built), passkeys later, new-device email, session revocation on password change, breached-password check (k-anonymity HIBP), credential-stuffing detection by many accounts per address | P0 | PARTIAL | Add breached-password check and new-device alerts; Turnstile after failures |
| CS-12 | Payment fraud: hosted payment page (no card data), manual confirmation first, refund hold, velocity limits, 3-D Secure, chargeback evidence log, payout two-person rule, payout destination change cooldown | P0 | PLAN | P3.09 and payout rules in plan; verify in code before first money |
| CS-13 | Security headers: CSP enforced (built, check Report-Only flag off in prod), HSTS raise to 1 year and consider preload after stable, secure and HttpOnly SameSite cookies, referrer policy | P0 | PARTIAL | HSTS 30 days now |
| CS-14 | Logging and detection: audit log hash-chained, log scrub, alerts for admin login, mass export, role grants, quota alarms; log retention policy | P1 | PARTIAL | |
| CS-15 | Backup and restore tested, encrypted, offsite; restore drill | P0 | PARTIAL | Runbook exists; drill evidence unknown |
| CS-16 | Upload hardening: the only file ingest is CSV/paste; size, row, encoding, CSV-injection (prefix `=+-@` on any export), zip-bomb and formula safety | P0 | PARTIAL | Text-only rule R01 helps; CSV formula escaping in exports not verified |
| CS-17 | SSRF and fetch safety for agents | P0 | BUILT | fetcher.py |
| CS-18 | Admin hardening: unguessable path, MFA, optional IP allow-list, separate admin session lifetime | P1 | PLAN | |

## 5. Social media linkage

| ID | Requirement | Pri | Status | Notes |
|---|---|---|---|---|
| SM-01 | OAuth/OIDC sign-in (Google first, ORCID for researchers), PKCE, state and nonce checks, verified-email-only account linking (no auto-merge on unverified email), minimal scopes (openid, email, profile) | P1 | PARTIAL | `accounts/social.py` and SocialIdentity exist; audit linking rules and tests |
| SM-02 | Account linking and unlinking with at least one other login method retained | P1 | BUILT (appears) | views.py around line 310 |
| SM-03 | No posting to user social accounts, no friend graph import, no tracking pixels; share = plain links | P0 | BUILT (share.py is link registry) | Keeps privacy page short and CSP clean |
| SM-04 | Open Graph and Twitter card tags on list and entry pages (title, description, canonical URL; no remote images because CSP and R01) or one generated text-card image served from own domain | P1 | NOT BUILT (not found) | Open decision: allow one first-party generated preview image despite R01 |
| SM-05 | WhatsApp, Facebook, X, LinkedIn, Telegram, Copy link, native share; per-country hide rules | P1 | BUILT | share.py |
| SM-06 | Privacy: share links must not carry personal data or tokens in URLs; sign-in provider list and data stored disclosed in privacy notice; social-login-only users can delete account | P0 | PARTIAL | |
| SM-07 | Business social links as entry fields (website, Facebook page, Instagram) stored as plain URLs with rel nofollow ugc, no fetch of profiles | P2 | NOT BUILT | Scraping Facebook/Instagram is red tier (R22) |
| SM-08 | Platform terms for login buttons (Google, Facebook brand rules); app verification for Google OAuth consent screen | P1 | NOT BUILT | Takes weeks; start early |

## 6. Bulk upload of very large lists (for example a company uploads 10 million user records)

Principle: a bulk upload is a partner data deal, not a form. Default posture: accept business facts (company name, address, category, business phone), refuse or hold anything that identifies a private person. Personal contacts are never published (R-rules and D-decisions on named individuals: consent only, contact through platform).

Current gap: `run_import` is synchronous, reads the whole file from a text field, creates every row in one request, has no staging, no rollback, no per-batch quarantine, no accuracy score. Plan says 5,000 rows/s for loaders and a 100 million job would take about 83 hours as batches (plan section 7).

| ID | Requirement | Pri | Status | Notes |
|---|---|---|---|---|
| BU-01 | Separate "partner bulk" path from paste import: contract record, named controller, data protection agreement, lawful basis recorded per batch, approval by staff before any load | P0 | NOT BUILT | `declared_rights` boolean only |
| BU-02 | Upload by signed object-storage link (resumable, checksum), not through Django; limits per account; virus/format scan; never a request-time import | P0 | NOT BUILT | Today `raw_text` TextField |
| BU-03 | Streamed, chunked parse (for example 5,000 rows per transaction) with checkpoint, resume and idempotency key per row (like `ExternalRecord`) | P0 | PARTIAL | Checkpoint pattern exists for open-data loaders only |
| BU-04 | Schema validation per field: phone (E.164 with country), email syntax and MX check on sample, URL, coordinates in country, address plausibility, encoding, field length, forbidden fields | P0 | PARTIAL | `normalise_row` does basic normalising |
| BU-05 | Personal-data classifier: detect personal emails (gmail etc.), mobile numbers of individuals, ID numbers (CNIC, SSN, Aadhaar), date of birth, home addresses, names with no business markers; those rows go to quarantine, not to drafts | P0 | NOT BUILT | Core of "no publication of personal contacts" |
| BU-06 | Publication rule enforced in code, not policy: imported rows are `draft`, and personal-class contact values are stored encrypted, flagged `no_publish`, never shown, never in extracts. Add a test | P0 | PARTIAL | Drafts earn nothing (R08, R09); no_publish flag not seen |
| BU-07 | Deduplication: within file (exact on normalised phone, domain, name+place), against existing entries (trigram + distance, existing `dedupe.py`), blocking keys so 10M x existing is not quadratic; auto-merge only above high threshold, rest to review sample | P0 | PARTIAL | dedupe.py is per entry, `candidates_for`; needs set-based blocking at scale |
| BU-08 | Accuracy scoring per row and per batch: field completeness, validity, checks passed, duplicate rate, match to independent source, bounce/disconnect rate on a sampled live check; batch gets grade A to D and gate thresholds | P1 | NOT BUILT | Feeds trust labels |
| BU-09 | Sampling audit: random sample (plan uses 385 per batch for 95 percent confidence, 5 percent margin, which holds for large N) verified by surveyors or automated checks; stratify by region and category; reject batch if error above threshold (set, for example, 10 percent) | P1 | PLAN | T1.03 sampler is planned; not applied to imports |
| BU-10 | Consent and lawful basis register per batch: basis (consent, contract, legitimate interest with LIA, public task), evidence, source of data, date, retention, Art. 14 notice plan (notify data subjects within one month where required; may be impossible for 10M so an exemption analysis or notice via supplier is needed) | P0 | PARTIAL | consent register exists per entry (`moderation/privacy.py`); batch-level basis not seen |
| BU-11 | Country rules: GDPR/UK GDPR, Pakistan PECA and draft data law, India DPDP Act 2023, UAE PDPL, CAN-SPAM/TCPA for any outreach built on the data. Each country switch default off until counsel signs | P0 | PLAN | Plan section on compliance; see 16 `country_switch` |
| BU-12 | Staged import: stage table (never public tables) then quarantine, then drafts, then verification queue, then publish; each stage gate has counts and a staff sign-off; publish cap per week | P0 | NOT BUILT | |
| BU-13 | Rollback: every row carries `batch_id`; one command removes or soft-deletes everything from a batch (entries, contacts, search index, cache purge, sitemaps), including merges made into existing entries (keep a merge log so original values can be restored) | P0 | NOT BUILT | `ImportRow.entry` link exists; merges are not reversible today |
| BU-14 | Quarantine: rows failing validation, personal class, suspected fake or honeypot, red-source marker, or abusive; encrypted, retention limit (for example 30 days), reviewed by staff, then purged | P0 | PARTIAL | `ImportRow.Status.HELD` exists, no UI or retention |
| BU-15 | Uploader abuse checks: seeded fake rows from AllLists in test files, flag batches that contain other platforms' trace records (cloned data), reputation of uploader, per-uploader size cap until trusted | P1 | NOT BUILT | Prevents laundering stolen databases into the platform |
| BU-16 | Provenance and licence per row (`source`, licence, date, consent status) and uploader warranty and indemnity clause | P0 | PARTIAL | Source model complete; contract text missing |
| BU-17 | Resource limits: background worker, queue priority below user traffic, DB write rate cap, no table locks, index maintenance plan, storage estimate (10M rows x several fields; confirm sizing) | P0 | NOT BUILT | |
| BU-18 | Reporting back to uploader: counts, rejected rows file, duplicates, quarantined count, no personal data echoed in logs | P1 | PARTIAL | `counts` JSON only |
| BU-19 | Deletion on request and on contract end; per-subject erasure traces back to batch | P1 | PARTIAL | `execute_erasure` exists; batch trace partial |
| BU-20 | Audit log row per stage, actor, counts; log scrub on any row dumps | P0 | PARTIAL | `import.run` audited once |

## 7. Suggested build order

1. P0 quick wins: AS-03 origin trust, CS-06 Dependabot file, CS-13 HSTS plan, CS-01 ASVS checklist, CS-09 security.txt, CS-05 DDoS runbook.
2. P0 for any bulk partner: BU-01, 02, 03, 05, 06, 12, 13, 14, 17 (design as one "bulk pipeline" epic, about the size of plan item P1.16).
3. P1 before paid extracts: AS-06 to AS-10, AC-01, AC-05, CS-07, CS-08, SM-04.

## 8. Open decisions for the founder (with default)

1. Bulk partner policy: business facts only, personal rows quarantined or refused (default yes).
2. Largest batch accepted without counsel review (default 100,000 rows; above needs signed DPA and sample audit).
3. Accuracy gate: minimum grade and error rate to publish (default sample error at most 10 percent, duplicates auto-merged at 0.9 score).
4. Turnstile now or only on abuse (plan M4 says only on abuse; recommend on signup and contact reveal from launch).
5. Allow one first-party generated Open Graph image despite no-media rule R01 (default no image, text tags only).
6. AI-crawler stance in robots.txt and terms (allow search, disallow training crawlers; counsel).
7. DMCA agent registration and outgoing enforcement budget (default: register only if US contributors; counsel).
8. Pen-test timing and budget (default before first payment).
9. Retention of quarantined and rejected rows (default 30 days).
10. Whether to mark scrape-trace canaries on public pages given risk of misleading users (default yes, fake businesses only in clearly non-user-facing indexes plus `noindex`-safe variants; counsel).
11. Counsel: does GDPR Art. 14 notice duty apply to a partner's 10M records, and who is controller (AllLists vs uploader).

## Sources (web, all standard search, treat as UNVERIFIED until read in full)
- Cloudflare Turnstile vs reCAPTCHA reviews: phpcaptcha.org, prosopo.io, pkgpulse.com, developers.cloudflare.com
- OWASP ASVS 5.0: softwaremill.com/whats-new-in-asvs-5-0, appknox.com, securitycompass.com
- Scraping law: fbm.com (hiQ v. LinkedIn; Meta v. Bright Data), fenwick.com, zyte.com
- Competitor protections: webscraping.ai FAQ pages on Yelp and ZoomInfo (low quality source)
- GDPR Art. 14: gdprlocal.com, legiscope.com, sota.io
