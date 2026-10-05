from django.conf import settings

from . import strings
from .strings import Translator


def site(request):
    lang = getattr(request, "lang", "en")
    other = "ur" if lang == "en" else "en"
    qs = request.META.get("QUERY_STRING", "") if hasattr(request, "META") else ""
    path = getattr(request, "path_info", "/")
    alt_url = ("/ur" if other == "ur" else "") + path + (("?" + qs) if qs else "")
    return {
        "alt_url": alt_url,
        "lang": lang,
        "dir": "rtl" if lang == "ur" else "ltr",
        "prefix": getattr(request, "prefix", ""),
        "T": Translator(lang),
        "demo_mode": settings.DEMO_MODE,
        "template_version": settings.TEMPLATE_VERSION,
        "other_lang": "ur" if lang == "en" else "en",
        "languages": strings.LANGUAGES,
    }
