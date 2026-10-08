# Deploy and rollback

**Who:** the engineer on duty. **Needed:** every release, and when a release misbehaves.

## Deploy
1. CI is green on the commit and the pull request is merged. Tag it: `git tag v2026.10.1 && git push --tags`.
2. On the server: `git --git-dir=/srv/alllists/repo.git fetch --tags` then `scripts/deploy.sh v2026.10.1`.
3. The script takes a dump, checks settings, shows the migration plan, migrates, collects static files, switches the `current` link, restarts the web service and calls `/healthz`. If the health check fails it points `current` back at the previous release by itself.
4. Open the home page, one list page, one entry page and `/staff/metrics/`. All alerts that were red before should be unchanged; a new red row is a reason to roll back.

## Roll back
- Code only (no migration in the release): `scripts/rollback.sh`.
- The release migrated: migrations are forward-only. Write a fix-forward release if it is small; otherwise restore the dump the deploy script took first (see `restore.md`) and then run `scripts/rollback.sh`.

## Write down
Tag, time, who, whether the smoke test passed, any rollback and why (add to `docs/DECISIONS.md` only if it changes a rule).
