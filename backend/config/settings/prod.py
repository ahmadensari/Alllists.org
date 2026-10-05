"""Production settings: nothing here relaxes base; it only fails fast when required values are missing."""

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F401,F403
from .base import CONTACT_HASH_PEPPER, DEBUG, FIELD_ENCRYPTION_KEYS

if DEBUG:
    raise ImproperlyConfigured("DJANGO_DEBUG must be off in production")
if not FIELD_ENCRYPTION_KEYS or not CONTACT_HASH_PEPPER:
    raise ImproperlyConfigured("Set FIELD_ENCRYPTION_KEYS, FIELD_ENCRYPTION_ACTIVE_KEY and CONTACT_HASH_PEPPER")
