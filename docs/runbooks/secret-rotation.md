# Secret rotation

**Who:** the founder with the engineer. **Needed:** every six months; at once after any suspected exposure; when someone with access leaves. **First occasion:** the founder pasted a source-control token and a database password into a chat early in the project; both must be treated as exposed and replaced before launch.

## What exists
`DJANGO_SECRET_KEY`, database passwords (`alllists_app`, `alllists_readonly`, owner), `FIELD_ENCRYPTION_KEYS`, `CONTACT_HASH_PEPPER`, payment-provider and messaging-provider keys and webhook secrets, the email password, GitHub and hosting tokens.

## Steps
1. **Database passwords:** `ALTER ROLE alllists_app PASSWORD '...'`, update `/etc/alllists/alllists.env`, restart the web service.
2. **Django secret key:** change it and restart. All sessions end; that is expected.
3. **Field encryption key:** add a new key id to `FIELD_ENCRYPTION_KEYS`, make it the active key, restart. New writes use the new key and old rows still decrypt. Then run the re-encryption pass (`python manage.py shell -c "from core.crypto import reencrypt_all; print(reencrypt_all())"`) and, once it reports zero old rows, remove the old key.
4. **Contact hash pepper:** do NOT change it casually. It keys the do-not-contact list and the lookups for contacts; changing it makes every stored hash unmatched. If it must change, rebuild every `value_hash` and every suppression hash in one maintenance window first.
5. **Provider keys:** create the new key at the provider, update the environment, restart, delete the old key at the provider, send a test message or sandbox payment.
6. **Tokens:** revoke in the provider's console, issue new ones, update the places that use them (CI secrets, deploy server).
7. Search the repository history and chats for the old values; if any are in git history, rotating is the only fix.

## Write down
Date, which secrets, who, and confirmation that the old values no longer work.
