from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup),
    path("login/", views.login_view),
    path("logout/", views.logout_view),
    path("verify/<str:token>/", views.verify_email),
    path("mfa/setup/", views.mfa_setup),
    path("mfa/verify/", views.mfa_verify),
    path("delete/", views.delete_account),
    path("security/", views.security),
    path("social/<str:provider>/", views.social_start),
    path("social/<str:provider>/callback/", views.social_callback),
    path(
        "password/reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/password_reset_email.txt",
            success_url="/account/password/reset/sent/",
        ),
    ),
    path(
        "password/reset/sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/message.html",
            extra_context={
                "heading": "Check your email",
                "body": "If that address is registered, a reset link is on its way.",
                "robots": "noindex,follow",
                "title": "AllLists",
            },
        ),
    ),
    path(
        "password/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url="/account/login/",
            extra_context={"robots": "noindex,follow", "title": "AllLists"},
        ),
    ),
    path("", views.dashboard),
]
