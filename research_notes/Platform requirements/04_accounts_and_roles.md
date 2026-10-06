# 04. Accounts and roles: platform requirements vs the repo

Prepared 6 October 2026. Scope: the 53 platforms in `reports/Established platform list types.md`. Repo read: `docs/TECHNICAL_PLAN.md` (section 11, 12), `backend/accounts`, `backend/catalog/templates/catalog/forms`, `backend/volunteers`, `backend/ledger`. No code was changed.

Evidence key. VERIFIED = seen in a search result this session (two searches only). UNVERIFIED = general knowledge of the platform, not re-checked; confirm before it drives a decision. The search tool returned little for Justdial, Practo, Yelp, LinkedIn, Zameen.

## 1. What the platforms do (cross-platform findings)

| Topic | Finding | Evidence |
|---|---|---|
| IndiaMART seller | Log in at the seller site, verify mobile and email by OTP, add at least 6 products, then a verification call. Business proof: CIN, electricity bill, invoice, GST, cancelled cheque or NACH form for paid plans. Mobile is the main identity; email OTP is the fallback if the phone is lost | VERIFIED (help.indiamart.com) |
| Upwork | Government ID, country on ID must match profile, profile photo, 7 days to finish or account is held; name must match bank beneficiary and tax form; US persons file W-9 or face withholding | VERIFIED (support.upwork.com) |
| Thumbtack | Optional free background check, badge not mandatory in every category; 1099-NEC or 1099-K tax forms for US pros | VERIFIED (Everlance, 1800accountant; secondary) |
| Justdial, Sulekha, Practo, Marham | Phone number and OTP is the main login; business claim by call or OTP to the listed number; doctors add registry number (medical council) and clinic proof | UNVERIFIED |
| Yelp, Google Business, Bing, Apple Business Connect | Owner claim by phone call, text, email or postcard; Google and Apple sign-in; Google video or document proof for some categories | UNVERIFIED |
| LinkedIn, Behance, GitHub, ORCID | Email or social sign-in; ORCID is itself an identity provider; free individual profiles; MFA and passkeys optional | UNVERIFIED |
| Alibaba, Made-in-China, Global Sources, TradeKey | Company account: business licence, legal rep ID, company bank account; paid "verified supplier" with third-party audit | UNVERIFIED |
| Angi, Checkatrade, Bark, Urban Company | Pros: licence and insurance, background check, ID; Checkatrade vets references. Urban Company trains and checks partners | UNVERIFIED |
| Zameen, PakWheels, OLX, Rozee | Phone or email plus OTP; agencies add business registration; Zameen agents sign up as agency staff under an agency account | UNVERIFIED |
| Support | All large platforms: help centre with search, ticket form, chat for paying users; Indian platforms add phone support for paying sellers | UNVERIFIED |
| Login pattern | Consumer platforms use a modal or drawer sign-in on a save, enquire or review action, returning to the same spot. Seller consoles use a full page | UNVERIFIED |

Patterns worth copying: phone-first OTP in South Asia; email as fallback; claim proof in tiers (OTP, then documents); payout KYC kept separate from sign-up and asked late (Upwork asks when money moves); name on ID must equal bank name; staff logins always with MFA.

## 2. Login and sign-up methods

| Method | Plan | Built in repo | Notes |
|---|---|---|---|
| Email and password with email verification | Yes (B6) | Built (`accounts/views.py` signup, verify, login, reset, throttle, delete) | Signup needs username, email, 2 passwords; no phone, no consent tick, no terms tick seen in view |
| Google | Later (B7) | Built (`accounts/social.py`, enabled by settings keys) | Own OAuth with PKCE, not allauth |
| ORCID | Later | Built (same file) | Fits contributors and researchers |
| Facebook | Later (B7) | Not built | Low value; business risk; decide |
| Apple | Not in plan | Not built | Required by Apple only if the app ships on iOS with other social login |
| Phone OTP login | Not in plan as login (OTP exists for claims) | Not built as login | Strongest platform pattern for PK and IN; needs an SMS or WhatsApp relay and cost |
| TOTP MFA with recovery codes | Yes, mandatory for moderator, finance, admin, surveyor lead | Built (`totp.py`, `mfa_*` views) | Roles list in `roles.py` `MFA_ROLES` |
| Passkeys (WebAuthn) | Not in plan | Not built | Add later for staff first |
| Sign out everywhere, idle timeout for staff | Yes | Not confirmed in code reviewed | Check `middleware.py` |
| Login throttle and lockout | Yes (P3 gate) | Built (`throttle.py`, `LoginAttempt`) | |
| Modal login | Not specified | Not built (full pages `/account/login/`, `next` handled by `_safe_next`) | See open decisions |

## 3. Tables per role

Columns: required details at sign-up and later, login options, screens. Status: BUILT, PARTLY, NOT BUILT.

### 3.1 Visitor (no account)
| Item | Requirement | Status |
|---|---|---|
| Details | None. Cookie and language preference only | BUILT (`/prefs/`, `prefs_location`) |
| Login | None | n/a |
| Screens | Browse, search, entry page, about, terms, privacy, plans, how checks work | BUILT. Cookie or consent banner not seen: PARTLY |
| Anonymous limits | Quota per address | BUILT (`access.quotas`) |

### 3.2 Free registered user
| Item | Requirement | Status |
|---|---|---|
| Details | Username, email (verified), password; optional display name, language, saved place | BUILT (`Profile`) |
| Optional later | Phone (for OTP login and enquiries), country | NOT BUILT |
| Login | Email, Google, ORCID, TOTP optional | BUILT. Phone OTP, Apple, Facebook, passkey NOT BUILT |
| Screens | Signup, login, verify, reset, dashboard, security, delete, my data, my enquiries | BUILT. Notification settings, profile edit page, saved lists, linked sign-ins manager: PARTLY or NOT BUILT (security page exists; confirm it lists social links) |
| Consent | Terms and privacy acceptance recorded, marketing consent separate | NOT BUILT at signup (consent register exists for outreach, `moderation/privacy.py`) |

### 3.3 Subscriber (viewer plan)
| Item | Requirement | Status |
|---|---|---|
| Details | Free account plus billing name, country, tax id for invoice (VAT or GST) | PARTLY (`billing`: Order, Payment, Invoice; buyer tax fields not confirmed) |
| Login | Same as user; MFA optional | BUILT |
| Screens | Plans page, checkout, invoices, quota use, cancel, enquiry to many | PARTLY (`/plans/`, `/enquiry/`; subscription management page not seen) |
| Model | Entitlement not a role | BUILT (`access.Subscription`, `Entitlement`) |

### 3.4 Contributor (list maker, populator)
| Item | Requirement | Status |
|---|---|---|
| Details | Display name, optional public credit, declared rights to data, rules quiz | BUILT (`ContributorProfile`: onboarded_at, declared_rights_at, quiz_score, show_credit, ref_code) |
| Later | Payout profile and KYC before first cash payout | BUILT (`PayoutProfile`) |
| Login | As user | BUILT |
| Screens | Contributor rules, onboarding quiz (5 questions, pass 4, English and Urdu), contributor page, my tasks, task detail, certificate, add entry, add area, payout | BUILT. Import (bulk) screen: not seen in account area; staff `imports` only |

### 3.5 Steward and verifier (surveyor)
| Item | Requirement | Status |
|---|---|---|
| Details | Contributor onboarding passed; segment assignment (place and type); independence rule (not on own entries) | BUILT for surveyor tasks; steward grant by role |
| Platform norm | Identity check and training for field staff (Urban Company, Checkatrade) UNVERIFIED | Identity check for surveyors NOT BUILT |
| Login | As user; MFA required for surveyor lead only | BUILT |
| Screens | My tasks, steward review queue (`/account/steward/`), certificates | BUILT. Mobile task screens: plan says yes; not confirmed |

### 3.6 Business owner and provider
| Item | Requirement | Status |
|---|---|---|
| Details | Claim with OTP to a stored contact, or text evidence; optional messaging opt-in | BUILT (`claim.html`) |
| Platform norm | Business registration number, GST or tax id, address proof, licence (health, trade), documents upload | Document upload NOT BUILT (text only by design at this stage) |
| Company content | Sections, Q and A, certifications (scheme, number, issuer) | BUILT (`owner.html`) |
| Login | As user | BUILT |
| Screens | Claim, owner page per entry, enquiries inbox, opt-out link | BUILT. Multi-staff access to one business (agency model, Zameen style): NOT BUILT. Verified-supplier tier with audit (Alibaba): NOT BUILT |
| Provider (individual freelancer or doctor) | ID, registry number, photo, payout KYC | NOT BUILT (individuals held back by plan, section 5 of platform report) |

### 3.7 Advertiser
| Item | Requirement | Status |
|---|---|---|
| Details | Entry code, place, list type, headline, text; company name | BUILT (`ads.html`, `Ad` pending state, `Placement`) |
| Platform norm | Billing identity, tax id, advertiser verification and policy acceptance | PARTLY (invoice exists; advertiser verification and policy tick NOT BUILT) |
| Login | As user | BUILT |
| Screens | Text ads, campaigns (outreach), orders | BUILT |

### 3.8 Company (buyer of outreach, plan "Buyer")
| Item | Requirement | Status |
|---|---|---|
| Details | Company name, category, budget, channel, approved template | BUILT (`campaigns.html`) |
| Platform norm | Company registration, authorised representative, team members with roles | NOT BUILT (single user per company) |
| Screens | Campaigns, dashboard | BUILT (dashboard detail not confirmed) |

### 3.9 Bulk uploader
| Item | Requirement | Status |
|---|---|---|
| Details | Contributor plus declared rights per import, source row with licence and tier | Capability `import_list` BUILT; rights declaration BUILT; source gate BUILT (per plan) |
| Login | As user, MFA recommended | optional |
| Screens | Staff imports console only; no self-serve upload page in account area | NOT BUILT for contributors |

### 3.10 Staff (surveyor lead, moderator, finance, admin)
| Item | Requirement | Status |
|---|---|---|
| Details | Invited by admin, MFA mandatory, audit logged | BUILT (`roles.py`, audit hash chain, `staff/` console) |
| Separation of duties | Payout approver differs from creator, no self approval | BUILT (test `test_staff_console.py`) |
| Login | Email plus TOTP; passkey NOT BUILT; idle timeout unconfirmed | PARTLY |
| Screens | Imports, sources, tasks, audit, switches, outbox, agents, jobs, statistics, ledger, metrics, subject access, extracts, queues (claims, kyc and others) | BUILT |
| Staff invite and role-grant screen | Admin grants | Role helper functions only; Django admin likely; custom screen NOT BUILT |

## 4. Cross-cutting areas

| Area | Platform norm | Repo status |
|---|---|---|
| Payout KYC | Legal name, country, bank or wallet, tax id; match name; review by a person (Upwork VERIFIED) | BUILT: `PayoutProfile`, encrypted, states submitted, approved, rejected, staff queue. ID document, address, sanctions screen, W-8 or W-9 style tax form: NOT BUILT |
| Tax | W-9 or W-8, 1099 style forms (VERIFIED for US); GST for India (VERIFIED for IndiaMART) | Only optional tax id string. Withholding and annual statements NOT BUILT |
| Privacy and consent | Consent at signup, cookie choices, data export, deletion | BUILT: delete account, my data page, subject access, consent and opt-in register. Cookie banner and signup consent NOT confirmed |
| Support and help centre | Help articles, contact form, ticket status | NOT BUILT: static pages only (about, terms, privacy, how checks work, rules). No help centre, contact form or ticket route |
| Notifications | Email, SMS, WhatsApp, in-app; per-topic settings | PARTLY: outbox and enquiry mail exist; user notification settings page NOT BUILT (plan lists it in profile) |
| Account settings | Profile, security, linked accounts, language, delete | PARTLY: dashboard, security, delete; profile edit and language switch beyond `/prefs/` unclear |
| Onboarding screens | Role picker, checklists, progress | PARTLY: contributor quiz only. No role chooser, no first-run checklist for owners |
| Session management | Device list, sign out everywhere | Plan only; NOT confirmed |

## 5. Gaps ranked
1. Support route (contact form and help centre): none exists, and every platform has one.
2. Signup consent record and cookie choice (legal gate before messaging tests).
3. Phone OTP login and phone field (main login in IN and PK).
4. Payout KYC depth and tax form before real payouts.
5. Owner documents upload, multi-user business accounts.
6. Notification settings page.
7. Self-serve bulk upload for contributors.
8. Passkeys, Apple, Facebook.

## 6. Open decisions
1. Phone OTP as a login method, or only for claims and enquiries? Cost of SMS or WhatsApp relay per country.
2. Modal login (drawer on save, enquire, claim) or keep full pages with `next`? Modal needs CSRF, focus and no-JS fallback care.
3. Facebook and Apple: skip, or add Apple only if an iOS app is planned.
4. Passkeys: staff only first, or all?
5. Claim proof: keep text-only at stage 1, or accept documents (GST, licence) now? Storage, retention and review cost.
6. Business accounts: one login per business, or a company account with team seats?
7. Individual providers (doctors, freelancers, tutors): list only from public registers, or let them sign up with ID and registry number? Plan holds back named individuals.
8. Payout KYC provider: manual review only, or a third party (cost, data location)?
9. Tax handling per country: collect W-8 or W-9 and GST or NTN, who issues year-end statements?
10. Staff role granting: Django admin only, or an audited screen with two-person rule?
11. Support channel: email only, form with tickets, WhatsApp? Who answers, in what languages (English and Urdu)?
12. Minimum age and children's data rule for signup.
13. Notification defaults and channels per role; which are mandatory (security, payout).

## 7. Sources
- https://help.indiamart.com/knowledge-base/how-to-become-verified-supplier
- https://help.indiamart.com/knowledge-base/why-indiamart-asks-for-number
- https://support.upwork.com/hc/en-us/articles/9908325862163-ID-Verification
- https://www.everlance.com/gig-guides/thumbtack-requirements
- https://1800accountant.com/blog/thumbtack-pro-taxes
