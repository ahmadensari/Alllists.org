# Personal-data breach response

**Who:** the founder (decisions) and the engineer (containment). Counsel is called on the first day. **Needed:** any sign that personal data (contacts, encrypted fields, account details, payout details) left our control.

## First hour
1. Contain: revoke the exposed credential, rotate secrets (`secret-rotation.md`), block the address, or take the affected route offline. Do not delete evidence.
2. Preserve: copy the web and database logs for the window; note times in UTC.
3. Write a timeline in a private document as facts come in.

## First day
4. Establish what was exposed: which tables, how many people, which countries. Contacts and payout details are encrypted at rest; say whether keys were also exposed.
5. Check the audit log for the actor and the actions (`/staff/audit/`). Run the subject-access report for a sample person to see what was linked to them.
6. Call counsel. Some countries require notice to the regulator within 72 hours of becoming aware and notice to the people affected when the risk is high.

## After
7. Tell the affected people plainly: what happened, what data, what we did, what they can do.
8. Fix the cause. Add a test so it cannot recur. Update `docs/DECISIONS.md` and the threat table in the technical plan.
