"""The visitor's address, trusted only from the right header (security requirement AS-01)."""

from django.conf import settings


def client_address(request):
    """Use Cloudflare's header only when the site is configured to sit behind Cloudflare; otherwise the socket address."""
    if getattr(settings, "BEHIND_CLOUDFLARE", False):
        forwarded = request.META.get("HTTP_CF_CONNECTING_IP")
        if forwarded:
            return forwarded
    return request.META.get("REMOTE_ADDR", "")
