# Trust, money and legal solutions: concrete designs for challenges C43 to C47, C50, C51, C53, C55

Research date: 2026-10-06. Scope: English only. Design only; no code was changed and nothing was committed. Not legal or tax advice: every legal and tax item below needs counsel or a local accountant before it drives a decision.

Reads: `research_notes/Scale research/03_capabilities_and_skills_matrix.md` (challenges C39 to C55), all four notes in `research_notes/Platform requirements/`, `docs/DECISIONS.md`, and the code in `backend/billing/`, `backend/ledger/`, `backend/accounts/`, `backend/moderation/` (plus the models they touch in `entries`, `outreach`, `intake`, `volunteers`, `core`, `analytics`, and `scripts/backup.sh`).

Evidence tags (same as the matrix):

- **[R]** read in this repository, or read in a package file I downloaded and unpacked this session (PyPI wheels, see section 1).
- **[S]** web search summary. I did not open the page. UNVERIFIED until a person opens the source.
- **[K]** my background knowledge. UNVERIFIED.
- **[I]** inference or arithmetic (inputs stated).
- **[H]** proposal or hypothesis: a design choice or threshold that has not been tested.

---

## 0. Summary

1. **Shape.** Nine challenges, one spine. Every adverse decision (hold a listing, reject a claim, remove a review, freeze a payout, suspend an account) writes one `EnforcementAction` row with a reason code and a statement of reasons (C50). C43, C44, C45, C46 and C47 are detectors that feed that spine. C51 and C53 change `billing` and `ledger`. C55 is a procedure plus a registry of every derived copy of an entry. Two new Django apps are proposed: `trust` and `compliance`. Nothing already built is replaced.
2. **Biggest findings in the repo [R].** (a) `execute_erasure` wipes contacts, socials and name variants but leaves services, products, branches, identifiers, hours and the evidence text on checks, claims and reports; it does not touch the staged import text (`ImportBatch.raw_text`, `ImportRow.raw`), agent drafts, enquiry text, extract files or the CDN. (b) Backups keep up to 56 days (14 daily plus 8 weekly) and nothing re-applies erasures after a restore. (c) Order tax is looked up by the country of the list (`scope_path`), not the buyer's country, and has one flat rate per country, so reverse charge, OSS and a Gulf buyer buying a Pakistan list are all wrong today. (d) A payment must equal the order amount, so a customer who withholds tax and pays net (normal in Pakistan) cannot be recorded. (e) The refund hold is 14 days (`REFUND_HOLD_DAYS`) but a card chargeback window is about 120 days [S]; a refund after payout drives the contributor's payable balance negative with no explicit clawback record or test. (f) The payment webhook ignores every status except "succeeded", so refunds and disputes from a gateway are invisible.
3. **Licences (verified from the published wheels, not from GitHub).** python-stdnum 2.2: LGPL-2.1-or-later. rapidfuzz 3.14.6: MIT. Splink 5.0.0: MIT. datasketch 2.0.0: MIT (needs numpy and scipy). networkx 3.6.1: BSD-3-Clause. phonenumbers 9.0.40: Apache-2.0. django-axes 8.3.1: MIT. nomenklatura 4.17.0: MIT. The GitHub tool refused every third-party repository ("not configured for this session"), so no repository LICENSE file was read; the wheel metadata and bundled licence files were read instead. OpenSanctions data is CC BY-NC 4.0 and needs a paid licence for business use [S]; its engine yente is MIT [S].
4. **python-stdnum coverage, checked in the wheel [R].** Pakistan: CNIC only (no NTN, STRN or SECP number). UAE: nothing (no TRN, no trade licence). India: GSTIN, PAN, Aadhaar, EPIC, VID (no CIN, no TAN). UK: VAT, UTR, NHS and others (no Companies House number). EU: VAT (online VIES check needs the `zeep` extra), OSS. US: EIN, ITIN, SSN, TIN. Also `iban` (Pakistan 24 characters, UAE 23) and `lei`. We must write small format checks for SECP CUIN, NTN, STRN and UAE TRN ourselves.
5. **Merchant of record (MoR) versus own tax handling.** Decision table in section 12.3. Short version: keep Pakistan domestic sales on own handling; until a MoR is chosen, sell outside Pakistan to businesses only, by invoice and bank transfer, with a validated tax id and the reverse-charge legend; put card and subscription sales to the UK, EU, India and the US on a MoR before the first such sale. MoR fees are about 4 to 5 percent plus 40 to 50 US cents per order [S]. Check each MoR's acceptable-use policy in writing: Paddle's policy reportedly excludes advertising and sponsorship products [S], which overlaps our paid ranking and ad products, and I found nothing either way on data lists.
6. **Sanctions.** Use the free government lists (OFAC SDN, UN consolidated, UK, EU, Pakistan proscribed persons, UAE Local Terrorist List) fetched daily into our own table and matched with rapidfuzz, with a human review queue. Cost: USD 0 in licences. Paid OpenSanctions or a vendor only if PEP screening or volume demands it. Screening is a payout and paid-product gate, not an entry filter.
7. **Erasure and backups.** Section 14.3 is the procedure. Live systems within 24 hours; derived copies tracked step by step; backups kept at most 35 days (change from 56) and never restored without replaying an erasure log (hash only). Stated promise to the person: erased data may stay in encrypted backups for up to 35 days, is never used, and is deleted on schedule. This follows the ICO "beyond use" test [S].
8. **Pilot minimum (section 15).** Pilot = Pakistan, one city, one trade, manual bank transfer and Raast. Build: reason codes and enforcement log, registry-number format checks, manual registry check queue, sanctions table and screening gate on payouts, signup velocity and Turnstile, erasure step table with 35-day backups and restore replay, tax decision function with B2B-only outside Pakistan, withholding-aware payment, clawback and dispute records. Defer: reviews (do not launch ratings in the pilot), vendor KYB, graph analytics, MoR integration, automatic rails.
9. **Pakistan tax is unsettled.** The 5 percent Digital Presence Proceeds Tax on foreign suppliers was switched off from 1 July 2025 by SRO 1366(I)/2025 [S]. The Finance Act 2026 (enacted 27 June 2026, mostly from 1 July 2026) added a 5 percent withholding on social-media creator earnings and, in proposals, a 5 percent digital tax on foreign vendors [S, conflicting]. Provincial sales tax on services runs 13 to 16 percent, Punjab 16 percent, reduced 5 percent for IT services [S]. The operating-entity location decision comes before every tax decision here.
10. **Counts.** New tables: 35 across `trust`, `compliance`, `billing`, `ledger` (sections 6 to 14), plus added fields on `Order`, `Payment`, `Invoice`, `Sale`, `Payout`, `PayoutProfile`. New routes and commands: about 43. Acceptance tests named: 157. Open decisions for the founder with defaults: section 18.

---

## 1. Method, grades and what I could not verify

| Item | What happened |
|---|---|
| GitHub tool | Refused for `arthurdejong/python-stdnum` ("repository not configured for this session"; only this repository is allowed). I did not call `add_repo` because the task did not ask for repositories to be added. So **no repository LICENSE file on GitHub was read**. |
| Package files | `pip download --no-deps` of eight packages into a scratch directory, unzipped each wheel in its own directory, read `METADATA`, `Requires-Dist` and the bundled licence files, and listed `stdnum/` modules. Nothing was imported or run. A licence in a wheel is what the maintainers ship; the repository could differ (grade [R] for wheel facts). |
| WebFetch | Blocked by the network proxy for paddle.com, opensanctions.org and regfollower.com. Everything from the web below is therefore a standard-mode search summary, grade [S], UNVERIFIED. |
| Conflicts | Pakistan digital taxes (section 5.2) and Paddle's acceptable-use scope are reported differently by different sources. Marked where they occur. |
| Not checked at all | Pakistan NTN and STRN exact formats; UAE trade licence number formats by emirate; Indian CIN lookup access; whether EU DSA article 30 applies to a B2B directory; Pakistani withholding on contributor payouts; EU DAC7 reporting for contributors. All need an adviser. |

---

## 2. Starting position and scale arithmetic

### 2.1 What exists today, by challenge [R]

| Challenge | Built | Not built |
|---|---|---|
| C43 fake suppliers | `Report.Kind.FAKE` (upheld sets the entry to `suppressed`, `moderation/services.py`); `Claim` (otp_phone, otp_email, documents); `Identifier` child model (scheme, value, issuer, `last_checked`, `register_url`); `outreach.SupplierVerification` (buyers only); `volunteers.CanaryEntry` (surveyor canaries); `Contact.value_hash` (lets us count phone reuse); `PayoutProfile` plus `details_fingerprint` | Registry checks, risk score, reuse graph, domain age, planted fake suppliers for the detector |
| C44 KYB and KYC | Payout KYC (`ledger.submit_kyc`, `decide_kyc`: encrypted legal name, country, method, account, tax id; self-approval refused; any change goes back to review); claims; two-person payouts | Business profile, registry-number validation, documents (text-only rule), UBO declaration, expiry, DSA article 30 view, advertiser verification above a spend threshold (M-33) |
| C45 sanctions and PEP | Nothing | Everything |
| C46 fake reviews | Decision Q-P3 only (verified users, one per user, owner reply, separate from paid rank). No review model found | Everything. Reviews do not exist yet |
| C47 account farms | Login throttle by account (5) and address (20) per 15 minutes (`accounts/throttle.py`); honeypot field `website2` (`catalog/forms_views.py`); quotas by address and account (`access/quotas.py`); `BEHIND_CLOUDFLARE` address trust; email verification; TOTP | Signup velocity, disposable-email block, phone uniqueness, Turnstile, shared-attribute graph, flag ladder |
| C50 appeals | `Report.resolution`, `Takedown.log`, `SuggestedEdit` decisions, `Claim` decisions: each has a decision but none has a reason code, statement, appeal, SLA or public counts | Whole spine |
| C51 tax | `TAX_RATES` (country to percent, empty by default), `tax_for`, `Order.tax_rate`, `tax_minor`, `Order.billing` (name, address, tax_id), gap-free `Invoice`, credit notes, `COMPANY_DETAILS` seller block | Tax mode (charge, reverse charge, MoR), buyer type, tax-id validation, place-of-supply evidence, withholding by customer, filing exports |
| C53 payout compliance | Holds (14 days), release job, exact refund reversal, `PayoutProfile` KYC, two-person payout and batch approval, details fingerprint, per-person advisory lock, minimum payout, daily reconciliation, payout cycle runbook | Sanctions gate, tax form, rail rules, name match, clawback record, dispute state, gateway refund and dispute events, reserve for new payees |
| C55 erasure | `Takedown` with 30-day due date, `execute_erasure` tombstone, global `Suppression` by keyed hash, consent withdrawal, subject access, audit chain, runbook | Derived-copy steps, index and CDN purge, extract notice, staging purge, backup window and restore replay |

### 2.2 Scale arithmetic (rule 13: state it before design)

| Quantity | Figure | Grade | Consequence |
|---|---|---|---|
| Entries | 5k (S0), 50k (S1), 1M (S2), 10M (S3), 100M (S4) | [R] matrix stage table | Never screen or score every entry on a schedule; trigger on events (claim, paid order, report) |
| Money parties (payees plus paid businesses plus extract buyers) | about 500 at S1, 7,000 at S2, 500,000 at S4 | [H] | Sanctions screening applies to these only |
| Sanctions list size | order of 10^4 to 10^5 rows across all lists | [I] (OFAC alone is in the tens of thousands, [K]) | Fits one indexed table |
| Brute-force fuzzy match | 7,000 subjects times 10^5 list rows is 7x10^8 comparisons; at about 10^7 comparisons a second that is about a minute | [I], [H] speed | Brute force is fine to about 10^4 subjects. Above that block by trigram index (`pg_trgm` on the list table) or run yente |
| Daily delta re-screen | 500,000 subjects times about 300 changed list rows is 1.5x10^8 | [I] | Re-screen against list deltas only, not full lists |
| Erasures | 0.1 percent of entries a year gives 100k a year at 100M entries, about 274 a day | [H] | CDN purge by tag, at 5 requests a minute on the free plan [S], is enough even at one tag per call (7,200 a day) |
| Review volume | unknown | [H] | One unique row per (entry, user); burst check reads only the last 24 hours of one entry |
| Account attribute edges | about 5 per account, 90-day retention; at 10M accounts about 50M rows | [H] | Hash only; delete after 90 days; component job runs on new edges only |
| Chargeback ratio | one dispute among 50 card sales is 2 percent | [I] | Visa excessive threshold is 1.5 percent from 1 April 2026 and Mastercard ECM is 1.5 percent with 100 or more in a month [S]; the ratio is unstable at pilot volume, so keep card volume off or on a MoR at the pilot |
| Order value | USD 49 text ad, USD 149 company page for 90 days, USD 199 city rank, USD 1,000 and up extract | [R] seeded products and decisions | MoR fee of 5 percent plus USD 0.50 is 6.0 percent on USD 49 and 5.3 percent on USD 199 [I] |

---

## 3. Shared design

### 3.1 Apps

| App | Holds | Depends on |
|---|---|---|
| `trust` (new) | `EnforcementAction`, `Appeal`, `ReasonCode`, `BusinessProfile`, `RegistryCheck`, `RiskCase`, `RiskSignal`, `Review` and friends, `AccountSignal`, `AccountCluster` | `core`, `entries`, `accounts`, `moderation` |
| `compliance` (new) | `SanctionsList`, `SanctionsEntry`, `ScreeningSubject`, `ScreeningHit`, `ScreeningDecision`, `TaxProfile`, `ErasureStep`, `DerivedCopy` registry, `ExtractMember`, `BankStatementLine` | `core`, `ledger`, `billing`, `entries` |
| `billing`, `ledger`, `moderation` (extended) | Tax decision, withholding, dispute, clawback, erasure steps | as today |

### 3.2 Rules every design below obeys

1. **Four check labels only.** KYB level, risk score and screening state are internal. They may be evidence for Owner-verified or Surveyor-verified through the existing guards. They never become a new public label, and paid rank never changes any of them (rule 4).
2. **Contacts and personal fields stay encrypted** (`EncryptedTextField`) with a keyed hash column for lookups and suppression. No national id number is kept beyond the check (note 03 LP-01). A CNIC or Aadhaar number is checked by shape and discarded unless counsel says to keep it.
3. **Text and numbers only on public pages.** Document images are not accepted on our own servers in the pilot (section 7 explains the vendor-hosted route).
4. **Every change is audited** with `core.models.audit(...)`. Audit payloads never carry names, contacts or ids (test in 14.6), because the audit chain is append-only and cannot be erased.
5. **Country switches gate behaviour.** Add `payouts_on` and `kyb_required` to `CountrySwitch` (default off and off). Nothing sells or pays in a country until the switch is on.
6. **Two people for money, one person per decision.** The decider of an appeal is never the original decider (same pattern as `decide_kyc` refusing self-approval).
7. **No real payments, upscaling or deployment** until the founder asks (rule 7). Everything here is staging and tests.

### 3.3 The enforcement spine (C50 is the base for the others)

`EnforcementAction` is written by every detector and every moderator action. Detectors never act silently.

| Field | Type | Note |
|---|---|---|
| id, created_at | | |
| subject_type, subject_id | char, bigint | entry, claim, review, user, order, payout, ad, placement |
| action_kind | choice | entry_suppressed, claim_rejected, paid_product_held, review_held, review_removed, account_limited, account_suspended, payout_held, credit_revoked, kyb_rejected, ad_rejected, screening_block |
| reason_code | fk `ReasonCode` | see 3.4 |
| statement | text | plain English, built from the code plus facts; see C50 for contents |
| decided_by | fk user, null | null only when `automated` and the action is reversible (hold, not removal) |
| automated | bool | true when a rule decided |
| state | choice | active, appealed, reversed, upheld, expired |
| appeal_until | datetime | 180 days from notice (H, see C50) |
| legal_hold | bool | true for screening blocks: statement may be limited by law; counsel |

### 3.4 Reason codes (seed list, `ReasonCode(code, text, appealable, user_visible)`)

| Code | Meaning | Appealable |
|---|---|---|
| SUP-01 | Registration number is not valid in its country | yes |
| SUP-02 | Registry name does not match the listed name | yes |
| SUP-03 | Registry shows the company closed | yes |
| SUP-04 | Same phone or address used by many unrelated listings | yes |
| SUP-05 | Several risk signals together | yes |
| KYB-01 | Evidence not enough for the level asked | yes |
| SCR-01 | Possible match to a sanctions list, under review | limited |
| SCR-02 | Confirmed match | limited (counsel) |
| REV-01 | Review looks copied or part of a burst | yes |
| REV-02 | Reviewer is connected to the business | yes |
| REV-03 | Review text breaks the rules | yes |
| ACC-01 | Many accounts share attributes | yes |
| ACC-02 | Automated sign-up pattern | yes |
| PAY-01 | Payout details changed, review needed | yes |
| PAY-02 | Open dispute on a sale that paid this share | yes |
| PAY-03 | Negative balance after a refund or chargeback | yes |
| LEG-01 | Legal order or court order | no |

---

## 4. Tool and licence register

Grade [R] means read in the unpacked wheel this session. GitHub repository LICENSE files were **not** read (tool refused). Costs are list prices from search summaries [S] unless stated.

| Tool | Use | Licence | How verified | Cost | Notes |
|---|---|---|---|---|---|
| python-stdnum 2.2 | Validate GSTIN, PAN, EU VAT, UK VAT, EIN, CNIC, IBAN, LEI | LGPL-2.1-or-later (COPYING and METADATA) | [R] wheel | free | Import as a library, do not copy modified files into our tree. `check_vies` needs the `zeep` extra and calls the old VIES SOAP service ([R] source); a newer REST route exists [K, UNVERIFIED]. `requires-python >=3.8` so fine for 3.11 to 3.13 |
| rapidfuzz 3.14.6 | Name matching for registry and sanctions | MIT | [R] wheel metadata | free | `requires-python >=3.11`; compiled wheels exist for our Pythons |
| Splink 5.0.0 | Probabilistic entity linking across entries and accounts at scale | MIT | [R] | free | Pulls duckdb, pyarrow, sqlglot. Full version only; matrix already plans it for C04/C05 |
| datasketch 2.0.0 | MinHash and LSH for review text similarity | MIT | [R] | free | Pulls numpy and scipy. For the pilot use `pg_trgm` similarity instead (already in the stack) and add this at scale |
| networkx 3.6.1 | Connected components and cluster analysis of account graphs | BSD-3-Clause | [R] | free | Weekly offline job, not in the request path |
| phonenumbers 9.0.40 | Normalise and validate phone numbers (region data for PK, AE, IN, GB, US present, [R]) | Apache-2.0 | [R] | free | Needed for C47 phone uniqueness; matrix says it is not in `requirements.txt` |
| django-axes 8.3.1 | Login lockout | MIT | [R] | free | **Not adopted**: `accounts/throttle.py` already does this and is tested |
| nomenklatura 4.17.0 | Entity matching framework behind OpenSanctions | MIT (copyright Lindenberg and OpenSanctions Datenbanken GmbH) | [R] | free | Optional; heavier than we need |
| yente | Self-hosted sanctions search API (needs Elasticsearch) | MIT | [S] | engine free; data licence needed | Full version if volume demands |
| OpenSanctions data | Sanctions and PEP data in one format | CC BY-NC 4.0; business use needs a licence (three tiers: internal use, financial services, reseller) | [S] | price on request, UNVERIFIED | Do not use the bulk data commercially without a licence |
| OFAC SDN list | Sanctions list | US government record; no use restriction stated [S] | [S] | free; XML and CSV, no key | UNVERIFIED legal wording; counsel |
| UN Security Council consolidated list | Sanctions list | XML on the Council's site [S] | [S] | free | |
| UK Sanctions List | Sanctions list | The OFSI consolidated list closed and the UK Sanctions List became the only source from 28 January 2026 [S]; Open Government Licence not confirmed | [S] | free | UNVERIFIED reuse terms |
| EU Financial Sanctions Files | Sanctions list | Reuse terms not found | [S] | free | UNVERIFIED reuse terms |
| Pakistan proscribed persons (Fourth Schedule) | Local list | Government notice; machine-readable copy via OpenSanctions dataset `pk_proscribed_persons` [S] | [S] | list free, copy under OpenSanctions licence | Take from NACTA and Ministry of Foreign Affairs notices at source |
| UAE Local Terrorist List and UN list | Local list | EOCN publishes; screening and goAML reports apply to regulated firms [S] | [S] | free | We are probably not a regulated firm; counsel |
| Cloudflare Turnstile | Bot challenge on signup, reveal, reports, enquiries | Cloudflare service terms | [S] | free, unlimited requests on the standard plan [S] | One review reported low detection (about 33 percent, from note 02, UNVERIFIED): a speed bump, not the defence |
| FingerprintJS 5 | Device id | MIT since v5.0 (22 Oct 2025); v4 was BSL 1.1 [S] | [S] | free | **Not adopted** for the pilot: fingerprinting needs consent in EU and UK [K, UNVERIFIED]. Use a first-party random cookie id instead |
| disposable-email-domains | Block throwaway email domains | CC0 [S] | [S] | free | A text list we load into a table |
| Have I Been Pwned Pwned Passwords | Breached-password check by k-anonymity | API free for passwords [S] | [S] | free | Already listed as CS-11 |
| pgBackRest | Postgres backups, retention, point in time | MIT [S] | [S] | free | Use at S2 when point-in-time recovery is needed; WAL retention must also be 35 days or less |
| WAL-G | Same | Apache-2.0 (LZO part GPL-3) [S] | [S] | free | Alternative |
| Meilisearch Community | Search engine at S3 | MIT; sharding is Enterprise under BUSL [S] | [S] | free | Delete is asynchronous (returns a task id) [S] |
| OpenSearch | Search engine at S3 | Apache-2.0 [S] | [S] | free | Deleted documents stay in segments until merged [K, UNVERIFIED] |
| Typesense | Search engine | GPL-3 [S] | [S] | free | Avoid unless counsel is happy with copyleft |
| Sumsub | KYC and KYB vendor | Commercial | [S] | USD 1.35 a verification, USD 149 monthly minimum (Basic); USD 1.85 and USD 299 minimum (Compliance) | KYB (company) price not found, UNVERIFIED |
| Veriff | KYC | Commercial | [S] | USD 49 a month plus USD 0.80 a verification | |
| Didit | KYC | Commercial | [S] | 500 free full-KYC checks a month, said to be permanent | UNVERIFIED claim |
| Stripe Identity | KYC | Commercial | [S] | price not confirmed; 50 free once | |
| Paddle | MoR | Commercial | [S] | 5 percent plus USD 0.50 | FTC settlement of USD 5 million in June 2025 over payment processing practices [S]; acceptable-use scope in section 12 |
| Lemon Squeezy | MoR (Stripe-owned) | Commercial | [S] | 5 percent plus USD 0.50, plus 1.5 percent international [S]; moving to Stripe Managed Payments (3.5 percent plus Stripe processing, waitlist) | Pakistani sellers fall in the "rest of world" payout group: PayPal only, 3 percent withdrawal fee capped at USD 30 [S] |
| Polar, Dodo Payments | MoR | Commercial | [S] | 4 percent plus USD 0.40 | Dodo says payouts to Pakistan work through Payoneer, Wise or local bank [S], UNVERIFIED |
| Stripe Tax | Tax calculation | Commercial | [S] | 0.5 percent a transaction, minimum USD 0.50 | Calculates; filing is separate |
| Quaderno, Avalara, TaxJar | Tax calculation and filing | Commercial | [S] | not found | |
| Simpaisa | Pakistan disbursement and collection | Commercial | [S] | not found | One API for bank, JazzCash, Easypaisa payouts [S] |
| Companies House API (UK) | UK company check | UK government terms | [S] | free; 600 requests per 5 minutes | |
| HMRC VAT number check API | UK VAT check | UK government terms | [S] | free; developer registration; returns a reference proving the check | |
| EU VIES | EU VAT check | EU service | [S] | free; usage limits | |

**Sizing note.** Everything in this table that is marked free costs USD 0 at the pilot. The only recurring pilot costs are an accountant and counsel, which I could not price.

---

## 5. Country reference tables (Pakistan, UAE, India, UK and EU, US)

### 5.1 Identity, registry and numbers

| | Company register and id | Tax id and format | python-stdnum [R] | How we verify | Notes |
|---|---|---|---|---|---|
| **Pakistan** | SECP eServices (eservices.secp.gov.pk). Company id is the CUIN, 7 digits [S]. Search returns name, CUIN, incorporation date, kind (private, public, SMC-private, non-profit), registered office, CRO jurisdiction, status; basic search free, certified extracts PKR 200 to 3,000 [S] | NTN (FBR). STRN for sales tax. CNIC is 13 digits (5 locality, 7 serial, 1 gender digit [R] source of `pk/cnic.py`). Exact NTN and STRN formats not confirmed, UNVERIFIED | `pk.cnic` only. **No NTN, STRN or CUIN** | Moderator searches SECP by CUIN; FBR Active Taxpayer List by CNIC or NTN through IRIS or the online verification page; SMS 9966 with a CNIC works for individuals [S]. NADRA identity checks only through a licensed partner [K, UNVERIFIED] | Sole traders and partnerships are not on SECP. For those use FBR ATL, chamber membership (for example Sialkot chamber) as supporting evidence, and a surveyor visit. Never store a CNIC after the check |
| **UAE** | No single national trade-licence number. Each emirate's economic department issues licences (Dubai DET, Abu Dhabi ADDED with its TAHAQAQ check, others by emirate); free zones issue their own [S] | TRN: 15 digits, same number for VAT, checked on the FTA site [S] | **None** for UAE | Licence number plus issuing authority plus name, checked on the emirate portal or u.ae "verify business licences" (free, no registration) [S]. TRN check on tax.gov.ae [S] | Store `issuing_authority` with the licence number; the number alone is ambiguous |
| **India** | MCA (CIN, 21 characters [K]); GST portal taxpayer search [K, UNVERIFIED access]; Udyam for MSMEs [K] | GSTIN 15 characters: 2-digit state, 10-character PAN, entity number, `Z`, check character (Luhn mod 36) [R] `in_/gstin.py`; PAN | `in_.gstin`, `in_.pan` (and `gstin.to_pan`, `info`), `in_.aadhaar`, `epic`, `vid`. **No CIN, no TAN** | Format and checksum with stdnum; name and status by manual check of the GST portal; registry data by manual MCA check | Never collect Aadhaar for verification: there are legal limits on private use [K, UNVERIFIED]. Do not store it |
| **UK** | Companies House (8-character number). Free API, 600 requests per 5 minutes [S] | UK VAT number: checked with the HMRC API, which returns name, address and a proof reference [S]. UTR for sole traders | `gb.vat`, `gb.utr`, `gb.nhs`, `gb.sedol`, `gb.upn`. **No company number** | API call; keep the HMRC reference with the check | Companies House data includes officers: personal data; store only what the check needs |
| **EU** | National registers; no single API (BRIS through e-Justice [K, UNVERIFIED]) | EU VAT, validated in VIES | `eu.vat` (dispatches to each country module, `check_vies` online), `eu.oss`, `vatin`, `lei` | stdnum format then VIES; keep the VIES result and date (the proof for reverse charge) | OSS number format is covered by `eu.oss` [R] |
| **US** | State secretary-of-state registries (no federal register) | EIN 9 digits | `us.ein`, `us.itin`, `us.ssn`, `us.tin`, `us.atin`, `us.ptin`, `us.rtn` | EIN is format-only; ownership proof by W-9 plus bank match. **OpenCorporates is excluded** (share-alike, backend research default) | Never store SSN. Collect W-9 or W-8BEN by self-declaration with counsel's form wording |

Phone numbers: `phonenumbers` has region data for PK, AE, IN, GB and US [R]. IBAN: Pakistan format is 4 letters (bank code) plus 16 alphanumeric characters, 24 characters in all; UAE is 3 digits plus 16 digits, 23 characters; India has no IBAN [R] `iban.dat`.

### 5.2 Tax on what we sell (subscriptions, ranking, company pages, ads, extracts)

| | Rule for our products | Grade | What we do |
|---|---|---|---|
| **Pakistan, domestic** | Sales tax on services is provincial: Sindh, Punjab, Khyber Pakhtunkhwa, Balochistan at 13 to 16 percent; Punjab 16 percent; reduced 5 percent for IT services. Which rate our directory, advertising or database access falls under is not confirmed | [S] vatcalc, Kintsugi; UNVERIFIED | Register with the authority of our home province (Punjab Revenue Authority if we are in Punjab). Accountant to classify each product. Config table, not code |
| **Pakistan, withholding by customers** | Customers who are withholding agents may deduct income tax and sales tax and issue a certificate; we receive net. Rates for services reported at 9 percent for companies and 11 percent for others for filers, double for non-filers (Section 153 as reported by a tax-help site, low quality) | [S, low quality]; UNVERIFIED | Record `withheld_minor` and the certificate reference on the payment; the order is settled when cash plus withheld equals the invoice (section 12.2) |
| **Pakistan, foreign suppliers into Pakistan** | Digital Presence Proceeds Tax of 5 percent was introduced in June 2025 and stopped from 1 July 2025 (SRO 1366(I)/2025) [S]. Finance Act 2026 (enacted 27 June 2026) added 5 percent withholding on social-media creator earnings and, in proposals, a 5 percent tax on foreign vendors with a significant digital presence; sources conflict | [S, conflicting] | Not our sales. It matters only if we pay a foreign platform or contributor: Section 152 requires deduction on royalties and fees to non-residents at schedule rates [S]. Ask the adviser |
| **UAE** | VAT 5 percent. A non-resident that makes taxable supplies where no one else is liable must register with no threshold; digital providers register from the first supply [S]. E-invoicing: ministerial decisions 243 and 244 of 2025, voluntary from July 2026, mandatory from 2027 on a Peppol (PINT AE) model [S] | [S] | Pilot: sell to UAE businesses with a TRN only, invoice with the reverse-charge legend, no UAE B2C. Re-check the reverse-charge rule with an adviser [S source wording is general] |
| **India** | Online information and database access or retrieval (OIDAR) from abroad: 18 percent IGST; the exemption for non-business recipients ended 1 October 2023; overseas suppliers register on form GST REG-10 whatever their turnover [S]. Online ads and cloud services are named as OIDAR [S] | [S] | Pilot: Indian businesses with a GSTIN only, by invoice, adviser to confirm reverse charge. Indian B2C or no GSTIN: MoR or decline. TDS 194-O (0.1 percent from 1 Oct 2024) applies to e-commerce operators paying participants, not to us unless we run an e-commerce marketplace [S] |
| **UK** | A non-UK business selling digital services to UK consumers registers from the first sale, no threshold; UK-established businesses have a GBP 90,000 threshold [S]. B2B: reverse charge with a valid UK VAT number | [S] | B2B with valid number: no UK VAT, legend. B2C: MoR |
| **EU** | Non-Union One Stop Shop for B2C digital services: no threshold for non-EU sellers (the EUR 10,000 relief is for EU-established sellers), quarterly returns, records kept 10 years from the end of the year of the transaction. B2B: reverse charge only with a valid VAT number; failing to check makes us liable [S] | [S] | B2B with VIES-valid number: legend. B2C: MoR |
| **US** | State sales tax by economic nexus (often USD 100,000 or 200 transactions a year; California USD 500,000) and state-by-state taxability: about 20 states tax SaaS, the rest do not [S]. Payee side: Form 1099-NEC and 1099-MISC threshold rises from USD 600 to USD 2,000 for 2026; 1099-K back to USD 20,000 and 200 transactions; foreign payees without a W-8BEN face 30 percent withholding (this binds US payers) [S] | [S] | Track US revenue per state against 60 percent of the lowest threshold [H]; MoR for US card sales. For US-person contributors, collect W-9; counsel decides if any filing duty exists for a non-US payer [K, UNVERIFIED] |
| **Records** | EU OSS: 10 years [S]. India, UAE, Pakistan, US retention periods not checked | [S] | Keep every invoice, credit note and tax evidence 10 years (design in 12.2) and say so in the privacy notice |

### 5.3 Payment rails

| Rail | Direction | What we know | Grade | Design use |
|---|---|---|---|---|
| Bank transfer (IBFT, IBAN) | in, out | IBAN checked with stdnum `iban`. Order reference goes in the transfer remarks; staff mark paid (already built as provider `manual`) | [R] | Pilot rail in and out |
| Raast | in (person to merchant QR), out (person to person) | P2M QR subsidy of 0.5 percent of value or PKR 100, whichever is lower, for 1 Sep 2025 to 30 Jun 2026; onboarding providers may charge up to 0.25 percent; over 2.6 million merchants onboarded or aliased by end of March 2026; merchants often still push customers to cash or wallets [S] | [S] | Pilot rail in through a bank's Raast merchant account; subsidy may have ended, check |
| Easypaisa, JazzCash | in, out | Wallets with merchant accounts; Simpaisa offers one disbursement API over bank, JazzCash and Easypaisa [S] | [S] | Full version via an aggregator; wallet limits depend on wallet KYC level [K, UNVERIFIED] |
| Cards, local PSP | in | Safepay named as a Stripe-backed local player; Checkout.com covers PK in MENAP but enterprise only [S] | [S] | Full version only; chargebacks apply |
| Stripe | in | Does not support businesses registered in Pakistan directly [S] | [S] | Not available unless the operating entity is elsewhere |
| PayPal, Payoneer, Wise | in, out | Payoneer and Stripe partnership for Pakistan merchants; PayPal for Pakistani sellers via MoR payouts only [S] | [S] | Foreign contributors: do not pay cash in the pilot (non-cash rewards exist already) |
| Cross-border outward payment from Pakistan | out | Needs bank or SBP rules [K, UNVERIFIED] | [K] | `payouts_on` per country; pilot pays only domestic rails |

### 5.4 Sanctions and watch lists to load

OFAC SDN, UN Security Council consolidated, UK Sanctions List, EU Financial Sanctions Files, Pakistan proscribed persons and the Fourth Schedule, UAE Local Terrorist List (plus UN list) [S]. India's own list not researched, UNVERIFIED. PEP data has no free comprehensive source; see C45.

---

## 6. C43 Fake supplier listings

### 6.1 Decision flow

Triggers: claim submitted; paid product ordered (company page, rank, ad); verified-supplier tier asked for; supplier-type bulk row published; report of kind `fake`; weekly sweep of entries that gained a placement.

1. **Normalise** identifiers the owner gave (Identifier rows: scheme, value) using stdnum or our own shape checks (section 5.1). Invalid shape gives signal S01 and stops the registry step.
2. **Registry check** (`RegistryCheck`): a moderator (pilot) or adapter (full) looks the number up at the register in 5.1. Record found or not, the registered name, address and status. Match score is `rapidfuzz.fuzz.token_set_ratio` on folded names (`core.textfold.fold`). Name match at 85 or more counts as matched [H].
3. **Signals** are computed from our own data and written as `RiskSignal` rows (code, weight, evidence hash). Weights are [H] to be fitted on the planted fakes.

| Signal | Rule | Weight |
|---|---|---|
| S01 | Registration or tax number fails format or checksum | +30 |
| S02 | Valid number, registry name score below 85 | +25 |
| S03 | Registry shows dissolved or struck off | +40 |
| S04 | Only free-mail contacts and no website on its own domain | +10 |
| S05 | Website domain registered less than 90 days ago (RDAP lookup, free [K]) | +15 |
| S06 | Phone hash (`Contact.value_hash`) used by 3 or more entries with different folded names | +25 |
| S07 | Same folded address on 5 or more entries with different names | +15 |
| S08 | Payout details fingerprint equals another account's | +30 |
| S09 | Description text similarity 0.9 or more to another entry (`pg_trgm similarity`) | +15 |
| S10 | Claimant account less than 7 days old | +10 |
| S11 | Name equals or nearly equals a well-known brand on a protected list | +20 |
| N01 | Registry matched and name score 95 or more | -20 |
| N02 | Surveyor visit recorded (verification event, level surveyor, field group identity) | -30 |
| N03 | Chamber or association membership recorded as evidence | -10 |

4. **Bands** (H): below 30 green; 30 to 59 amber; 60 or more red.
   - Green: nothing happens.
   - Amber: ordinary sale allowed, no verified-supplier tier, 1 in 5 sent to a surveyor sample (H).
   - Red: place the paid product on hold (`EnforcementAction` with `paid_product_held`, code SUP-05 or the strongest signal), tell the owner in plain English, queue for a moderator within 3 working days (H). A claim stays pending.
5. **Moderator decision**: clear (writes a `RegistryCheck` with `checked_by`), reject (action `claim_rejected` or `entry_suppressed`), or send to surveyor. Every outcome writes the spine row; an owner may appeal (C50).
6. **Planted fakes**: extend `CanaryEntry` with a supplier set: made-up businesses with an invalid CUIN, a 20-day-old domain, a phone reused 4 times, a registry name mismatch. The nightly job runs the engine on them and records recall. Target: red or amber on 95 percent or more of the planted fakes and on no more than 2 percent of a sample of known-good verified suppliers [H].

### 6.2 Data fields

`RegistryCheck`: entry fk, identifier fk (null), country, scheme, value_enc, value_hash, format_ok, lookup_source (secp, ded_dubai, added_abudhabi, mca, gst_portal, companies_house, vies, hmrc, manual, none), found bool, registered_name_enc, registered_address_enc, status (active, dissolved, unknown), name_score smallint, checked_by_id, checked_at, reference (HMRC or VIES proof reference), expires_at (re-check after 12 months).

`RiskCase`: entry fk, trigger, score, band, state (open, cleared, actioned), decided_by_id, decided_at, enforcement fk.

`RiskSignal`: case fk, code, weight, evidence_hash, created_at.

`ProtectedName` (brand list for S11): name_fold, country (blank for all), source, added_by.

### 6.3 Tools, licence, cost

python-stdnum (LGPL-2.1+), rapidfuzz (MIT), `pg_trgm` (PostgreSQL contrib, already used by the dedupe pipeline [R]), RDAP for domain age (public protocol, free [K]). Cost USD 0 in licences. The registry lookups at SECP are free for a basic search and PKR 200 to 3,000 for a certified extract [S]; buy extracts only for red cases.

### 6.4 Country notes

Per-country ids and routes: section 5.1. Pakistan: sole traders have no SECP record; weight N03 and N02 higher for them and never take a CNIC. UAE: the licence number needs the issuing authority. India: GSTIN checksum plus PAN consistency (`gstin.to_pan`). UK and EU: free API checks give a proof reference worth keeping.

### 6.5 Pilot versus full

| | Pilot | Full |
|---|---|---|
| Registry | Moderator checks SECP, FBR ATL, chamber, by hand; format checks in code | Adapters for Companies House, VIES, HMRC; vendor KYB where no API exists |
| Signals | S01, S02 (manual), S04, S06, S07, S08, S10, N02, N03 | All, plus Splink linking and weekly graph run (C47) |
| Review | One moderator queue; 3-working-day target | SLA timers, sampling, surveyor routing |
| Canaries | 20 planted fakes | Rotating sets, recall dashboard |

### 6.6 New tables and endpoints (design only)

Tables: `trust.RegistryCheck`, `trust.RiskCase`, `trust.RiskSignal`, `trust.ProtectedName`.

| Method and path | Who | Purpose |
|---|---|---|
| GET `/staff/risk/` | moderator | Queue (uses the existing generic `/staff/<key>/` queue mechanism) |
| POST `/staff/risk/<id>/clear/`, `/reject/`, `/to-surveyor/` | moderator | Decide (uses `/staff/<key>/<pk>/<action>/`) |
| GET `/account/business/` | owner | See what was asked and why a hold exists |
| management command `score_suppliers` | job | Weekly sweep and nightly canary recall |

### 6.7 Acceptance tests (`backend/trust/tests/test_supplier_risk.py`)

- `test_invalid_gstin_checksum_adds_signal_s01_and_no_registry_lookup_is_attempted`
- `test_valid_gstin_whose_embedded_pan_differs_from_the_stated_pan_is_flagged`
- `test_cnic_shape_is_checked_and_the_number_is_never_stored`
- `test_registry_name_below_85_adds_s02_and_name_at_95_subtracts_n01`
- `test_dissolved_company_in_registry_forces_red_band`
- `test_phone_hash_on_three_unrelated_entries_adds_s06`
- `test_same_folded_address_on_five_unrelated_names_adds_s07`
- `test_payout_fingerprint_shared_between_two_accounts_adds_s08`
- `test_new_claimant_account_under_seven_days_adds_s10`
- `test_surveyor_visit_lowers_the_score_and_never_creates_a_new_check_label`
- `test_red_case_holds_the_paid_product_and_writes_an_enforcement_action_with_a_reason_code`
- `test_green_case_changes_nothing_and_writes_no_action`
- `test_paid_rank_never_changes_a_risk_band_or_a_check_label`
- `test_planted_fake_suppliers_are_flagged_with_recall_at_least_95_percent`
- `test_known_good_supplier_sample_is_not_flagged_above_2_percent`
- `test_registry_check_expires_after_twelve_months_and_requeues`
- `test_owner_can_see_hold_reason_in_plain_english_without_other_entries_names`

---

## 7. C44 Business onboarding KYC and KYB

### 7.1 Levels (internal; never public labels)

| Level | Meaning | Gives |
|---|---|---|
| L0 | Self-declared: legal name, id numbers, address, representative | Free listing, claim by code |
| L1 | A contact value proven by one-time code (built in claims) | Company page, ordinary placement |
| L2 | Registry matched (6.1 step 2) and payment account name matches the legal name | Verified-supplier tier for outreach campaigns; sponsored slots; spend above the threshold |
| L3 | Evidence reviewed by a person or a vendor-hosted check, or a surveyor visit | Highest tier; feeds Owner-verified and Surveyor-verified through the existing guards |

Spend threshold for L2: cumulative paid spend above USD 500 in 12 months [H] (note 01 M-33 asks for advertiser verification before large spend). Payee KYC is separate and stays at payout time, as at Upwork (note 04).

### 7.2 Decision flow

1. A business starts from claim, order or campaign. Collect `BusinessProfile` (7.3). Validate id shapes at once (section 5.1).
2. L1 by one-time code (exists).
3. L2: moderator performs the registry check; payment account name compared with legal name (manual in pilot, exact or token-set 90 or more [H]).
4. L3: pilot uses a surveyor visit or a call; full version uses a **vendor-hosted flow** (Sumsub, Didit or similar): the vendor holds images, we receive only a verdict and a reference (`vendor_ref`). This keeps document images off our servers, which respects the text-only rule and avoids storing id documents. If the founder wants documents on our side, that is a decision (section 18, item 7): an encrypted private bucket, staff-only, retention 90 days after decision.
5. Screen the business name and representative (C45) before any L2 or L3 grant.
6. Expiry: levels expire after 12 months and drop one level until re-checked.
7. **DSA article 30**: where it applies (an EU-facing marketplace with distance contracts between consumers and traders, not exempt as a small or micro enterprise [S]), the marketplace must collect name, address, phone, email, ID copy, payment account and trade register number and show them to consumers, plus a self-certification [S]. A B2B directory may fall outside this [UNVERIFIED]; build the `trader_disclosure` view behind a per-country flag, default off, and ask counsel (note 03 question 7).

### 7.3 Data fields (`trust.BusinessProfile`)

user fk, entry fk (null), legal_name_enc, trade_name, entity_form, country, registry_scheme, registry_number_enc, registry_number_hash, tax_id_scheme, tax_id_enc, tax_id_hash, tax_id_valid bool, registered_address_enc, representative_name_enc, representative_role, beneficial_owners_enc (JSON; declared owners above 25 percent [K, UNVERIFIED]; self-declared in pilot), level (L0 to L3), state (open, under_review, approved, rejected, expired), vendor, vendor_ref, evidence_note (plain text from reviewer), decided_by_id, decided_at, expires_at.

Keep: `ledger.PayoutProfile` as is for people who receive money. A business that both buys and earns has one `BusinessProfile` and one `PayoutProfile`; the payout gate checks both names agree (C53).

### 7.4 Tools, licence, cost

Pilot: none (manual). Vendors [S, UNVERIFIED]: Sumsub USD 1.35 a verification with USD 149 monthly minimum (Basic); Veriff USD 49 a month plus USD 0.80; Didit 500 free checks a month; Stripe Identity 50 free once. KYB (company) pricing was not found. At fewer than 100 checks a month the Sumsub minimum alone is USD 1,788 a year [I], so use manual review or the Didit free tier at the pilot.

### 7.5 Country notes

Section 5.1 gives ids and registers. UAE: licence plus issuing authority, TRN separately. India: GSTIN plus PAN; do not collect Aadhaar. Pakistan: NADRA checks only through a licensed partner; avoid in pilot. UK and EU: API checks. US: W-9 self-declaration plus bank name match.

### 7.6 Pilot versus full

| | Pilot | Full |
|---|---|---|
| Evidence | Text fields, registry by hand, OTP, bank name match, surveyor | Vendor-hosted KYB, adapters |
| Levels | L0 to L2 | L0 to L3 and expiry job |
| DSA view | Off | Per country flag |

### 7.7 New tables and endpoints

Tables: `trust.BusinessProfile`; extends `compliance.TaxProfile` (C51).

| Method and path | Who | Purpose |
|---|---|---|
| GET and POST `/account/business/` | any user | Create and edit own profile |
| POST `/account/business/<id>/start-check/` | owner | Ask for L2 or L3 |
| GET `/staff/kyb/`, POST `/staff/kyb/<id>/approve/` and `/reject/` | moderator | Queue and decision; the approver is never the account owner |
| POST `/webhooks/kyb/<provider>/` | vendor | Verdict and reference, signed, idempotent (same pattern as payments) |
| GET `/e/<uid>/<slug>/trader/` | public, flagged by country | DSA article 30 disclosure view |

### 7.8 Acceptance tests (`backend/trust/tests/test_kyb.py`)

- `test_business_profile_encrypts_legal_name_registry_and_tax_ids_at_rest`
- `test_profile_search_by_hash_finds_a_company_without_decrypting`
- `test_level_two_needs_registry_match_and_payment_name_match`
- `test_level_two_is_required_before_cumulative_spend_passes_the_threshold`
- `test_level_three_via_vendor_stores_only_verdict_and_reference_never_images`
- `test_vendor_webhook_signature_and_replay_are_safe`
- `test_levels_drop_one_step_after_twelve_months`
- `test_approver_cannot_be_the_profile_owner`
- `test_business_level_never_creates_a_fifth_public_check_label`
- `test_trader_disclosure_view_is_404_unless_the_country_flag_is_on`
- `test_gstin_with_wrong_state_code_is_refused_at_form_time`
- `test_uae_licence_number_requires_an_issuing_authority`
- `test_screening_runs_before_level_two_is_granted`

---

## 8. C45 Sanctions and PEP screening

### 8.1 What to screen, and when

| Subject | Trigger |
|---|---|
| Payee (legal name, country) | KYC submitted; payout created; list delta |
| Business buyer at L2 or above, or spend above the threshold | Level grant; order above the threshold; list delta |
| Extract buyer (institution) | Before an extract order is accepted |
| Verified-supplier tier | At grant |

Entries are not screened (see 2.2).

### 8.2 Decision flow

1. **Fetch** each list daily as a job (`JobRun`), store a `SanctionsList` row (list code, version, fetched_at, sha256, entry count) and upsert `SanctionsEntry` rows. A failed or stale fetch (older than 48 hours [H]) raises the existing health alarm and blocks new payouts until fixed.
2. **Normalise** the subject name and every list name and alias with `fold()`; also a token-sorted form.
3. **Match** with rapidfuzz `fuzz.WRatio` and `token_sort_ratio`:
   - 95 or more: hard hit, auto-hold, escalate.
   - 85 to 94: possible hit, review queue; country or birth year, if available, corroborates.
   - below 85: clear.
   (all thresholds [H]; fit them on a labelled set of 200 names, half true list names with spelling changes, half common Pakistani, Arabic and Indian names that are not listed.)
4. **Review**: a second person (not the payout creator) marks false positive, true match or needs more information, writing a rationale. `ScreeningDecision` stores the list versions, scores and reviewer. A true match keeps the hold, writes `screening_block` with `legal_hold = true`, and goes to counsel: tipping-off, reporting and freezing duties vary (UAE regulated firms file name-match reports through goAML [S]; we are probably not regulated, UNVERIFIED).
5. **Gate**: payout creation and L2 grant refuse if a subject has an open hit or no clear screening newer than the last list version for that country's lists.
6. **PEP**: pilot asks one question at payout KYC ("holds or held a senior public position, or is a close family member or associate") and sends a yes to manual review. There is no free complete PEP list; full version licenses OpenSanctions PEP data or a vendor.

### 8.3 Data fields

`SanctionsList`(code, version, fetched_at, sha256, count, source_url, licence_note). `SanctionsEntry`(list fk, source_ref, type person or entity, name, name_fold, aliases JSON, countries JSON, birth_year, programme, added_on, removed_on). `ScreeningSubject`(subject_type, subject_id, name_enc, name_fold, country, birth_year null, last_screened_at, last_list_versions JSON). `ScreeningHit`(subject fk, entry fk, score, matched_on, state open, cleared, true_match). `ScreeningDecision`(hit fk, decided_by_id, outcome, rationale, list_versions JSON, decided_at).

### 8.4 Tools, licence, cost

Government lists: free [S]. rapidfuzz MIT [R]. `pg_trgm` index on `SanctionsEntry.name_fold` as the blocking step above about 10^4 subjects. OpenSanctions data is CC BY-NC 4.0 and business use needs a licence (internal use, financial services or reseller tiers; price on request) [S]; yente is MIT [S]. I did not find OpenSanctions pricing. Recommendation: government lists at the pilot; ask OpenSanctions for a quote before S2 if PEP data is wanted.

### 8.5 Country notes

Pakistan: proscribed persons under the Anti-Terrorism Act and the Fourth Schedule; Ministry of Foreign Affairs notices for UN lists; NACTA publishes [S]. UAE: Local Terrorist List and UN list; screening on onboarding, on change and on every list update; reports through goAML for regulated firms [S]. India: not researched. UK: UK Sanctions List (the only source from 28 January 2026 [S]). EU: Financial Sanctions Files. US: OFAC. We load all six sets whatever the payee's country because a clearing bank may apply OFAC to dollar flows [K, UNVERIFIED].

### 8.6 Pilot versus full

| | Pilot | Full |
|---|---|---|
| Lists | OFAC, UN, UK, EU, Pakistan, UAE | Same plus PEP data under licence |
| Matching | rapidfuzz brute force | trigram blocking or yente |
| Review | Finance and moderator, two people | SLA, tuned thresholds, audit sample |
| Re-screen | Daily against list deltas | Same |

### 8.7 New tables and endpoints

Tables: the five in 8.3.

| Method and path | Who | Purpose |
|---|---|---|
| GET `/staff/screening/` | finance, moderator | Hit queue |
| POST `/staff/screening/<id>/false-positive/`, `/true-match/`, `/more-info/` | finance, moderator (not the payout creator) | Decide |
| management command `fetch_sanctions` | job | Daily |
| management command `rescreen_subjects` | job | Delta re-screen |

### 8.8 Acceptance tests (`backend/compliance/tests/test_screening.py`)

- `test_list_fetch_stores_version_hash_and_entry_count`
- `test_stale_list_older_than_48_hours_blocks_new_payouts_and_raises_an_alarm`
- `test_exact_listed_name_is_a_hard_hit_and_holds_the_payout`
- `test_transliteration_variant_of_a_listed_name_lands_in_the_review_band`
- `test_common_unlisted_pakistani_name_is_clear_on_the_labelled_set`
- `test_labelled_set_reports_recall_at_least_98_percent_and_false_positive_rate_below_5_percent`
- `test_birth_year_mismatch_lowers_a_review_band_hit_to_clear_with_log`
- `test_payout_creator_cannot_decide_a_hit_on_their_own_payout`
- `test_true_match_writes_screening_block_with_legal_hold_and_a_limited_statement`
- `test_payout_refused_while_a_hit_is_open`
- `test_new_list_entry_triggers_rescreen_of_existing_payees_only`
- `test_removed_list_entry_clears_open_hits_with_a_log_line`
- `test_subject_names_are_encrypted_at_rest_and_never_in_audit_payloads`
- `test_pep_yes_answer_routes_to_manual_review`

---

## 9. C46 Fake reviews

### 9.1 Position

No review model exists [R]. The only decision is Q-P3: verified users only, one per user, owner reply, separate from paid ranking [R]. The law is tightening: the US FTC rule (16 CFR 465, effective 21 October 2024) bans fake and bought reviews, insider reviews, review suppression and bought followers, with civil penalties reported at USD 51,744 a violation in 2024 [S]; the UK Digital Markets, Competition and Consumers Act bans fake reviews from 6 April 2025 with fines up to 10 percent of global turnover and expects platforms to take reasonable steps and have a policy [S]; India's IS 19000:2022 (voluntary) bars reviews bought or written by paid individuals [S]. Pakistan and the UAE not researched, UNVERIFIED.

**Recommendation: do not launch star ratings in the pilot.** There is no traffic to protect and nothing to defend. Build the rules and tables, keep the feature flag off, and turn it on per list type after the first thousand verified entries with traffic [H]. Contributors and surveyors never earn credit for reviews, which removes the main incentive.

### 9.2 Decision flow (when on)

1. **Eligibility**: verified email, account at least 7 days old, phone proven by one-time code (H, the phone hash must be unique across accounts), not the owner, not a contact of the entry (the reviewer's phone or email hash must not equal any `Contact.value_hash` of the entry or of entries sharing its registry number).
2. **One review per (entry, user)**; an edit replaces and is logged (`edited_at`).
3. **Content rules**: text and numbers only, 20 to 2,000 characters, no contact values (the existing contact-extraction scan), facts about the experience, no opinions about other businesses.
4. **Automatic checks on submit**:
   - Burst: reviews on this entry in 24 hours exceed baseline (median daily count over 90 days) by more than 5 times and at least 4 reviews [H] gives REV-01.
   - Similarity: `pg_trgm` similarity of 0.8 or more to any other review in the last 90 days gives REV-01 (datasketch MinHash later).
   - Link: reviewer account shares a cluster flag (C47) with the owner or with 2 or more other reviewers of the same entry gives REV-02.
   - Pattern: reviewer has only five-star reviews and all for entries sharing an owner or registry cluster gives REV-02.
5. **State**: pending, published, held, removed. Any REV code puts the review in held and creates an `EnforcementAction`; the reviewer is told why, may appeal; a moderator decides.
6. **Show a score** only with 5 or more published reviews (H). Rank by the platform ordering, never by the reviews, and never by payment (decision, `Placement` rules unchanged).
7. **Owner reply**: one public reply, text only, labelled "Reply from the business".
8. **Disclosure page**: "How reviews are checked" says what is checked, that no one is paid to write reviews and that sponsorship does not touch reviews (the DMCC policy requirement [S]).
9. **Insider and incentive ban** in the terms: owners, staff, relatives and anyone rewarded may not review (matches the FTC insider rule [S]).

### 9.3 Data fields

`Review`: entry fk, user fk, rating smallint 1 to 5, text, state, created_at, edited_at, reason_code fk null, phone_hash, ip24_hash, did_hash, `interaction_proof` (bool: reviewer used the enquiry relay with this entry, for a "contacted via AllLists" mark), unique(entry, user). `OwnerReply`: review fk unique, text, created_by, created_at. `ReviewSignal`: review fk, code, detail JSON.

### 9.4 Tools, licence, cost

`pg_trgm` (in stack), rapidfuzz MIT [R], datasketch MIT (needs numpy and scipy) [R] at scale. No third-party fake-review product is proposed. Cost USD 0.

### 9.5 Pilot versus full

| | Pilot | Full |
|---|---|---|
| Feature | Off. Tables and rules exist; "report a fake" works (exists) | On per list type |
| Checks | Eligibility, one per user, manual moderation | Burst, similarity, link checks, appeal |
| Score | None | Shown after 5 published |

### 9.6 New tables and endpoints

Tables: `trust.Review`, `trust.OwnerReply`, `trust.ReviewSignal`.

| Method and path | Who | Purpose |
|---|---|---|
| POST `/e/<uid>/<slug>/review/` | eligible user | Submit |
| POST `/account/reviews/<id>/edit/` | author | Edit |
| POST `/account/owner/<uid>/reply/<review_id>/` | owner | Reply |
| GET `/staff/reviews/`, POST `.../<id>/publish/` `/remove/` | moderator | Decide |
| GET `/how-reviews-work/` | public | Policy page |

### 9.7 Acceptance tests (`backend/trust/tests/test_reviews.py`)

- `test_review_needs_verified_email_phone_proof_and_seven_day_old_account`
- `test_owner_and_entry_contact_cannot_review_their_own_entry`
- `test_reviewer_phone_equal_to_an_entry_contact_hash_is_refused_as_insider`
- `test_one_review_per_user_per_entry_and_edit_replaces_with_a_log`
- `test_review_with_a_phone_number_in_the_text_is_refused`
- `test_burst_of_five_times_baseline_holds_new_reviews_with_rev_01`
- `test_near_copy_of_another_review_is_held`
- `test_reviewer_in_the_same_cluster_as_the_owner_is_held_with_rev_02`
- `test_held_review_creates_an_enforcement_action_and_a_reviewer_notice`
- `test_score_is_hidden_below_five_published_reviews`
- `test_paid_placement_never_changes_review_score_order_or_state`
- `test_no_contributor_credit_event_is_created_by_a_review`
- `test_owner_gets_one_reply_and_it_is_labelled`
- `test_review_feature_flag_off_returns_404_for_every_review_route`

---

## 10. C47 Account farms and sybil accounts

### 10.1 Decision flow

1. **At signup**: Turnstile token checked (free, [S]); honeypot field (exists); disposable-email domain list (CC0, [S]); normalise email (strip dots and plus tags for known providers) and refuse a duplicate normalised address; phone uniqueness is asked later (reviews, claims by phone, payout).
2. **Velocity**: more than 3 signups per hashed /24 (IPv4) or /64 (IPv6) in 24 hours, or more than 10 per hour site-wide from one ASN [H], triggers a Turnstile interactive challenge, not a block.
3. **Record signals** as hashes (`AccountSignal`): ip_block, did (first-party random cookie set at first visit, no fingerprinting), phone_hash, payout_fingerprint, email_domain (custom domains only), claim_contact_hash. Retention 90 days, then deleted.
4. **Graph**: weekly job builds edges between accounts that share a signal value. Edge weights [H]: payout_fingerprint 1.0, phone_hash 1.0, did 0.6, claim_contact_hash 0.6, ip_block 0.2, custom email domain 0.3. Connected components by weighted threshold 1.0 (networkx at scale; a recursive query in the pilot). A cluster with 4 or more accounts, or total edge weight 3 or more, gets `AccountCluster` and `RiskFlag`.
5. **Ladder** (matches AS-11): clear, then Turnstile on every form, then lower quotas, then hold contributor credit payouts for cluster members (PAY-02 style), then suspend with a statement and an appeal. Every step writes an `EnforcementAction`.
6. **Credit gaming link (C48)**: contributor credit is already payable only after an independent verification [R]; the payout gate also refuses a payee who sits in an open cluster until a moderator clears it.
7. **Existing quotas**: new accounts get the lower anonymous-like quota for the first 7 days [H] (AS-10 not built).

### 10.2 Data fields

`AccountSignal`: user fk, kind, value_hash, first_seen, last_seen, count; index on (kind, value_hash). `AccountCluster`: id, created_at, member_count, weight, state (open, cleared, actioned). `AccountClusterMember`: cluster fk, user fk. `DisposableDomain`: domain, source, added_at.

### 10.3 Tools, licence, cost

Cloudflare Turnstile free [S]; disposable-email-domains CC0 [S]; phonenumbers Apache-2.0 [R]; networkx BSD-3 [R]; Postgres recursive queries [K]. Not adopted: FingerprintJS (v5 is MIT [S] but fingerprinting needs consent in EU and UK, UNVERIFIED) and django-axes (we already have a throttle [R]). Cost USD 0.

### 10.4 Country notes

Pakistan and India: phone is the main identity (note 04), so phone uniqueness is the strongest signal; shared family phones and shop phones exist, so a shared phone is a weight, not a ban. Carrier-grade NAT puts many mobile users behind one address in Pakistan and India [K, UNVERIFIED], so keep the IP-block weight at 0.2. EU and UK: no cookie id before consent where the id is not strictly necessary [K, UNVERIFIED]; set the `did` cookie only after the cookie choice or treat it as security-necessary with counsel's advice.

### 10.5 Pilot versus full

| | Pilot | Full |
|---|---|---|
| Signup | Turnstile, honeypot, disposable list, email normalisation | Same |
| Graph | Weekly SQL on phone and payout fingerprint only | Full signals, networkx, Splink |
| Action | Moderator reviews clusters; payouts held | Automated ladder with reviewers |

### 10.6 New tables and endpoints

Tables: `trust.AccountSignal`, `trust.AccountCluster`, `trust.AccountClusterMember`, `trust.DisposableDomain`.

| Method and path | Who | Purpose |
|---|---|---|
| GET `/staff/clusters/`, POST `.../<id>/clear/` `/action/` | moderator | Review clusters |
| management command `build_account_graph` | job | Weekly |
| management command `purge_account_signals` | job | Daily, deletes rows older than 90 days |

### 10.7 Acceptance tests (`backend/trust/tests/test_account_farms.py`)

- `test_signup_without_a_valid_turnstile_token_is_refused_when_the_switch_is_on`
- `test_disposable_email_domain_is_refused_at_signup`
- `test_gmail_dots_and_plus_tags_do_not_create_a_second_account`
- `test_fourth_signup_from_one_ip_block_in_a_day_requires_an_interactive_challenge`
- `test_honeypot_filled_signup_is_dropped_silently_and_logged`
- `test_phone_hash_is_unique_across_accounts_for_phone_proof`
- `test_two_accounts_with_one_payout_fingerprint_form_a_cluster`
- `test_cluster_of_four_accounts_creates_a_risk_flag`
- `test_shared_ip_block_alone_never_flags_a_cluster`
- `test_flagged_cluster_member_cannot_create_a_payout_until_cleared`
- `test_signals_older_than_90_days_are_deleted`
- `test_signals_store_hashes_only_never_addresses_or_phone_numbers`
- `test_each_ladder_step_writes_an_enforcement_action`
- `test_new_account_quota_is_lower_for_the_first_seven_days`

---

## 11. C50 Appeals and enforcement fairness

### 11.1 Statement of reasons

Modelled on the EU Digital Services Act article 17 elements as summarised in search results [S, UNVERIFIED wording]: what action was taken and its scope; the facts and circumstances; whether automated means were used; the rule or contract term relied on (or the legal ground); how to contest. Written in plain English from the reason code plus facts. For screening blocks the statement may be limited (counsel).

### 11.2 Decision flow

1. A detector or moderator creates an `EnforcementAction` (3.3). The user is notified by email at once, with the statement and a link.
2. **Appeal**: free, by form, within 180 days of the notice [H] (the DSA internal complaint system is said to be free, electronic and open for a period; I did not confirm the period, UNVERIFIED [S]). Fields: action, why the user thinks it is wrong, optional evidence text.
3. **Acknowledge** within 2 days (India's e-commerce rules require acknowledgement of a consumer complaint within 48 hours by a grievance officer [S]); **decide** within 14 days [H].
4. **Reviewer** is different from the original decider and, for automated actions, is a moderator. For amber and red supplier cases and held reviews the second reviewer sees the signals.
5. **Outcome**: overturned (reverse handler runs), upheld (reason recorded), partly (e.g., hold lifted but tier not granted). A `REVERSE` registry maps each `action_kind` to a function that undoes it (reinstate entry, release hold, restore review, lift limit).
6. **Out-of-court settlement** (DSA article 21) and the micro and small enterprise exemption from the platform complaint duties (article 19 [S]): we are likely exempt as a small enterprise at first, UNVERIFIED; build it anyway because it is cheap and is also the grievance route India expects (note 03 LP-12).
7. **Transparency**: `/transparency/` page with monthly counts by action kind and reason, appeals received, overturned, median days to decide. Counts under 5 are hidden, the same rule as the statistics reports [R].
8. **Repeat-offender policy** (note 03 LP-10): three upheld actions in 12 months leads to suspension review; payouts are held while a claim is open (ledger holds exist).
9. **Limits**: legal orders (LEG-01) are not appealable to us; we point to the issuing authority.

### 11.3 Data fields

`EnforcementAction`: 3.3. `Appeal`: action fk, filed_by, filed_at, text, evidence_text, state (received, acknowledged, in_review, decided), acknowledged_at, decided_by_id, decided_at, outcome (overturned, upheld, partial), outcome_text. `ReasonCode`: code, text, appealable, user_visible. `TransparencyCount` (derived, monthly): month, action_kind, reason_code, count, appealed, overturned, median_days.

### 11.4 Tools, licence, cost

None needed; Django only. Cost USD 0. The article text came from search summaries [S]; read the Regulation before quoting it.

### 11.5 Pilot versus full

| | Pilot | Full |
|---|---|---|
| Spine | `EnforcementAction` and `ReasonCode` wired into existing moderator decisions (reports, claims, ads, suggestions) | Every detector wired |
| Appeal | Form, email, moderator queue, 14-day target | SLA timers, reviewer assignment, escalation |
| Public | Terms page with the process; no counts | `/transparency/` monthly counts |

### 11.6 New tables and endpoints

Tables: `trust.EnforcementAction`, `trust.Appeal`, `trust.ReasonCode`, `trust.TransparencyCount`.

| Method and path | Who | Purpose |
|---|---|---|
| GET `/account/notices/`, GET `/account/notices/<id>/` | affected user | See actions and statements |
| POST `/account/notices/<id>/appeal/` | affected user | File an appeal |
| GET `/staff/appeals/`, POST `/staff/appeals/<id>/overturn/` `/uphold/` `/partial/` | moderator, not the original decider | Decide |
| GET `/transparency/` | public | Counts |
| management command `build_transparency_counts` | job | Monthly |

### 11.7 Acceptance tests (`backend/trust/tests/test_appeals.py`)

- `test_every_enforcement_action_has_a_reason_code_and_a_plain_english_statement`
- `test_automated_action_is_marked_automated_and_names_the_rule`
- `test_user_is_emailed_the_statement_and_appeal_link_at_once`
- `test_appeal_is_free_and_can_be_filed_until_the_deadline_only`
- `test_appeal_is_acknowledged_within_two_days_or_it_appears_on_the_overdue_list`
- `test_appeal_decider_cannot_be_the_original_decider`
- `test_overturned_appeal_runs_the_reverse_handler_for_each_action_kind`
- `test_upheld_appeal_stores_a_reason_and_the_user_is_told`
- `test_legal_order_action_is_not_appealable_and_shows_the_authority`
- `test_screening_block_statement_is_limited_and_does_not_name_the_list_entry`
- `test_three_upheld_actions_in_twelve_months_open_a_suspension_review`
- `test_transparency_page_hides_counts_below_five`
- `test_transparency_counts_match_the_underlying_rows`
- `test_audit_chain_records_action_appeal_and_decision`

---

## 12. C51 Cross-border tax on subscriptions and list sales

### 12.1 What the code does today [R]

`billing.services.create_order` takes `country = scope_path.split(".")[0]` (the country of the place being sold) or the entry's country, then `tax_for(country, price)` with one flat percent from `settings.TAX_RATES`. It never looks at the buyer's country, buyer type or tax id; `Order.billing` keeps whatever name, address and tax id the buyer typed. `issue_invoice` writes a tax line only if `tax_minor` is non-zero. `_record_payment` demands the paid amount equals the order amount.

### 12.2 Design

**Tax decision function** (new `billing/tax.py`, design only): `tax_decision(seller_entity, buyer, product_kind, date)` returns `TaxDecision(rate, mode, legend, evidence)` where `mode` is one of `charge`, `reverse_charge`, `export_none`, `mor`, `blocked`.

Inputs: seller entity (country, tax id), buyer country, buyer type (business or consumer), buyer tax id and its validation result, product kind, date.

```
1  buyer country  = billing country (typed); evidence list collects:
                    billing country, edge-header country (exists), payment-card or bank country
2  if evidence contradicts (two disagree):      mode = blocked   -> ask the buyer, stop
3  if buyer country = seller country:           mode = charge    -> rate from TaxRule(country, region, product)
4  if buyer is a business AND tax id valid
   (stdnum shape + VIES/HMRC/FTA check):        mode = reverse_charge, rate 0, legend, keep check reference
5  if buyer is a consumer (or no valid id):
       if a MoR is configured for the country:  mode = mor
       else if country switch allows B2C:       mode = charge (registered) 
       else:                                    mode = blocked, message "business customers only"
6  store mode, rate, evidence, check reference on the Order
```

Place of supply by country is in 5.2. EU rule on evidence (two non-contradictory pieces of evidence for consumer digital supplies) is from my memory [K, UNVERIFIED]; the design stores three pieces so any rule can be met.

**Config, not code**: `TaxRule(country, region, buyer_type, product_kind, rate, mode, requires_tax_id, valid_from, valid_to, note)`. The existing `TAX_RATES` becomes a fallback and migration source.

**Fields to add**: `Order.tax_mode`, `Order.tax_evidence` (JSON), `Order.buyer_country`, `Order.buyer_type`, `Order.tax_check_ref`; `Invoice.legend`, `Invoice.issuer` (`self` or `mor`), `Invoice.seller_tax_id`, `Invoice.buyer_tax_id`; `Sale.tax_collected_by` (`self` or `mor`).

**Withholding by customers** (Pakistan, and TDS in India): `Payment.withheld_minor` and `Payment.withholding_cert_ref`. The order is settled when `amount_minor + withheld_minor` equals the order total. A new ledger account kind `withheld` (tax withheld by customers, claimable against our tax) takes the withheld part; reconciliation includes it. A certificate tracker `WithholdingCertificate`(payment fk, type, number, tax_year, amount_minor, received_at) closes the loop: an alarm when no certificate arrives within 60 days [H].

**Records**: invoices, credit notes, tax evidence and VIES, HMRC and FTA check references are kept 10 years (EU OSS rule [S]; adopt it everywhere). Erasure does not remove them (legal obligation); they are fenced off from every other use (section 14).

**Invoice content**: seller legal name and address, seller tax id, buyer legal name and address, buyer tax id where applicable, tax mode legend ("Reverse charge: VAT to be accounted for by the recipient" or the local wording), currency, tax rate and amount per line, credit note linked. UAE e-invoicing (Peppol PINT AE, mandatory from 2027 [S]) and Indian e-invoicing are later; keep invoice lines structured JSON so a Peppol mapping is possible.

**Filing support**: monthly `tax_report` by country, mode and rate (extends `billing/reporting.py`) for the accountant; OSS and UK returns are the accountant's or the MoR's job.

**Operating-entity prerequisite**: the seller entity's country decides which of these rules we are on the wrong end of. The founder has not chosen it (note 03 question 12, LC-01). Do not build filing features before that decision.

### 12.3 Decision table: merchant of record versus own tax handling

| Situation | Recommended | Why | Trigger to change |
|---|---|---|---|
| Pakistan buyer pays by bank transfer, Raast, JazzCash or Easypaisa | Own handling | MoRs are built for card checkout from abroad; PRA and FBR registration and withholding certificates are ours anyway | None |
| Pakistan buyer pays by card through a local PSP | Own handling | Same | Chargeback ratio near 1 percent |
| UAE business with a valid TRN, invoice by bank transfer | Own handling, reverse-charge legend | No UAE VAT registration if the buyer self-accounts [S, confirm] | UAE revenue large enough to justify registration, or UAE B2C wanted |
| UAE consumer or business without TRN | MoR, or decline in the pilot | Non-resident digital suppliers register from the first supply with no threshold [S] | Founder decides on UAE B2C |
| India business with valid GSTIN, invoice by bank transfer | Own handling, adviser confirms reverse charge | OIDAR from abroad is 18 percent IGST; B2B mechanics need an adviser [S] | India revenue justifies REG-10 registration |
| India consumer or no GSTIN | MoR, or decline | GST REG-10 registration is required whatever the turnover [S] | As above |
| UK or EU business with a valid VAT number (VIES or HMRC check passed) | Own handling, reverse charge | Reverse charge only works with a checked number; we are liable if it is invalid [S] | Volume |
| UK or EU consumer | MoR (or Non-Union OSS and UK VAT registration later) | No threshold for non-EU or non-UK sellers; quarterly OSS returns; 10-year records [S] | Annual non-pakistan revenue above the break-even below |
| US, any buyer, card | MoR or Stripe Tax plus own registration | State nexus and SaaS taxability vary; about 20 states tax SaaS [S] | Revenue in one state passes 60 percent of its threshold |
| Recurring subscription paid by card, any non-PK country | MoR | Renewals, strong customer authentication, dunning, refunds and chargebacks are the MoR's job | Never go back |
| Contributor payouts | Own, always | A MoR sells for us; it does not pay our contributors | None |
| Paid ranking, ads, sponsored slots | Check the MoR's acceptable-use policy in writing | Paddle's published prohibition list reportedly includes advertising and sponsorship [S, UNVERIFIED]; nothing found on data lists or lead generation | Written answer from vendor |
| Extract sold to an institution, USD 1,000 and up | Own, invoice and wire | Few large B2B sales; reverse charge by country; extract terms apply | Buyer country has no workable B2B route |

**Cost comparison** [S, I]: Paddle and Lemon Squeezy 5 percent plus USD 0.50 (Lemon Squeezy plus 1.5 percent international); Polar and Dodo 4 percent plus USD 0.40; Stripe Managed Payments 3.5 percent plus Stripe processing (waitlist). On USD 49 that is 6.0 percent (5 percent plus 0.50) or 4.8 percent (4 percent plus 0.40); on USD 199, 5.3 percent or 4.2 percent [I]. Own handling has fixed costs per registration (adviser, filing) I could not price. **Break-even rule**: use a MoR while 5 percent of annual non-Pakistan revenue is below the yearly cost of the registrations you would otherwise need. At USD 24,000 a year of non-Pakistan revenue the MoR fee is USD 1,200 [I], below the likely cost of even one registration [H]. Collect adviser quotes before moving off a MoR.

**Ledger effect of a MoR** (so the contributor split stays exact): the sale is recorded with gross = customer price, `tax_minor` = tax the MoR collected and remits (not our liability, `Sale.tax_collected_by = 'mor'`), `fees_minor` = MoR fee, so `net_minor` (the contributor pool base) is what reaches us. `reconcile` must exclude MoR-collected tax from the tax account. Invoices are issued by the MoR; our `Invoice` becomes a mirror with `issuer = 'mor'`. Refunds and chargebacks arrive as MoR webhooks into the existing refund path. MoR payouts to a Pakistani entity may be PayPal only with fees [S]: check before choosing.

### 12.4 Pilot versus full

| | Pilot | Full |
|---|---|---|
| Sales | Pakistan domestic plus business-only abroad by invoice and bank transfer | MoR for card and subscription sales outside Pakistan |
| Tax | `TaxRule` table, decision function, legends, tax-id checks, withholding-aware payment | Filing exports, OSS and UK returns by accountant, e-invoicing |
| Records | 10-year retention | Same |

### 12.5 New tables and endpoints

Tables: `billing.TaxRule`, `billing.WithholdingCertificate`, `compliance.TaxProfile` (buyer or payee tax residency, tax id scheme and value encrypted, validated flag, check reference, form type W-8BEN or W-9 self-declaration date), plus the field additions in 12.2.

| Method and path | Who | Purpose |
|---|---|---|
| GET and POST `/account/tax/` | any user | Tax profile (country, business or consumer, tax id) |
| POST `/account/tax/check/` | any user | Run the id check; stores the reference |
| GET `/staff/tax-rules/`, POST edit | finance, admin | Maintain rules, with audit |
| GET `/staff/tax-report/?month=` | finance | Report by country, mode, rate; CSV |
| POST `/staff/payments/<id>/withholding/` | finance | Record withheld amount and certificate |
| POST `/webhooks/payments/<provider>/` (exists) | gateway or MoR | Extended event types (12.2, section 13) |

### 12.6 Acceptance tests (`backend/billing/tests/test_tax_modes.py`)

- `test_tax_country_is_the_buyers_country_not_the_list_country`
- `test_pakistan_buyer_of_a_pakistan_list_is_charged_the_configured_rate`
- `test_uae_buyer_with_valid_trn_gets_reverse_charge_legend_and_zero_tax`
- `test_uae_trn_that_is_not_fifteen_digits_is_refused`
- `test_indian_buyer_without_gstin_is_blocked_or_sent_to_mor_by_rule`
- `test_gstin_with_bad_checksum_is_refused_and_no_reverse_charge_is_given`
- `test_eu_buyer_with_vies_valid_vat_gets_reverse_charge_and_the_check_reference_is_stored`
- `test_eu_vat_number_that_fails_vies_is_charged_or_blocked_never_reverse_charged`
- `test_uk_vat_number_checked_with_hmrc_and_reference_stored`
- `test_contradicting_country_evidence_blocks_the_order_and_asks_the_buyer`
- `test_order_stores_tax_mode_rate_evidence_and_check_reference`
- `test_invoice_shows_legend_seller_and_buyer_tax_ids_and_credit_note_negates_lines`
- `test_payment_net_of_withholding_settles_the_order_when_amount_plus_withheld_equals_total`
- `test_withheld_amount_is_posted_to_the_withheld_account_and_reconcile_still_agrees`
- `test_missing_withholding_certificate_after_sixty_days_raises_an_alert`
- `test_mor_sale_records_mor_tax_outside_our_tax_account_and_contributor_pool_uses_net`
- `test_mor_refund_event_reverses_the_sale_exactly`
- `test_tax_rule_valid_dates_pick_the_right_rate_on_the_order_date`
- `test_rate_change_never_alters_an_existing_invoice`
- `test_tax_report_totals_by_country_mode_and_rate_equal_the_ledger_tax_account`
- `test_invoices_and_tax_evidence_survive_an_erasure_request_and_are_flagged_legal_hold`
- `test_us_revenue_alarm_at_sixty_percent_of_the_lowest_state_threshold`

---

## 13. C53 Payout compliance, chargebacks and refunds after payout

### 13.1 Payout gate (extends `create_payout` and `approve_payout`)

Order of checks; any failure refuses with a plain reason and writes an `EnforcementAction` when it holds money:

1. Country switch `payouts_on` for the payee's country (new).
2. `PayoutProfile.state == approved` and details unchanged since approval (exists: `kyc_ok`, `details_fingerprint`).
3. Legal name on the profile equals the account holder name on the bank or wallet (new `name_match_state`: exact, near, manual-confirmed). Upwork does the same [S, note 04].
4. Screening clear and newer than the last list version (C45).
5. No open cluster flag (C47).
6. Tax form on file: self-declared tax residency; for Pakistani residents, CNIC or NTN shape (stdnum `pk.cnic`; never stored after check) and filer status from the FBR active list (filer or non-filer changes withholding rates, [S]); for US persons a W-9 self-declaration; for others a W-8BEN style self-declaration (collected through counsel-approved wording).
7. Rail rules: IBAN valid (stdnum `iban`; Pakistan 24 characters [R]); wallet number valid for the wallet; currency rule below.
8. Payable balance above the minimum (exists: 500 minor units) and not negative.
9. New-payee reserve: first payout holds back 20 percent for 60 days or until USD 500 is paid [H], to cover clawbacks.
10. Velocity: more than 3 payout requests in 30 days, a payout above 3 times the payee's 90-day average, or payout details changed in the last 7 days sends to manual review [H].
11. Two-person rule (exists).
12. Withholding computed if the adviser says we are a withholding agent (Pakistan section 153 filer or non-filer rates, reported as 9 and 18 percent for companies and 11 and 22 percent for others [S, low quality, UNVERIFIED]); the deduction is a ledger posting to the `tax` account with a certificate number issued to the payee.

**Currency**: ledger is in USD today; payouts to Pakistan are in PKR. Rate fixed at payout creation and stored (`Payout.fx_rate`, `fx_source`, `local_amount_minor`, `local_currency`); the ledger stays in the sale currency (C52 rule: rate fixed at order, indicative USD only where rates exist [R]).

**Rails**: pilot pays domestic only, by bank transfer or Raast, with the bank reference entered at `mark_paid` (exists). Foreign contributors earn non-cash rewards in the pilot (exists). Full version: Simpaisa-type disbursement API [S] for bank, JazzCash and Easypaisa, with a payout status callback.

### 13.2 Refunds and clawbacks after payout

Today `refund_sale` reverses each release and the sale. If the money was already paid, the contributor's payable balance goes below zero; `payable_balance` then returns a non-positive number and `create_payout` refuses (`amount <= 0`). That is correct by accident, not by design, and there is no record, notice or limit [R, I].

Design:

1. When a refund or chargeback arrives, for each allocation already released: post as today; if the payee's payable balance becomes negative, create a `Clawback` row (user, sale, amount, state open) and an `EnforcementAction` (PAY-03) with a statement.
2. Recovery: net the clawback against future payable earnings automatically; no cash demand in the pilot.
3. Write-off after 12 months with no earnings (finance, two-person), posted to the platform account.
4. Reserve (13.1 item 9) covers new payees.
5. Reconciliation report lists open clawbacks and their age; the existing daily `reconcile` must still agree.

### 13.3 Chargebacks and disputes

Card chargeback windows are 120 days in general, up to 540 for non-delivery [S]. Our hold is 14 days, so a contributor can be paid before a dispute lands. Push payments (bank transfer, Raast, wallets) have no card chargeback, only recall or fraud complaints, so the exposure is card sales only: **keep cards off or on a MoR at the pilot**.

Monitoring thresholds, so the design has a target: Visa excessive-dispute threshold 1.5 percent from 1 April 2026 with USD 8 a dispute fee; Mastercard excessive chargeback 1.5 percent and 100 or more chargebacks in a month [S].

`Dispute` state machine: `opened` (webhook), `evidence_due`, `submitted`, `won`, `lost`, `accepted`. Effects:

- On `opened`: freeze every unreleased allocation of the sale (extend `hold_until`), mark released-and-paid allocations as `at_risk`, write PAY-02 notices only to paid payees, and start a 7-day evidence clock [H].
- Evidence pack (text): order, payment reference, delivery proof (entitlement log, access log counts), invoice, terms accepted and when, contact relay log for outreach orders. For fraud disputes card networks accept stronger "compelling evidence" showing prior undisputed transactions by the same device or account [K, UNVERIFIED].
- On `won`: release freeze. On `lost`: post as a refund (reuse `refund_sale`), add a `dispute_fee` posting to the `fees` account, create clawbacks as in 13.2. On `accepted`: same as lost.
- Extend `handle_webhook`: it currently returns "ignored" for any status other than `succeeded` [R]. Add event types `refund`, `dispute_opened`, `dispute_won`, `dispute_lost`, each idempotent on `event_id`.

Refunds outside cards: a refund on a push payment is a payout out; it goes through the same two-person rule as a payout and records the bank reference in a `RefundPayment` row.

### 13.4 Data fields

`Clawback`: user, sale, amount_minor, currency, state (open, recovered, written_off), opened_at, recovered_at, note. `Dispute`: order, payment, provider, provider_ref, amount_minor, fee_minor, reason, state, due_by, evidence_text, opened_at, decided_at. `PayoutReserve`: user, amount_minor, release_on, state. `RefundPayment`: order, rail, reference, amount_minor, created_by, approved_by. `PaymentRail`(code, country, direction, name_match_required, auto_confirm, chargeback_possible, fee_note). `BankStatementLine`(account_label, ts, amount_minor, currency, reference_text, counterparty_name_enc, matched_order fk, state): staff import a bank CSV and the matcher looks for `Order.ref` in the reference text (pilot reconciliation for manual rails). Add to `PayoutProfile`: `name_match_state`, `filer_status`, `tax_residency`. Add to `Payout`: `fx_rate`, `local_amount_minor`, `local_currency`, `rail`, `withheld_minor`, `certificate_no`.

### 13.5 Tools, licence, cost

Own code. stdnum `iban` (LGPL-2.1+) [R]. A disbursement aggregator (Simpaisa or similar) priced on request [S]. Cost in the pilot: USD 0 plus bank fees for each transfer.

### 13.6 Country notes

Pakistan: bank (IBAN, 24 characters), Raast, Easypaisa and JazzCash wallets (section 5.3); filer versus non-filer affects withholding [S]. UAE: IBAN 23 characters [R]; Emirates ID not collected. India: no IBAN, bank account plus IFSC [K]; TDS and PAN needed for any Indian payee if a withholding duty applies [K, UNVERIFIED]. UK and EU: IBAN; no withholding by us on contributors; EU DAC7 platform reporting may apply to us as a platform operator [K, UNVERIFIED]. US: W-9 or W-8BEN; the 1099-NEC threshold is USD 2,000 for 2026 and binds US payers [S].

### 13.7 Pilot versus full

| | Pilot | Full |
|---|---|---|
| Rails | Bank transfer and Raast, domestic only, manual with reference | Aggregator API for banks and wallets |
| Gate | Items 1 to 8, 11 | All 12 |
| Chargebacks | Cards off or on MoR; clawback record and dispute table exist | Webhooks, evidence pack, reserve |
| Withholding | Adviser's answer, config flag | Automatic with certificates |

### 13.8 New tables and endpoints

Tables: `ledger.Clawback`, `billing.Dispute`, `ledger.PayoutReserve`, `billing.RefundPayment`, `billing.PaymentRail`, `compliance.BankStatementLine`; fields on `PayoutProfile` and `Payout`.

| Method and path | Who | Purpose |
|---|---|---|
| GET `/staff/clawbacks/`, POST `.../<id>/write-off/` | finance (two people) | Review and write off |
| GET `/staff/disputes/`, POST `.../<id>/submit-evidence/` | finance | Work disputes |
| POST `/staff/bank-statements/import/` | finance | CSV import and match |
| POST `/staff/refunds/<order>/pay/`, `/approve/` | finance (two people) | Cash refund on push rails |
| GET `/account/payout/` (exists) | payee | Adds tax form, name match status, reserve, clawbacks |
| POST `/webhooks/payments/<provider>/` (exists) | gateway | New event types |

### 13.9 Acceptance tests (`backend/ledger/tests/test_payout_compliance.py` and `backend/billing/tests/test_disputes.py`)

- `test_payout_refused_when_country_switch_payouts_is_off`
- `test_payout_refused_when_legal_name_and_account_holder_name_do_not_match`
- `test_payout_refused_with_open_screening_hit`
- `test_payout_refused_with_open_cluster_flag`
- `test_payout_refused_without_tax_residency_declaration`
- `test_pakistan_payee_cnic_shape_checked_and_not_stored`
- `test_invalid_pakistan_iban_is_refused`
- `test_first_payout_holds_back_twenty_percent_for_sixty_days`
- `test_payout_details_changed_in_last_seven_days_goes_to_manual_review`
- `test_payout_above_three_times_ninety_day_average_goes_to_manual_review`
- `test_fx_rate_is_fixed_at_payout_creation_and_stored`
- `test_withholding_posts_to_the_tax_account_and_issues_a_certificate_number`
- `test_refund_after_payout_creates_a_clawback_and_a_notice`
- `test_clawback_is_netted_against_the_next_payable_earnings`
- `test_negative_payable_balance_never_allows_a_new_payout`
- `test_clawback_write_off_needs_two_people`
- `test_reconcile_agrees_after_refund_after_payout_with_open_clawback`
- `test_dispute_opened_freezes_unreleased_allocations_and_marks_paid_ones_at_risk`
- `test_dispute_lost_reverses_the_sale_posts_the_fee_and_creates_clawbacks`
- `test_dispute_won_unfreezes_the_hold_and_changes_no_balance`
- `test_webhook_dispute_events_are_idempotent_and_signature_checked`
- `test_unknown_webhook_event_type_is_logged_and_returns_200_ignored`
- `test_cash_refund_on_a_bank_transfer_order_needs_a_second_approver_and_a_bank_reference`
- `test_bank_statement_import_matches_order_ref_and_flags_amount_differences`
- `test_property_total_cash_out_never_exceeds_collections_with_refunds_chargebacks_and_clawbacks`

---

## 14. C55 Right to erasure across derived copies

### 14.1 Inventory of every copy of an entry's data [R unless marked]

| ID | Copy | Holds personal data? | Cleared by `execute_erasure` today? | Needed step |
|---|---|---|---|---|
| D01 | `Entry` row (name, description, address, website, lat, lon, addons) | yes | yes (tombstone) | keep |
| D02 | `Contact`, `Social`, `NameVariant` | yes | yes (deleted) | keep |
| D03 | `Service`, `Product`, `Speciality`, `Branch` (address, coordinates), `Equipment`, `Hours`, `AreaServed`, `Identifier` (registration number, register URL) | yes for individuals and sole traders | **no** | delete or blank for the entry |
| D04 | `ValueMeta.evidence_text`, `VerificationEvent.evidence_text`, `Claim.evidence_text` | may quote names, numbers | **no** | blank text, keep the event and level (the check history stays, minus the text) |
| D05 | `Report.text`, `Report.reporter_contact_enc` about the entry; `Enquiry.text`, `reply_to_enc`; `OutboxMessage.body` | yes (third party and the entry's contacts) | **no** | purge text where the entry is the subject; keep counts |
| D06 | `ImportRow.raw`, `ImportRow.normalised`, `ImportBatch.raw_text`, `ExternalRecord` | yes (full uploaded text) | **no** | null the row; purge `raw_text` after publish plus 30 days (BU-14 retention) |
| D07 | Agent drafts: `raw`, `evidence_quotes`, `source_urls` | yes | **no** | null on erasure |
| D08 | `DedupeCandidate.features` | may hold folded names | **no** | clear |
| D09 | `ConsentRecord` (append-only) | proof of consent and withdrawal | no | keep minimal proof (entry uid, status, timestamps, method); no name |
| D10 | `analytics.RollupCell` counts | aggregate only | no | recount; no personal data |
| D11 | Extract files and `TraceEntry`; buyers' copies | yes (names, addresses) | **no** | notify and suppression feed (14.3 step 5) |
| D12 | Search index. Pilot: Postgres queries over D01, so erasing D01 erases it. S3: Meilisearch or OpenSearch copy | yes | not covered | delete by uid and verify |
| D13 | Shared page caches at the edge: entry page and every list page showing the entry (`s-maxage` with ETag from template, data and cell stamp [R]); sitemap files | yes | not covered | purge by tag (14.3 step 4) |
| D14 | Application and web logs (URLs carry names), error tracker | partly (log scrubber strips contacts [R]) | n/a | retention 30 days |
| D15 | Database backups, off-site copies, replicas | yes | not covered | 35-day window and restore replay (14.3) |
| D16 | Processor logs: email and messaging providers | yes (message bodies, recipient) | n/a | provider retention setting; request deletion where needed |
| D17 | Search engines' own caches | yes | n/a | removal request tool (manual) [K, UNVERIFIED] |
| D18 | `AuditLog` (append-only hash chain) | must be **no** | n/a | policy and test: payloads carry uids and codes only |
| D19 | Invoices, orders, tax evidence (`Order.billing`, `Invoice.buyer`) | yes (buyer name, address, tax id) | no | retain under legal obligation, fenced off |
| D20 | Account holder data (Profile, social identities) | yes | separate flow `delete account` exists [R] | link the two flows |

### 14.2 Why backups need a rule

Erasure applies to backups as well as live systems unless an exemption applies; the ICO accepts putting data "beyond use" until it is overwritten on a schedule if the controller will not use it for any decision, gives no one else access, keeps it secure, and commits to delete it when possible; and the person must be told clearly what happens to backups [S, ICO guidance as summarised]. Repo today [R]: `scripts/backup.sh` writes a nightly `pg_dump` and keeps 14 daily and 8 weekly dumps, so a backup can be up to about 56 days old (plus any off-site copy, which the script comments say you must make). `docs/runbooks/restore.md` restores and verifies the audit chain and the ledger but does not re-apply erasures.

### 14.3 Erasure procedure

**Statement of backup retention (published in the privacy notice and sent to the requester):** "We remove your data from the live service within 1 day of confirming your request and finish clearing our systems within 30 days. Encrypted backups made before your request may still hold your data for up to 35 days. They are kept only to recover from a disaster. We do not read them or use them for any other purpose, we do not give anyone access to them, and if one is ever restored we remove your data again before the service reopens."

**Backup change (decision for founder, default yes):** keep 14 daily and 5 weekly dumps (35 days maximum age, replacing 14 and 8 which is up to 56 days); apply the same 35-day expiry to every off-site copy (`find ... -mtime +35 -delete` or the object-store lifecycle rule); no monthly or yearly archives of personal data. Cost: you lose recovery points older than 35 days; for a directory whose live data is re-derivable that is acceptable at the pilot [H]. At S2 move to pgBackRest (MIT [S]) with retention set to expire full, differential and WAL at the same 35 days; WAL archive retention must also be at most 35 days, or the window is longer than stated.

**Timeline** (statutory one month is the repo's own `ERASURE_DAYS = 30` [R]):

| Step | When | Who | What |
|---|---|---|---|
| 0 | Day 0 | Anyone | "Remove my data" opens a `Takedown` (exists) |
| 1 | Day 0 to 2 | Moderator | Identify the person: a one-time code through the platform to a contact on the entry (exists in the runbook). Check exemptions (legal obligation such as invoices and tax records; legal claims). Decide: erase or refuse with a written reason (exists) |
| 2 | Same day | System | `execute_erasure` tombstone and suppression (exists), widened to D03 to D08 (14.4) |
| 3 | Within 1 hour of step 2 | Job | **Search index**: delete document by uid; for Meilisearch wait for the task to report success (deletion is asynchronous [S]); for OpenSearch force-merge to expunge deletes later [K]; then query the name and confirm zero hits. In the pilot the index is Postgres, so step 2 already did this and the check still runs |
| 4 | Within 1 hour | Job | **CDN purge**: shared pages carry `Cache-Tag: entry:<uid>` for the entry page and for each of the up to 25 rows on a list page (header size about 700 bytes [I]); purge by tag `entry:<uid>`. Purge by tag is available on every Cloudflare plan since April 2025, 5 requests a minute on free, bucket of 25 [S]; at 274 erasures a day that is far below the limit [I]. Batch size per call not confirmed. Also purge the sitemap shard containing the entry URL and regenerate it |
| 5 | Within 7 days | Job and finance | **Extracts**: look up `ExtractMember` (new) for extracts containing the entry. Each extract licence says buyers must apply a monthly **suppression feed** (a file of keyed hashes of erased entries, no personal data) and delete listed records; buyers of extracts made in the last 12 months get the feed. Planted trace entries are not affected |
| 6 | Within 7 days | Job | **Staging and drafts**: blank D06 and D07 rows for the entry; schedule `ImportBatch.raw_text` purge at publish plus 30 days; clear D08 |
| 7 | Within 7 days | Moderator | **Processors**: ask the email and messaging providers to delete logs for the entry's contact hashes where their retention is longer than 30 days (D16); record the answer |
| 8 | Within 30 days | Job | Logs older than 30 days are gone by schedule (D14); confirm |
| 9 | Day 0 + 35 | Backup rotation | Every backup that could hold the data has expired; record `backups_clear_on` on the takedown at step 2 |
| 10 | Day 0 | System | Add the erasure to the `ErasureLog` (hash only) kept indefinitely |
| 11 | On any restore | Operator | **Replay**: `manage.py replay_erasures --since <backup timestamp>` re-runs steps 2 to 4 for every erasure recorded after the backup was taken; the restore runbook gets a mandatory step 5a: do not reopen the service until the replay reports zero differences |
| 12 | Day 0 | System | Page for the erased URL returns **410 Gone** with no name (not 404, not a soft page); search engines drop it faster [K]. Optional: request removal from search engines [K, UNVERIFIED] |
| 13 | Day 0 to 30 | Moderator | Send the requester a written confirmation listing each copy, its status, and `backups_clear_on` |

`ErasureStep` rows track each step (takedown fk, step code, state pending or done or failed, detail, done_at). The job is idempotent and resumable: a failed step retries and shows red on the staff Takedowns queue. A takedown cannot be marked `done` until steps 2 to 8 are `done`.

**Not erased, by design, with the reason stored:** invoices, credit notes, order and tax evidence (legal obligation, 10 years, fenced from all other use); the hash-chained audit log (it must contain no personal data); the suppression list and `ErasureLog` (hashes only, they exist to stop re-import); minimal consent proof (D09).

**Optional extra not adopted:** cryptographic erasure of backups by destroying old key versions would shred the encrypted contact columns in old dumps but not plain names or addresses, so it does not replace the 35-day window.

### 14.4 Code change to `execute_erasure` (design)

Wrap it in the step framework; add deletion or blanking for D03 to D08; make the purge idempotent; take a `scope` argument (`entry`) so a later `person` scope can erase across many entries by contact hash (needed when one phone appears on 50 entries: the suppression already works by hash, the sweep must find all entries by `Contact.value_hash` before deleting). For D03 on business entries (not individuals), the founder may choose to keep non-personal services and products; default: erase for individuals and child-facing types, keep for businesses where the request names only the person's details [H].

### 14.5 Country notes

GDPR and UK GDPR: erasure on request, with notice to recipients, one month [K, UNVERIFIED here; the ICO page was summarised in search only]. India: DPDP rights phased in from the November 2025 rules (note 03) [S]. UAE PDPL: erasure right in article 15 [K, UNVERIFIED]. Pakistan: no enacted data protection law as of May 2026 per note 03, but PECA takedown orders can arrive; the same procedure serves both. US: state rights apply to consumers above thresholds and may not reach B2B listings [K, UNVERIFIED]. Counsel per country before the switch is on.

### 14.6 Pilot versus full

| | Pilot | Full |
|---|---|---|
| Steps | 2, 3 (Postgres), 4 (when CDN on), 5, 6, 7, 9 to 13; backups at 35 days | Index engine, CDN tag purge job, extract feed automation, pgBackRest |
| Copies | D01 to D08, D11, D13, D15 | All |
| Tests | Section 14.8 | Same plus index engine tests |

### 14.7 New tables and endpoints

Tables: `compliance.ErasureStep`, `compliance.ErasureLog` (subject_hash, entry_uid, erased_at, scope, backups_clear_on), `compliance.ExtractMember` (extract fk, entry_uid, country; no personal values), `compliance.DerivedCopy` (registry of copy types: code, description, owner, purge_function, verify_function, retention_days) so a new copy cannot be added without a purge function (a test fails otherwise), `compliance.SuppressionFeed` (period, file_sha256, count, sent_to).

| Method and path | Who | Purpose |
|---|---|---|
| GET `/staff/takedowns/` (exists) | moderator | Add step status columns |
| POST `/staff/takedowns/<id>/retry/<step>/` | moderator | Retry a failed step |
| GET `/staff/erasure-feed/`, POST `.../build/` | admin | Build and log the suppression feed |
| management commands `replay_erasures`, `purge_staging`, `build_suppression_feed` | job, operator | As above |
| GET `/<erased-path>/` | public | 410 Gone |

### 14.8 Acceptance tests (`backend/moderation/tests/test_erasure_copies.py`, `backend/compliance/tests/test_erasure_restore.py`)

- `test_erasure_blanks_services_products_branches_equipment_hours_and_identifiers`
- `test_erasure_blanks_evidence_text_on_checks_claims_and_reports_and_keeps_the_levels`
- `test_erasure_nulls_import_rows_agent_drafts_and_dedupe_features_for_the_entry`
- `test_staged_import_text_is_purged_thirty_days_after_publish`
- `test_search_backend_returns_zero_hits_for_the_erased_name_on_both_implementations`
- `test_memory_and_model_search_backends_delete_by_uid`
- `test_erasure_issues_a_cache_tag_purge_for_the_entry_and_every_list_page_that_showed_it`
- `test_sitemap_shard_no_longer_lists_the_erased_url`
- `test_erased_entry_page_returns_410_with_no_name`
- `test_extract_members_found_and_suppression_feed_contains_only_hashes`
- `test_takedown_cannot_be_marked_done_until_steps_two_to_eight_are_done`
- `test_failed_step_is_retried_and_shows_red_in_the_queue`
- `test_erasure_is_idempotent_when_run_twice`
- `test_erasure_by_contact_hash_finds_all_entries_sharing_the_phone`
- `test_erasure_log_stores_hash_and_uid_only`
- `test_backups_clear_on_is_thirty_five_days_after_the_erasure`
- `test_backup_script_keeps_fourteen_daily_and_five_weekly_dumps_only`
- `test_replay_after_restore_re_erases_entries_erased_after_the_backup_was_taken`
- `test_restore_runbook_check_fails_if_replay_reports_a_difference`
- `test_audit_payloads_never_contain_names_phone_numbers_emails_or_ids`
- `test_orders_invoices_and_tax_evidence_remain_after_erasure_and_are_flagged_legal_hold`
- `test_every_registered_derived_copy_has_a_purge_and_a_verify_function`
- `test_confirmation_letter_lists_each_copy_status_and_backups_clear_on`
- `test_erasure_does_not_touch_other_entries_that_share_a_name`

---

## 15. Pilot minimum versus full, in one table

| Challenge | Pilot minimum (Pakistan, one city, one trade, manual rails) | Full version | Cost at pilot |
|---|---|---|---|
| C43 | Format checks, moderator registry lookup, six signals, one queue, 20 planted fakes | Adapters, all signals, Splink, weekly graph | USD 0 |
| C44 | L0 to L2 by hand, OTP, bank name match, surveyor | Vendor-hosted KYB, L3, expiry job, DSA view | USD 0 (or Didit free tier [S]) |
| C45 | Six government lists, rapidfuzz, two-person review, payout and L2 gate | PEP data under licence, blocking, yente | USD 0 |
| C46 | Feature off; report fake works | Reviews on per list type with burst and similarity checks | USD 0 |
| C47 | Turnstile, honeypot, disposable list, email normalisation, SQL cluster on phone and payout fingerprint | Full graph, ladder automation | USD 0 |
| C50 | Reason codes and spine on existing decisions, appeal form, 14-day target | Transparency page, SLA timers | USD 0 |
| C51 | `TaxRule`, decision function, B2B-only abroad, withholding-aware payment, 10-year records | MoR for card and subscription outside Pakistan, filing exports, e-invoicing | Accountant (unpriced) |
| C53 | Gate items 1 to 8 and 11, domestic rails, clawback and dispute tables, cards off | Aggregator API, reserve, velocity, withholding automation | Bank fees |
| C55 | Step framework, D03 to D08 fixed, 35-day backups, restore replay, 410 pages | Index engine, CDN tag job, extract feed automation, pgBackRest | USD 0 |

---

## 16. Requirements (house style): ID, priority, status against the repository

Priority: P0 before first real money or first paid listing; P1 before the first paying market opens; P2 later. Status: built, partly, not built.

| ID | Requirement | Pri | Status |
|---|---|---|---|
| TM-01 | Reason codes and enforcement log for every adverse action | P0 | not built |
| TM-02 | Statement of reasons emailed with each action | P0 | not built |
| TM-03 | Appeal form, second reviewer, 14-day target | P0 | not built |
| TM-04 | Transparency counts page | P2 | not built |
| TM-05 | Registry-number format checks (CNIC, GSTIN, PAN, UK VAT, EU VAT, IBAN; own checks for CUIN, NTN, STRN, TRN) | P0 | not built (stdnum not in `requirements.txt`) |
| TM-06 | Registry check record and moderator queue | P0 | not built |
| TM-07 | Supplier risk score with six pilot signals | P1 | not built |
| TM-08 | Planted fake suppliers and recall measure | P1 | partly (`CanaryEntry` is for surveyors) |
| TM-09 | Business profile with levels L0 to L2 | P0 | partly (claims, supplier verification for campaigns) |
| TM-10 | Vendor-hosted KYB at L3 | P2 | not built |
| TM-11 | DSA article 30 trader view behind a country flag | P2 | not built |
| TM-12 | Sanctions lists fetched daily and screening gate on payouts and L2 | P0 (before first payout) | not built |
| TM-13 | PEP question at payout KYC | P0 | not built |
| TM-14 | PEP data under licence | P2 | not built |
| TM-15 | Review model, eligibility and one per user | P1 | not built |
| TM-16 | Review burst, similarity and link checks | P2 | not built |
| TM-17 | Signup Turnstile, disposable-email block, email normalisation | P1 | partly (honeypot only) |
| TM-18 | Account signal table and weekly cluster job | P1 | not built |
| TM-19 | Phone uniqueness for phone proof | P1 | not built |
| TM-20 | Tax decision function and `TaxRule` | P0 (before first real sale) | not built (flat rate by list country) |
| TM-21 | Buyer tax-id validation and check reference | P0 | not built |
| TM-22 | Withholding-aware payment and certificate tracker | P1 | not built (exact amount required) |
| TM-23 | MoR integration | P1 | not built |
| TM-24 | 10-year retention of invoices and tax evidence | P0 | partly (rows are never deleted; no policy or flag) |
| TM-25 | Payout gate items 1 to 8 | P0 | partly (KYC, fingerprint, minimum, two-person built) |
| TM-26 | Clawback record and notice | P0 | not built (negative balance by accident) |
| TM-27 | Dispute table and webhook event types | P1 | not built (webhook ignores non-success) |
| TM-28 | New-payee reserve and velocity checks | P1 | not built |
| TM-29 | Bank statement import and match | P0 for manual rails | not built |
| TM-30 | Erasure step framework with registry of derived copies | P0 | not built |
| TM-31 | Erasure widened to D03 to D08 | P0 | partly (D01, D02 only) |
| TM-32 | Search and CDN purge on erasure | P1 | not built (index is Postgres now; CDN not yet used) |
| TM-33 | Extract suppression feed | P1 | not built |
| TM-34 | Backups 35 days and restore replay | P0 | not built (56 days, no replay) |
| TM-35 | 410 page for erased entries | P1 | not built (404 or tombstone page) |
| TM-36 | Audit payloads free of personal data, enforced by test | P0 | partly (current payloads are uids and codes; no test) |

---

## 17. Gaps and conflicts

| Item | Detail |
|---|---|
| Text-only rule versus KYB documents | Rule 3 forbids images on the public product; KYB needs documents. Resolved by vendor-hosted flows (only verdict and reference come back). If the founder wants documents on our side, that is a new private-store decision. |
| Four check labels versus trust tiers | KYB levels and risk bands are internal. They never appear as labels and never change one. |
| "Only a platform" position (note 03) | Enforcement, reviews and detectors are our own acts and make us look more like an operator; that is consistent with note 03's recommended wording, not a reason to skip them. |
| Backups 56 versus 35 days | Current script is 56 days. Shortening costs recovery points; the 35-day figure is a proposal [H]. |
| Pakistan digital tax sources conflict | 2025 tax scrapped; 2026 proposals reported both as enacted social-media withholding and as proposals for a foreign-vendor tax [S]. Needs an adviser and the Finance Act text. |
| Paddle acceptable use | A search summary says advertising and sponsorship are excluded; the page was blocked and I found nothing on data lists. Ask in writing before building a MoR adapter. |
| Orders carry the list's country | Tax uses the list country. A UAE buyer of a Pakistan list is taxed as Pakistani today. Fix before any non-Pakistan buyer. |
| Hold 14 days versus 120-day card window | Cards only; mitigated by keeping cards off or on a MoR. |
| GitHub licence files | None read. Wheel licences only. Re-check on GitHub with `add_repo` before adoption (plan 2.2 rule). |
| Not researched | Pakistan withholding on contributor payouts (rates cited are low quality), UAE trade licence number formats, India CIN access, EU DAC7 for contributors, UAE and Pakistan fake-review rules, Pakistan data law status in 2026. |

---

## 18. Open decisions for the founder, with suggested defaults

| # | Decision | Suggested default |
|---|---|---|
| 1 | Operating entity country (decides tax registration, banks, MoR payouts) | Decide with counsel and an accountant before any tax feature beyond the rule table; Pakistan company for Pakistan domestic sales, revisit for an overseas entity if Stripe-type tools are wanted |
| 2 | Outside Pakistan in the pilot | Businesses with a valid tax id only, by invoice and bank transfer; no consumer sales; no card sales until a MoR is chosen |
| 3 | MoR choice and timing | Choose before the first card or subscription sale to the UK, EU, India or the US; get written answers on acceptable use (ads, rank, data lists) and on payouts to a Pakistani entity from Paddle, Lemon Squeezy or Stripe Managed Payments, Polar, Dodo |
| 4 | Cards in the pilot | Off |
| 5 | Backup window | 35 days (14 daily, 5 weekly), restore replay mandatory |
| 6 | Reviews | Off in the pilot; on per list type after traffic |
| 7 | KYB documents | Vendor-hosted only; nothing stored on our side |
| 8 | Sanctions lists and data | Free government lists now; ask OpenSanctions for a quote before S2 |
| 9 | Spend above which L2 is required | USD 500 in 12 months |
| 10 | New-payee reserve | 20 percent for 60 days or USD 500 paid |
| 11 | Foreign contributors | Non-cash rewards only until counsel clears cross-border payouts |
| 12 | Withholding on contributor payouts | Ask the accountant whether we are a withholding agent; config flag meanwhile |
| 13 | Appeal period and SLA | 180 days to appeal, 2 days acknowledge, 14 days decide |
| 14 | Erasure for D03 on business entries | Erase for individuals and child-facing types; keep non-personal services and products for businesses unless the request covers them |
| 15 | Device id cookie | First-party random id after the cookie choice; no fingerprinting library |

**Suggested decision-log text** (for `docs/DECISIONS.md`, not added by me): "Trust, money and legal designs for C43 to C47, C50, C51, C53 and C55 are recorded in `research_notes/Scale research/08_trust_money_legal_solutions.md`. Defaults in force until changed: outside Pakistan sell to verified businesses only, by invoice, no card sales before a merchant of record is chosen; sanctions screening uses free government lists and gates payouts; reviews stay off in the pilot; backups are kept 35 days and any restore replays the erasure log; every adverse action writes a reason code and a statement of reasons and can be appealed."

---

## 19. Sources

Repo [R]: `docs/DECISIONS.md`; `research_notes/Scale research/03_capabilities_and_skills_matrix.md`; `research_notes/Platform requirements/01` to `04`; `backend/billing/{models,services,reconcile,reporting,views}.py`; `backend/ledger/{models,services}.py`; `backend/accounts/{models,roles,throttle}.py`; `backend/moderation/{models,services,privacy}.py`; `backend/entries/models.py`; `backend/outreach/models.py`; `backend/intake/models.py`; `backend/analytics/{models,extracts}.py`; `backend/config/urls.py`; `backend/catalog/urls.py`; `scripts/backup.sh`; `docs/runbooks/{restore,takedown-request,payout-cycle,breach-response}.md`.

Package files read [R] (scratch download, unpacked, nothing run): python_stdnum-2.2, rapidfuzz-3.14.6, splink-5.0.0, datasketch-2.0.0, networkx-3.6.1, django_axes-8.3.1, phonenumbers-9.0.40, nomenklatura-4.17.0 wheels from PyPI.

Web search summaries [S], all UNVERIFIED (pages not opened; WebFetch was blocked): OpenSanctions licensing and yente (opensanctions.org); OFAC SDN downloads (sanctionslist.ofac.treas.gov); Paddle fees and policy (paddle.com support pages, FTC press release of June 2025, MoFo note); Lemon Squeezy and Stripe Managed Payments (dodopayments.com, learnwithhasan.com comparisons); Pakistan digital presence tax (Profit, Arab News, regfollower, bolnews, orbitax, phoneworld); Finance Act 2026 (pakobserver, nukta, paktaxcalculator, digitalpakistan); Pakistan section 152 and 153 (KPMG budget briefs, fbr.gov.pk, ettc.pk); Pakistan provincial sales tax (vatcalc, Kintsugi); SECP CUIN and eServices (businessdataguide, lemreveal, org-id.guide); FBR ATL verification (ict.edu.pk, zameen.com); Raast P2M (Business Recorder, APP, SBP circular, Tribune); Easypaisa, JazzCash disbursement (simpaisa.com); Stripe in Pakistan (learnwithhasan.com, Profit); UAE VAT and e-invoicing (numeral, Kintsugi, alphapartners, stackcue); UAE licence checks (u.ae, ADDED TAHAQAQ, aiprise, bestaxca); UAE targeted financial sanctions (ADGM guides, crowe.com, castellum.ai); India OIDAR (india-briefing, BDO India, taxguru, businessworld); India TDS 194-O (taxguru, tax2win); UK VAT for non-UK digital sellers (Stripe, Quaderno, vatcalc, Anrok); HMRC VAT API and Companies House limits (tax.service.gov.uk, developer-specs.company-information.service.gov.uk); EU OSS (taxdoo, Stripe docs, vat-one-stop-shop.ec.europa.eu, hellotax, Belgian finance site); FTC fake review rule (Olshan, Morgan Lewis, DWT, etcentric); UK DMCC fake reviews (Which?, CMS, Ashurst, A&O Shearman); DSA articles 17, 19, 20, 21 and 30 (presencis, springlex, streamlex, Mondaq, CCPC, Pinsent Masons, Freshfields); India e-commerce rules and IS 19000:2022 (moneylife, Inc42, iasgyan, LiveLaw); Visa VAMP and Mastercard ECM (fraud.net, chargeflow, chargebacks911, chargeback.io, redo.com); ICO erasure and backups (ico.org.uk and secondary summaries); Cloudflare purge (developers.cloudflare.com changelog 2025-04-01, blog); Meilisearch, Typesense, OpenSearch licences (meilisearch.com docs, comparisons, Wikipedia); pgBackRest and WAL-G (pgbackrest README, pkg.go.dev); KYC vendor pricing (didit.me, costbench, signzy); Turnstile (developers.cloudflare.com, prosopo.io); disposable-email-domains (GitHub topic pages); Pwned Passwords (troyhunt.com); US 1099 thresholds and W-8BEN (patriotsoftware, cpapracticeadvisor, beancount.io); US state sales tax on SaaS (Pillsbury, getsphere, beancount.io); Pakistan proscribed persons (nacta.gov.pk, opensanctions.org dataset page, dawn.com); UK Sanctions List (gov.uk, opensanctions.org); FingerprintJS licence (fingerprint.com blog).
