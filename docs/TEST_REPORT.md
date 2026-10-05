# Test report

What was tested, how hard, what it found, and what is still untested. Written for the founder; the commands at the end let anyone repeat it.

## In one paragraph

About 570 automated tests run against a real PostgreSQL 16 database on every change (Python 3.11, 3.12 and 3.13), in random order, with lint, a security scan and a migration forward and back check. Line coverage is 96 percent of the application code. Beyond ordinary tests there are six harder layers: a whole-site matrix, an authorization matrix for the staff console, property and fuzz tests, concurrency tests with real threads, a mutation check that breaks one rule at a time to prove the tests would notice, and runs against a real server and a real browser. These layers found and fixed about 25 defects, listed below. Nothing here has touched a real payment provider, a real messaging provider, a real domain or a production server; that is the next stage.

## The layers

| Layer | What it does | Where |
|---|---|---|
| Unit and module tests | Every module's rules: verification guards, credit eligibility, allocation arithmetic, claims, consent, import, duplicates, search, loaders, billing, payouts | `backend/*/tests/` |
| Property tests (Hypothesis) | The allocation split conserves every cent for any input; the paywall rule matches a plain-language reference for any scopes and places; text folding, contact filter, import parser, one-time codes (against the published RFC 4226 and 6238 vectors) never crash and keep their promises | `ledger`, `access`, `core/tests/test_fuzz.py` |
| Whole-site matrix | Every route, seven kinds of visitor (anonymous, plain account, surveyor, subscriber, moderator, finance, admin), both GET and POST: no server error anywhere, access levels enforced, no contact value or stored ciphertext in any page, shared pages byte-identical for everyone and without cookies, private pages never cacheable, only webhooks skip CSRF | `core/tests/test_site_matrix.py` |
| Staff console matrix | Every queue and every action: does what it says, refused to the wrong role, GET refused, a second press never crashes, nobody approves their own payout details | `catalog/tests/test_staff_console.py` |
| Concurrency | Eight threads replay one sale; six threads pay one order with different references; four payout requests race for one balance; surveyors race for tasks; counters and invoice numbers under load | `core/tests/test_concurrency.py` |
| Fetcher security | Private, loopback, link-local, shared, reserved and IPv6-disguised addresses, redirects, ports, robots.txt in every state, oversize pages, DNS rebinding | `agents/tests/test_fetcher_security.py` |
| Commands and production settings | Every management command; production refuses to start without secrets or in debug mode, passes the deployment check, redirects HTTP to HTTPS except the health check | `core/tests/test_commands.py` |
| Mutation check | Changes one comparison or boolean at a time in the money, access, verification and contact-safety code, runs the tests, and lists every change nobody noticed | `scripts/mutation_check.py` |
| Real server and browser | Production settings under gunicorn, a headless browser at phone width in light and dark, English and Urdu, and a real HTTP sign-up to entry to enquiry journey | run by hand, results in `docs/DECISIONS.md` |

## What the harder layers found (all fixed, each with a regression test)

Security and privacy: a creator could prove "ownership" of their own entry with a code sent to a contact they supplied and earn payout credit from it; the add form let a client list a named person as a business, skipping consent; a payout's bank details could be swapped between approval and payment; a checker's login name was shown publicly beside every check; the enquiry reply address could carry phone numbers and links past the relay filter; a leak could be traced to the wrong extract because trace addresses are not unique; the page fetcher followed a name that changes its answer between the safety check and the connection.

Money: two payments for one order with different references both fulfilled it; the same payment reference arriving twice at once broke the transaction; a replayed sale arriving at the same moment hit a database error; four payout requests at once could pay out four times the payable balance; a subscription could be bought for the whole world at the one-city price; a negative fee or tax was accepted when the net stayed positive.

Crashes on hostile input: a pasted file with a bare carriage return, a non-ASCII one-time code on the two-step sign-in, and any NUL character in an address, query or form value each caused a server error.

Operations: account, staff and form pages carried no cache header; production did not insist that the active encryption key is among the keys; loading Overture divisions after GeoNames made a twin country; the development encryption key changed on every start; a forgotten `collectstatic` would have broken every page.

## What the mutation check showed about the tests themselves

On the ledger, the paywall policy and the verification code, the first run left 8 to 9 of every 40 changes unnoticed (for example a revoked check still earning, entry counts wrong, the paywall rule's boundaries). Tests were added for each real gap; the policy file now has every code change noticed. The remaining unnoticed changes are inside comments and messages, which are harmless and are now skipped by the script.

## Not tested, and why

| Not tested | Why | What to do |
|---|---|---|
| A real payment provider, real WhatsApp, SMS or email delivery | None chosen yet; the code runs against a manual path, a signed-webhook path and a sandbox sender | Bake-off, then adapter tests against the provider's sandbox |
| Real Google and ORCID sign-in | Needs client credentials | Test on staging with real credentials |
| Production server, HTTPS certificates, CDN, backups and restore on a real host | No server yet | Staging rehearsal in `docs/DEPLOYMENT.md` section 9 |
| Load at three times peak | Needs staging | `scripts/loadtest.py` |
| A person reading the Urdu text | The strings are first drafts | Native review |
| Accessibility with a screen reader | Automated checks only (labels, contrast tokens, no horizontal scroll) | Manual pass |

## Repeat it

    docker compose up -d db
    cd backend && pip install -r requirements.txt pytest-cov pytest-randomly
    export POSTGRES_DB=alllists POSTGRES_USER=alllists POSTGRES_PASSWORD=alllists POSTGRES_HOST=localhost
    pytest -p randomly --cov=. --cov-report=term-missing
    flake8 .. && bandit -r . -x "*/tests/*","*/migrations/*" -ll
    python ../scripts/mutation_check.py ledger/services.py ledger billing --max 40 --seed 5
    python ../scripts/loadtest.py http://localhost:8000 --users 20 --seconds 60
