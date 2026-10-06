---
name: alllists-rules
description: The standing rules of the AllLists.com project. Use at the start of any task in this repository and before changing data, pages, money, consent or security code.
---

# AllLists.com standing rules

Read `docs/DECISIONS.md` first. Nothing marked Decided is reopened unless the founder says so.

1. **English only** for now: pages, labels, messages, documents, list names. No new translations. Existing Urdu labels and right-to-left support stay untouched.
2. **Contacts are never shown.** Phone, WhatsApp and email stay encrypted; messages are relayed.
3. **Entries are stored once**; lists are a list type at a place. Text and numbers only, no images or video.
4. **Four check labels** only: Surveyor-verified, Owner-verified, AI-checked, Not verified yet. Paid rank can never change a label.
5. **Individuals and child-facing lists** are gated: consent only, no public contact, counsel first.
6. **Agents are capped** (spend caps default to 0), have a kill switch, and stop below 90% audited accuracy or above USD 0.30 per verified record.
7. **No deployment, upscaling or real payments** until the founder asks. Staging and tests only.
8. **Record every decision** in `docs/DECISIONS.md` (build log section) and keep `docs/MASTER_DOCUMENT.md` consistent.
9. **Keep CI green**: flake8 (root `.flake8`), `bandit -ll`, `pip-audit`, migrations check, and the full test suite on Python 3.11, 3.12, 3.13. Run `../.venv/bin/pytest -q` from `backend/`.
10. Never print or commit secrets. The founder's pasted tokens and passwords stay redacted; only the founder can rotate them (`docs/runbooks/secret-rotation.md`).
11. Do not ask the founder routine questions. Ask only when a decision is genuinely theirs, using a short pop-up question; otherwise use the defaults in `docs/DECISIONS.md` section 9.
12. Branch: work on `claude/zen-wright-fudnux`, open drafts as pull requests, never push elsewhere.
13. **Depth and scale:** follow `docs/REQUIREMENTS_DEPTH_AND_SCALE.md` and the `depth-and-scale` skill: the Hotels logic at every place level, depth over generalisation (manufacturing deepest), state scale arithmetic before design.
