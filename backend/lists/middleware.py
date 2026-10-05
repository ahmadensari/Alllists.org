from .models import Place


class PreferencesMiddleware:
    """Language, theme, list/cards view and viewer plan. Same URL for everyone; cookies only change presentation."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        c = request.COOKIES
        request.lang = c.get("lang") if c.get("lang") in ("en", "ur") else "en"
        request.theme = c.get("theme") if c.get("theme") in ("light", "dark") else ""
        request.view_mode = c.get("view") if c.get("view") in ("list", "cards") else "list"
        from django.conf import settings
        sub = False
        u = getattr(request, "user", None)
        if u is not None and u.is_authenticated:
            p = getattr(u, "profile", None)
            sub = bool(p and p.subscriber)
        if settings.DEMO_MODE and request.session.get("demo_plan") == "subscriber":
            sub = True
        request.subscriber = sub
        return self.get_response(request)


class LocationMiddleware:
    """Auto location: session choice first, then the edge IP guess (Cloudflare headers), never a redirect.
    The guess only fills the 'near you' piece so the main page stays cacheable and identical for all."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.my_place = None
        pid = request.session.get("place_id")
        if pid:
            request.my_place = Place.objects.filter(pk=pid).first()
        if request.my_place is None:
            country = request.META.get("HTTP_CF_IPCOUNTRY", "").upper()[:2]
            city = request.META.get("HTTP_CF_IPCITY", "")[:120]
            if country and city:
                request.my_place = Place.objects.filter(
                    kind="city", name__iexact=city, country_code=country).first()
            if request.my_place is None and country:
                request.my_place = Place.objects.filter(kind="country", country_code=country).first()
            request.location_source = "guess" if request.my_place else "none"
        else:
            request.location_source = "chosen"
        return self.get_response(request)
