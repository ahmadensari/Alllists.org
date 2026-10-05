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
        return response
