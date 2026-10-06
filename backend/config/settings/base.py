"""AllLists settings. Secure by default; everything environment-specific comes from env vars."""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = os.environ.get("DJANGO_DEBUG", "") == "1"
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY") or ("dev-only-insecure-key" if DEBUG else "")
if not SECRET_KEY:
    if "pytest" in sys.modules or os.environ.get("DJANGO_ALLOW_TEST_KEY") == "1":
        SECRET_KEY = "test-key-not-for-production"
    else:
        from django.core.exceptions import ImproperlyConfigured

        raise ImproperlyConfigured("Set DJANGO_SECRET_KEY (or DJANGO_DEBUG=1 for local development).")
ALLOWED_HOSTS = [h for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,testserver").split(",") if h]
CSRF_TRUSTED_ORIGINS = [o for o in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if o]

# Demo switch lets a visitor flip between Free and Subscriber to preview. Never on in production.
DEMO_MODE = os.environ.get("ALLLISTS_DEMO", "1" if DEBUG else "0") == "1"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "places",
    "taxonomy",
    "entries",
    "intake",
    "analytics",
    "access",
    "accounts",
    "moderation",
    "ledger",
    "billing",
    "outreach",
    "volunteers",
    "agents",
    "catalog",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "core.middleware.RejectNullBytesMiddleware",
    "catalog.middleware.LanguagePrefixMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "accounts.middleware.StaffMFAMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "catalog.middleware.TemplateVersionMiddleware",
    "core.middleware.SecurityHeadersMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "catalog.context.site",
            ]
        },
    }
]
WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.environ.get("ALLLISTS_DB", BASE_DIR / "db.sqlite3")}
}
if os.environ.get("POSTGRES_DB"):  # PostgreSQL in production (install psycopg)
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ.get("POSTGRES_USER", ""),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
if os.environ.get("DATABASE_REPLICA_HOST") and os.environ.get("POSTGRES_DB"):  # read replica (plan P6.03)
    DATABASES["replica"] = {
        **DATABASES["default"],
        "HOST": os.environ["DATABASE_REPLICA_HOST"],
        "USER": os.environ.get("POSTGRES_REPLICA_USER", DATABASES["default"]["USER"]),
        "PASSWORD": os.environ.get("POSTGRES_REPLICA_PASSWORD", DATABASES["default"]["PASSWORD"]),
        "TEST": {"MIRROR": "default"},
    }
    DATABASE_ROUTERS = ["config.dbrouter.ReplicaRouter"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"django.contrib.auth.password_validation.{n}"}
    for n in (
        "UserAttributeSimilarityValidator",
        "MinimumLengthValidator",
        "CommonPasswordValidator",
        "NumericPasswordValidator",
    )
]
LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_ROOT.mkdir(exist_ok=True)
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}

# Security headers and cookies
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
if not DEBUG:
    SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = os.environ.get("DJANGO_INSECURE_COOKIES", "") != "1"
    SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_HSTS_SECONDS", "0"))
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Business rules (decisions Q-S15 and the 50/40/30 phase decision)
CONTRIBUTOR_PHASE_RATES = {1: 50, 2: 40, 3: 30}
CURRENT_PHASE = int(os.environ.get("ALLLISTS_PHASE", "1"))
FREE_PREVIEW_NAMES = 25  # names-only preview beyond the visitor's own place
FREE_MAX_SPECIALITIES = 3

# Field encryption and keyed hashes (plan section 17). Dev values are throwaway; production sets real ones.
FIELD_ENCRYPTION_KEYS = {}
FIELD_ENCRYPTION_ACTIVE_KEY = os.environ.get("FIELD_ENCRYPTION_ACTIVE_KEY", "")
for _item in [i for i in os.environ.get("FIELD_ENCRYPTION_KEYS", "").split(",") if i]:
    _kid, _, _key = _item.partition(":")
    FIELD_ENCRYPTION_KEYS[_kid] = _key
CONTACT_HASH_PEPPER = os.environ.get("CONTACT_HASH_PEPPER", "")
if not FIELD_ENCRYPTION_KEYS and (DEBUG or "pytest" in sys.modules):
    import base64  # noqa: E402
    import hashlib  # noqa: E402

    # Stable across restarts (derived from the dev secret) so data seeded in one run can still be read in the next.
    FIELD_ENCRYPTION_KEYS = {
        "dev": base64.urlsafe_b64encode(hashlib.sha256(b"dev-field-key:" + SECRET_KEY.encode()).digest()).decode()
    }
    FIELD_ENCRYPTION_ACTIVE_KEY = "dev"
    CONTACT_HASH_PEPPER = CONTACT_HASH_PEPPER or "dev-pepper-not-secret"

# Verification defaults (plan section 6.3, Q-T4): validity in days per level; grace before an expired entry returns to draft
CHECK_VALIDITY_DAYS = {"surveyor": 365, "owner": 365, "ai": 180}
GRACE_DAYS = 90
INDEX_THRESHOLD = 10
TEMPLATE_VERSION = "1"  # bump on any template change; part of cache keys and ETags (rule R25)
PAGE_SIZE = 25

# Passwords: Argon2id first; PBKDF2 stays only so older hashes can be read and upgraded.
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "1") == "1"
EXTRACT_DIR = os.environ.get("EXTRACT_DIR", str(BASE_DIR / "var" / "extracts"))
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "AllLists <no-reply@alllists.com>")
LOGIN_MAX_PER_ACCOUNT = 5
LOGIN_MAX_PER_ADDRESS = 20
SITE_URL = os.environ.get("SITE_URL", "http://localhost:8000")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"scrub": {"()": "core.logscrub.ScrubFilter"}},
    "handlers": {"console": {"class": "logging.StreamHandler", "filters": ["scrub"]}},
    "root": {"handlers": ["console"], "level": os.environ.get("LOG_LEVEL", "INFO")},
}
CSP_REPORT_ONLY = os.environ.get("CSP_REPORT_ONLY", "") == "1"

REFUND_HOLD_DAYS = 14
SUBSCRIPTION_SCOPE_MULTIPLIER = {1: 20, 2: 10, 3: 1}  # place depth (country, region, city) -> times the city price
SUBSCRIPTION_ANY_TYPE_MULTIPLIER = 3  # a subscription with no list type covers every list type in the place
COMPANY_DETAILS = {  # the seller on every invoice; fill in once the company exists
    "name": os.environ.get("COMPANY_NAME", "AllLists"),
    "address": os.environ.get("COMPANY_ADDRESS", ""),
    "tax_id": os.environ.get("COMPANY_TAX_ID", ""),
}
REPORT_RATES_TO_USD = {}  # currency -> units of USD per unit; only used for the indicative consolidated line
TAX_RATES = {}  # country code -> percent (decimal string), configured per country; empty means none
PAYMENT_WEBHOOK_SECRETS = {}  # provider name -> shared secret (set per environment; none by default)
PAYMENT_INSTRUCTIONS = os.environ.get("PAYMENT_INSTRUCTIONS", "")

# AI agent track (plan 7.6): nothing runs until the caps are set. Amounts are minor units (cents).
AI_KILL_SWITCH = os.environ.get("AI_KILL_SWITCH", "") == "1"
AI_DAILY_CAP_MINOR = int(os.environ.get("AI_DAILY_CAP_MINOR", "0"))
AI_MONTHLY_CAP_MINOR = int(os.environ.get("AI_MONTHLY_CAP_MINOR", "0"))
AI_JOB_CAP_MINOR = int(os.environ.get("AI_JOB_CAP_MINOR", "50"))

# Subscription allocation (plan 12.2, F8): weight 1.0 plus a bonus for entries re-verified recently
# Social sign-in (plan P6.02): a provider is on only when its client id and secret are set.
SOCIAL_PROVIDERS = {
    name: {
        "client_id": os.environ.get(f"{name.upper()}_CLIENT_ID", ""),
        "client_secret": os.environ.get(f"{name.upper()}_CLIENT_SECRET", ""),
    }
    for name in ("google", "orcid")
    if os.environ.get(f"{name.upper()}_CLIENT_ID")
}
ALERT_EMAILS = [e for e in os.environ.get("ALERT_EMAILS", "").split(",") if e]  # who is told when a check turns red
FRESHNESS_BONUS = "0.25"
FRESHNESS_DAYS = 90
PLACEMENT_SLOTS = 2  # sponsored slots per list (Q-T8)

# Outreach (plan 13): everything stays off until counsel clears a country; these are the rules once it is on.
OUTREACH_SHARE_PERCENT = (
    None  # contributor share of outreach revenue (decision F7 leaves the figure open); must be set to start
)
OUTREACH_PRICE_MINOR = {"whatsapp": 5, "sms": 2, "email": 1}
OUTREACH_WEEKLY_CAP_PER_SHOP = 2
OUTREACH_DAILY_CAP_PER_SENDER = 500
OUTREACH_DEFAULT_WINDOW = (9, 21)  # local hours in which messages may be sent
OUTREACH_QUIET_WINDOW = {"AE": (9, 18)}
OUTREACH_TZ = {"PK": "Asia/Karachi", "AE": "Asia/Dubai", "SA": "Asia/Riyadh"}
OUTREACH_PAUSE_OPTOUT = 0.02
OUTREACH_PAUSE_FAILURE = 0.10
OUTREACH_PAUSE_MIN_SAMPLE = 50
MESSAGING_WEBHOOK_SECRETS = {}
