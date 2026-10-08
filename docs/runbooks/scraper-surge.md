# Scraper surge

**Who:** the engineer. **Needed:** the abuse alert (an address or account loading over 500 list fragments in a day) or a traffic spike on list pages.

1. `/staff/metrics/` shows how many addresses crossed the line; the audit log has `abuse.alarm` rows with a hashed subject.
2. Free viewers are already limited by the daily row quota; past 2000 fragment requests an address is refused. Check that this is working in the log (status 429).
3. If the traffic comes from one network, block it at the proxy or CDN. If it uses many accounts, suspend the accounts and look for how they were created.
4. Remember the page itself is the same for everyone and the valuable details arrive only in the private part; confirm nobody found a way around that (read the access log for direct fragment calls without a page load).
5. Check an extract was not leaked instead: search a sample against `identify_leak` (see `docs/runbooks/README.md` and the extracts module) using the planted trace entries.
