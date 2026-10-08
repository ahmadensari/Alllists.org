# Runbooks

One page for each thing that goes wrong or must be done on a schedule (plan 18.8). Each one says who does it, how to know it is needed, the steps, how to check it worked, and what to write down. Keep them short; if a step is unclear, fix the runbook after the incident.

| Runbook | When |
|---|---|
| [deploy-rollback.md](deploy-rollback.md) | Every release; a bad release |
| [restore.md](restore.md) | Data loss; the quarterly drill |
| [secret-rotation.md](secret-rotation.md) | Every 6 months; any suspected exposure; a person with access leaves |
| [breach-response.md](breach-response.md) | Personal data may have leaked |
| [takedown-request.md](takedown-request.md) | Someone asks for removal or erasure |
| [payout-cycle.md](payout-cycle.md) | Monthly contributor payouts |
| [reconciliation-difference.md](reconciliation-difference.md) | The money check shows a difference |
| [sender-paused.md](sender-paused.md) | A campaign or sender is auto-paused or banned |
| [ai-spend-runaway.md](ai-spend-runaway.md) | AI spend alert at 50% or 80% |
| [template-rollback.md](template-rollback.md) | A page-template or message-template change goes wrong |
| [indexing-drop.md](indexing-drop.md) | Search engines stop indexing us |
| [scraper-surge.md](scraper-surge.md) | One address or account reads far too many pages |

Where the commands name `manage.py`, run them as the service user from `/srv/alllists/current/backend` with the environment loaded (`set -a; . /etc/alllists/alllists.env; set +a`).
