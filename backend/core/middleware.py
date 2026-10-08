"""Security headers (plan 17.2). The policy allows only this site's own files: no remote images, fonts or scripts (R01)."""

from django.conf import settings

CSP = "; ".join(
    [
        "default-src 'self'",
        "img-src 'self' data:",
        "script-src 'self'",
        "style-src 'self'",
        "style-src-attr 'unsafe-inline'",  # the trust bar sets one custom property per segment
        "font-src 'self'",
        "connect-src 'self'",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "frame-ancestors 'none'",
    ]
)
ADMIN_CSP = "; ".join(
    [
        "default-src 'self'",
        "img-src 'self' data:",
        "script-src 'self'",
        "style-src 'self' 'unsafe-inline'",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "frame-ancestors 'none'",
    ]
)
PERMISSIONS = "camera=(), microphone=(), payment=(), usb=(), geolocation=(self)"


class RejectNullBytesMiddleware:
    """A NUL character in an address, a query or a form value cannot be stored by PostgreSQL and has no honest use, so the
    request is refused with 400 before any code sees it (otherwise it surfaces as a server error)."""

    FORM_TYPES = ("application/x-www-form-urlencoded", "multipart/form-data")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.http import HttpResponseBadRequest

        bad = "\x00" in request.path_info or any("\x00" in k or "\x00" in v for k, v in request.GET.items())
        # webhooks verify a signature over the raw body, which must still be readable, so their bodies are left alone
        if (
            not bad
            and request.method == "POST"
            and request.content_type in self.FORM_TYPES
            and not request.path_info.startswith("/webhooks/")
        ):
            bad = any("\x00" in k or "\x00" in v for k, v in request.POST.items())
        if bad:
            resp = HttpResponseBadRequest("Bad request", content_type="text/plain")
            resp["Cache-Control"] = "no-store"
            return resp
        return self.get_response(request)


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        admin = request.path.startswith("/admin/")
        header = (
            "Content-Security-Policy-Report-Only"
            if getattr(settings, "CSP_REPORT_ONLY", False)
            else "Content-Security-Policy"
        )
        response.setdefault(header, ADMIN_CSP if admin else CSP)
        response.setdefault("Permissions-Policy", PERMISSIONS)
        response.setdefault("Cross-Origin-Opener-Policy", "same-origin")
        # Default-deny for shared caches: only responses that chose their own caching (shared pages, static files, sitemaps)
        # may be stored. Everything else, every account, staff and form page included, is private.
        response.setdefault("Cache-Control", "private, no-store")
        return response
