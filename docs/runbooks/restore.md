# Restore from backup

**Who:** the engineer on duty, with a second person watching. **Needed:** data loss or corruption, a lost server, and every quarter as a drill.

## Drill (every quarter, a skipped drill raises an alert)
1. `scripts/restore_drill.sh`. It restores the newest dump into a scratch database, checks that the audit chain and the ledger reconciliation still hold in the copy, records the time, and drops the scratch database.
2. Write the timing in the log below. Goal: restore within one day at the first stage, four hours at the second stage, one hour later.

## Real restore
1. Stop the web service and the timers: `sudo systemctl stop alllists-web alllists-scheduler.timer alllists-campaigns.timer`.
2. Keep the damaged database: rename it (`ALTER DATABASE alllists RENAME TO alllists_damaged`), do not drop it.
3. `createdb alllists` then `pg_restore -j 4 --no-owner -d alllists /var/backups/alllists/daily/<file>.dump`.
4. Re-apply grants: `python manage.py db_roles --apply`.
5. Check: `python manage.py shell -c "from core.models import verify_audit_chain; print(verify_audit_chain())"` prints `None`; open `/staff/ledger/` and confirm every line agrees.
6. Work out what was lost since the dump (audit rows after the dump time live only in the damaged copy). Payments taken in that window are in the payment provider's records; record them again through `/staff/orders/`.
7. Start the services. Write the incident down, including the data-loss window.

## Drill log
| Date | Dump | Restore time | Checks passed | By |
|---|---|---|---|---|
| (first drill before launch) | | | | |
