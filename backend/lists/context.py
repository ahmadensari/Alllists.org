from django.conf import settings

from . import strings


def site(request):
    lang = getattr(request, "lang", "en")
    return {"T": strings.STRINGS[lang], "lang": lang, "dir": "rtl" if lang == "ur" else "ltr",
            "theme": getattr(request, "theme", ""), "subscriber": getattr(request, "subscriber", False),
            "view_mode": getattr(request, "view_mode", "list"), "my_place": getattr(request, "my_place", None),
            "location_source": getattr(request, "location_source", "none"), "demo_mode": settings.DEMO_MODE}
