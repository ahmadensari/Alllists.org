# 03. The rule "we are only a platform; providers are legally responsible"

Not legal advice. Prepared 2026-10-06 from `docs/DECISIONS.md`, `reports/Which lists pay.md`, and standard web searches. Items marked UNVERIFIED come from memory or a search summary and must be checked by counsel. English only.

## 1. The proposed rule

"This is only a platform where data is loaded and sold by the providers, not us. So the legal responsibility is of the providers, not ours."

## 2. Verdict: CHANGE it. Do not adopt it as written.

Keep the first half as a design aim (we host what providers submit). Drop the second half as a legal position. Replace it with:

> "AllLists hosts data that providers submit and warrant. We act on notices promptly. For the parts of the service we design, run or sell ourselves (agent-drafted entries, ranking, subscriptions, extracts, contributor payments, outreach), we accept responsibility as an operator."

Why, in short:

1. Safe harbours protect hosting of third-party content from liability for that content. They do not protect our own acts (selling, ranking, drafting, paying).
2. Data protection law (GDPR and its cousins) does not recognise the safe harbour. A platform can be controller or joint controller of personal data that users upload.
3. The repo's own design makes AllLists look like a data business, not a neutral host. Agents draft entries, the platform sets prices, sells subscriptions and extracts, pays contributors from sales, and runs outreach. Each of these weakens the "only a platform" claim.
4. Even where a provider is liable, that does not remove ours. Liability is usually shared, and a provider in Pakistan or the Gulf may be unreachable or insolvent. An indemnity is only as good as the indemnifier.

The rule can hold in a narrow form: for business facts a provider (owner or importer) supplied about itself or its own list, under a warranty, with notice-and-takedown, and where we did not draft, rank, pay for, or rewrite that content. It cannot hold for agent-filled data, extracts, or personal data.

## 3. Regime by regime (what is true, and the catch for AllLists)

| Regime | What it gives | What removes it or limits it | AllLists catch |
|---|---|---|---|
| US, Section 230 | Immunity for third-party content; no duty to monitor | Does not apply to content we help create or develop (material-contribution test, Roommates.com); federal criminal law and IP are carved out | Agent-drafted entries are our content. Paid contributors, templates that require fields, and ranking blur the line. Source: [CDT on 230 and generative AI](https://cdt.org/insights/section-230-and-its-applicability-to-generative-ai-a-legal-analysis/) |
| US, DMCA 512 | Safe harbour for copyright claims on user content | Needs registered agent, notice-and-takedown, repeat-infringer policy, no direct financial benefit with right and ability to control (UNVERIFIED detail) | Database and licensed-source copyright (Overture, Foursquare, registers) is a real issue; sales of extracts are direct financial benefit |
| EU, DSA (and e-Commerce Directive hosting rules) | Hosting exemption if no actual knowledge and expeditious removal on notice; notice-and-action, statements of reasons, trader traceability (Art. 30 for marketplaces; UNVERIFIED applicability to a B2B directory) | Lost when the platform plays an "active role" with knowledge or control over the data (CJEU L'Oreal v eBay line) | Ranking, editing and enriching are active-role risks |
| EU, GDPR | None. Hosting exemption does not override GDPR | Platform becomes controller or joint controller by influencing purposes and means | CJEU Russmedia (C-492/23, 2 Dec 2025): a marketplace operator is a (joint) controller of personal data in user ads and cannot hide behind the hosting exemption. Sources: [Mondaq](https://www.mondaq.com/ireland/data-protection/1721724/gdpr-liability-of-online-marketplaces-for-user-published-advertisements), [Greenberg Traurig](https://www.gtlaw.com/en/insights/2026/2/cjeus-russmedia-decision-expands-platform-controller-duties-under-gdpr). Our lists of sole traders, doctors, tutors are personal data. Selling contact data for a fee makes us a controller beyond doubt |
| UK | Hosting defence under retained e-Commerce rules and Defamation Act s5 (website operator defence, needs poster identifiable or notice procedure; UNVERIFIED); Online Safety Act duties for user-to-user services | UK GDPR and PECR apply like the EU; the ICO treats sole-trader details as personal data | See `reports/Which lists pay.md` (ICO B2B marketing note) |
| India, IT Act s79 and IT Rules 2021 | Conditional safe harbour: no initiating, selecting or modifying; due diligence, grievance officer, takedown on court or government order or notice within set times | Lost if we initiate, select receiver, or modify content, or fail due diligence | Agents drafting entries and us ranking is "modifying or selecting". DPDP Act and Rules (Nov 2025, phased in) make us a data fiduciary for personal data we decide the purpose of. Source: [search summary on s79](https://laex.in/?p=13903). Interaction with DPDP not confirmed in search |
| Pakistan, PECA 2016 and 2025 amendment | Historically some intermediary relief (UNVERIFIED section numbers); new Social Media Protection and Regulatory Authority can order blocking and removal | A reported September 2025 amendment proposal would end the exemption for ISPs, hosts and platforms (UNVERIFIED whether enacted). No enacted data protection law as of May 2026 (per our report) | Our first market has the least certain safe harbour and broad takedown powers. Plan for takedown on order, local entity and local representative. Source: [ARY summary](https://arynews.tv/peca-amendment-act-2025-the-key-points/) |
| UAE | Federal PDPL (Decree-Law 45/2021) applies to controllers and processors; e-commerce and cybercrime laws impose removal duties; free-zone regimes (DIFC, ADGM) have their own data law (all UNVERIFIED) | No general safe harbour known to me; executive regulations of PDPL had been delayed (UNVERIFIED) | Treat as controller exposure; counsel needed on directory sales and unsolicited messaging |

Common thread: hosting protection is conditional, narrow, and absent for data protection. "The provider is responsible" is not a defence anywhere I checked.

## 4. What keeps protection, and what removes it (applied to this repo)

| Keeps protection | Removes protection | Where the repo stands |
|---|---|---|
| Notice-and-takedown with fast, logged action | Ignoring notices, slow action | Built: reports, takedown and erasure with tombstones, global suppression list |
| No editorial role: show what was submitted | Editing, enriching, ranking, curating, merging | Merge service, dedupe, checks, "sponsored" slots, ranking all exist. Mixed |
| Terms of use, provider warranties and indemnity | None, but weak alone | Rights declaration on add form exists. Need contract-grade terms (see requirements) |
| Provider identification (KYC) | Anonymous providers | Accounts and payout details exist. No provider KYC for sellers of lists yet |
| Record keeping (who, when, source, licence, consent) | Missing provenance | Strong: source, licence, date, consent, hash-chained audit log |
| Provider, not platform, chooses and uploads | Platform pays contributors to create content; paid ranking; agents draft entries (D14); selling data itself (E13, extracts); selling subscriptions to the data; being controller of personal data; outreach to listed people | All present in design. Contributor payments and agent drafting are the biggest conflict with "only a platform" |

Honest conclusion: AllLists is closer to a publisher-aggregator or data broker with a marketplace layer than to a pure host. Safe harbour will cover at most a part of the content flow.

## 5. Content flows and how the rule fares

| Flow | Who authored | Rule holds? | Notes |
|---|---|---|---|
| Owner claims and edits own entry | Provider | Mostly yes | Best case. Keep it unedited and labelled "Provided by the company" (already designed) |
| Importer uploads own list, warrants rights | Provider | Partly | Platform still controller of any personal data, and sells it |
| Volunteer adds entries, paid share on sale | Contributor | Weak | Payment from sales is financial interest in content; "no one paid up front" helps a little, not much |
| Agent drafts from open sources and registers | Platform (or its tool) | No | Our content. Our responsibility. Needs a second check (already designed) |
| Platform-run loaders (GeoNames, Overture) | Platform | No | Licence and accuracy are ours |
| Subscriptions, extracts, outreach | Platform product | No | We are the seller and processor of data, and the sender of messages |

## 6. Requirements for the rule to hold in its changed form

Format: ID, requirement, type. T = terms/legal text, P = product feature, O = operations, C = company/structure. Priority: M = must before any public launch, S = should before charging, L = later.

### Terms and contracts
- LR-01 (T, M) Platform status clause: AllLists hosts and sells access to provider-submitted data; states which parts are platform-made (agent drafts, checks, rank, statistics) so the claim is accurate, not overstated.
- LR-02 (T, M) Provider warranty: the provider owns or has lawful right to submit and license the data; data is accurate; no unlawful personal data; consent evidence where the person is an individual.
- LR-03 (T, M) Provider indemnity and defence, with a cap-free carve-out for IP and personal data claims; plus provider licence to AllLists to host, display, sell, create extracts and statistics, sublicense to buyers.
- LR-04 (T, M) Buyer terms: lawful use only; no resale; no unsolicited messaging; compliance with local marketing rules; audit and suspension; planted-record leak clause (matches extract design).
- LR-05 (T, M) Contributor agreement: contributor is not an employee; share is a revenue share on net sales, not editorial control; contributor warrants rights; clawback if entry removed for breach (aligns with ledger holds).
- LR-06 (T, S) Acceptable-use and prohibited-content list: individuals without consent, children, patient data, personal mobiles, defamation, counterfeit, licence claims not seen (from the report's rules).
- LR-07 (T, M) Notice policy: how to report, response targets, counter-notice, repeat-offender policy, and a statement that payment does not buy removal-immunity or exemption.
- LR-08 (T, M) Privacy notice naming AllLists as controller (or joint controller) for list data, with purposes, sources, retention, rights, and contact; separate notice to listed individuals (Art. 14 GDPR style) (UNVERIFIED local equivalents).
- LR-09 (T, S) Limitation and disclaimer to buyers: data provided "as is", provider-supplied accuracy levels labelled (verification levels already exist); do not disclaim away data protection duties.

### Product features
- LP-01 (P, M) Provider identity (KYC): verified legal name, entity or ID, contact, and country for every provider who uploads or sells lists; stored encrypted; no national ID numbers kept beyond check (matches report rule).
- LP-02 (P, M) Per-record provenance shown to staff: provider, source, licence, date, consent status, verification level (exists; keep it mandatory, block publish without it).
- LP-03 (P, M) Notice-and-takedown workflow: public report form, SLA timers, reasons recorded, tombstone, global suppression so removed data is not reimported (exists; add SLA clock and statement of reasons).
- LP-04 (P, M) Data-subject rights tooling: access, correction, erasure, objection, free of charge; honour within statutory time (exists; confirm objection to extracts and outreach).
- LP-05 (P, M) Individuals: list named people only with consent; area only, no home address; contact through relay (matches Q-S2).
- LP-06 (P, M) Content labels: "Provided by the company", "Added by contributor", "Drafted by agent, checked by X", "Sponsored". Never let labels hide who authored what.
- LP-07 (P, S) Separation of paid and organic: payment affects only labelled sponsored slots; payment never changes verification level, removes content, or edits wording (matches C35 and section 7 of the build log).
- LP-08 (P, M) Agent drafts must stay draft and need human or second-source check before public (exists); treat as platform-authored for liability.
- LP-09 (P, S) Extract controls: purpose statement, buyer KYC, no personal contacts, planted records, per-buyer log (exists in part); add buyer terms acceptance and a purpose-limitation check.
- LP-10 (P, S) Repeat-infringer and abusive-provider policy: strikes, suspension, withholding of payouts while a claim is open (ledger holds exist).
- LP-11 (P, S) Country switches: each market can disable features (selling extracts, outreach, named individuals) until counsel signs off (exists).
- LP-12 (P, M) Local grievance contact and published contact for legal orders (India grievance officer; Pakistan authority orders; EU DSA contact point and legal representative where needed; UNVERIFIED which apply).

### Operations and company
- LO-01 (O, M) Written takedown and law-enforcement request procedure, with named responsible person, logged in the audit chain.
- LO-02 (O, M) Record retention schedule for provider KYC, consent, notices and actions; deletion after the period.
- LO-03 (O, S) Records of processing and a data protection impact assessment for list data, agents, extracts and outreach.
- LO-04 (O, S) Copyright and database-right review of every source licence before use (Overture, Foursquare, registers, chambers).
- LC-01 (C, M) Operating entity separate from the founder; insurance (media liability, cyber, E&O) priced before launch (UNVERIFIED availability in Pakistan).
- LC-02 (C, S) Local representatives or entities where required (EU Art. 27 and DSA representative; India; UAE) before targeting those markets.
- LC-03 (C, M) Marketing messages only to opted-in recipients; operator sends under its own name; suppression list honoured (exists).

## 7. Honest assessment of weakest points in the current design

1. Agents fill lists (D14). The platform authors this data. No safe harbour; accuracy and personal-data duties are ours.
2. Contributors earn a share of sales (CP1, F2). Money tied to content and to what sells pushes towards "active role" and "financial benefit with control". Mitigate with terms, takedown, no editorial instructions beyond a template, and disclosure.
3. Subscriptions and extracts monetise personal data. Controller status is hard to avoid (Russmedia logic, applied by analogy to a directory: UNVERIFIED).
4. Paid ranking and sponsored slots. Labelled and separate is defensible; unlabelled is a consumer-law risk as well as a safe-harbour one.
5. Outreach on behalf of buyers makes us the sender; "providers' responsibility" does not apply.
6. Pakistan: no clear data protection statute (per our report) cuts both ways. Less certainty, and a regulator with broad takedown powers. Do not read the lack of a law as permission.
7. Indemnities from small providers in poor markets will rarely be collectable. Do not rely on them as the main protection.

## 8. Questions for counsel

1. Under Pakistani law (PECA and its 2025 amendment, any pending data protection bill), is there an intermediary exemption for a directory host? Was the September 2025 amendment on host liability enacted?
2. Does the CJEU Russmedia reasoning (controller of user-posted personal data) apply to a B2B directory of sole traders and professionals? What is our lawful basis (legitimate interest, consent) for listing individuals and for selling their contact data?
3. Can contributor revenue share and agent drafting coexist with hosting protection in the US, EU, UK, India and UAE? Which structure (for example separate "provider-published" and "platform-compiled" products) is safest?
4. Does selling extracts and subscriptions make us a data broker needing registration anywhere (for example US state broker laws, India, UAE)? (UNVERIFIED which apply)
5. India: are we an "intermediary" under s79 given agent drafting and ranking? Do we need a grievance officer and local representative if we serve India? How does DPDP treat publicly available business contacts?
6. UAE: which PDPL provisions and executive regulations are in force; are free-zone rules relevant; what are the rules on unsolicited commercial messages and WhatsApp outreach?
7. UK and EU: do we need a DSA legal representative or Art. 27 GDPR representative if we do not target those markets but are accessible from them? Does the UK Online Safety Act apply to a directory?
8. What wording of the platform-status clause is accurate and enforceable, and what must we avoid saying (for example "we are not responsible")? Does an over-broad disclaimer harm us under consumer law?
9. Are indemnities and warranties from individuals and small firms in Pakistan and the Gulf enforceable, and what insurance fits?
10. Source licences: can we sell extracts and subscriptions derived from Overture, Foursquare, GeoNames and trade-register data, and what attribution or share-alike duties follow?
11. Health, children and prices: what extra duties apply to health facility prices, doctors, and child-facing tutors (Punjab Healthcare Commission, DRAP advertising, local child-protection rules)?
12. Where should the operating entity sit, and does a split (software company and data company) reduce exposure or look like avoidance?

## 9. Suggested decision log wording (for the founder to approve)

"AllLists is a marketplace and data service. Providers warrant what they submit and indemnify us, and we remove content on notice. We do not claim that providers alone are responsible: agent-drafted entries, extracts, subscriptions, ranking and outreach are our own acts, and the platform is responsible for them. Legal basis and terms to be settled with counsel before any public launch, individual listing, or messaging."

## 10. Sources used

- [Mondaq on Russmedia](https://www.mondaq.com/ireland/data-protection/1721724/gdpr-liability-of-online-marketplaces-for-user-published-advertisements)
- [Greenberg Traurig on Russmedia](https://www.gtlaw.com/en/insights/2026/2/cjeus-russmedia-decision-expands-platform-controller-duties-under-gdpr)
- [CDT on Section 230 and generative AI](https://cdt.org/insights/section-230-and-its-applicability-to-generative-ai-a-legal-analysis/)
- [ARY News on PECA Amendment Act 2025](https://arynews.tv/peca-amendment-act-2025-the-key-points/)
- [LAEX on section 79 IT Act](https://laex.in/?p=13903)
- Repo: `docs/DECISIONS.md`, `reports/Which lists pay.md`. UAE, UK, DMCA and DSA rows are UNVERIFIED (no source opened in this pass).
