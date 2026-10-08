"""Language prefix and template version (plan 3.4, 8.2). Nothing here reads cookies or the session, so the shell
of every page stays identical and shareable by a CDN (rule R05)."""

from django.conf import settings


class LanguagePrefixMiddleware:
    """`/ur/...` serves Urdu; the prefix is stripped before URL resolution and `request.prefix` keeps it for links."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        if path == "/ur" or path.startswith("/ur/"):
            request.lang, request.prefix = "ur", "/ur"
            request.path_info = path[3:] or "/"
        else:
            request.lang, request.prefix = "en", ""
        return self.get_response(request)


class TemplateVersionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["X-Template-Version"] = settings.TEMPLATE_VERSION
        return response
