# Social buttons and campaigns for list pages and entry pages

Researched 2026-10-05 by web search (35 standard searches; WebFetch was tried on faq.whatsapp.com and datareportal.com and was blocked by the network proxy, so everything below rests on search summaries and documentation snippets). Search budget ran out at the end, so a few planned checks were not done (see Gaps).

Marker convention: **UNVERIFIED** = single-sourced, undated, from a vendor or blog, from general knowledge not checked in this session, or contradicted by another source. Dates given are the dates shown in the source or snippet; "undated" means none was visible. Retrieval date for all URLs: 2026-10-05.

Decisions respected (docs/DECISIONS.md, not reopened): text and numbers only, no pictures or videos (C29); contacts stay hidden and buyers use platform-delivered outreach (E13); list page shows first few entries plus statistics (E14); non-cash rewards only: levels, certificates, visible credit, free or discounted access (CP9); contributors paid only when a list is sold (CP1); outreach is opt-in and platform-sent, WhatsApp first, after counsel (Q-N5); named individuals only with consent, no home address, child-facing and Quran tutors not public (Q-S2); personal lists private by default; counsel booked before any messaging test or list of individuals.

---

## 1. Takeaway

1. **WhatsApp is the share button that matters.** In Pakistan it is the most-used app (27% name it first, IPOR survey, Aug 2025) and about 89.5% of messaging-app share (one statistics site, 2026); in Saudi Arabia 94.4% of men and 90.4% of women use it (2026 report); India has about 535.8 million users (aggregator, 2026). Facebook is second in Pakistan (about 69 to 71 million accounts, NapoleonCat, Jun to Aug 2026), then YouTube, TikTok and Instagram. X is marginal in Pakistan (2%). Snapchat and TikTok are big in Saudi Arabia, but neither offers a simple "share this web link" URL, so they are follow links, not share buttons.
2. **Build every share button as a plain link or the browser's native share sheet.** All the share formats we need are documented URLs that need no script, no SDK, no app ID and no tracking pixel: wa.me, Facebook sharer, X intent, LinkedIn share-offsite, Telegram share, mailto, plus `navigator.share()` and copy-link. Nothing loads from a social network until the visitor clicks. This avoids the joint-controller and consent problem that the EU court found for embedded "Like" buttons (Fashion ID, 2019).
3. **The preview card is the real campaign asset.** On WhatsApp, a shared link shows title, description and (if present) an image. With no images allowed at this stage, ship good `og:title` and `og:description` text on every list and entry page, and either one static brand card or a generated text-only card (image made from words and numbers, not photographs). Keep any image under 300 KB.
4. **Track with our own links, not third-party scripts.** Tag each share link with UTM parameters plus our own `ref` code, route through a short path on our own domain, and expect most WhatsApp shares to arrive as "direct" traffic anyway (industry claims 60 to 85% of sharing is "dark", UNVERIFIED). Measure shares (button clicks) separately from sign-ups (landing with a `ref` or UTM, then account created, then verified contribution).
5. **Reward verified contribution, not shares.** Meta bans making sharing, tagging or following a condition of entry to a promotion; FTC-style rules require disclosure of any reward for promotion. A level, certificate or credit earned when a referred person makes a verified contribution fits both the platform rules and the non-cash decision.
6. **Entries about people need a different default.** Share buttons on entries are fine for businesses and facilities. For named individuals (tutors, doctors, tradespeople) and anything child-facing, hide share buttons until the person has consented, put only the name, trade and area in the preview text, never a phone number or address, and give every entry a visible "not you? opt out" route. Pakistan has no general data protection law in force as of May 2026, but the UAE and Saudi laws are consent-first and Saudi enforcement began 14 Sept 2024.

---

## 2. Cited findings

### 2.1 What established platforms put on list and entry pages

Search results for UI details were thin; most platform findings are old or from third parties. Treat all as UNVERIFIED for the current design of each site unless stated.

| Platform | What was found | Source (date) | Grade |
|---|---|---|---|
| Product Hunt | Upvote, comment and share on launches; badges and embeds so makers can drive their own community to the launch page; "Product of the Day/Week/Month" badge that a maker can place on their site; homepage daily leaderboard; guidance to share on all your channels but not to ask directly for upvotes; every Product of the Day winner had a maker comment | https://www.producthunt.com/launch/guide ; https://www.producthunt.com/protips (both undated, via search summary) | Single source, UNVERIFIED |
| Goodreads | "Share This Book" buttons for Facebook, Twitter, Pinterest (and Google+, so the snippet pre-dates 2019) plus Facebook "like"; Facebook Timeline integration (reading status, reviews, quotes); year-end Reading Challenge infographic with badges members can paste into pages | https://www.goodreads.com/author_blog_posts/26174543-listopia (undated); https://www.goodreads.com/blog/show/335-introducing-goodreads-for-facebook-timeline (about 2011 to 2012); https://www.goodreads.com/blog/show/1602 (undated) | Old, UNVERIFIED for today |
| Yelp | Share button leading to a form for Facebook or Twitter; "Send to a friend" with a Facebook link | https://smallbusiness.chron.com/put-yelp-reviews-facebook-26997.html (undated, third party) | Old, UNVERIFIED |
| Tripadvisor | "Save" to My Trips; Facebook Like plugin integration (2007 and 2010 press releases) | https://tripadvisor.mediaroom.com/2010-04-21-TripAdvisor-Announces-Facebook-R-Like-Button-Integration ; https://tripadvisor.mediaroom.com/2007-01-30-TripAdvisor-Lets-You-Save-It-And-Go-With-New-Personalization-Tool | Old, UNVERIFIED |
| Pinterest | Follow button for a profile or board, built from the board URL; Pin-it share (via third-party button vendors); boards shareable by link | https://support.wix.com/en/article/pinterest-follow-button-334687 ; https://sharethis.com/platform/follow-buttons/pinterest/ (undated) | Third party, UNVERIFIED |
| Letterboxd | Lists public or private, "easily share on social media"; no button detail found | https://www.popsci.com/diy/how-to-use-letterboxd/ (undated) | UNVERIFIED |
| Zameen.com (Pakistan) | Property listings show share buttons for Facebook, X, WhatsApp, Gmail and email, plus copy link | Search summary of https://www.zameen.com/agents/ pages (undated) | Single source, UNVERIFIED |
| IndiaMART | "IM Insta" WhatsApp integration lets sellers share product details and chat with buyers on WhatsApp from the lead system; WhatsApp icon on catalogue pages said to raise direct enquiries; buyer responsiveness "about 3x" (company claim) | https://corporate.indiamart.com/im-insta ; https://corporate.indiamart.com/2025/01/02/empowering-commerce-cxo-today/ (2025-01-02) | Company claim, UNVERIFIED |
| Justdial, Practo, G2, Wikipedia | No usable result on the share and follow buttons of their list or entry pages | Searches returned only investor documents and scraper pages | **Not found (gap)** |
| Spotify Wrapped (mechanic, not a button) | Slides built at 9:16 for Stories and TikTok, a prominent one-tap share button, subtle branding on every share card; Spotify reported "500 million" shares in the first 24 hours of 2025 (+41% year on year) and fastest sharing growth in Colombia, India, Indonesia, Japan, Thailand and the US | https://nogood.io/2025/01/20/spotify-wrapped-marketing-strategy/ ; https://avenuez.com/blog/2025-spotify-wrapped-proves-success-once-again/ (both marketing blogs; the 500 million figure looks too high for shares and is UNVERIFIED) | UNVERIFIED figure; design pattern plausible |
| Strava | Annual achievements, KOM/QOM/course-record trophies, yearly leaderboards so newcomers can place; past records stay as profile badges | https://bikebiz.com/strava-launches-annual-achievement-trophies/ (2015 launch); https://roadcyclinguk.com/?p=107316 (undated) | Old, but the mechanic is clear |

### 2.2 Which networks are used in Pakistan, South Asia and the Gulf

| Market | Figure | Source (date) | Grade |
|---|---|---|---|
| Pakistan, first-choice app | WhatsApp 27%, Facebook 19%, YouTube 18%, TikTok 17%, Instagram 10%, X 2% (share who name it most-used) | Institute for Public Opinion Research survey, Aug 2025, via https://www.wmtips.com/technologies/social-media/country/pk and https://ipor.com.pk/uploads/68b54b0f2e3b4.pdf | One survey; the summary is second-hand |
| Pakistan, messaging share | WhatsApp 89.5% of instant messaging app share, 2026 | https://www.wmtips.com/technologies/instant-messaging/country/pk/ | Single source, UNVERIFIED |
| Pakistan, social identities | 79.9 million social media user identities in Oct 2025 (31.2% of population) | https://datareportal.com/reports/digital-2026-pakistan (via search summary; page itself blocked) | Reasonably reliable, second-hand |
| Pakistan, Facebook | 71,198,101 users in Jun 2026 (29.9%), 75.4% male; 69,371,601 in Aug 2026 (29%), 75.2% male; Messenger 53.7 million (Aug 2026) | https://stats.napoleoncat.com/facebook-users-in-pakistan/2026/06/ ; .../2026/08/ (via summary) | Ad-reach based estimate |
| Pakistan, Instagram | 26,602,300 users in Aug 2026 (11.1%), 64.1% male | https://stats.napoleoncat.com/instagram-users-in-pakistan/ | Ad-reach based estimate |
| Pakistan, LinkedIn | 15,050,000 members in Aug 2026 (6.3%) | https://stats.napoleoncat.com/ (via summary) | Ad-reach based estimate |
| Pakistan, YouTube, TikTok, Telegram, Snapchat | **No usable user counts found** | | Gap |
| Saudi Arabia | WhatsApp used by 94.4% of men and 90.4% of women; Snapchat 88.2% of women and 80.2% of men; TikTok 77.6% of women and 76.5% of men; users average 8.7 platforms a month (UAE 7.7) | https://minutemirror.com.pk/whatsapp-is-most-used-app-in-saudi-arabia-report-finds-620330/ ; https://communicateonline.me/news/social-chat-and-ai-reshape-consumer-behavior-in-uae-saudi-report/ (2026) | One report, second-hand |
| UAE and Saudi Arabia | More than 80% of the population active on WhatsApp | same Communicate Online report (2026) | UNVERIFIED |
| India | WhatsApp about 535.8 million, YouTube about 500 million, Instagram about 481 million, Facebook about 403 million, Telegram about 104 million (2026) | https://www.wscubetech.com/blog/social-media-platforms/ ; https://www.grabon.in/indulge/statistics/social-media-statistics/ | Aggregator blogs, UNVERIFIED |

### 2.3 Documented share-link formats (no third-party script needed)

All values must be percent-encoded (JavaScript `encodeURIComponent`). When the shared page URL carries its own `?utm_...` parameters, encode the whole URL again inside the share link.

| Channel | Format | Documentation | Notes |
|---|---|---|---|
| WhatsApp | `https://wa.me/?text=<encoded text>` (opens contact picker; text pre-filled and editable). With a number: `https://wa.me/<number>?text=...` | https://faq.whatsapp.com/5913398998672934 (blocked; described via https://www.unipile.com/it/?p=275019 and https://support.dotdigital.com/en/articles/11331301-click-to-chat-for-whatsapp, undated) | No sign-in, developer account or code. Number format (international, digits only, no plus or leading zeros) is from general knowledge, UNVERIFIED here. Use the no-number form for sharing; a number form would expose a listed entry's WhatsApp contact |
| Facebook (legacy, no app ID) | `https://www.facebook.com/sharer/sharer.php?u=<encoded URL>` | Not in current official docs; forum evidence that it works without app_id and is "legacy" (https://onlinecommunityhub.nl/forum/jssocials/80-feature-request-fb-appid, undated) | Facebook ignores any pre-filled text; the card comes from Open Graph tags. Could be withdrawn; UNVERIFIED |
| Facebook (documented) | `https://www.facebook.com/dialog/share?app_id=...&display=popup&href=<URL>&redirect_uri=<URL>` | https://developers.facebook.com/docs/sharing/reference/share-dialog | Needs a Facebook app ID and a redirect; no SDK required for the URL form |
| X (Twitter) | `https://x.com/intent/tweet?text=...&url=...&hashtags=a,b&via=handle` (twitter.com still redirects) | https://docs.x.com/x-for-websites/post-button/guides/web-intent | Text plus hashtags, via and url up to 280 characters; url is shortened by t.co; `related` suggests accounts to follow after posting |
| LinkedIn | `https://www.linkedin.com/sharing/share-offsite/?url=<encoded URL>` | Official page referenced in forum results: https://docs.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/plugins/share-plugin (not opened); format seen on https://forum.bubble.io/t/share-linkedin-button/220605 | URL only, no text field; title and description come from Open Graph tags |
| Telegram | `https://t.me/share/url?url=<URL>&text=<text>` | https://core.telegram.org/widgets/share ; https://core.telegram.org/api/links | Opens a chat, group or channel picker; text editable |
| Email | `mailto:?subject=<encoded>&body=<encoded>` | RFC 6068 (not opened this session); format from general knowledge, UNVERIFIED | Works on every device with a mail app; no script |
| SMS | Android: `sms:?body=<text>`; iOS: `sms:;body=<text>` (iOS rejects `?` in some versions; multi-recipient differs) | https://sethmlarson.dev/sms-urls ; https://weblog.west-wind.com/posts/2013/Oct/09/Prefilling-an-SMS-on-Mobile-Devices-with-the-sms-Uri-Scheme | RFC 5724 is the standard but iOS deviates; fragile, so not worth a button now |
| Native share sheet | `navigator.share({title, text, url})` | https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share | HTTPS only; must run inside a click; "limited availability, not Baseline", so always keep a fallback. On phones it lists WhatsApp, Telegram, Facebook, SMS and email in one tap. Desktop support is patchy (general knowledge, UNVERIFIED) |
| Copy link | `navigator.clipboard.writeText(url)` with a text-field fallback | General knowledge, UNVERIFIED (not searched) | Needs HTTPS and a click; add a visible "Copied" confirmation |
| Instagram, TikTok, Snapchat, YouTube | No documented web URL to share an arbitrary web link into a post or story. Use as follow links to our own profile pages (`https://instagram.com/<handle>`, `https://www.tiktok.com/@<handle>`, `https://www.youtube.com/@<handle>`, `https://www.snapchat.com/add/<handle>`) | General knowledge, not verified | Snapchat has a "Snap Kit" share route that needs an SDK or app registration, UNVERIFIED. Use the native share sheet instead |

### 2.4 Plain links versus official plugins and widgets

- Fashion ID (CJEU, C-40/17, 29 July 2019): a site that embeds Facebook's Like button is a joint controller with Facebook for the collection and transmission of visitors' data (including IP addresses of people who never click), and needs consent for processing at and before the plugin loads. Liability is limited to the stage where the site operator influences the means and purposes; later processing by Facebook is Facebook's. Source: https://www.thomashelbing.com/en/wissen/dsgvo-hub/rechtsprechung/1.4.13-eugh-fashion-id ; https://www.foxrothschild.com/publications/less-like-and-more-in-a-relationship-cjeu-on-joint-controllership-in-social-plug-ins (law-firm summaries; date of judgment is solid).
- Shariff (c't, Germany): static links or images, nothing is sent to the network until the visitor clicks; the vendor describes it as designed to meet GDPR. Source: https://de.wordpress.org/plugins-wp/shariff/ (vendor description, undated). Our plain-link approach is the same idea without any plugin.
- Trade-offs, summarised from the above plus general knowledge (UNVERIFIED where not cited): official plugins give live counts, "like" state and login convenience, but add third-party scripts (slower pages, more JavaScript), set or read cookies, and trigger consent duties in the EU and, for newer laws, in the UAE and Saudi Arabia. Plain links cost nothing at load time, work on slow phones, and need no consent banner for the buttons themselves. The price is no share counts and no "already liked" state; share counts are not worth showing on a new site anyway.
- Official tools worth knowing but not needed now: X's embedded button script, LinkedIn share plugin, Facebook SDK `FB.ui`, Pinterest "Pin it" script. All load third-party JavaScript.

### 2.5 Metadata that makes shared links look right

- `og:title`: roughly 40 to 60 characters before truncation. `og:image`: 1200 x 630 (1.91:1) is the common choice; absolute `https://` URL; JPG or PNG; keep under about 5 MB for most networks. Twitter/X: `twitter:card` set to `summary_large_image` (image about 1200 x 628) plus title, description and image; X falls back to Open Graph tags if Twitter ones are missing. Source: https://screenhance.com/blog/og-image-size-guide ; https://frontendchecklist.io/rules/seo/og-image-size ; https://specification.website/spec/foundations/open-graph/ (third-party guides, 2026, UNVERIFIED on exact numbers).
- WhatsApp, per Meta's developer page: `og:image` should be an absolute URL, under 600 KB, at least 300 px wide, aspect ratio no more than 4:1, and the Open Graph tags must appear in the first 300 KB of HTML; community reports say previews fail above about 300 KB. Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/link-previews/ ; https://chatarmin.com/en/blog/whats-app-image-size-guide (the 300 KB practical limit is UNVERIFIED).
- Without images (our case): publish `og:title`, `og:description`, `og:url`, `og:type`, `og:site_name`, `og:locale`, and a canonical link, and leave `og:image` out or point it at one small static brand card. WhatsApp and Telegram show title, description and domain without an image; Facebook and LinkedIn show a smaller link card. A generated text-only card (page title, entry count, place name, rendered to PNG) is possible with open tools such as Satori (JSX to SVG) and Vercel's OG generator (https://vercel.com/docs/og-image-generation). Facebook does not accept SVG for `og:image` (general knowledge, UNVERIFIED), so render to PNG. This is a design asset made from words and numbers, not a user picture, so it does not breach C29; the owner can still choose to skip it.
- Content rules I recommend (inference): list page description = "N entries in <trade> in <place>. Names free, details by account." (this uses the statistics already allowed by E14); entry page description = type, area and verification level only; no phone, WhatsApp number, street address, or owner name in any meta tag.

### 2.6 Tracking campaigns

- UTM parameters: `utm_source` and `utm_medium` are required together; `utm_campaign`, `utm_term`, `utm_content` and `utm_id` are optional. Source: https://support.google.com/analytics/answer/1033863 (Google Analytics help, legacy page) and https://www.ionos.co.uk/digitalguide/online-marketing/web-analytics/utm-parameters-explained/. Because UTM is just text on the URL, it also works with our own server logs, with no analytics vendor.
- Dark social: links shared in WhatsApp, Telegram, email and DMs arrive with the referrer stripped and are counted as "direct"; vendor estimates put these at 60 to 85% of all social sharing (https://www.stackmatix.com/blog/dark-social ; https://www.tryordinal.com/blog/dark-social, UNVERIFIED vendor claims). Consequence: the only reliable way to attribute a WhatsApp share is a parameter inside the link itself.
- Referral and K-factor: common practice is a 30-day attribution window; both codes and links are offered; K = invites per user x conversion per invite; K below 0.15 is "nice to have", 0.2 to 0.4 is a realistic target, above 1 is rare; benchmarks quoted: participation 15 to 25%, shares per user 3 to 5, click-through 20 to 40%, conversion 10 to 25%. Source: https://tessl.io/registry/skills/github/Eronred/aso-skills/referral-program and similar skill-library pages (secondary, undated, no primary data; UNVERIFIED, treat as rough guides only).

### 2.7 Campaign mechanics seen on other platforms

- Product Hunt: launch day with badges and embeds that let makers pull their own audience to the launch page; public daily leaderboard; Product of the Day/Week/Month badge that winners display. Source: https://www.producthunt.com/launch/guide (undated, UNVERIFIED).
- Spotify Wrapped: personal, data-led, shareable, "no strings attached" cards sized for Stories, single share button. Sources in 2.1.
- Goodreads: Reading Challenge with a year-end infographic and pasteable badges; Listopia lists ordered by member votes. Sources in 2.1.
- Strava: leaderboards per segment with yearly resets, trophies and badges that stay on the profile. Sources in 2.1.
- Pinterest: follow button for board or profile built into other sites. Source in 2.1.
- Meta rules for promotions: Facebook's guideline says a promotion must not require or incentivise sharing, reposting or tagging; Instagram's 2025 update bans mandatory liking, following, tagging or sharing to Story as entry conditions, but optional encouragement is allowed. A form-based refer-a-friend route is a valid alternative. Source: https://www.shortstack.com/help/facebook-promotion-guidelines/ ; https://www.plexus.co/resources/blog/trade-promotions/social-media/terms-and-conditions/instagram (vendor summaries, 2025; original Meta policy not opened, UNVERIFIED).

### 2.8 Rules and risks (cited)

- WhatsApp: businesses may message only people who gave their number and opted in to that business and message type; unsolicited bulk messages are not allowed; clear opt-out must be offered and honoured; Meta can restrict or ban a number without warning. Source: https://developers.facebook.com/documentation/business-messaging/whatsapp/getting-opt-in ; https://learn.rasayel.io/en/books/whatsapp/whatsapp-business/whatsapp-business-messaging-policy (2026 docs via search; secondary summary for the second). A user tapping a share button and choosing their own friends is a personal message, not a business message, but a platform-sent invite to a list of numbers is the regulated case.
- FTC (US, for reference): Endorsement Guides (16 CFR Part 255) updated in 2023; material connections (payment, free product, other benefit) must be disclosed clearly; reward must not depend on a positive review. Fake reviews rule effective October 2024 bans buying or creating fake reviews, undisclosed insider reviews and review suppression; civil penalties up to USD 50,120 per violation (figure adjusts yearly). Source: https://revisionlegal.com/internet-law/ftc-clamps-down-on-false-and-misleading-customer-reviews/ ; https://mwe.com/?p=244036 (law-firm summaries).
- Pakistan: PEMRA social media influencer regulations and the PASC advertising code require a disclosure label such as #ad, #collab, #promo, #sponsorship or #partnership on sponsored content (https://synergyzer.com/freedom-or-folly-when-content-creation-crosses-the-line/ ; https://avia.org/wp-content/uploads/2024/11/Pakistan-2024-Advertising-Matrix_Final.pdf, undated, UNVERIFIED on the exact scope). PECA amendments assented in January 2025 added section 26A: intentionally spreading false information likely to cause fear, panic or unrest can bring up to three years' prison and a fine up to Rs 2 million (https://www.dawn.com/news/1888224/senates-approval-of-contentious-peca-amendments-bill-triggers-protests-across-country ; https://arynews.tv/peca-amendment-act-2025-the-key-points/, Jan to Feb 2025). No comprehensive data protection law was in force as of May 2026; the Personal Data Protection Bill is still a draft (https://practiceguides.chambers.com/practice-guides/data-protection-privacy-2026/pakistan ; https://commoner-law.com/pakistan/data-privacy-digital-rights/data-privacy-without-pdp-act, 2026). One source says Pakistan has no specific rules on children's online content (synergyzer link above, UNVERIFIED).
- UAE: Advertiser Permit required for anyone advertising on social media from 1 February 2026, covering paid and unpaid promotions; sources disagree on the penalty (up to AED 1 million in one, AED 10,000 in another) and say the permit is free for the first three years. Source: https://gulfnews.com/uae/new-uae-law-advertiser-permit-now-mandatory-for-influencers-and-creators-for-social-media-1.500427938 ; https://communicateonline.me/news/uae-influencers-risk-aed-10000-fine-for-missing-advertiser-permit-deadline/ (2025 to 2026; figures conflict, UNVERIFIED). UAE PDPL (Decree-Law 45 of 2021, in force 2 January 2022) is consent-first with no general legitimate-interest basis (https://securiti.ai/uae-personal-data-protection-law/ ; https://www.cookieyes.com/blog/uae-data-protection-law-pdpl/).
- Saudi Arabia: PDPL effective 14 September 2023, fully enforceable from 14 September 2024; promotional messages need prior documented consent, simple opt-out and clear sender identity. Source: https://captaincompliance.com/education/saudi-pdpls-first-anniversary-amendments-enforcement-signals-and-whats-next/ ; https://cms.law/en/omn/legal-updates/one-year-anniversary-saudi-personal-data-protection-law (2024 to 2025).
- EU/GDPR: Fashion ID, see 2.4.

---

## 3. Recommended buttons

Conventions: "Link" shows the format with the encoded values written in angle brackets. `U` means the canonical page URL with tracking added: `U = https://alllists.org/<path>?utm_source=<channel>&utm_medium=share&utm_campaign=<list_share|entry_share>&utm_content=<list or entry id>&ref=<sharer code if signed in>`. No pixel, no third-party script on any button. (Domain is still open: alllists.org or alllists.com.)

### 3.1 LIST page

| Button | Link format | Tracking | Privacy note | Prototype |
|---|---|---|---|---|
| Share (native sheet) | `navigator.share({title, text, url: U})` shown only where supported; on phones this is the primary button | `utm_source=native` (we cannot tell which app the user chose) | Nothing sent to third parties by us; the OS handles it | Yes |
| WhatsApp | `https://wa.me/?text=<title + short line + U>` | `utm_source=whatsapp` | No number in the link; no script; opens the app or WhatsApp Web | Yes |
| Copy link | `navigator.clipboard.writeText(U)` | `utm_source=copy` | Local only | Yes |
| Facebook | `https://www.facebook.com/sharer/sharer.php?u=<U>` | `utm_source=facebook` | Plain link opening a new tab with `rel="noopener noreferrer"`; Facebook sees the visitor only after the click; legacy URL could change | Yes |
| Email | `mailto:?subject=<title>&body=<text + U>` | `utm_source=email` | Local mail app | Yes |
| LinkedIn | `https://www.linkedin.com/sharing/share-offsite/?url=<U>` | `utm_source=linkedin` | Plain link; no text field | Yes (matters for B2B and talent lists such as contractors, exporters, data scientists) |
| X | `https://x.com/intent/tweet?text=<text>&url=<U>&hashtags=<tags>` | `utm_source=x` | Plain link; X shortens the link | Yes, in the "more" menu (low use in Pakistan, 2%) |
| Telegram | `https://t.me/share/url?url=<U>&text=<text>` | `utm_source=telegram` | Plain link | Later (no Pakistan figure found; 104 million in India, UNVERIFIED) |
| SMS | `sms:` link, two syntaxes | `utm_source=sms` | Fragile across iOS and Android | No (native share sheet and WhatsApp cover it) |
| "Share my list" (list creator or contributor view only) | Same links, but with a ready-made message such as "I helped build the list of <type> in <place> on AllLists" and the sharer's `ref` code | `ref=<creator code>` plus `utm_campaign=creator_share` | Shows only the public profile name the contributor has chosen; make it opt-in | Yes (text version only) |
| Follow AllLists (footer) | Plain links to our own Facebook, Instagram, YouTube, TikTok, X, LinkedIn pages once they exist | Normal links, no tags needed | No embeds, no follow widgets | Yes, text links in footer, only for accounts that exist |
| Embed or badge snippet ("This list on your site") | Copy-paste HTML with a plain link and static text (no iframe, no script) | `utm_source=<site domain>&utm_medium=embed` | Plain text link avoids a tracking widget; backlink gives us referral traffic | Later |
| QR code for the list | Generated locally from `U` with `utm_medium=qr`; downloadable for posters in societies and shops | `utm_medium=qr` | Generated in our code, nothing sent out | Later (offline spread in Pakistan; inference) |

### 3.2 ENTRY page

| Button | Link format | Tracking | Privacy note | Prototype |
|---|---|---|---|---|
| Share (native sheet) | As above, `U` pointing at the entry | `utm_campaign=entry_share` | **Hidden for named individuals who have not consented, for anything child-facing, and for entries with the "do not share" flag** | Yes (businesses and facilities only) |
| WhatsApp | `https://wa.me/?text=<name, trade, area + U>` | `utm_source=whatsapp` | Message text holds name, trade and area only, never phone or address. This is the most likely route for a user to forward a shop or clinic to a friend | Yes |
| Copy link | As above | `utm_source=copy` | Local only | Yes |
| Email | `mailto:` as above | `utm_source=email` | Local only | Yes |
| Facebook | sharer.php as above | `utm_source=facebook` | Same as list; shows only the page title and description | Yes, in the "more" menu |
| LinkedIn, X, Telegram, SMS | As in the list table | As above | Individuals and health entries: off | Later |
| Owner "Share my listing" (shown after claim or verification) | Same links, with message "We are listed on AllLists, <verification level>" and a "listed on" text badge to copy | `ref=<owner code>` | Owner action, so consent is clear; show verification level honestly, no unearned badge | Yes (text only) |
| Business's own social page (field C17) | Plain outbound link to the Facebook, Instagram or other page already stored in the entry, `rel="nofollow noopener noreferrer"` | None added | This is entry data; show it only to viewers allowed to see that field (the paywall decisions E13 and E14 still apply) | Yes, but only where the field is visible |
| Contact on WhatsApp (`wa.me/<number>`) | Direct chat link to the listed number | n/a | Not a share button. It would reveal a stored contact, which conflicts with "contacts stay hidden" (E13) and with named-individual rules (Q-S2). Use platform relay | No |
| "Not you? Remove or correct this entry" | Link to a form with entry ID and reason | Count of requests per entry | See 5.3 | Yes (this is required, not optional) |

---

## 4. Campaign mechanics, ranked by effort and likely effect

Effect is my estimate (labelled inference); no source measured these for a directory like ours.

| Rank | Mechanic | Effort | Likely effect | Notes and fit with decisions |
|---|---|---|---|---|
| 1 | Share buttons (WhatsApp, native, copy) with good preview text and tagged links | Low (a day or two of front-end work) | High, because WhatsApp is the main channel in Pakistan, Saudi Arabia and India | Preview text matters more than any button. Spotify's lesson: one prominent share button |
| 2 | Tagged links plus `ref` code per user or creator, with a simple counts page (clicks, sign-ups, verified contributions) | Low to medium | Medium; the base for everything below | Server-side counting avoids third-party analytics; short links on our own domain keep previews intact (inference) |
| 3 | Contributor profile with levels and certificate, and a "share my progress" text card ("I verified 50 pharmacies in Sector F-8") | Medium | Medium to high among students and CV-minded volunteers | Fits CP9 exactly. Mirrors Goodreads challenge and Strava trophies. Make sharing the contributor's choice and show only the chosen name |
| 4 | Referral by verified contribution: a referrer earns levels, credit or free or discounted access when the invited person makes a verified contribution (not on click or sign-up) | Medium | Medium | Matches non-cash decision (CP9) and avoids paying for fake accounts. K-factor in the range 0.2 to 0.4 is a realistic goal per generic benchmarks (UNVERIFIED) |
| 5 | List and area leaderboards (top verified contributors per list, per city), weekly or yearly reset | Medium | Medium; risk of gaming | Strava and Product Hunt use leaderboards. Rank on verified entries, not raw volume, to avoid junk; let volunteers opt out of public display, and check ages first |
| 6 | "Launch a list" campaign (Product Hunt style): a creator opens a new list type or area, gets a ready-made post for WhatsApp, Facebook and LinkedIn and a launch-day count | Medium | Medium for the first lists in a place | Product Hunt guidance: share on your own channels, do not beg for upvotes. Creator's early-sales bonus (Q-O1) is separate |
| 7 | Owner badge and "listed on" text snippet for businesses that claimed their entry | Medium | Medium; brings backlinks and claim requests | Static text, no script. Only for owner-verified entries |
| 8 | Housing society or association pilots with a QR poster and a shared link | Low to medium, offline work | High within a society (inference) | Fits the one-society opt-in pilot (Q-P2); no recruitment commission |
| 9 | "Year in lists" recap (Wrapped style) for contributors and, later, subscribers | High | High but only once there is data | Needs months of data; later |
| 10 | Embed widgets (iframe or script) showing a live list on other sites | High | Low at first | Adds third-party loading and consent issues; later, if buyers ask |
| 11 | Platform-sent WhatsApp invites to listed businesses | Medium, plus legal work | Potentially high but riskiest | Opt-in only, after counsel (Q-N5); no cold bulk sends |
| 12 | Share-to-win contests or "tag three friends" | Low | Low and risky | Breaks Meta promotion rules if sharing is required; do not use |

---

## 5. Risks and rules

### 5.1 Platform terms
- Do not make sharing, tagging, liking or following a condition of any prize, level or credit on Facebook or Instagram (Meta promotion guidelines, summarised in 2.7). Optional encouragement is allowed. Rewarding a verified contribution that a referral led to is a different thing from rewarding the share itself.
- Do not post or message at scale from our own accounts or numbers to people who did not opt in (WhatsApp policy, 2.8). Do not buy followers, likes or shares; do not run networks of fake accounts (inference, consistent with FTC fake-review rule and platform terms).

### 5.2 Endorsement and disclosure
- If a creator or contributor receives anything (level, credit, certificate, discounted access) tied to promoting AllLists, the post should carry a clear label such as #ad or #collab (Pakistan label list, 2.8). In the UAE an Advertiser Permit may apply to people who advertise (2.8; figures disputed). FTC-style rules apply to US audiences and are a sensible global standard: disclose the benefit; the reward must not depend on positive content.
- Our own rule (recommendation): show "contributor earns credit for referrals" in plain text next to any referral link; ban rewards that depend on ratings (links to the reviewer-ranking decision Q-P3).

### 5.3 Personal data, children, health, opt-out
- Entries about individuals: the share button, preview text and URL must not leak data the viewer is not allowed to see. Previews show name, trade and area only. No phone, home address, ages, or children's details in any meta tag or share text. Health professionals: no prices or claims in the preview until the health rules (Q-S1) are adopted.
- Child-facing tutors and Quran tutors: no public entries, so no share buttons, until safeguarding is designed (decision Q-S2). Volunteer contributors may be students under 18: do not publish names or run leaderboards for minors without guardian consent (inference; no Pakistan rule found on this, see Gaps).
- Opt-out design (inference): (a) every entry has a visible "not you? remove or correct" link; (b) a per-entry "do not share" flag removes share buttons, adds `noindex` and a minimal preview; (c) removal is free (P17); (d) opt-out requests are logged and answered within a fixed time; (e) entries from a person who objects are suppressed from share cards and leaderboards at once; (f) any platform-sent WhatsApp message carries an opt-out instruction and a stored consent record (D17).
- Law by market: GDPR (Fashion ID) if EU visitors see third-party plugins; UAE PDPL consent-first; Saudi PDPL enforced since 14 September 2024; Pakistan has no general law in force (as of May 2026) but PECA covers cyber-offences, including false information (s26A) and the law could change; counsel to confirm before any list of individuals.
- PECA: do not let users post unverified claims in share text or "reviews" in a way that may amount to false information. Moderation and a report button are the practical protection (inference).

### 5.4 Fake engagement and gaming
- Referral credit tied to clicks or sign-ups will attract fake accounts. Tie credit to verified contribution and cap per-referrer rewards (inference). Use one account per phone number or verified email and review unusual referral clusters.
- Do not show public share counts or "likes" on entries at this stage; they invite manipulation and add third-party scripts.

### 5.5 Technical hygiene
- `rel="noopener noreferrer"` on outbound share links; encode every parameter; keep Open Graph tags in the first 300 KB of HTML; test previews in the WhatsApp, Facebook Sharing Debugger and X Card validators (named from general knowledge, UNVERIFIED).
- Strip tracking parameters from the canonical URL so shared and copied links do not fragment search ranking (inference: use `rel="canonical"`).
- If the `ref` code is stored in a cookie or local storage for attribution, that storage may need consent in the EU, UAE or Saudi Arabia; the simplest lower-risk design is to carry `ref` in the URL through sign-up and record it server-side at account creation (inference; counsel to confirm).

---

## 6. Inferences (labelled)

1. A prototype with only plain-link buttons has no consent banner duty for the buttons themselves, because nothing loads from a social network before a click. This follows from Fashion ID's reasoning (consent needed for what loads at or before the plugin) and the Shariff design, but is not a legal opinion. Counsel to confirm for each market.
2. On a phone, three buttons (native Share, WhatsApp, Copy link) cover almost all real sharing in Pakistan, Saudi Arabia and India; the rest go in a "more" menu on desktop. Basis: the usage data in 2.2 and Zameen's use of WhatsApp, Facebook, X, Gmail, email and copy.
3. A generated text-only preview card is consistent with the no-pictures decision because it carries no user image. The owner can choose to skip it and rely on text previews.
4. Short links on our own domain (for example `alllists.org/s/<code>`) give tracking, tidy messages and no dependence on a third-party shortener; the redirect must return Open Graph tags or a fast redirect so preview crawlers still read them.
5. Referral reward on verified contribution, not sign-up, is the best fit with CP1, CP9 and the verification levels (D19, D20) and also the safest under Meta's promotion rules.
6. The contributor "progress card" and the owner "listed on" badge are the two mechanics most likely to create organic shares, because they carry a person's own achievement or business name (compare Wrapped and Goodreads challenge badges). No source measured this for directories.
7. Quran tutors, child-facing services and health entries should have share buttons off by default even after listing, with opt-in sharing by the person or institution.
8. For B2B lists (Sialkot exporters, contractors, data scientists), LinkedIn and email are more useful than Facebook; for hyper-local lists (plumbers in a society), WhatsApp is the main channel, possibly with QR posters.

---

## 7. Gaps

- Official WhatsApp wa.me documentation (faq.whatsapp.com) and DataReportal pages were blocked; wa.me details come from vendor summaries, and the number format rule is from general knowledge.
- Official LinkedIn share-offsite documentation was not opened; format confirmed only by developer examples. Facebook `sharer.php` has no current official documentation found; only the `dialog/share` form (which needs an app ID) is documented.
- No usable button inventory for Justdial, Practo, G2, Wikipedia; Yelp, Tripadvisor and Goodreads results are old; Product Hunt, Letterboxd, Pinterest and IndiaMART are indirect. A hands-on look at each live site is needed to fill this in.
- No Pakistan user figures for YouTube, TikTok, Telegram or Snapchat; no Gulf figures beyond Saudi Arabia and a generic UAE line; Kuwait, Qatar, Oman and Bahrain not covered.
- No primary source for attribution windows or K-factor benchmarks (generic skill-library pages only); no measured effect for any mechanic on a directory.
- The Spotify Wrapped "500 million shares in 24 hours" figure looks implausible and was not corroborated.
- Not checked: Pakistan Telecommunication Authority rules on unsolicited commercial messages (search budget ran out), Pakistan rules on children's data and minors' contributions, Gulf rules on endorsements outside the UAE, Saudi advertising rules for influencers, the exact current text of Meta's promotion policy and WhatsApp's commerce policy, Instagram and TikTok web share capabilities, Web Share API desktop support by browser, and RFC 6068 and RFC 5724 text.
- Not covered by the brief but needed later: "follow this list" alerts as a product feature (not a social button), and legal advice on whether a user-initiated WhatsApp share counts as a business message.
