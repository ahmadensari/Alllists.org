# Reconciliation difference

**Who:** finance with the engineer. **Needed:** `/staff/ledger/` shows a line that does not agree, or the daily job raises an alert.

1. Do not edit anything. The ledger is append-only; corrections are new reversing entries.
2. Read the line that differs and its expected and actual numbers (minor units).
   - *clearing vs payments:* a payment was recorded without a sale, or a sale without a payment. Look at orders in `paid` that are not `fulfilled`.
   - *holding or payable:* an allocation was released or reversed outside the normal job. Check `release_holds` and refunds in the audit log.
   - *fees or tax:* a payment was recorded with the wrong fee or tax figure.
   - *payout:* a payout was marked paid without a posting (should be impossible) or a batch was only partly paid.
3. Find the cause in the audit log (`/staff/audit/`) around the time the difference first appeared (the daily job log shows the first failing day on `/staff/jobs/`).
4. Fix by an explicit correcting action: a reversing refund, a recorded payment, or an adjustment entry approved by two finance people.
5. Re-run reconciliation; write down the cause and the fix. If the cause was a bug, add a test.
