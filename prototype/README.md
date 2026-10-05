# Prototype: one list page and one entry page

A static design prototype. One file, `alllists-prototype.html`, with no server, no database and no outside scripts. Open it in any browser.

- All businesses, numbers, certificates and dates are invented sample data.
- It shows the components in `docs/LIST_AND_ENTRY_COMPONENTS.md`: the list page (sections 3 and 9 of that file) and the entry page (sections 4 to 9).
- Use the "Free visitor / Subscriber" switch at the top to see names-only versus unlocked views. Phones, WhatsApp numbers and emails are never shown in either view (decision E13).
- Share buttons are plain links (WhatsApp, Facebook, email, LinkedIn, X under "More", native share on phones, copy link) with tracking tags. Nothing loads from a social network until a button is clicked.
- Statistics and counts are computed from the sample entries so the numbers always match the rows.
- It is not the production system. The production code lives in `backend/`.

Tested in Chromium at desktop and phone width, no script errors.
