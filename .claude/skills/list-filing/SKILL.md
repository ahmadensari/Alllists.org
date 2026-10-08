---
name: list-filing
description: How the AllLists.com filing agents draft entries for lists. Use when configuring, running or improving the agents that fill lists from permitted sources.
---

# List-filing agents

Goal: draft accurate entries for a list type at a place from permitted sources, at low cost, as drafts that earn nothing until verified.

1. **Sources first.** Only sources rated green or reviewed amber in the source gate (`backend/intake/gate.py`); see `research_notes/Backend research/02_data_sources_by_country.md`. Never scrape Google Maps, Facebook or Baidu Maps. Fetch only through `backend/agents/fetcher.py` (public ports 80/443, robots respected).
2. **Fill by template.** Use the family field template (`research_notes/Backend research/01_entry_fields_per_family.md`); fill only fields the source states; leave the rest empty; never invent a value.
3. **Record provenance** for every field: source, licence, date, consent status.
4. **Individuals and child-facing types** are not filled by agents without consent; rows that look like named people are held.
5. **Bulk path:** stage, sample audit, publish drafts (`backend/intake/bulk.py`). Never publish a batch the auditor rejected.
6. **Caps:** respect the job's spend cap and the kill switch. Report cost per verified record.
7. **Learn from audits:** after each audit, add the rejected rows as counter-examples to the job's prompt notes (versioned), and promote or demote the job kind by its audited accuracy.
