"""Production settings: nothing here relaxes base; it only fails fast when required values are missing."""

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F401,F403
from .base import CONTACT_HASH_PEPPER, DEBUG, FIELD_ENCRYPTION_ACTIVE_KEY, FIELD_ENCRYPTION_KEYS

if DEBUG:
    raise ImproperlyConfigured("DJANGO_DEBUG must be off in production")
if not FIELD_ENCRYPTION_KEYS or not CONTACT_HASH_PEPPER:
    raise ImproperlyConfigured("Set FIELD_ENCRYPTION_KEYS, FIELD_ENCRYPTION_ACTIVE_KEY and CONTACT_HASH_PEPPER")
if FIELD_ENCRYPTION_ACTIVE_KEY not in FIELD_ENCRYPTION_KEYS:
    raise ImproperlyConfigured("FIELD_ENCRYPTION_ACTIVE_KEY must name one of the keys in FIELD_ENCRYPTION_KEYS")

# Behind the reverse proxy (Caddy or Nginx), which terminates HTTPS and passes X-Forwarded-Proto.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SECURE_REDIRECT_EXEMPT = [
    r"^healthz$"
]  # the deploy smoke test and uptime monitors call it over plain http on localhost
# HSTS starts short (30 days) so a mistake can be undone; raise it with ALLLISTS_HSTS_SECONDS once HTTPS is proven.
SECURE_HSTS_SECONDS = int(__import__("os").environ.get("ALLLISTS_HSTS_SECONDS", "2592000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
