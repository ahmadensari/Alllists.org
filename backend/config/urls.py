from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/login/", RedirectView.as_view(url="/account/login/?next=/admin/", query_string=False)),
    path("admin/", admin.site.urls),
    path("account/", include("accounts.urls")),
    path("", include("catalog.urls")),
]

handler404 = "catalog.views.not_found"
