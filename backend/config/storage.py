"""Static file storage for production: hashed names when the build has run, plain names when it has not.

`CompressedManifestStaticFilesStorage` gives every file a content hash (app.3f2a1c.css) that browsers and the CDN can keep
for a year. On its own it raises an error for every page if `collectstatic` was forgotten, which turns a missed step into
an outage. This subclass falls back to the plain name instead; `scripts/deploy.sh` always runs collectstatic."""

from whitenoise.storage import CompressedManifestStaticFilesStorage


class SafeManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False

    def stored_name(self, name):
        try:
            return super().stored_name(name)
        except ValueError:
            return name

    def hashed_name(self, name, content=None, filename=None):
        try:
            return super().hashed_name(name, content, filename)
        except ValueError:
            return name
