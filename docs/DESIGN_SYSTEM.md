# AllLists.org: design system for the list and entry page template (v1)

This is the design contract for the one page template that will be repeated for every list and every entry. It is built from the working prototype (`prototype/alllists-prototype.html`, also the living style guide at `#/system` inside it), the component specification (`docs/LIST_AND_ENTRY_COMPONENTS.md`) and two independent reviews (`research_notes/Design review/`). Text and numbers only (C29). Decisions in `docs/DECISIONS.md` are not reopened.

Status: v1 for owner sign-off (Q-S12). The Urdu wording is a draft that needs a native speaker.

## 1. How the design was checked

- The design guidance in the design tools was applied: one token system, ruled sections instead of stacked cards, both themes, consistent repeated parts, plain copy, no templated "AI look".
- The account has a design canvas type available but no design system attached; the design-sync tool only syncs designs held in your claude.ai design projects, so it was not used.
- Two independent reviewers examined the prototype: user experience and information design (12 must-fix, 14 should-fix findings), and accessibility, language and speed (5 must-fix, several should-fix). Every must-fix finding that applies to the prototype is fixed; the rest is listed in section 11.

## 2. Principles

1. **A register, not a feed.** Title, one-line scope, trust line, then filters and results. Everything else sits below the results.
2. **Trust before action.** The check labels and their dates are visible on every row and every entry. A key explains them in plain words.
3. **One fixed line between free and paid.** One panel names what subscribers also see. No lock box on every field.
4. **Contacts are never shown.** One message button. Phone, WhatsApp and email stay private (decision E13).
5. **Rows with no value are left out.** The page never says "Not stated".
6. **Light by design.** System fonts, no third-party scripts, no images. A server-rendered list page of 25 rows should be about 11 KB compressed (budget in section 9).
7. **Right-to-left from the start.** Logical CSS (start and end), never left and right.

## 3. Tokens (single source in the page's style block)

| Token group | Values (light / dark) | Notes |
|---|---|---|
| Paper, surface | `#f5f7fa`, `#ffffff` / `#0c111d`, `#131a29` | Cool neutrals biased toward the accent |
| Ink, ink-2 | `#101828`, `#475467` / `#f2f4f7`, `#a4aebd` | Text; muted text passes 4.5:1 on paper and surface |
| Rule, control | `#d0d5dd`, `#667085` / `#2a3447`, `#8592a8` | Rule is decorative; control borders pass 3:1 |
| Accent | `#1d4e89` / `#84adff` | The only accent colour |
| Semantic | ok `#067647` / `#47cd89`; bad `#b42318` / `#f97066`; warn `#fef0c7` and `#7a2e0e` / `#3a2a07` and `#fec84b` | Separate from the accent. Never the only signal |
| Focus | `#b54708` / `#fec84b` | 3 px outline |

Theme rule: every colour is a token defined on the bare root, redefined for dark under the system preference unless the user chose light, and under an explicit dark choice. The theme switch stores the choice in the browser.

## 4. Type and space

| Role | Size | Use |
|---|---|---|
| Page title | 28 px | One per page |
| Section title | 18 px (page sections), 22 px reserved | |
| Row title | 18 px, semibold | |
| Body | 16 px, up to 68 characters a line | |
| Small | 15 px | Notes, descriptors |
| Caption | 14 px | Never below 14 |
| Mono | system mono | IDs, codes |

- Fonts: system stacks only. Urdu falls back to a Naskh face. Nastaliq is the usual Urdu print style but loading it costs data; that choice is open (Q-S14).
- Urdu pages: body 18 px with line height 1.95, titles line height 1.6. Urdu letters need the room.
- Numbers use tabular figures. Digits are Western (0 to 9) in all languages for consistency across Pakistan and the Gulf.
- Space is a 4 px scale (4, 8, 12, 16, 24, 32). Spacing uses gap and logical padding, never margins that collapse.

## 5. Parts (components)

| Part | Rule |
|---|---|
| **Breadcrumb** | One row, place only (global to area). The list type shows as a tag. |
| **Title and scope** | Title "{List type} in {Place}". One sentence of scope. |
| **Trust line** | "{n} businesses listed. Last checked {date}." and a split that adds up to the total: visited by a surveyor, confirmed by the owner, checked by computer only. A tap-to-open key explains each check in plain words. |
| **Check labels** | The four decided names, with shape and words (solid thick, solid, dashed, dotted). Colour never carries meaning alone. Wrap on small screens. |
| **Primary action** | One per area. List: "Send one enquiry to several makers" (subscribers). Entry: "Message this business". Secondary: save, or "Tell me when this list changes". |
| **Share** | One native Share button where the browser supports it, plus WhatsApp and Copy link. Facebook, email, LinkedIn and X sit under "More options". Copy link copies the clean address without tracking tags. |
| **Filters** | Area, check type, sort. Changing one keeps focus where it was, announces the new count, and does not jump the page. "Clear filters" appears when any filter is on. |
| **Result row** | Name (and the other-language name), type and area, up to three specialities and "+n more", check labels, "Checked {date} · {age}". No position number, no open button, no lock boxes. |
| **Paging** | Five rows, then "Show n more". A stated per-account limit for free visitors. |
| **Subscriber panel** | One panel per page naming what subscribers also see, built from the fields that exist for that entry, with one button. |
| **Sponsored** | An empty slot shows nothing. A filled slot is a normal row with a Sponsored label and the same checks and date. |
| **Advertising** | Free visitors only, below the results, labelled. |
| **Key facts** | A definition list. Only rows that have a value. |
| **Records** | Prices and certificates are stacked records (item, value, date), not wide tables, so they read on a phone. |
| **Something wrong?** | One section at the bottom of every list and entry: report, claim, suggest a correction, remove or correct my data. |
| **Footer** | "A check is a record, not a guarantee. Listings are not endorsements." Privacy and opt-out. Report. |
| **Notices** | Closed entry: a left-ruled notice, messaging removed, checks shown as past. |
| **Empty list** | A designed page: what is missing, who can add it, link to the nearest filled list. Marked noindex but followed. |

## 6. States every page must handle

| State | What the page does |
|---|---|
| Empty list | Empty-state panel; no results block |
| One or zero results after a filter | Count and "Clear filters" |
| More than five results | "Show n more" and the free limit |
| Not verified yet | Hidden from the public list; the list counts only published entries |
| Closed entry | Closed notice, no message button, checks shown as past |
| Missing contact, hours, website, social | The row is left out, the page never says "Not stated" |
| Many specialities | First three on a row, all on the entry as tags |
| Long names | Wrap; long strings break |
| Individuals | Words come from the entity type; no ranking of people; area only; consent shown; share hidden (see the specification) |
| Children's services | Relay-only variant: no personal name in shares, no share button, Report foregrounded |
| Sponsored entry that is unchecked | Shows "Not verified yet" like any other row |

## 7. Language and right-to-left

- English is the source. Urdu is translated as whole sentences with placeholders, never joined from pieces.
- Names appear in both scripts: the main name in the page language, the other below it, each isolated so punctuation stays put.
- Dates read "18 Sep 2026" in English and use the Urdu month names in Urdu, with an age ("2 weeks ago").
- Controls, tables, breadcrumbs and the row grid mirror automatically.
- Test every release in English and Urdu at 320, 390 and 1100 px.

## 8. Accessibility rules

- Text contrast at least 4.5:1, controls and borders at least 3:1, in both themes. Checked.
- Touch targets at least 44 px.
- One heading level 1, then level 2 sections; landmarks for header, main, footer; a skip link to the results.
- Keyboard: every control reachable, visible focus ring, focus kept after a filter change. Status announcements use one polite region, not the whole page.
- Forced-colours mode keeps borders and the pressed state.
- Reduced motion respected. No motion is used.

## 9. Performance and search rules (budget proposed by the reviewer)

| Item | Budget |
|---|---|
| Requests | One (HTML with inline CSS), no web fonts, no third-party scripts |
| List page, 25 rows | About 11 KB compressed |
| Entry page | About 7 KB compressed |
| Works without JavaScript | Yes in the real product; JavaScript only improves filters and sharing |
| Titles | Unique per page: "{Name} – {List type} in {Place} – AllLists" |
| Canonical | Clean address without tracking tags |
| Empty lists | noindex, follow |
| Structured data | Names and addresses only, matching what is visible; no locked fields |

The prototype builds its page in JavaScript for convenience. The production page is server-rendered.

## 10. What is identical on every page and what may vary

Identical: header, search, theme and language, breadcrumb and title pattern, the order of sections, check labels and dates, the subscriber panel, the report path, the legal footer, the sponsored and advertising labels.

May vary by list type: the descriptor shown in a row, the details block, extra filters, the words for the kind of thing, and which actions exist.

## 11. Findings not yet applied (for the build phase)

| Item | Why it waits |
|---|---|
| Server-rendered pages, canonical tags, structured data, per-page titles | Belongs to the production build; the prototype only simulates titles and robots |
| Urdu wording review by a native speaker; Nastaliq versus Naskh | Needs a person; Q-S14 |
| Real phone and screen-reader testing | Needs devices and people |
| Prev and next inside a list, similar entries, open-now from hours, shortlist and enquiry to several | Later features |
| Individuals and child-facing variants as built pages | Specified in section 6; built when those lists launch |
| Price and number formats per locale (PKR, lakh and crore grouping) | Decide with the first priced list |
| Whether "Send one enquiry to several makers" is subscriber-only or limited-free | Pricing decision (Q-N1, Q-N5) |

## 12. Open decisions

| # | Decision | Suggested default |
|---|---|---|
| 1 | Urdu type style | Naskh system fallback now; Nastaliq later if data cost allows (Q-S14) |
| 2 | Accent colour and logo | Keep the blue accent; logo wordmark only until a name decision |
| 3 | Wording of the four check labels | Keep the decided names; add the plain key |
| 4 | Number format by locale | Western digits; grouping decided with the first priced list |
