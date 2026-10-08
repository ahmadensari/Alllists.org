# Making the page modern, dynamic and moving: tools and choices (2026)

The owner asked for tools that make the prototype a modern, dynamic, moving website of 2026 and not a website of the 1990s. This note records what the search found, what I recommend, and what is already built into the prototype. Facts come from search summaries of web pages and are graded: **S** a search summary of a source, **U** a single or conflicting source, **I** my judgement. No code beyond the prototype is written.

Last updated: 2026-10-05.

## The idea in one paragraph

Modern in 2026 mostly means the browser itself can now do what used to need libraries: animated page changes, scroll effects, pop-up menus and responsive parts. So the plan is CSS first and server-rendered pages with small bits of interaction, and a library only where CSS cannot do the job. That keeps each page light, which matters for slow phones in Pakistan, for search-engine ranking, and for a template repeated a very large number of times. "Moving" means purposeful motion that helps people see what changed, not decoration.

## 1. What the browser can now do without libraries

| Feature | What it gives us | Support (search summaries) | Grade |
|---|---|---|---|
| View Transitions (same page and page to page) | Smooth fades and slides between pages, list rows that glide when sorted or filtered | Same-page: Chrome and Edge 111+, Safari 18+, Firefox 133+. Page to page: Chrome 126+, Safari 18, Firefox 132. About 88% of global browsers in April 2026. Called Baseline since October 2025 | S |
| Scroll-driven animations | Effects tied to scrolling (a header shadow, reveals) with no scroll code | Baseline newly available in 2026; sources disagree on the exact Firefox version | S, U |
| Anchor positioning and the popover and dialog elements | Menus, tooltips and dialogs without a library | Baseline in all major engines in 2026 | S |
| Container queries, `:has()`, nesting, subgrid | Parts that adapt to their space, parent-based styling, simpler style files | Widely supported | S |
| Speculation Rules (prerender the next page) | Pages that open instantly | Chrome and Edge only; Safari behind a flag; Firefox not yet. Use as a bonus only | S |
| `@starting-style`, `light-dark()` | Fade-in for elements and simpler themes | Modern browsers | I |

**Rule:** every effect is an enhancement. The page works without it, and reduced-motion users get none of it.

## 2. How the page gets its interaction

| Option | What it is | Weight | Fit |
|---|---|---|---|
| **Django templates with HTMX and Alpine.js** | The server sends finished HTML; HTMX swaps pieces of the page; Alpine handles small client actions such as a menu | Small | **Best fit for this project.** Matches the Django suggestion (Q-S9), server-rendered for search engines, one language for the team |
| Datastar | One 11 KB library that combines both ideas and streams updates from the server | About 11 KB | Newer and smaller community; worth watching |
| Astro (islands) | Pages ship almost no JavaScript; interactive islands only where needed | About 0 to 15 KB per content page | Strong if the front end is split from Django. Needs a Node build |
| SvelteKit | Compiled framework, small bundles | About 30 to 60 KB per page | Good, but a second language and runtime |
| Next.js or React Router | The large React ecosystem | About 80 to 150 KB per page | Largest hiring pool; heaviest for slow phones. Choose only if a React team is the priority |

Bundle sizes come from comparison blogs (U). For a template repeated for every list and entry, the per-page weight matters more than anything else.

## 3. Components and styling

- **Tailwind CSS v4** is a build-time engine with design tokens declared in the style file (S). Our tokens already live in one block, so Tailwind is optional here.
- **Component libraries** apply only if React is chosen: shadcn/ui now builds on Base UI (version 1.0 in December 2025), the headless successor to Radix, with React Aria another accessible base (S, U on dates).
- With Django, native elements plus popover, dialog and anchor positioning replace most component libraries.

## 4. Motion libraries, only where CSS is not enough

| Tool | Size and licence | Use here |
|---|---|---|
| Motion (formerly Framer Motion) | About 2.6 KB for the small core, about 34 KB full; MIT | Layout and gesture animation if React is used |
| GSAP | About 23 KB; free for commercial use since April 2025 including its plugins; closed source | Complex scroll scenes. Not for list and entry pages |
| Rive | Compact binary files; the vendor says 10 to 15 times smaller than Lottie | Rare illustrations, onboarding, empty states |
| Lottie | Large JSON files; a new state machine since late 2025 | Skip unless a designer needs it |

Figures are search summaries (S, vendor claims U). Neither GSAP nor Rive belongs on the repeated list and entry pages.

## 5. Search, maps and live updates

- **Search as you type:** Meilisearch (about 50 ms) and Typesense (GPL-3, in memory, under 50 ms) both have InstantSearch adapters (S). Postgres search with HTMX is enough at first; the prototype already filters as you type.
- **Maps (later, because pictures and maps come after text and numbers):** MapLibre GL JS with Protomaps PMTiles lets us self-host vector maps with no API key; the vendor says non-commercial use is free and commercial use asks for sponsorship (S, U; read the terms before use).
- **Live updates:** server-sent events (used by Datastar, and by HTMX through an extension) suit live counts and notifications. Add only when a feature needs it.

## 6. Design and hand-off tools

| Tool | Notes |
|---|---|
| Penpot | Open source (AGPL-3.0), self-hostable, native design tokens in the W3C format, free developer mode; prototyping is weaker than Figma (S) |
| Figma | Proprietary; about USD 15 per seat a month for teams (S); the largest plugin library |
| This environment | The design guidance and design canvas used earlier. No design system is attached to the account, so the tokens live in the prototype's style block and `docs/DESIGN_SYSTEM.md` |

## 7. Speed guardrails

- Interaction to Next Paint: 200 ms or less is good; 87.1% of sites were good in January 2026 (S).
- No third-party scripts on list and entry pages. Motion uses only opacity and position, and respects reduced-motion settings.
- Keep the repeated-page budgets in `docs/DESIGN_SYSTEM.md` section 9; add a JavaScript limit of 30 KB compressed for the interaction layer (my proposal, I).

## 8. What is built into the prototype now (CSS first, no libraries)

| Effect | How |
|---|---|
| Smooth page changes | View Transitions on route changes (fade and slide) |
| Rows glide on sort and filter | Each row has a transition name, so the browser animates the move |
| Search as you type | Typing in the search box filters the list live and keeps focus; typing on another page jumps to the list |
| Sticky header with a shadow that appears on scroll | Scroll-driven animation, no scroll code; only on wide screens |
| Toast fade-in | `@starting-style` |
| Hover feedback on rows and buttons | Plain CSS transitions |
| Reduced motion | All of the above switch off |
| Trust hero | A large count and a trust bar that fills on load; the bar uses patterns and a legend, not colour alone |
| Area chips | Tap an area chip instead of using a drop-down; scrolls sideways on phones |
| List or cards | A toggle switches the results between a ruled list and a card grid, with the cards gliding into place |
| Entrance and press effects | Rows rise in one after another when a page opens; buttons give a small press response |
| Company pages | Paid companies have a fuller page (C35) |

Everything adds about one kilobyte and loads no library. It was tested in Chromium; Safari and Firefox fall back to instant changes where a feature is missing.

## 9. Recommendation

1. **Stack for the modern layer:** Django templates with HTMX and Alpine.js, CSS-first motion, no animation library on repeated pages. Astro is the alternative if the front end is separated from Django.
2. **Add on demand:** Motion or GSAP for one specific component that needs it; Rive for rare illustrations; MapLibre and PMTiles when maps arrive; Meilisearch or Typesense when Postgres search is no longer enough.
3. **Design tool:** Penpot if the team wants an open-source tool with token support; the repository's tokens remain the source of truth either way.
4. **Test on the devices that matter:** low-end Android phones on slow data, plus Safari and Firefox, before choosing anything heavier.

## 10. Open decisions

| Decision | Suggested default | Ref |
|---|---|---|
| Interaction layer | Django with HTMX and Alpine.js | Q-S18 |
| Motion library on repeated pages | None | Q-S18 |
| Design tool | Penpot, or keep working from the token block | Q-S18 |
| Maps provider when maps start | MapLibre with self-hosted PMTiles, after reading the terms | later |
