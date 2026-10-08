# Sender or campaign paused or banned

**Who:** moderator and the engineer. **Needed:** a campaign shows `paused`, a supplier shows `paused`, or the messaging provider warns or bans the sender.

1. Auto-pause happens when opt-outs pass 2% or failures pass 10% (after a minimum number of messages). It also pauses the buyer's supplier verification.
2. Read the campaign report: cost per reply, opt-outs, failures. Read a sample of the rendered messages and the template.
3. If the template or targeting was bad: tell the buyer, fix the template (a new approved template, never edit an approved one), and only then re-approve. If the buyer broke the rules, keep the supplier paused.
4. If the provider banned the number or template: stop all sending in that country with the country switch (`/staff/switches/`), tell counsel, and do not retry on another number until the cause is understood.
5. Check that every opt-out in the period is on the do-not-contact list.
6. Write down the cause and the change.
