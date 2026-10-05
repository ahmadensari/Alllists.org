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
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "core", "places", "taxonomy", "entries", "intake",
    "lists",  # legacy demo app, replaced by catalog in phase P2
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "lists.middleware.PreferencesMiddleware",
    "lists.middleware.LocationMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
        "lists.context.site",
    ]},
}]
WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3",
                         "NAME": os.environ.get("ALLLISTS_DB", BASE_DIR / "db.sqlite3")}}
if os.environ.get("POSTGRES_DB"):  # PostgreSQL in production (install psycopg)
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql", "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ.get("POSTGRES_USER", ""), "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": os.environ.get("POSTGRES_HOST", "localhost"), "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = [{"NAME": f"django.contrib.auth.password_validation.{n}"} for n in
                            ("UserAttributeSimilarityValidator", "MinimumLengthValidator",
                             "CommonPasswordValidator", "NumericPasswordValidator")]
LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_ROOT.mkdir(exist_ok=True)
STORAGES = {"default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
            "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"}}

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
FREE_PREVIEW_NAMES = 25          # names-only preview beyond the visitor's own place
FREE_MAX_SPECIALITIES = 3

# Field encryption and keyed hashes (plan section 17). Dev values are throwaway; production sets real ones.
FIELD_ENCRYPTION_KEYS = {}
FIELD_ENCRYPTION_ACTIVE_KEY = os.environ.get("FIELD_ENCRYPTION_ACTIVE_KEY", "")
for _item in [i for i in os.environ.get("FIELD_ENCRYPTION_KEYS", "").split(",") if i]:
    _kid, _, _key = _item.partition(":")
    FIELD_ENCRYPTION_KEYS[_kid] = _key
CONTACT_HASH_PEPPER = os.environ.get("CONTACT_HASH_PEPPER", "")
if not FIELD_ENCRYPTION_KEYS and (DEBUG or "pytest" in sys.modules):
    from cryptography.fernet import Fernet  # noqa: E402
    FIELD_ENCRYPTION_KEYS = {"dev": Fernet.generate_key().decode()}
    FIELD_ENCRYPTION_ACTIVE_KEY = "dev"
    CONTACT_HASH_PEPPER = CONTACT_HASH_PEPPER or "dev-pepper-not-secret"

# Verification defaults (plan section 6.3, Q-T4): validity in days per level; grace before an expired entry returns to draft
CHECK_VALIDITY_DAYS = {"surveyor": 365, "owner": 365, "ai": 180}
GRACE_DAYS = 90
INDEX_THRESHOLD = 10
