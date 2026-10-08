# Payout cycle

**Who:** two people from finance: one creates, a different one approves. **When:** monthly, after refund holds have released (the daily job does the release).

1. `/staff/ledger/`: every reconciliation line must read "agrees". If not, stop and use `reconciliation-difference.md`.
2. Check `/staff/kyc/`: approve or reject payout details waiting for review. People without approved details are skipped.
3. Person A: **Create batch from payable balances**. The batch lists each person and amount (only balances at or above the minimum).
4. Person B: read the batch, then **Approve**. The creator cannot approve their own batch.
5. Pay each person through the bank or wallet. Put each payment reference on its own line as `payout id = reference` in the box and press **Mark paid**. Every payout needs a reference.
6. Reconcile again; every line must still agree. Save the bank statement with the batch number.
7. Record the cycle in the payout log (date, batch number, total, who created, who approved).
