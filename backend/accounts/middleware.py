"""Staff routes need a signed-in user with the right role and, for MFA roles, a verified second step (plan 11.2)."""

from django.shortcuts import redirect

from .roles import has_cap, needs_mfa

PROTECTED = ("/admin/", "/staff/")


class StaffMFAMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info
        if path.startswith(PROTECTED) and not path.startswith("/admin/login"):
            user = request.user
            if not user.is_authenticated:
                return redirect(f"/account/login/?next={request.path}")
            if path.startswith("/staff/") and not has_cap(user, "staff_console"):
                from django.http import HttpResponseForbidden

                return HttpResponseForbidden("Not allowed")
            if needs_mfa(user) and not request.session.get("mfa_ok"):
                request.session["pre_mfa_user"] = user.pk
                request.session["pre_mfa_next"] = request.path
                has = hasattr(user, "totp") and user.totp.confirmed
                return redirect("/account/mfa/verify/" if has else "/account/mfa/setup/")
        return self.get_response(request)
