# AI spend runaway

**Who:** the engineer. **Needed:** alert at 50% or 80% of the daily or monthly cap, or any job reports its own cap hit.

1. Press the kill switch if spend is rising unexpectedly: switch on the `agent_kill_switch` feature flag (admin) or set `AI_KILL_SWITCH=1` and restart. Nothing new starts while it is on.
2. `/staff/agents/` shows today's and the month's spend, jobs, stop reasons and cost per verified record.
3. Find the job that spent the money: kind, source, tokens, stop reason. A job that ignored its own cap is a bug: fix and add a test.
4. Check what the jobs produced: drafts are never published, so the damage is cost only. Discard drafts from a bad run.
5. Turn caps back up only with a written reason. Record the incident.
