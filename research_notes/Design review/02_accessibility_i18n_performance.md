# Review 02: accessibility, internationalisation and performance of the page template

Reviewer: independent (accessibility, i18n, performance). Date: 2026-10-05.
Scope: `prototype/alllists-prototype.html` (routes `#/list`, `#/entry/e1`, `#/empty`, `#/entry/e9`, `#/system`), read against `docs/LIST_AND_ENTRY_COMPONENTS.md`. `docs/DECISIONS.md` is respected and not reopened. No repository file was changed.

How I tested: Playwright 1.x with Chromium (headless), widths 320, 390 and 1100, English and Urdu, free and subscriber views, light and dark, forced-colors and reduced-motion emulation, JavaScript off, CPU throttling 4x and 6x. Contrast ratios are computed from the token hex values with the WCAG 2.x formula. Scripts and raw output are in the scratchpad (`/tmp/claude-0/scratchpad/rev/`), not in the repository.

Limits you should know about:
- Chromium only. No real Android phone, no screen reader (NVDA, TalkBack, VoiceOver) was run. Screen-reader statements below are reasoned from the markup and from measured focus and DOM behaviour, and are marked "not heard".
- The container has no Urdu or Naskh font (only DejaVu and Unifont for Arabic script). The existing `v2_*_ur*.png` screenshots therefore show DejaVu glyphs, not what a Pakistani phone shows. For typography checks I loaded Noto Naskh Arabic and Noto Nastaliq Urdu (from npm `@fontsource`, outside the repo) into the page at test time only.
- The Urdu strings are judged by a non-native reviewer. Treat section 4.5 as questions for the native speaker, not corrections.

---

## 0. Ranked summary

### Must fix (before this becomes the template)

| # | Finding | Evidence | Fix |
|---|---|---|---|
| M1 | The page does not exist without JavaScript. `<main>` is empty in the HTML; everything, including `lang`/`dir`, `<title>` and all links, is built in JS. | JS off: `#app` text length 0, only "English اردو · · AllLists" in body. Hash routes (`#/list`) are not URLs a crawler or WhatsApp can fetch. | Server-render real documents with real URLs. See section 5.3 for the exact list. |
| M2 | Every route has the same `<title>` ("AllLists page template") and a constant meta description; no canonical; no robots meta; no structured data. | `document.title` identical on all 5 routes. | Per-page title, description, canonical, robots, hreflang (in the sitemap), BreadcrumbList. Section 6. |
| M3 | Strings are built by concatenation in JS ("Position "+rank+" of "+pub, "Locked: "+x, "N of M shown"). 61 of 110 text nodes on the Urdu entry page and 72 of 149 on the Urdu list page are English, with no `lang="en"`. Urdu word order and Arabic plural forms (six categories) cannot be expressed. | Counted in Playwright (section 4.4). | Whole-sentence message templates with placeholders and CLDR plural rules (ICU MessageFormat or equivalent); tag every foreign-script fragment with `lang`. Do this now; it is the hardest thing to retrofit across a million pages. |
| M4 | Text and borders that fail contrast: (a) input, select and secondary-button borders (`--rule`) are 1.37 to 1.51:1, the WCAG minimum for UI component boundaries is 3:1; (b) the search placeholder is 4.29:1 light and 4.09:1 dark (browser default grey); (c) `.row.closed{opacity:.7}` drops ink-2 to 3.48, ok-green to 3.04, bad-red to 3.63, accent to 3.76 (light). | Section 1. | Add a `--field-border` token (light `#7a8294`, dark `#667085`), set `::placeholder{color:var(--ink-2)}`, replace the opacity with a muted style that keeps tokens. |
| M5 | Filter, sort and checkbox controls re-render the whole `<main>`: keyboard focus is lost to `<body>` and the page scrolls to the top. `<main aria-live="polite">` means a screen reader is likely to be told to re-read the entire page each time. | After changing `#so`, `#fl` or `#uv`: `document.activeElement` = BODY, `scrollY` = 0 (measured, all three). | Real product: a GET form with a visible "Apply" button that loads a new URL (works without JS). Remove `aria-live` from `<main>`. If any in-place update is kept, update only the results list, keep focus, and announce one short status line. |
| M6 | Entry page overflows horizontally at 320 px. | `#/entry/e1` at 320: `scrollWidth` 389 vs `clientWidth` 320 (EN and UR, free and sub). Cause: `.chip{white-space:nowrap}` with detail text "Surveyor-verified (Surveyor S-101, 2026-09-18)". At 390 the chip already sticks out 6 px past the 16 px gutter. | Allow chips to wrap (`white-space:normal`), or split the chip label from the who/when text. |
| M7 | Urdu line-height is wrong for Nastaliq and tight for headings: `body` 1.55, `h1` 1.2. With Noto Nastaliq Urdu the h1 collides with the breadcrumb above and the tags below (screenshot `u_nast_list.png`). | Section 4.3. | `:lang(ur)` line-height 1.9 for body, 1.7 to 1.9 for headings; `letter-spacing:0` on Arabic-script text. |
| M8 | Toast is not reliably announced and disappears after 1.8 s. The `role="status"` element is `display:none` until the text is set (a live region that appears and fills in the same moment is often not announced); the text is English even in Urdu mode. | Measured: initial `display:none`; class removed after 1.8 s. | Keep the status element in the DOM (visually hidden when empty), set its text after, show for at least 5 s, translate the message. In forced colors it also has no border and overprints page text (`forced_toast.png`). |

### Should fix

| # | Finding | Evidence |
|---|---|---|
| S1 | Touch targets: 47 of 55 interactive elements on the list page, 22 of 30 on the entry page, are under 44 px in height (or width) at 390 px. Share buttons, selects 36 px; breadcrumb links 18 px; row name link 19 px; related-list links 19 px; checkboxes 13 px; footer links 15 px. | Section 3. |
| S2 | Every list row has two links to the same entry: the name and an "Open" button. Two tab stops per row (50 for a 25-row page), and the name "Open" repeated seven times is not descriptive. | Section 2. |
| S3 | Focus ring is clipped on the segmented controls (`.seg{overflow:hidden}`); only a sliver is visible. The same pattern would break a real language switcher. | `focus_seg2.png`. |
| S4 | Segmented groups (`.seg role="group"`) have no accessible name (all three: `aria-label` and `aria-labelledby` are null). | Measured. |
| S5 | Landmark and heading details: the results heading is "7 of 7 shown" (not a useful name); the results `<section aria-label>` repeats it; the two breadcrumb `<nav>`s have English-only `aria-label`s ("Place", "List type", "Breadcrumb") even in Urdu; empty table cells for locked prices; `title` attributes carry the "who, when, how" of a verification chip (not available on touch or keyboard). | Section 2. |
| S6 | Dates break across lines at the hyphen ("2026-" / "09-18") on narrow screens. | `ent_ur2.png`; Hours row. Wrap dates in `<time datetime>` with `white-space:nowrap`. |
| S7 | Mixed-direction handling uses `dir="auto"` on blocks (`p`, `ul`, `dd`, `td`), so English values on an Urdu page flip to left alignment next to right-aligned labels. | `ent_ur2.png`. Use page direction for blocks and `<bdi>` plus `lang` for inline foreign fragments. |
| S8 | Urdu and Arabic body size: 13 px (`--t-xs`) is used for notes, table headers, chips, locks, footer. Arabic-script text at 13 px is hard to read on a low-end phone. | Section 4.3. |
| S9 | Forced colors (Windows high contrast): the pressed state of the segmented buttons is nearly invisible (white fill vs transparent, differs only by bold), primary and secondary buttons look the same (white fill, black border, differ only by weight), the toast has no boundary. | Section 7. |
| S10 | Share links and map links open new tabs with no warning to assistive technology. A lone "More" disclosure holds one link ("X") and a developer note. | Section 2. |
| S11 | Sections that scroll (`.tablewrap{overflow-x:auto}`) are not keyboard focusable. They did not overflow in my tests, but the first real table with long values will. | Add `tabindex="0"`, `role="region"` and a label, or avoid horizontal scroll. |
| S12 | First entry row is 2,307 px down the page at 390 px (page height 5,628 px, 2.7 screens). On a slow phone the names, which are the content people came for, arrive after about 1,800 px of explanatory text, statistics and filters. | Section 5.5. |

### Nice to have

N1 Skip link (cheap; the real header has only three stops). N2 `role="list"` on list-style:none lists for Safari VoiceOver. N3 `<meta name="color-scheme">` and `theme-color`. N4 `dir="auto"` on the search input. N5 Remove the reduced-motion rule or keep it as an explicit guard (the page has no animation today). N6 Breadcrumb separator is a plain "/" in both directions; in RTL a mirrored chevron reads better. N7 Inline `style=""` attributes (11) block a strict Content Security Policy.

---

## 1. Colour contrast (WCAG 2.x)

Tokens are in `:root` (light) and in the dark blocks. Ratios below are computed from hex. Thresholds: 4.5:1 normal text, 3:1 for large text and for UI component boundaries or states.

### 1.1 Text pairs, light theme

| Pair | Ratio | Result |
|---|---|---|
| ink `#101828` on paper `#f5f7fa` | 16.54 | pass |
| ink on surface `#fff` | 17.75 | pass |
| ink-2 `#475467` on paper | 7.16 | pass |
| ink-2 on surface | 7.69 | pass |
| ink-2 on lock `#eaecf0` | 6.50 | pass |
| accent `#1d4e89` on paper | 7.82 | pass |
| accent on surface | 8.39 | pass |
| accent on lock | 7.09 | pass |
| accent-ink `#fff` on accent (primary button) | 8.39 | pass |
| ok `#067647` on paper | 5.30 | pass |
| ok on surface | 5.69 | pass |
| ok on lock | 4.81 | pass |
| bad `#b42318` on paper | 6.13 | pass |
| bad on surface | 6.57 | pass |
| bad on lock | 5.56 | pass |
| warn-ink `#7a2e0e` on warn-bg `#fef0c7` (prototype bar, sponsored box) | 8.32 | pass |
| ink-2 on warn-bg | 6.77 | pass |

### 1.2 Text pairs, dark theme

| Pair | Ratio | Result |
|---|---|---|
| ink `#f2f4f7` on paper `#0c111d` | 17.12 | pass |
| ink on surface `#131a29` | 15.78 | pass |
| ink-2 `#98a2b3` on paper | 7.32 | pass |
| ink-2 on surface | 6.75 | pass |
| ink-2 on lock `#1d2636` | 5.90 | pass |
| accent `#84adff` on paper | 8.44 | pass |
| accent on surface | 7.79 | pass |
| accent on lock | 6.80 | pass |
| accent-ink `#0c111d` on accent | 8.44 | pass |
| ok `#47cd89` on paper / surface / lock | 9.31 / 8.58 / 7.49 | pass |
| bad `#f97066` on paper / surface / lock | 6.77 / 6.24 / 5.45 | pass |
| warn-ink `#fec84b` on warn-bg `#3a2a07` | 8.97 | pass |
| toast: paper on ink (both themes) | 16.54 / 17.12 | pass |

All the token pairs for text pass 4.5:1 in both themes. The weakest are ok on lock (4.81, light) and bad on lock (5.45, dark); neither is a combination the page currently uses for the chip, but keep it in mind if chips are ever placed on `--lock`.

### 1.3 Text that fails because of how the tokens are used

| Where | Computed | Ratio | Result |
|---|---|---|---|
| `.search input::placeholder` (browser default `rgb(117,117,117)`) on paper | measured in Chromium | light 4.29, dark 4.09 | **fail** (4.5 needed) |
| `.row.closed{opacity:.7}`, light: ink-2 text (muted Urdu alt name) | 3.48 | **fail** |
| same, ok-green chip text (an owner-verified chip on a closed row) | 3.04 | **fail** |
| same, bad-red chip text ("Permanently closed") | 3.63 | **fail** |
| same, accent link | 3.76 | **fail** |
| same, ink (the name) | 6.36 | pass |
| `.row.closed{opacity:.7}`, dark: ink-2 | 4.13 | **fail** |
| same, bad | 3.81 | **fail** |
| same, accent / ok / ink | 4.67 / 5.08 / 8.68 | pass |

The closed rows are shown only when the "Show closed entries" box is ticked, but the entry page for a closed business is the page most often reached from old links, and the pattern will be copied. Fix: remove `opacity`; keep full-contrast text and mark the row with the existing "Permanently closed" chip, a dashed rule or a muted left border.

### 1.4 Non-text pairs (3:1 for UI component boundaries and states)

| Element and pair | Light | Dark | Result |
|---|---|---|---|
| Input / select / secondary button border `--rule` on paper | 1.37 | 1.51 | **fail** |
| `--rule` on surface | 1.47 | 1.39 | **fail** |
| Search input background (paper) against header (surface) | 1.07 | 1.08 | no help from fill |
| Chip border (`--ink-2`) on paper | 7.16 | 7.32 | pass |
| `ok` and `bad` chip borders | 5.30 / 6.13 | 9.31 / 6.77 | pass |
| `.tag` border (rule), `.lock` dashed border (rule), panel and section rules | 1.25 to 1.47 | 1.22 to 1.51 | decorative; the text inside carries the meaning, so not a failure |
| Focus ring `--focus` (3 px, 2 px offset) on paper / surface / lock / warn-bg | 5.06 / 5.43 / 4.59 / 4.78 | 12.19 / 11.24 / 9.82 / 8.97 | pass |
| Focus ring on accent (primary button fill) | 1.55 | 1.44 | would fail, but the 2 px offset puts the ring on the page background, so it passes in practice |
| Pressed seg button: `--warn-ink` fill vs `--warn-bg` | 8.32 | 8.97 | pass |

Real failures (WCAG 1.4.11): the borders that define text inputs, selects and the search box (1.37 to 1.51:1). The secondary `.btn` (surface fill, rule border, text label) is a borderline case: the visible text identifies it, but a user with low vision sees a nearly invisible box. Treat it the same.

Proposed new token, tested against paper, surface and lock:

| Theme | `--field-border` | on paper | on surface | on lock |
|---|---|---|---|---|
| light | `#7a8294` | 3.59 | 3.85 | 3.26 |
| dark | `#667085` | 3.79 | 3.50 | 3.05 |

Use it for `input`, `select`, `.btn` (non-primary). Keep `--rule` for dividers. Placeholder: `::placeholder{color:var(--ink-2);opacity:1}` gives 7.16 light and 7.32 dark.

### 1.5 Colour used as the only signal

Passes. The chips use border style (solid, 2 px solid, dashed, dotted) plus words, as the design system page says. Keep that rule when adding statuses.

---

## 2. Keyboard and screen-reader semantics

### 2.1 What is good

- One `<h1>` per route (measured on all five). Heading order is h1, then h2s with no skipped levels.
- Landmarks: `header` (banner), `form[role=search]`, `main`, `footer` (contentinfo). Search has a visually hidden `<label for="q">` and a button.
- Real tables with `<th scope="row">` for the statistics table and `<thead>` for the areas table; `<dl>` for key facts; `<ol>` for results; `<ol>` in `<nav aria-label>` for breadcrumbs with `aria-current="page"`.
- `aria-pressed` is used on genuine toggle buttons (view, theme, language). The "More" control is a correct disclosure pattern: `aria-expanded` and `aria-controls`; the toggle updates (measured: `true` after click). Escape does not close it, which is acceptable for a disclosure.
- The viewport meta does not block zoom; inputs use 16 px text so iOS does not zoom on focus.
- Share group: `role="group"` with a translated `aria-label`. Native share button is hidden until `navigator.share` exists (a good progressive-enhancement pattern; keep it for copy-link too).

### 2.2 Problems

1. **Whole-main live region (M5).** `<main id="app" aria-live="polite">` receives a full `innerHTML` replacement on every filter, sort, plan, language change. Not heard on a screen reader, but a polite live region whose entire content is replaced is expected to be read in full. In the real product `<main>` must not be a live region; at most a single `role="status"` line that says "7 of 25 shown".
2. **Focus and scroll loss on change (M5).** Measured after changing sort, verification filter and the "show unverified" box: `document.activeElement` is `BODY` and `scrollY` is 0. A keyboard or switch user must tab again from the top; a TalkBack user loses their place. Also WCAG 3.2.2 (changing a select must not unexpectedly change context): the select changes results at once with no "Apply".
3. **Route changes.** Navigation is by `hashchange` with no focus move, no title change and no announcement. In the real product each route is a real page, so the browser handles it; do not reintroduce client routing for the common path.
4. **Unnamed groups (S4).** The three `.seg` groups have no name; the visible caption ("Viewing as", "Theme", "Language") is not associated. These are prototype controls, but the language switch is a real component: make it a nav with links (section 5.3), or a group with `aria-labelledby`.
5. **Duplicate links per row (S2).** Each result row links the same entry twice (`a.nm` and `a.btn "Open"`). The "Open" label is the same seven times. Remove the button; make the name the single link; keep the whole row tappable with a stretched link (`a.nm::after{content:"";position:absolute;inset:0}` on a `position:relative` row) so the touch target is the row.
6. **Results heading (S5).** `<h2>7 of 7 shown</h2>` is the heading screen-reader users jump to. Make it "Entries" (translated) and put the count in a following `<p>`. Use `aria-labelledby` on the section instead of a duplicate `aria-label`.
7. **Navigation names (S5).** `nav[aria-label="Place"]`, `nav[aria-label="List type"]` and `nav[aria-label="Breadcrumb"]` are hard-coded English (measured in Urdu mode: still "Breadcrumb"). There are two breadcrumb landmarks on a list page; one landmark with two `<ol>`s, or one trail, is less noisy.
8. **`title` as the only home for verification detail (S5).** `<span class="chip" title="Surveyor S-101, 2026-09-18, Visit, checklist 12 of 12">`. `title` is not available on touch, is inconsistently exposed to screen readers, and is not keyboard reachable. On the entry page the same detail is already printed in the list below the chips, so this is only a problem on list rows. Use visible text (the spec's "click for what was checked" needs a `<details>` or a link to the entry's Trust section).
9. **Empty cells.** The price and certificate tables have `<td></td>` for locked rows; announced as "blank". Put an em dash with `<span class="visually-hidden">not available</span>`.
10. **Language of fragments (M3).** `<html lang="ur">` is set in Urdu mode, so every English fragment (type, area, chip labels, notes) is announced by a screen reader with an Urdu voice. 61/110 (entry) and 72/149 (list) text nodes affected in the prototype. In the real product the whole page is translated, but names, areas and user-entered text will still arrive in other scripts: tag each with `lang`.
11. **External links (S10).** `target="_blank"` links (WhatsApp, Facebook, LinkedIn, X, maps) give no warning. Add a small visually hidden "(opens in a new tab)" or drop `target="_blank"` and let users choose. `rel="noopener noreferrer"` is correct.
12. **Toast (M8).** `role="status"` on an element that is `display:none` until used. Keep it in the layout tree (position fixed, visually hidden when empty) and change only its text. Four seconds is the usual minimum; give a Close or leave it long enough to read.
13. **Pointer-only hint.** The "More" menu contains one link ("X") and the text "Telegram, QR code and embed come later." That is a development note rendered in the product UI; remove it, and consider removing "More" until it holds at least three items.
14. **Scrollable regions (S11).** `.tablewrap` scrolls but cannot take focus. Add `tabindex="0" role="region" aria-label="..."` only if the table can overflow.
15. **Primary actions that need JS.** "Contact through AllLists", "Request a quote", "Follow/Save" are `<button>`s that show a toast. In the real product these must be links or forms (to a sign-in or contact form page) so they work without JS and are reachable by crawlers and by Opera Mini.

### 2.3 Focus order and skip link

- Tab stops before the first content element: 13 in the prototype (10 are the prototype bar). In the real product: logo, search field, search button = 3, then breadcrumbs. A skip link is not required by WCAG 2.4.1 here because landmarks and headings already bypass blocks; it costs about 100 bytes and helps keyboard-only and switch users on a page with 7 to 10 breadcrumb links. Nice to have (N1).
- The list page has 59 tab stops with 7 rows; with 25 rows and the duplicate "Open" it would be about 100. After removing "Open" and collapsing the share row into the native share button where available (already hidden by default) it falls to about 60.
- The visual order equals the DOM order in LTR and RTL (flex and grid follow `dir`). Good.

### 2.4 Focus ring

`:focus-visible{outline:3px solid var(--focus);outline-offset:2px}` passes contrast on every surface (1.4 table) and is thick enough (WCAG 2.2 focus appearance). Except: `.seg{overflow:hidden}` clips it (S3, `focus_seg2.png` shows the ring as a thin sliver between buttons). Fix: drop `overflow:hidden`, round the first and last button corners with `border-start-start-radius` etc.

---

## 3. Touch targets at 390 px (Playwright, `is_mobile`, `has_touch`)

Guidance used: 44 CSS px (WCAG 2.5.5 AAA, Apple), 48 dp (Material); WCAG 2.2 AA 2.5.8 minimum is 24 px unless spacing or inline text exempts.

| Element | Measured size (w x h) | Count (list / entry) | Verdict |
|---|---|---|---|
| `.btn` (search button, primary, secondary) | wide x 44 | few | pass |
| search input | wide x 44 | 1 | pass |
| `.btn.sm` links and buttons (Report, WhatsApp, Facebook, Email, LinkedIn, Open, Share, Copy link, More, "Report entry") | wide x **36** | 17 / 8 | below 44, passes 24 |
| `select` (verification, sort) | wide x **36** | 2 / 0 | below 44 |
| Logo `.logo` | wide x **34** | 1 | below 44 |
| Breadcrumb links | wide x **18** | 10 / 6 | below 44; at 18 px tall they fail 2.5.8 unless the 4 px row gap counts as spacing (it does, narrowly) |
| Row name link `a.nm` | wide x **19** | 9 | below 44; this is the main tap target of the page |
| Related-list links | wide x **19** | 3 | below 44 |
| Map and social links in the key facts | wide x **19** | 0 / 5 | below 44 |
| Native checkbox `#uv`, `#cl` | **13 x 13**; the wrapping label is 24.8 px tall | 2 | label passes 24, fails 44 |
| Footer links ("Privacy and opt-out", "Report") | **15** tall; "Report" is 43 wide | 2 | inline-in-footer; fails 44 |
| Seg buttons (prototype bar only) | wide x 32 | 8 | prototype only |

Totals at 390 px: list page 47 of 55 interactive elements under 44 px in at least one dimension; entry page 22 of 30; empty page 8 of 13; system page 4 of 8.

Fixes in one block of CSS (about 120 bytes):
- `.btn.sm, select, .logo {min-height:2.75rem}` inside `@media (pointer:coarse)` (keeps desktop compact).
- `nav.crumbs a, .nm, .related a, footer a {display:inline-block; padding-block:.625rem}` (adds 20 px of height without changing the look; negative margin on the list to keep spacing).
- Checkbox: `input[type=checkbox]{width:1.5rem;height:1.5rem}` and `label{display:flex;min-height:2.75rem;align-items:center;gap:.5rem}`.
- Row: make the whole row a stretched link (see 2.2.5).
- Gaps between adjacent targets: share buttons are separated by 8 px; with 44 px height this is fine.

---

## 4. Right-to-left, Urdu and Arabic

### 4.1 Logical properties

Complete. A grep of the stylesheet finds no `left`, `right`, `margin-left`, `padding-right`, `float`, `text-align:left`, `translateX` or directional icon. Everything uses `margin-inline`, `padding-block`, `inset-inline`, `border-inline-start`, `text-align:start`, `grid` and `flex` which flip with `dir`. Measured overflow at 320, 390 and 1100 px in Urdu is the same as in English (only the entry-page chip, see section 8). The toast centring (`inset-inline:0; margin-inline:auto; width:max-content`) works in both directions.
Small points: breadcrumb separator "/" is not mirrored (N6); a separator wrapped to the start of a new line leaves an orphan "/" at the line start (`ent_ur1.png`); `.chip` right-side margin uses `margin-inline-end` (correct).

### 4.2 Bidi handling of mixed English and Urdu

What the prototype does: sets `dir="auto"` on every `p`, `ul`, `dd`, `td` in Urdu mode (in JS, after render), sets `lang`/`dir` explicitly on the second-name line (`<div lang="en" dir="ltr">` in Urdu, `<div lang="ur" dir="rtl">` in English) and uses `<bdi dir="ltr">` on the website.

Problems seen in `ent_ur1.png` and `ent_ur2.png`:
- `dir="auto"` on blocks makes each English value left-aligned under a right-aligned Urdu label ("Area" right, "Paris Road, Sialkot..." left). The result is a ragged two-sided page. This will happen constantly in the real product: names, addresses and descriptions are user data in whatever script the contributor typed.
- Dates break at the hyphen ("2026-" / "09-18").
- Phone numbers, IDs ("DEMO-0001", "S-101", "ISO 13485"), prices ("USD 1.20"), URLs and coordinates sit inside Urdu sentences; without isolation, punctuation next to them can move to the wrong side.

Rules for the template:
1. The page direction (`dir` on `<html>`) sets block alignment. Never `dir="auto"` on blocks.
2. Every user-supplied inline string (entry name, area, speciality, certificate number, address line) is wrapped in `<bdi lang="xx">`. `<bdi>` isolates direction without hiding punctuation problems.
3. Dates, numbers with units, IDs and URLs: `<bdi dir="ltr">` or `<time datetime>` plus `white-space:nowrap`.
4. Store a language tag per name and per text field (the spec already says BCP 47); emit it as `lang`. For fields with no tag, `dir="auto"` on the `<bdi>` only.
5. Search input: `dir="auto"` so a Latin query in an Urdu page does not look broken (N4).
6. Test pages that mix three scripts in one line (Urdu sentence, Latin brand name, Arabic-Indic digits from a Gulf source).

### 4.3 Numerals, punctuation, fonts, line-height

**Numerals.** The prototype always uses Western digits (0 to 9). Real behaviour of the platform's own locale data (Node 22 ICU, evidence run here):

| Locale | `Intl.NumberFormat` 1234567.5 | numbering system | Date (medium) |
|---|---|---|---|
| ur, ur-PK | 1,234,567.5 | latn | 18 ستمبر، 2026 |
| ar | 1,234,567.5 | latn | 18/09/2026 |
| ar-AE | 1,234,567.5 | latn | 18/09/2026 |
| ar-SA, ar-EG, ar-KW, ar-OM, ar-QA, ar-BH | ١٬٢٣٤٬٥٦٧٫٥ | arab | ١٨/٠٩/٢٠٢٦ |
| fa-IR (for reference) | ۱٬۲۳۴٬۵۶۷٫۵ | arabext | 27 Shahrivar 1405 (Persian calendar) |

So the Gulf is not uniform and Urdu uses Western digits by default. Recommendation: Western digits (`nu-latn`) for all data in the first version: phone numbers, IDs, years, prices, counts. They are what users type into search and into WhatsApp, they stay LTR-stable, and the Pakistan and UAE locale defaults agree. Make this an explicit decision, not an accident of the library; revisit for Saudi Arabia, Egypt and Kuwait with native reviewers. The same applies to separators (`,` vs `٬`) and to the calendar (Hijri shown beside Gregorian in Saudi Arabia is a later question). Never format by hand; use the locale's formatter, always with `-u-nu-latn` when that is the decision.

**Punctuation.** The Urdu draft strings use the correct Urdu full stop "۔", comma "،" and question mark "؟" (checked in `proto`, `emptyBody`, `closedNote`, `claim`). English strings concatenated into Urdu pages keep "." and ",", which then look foreign. Another reason for M3.

**Fonts: what will actually render.**
- Stack today: `ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Noto Sans", "Noto Naskh Arabic", "Geeza Pro", sans-serif`. No Arabic-script font is specified before the generic, so the browser falls back per character.
- Android: `system-ui` and Roboto have no Arabic-script glyphs; the platform fallback is Noto Naskh Arabic on stock-based builds. To my knowledge standard Android does not ship a Nastaliq font (the Noto Nastaliq Urdu file is more than a megabyte); Pakistani-market skins vary and some add Urdu fonts. I could not test on devices; check on three real low-end handsets (Android Go 8/9/10, a Transsion Tecno or Infinix, a Samsung A series). Expect Naskh, not Nastaliq, on most phones, and expect a missing bold (synthesised bold looks smeared on Naskh).
- iOS and macOS: Geeza Pro (Naskh) for Arabic; Urdu text on recent iOS generally picks a Nastaliq face when `lang="ur"` is set. Windows: Segoe UI for Arabic, "Urdu Typesetting" (Nastaliq) exists on Windows 8 and later.
- Consequence: the same page will show Naskh on most Android phones and Nastaliq on some Apple and Windows devices. Design for both, because users switch devices and because screenshots shared on WhatsApp come from both.

**Naskh vs Nastaliq decision for a data-heavy, low-bandwidth product.** Naskh is far more readable at 14 to 16 px in tables and chips, shares the digit and punctuation set with Arabic (one design for Urdu and Arabic), and is already on most phones. Nastaliq is what many Urdu readers prefer for prose and headlines, but it needs 1.9 to 2.2 line-height, larger sizes, and the web font is about 160 KB (woff2, Arabic subset only, measured from the npm package: 159,368 bytes regular; 157,608 bold), which breaks any page budget. Recommendation: Naskh by default for UI and data; optionally allow installed Nastaliq (local fonts only, zero download) for `h1` and headings:

```css
:lang(ur),:lang(ar){font-family:system-ui,"Noto Naskh Arabic","Geeza Pro","Segoe UI",Tahoma,sans-serif;letter-spacing:0}
:lang(ur) h1{font-family:"Noto Nastaliq Urdu","Jameel Noori Nastaleeq","Urdu Typesetting",system-ui,"Noto Naskh Arabic",sans-serif}
```
Only add the second rule after the native speaker approves; it forces taller headings (below).

**Line-height.** Measured with real fonts loaded (screenshots `u_naskh_list.png`, `u_nast_list.png`, `u_nast_lh_list.png`):
- Noto Naskh at `h1{line-height:1.2}`: two lines at 390 px fit, but tight; marks come close.
- Noto Nastaliq at `h1{line-height:1.2}` and `body 1.55`: the wrapped h1 overlaps the breadcrumb row above and the tags below; button text is cramped. This is not usable.
- Noto Nastaliq at body 2.1, h1 1.9, `letter-spacing:0`: clean. 
- Proposed: `:lang(ur),:lang(ar){line-height:1.9}` (body), `h1,h2:lang(ur){line-height:1.6}` for Naskh (raise to 1.9 if Nastaliq headings are enabled). English stays at 1.55.
- Also raise the Urdu base size by about 6 percent (`:lang(ur){font-size:1.0625rem}`) and give `--t-xs` a floor of 14 px for Arabic script (S8). Arabic-script x-height is smaller than Latin at the same size.
- `letter-spacing:-.01em` on `h1` and `-.02em` on `.logo` applies to Urdu headings; CSS Text says user agents should not apply letter-spacing to cursive scripts and it can break joins. Set it to 0 for `:lang(ur),:lang(ar)` (included in the rule above).
- Bold: `.chip` uses 600 to 700; Nastaliq has no true bold in most system fonts. Use colour and shape (already used) rather than weight for Urdu chips.

### 4.4 Language tagging and untranslated fragments

In Urdu mode: `html lang="ur" dir="rtl"` (set by JS; the real page must carry it in the HTML), but 72 of 149 text nodes on the list page and 61 of 110 on the entry page are English-only and still sit under `lang="ur"`. The English fallback (`T(k)` falls back to `EN[k]`) is sensible during drafting, but in production an untranslated string must be tagged `lang="en"` automatically, and the build must report the percentage translated per page template. Titles and descriptions must be translated too (the Urdu page's `<title>` stays English).

### 4.5 Urdu draft strings (UR dictionary): plausibility check

I have judged each string for meaning and idiom. Flags are for the native-speaker review, ranked by the harm if left as is.

| Key | Draft | Issue |
|---|---|---|
| `reach` | اس فہرست تک پہنچیں | **Probable wrong meaning.** English "Reach this list" means contact the people in the list (the outreach action). "پہنچیں" means "arrive at / get to this list", which reads as navigation. Suggest wording such as "اس فہرست کے اندراجات سے رابطہ کریں". |
| `contact` | اے آل لسٹس کے ذریعے رابطہ کریں | **Brand transliteration looks wrong.** "اے آل لسٹس" reads "ay aal lists" with an extra "اے". Either keep the brand in Latin script inside `<bdi>` ("AllLists کے ذریعے رابطہ کریں") or transliterate once as "آل لسٹس" and use that everywhere. Decide once; the brand also appears in the logo. |
| `viewing` | بطور دیکھیں | Awkward: "بطور" needs a noun ("view as X"). Prototype control only, but the phrase will be reused. Suggest "اس حیثیت سے دیکھیں". |
| `az` | نام الف سے ی | Urdu alphabetical order ends with "ے" (bari ye), not "ی". Likely "نام الف سے ے". |
| `whence` | یہ معلومات کہاں سے آئیں | Reads as past tense "came from where". For a heading, "معلومات کا ذریعہ" is more natural. |
| `reportEntry` | اندراج کی رپورٹ | A noun ("report of entry") next to the imperative button style used elsewhere ("رپورٹ کریں"). Suggest "اندراج کی رپورٹ کریں". |
| `remove` | آپ نہیں؟ اندراج ہٹائیں یا درست کریں | "Not you?" is ambiguous in Urdu ("آپ نہیں؟"). Suggest "یہ آپ نہیں ہیں؟". |
| `quote` | قیمت کی درخواست | Understandable ("request for price"), but a business reader may expect "کوٹیشن" or "قیمت معلوم کریں". |
| `claim` / `yours` / `fix` | ...دعویٰ کریں | "دعویٰ" is a legal-sounding "make a claim". Plausible and used on maps products, but ask whether "اپنا کاروبار کلیم کریں" feels more natural. |
| `global` | دنیا | "World". For a place hierarchy "عالمی" may be preferred. |
| `ranked` and `reviews` | درجہ بندی (both) | Same word for "ranked order" and "rankings and ratings"; check that this is not confusing next to each other. |
| `scale` | قومی برآمدی مرکز | "National export cluster" rendered as "hub"; fine, but "کلسٹر" may be the trade word. |
| `fam2` | مینوفیکچررز | Fine (loanword); "صنعت کار" or "بنانے والے" is the alternative. |
| `lang` | زبان | fine. `theme/system/light/dark`: fine; "تاریک" for dark is acceptable, "گہرا" is the alternative. |
| `locked` | مقفل | Fine, but the code joins it with an English tail ("مقفل: subscribers"), see M3. |
| `title`, `ltype`, `emptyTitle`, `emptyBody`, `closedNote`, `proto`, `about`, `stats`, `help`, `searchPh`, buttons for share and contact apps | | read naturally; use the correct Urdu punctuation. |
| Entry names (`urdu` field) | e.g. ڈیمو سرجیکل ورکس | Fine as transliterations. Note "Co." was dropped from "سیمپل انسٹرومنٹس" (Sample Instruments Co.); decide whether legal suffixes are kept. |

Still missing from the dictionary (so they stay English today): verification levels (`LEVEL`), chip detail text, "Position X of Y", the stats table row labels, all `dt` labels, notes, hours, status words, "Locked: ..." tails. About half of the visible words.

### 4.6 Search and data (Urdu and Arabic specific)

Not visible in the prototype but needed in the template promise ("alternate names and other scripts are stored and searched"): normalise at index and query time: Arabic yeh "ي" and Urdu "ی" and "ے", Arabic kaf "ك" and Urdu "ک", heh forms "ہ ه ھ", alef variants, remove diacritics and tatweel, treat ZWNJ and ZWJ consistently, and map digits. Sort with the locale collator (`Intl.Collator('ur')`); the prototype uses default `localeCompare` for "Name A to Z". Names in mixed Latin and Urdu lists need a per-language sort key.

### 4.7 Plurals

Urdu has two plural categories (one, other); Arabic has six (zero, one, two, few, many, other). "7 published" and "1 awaiting verification" need real plural rules, not a suffix "s". This is part of M3.

---

## 5. Performance

### 5.1 Measured weight of the prototype

| Item | Raw | gzip -9 | brotli 11 |
|---|---|---|---|
| Whole HTML file (single request, no other requests) | 47,069 B | 14,828 B | 12,653 B |
| Inline CSS | 8,796 B | 2,687 B | 2,290 B |
| Inline JS (code, templates, English and Urdu dictionaries, 9 sample entries) | 36,421 B | 11,713 B | 9,993 B |
| Urdu dictionary alone | 2,915 B (UTF-8) | | |

The file makes one request. No fonts, images, third-party scripts or network calls (correct and worth protecting).
Rendered DOM: list page 301 elements (7 rows), entry page 215, empty page 75. About 650 raw bytes per result row in the rendered HTML.

Parse and execute cost (Chromium, local file, so no network): total `ScriptDuration` 4.8 ms unthrottled, 19.7 ms at 4x CPU, 27.3 ms at 6x; layout 22 / 67 / 135 ms; style recalc 7 / 32 / 49 ms; first paint and first contentful paint 72 / 200 / 324 ms (same moment, because the whole page waits for the last script). The JS itself is cheap. The problems with the prototype's approach are not CPU: they are that no paint happens until the script ends, nothing works without JS, the JS is 11.7 KB gzipped that carries no value for a read-only page, and the markup the JS generates is not visible to crawlers or link previews.

### 5.2 Estimate of the server-rendered equivalent

Method: took the rendered `<main>` of each route, wrapped it in a real document shell (title, description, canonical, Open Graph, `color-scheme`, a BreadcrumbList JSON-LD block, the CSS with prototype-only rules stripped and minified to 6.8 KB raw, header, footer) and compressed. The page text still includes the prototype's explanatory "dev notes", so real pages will be a little smaller; they will be larger when real names, descriptions and Urdu text replace the repeated sample data.

| Page | Raw HTML | gzip | brotli |
|---|---|---|---|
| Inline CSS only (minified) | 6,827 B | 2,005 B | 1,743 B |
| List page, free, 7 rows | 20,901 B | 5,728 B | 4,685 B |
| List page, subscriber, 7 rows | 19,728 B | 5,656 B | 4,631 B |
| Entry page, free | 16,913 B | 5,100 B | 4,199 B |
| Empty list page | 9,758 B | 3,164 B | 2,601 B |
| List page scaled to 25 rows | 32,887 B | 6,107 B | 4,905 B |
| List page scaled to 50 rows | 49,370 B | 6,615 B | 5,065 B |

Caveat on the last two rows: I replicated the sample rows, which gzip unrealistically well. Real names are varied, so budget about 0.15 to 0.25 KB gzipped per row: **a 25-row list page of about 8 to 11 KB gzipped, a 50-row page of about 12 to 16 KB**. Urdu text is 2 bytes per character in UTF-8; gzip claws most of it back, so Urdu pages are about 10 to 20 percent larger than English, not double.

Compared with the prototype: a server-rendered list page is about 5.7 KB gzipped (7 rows) against 14.8 KB gzipped for the prototype file, because the JS and the Urdu dictionary stay on the server.

### 5.3 What must change for the real product to work with JavaScript off

The prototype is blank without JS (measured: `#app` empty, screenshot `nojs.png`). For the real product:

1. Server-render every page from templates; `<html lang dir>`, `<title>`, meta, canonical and the full `<main>` come from the server. The strings dictionary lives on the server, not in the page.
2. Real URLs, no hash routes. Every crumb, row, related link, "Report", "Claim", "Add an entry" is a real `<a href>` to a real page (in the prototype most go to `#/list` or a stub).
3. Filters and sort: a `<form method="get">` with a visible "Apply" button; the result is a new URL. Canonical to the unfiltered page; filtered variants `noindex,follow` (section 6).
4. Language switch: plain links to the other language's URL with `hreflang`, not a toggle button that mutates the page.
5. Theme: follow the system with CSS (`prefers-color-scheme`). If a manual toggle is wanted, it needs JS plus a cookie or `localStorage`, which brings back the flash problem (section 7.2). Recommended default: no toggle at launch.
6. "More" menu: `<details><summary>More</summary>...</details>` (zero JS). Better: remove it until it has content.
7. Copy link and native share: render them with the `hidden` attribute and let a 400-byte script reveal them (already how native share works). Without JS, the share links (WhatsApp, Facebook, e-mail, LinkedIn) are plain anchors and keep working.
8. Contact, quote, save and follow: links to pages with forms (sign-in when needed), not buttons that call JS.
9. Toast: not needed without JS; with JS, only for "Link copied".
10. Search: `<form role="search" action="/search" method="get">` (already semantically right).
11. Everything else (tables, dl, chips, lock markers) is already plain HTML.
Result: JS is optional enhancement of about 1 to 2 KB gzipped (reveal copy and share, optional prefetch), not a requirement.

### 5.4 Proposed per-page budget

Aim: a page that arrives in one network round trip on a slow connection. The first flight of a fresh TCP/QUIC connection carries about 14 KB; a 25-row list should fit it.

| Budget item | Target | Hard ceiling (build fails) |
|---|---|---|
| Requests to render the page | 1 (the document) | 2 |
| Blocking subresources (CSS, fonts, JS) | 0 | 0 |
| Web fonts | 0 | 0 |
| Images (decided: none, C29) | 0 | 0 |
| Inline CSS | 2 KB gzipped | 3 KB gzipped |
| JavaScript | 0 required; optional 1 KB gzipped, `defer` | 5 KB gzipped, never blocking |
| Document, list page with 25 rows | 11 KB gzipped (brotli 9 KB) | 18 KB gzipped |
| Document, entry page | 7 KB gzipped | 12 KB gzipped |
| Document, empty list | 4 KB gzipped | 6 KB gzipped |
| DOM elements | 500 (list, 25 rows), 300 (entry) | 800 |
| Elements per result row | 12 | 18 |
| Rows per page | 25 (spec L15 already says paginate) | 50 |
| Largest Contentful Paint, Moto G-class, 4x CPU throttle, "slow 4G" | 2.0 s | 3.0 s |
| Total blocking time, same profile | 0 ms | 100 ms |
| Cumulative layout shift | 0 | 0.05 |
| `Save-Data` header | drop optional blocks (related lists, contributors) | |

Delivery: brotli at the edge, `Cache-Control: public, s-maxage=...` with `stale-while-revalidate`, HTTP/2 or 3, a CDN with points of presence near Karachi, Lahore and Dubai. Inline the CSS (a cached external stylesheet saves about 2 KB on the second page but costs a full extra round trip, 300 to 500 ms on a poor mobile link, on the first; most visits from search will be single-page). Re-examine only if real data show many pages per visit. Enforce the budget in CI with a script that fetches 20 sample pages (English and Urdu) and fails over the ceilings.

### 5.5 Content order for slow phones (S12)

At 390 px, the first result row starts 2,307 px down a 5,628 px page. Everything above it is: breadcrumbs, title, scale tags, summary, action panel with seven buttons, "About this list", the statistics table, the areas table, filter and sort controls, sponsored slot. Spec order L1 to L12 is respected, but on a phone the user sees names about three screens in. Options that respect the spec and the decisions: put results immediately after the action row and move "About", statistics and areas below the list, or collapse statistics and areas into `<details>` (works without JS); keep the one-line summary above. Same applies to the entry page (the Trust strip and actions are above the fold, which is right).

---

## 6. Search-engine and data issues

1. **Titles and headings.** Real pattern: list page `<title>`: "{List type} in {Place}, {Country} | AllLists" (under about 60 characters), `<h1>` the same without the suffix; entry page `<title>`: "{Name} - {type} in {Area}, {City} | AllLists". The prototype's `<h1>` on entries is the name only; the title tag and breadcrumb must carry the place and type. Check Urdu titles for length in pixels, not characters.
2. **Canonical.** None in the prototype. Needed on every page, absolute, language-specific, no query parameters. The share links add `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` and `ref=...`; every shared link is a URL variant, so the canonical must point to the clean URL. Prefer ASCII slugs plus a stable ID (`/pk/punjab/sialkot/surgical-instrument-makers`, `/e/{id}-{slug}`): percent-encoded Urdu slugs are about nine bytes per character and ugly when copied, and the prototype's `/e1` has no slug.
3. **hreflang.** Put the `en`/`ur`/`ar` alternates in the XML sitemaps, not in every page head (saves about 100 B per language per page). Add `x-default`.
4. **Empty lists.** The spec says empty pages are not indexed. Implement as `<meta name="robots" content="noindex,follow">` and the same as an `X-Robots-Tag` header, remove from sitemaps, and do not block them in `robots.txt` (a blocked page cannot show its noindex). Choose a threshold for index (a one-entry list is nearly a duplicate of the entry page); it is an open product choice, flagged not decided here. Because the template links to empty sibling lists ("Surgical instrument makers in Gujrat (empty list)"), crawlers will keep revisiting them; link them only when useful, not from every page.
5. **Filters, sort, pagination.** Faceted URLs (`?level=owner&sort=az`) multiply pages. Canonical to the base list; `noindex,follow`; `rel="nofollow"` on facet links; disallow facet parameters in `robots.txt` for crawl budget. Paginated pages: self-canonical, crawlable `<a>` links, no reliance on `rel=prev/next` (ignored).
6. **Structured data fit with names-only previews.**
   - Markup must describe what the visitor can see. For locked data (street address, exact pin, specialities, certificate, minimum order) do not output it in JSON-LD even though the server knows it; search engines treat hidden or paywalled facts in markup as a violation unless marked properly.
   - List page: `BreadcrumbList` (cheap, still shown in results) and `CollectionPage` with an `ItemList` (position, name, url per row). Names and URLs only: this fits the names-only free view exactly. This is not a rich-result feature by itself, so treat as harmless metadata, not a promise of visibility.
   - Entry page: a minimal `LocalBusiness` (or `Organization`) with `name`, `url`, and `address` at locality level only (`addressLocality`, `addressRegion`, `addressCountry`), `inLanguage`. No `telephone`, no `email`, no `geo`, no `sameAs` (locked or hidden by decision E13). Without a street address the page will probably not qualify for local-business rich results; that is acceptable and consistent with the data model. Add `aggregateRating` only after review rules exist.
   - If subscription-gated sections should be flagged, use the documented paywalled-content pattern (`isAccessibleForFree`, `hasPart` with a CSS selector). Search engines must be served the same locked view as free visitors (no cloaking).
   - Size: about 300 to 500 B gzipped per page for BreadcrumbList plus ItemList on 25 rows (roughly 90 B per row); inside the budget.
7. **Link previews (WhatsApp is the main distribution channel).** Add `og:title`, `og:description`, `og:type`, `og:url`, `og:site_name`, `og:locale` (`ur_PK`, `ar_AE`...), `og:locale:alternate`. No image (decision C29), so the preview is text-only; keep the description to one short sentence with counts. Server-side rendering is required: scrapers do not run JS (M1).
8. **Meta description** must be generated per page ("7 published surgical instrument makers in Sialkot, Punjab. Verified by surveyors, owners and AI checks. Updated 2026-10-05"), in the page language.
9. **`<html lang>`** must be in the server HTML. Use region tags where relevant (`ur-PK`, `ar-AE`) only if content differs.
10. **Outbound links**: `rel="nofollow noopener noreferrer"` on user-submitted social links is right; add `ugc` for contributor-supplied URLs and `sponsored` on the sponsored slot.
11. **Closed entries**: keep 200 with the "permanently closed" notice and `noindex` after a period, or keep indexable if they get old-link traffic; undecided, flag for the SEO owner.

---

## 7. Reduced motion, dark-mode flash, forced colors

### 7.1 Reduced motion

The stylesheet has a `prefers-reduced-motion` rule that disables `scroll-behavior`, `transition` and `animation`, but the page defines none of them: `document.getAnimations().length` is 0 with reduced motion on, and there is no `transition` or `animation` anywhere else in the CSS. The rule is a harmless guard; it is a universal `*` selector with `!important`, which is a few hundred wasted style matches. Keep as a deliberate guard comment, or remove (N5). `window.scrollTo(0,0)` on re-render is an instant jump (no smooth scrolling) and fine.

### 7.2 Dark-mode flash

In the prototype there is no visible flash: `localStorage` is read at 18.6 ms (unthrottled), 44.7 ms (4x) and 79 ms (6x), before first paint at 72, 200 and 324 ms. This is only because the script blocks the first paint, and the page is blank until then. Checked: OS dark with a stored "light" choice gives `data-theme="light"` and the light background after the script.
In the real, server-rendered product the CSS and content paint immediately, so a stored theme applied by a script at the end would flash the wrong theme. Avoid by (a) following the system with CSS alone, no stored choice; or (b) a 150-byte inline script in `<head>` that sets `data-theme` before the body is parsed; add `<meta name="color-scheme" content="light dark">` and `:root{color-scheme:light dark}` so the canvas, form controls and scrollbars match before CSS applies (today `color-scheme` is only set in the dark blocks). The token blocks are triplicated (media query, `:not([data-theme=light])`, explicit dark). If the manual toggle is dropped, only the media block is needed (saves about 350 B raw).

### 7.3 Forced colors (Windows high contrast), measured with `forced_colors: active`

- Text, links and borders are system colours; content is fully readable (screenshot `forced_list.png`). The dashed and dotted chip borders survive, so the verification chip levels remain distinguishable: good.
- Pressed state of the segmented buttons: pressed button fill `rgb(255,255,255)` vs unpressed transparent; bold is the only other difference. Add `@media (forced-colors:active){[aria-pressed=true]{background:Highlight;color:HighlightText;forced-color-adjust:none}}` or add a check mark or underline (S9).
- Primary and secondary buttons are visually identical (white, 1 px black border); only the weight differs. Give `.btn.primary` a thicker border (`border-width:2px`) in forced colors.
- Toast: `background-color` computes to the canvas colour, border width 0: text overprints the page behind it (`forced_toast.png`). Add `border:1px solid` (it is invisible in normal mode, harmless).
- Swatches on `#/system` use inline backgrounds and vanish; add `forced-color-adjust:none` there (design system page only).
- Focus ring (outline) is kept; with the `.seg` overflow fix it is visible.

---

## 8. Overflow and clipping at 320, 390, 1100 px (Playwright)

Matrix: widths 320, 390, 1100; English and Urdu; routes list (with unverified and closed shown), entry e1, empty, entry e9 (closed), system; free and subscriber plans. Checked document `scrollWidth` vs `clientWidth`, elements outside the viewport, and clipped or scrolling containers. Run twice: container default fonts, and with Noto Naskh loaded.

Result: 96 combinations (48 per font set), the only failure is the same one in all runs.

| Width | Language | Route | Result |
|---|---|---|---|
| 320 | EN and UR | `#/entry/e1` (free and subscriber) | **overflow** `scrollWidth` 389 (default fonts) or 384 (Naskh) vs 320. Element `span.chip.surveyor` ("Surveyor-verified (Surveyor S-101, 2026-09-18)") extends to 385 px (EN) or to x = -65 px (UR). Cause: `white-space:nowrap` on `.chip`. |
| 320 | EN and UR | all other routes | no overflow |
| 390 | EN and UR | all routes | no overflow, but on `#/entry/e1` the same chip is wider than the 358 px content box and protrudes about 6 px into the gutter (visible in `ent_ur1.png`) |
| 1100 | EN and UR | all routes | no overflow; no clipped or scrolling container (the `.tablewrap` elements do not scroll) |

Also seen: wrapped breadcrumb separators leave an orphan "/" at the start of a line; fixed by putting the separator in the same flex item as the link before it.

---

## 9. What is already right (keep it)

System fonts only; no images, no third-party requests; one small CSS block; logical properties throughout; tokens for every colour; chips encode meaning with shape plus text; every control has a text label; every price carries a date; `lang`/`dir` set on the second name; share links are plain links; forms inputs use 16 px text; the design system page documents the rules. These are what make a good, light, RTL-ready template. The work above is about moving it from a JS mock-up to a server-rendered page with the same look.

## 10. Questions for the owner or the native reviewers

1. Digits: Western digits for all data in v1 (recommended), or per-locale digits for the Gulf?
2. Naskh only, or Naskh plus Nastaliq headings where the device has it (needs native speaker sign-off on look)?
3. Index threshold for lists (zero entries is decided; what about one or two)?
4. Brand spelling inside Urdu text: Latin "AllLists" or transliteration, and which?
5. Does the first version keep a manual theme toggle (needs head script) or follow the system only?
6. Which three real handsets are the test devices for Urdu rendering?

Evidence files (scratchpad, not repo): `rev/contrast.py`, `rev/touch.py`, `rev/sem.py`, `rev/overflow.py` (+ `overflow_out.txt`), `rev/perf.py`, `rev/ssr.py`, `rev/misc.py`, `rev/urdu.py`, screenshots `u_naskh_list.png`, `u_nast_list.png`, `u_nast_lh_list.png`, `ent_ur1.png`, `ent_ur2.png`, `focus_seg2.png`, `forced_list.png`, `forced_toast.png`, `nojs.png`.
