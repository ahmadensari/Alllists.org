# Platform requirements 01: Monetisation

Date: 2026-10-06. Scope: what the 53 platforms in `reports/Established platform list types.md` do to earn, mapped to AllLists requirements, then compared with `backend/billing`, `backend/access`, `backend/ledger`. English only. Research method: standard web search, snippets only (most pages not opened). Anything not confirmed on an official page is marked UNVERIFIED. Prices are from third-party summaries unless stated.

Priority: P0 = needed before first paid sale; P1 = needed within the first paying markets; P2 = later.

## 1. Evidence gathered (short)

| Topic | Finding | Grade |
|---|---|---|
| Yelp self-serve ads | From about USD 150 a month with a monthly cap you set; billed per click; click price set by category, market and season; no contract, cancel anytime; separate "Upgrade" package (about USD 180) removes competitor ads from your page; dashboard with analytics and location/category targeting | Third-party (WebFX, Stackmatix), UNVERIFIED |
| Thumbtack | Pay per lead, about USD 15 to 80+, bought as credits; refunds rare (silent customer is not refundable; even scams and minors are disputed in the pro community) | Third-party and forum, UNVERIFIED |
| IndiaMART | Silver, Gold, Platinum annual plans (about Rs 30,000 to 250,000+ a year); RFQ/buy-lead credits; payment by NACH auto-debit, UPI, credit card; about 220,000 paying suppliers | Help-centre page found (NACH, UPI, card); the rest third-party |
| Justdial, Practo, Zameen, Rightmove, G2, Clutch | Tiered listing plans, per-lead or per-click fees, sponsored placement (details in `reports/` and `research_notes/Which lists pay/`) | Already graded there |
| AdSense | From 16 Jan 2024 a Google-certified CMP using the IAB TCF is required to serve ads in the EEA, UK and Switzerland; consent needed for cookies and personalised ads; thin-content pages and some site structures risk account action | Official Google support pages (snippet only) |
| Meta Pixel / CAPI | EU data-protection authorities (Austria, France) require opt-in before any Pixel call; a 2026 German court ruling is reported saying even server-side Conversions API needs consent; each CAPI event should carry consent parameters | Third-party consent vendors, UNVERIFIED |
| Pakistan payments | JazzCash and Easypaisa merchant accounts and wallets, Raast instant bank transfer, cards via a gateway or aggregator (Simpaisa and similar) | Third-party, UNVERIFIED |
| Pakistan tax | 2026-27 Finance Bill reported to bring foreign-platform creator and publisher income into withholding (about 5 percent filers, up to 10 percent non-filers); a 15 percent digital-ad tax was proposed in 2025-26 and a 5 percent digital tax was later reported scrapped | News snippets, conflicting, UNVERIFIED; needs a local tax adviser |
| India tax | Online advertising and digital services supplied from abroad are OIDAR; 18 percent IGST; exemption for overseas providers ended 1 Oct 2023 | Third-party tax sites, UNVERIFIED |

## 2. Requirements

| ID | Requirement | Seen at | Priority |
|---|---|---|---|
| M-01 | Self-serve ad purchase flow: pick place, list type, dates, creative, pay, no sales call | Yelp, Justdial, IndiaMART (inside plans), Zameen, Property portals, G2 | P0 |
| M-02 | Flat monthly pricing for fixed placement (sponsored slots) | Rightmove, Zameen, Justdial tiers, Product Hunt, Clutch | P0 |
| M-03 | Cost-per-click pricing with auction or fixed floor, monthly budget cap, pause and cancel anytime | Yelp, G2, Capterra, Google LSA | P1 |
| M-04 | CPM (impression) pricing option | Property portals, ad networks (not confirmed at the 53) | P2 |
| M-05 | Cost-per-lead pricing (pay when an enquiry is delivered), with lead-quality refund rules | Thumbtack, Sulekha, Clutch, Zocdoc, Bark, Angi | P1 |
| M-06 | Ad review before going live (policy: no misleading claims, category rules such as health and law), rejection reasons shown, appeal | Yelp, Google, Meta (platform norm) | P0 |
| M-07 | Clear label on every paid item ("Sponsored", "Ad") plus rel="sponsored nofollow" | Yelp, Google, all | P0 |
| M-08 | Paid ranking separated from organic rank and from review score; capped slots per list | Yelp, Justdial, G2 | P0 |
| M-09 | Advertiser performance dashboard: impressions, clicks, enquiries, spend, per list and place | Yelp, Justdial, IndiaMART, Practo, G2 | P0 (basic), P1 (full) |
| M-10 | Invalid-click and fake-lead protection (bot filtering, duplicate click suppression) | Yelp, Google | P1 |
| M-11 | Subscription tiers for sellers (free, basic, premium; Silver/Gold/Platinum style) with clear feature table | Justdial, IndiaMART, Practo, Zameen, Rightmove | P0 |
| M-12 | Subscription tiers for readers (live access, no ads for subscribers) | Decision CP5, E7 | P0 |
| M-13 | Auto-renew with local mandate where possible (NACH/UPI AutoPay in India; card on file elsewhere), renewal reminders, easy cancel | IndiaMART, Practo | P1 |
| M-14 | Verified or premium badge tied to a paid tier, but only after identity checks (not sold as trust) | Justdial Verified, Zameen, Practo | P1 |
| M-15 | Lead products: buy-lead lists, enquiry relay with contact hidden until purchase, credits wallet | IndiaMART, Thumbtack, TradeKey, Alibaba | P1 |
| M-16 | Lead refund and dispute process (fake, duplicate, minor, out-of-area) with time limit and reason codes | Thumbtack, Angi | P1 |
| M-17 | Credits or prepaid wallet with expiry rules and statement | Thumbtack, IndiaMART | P1 |
| M-18 | AdSense (or other network) for free viewers: ads.txt, certified CMP in EEA/UK/CH, labelled slots, no ads on thin or empty list pages, no ads next to health or restricted content where network policy bans it | Directories generally; G2, Capterra, AI directories (UNVERIFIED) | P1 |
| M-19 | CSP and consent compatibility: script-src, frame-src and img-src allowlists for the network and Meta, loaded only after consent; cache-safe pages | AdSense / Meta requirement | P1 |
| M-20 | Consent banner (per region), stored consent record, withdraw control, no tracking before opt-in in EU/UK | Required by GDPR/ePrivacy; AdSense | P1 |
| M-21 | Meta Pixel and Conversions API for AllLists' own acquisition ads (sign-up, purchase events, deduplication by event id, consent flag) | Platform norm | P2 |
| M-22 | Advertiser-side conversion tracking (UTM links, enquiry count, optional advertiser pixel is NOT offered at start) | Yelp, Justdial | P2 |
| M-23 | Payment methods per market: cards (Stripe, PayPal), India (Razorpay: UPI, NetBanking, NACH), Pakistan (JazzCash, Easypaisa, Raast, bank transfer, cards via a local acquirer), Gulf (card, bank transfer, Tabby-style later) | IndiaMART (NACH/UPI/card), local portals | P0 for one gateway plus manual bank transfer; P1 rest |
| M-24 | Manual and offline payment (bank transfer with reference, staff marks paid) for markets without a gateway | Justdial and Zameen sales-assisted | P0 |
| M-25 | Multi-currency pricing with local price points and FX policy | Thumbtack, Rightmove (GBP), Practo (INR) | P1 |
| M-26 | Gap-free numbered invoices, seller and buyer tax details, PDF download, credit note on refund | All paid portals; legal in EU, India, PK | P0 |
| M-27 | Tax: VAT/GST/sales tax collection by buyer country, tax number capture, reverse charge for B2B, Pakistan sales tax and withholding certificates, India GST (18 percent, e-invoice thresholds), UAE VAT 5 percent, EU OSS | Legal requirement; confirm per market | P0 for rate table; P1 for filing |
| M-28 | Withholding tax handling on advertiser payments (customer deducts tax and sends a certificate) and on payouts to contributors | Pakistan, India (TDS) practice (UNVERIFIED) | P1 |
| M-29 | Refund policy: pro-rata for subscriptions, none after ad delivered, full within a short window for unfulfilled orders; refunds reverse revenue and contributor share | Platform norm; Thumbtack as the cautionary case | P0 |
| M-30 | Chargeback handling and dispute evidence pack | Card platforms | P1 |
| M-31 | Seller dashboard: plan, renewals, invoices, orders, leads inbox, ad status, visibility stats, edit company page | Justdial, IndiaMART, Practo, Zameen, G2 Vendor Hub | P0 (basic) |
| M-32 | Staff console: revenue report, reconciliation, manual payment entry, refund, ad approval | Internal norm | P0 |
| M-33 | Fraud and advertiser verification (business check before large spends, blocklist for banned categories) | Yelp, Google | P1 |
| M-34 | Sales-assisted channel (field agents, commissions) for low-digital markets | Justdial, IndiaMART, Zameen | P2 (see open decisions) |
| M-35 | Paid placement rules for regulated sectors (health ads and prices, law, finance) | Report health rules, Q-S1 | P0 before any health ad |
| M-36 | Affiliate links with disclosure for software and product lists | G2, Capterra, Wirecutter, AlternativeTo | P2 |
| M-37 | Paid submission or "claim and upgrade" for topic lists (AI tools, apps) | AI directories, Product Hunt | P2 |

## 3. Built versus not built in the repo

Checked by reading models and services in `backend/billing`, `backend/access`, `backend/ledger`, plus templates and settings.

| Req | Status | Evidence in repo |
|---|---|---|
| M-01 | Partly | `access.placements.submit_ad`, `create_order(... ad=...)`, product `ad-month` (USD 49 a month text ad), `rank-city-month` (USD 199). Seller UI for buying not confirmed |
| M-02 | Built | Flat monthly `Product` rows, `scoped_price` multipliers by place depth and list type, `PLACEMENT_SLOTS` (2 per list) |
| M-03, M-04 | Not built | No bid, budget, CPC or CPM fields; `Ad.shown` and `Ad.clicks` counters exist only |
| M-05 | Not built | `outreach` app and enquiry relay exist; no per-lead pricing product |
| M-06 | Built (basic) | `Ad.State` pending/active/rejected, `decide_ad`. No rejection reason field, no appeal, no policy text |
| M-07 | Built | `Placement.label="Sponsored"`, ad template with label and `rel="nofollow sponsored"` |
| M-08 | Built | Sponsored rows rendered in a separate slot above rows; capacity check |
| M-09 | Minimal | Only `shown` and `clicks` counters; no per-advertiser dashboard view found in `billing/views.py` (staff revenue and orders only) |
| M-10 | Not built | `ad_click` increments clicks with no dedupe or bot filter |
| M-11 | Partly | `Plan`, `Product` kinds listing, rank, subscription; seed has one company-page product (USD 149 for 90 days); no tiered Silver/Gold ladder |
| M-12 | Built | `Subscription`, `Entitlement`, scoped subscription product, free viewers see ads, subscribers do not (decision CP5) |
| M-13 | Not built | `Subscription.provider_ref` field only; no renewal, mandate or reminder logic |
| M-14 | Not built here | Verification lives elsewhere; not tied to paid tier |
| M-15 | Not built | No buy-lead list product, credits or paid contact reveal; contacts hidden by policy |
| M-16, M-17 | Not built | No lead object, wallet or credits |
| M-18 | Not built | No ad-network code, ads.txt or CMP. Own first-party ads only |
| M-19 | Conflict | `core/middleware.py` CSP uses `script-src 'self'`; any network or Meta script needs a deliberate, consent-gated change |
| M-20 | Not built | Only session and CSRF cookie settings; no consent banner or record |
| M-21, M-22 | Not built | No pixel, CAPI or UTM handling found |
| M-23 | Partly | `Payment.provider` string and signed generic webhook (`handle_webhook`, HMAC, idempotent by provider ref). No gateway adapters for Stripe, Razorpay, JazzCash, Easypaisa; `PAYMENT_WEBHOOK_SECRETS` empty by default |
| M-24 | Built | `record_payment` with provider "manual", actor recorded |
| M-25 | Partly | Currency fields on product, order, placement, ledger; USD seeds; `consolidated_usd` report; no local price points or FX source |
| M-26 | Built | `Invoice` with per-year gap-free counter, seller and buyer JSON, credit note on refund, invoice page template. No PDF seen |
| M-27 | Partly | `TAX_RATES` per country (empty), `tax_for`, `Order.tax_rate`, `tax_minor`; buyer tax number in `billing` JSON. No tax-type logic (reverse charge, OSS, e-invoice), no filing export |
| M-28 | Partly | Payout side has KYC with `tax_id` (`ledger.submit_kyc`); no withholding on incoming advertiser payments, no certificate tracking |
| M-29 | Built (basic) | `refund_order` reverses ledger sale, revokes entitlements, cancels placements and ads, issues credit note. No pro-rata, no time window rule |
| M-30 | Not built | No chargeback state |
| M-31 | Partly | Subscription page, order page, invoice page, company page; no unified seller dashboard |
| M-32 | Built | `staff_revenue`, `staff_orders`, `reconcile`, `revenue_csv` |
| M-33 | Not built | |
| M-34 | Not built | |
| M-35 | Not built | Open decision Q-S1 |
| M-36, M-37 | Not built | |

Also built and useful to monetisation: double-entry `ledger` (accounts, postings, sales, allocations, holds, refunds, payout batches with approvals, KYC), contributor rate phases, and reconciliation.

## 4. Open decisions for the owner

1. First payment gateway per market: Stripe or PayPal for global, Razorpay for India, which Pakistani acquirer (JazzCash, Easypaisa, or an aggregator) and whether Raast/bank transfer alone is enough at launch. Suggested: manual bank transfer plus one global card gateway first.
2. Ad pricing model after flat slots: add CPC with monthly cap (Yelp style) or stay flat until traffic is proven. Suggested: flat only until a list type has steady traffic; CPC as P1.
3. Lead products: pay per lead or credits, and the refund rules (Thumbtack is the cautionary case). Conflicts with the hidden-contact rule (E13), so leads must be delivered by relay, not by contact reveal. Needs a decision.
4. Ad network for free viewers: AdSense or own supplier ads only (Q-R3). If AdSense, accept the consent banner, CSP change and thin-page risk, and avoid it on health pages. Suggested: own ads first, network only on pages with enough content.
5. Consent and tracking: which regions get a consent banner at launch, and whether Meta Pixel/CAPI is used at all in v1.
6. Tax: which countries to register in first; whether prices are tax-inclusive; who handles Pakistan withholding and India GST/TDS (needs local accountant; web sources conflict).
7. Refund policy wording: pro-rata for subscriptions, none for delivered ads or leads, and whether a refund also claws back contributor share (ledger already reverses; confirm policy).
8. Seller tier ladder and names, and whether the verified badge is part of a paid tier.
9. Advertiser verification before spend above a threshold, and banned or restricted categories.
10. Sales-assisted channel (field agents and commission) as in Justdial and IndiaMART, versus self-serve only.
11. Revenue share on ads: whether contributors earn from ad revenue (open Q-R3).

## 5. Sources

Google AdSense CMP and policy pages (support.google.com/adsense, snippets); WebFX and Stackmatix on Yelp Ads; Thumbtack community and third-party pricing pages; help.indiamart.com NACH and paid-services pages; Simpaisa and other Pakistan payment blogs; ProPakistani, TechJuice and Profit (Pakistan Today) on withholding and digital tax; India Briefing, BDO India, ClearTax on OIDAR; FlexyConsent, Seers, ConsentStack on Meta consent. All UNVERIFIED unless noted above.
