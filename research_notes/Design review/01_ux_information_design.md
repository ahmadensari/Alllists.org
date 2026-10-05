# Design review 01: UX and information design of the list and entry templates

Reviewer: independent UX and information-design pass. Scope: `prototype/alllists-prototype.html` (list, entry, empty, closed entry, system page), `docs/LIST_AND_ENTRY_COMPONENTS.md`, `docs/DECISIONS.md`, and the v2 screenshots. Decisions in DECISIONS.md are treated as fixed (names-only free preview, hidden contacts behind an outreach button, the four verification levels, paid ranking separate and labelled, text and numbers only). Where I criticise something that touches a decision, I criticise the execution, not the decision.

Method note: positions in pixels below are read from the 390 px wide screenshots and rounded. The prototype banner at the top (about 100 px) is not part of the product, so I subtract it. No web searches were used.

Severity key: **MUST** = fix before the template is frozen (the flaw is multiplied by every page). **SHOULD** = fix before launch. **NICE** = improvement when time allows.

---

## 0. Verdict in one paragraph

The skeleton is sound: ruled sections, one accent, system fonts, logical CSS properties, chips that carry meaning in words and shape, and honest "what was checked, by whom, when" thinking. The problems are mostly about **order and repetition**. The list page puts about eight blocks of meta-information (summary, actions, share, about, statistics, areas, filters, sponsored slot) between the title and the first result, so on a phone the first named business is roughly 3,200 px down, about four and a half screens. The free-versus-subscriber line is drawn in two inconsistent places (the list row hides specialities, the entry page shows them), and it is signalled with a "Locked" box on every row and about eleven times on a single free entry page, which at scale becomes wallpaper and reads as hostile. Trust cues exist but are written for the founder (S-101, OTP, confidence 0.82, decision E13), have no legend, and the key one, the date, is invisible on list rows. Urdu mode is a draft: the layout mirrors correctly, but concatenated strings, English chips and per-block `dir="auto"` produce visibly broken lines. None of this needs a redesign; it needs about a dozen precise changes, listed in the ranked summary.

---

## 1. Ranked summary

### MUST fix

| # | Finding | Where | Fix in one line |
|---|---|---|---|
| M1 | The first screen on a phone does not say what the list covers or whether to trust it, and the one primary button ("Reach this list") is unexplained | List page, top | Replace the top block with title, one-line scope, a trust summary (how many checked and how), then filters and results |
| M2 | Eight blocks sit between the title and the first result (first row about 3,200 px down) | List page | Results come straight after the summary and filters; About, statistics, areas, sponsored explanation and contributors move below or into disclosures |
| M3 | Locked markers repeat on every row and about 11 times per free entry page | Rows, entry facts, tables, stats | One "what subscribers also see" panel per page; no per-field lock boxes |
| M4 | Free and paid line is inconsistent: list rows lock specialities, certificate, minimum order; the entry page shows specialities and product categories free | List rows vs entry About and Manufacturer details | One table of what free sees on a row and on an entry; enforce it in the template |
| M5 | Trust cues have no legend and rely on hover (`title`), which does not exist on phones; wording is internal ("OTP to stored number", "Surveyor S-101", "confidence 0.82") | Chips, Trust section | Plain one-line gloss under each level, a tap-to-open key, rewrite all `how` strings |
| M6 | List rows show no date and no "who"; the page copy promises "what was checked, by whom and when" | Result rows | Add "Checked 18 Sep 2026" to each row; fix the copy |
| M7 | The entry page puts a long Trust block above the actions; the Contact button is about 780 px down, at or below the fold on most phones | Entry page, top | Name, one-line facts, chips, Contact in the first screen; details of checks below |
| M8 | Action areas are overloaded: 3 to 4 actions plus 7 share buttons; Report sits beside the primary action; Contact and Request a quote are indistinguishable to a buyer | List and entry action panel | One primary, one secondary, Save; one Share button; Report to a single "Something wrong?" section |
| M9 | Closed entry still shows Contact, Request a quote and Owner-verified chips as if live | Entry page, `status:closed` | Closed state suppresses outreach and quote, greys the checks and leads with "Closed" |
| M10 | Template breaks on realistic data: no pagination or page limit, 40 specialities printed as text, no-contact and no-hours cases undefined, the same "Manufacturer" printed on every row, nowrap chips can overflow 390 px | Whole template | Specify empty-field rules and caps (section 7) |
| M11 | Urdu mode: concatenated strings break ("of 7 shown 7", "subscribers :مقفل"), chips stay English, Urdu name floats to the opposite edge, type is too small for Urdu | Urdu list and entry | Whole-sentence translation strings, translated chips, `:lang(ur)` type scale, inline-block for the second name |
| M12 | Prototype or internal copy would ship: "decision E13", "moderator view", "awaiting verification (hidden)", "(sample)", "In the real product", "Baidu and Amap links need a coordinate conversion" | Throughout | Strip; list in section 8 |

### SHOULD fix

| # | Finding |
|---|---|
| S1 | "Position 1 of 7" on every row reads as a quality ranking and is meaningless at 5,000 entries; rank of individuals is hostile |
| S2 | Statistics table by "check type" adds to more than the total and needs a footnote; use a partition (highest check) that sums to the total |
| S3 | Areas table is a block above the results; at 400 areas it is a wall and its links are not filters |
| S4 | Two breadcrumb rows before the title on the list page; five-level crumb on the entry wraps on mobile |
| S5 | Sponsored slot is a yellow warning-coloured box addressed to the founder; an empty slot must render nothing, a filled slot should use the row layout with a label |
| S6 | Three overlapping routes to report or correct an entry plus the footer; merge |
| S7 | Duplicated information on the entry (specialities twice, verification tier twice, type four times, contact twice, dates six times) |
| S8 | Empty placeholder sections ("Rankings and reviews: No rankings yet") would appear on every page for years; hide until real |
| S9 | Share links carry `utm_*` and `ref` parameters even for "Copy link"; copy the clean link |
| S10 | Tables on mobile (prices, certificates) wrap to 4 or 5 lines per cell; use stacked records |
| S11 | Stats table label and value sit up to 900 px apart on desktop (in both directions in RTL) |
| S12 | The unlock panel has no price, no button and contradicts the entry page on whether outreach is free |
| S13 | Dates in ISO form (2026-09-18) and no age ("3 weeks ago") for a reader who wants freshness |
| S14 | Touch targets 36 px (`.btn.sm`, selects) and 13 px chip text carry the most important information |

### NICE to have

N1 prev/next navigation inside a list while comparing. N2 "Similar entries" block (specified, not built). N3 response-rate cue for relayed messages. N4 "Open now" computed from hours. N5 shortlist and "send one enquiry to several" (this is probably what "Reach this list" is trying to be). N6 reduced opacity on closed rows fails contrast; use a label and a rule instead.

---

## 2. First screen on a phone (question 1)

**What a visitor sees now, 390 px wide, list page.** Logo and search; two breadcrumb rows (six links); H1 "Surgical instrument makers in Sialkot"; two tags ("National export cluster", "Sample list"); a summary line; then an action panel with "Reach this list", "Follow list", "Report", and three rows of share buttons. The first screen ends inside the share buttons. The About paragraph, the only text that says what the list covers, starts below the fold.

Scoring against the three questions:

| Question | Answered in first screen? | Why |
|---|---|---|
| What is this list? | Partly | The title says it. The scope sentence ("makers of surgical, dental, veterinary and beauty instruments... traders are listed separately") is below the fold. "National export cluster" is a founder's taxonomy term, not a buyer's. |
| Can I trust it? | No | The only trust cue is "Last updated 2026-10-05" in a line that otherwise talks about hidden entries. How well checked the list is lives in the Statistics table about 700 px lower. |
| What can I do? | Unclear | "Reach this list" is the loudest element and nobody can say what it does. It is unclear whether it messages all seven businesses, whether it is free, and the unlock panel below says outreach tools for the whole list are a subscriber feature. If a free visitor taps the primary button on the first screen and hits a paywall, that is a bad first interaction repeated on every list page. |

**M1 fix, a first screen that answers all three.** Top to bottom on a phone:

1. One breadcrumb row (place only; see S4).
2. H1 (unchanged pattern).
3. One scope sentence from the list type record (the "About" first line), not a tag.
4. A **trust bar**: "7 businesses listed. 2 visited by a surveyor, 2 confirmed by the owner, 3 checked by computer only. Last check 18 Sep 2026." Render the counts as a single segmented bar with the numbers in text so structure carries information. Use a partition by highest check so the numbers sum to the total (see S2).
5. Two actions only: **Search or filter** (a visible "Filter by area" control) and **Follow** (optional). No share block here.
6. First three results.

"Reach this list" should either become a per-selection action ("Send one enquiry to the makers you tick", with a free or subscriber label) or move off the first screen. As written it is the weakest-defined control carrying the strongest visual weight.

**The summary line.** "7 published, 1 awaiting verification (hidden), 1 closed (hidden)." Hidden things should not be mentioned to the public in the headline; "awaiting verification" is the pipeline, not a fact about the list. Say "7 listed". If the founder wants honesty about the unchecked ones, a small line lower down: "1 more entry is waiting for its first check and is not shown." Remove "closed (hidden)" entirely; a buyer gains nothing.

---

## 3. Hierarchy and scannability

### 3.1 List page

**Every section has the same weight.** On the desktop screenshot, "About this list", "Statistics for the whole list", "Areas in this list", the filter row and "7 of 7 shown" all use the same H2 size and the same rule. The results, which are the reason anyone came, are the eighth block. The page reads as a document of stacked tables, not a directory.

**M2 fix, reorder.** Proposed list-page order (identical for every list):

1. Place crumb, title, scope sentence
2. Trust bar and last check date
3. Filter row (area, verification, sort), one line on desktop, a single "Filter" button on mobile
4. Sponsored slot only when filled (row layout, labelled)
5. Results (page 1, with a stated limit; see M10)
6. Subscriber panel (single, with price and button)
7. Areas (collapsed to top 8 plus "all 40 areas")
8. About this list and how it is checked, merged with "Where this data comes from"
9. Contributors, steward, help build this list
10. Related lists
11. Legal footer

Statistics and areas are valuable to a buyer deciding whether to subscribe, but they are secondary to the names. If E14 stands ("first few entries plus statistics"), statistics could sit directly under the trust bar as the same bar, expanded on tap, instead of a table.

**Result row.** Desktop row is four columns: name and Urdu name; type, area, position stacked with `<br>`; chips plus a lock box; an Open button. Issues:

- The **name is the scan target and is the same size as body text** (16 px, weight 600) and smaller than the H2s above it. Raise to 18 px (`--t-lg`).
- **"Manufacturer" is printed on six of seven rows.** In a list titled "Surgical instrument makers" that column carries almost no information (it distinguishes only the one trader). Structure must encode real information. The second column should be a **list-type-defined descriptor slot** (for manufacturers: specialities, or a short "makes: dental, general surgery"; for doctors: specialty; for hotels: star class). Show "Trader" as an exception chip only when it differs from the list norm.
- **"Position 1 of 7"** is discussed in S1.
- **The Open button duplicates the name link.** It costs 44 px of height per row on mobile and adds noise at 5,000 rows. Remove it; make the whole row a tap target (name link stretched with CSS).
- **No date.** M6.
- Stacking by `<br>` instead of semantic columns means a screen reader announces one blob. A real table (name, area, checks, last checked) with sortable headers is better for a register of thousands.

**Mobile row height.** Each row is about 190 px (name, Urdu name, type, area, position, chips, lock box, Open). Seven rows are about 1,300 px, so one screen shows three and a half businesses. Target 100 to 110 px: line 1 name (Urdu name inline), line 2 descriptor and area, line 3 chips and "Checked 18 Sep 2026".

### 3.2 Entry page

Order now: crumbs, name, Urdu name, three tags, Trust, action panel, Key facts, About, type-specific details, prices, certificates, rankings, In this list, provenance, correct or claim. Mobile height is about 4,500 px.

Problems:

1. **Trust before action and before any fact.** M7. The spec (section 9) also puts the trust strip before actions; the spec is right to put trust above facts but the prototype makes it a full section with two chips, two bullets and a paragraph. Make a compact **trust strip** (chips plus one line "Last checked 18 Sep 2026") directly under the name. Move the detailed list of what was checked into an expandable "What was checked" below or into the provenance section.
2. **No lead summary.** The buyer's first questions (what do they make, where, since when) are in Key facts and About, 1,000 px down. Put one line under the name: "Manufacturer · Paris Road, Sialkot · General surgery, Dental · Since 1998." This line is also what a search snippet and a WhatsApp share should say.
3. **Tags "Manufacturer", "Business", "Open".** "Business" is the internal `entity_type` and means nothing to a reader. "Open" is ambiguous (open now? open for enquiries?) and is the default state; show a status tag only when it is not "open". Keep the type in the summary line, not as a tag.
4. **Key facts is a flat list of ten items with no priority.** Order by what a buyer needs: area, hours, languages, then established, size, website. Fine as a `dl`, but rows that are absent must be omitted by a single rule (M10).
5. **Duplicates.** See S7.
6. **Specified but missing:** "similar entries", and a clear route to the previous or next entry in the list (N1, N2).

---

## 4. Free versus subscriber (question 3)

### 4.1 Is the line fair and clear?

The principle (names and checks free; details by account) is clear in the decisions. The prototype does not apply it consistently.

| Field | List row (free) | Entry page (free) | Spec says |
|---|---|---|---|
| Specialities | Locked | **Shown** (About, "Specialities") | P |
| Product categories | n/a | **Shown** | P/L mixed |
| Certificate | Locked | Locked | P number with register link (identifiers, row `identifiers`) |
| Minimum order | Locked | Locked | add-on |
| Hours, languages, year, OEM flag | n/a | Shown | P |
| Address | n/a | Area shown, street locked | P area, L detail |
| Exact map pin | n/a | Locked | L |
| Website, social | n/a | Locked | L (Q-S13) |
| Statistics | Two of six rows locked | n/a | E14 says statistics are free for the whole list |

**M4.** A free visitor sees "Locked: specialities" on the row, taps a name, and reads the specialities on the entry page. That undermines the names-only mitigation against rebuilding paid lists (P15) because an entry page is exactly what a scraper walks, and it makes the lock look dishonest to the user. The spec table itself marks `specialities` as P while the row locks it; the spec and prototype disagree. Pick one rule and write it as a single table in the spec (row, entry, subscriber). My suggestion within the decisions: free row = name, area, descriptor-free, checks and date; free entry = name, area, type, checks and dates, status, hours, languages, year; everything else subscriber.

**Fairness to the buyer.** The thing a buyer of surgical instruments most needs in order to shortlist is what each maker makes and whether they hold a certificate. Both are locked in the free row. That is a legitimate commercial choice, but then the free list has to make the best use of what it does show:

- The **checks and their dates** are the free product. They must be visible on every row (M6).
- Where the data exists, show **presence without value**: "Certificate on file (number for subscribers)". This reveals nothing a scraper can use and is more persuasive than a grey "Locked" box. This does stay inside names-only for list rows; it concerns the entry page and I flag it as a proposal for the owner.
- The statistic "Verified in the last 12 months" is the single most trust-relevant number on the page and it is locked for free visitors (S12 below mentions the contradiction with E14). Free visitors who cannot see freshness are being asked to trust blind. Unlock it, or replace it with "Last check: 18 Sep 2026" which is already free.

### 4.2 Locked markers as clutter at a billion pages

Count on one free entry page (e1, free view): street address, exact pin, size, website, social pages, export markets, minimum order, two prices, two certificate cells. That is **eleven** grey dashed boxes saying "Locked: ...". With 40 priced services the prices table would hold 40 of them. On the list page, every row carries one that wraps to two or three lines on mobile ("Locked: specialities, certificate, minimum order"), plus two in the statistics.

Problems:

- It turns the page into a form full of blanks; the first impression of the product is of what it hides.
- Dashed grey boxes are the same visual element as the ad slot and sponsored slot (`.lock`, `.ad`, `.spons` all use dashed borders), so three different meanings share one look.
- The word "Locked" has a negative tone. "Locked" sells less than "subscribers also see".
- It adds 40 to 100 px per row of vertical noise for no information; the content of the lock is identical on every row.

**M3 fix.**

1. Rows: remove the lock box. One line above the results: "Free view shows name, area and checks. Subscribers also see specialities, certificates and minimum orders." with a link.
2. Entry page: delete locked rows from Key facts, Details, Prices and Certificates. At the end of Key facts, a single row: "**9 more details on this entry** for subscribers: street address, exact pin, website, 2 prices, ISO certificate number." Generate the list from the fields that actually exist for this entry, so it is both honest and a real teaser, and so entries with nothing hidden show nothing.
3. If a table has only locked cells (prices), replace the table with "2 prices, shown to subscribers", not a table of boxes.
4. Layout shift when the user subscribes is acceptable; the alternative is a permanently noisy free page.
5. Keep one visual language: the lock treatment is for the subscriber panel only; ad and sponsored slots get their own treatments.

---

## 5. Trust cues (question 4)

### 5.1 What exists and what is wrong

**Chips.** Four labels (decided) with shape and weight differences: surveyor (2 px solid green, bold), owner (1 px solid green), AI (dashed grey), none (dotted grey), closed (red). Good: not colour alone; labels are specific.

Issues:

1. **No legend.** The only explanation is a `title` tooltip, which does not exist on a touch screen. Fix: a visible key reachable from every chip (tap opens a four-line explanation), and one line of gloss on the list page under the trust bar. Suggested plain wording, to be translated and tested with Pakistani buyers:
   - Surveyor-verified: "Someone from AllLists visited and checked."
   - Owner-verified: "The owner proved they control the phone number we have for them."
   - AI-checked: "A computer matched public sources. Nobody visited."
   - Not verified yet: "Not checked." (Not shown publicly in v1.)
2. **"Owner-verified" is ambiguous.** Read as "verified by the owner" it sounds like self-declaration; read as "verified owner" it sounds stronger than it is. The label is decided; the gloss above fixes it. Do not let it use the same green and nearly the same shape as surveyor: the difference is one pixel of border. A buyer deciding between a visited and a self-confirmed business needs a clear difference. Add a leading mark that differs (for example a filled chip for surveyor, outline for owner) and make sure the difference survives at 13 px in sunlight.
3. **The chip detail text is written for staff.** "Surveyor-verified (Surveyor S-101, 2026-09-18)": S-101 means nothing to a buyer; "Owner-verified (Owner, 2026-09-02)" has the word "Owner" twice; the bullets underneath repeat the same chips again ("Visit, checklist 12 of 12", "OTP to stored number", "2 sources matched, confidence 0.82"). Rewrite as one line each:
   - "Visited by an AllLists surveyor on 18 Sep 2026. 12 of 12 checks passed."
   - "Owner confirmed by a code sent to the phone number on file, 2 Sep 2026."
   - "Computer check on 22 Aug 2026: matched 2 public sources."
   Drop the numeric confidence; "0.82" has no meaning to the reader and invites dispute. Show who only where it helps (a surveyor name or first name and a stable ID in the provenance section, not in the chip).
4. **"Claimed: yes" next to "Owner-verified"** is the same fact twice. Merge: if owner-verified exists, the claim is shown by that chip. Keep "Not claimed. Is this your business?" as the owner prompt instead (see section 6).
5. **"Last updated" on the entry is computed from the latest verification date**, so it is mislabelled: it is not when the data changed, it is when something was last checked. Label it "Last checked". Show a separate "Details last changed" only in provenance.
6. **Dates are ISO and bare.** For this audience "18 Sep 2026" or "3 weeks ago" reads faster than "2026-09-18"; show both ("18 Sep 2026, 3 weeks ago"). More important: the **age of a check matters** and the chips do not show it. A surveyor visit from July 2026 (e4) looks as strong as one from last week. The spec says expired checks drop back; show the expiry or a "checked X months ago" text on the chip so the visitor can judge it. Use text and an age bucket, not colour alone.
7. **Closed entry shows Owner-verified.** M9.
8. **Chip `white-space:nowrap` plus an unbounded "by" string** can overflow a 390 px screen when the detail variant is used (Trust section). A name like "Surveyor Muhammad Ahmad (Sialkot team), 2026-09-18" will cause horizontal scroll. Allow wrapping inside the chip detail or put the detail on a second line.
9. **Chip order implies a ladder** although the spec (section 7) says independent chips, not a ladder. Rows list the surveyor chip first and sort by position, so visitors will read surveyor > owner > AI. That reading is mostly right and probably acceptable, but then say so in the legend rather than leaving the conflict.

### 5.2 Can a non-technical Pakistani small-business owner or buyer understand them?

Not yet.

- "Surveyor", "verified", "OTP", "checklist", "claim", "steward", "AI-checked" are all English technical or process terms. A small shop owner knows "OTP" from banking apps, but "OTP to stored number" is a mechanism, not a meaning. "AI" will be understood by many as "computer", and the gloss should say "computer" explicitly.
- The chips are not translated in Urdu mode (`LEVEL` is English-only; the Urdu screenshot shows English chips). That alone makes the trust layer unreadable for Urdu-only users. It is the first thing to translate.
- Suggested handling: keep the four decided English labels as the canonical label, add a short Urdu label per chip, and show the gloss in the user's language. Test the Urdu wording with five real shop owners and five buyers before freezing.

---

## 6. The action area (question 5)

### 6.1 List page

Current: Reach this list (primary), Follow list, Report, then Share, WhatsApp, Copy link, Facebook, Email, LinkedIn, More. Thirteen controls in one card at the top of the page, which on a phone is about 300 px of buttons.

Findings:

- **M8 Report is in the primary row.** A destructive or negative action beside the primary action invites accidental taps and gives the page an anxious tone. Report belongs in a quiet "Something wrong with this list?" link near the bottom (the footer already has "Report", so it appears twice).
- **Primary action is unclear** (M1).
- **Follow list** is social-media vocabulary; say what happens ("Tell me when this list changes") and that it needs an account.
- **The share bar is too many buttons: yes.** Seven (Share, WhatsApp, Copy link, Facebook, Email, LinkedIn, More) at 36 px height wraps to three rows on a phone, has no label ("Share" next to "WhatsApp" reads as if Share is another channel), and carries equal visual weight to the primary action. Also the visitor has not seen any content worth sharing at this point on the page.
  - Mobile: one **Share** button that opens the native share sheet (which already lists WhatsApp, Telegram, SMS, copy and anything else installed). The prototype has this hidden button but keeps all the others visible. Show only Share, with a visible fallback of **WhatsApp** and **Copy link** where the native sheet is missing.
  - Desktop: **WhatsApp**, **Copy link**, **Email**, and a "More" menu for Facebook, LinkedIn, X. In Pakistan WhatsApp is the sharing channel; LinkedIn matters only for B2B export lists and could be per list-type configuration rather than universal.
  - Position: not above the content. For a list, a quiet "Share this list" line after the results or in the top-right as an icon-with-text; for an entry, in the action area as a single button.
- **S9 Copy link.** The copied URL contains `utm_source=copy&utm_medium=share&utm_campaign=list_share&utm_content=list&ref=DEMO`. Users paste it to others, who then see a tracking-looking link; some will distrust it. Share-to-channel links can carry the parameters; "Copy link" should give the clean canonical URL (plus the contributor's `ref` only when the sharer is a signed-in contributor).
- **Share text** (`"Names free, details by account."`) is awkward, internal and in English. Use a message in the page language: "Surgical instrument makers in Sialkot: 7 listed, last checked 18 Sep 2026. [link]".

### 6.2 Entry page

Current: Contact through AllLists (primary), Request a quote, Save, Report entry, then the same seven share buttons, then an explanatory note. Twelve controls.

Findings:

- **Contact vs Request a quote** are indistinguishable to a buyer: both send a message to the business. The spec says Request a quote is for B2B and trades; that can be a field inside one enquiry flow ("What do you need? Quote / Question / Visit"). One primary button.
- **Wording.** "Contact through AllLists" is the platform's mechanism, not the user's intention. From the user's side: "Message this business" with the reassurance underneath: "Your message goes through AllLists. Their phone and email stay private." The current note says "Phone, WhatsApp and email are stored but never shown. AllLists delivers the message (decision E13)": "stored" sounds like data retention, and "decision E13" is internal.
- **What happens next** is not said: do I need an account, how long until a reply, how will they answer? A buyer sending a message into a relay needs an expectation. Add "Usually answered within X" only when data exists (N3), otherwise "Free. You will get the reply by WhatsApp or email."
- **Save** is a secondary action, fine. **Report entry** should leave this row.
- **Primary on mobile** should be full width (44 px or more) so the thumb target is large; it is currently a content-width button with secondary buttons wrapping beside it.
- **Missing state: no reachable contact.** If the entry has no stored contact (very common for imported and AI-drafted entries), the button cannot work. Define it: "We do not have a way to reach this business yet. Is this yours? Add your number" for owners, and hide the button for buyers. The same applies to owner-verified entries that rely on OTP: it implies a stored number exists, but a not-yet-claimed AI-checked entry may not have one.

### 6.3 Where the owner's actions go

Claim, edit and removal are currently four links in a section at the very bottom ("Correct or claim this entry": Is this yours? Claim, Suggest an edit, Not you? Remove or correct). For supply, the owner's claim is the most valuable action on the site. Put a single quiet line directly under the trust strip: "Is this your business? Claim it. Free, takes about two minutes. We send a code to the phone number we have." and keep one "Report a problem or remove this entry" link at the bottom that opens a form with reasons (wrong, closed, duplicate, this is my business or data, remove my data). That replaces four buttons, plus "Report entry" in the action row, plus the footer Report, and the removal path stays visible as P17 requires.

---

## 7. Remove, merge, move, add (question 6) and stress tests (question 7)

### 7.1 Remove

- Prototype banner content; "Sample list" tag; "National export cluster" tag unless it is phrased for a buyer ("Export hub").
- "Business" tag and the "Open" tag (default state).
- "Show entries not verified yet (moderator view)" checkbox on the public page. Moderator tools do not belong in the public template.
- "Open" button on every row.
- Position on rows (S1).
- The empty "Rankings and reviews" section until reviews exist (S8). It is a section of internal promises ("this block states who may write them"). On a billion pages for years it is dead space.
- Business-type row in Details ("Business type: Manufacturer (a trader is not shown as a maker)") and "Verification tier" row. Both repeat information elsewhere; the second also contradicts the independent-chips rule.
- The "Contact: Through AllLists only" row in Key facts; the action area already says it.
- "Back to the list" inside "In this list" (breadcrumb exists).
- The "Claim it" button from the list-level "Help build this list" (claim is per entry; at list level it is meaningless).

### 7.2 Merge

- "Where this data comes from" and "Contributors and steward" into one "How this list is made" disclosure.
- All routes to report or fix an entry into one (section 6.3).
- Specialities and Product categories (same words twice in the screenshot: "General surgery, Dental" appears in About and in Details).
- Trust section bullets into the chips' one-line text.
- Statistics and trust bar (S2): one object.

### 7.3 Move lower

Share (below content), Areas (below results), About and Statistics (below results), Contributors, Related lists, Help build this list. Advertisement and subscriber panel stay below the results on the list page; on the entry page ads must never sit between the header and the actions.

### 7.4 Missing things a buyer or owner would expect

For a buyer:

- A **legend** for the checks (M5).
- **Pagination or a stated limit** (spec L15). The free-versus-paid moment of truth is the page limit ("Showing 20 of 5,000. Subscribers see all."), and the prototype never shows it. Without it the most important conversion state is unreviewed.
- **Filters promised by the spec** (L10: area, category, speciality, price band). The prototype has only verification and sort. A list of 5,000 needs an area filter at minimum, and the Areas table should be that filter.
- **A link explaining how the list is ordered** (spec L11 requires it once paid ranking exists). The prototype hides this in a small grey note. Because "ranked by verification and completeness" is a business-sensitive claim ("completeness" favours entries whose owners filled in more), explain it once on a page and link it.
- **Similar entries**, previous and next, and a shortlist (N1, N2, N5).
- **Directions**: at area precision only, a free "Open area in map" link; a buyer in Sialkot needs it.
- **Response expectation** for the relayed message (N3).

For an owner:

- A **prominent claim path** (6.3).
- **Reassurance about privacy**: "Your phone and email are not shown to visitors." That sentence is the strongest argument for a Pakistani business owner who has been burned by spam, and it sits in a muted xs note in the action panel.
- **What a complete entry gets** and a view of "what is missing from this entry" for claimed owners only.
- **A correction path** that is faster than "Suggest an edit".

---

## 8. Copy quality (question 8)

Copy should be written from the user's side and in plain words. Rewrites for the most visible strings (English; Urdu to be translated whole, not concatenated, and reviewed by a native speaker):

| Now | Problem | Better |
|---|---|---|
| "7 published, 1 awaiting verification (hidden), 1 closed (hidden)." | Pipeline words, hidden entries advertised | "7 businesses listed. Last checked 18 Sep 2026." |
| "Reach this list" | Unclear object, unclear cost | Depends on the feature; for example "Send an enquiry to several makers" (label free or subscriber) |
| "Follow list" | Social-media term | "Tell me when this list changes" |
| "Statistics for the whole list" | Data-room language | "How well checked is this list?" |
| "Entries with an AI check: 4" | Overlaps, jargon | "3 checked by computer only" in a partition that sums to 7 |
| "With a checkable certificate" | Jargon | "With a certificate you can look up" |
| "Show entries not verified yet (moderator view)" | Internal | Remove |
| "Order: by position in the list, which reflects verification and completeness. Paid placement, when it exists, appears only in the labelled slot below." | "when it exists" is a dev note; "completeness" unexplained | "Sorted by how well each entry has been checked and filled in. Paid listings are shown separately and marked Sponsored. How the order works." |
| "Sponsored (example slot, empty until sold). Labelled, capped at one or two, and never changes the verification order." | Addressed to the founder | When filled: "Sponsored" as a row label. When empty: nothing. |
| "Locked: specialities, certificate, minimum order" | Hostile, repeated | See M3 |
| "Messages go through the Contact button (decision E13)." | Internal ID in a public page | "Your message goes through AllLists. Phone numbers and emails are never shown." |
| "Phone, WhatsApp and email are stored but never shown." | "stored" sounds like surveillance | "Their phone and email stay private. We pass your message on." |
| "Contact through AllLists" | The platform's view | "Message this business" |
| "Owner-verified (Owner, 2026-09-02)" | Tautology, ISO date | "Owner confirmed with a code sent to their phone, 2 Sep 2026" |
| "OTP to stored number" | Mechanism | see above |
| "Surveyor-verified: Visit, checklist 12 of 12" | "checklist" unexplained | "Visited by an AllLists surveyor. 12 of 12 checks passed." |
| "AI-checked: 2 sources matched, confidence 0.82" | Number means nothing | "Computer check: matched 2 public sources." |
| "Claimed: yes. Last updated: ..." | Mislabelled | "Last checked: 18 Sep 2026" |
| "A badge says what was checked, by whom and when. It never claims 'guaranteed genuine'." | An internal commitment as page copy | Keep only the second half as a footer disclaimer: "A check is a record, not a guarantee." |
| "Map pin: 32.4945, 74.5229 (exact, WGS-84)" | Raw coordinates | Address and an "Open in Google Maps" link |
| "Quality or CE" | CE unknown to most readers | "Quality certificate (ISO, CE)" |
| "OEM or private label" | Jargon for local buyers | "Makes to your brand (OEM)" |
| "Size: Staff 50 to 100" | OK | "Staff: 50 to 100" |
| "Not you? Remove or correct this entry" | Unclear who "you" is | "This is about me and I want it removed or corrected" |
| "Apply to steward this list" | "steward" is unusual English | "Become the editor of this list" |
| "This list exists here but is empty. Add the first entry or apply to steward it." | Awkward | "Nobody has listed surgical instrument makers in Gujrat yet. Know one? Add it." |
| "It stays on record so that old links and history still make sense. It is not counted in the list." | Internal | "This business has closed. We keep the page so old links still work." |
| "Add an entry / Suggest an area / Is this your business? Claim it" (list page) | Mixed audiences | "Is a maker missing? Add it" and "Suggest an area" |

Other copy points:

- **Contradiction on the list page:** the About text says "Traders and agents are listed separately", but "Placeholder Trading Co." is in the same list with "Trader" in the type line. It also says "Each entry shows what was checked, by whom and when" and the row shows neither who nor when. Fix the copy or the rows (M6).
- **"Locked" vs "subscriber".** The unlock panel says outreach tools for the whole list are a subscriber feature; the entry page gives every free visitor the Contact button. State clearly which is free: single-entry message free (or with limits), multi-recipient subscriber.
- The `Sources: sample data only. In the real product this line lists each source...` style notes appear in at least a dozen places (e.g., "(sample)", "In the real product", "Baidu and Amap links need a coordinate conversion and are not shown here", "HS code in the real product"). They are fine in a prototype; in the template spec, mark them as "slot" annotations so none ship as copy.
- Entity-specific words are hard-coded: "Business", "Is this your business?", "Established", "Size", "Website". For individuals (see 7.6) they must come from the entity type vocabulary.
- Prices are in USD with a plain number format. For Pakistan-facing lists, PKR and lakh/crore digit grouping (1,50,000) are common; decide the number-format rule per locale.

---

## 9. Consistency and template stability (question 7)

### 9.1 What must be identical on every page

- Header, search, language switch, theme.
- Breadcrumb pattern and title pattern "{List type} in {Place}".
- Scope sentence, trust bar and "last checked" position on the list; name, summary line, trust strip and actions on the entry.
- Chip vocabulary, chip shapes, date format, the single lock treatment.
- Row skeleton: name, descriptor slot, place, checks and date. Same column order, same heights.
- One "what subscribers also see" panel, in one place.
- Report, claim and removal path, and legal footer.
- Sponsored label and ad label treatments, never mixed into the order.

### 9.2 What may vary by list type

- The **descriptor slot** in a row (specialities, specialty, star class, grade range).
- The **add-on block title and rows** on the entry ("Manufacturer details", "Doctor details"), from the registry.
- Which **filters** are offered (area and verification always; speciality or price band as the registry says).
- **Entity wording** (business, clinic, person, school).
- Which **actions** are offered (Request a quote on B2B only; Share hidden for named individuals and child-facing entries).

### 9.3 What must disappear when empty

Reviews, prices, certificates, hours, website, social, sponsored slot, ads (for subscribers), claim prompt (when claimed), add-on rows without data. Rule: **omit rows that have no value; never print "Not stated"** on the entry page. The prototype is inconsistent: "Established" prints "Not stated" for a missing year, while "Hours" always prints a hard-coded value and absent items elsewhere are simply omitted. In tables of many rows (the list), a dash is fine so columns stay aligned.

### 9.4 Stress tests against the code

| Case | What the code does | Result | Fix |
|---|---|---|---|
| **Long business name** (e.g. "M/S Muhammad Ibrahim and Sons Surgical Instruments Manufacturers (Pvt.) Ltd.") | `minmax(0,2fr)` column wraps; H1 `text-wrap:balance` | Works. No `overflow-wrap` rule, so long URLs and unbroken strings (website, email) can still overflow on a phone. | `overflow-wrap:anywhere` on text containers |
| **5,000 entries** | `rows.forEach` prints all; no pagination; "7 of 7 shown" | A 5,000-row DOM; the free limit state is never shown; "Position 3,412 of 5,000" is meaningless | Page size and stated limit; paginate; drop position on rows (S1) |
| **40 specialities** | `e.spec.join(", ")` in the subscriber row and on the entry | A ten-line comma wall per row and per entry | Show the first 3 and "+37 more" in rows; tags with "show all" on the entry |
| **400 areas** | Full table of every area before results | A very long table above the results | Top 8, "all N areas" link; use as a filter (S3) |
| **No phone, no contact** | The Contact button is always shown | A button that cannot work, on most imported entries | Define the no-contact state (6.2) |
| **No hours** | Hours row is hard-coded for everyone | Fake data in the template; real absence is not handled | Omit the row when absent; support "24 hours", split shifts, a Friday break, "by appointment" |
| **No website, no social** | Locked for free, sample for subscriber | Absence is not handled | Omit when absent |
| **Individual instead of business** | "Business" tag, "Is this your business?", "Established", "Size", "Website", "Position 3 of 12" | The entry and list read wrongly; ranking people publicly is hostile; consent not visible | Entity-type vocabulary; no position for people; a consent chip in the trust strip ("Listed with the person's consent"); area only, no street |
| **Children's tutors** | Template renders as any other entry | Spec says "not public until safeguarding is designed" but there is no suppressed state | Define a "centre-only" or "relay-only" variant: no personal name in shares, no share button, Report foregrounded, no exact area below a threshold |
| **Verification with many checks** | Chip row and detail chips nowrap | Horizontal overflow on a 390 px phone | Allow wrap; detail on a second line |
| **Trader in a makers list** | Shown inline with "Trader" in the type line; About says "listed separately" | Contradiction | Either separate section or fix the text; use the descriptor slot to mark it |
| **Closed entry** | Same actions as open entry (code: the action panel is unconditional) | A visitor can message a closed business | M9 |
| **Zero or one result after a filter** | "No entries match this filter." | Fine, but no way to clear the filter | Add "Clear filters" and a count |
| **Sponsored entry with no verification** | Not specified | A paid slot could hide that the business is unchecked | The sponsored row must show the same chips and date, including "Not verified yet" |
| **Page length at 7 entries** | 5,600 px list, 4,500 px entry | Both will grow with real data | Cut as above |

### 9.5 Dark theme and touch

The dark tokens work (screenshots show readable chips and good primary contrast). `.row.closed{opacity:.7}` lowers contrast on already grey text; use a label. `.btn.sm` and selects are 36 px tall (below the 44 px recommendation, relevant for phones used one-handed outdoors), and chip and note text is 13 px. The chips carry the trust information and should be 14 px at least.

---

## 10. Urdu and right-to-left (question 9)

What works: the whole layout mirrors via logical properties; breadcrumbs, headings, the row grid, tables (columns reverse order correctly) and buttons flip; the primary action sits at the reading start in each language.

What does not read naturally (all seen in the Urdu screenshots):

1. **Concatenated strings** break under bidi. "7 of 7 shown" renders as "of 7 shown 7"; "Locked: subscribers" renders as "subscribers :مقفل"; "Position 1 of 7" stays English. Fix: whole-sentence message strings per language with named placeholders (for example "{shown} of {total} shown"), never `a + ": " + b`.
2. **Mixed-language blocks.** In Urdu mode the code sets `dir="auto"` on each `p`, `ul`, `dd` and `td`. An English paragraph then left-aligns inside an otherwise right-aligned page, giving ragged edges (visible in About, Statistics note and the unlock panel). This is partly a symptom of untranslated copy, but the real fix is full translation plus `<bdi>` and `unicode-bidi:isolate` for inevitable embedded Latin (URLs, ISO names, numbers), not block-level `dir`.
3. **Chips and status stay English** in Urdu mode. M11.
4. **Second name floats to the opposite edge.** The Urdu name is a `dir="rtl"` block on an LTR page, so it right-aligns to the far edge while the English name is left-aligned (visible on the mobile list rows and the entry header). Make the second name `display:inline-block` or place it on the same line after the first, so the pair reads as one unit; in Urdu mode the two swap.
5. **Type size and leading.** Urdu in a Naskh stack at 16 px and line-height 1.55 looks smaller and cramped next to Latin text at the same size; marks collide. Add `:lang(ur){font-size:1.125em;line-height:1.9}` and use 14 px+ in chips. Pakistani readers usually expect Nastaliq; most Android phones do not ship a Nastaliq face and the no-web-fonts rule means the Naskh fallback will often be used. This is a trade-off for the founder to acknowledge; test on two or three cheap Android phones.
6. **Numerals and dates.** Choose Western or Urdu digits per page and stay consistent; dates and phone-like strings should be isolated as LTR. Lakh/crore grouping for PKR.
7. **Stats table gap.** In RTL the value lands at the far left edge, about 900 px from its label on desktop (in LTR the gap is also roughly 340 px). Constrain the table to about 28 rem or use label-then-value rows with a leader line.
8. **Prototype-only controls** appear in the same RTL flow; ignore for the product but note the segmented controls reverse order.
9. **Shared text** (share messages and the `Report` link text in the footer) is partly English in Urdu mode; the footer line mixes "Report" in Urdu with English sentences and renders broken.

---

## 11. Empty list and closed entry

**Empty list (`#/empty`).** The structure is right and this page will be the most common page on the site, so it matters most for scale.

- Primary action is "Add an entry", a contributor action; a buyer who arrived from search has no path except a hard-coded sibling link. Add, in order: nearest lists that do have entries (the parent roll-up "Surgical instrument makers in Punjab, 7 listed"), "Tell me when this list has entries" (follow), then the contributor actions.
- "Apply to steward" is jargon (section 8).
- The explanatory grey note ("Most list pages are empty at the start... not indexed by search engines") is a developer note; do not ship it.
- Write it from the visitor's side (section 8 rewrite).

**Closed entry (`#/entry/e9`).** The notice block is good placement. Problems: M9 (outreach still offered, check chips still shown as live), the notice text is internal, and the position text says "Not ranked" even though closed entries are excluded. Lead with the closed status in the H1 area, replace the action panel with "Report a mistake" only, and show the last verification as "last checked before closing".

---

## 12. The design system page

It is useful and accurate to the code. Gaps that matter for replication:

- It documents tokens but not **template rules** (section 9). Add the identical/varies/omit-when-empty tables.
- It lists chips but not the **legend wording**, the **closed variant** or the **detail variant** used on the entry.
- "Buttons and markers" shows `.lock`, `.spons`, `.ad` all with dashed borders: three meanings, one look (M3).
- It states "Rules every page follows: same sections in the same order on every page" while the entry sections are different from the list; make that "same order within each page type".
- Add the row skeleton, the trust strip and the "what subscribers also see" panel as named components, because they are the pieces that will be copied a billion times.

---

## 13. Suggested next steps for the owner

1. Approve the free/subscriber table (M4) and the list-page order (M2); these two decisions unlock most other changes.
2. Rewrite the trust wording (section 5) and test it with five Pakistani buyers and five shop owners, in Urdu, before the template is frozen.
3. Specify empty and edge states in the component spec (section 9.3 and 9.4) so they exist before there are real entries.
4. Treat Urdu as a first-class build, not an afterthought: translate chips, whole strings, type scale, and test on cheap Android phones.
5. Re-render the screenshots after these changes and re-check: first screen on a phone, row height, number of non-content blocks above the first result (target: two), and number of lock markers on a free entry page (target: one).
