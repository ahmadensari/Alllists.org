# Template rollback

**Who:** the engineer for page templates; a moderator for message templates. **Needed:** a page or message change breaks something.

- **Page templates:** `TEMPLATE_VERSION` is part of every cached page's address. To roll back: deploy the previous release (`rollback.sh`) which carries the previous version string; caches repopulate. If the CDN holds a bad page, purge by path.
- **Message templates:** never edit an approved template. Disable the bad one (provider state to `rejected` in the console), pause campaigns that use it, create a corrected template, send it for approval, and move campaigns to it.
- Check one list page, one entry page and the Urdu version after the change.
