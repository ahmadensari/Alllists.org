from django.contrib import admin
from billing import views as billing_views
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/login/", RedirectView.as_view(url="/account/login/?next=/admin/", query_string=False)),
    path("admin/", admin.site.urls),
    path("account/", include("accounts.urls")),
    path("account/subscription/", billing_views.subscription_page),
    path("account/orders/<str:ref>/", billing_views.order_page),
    path("webhooks/payments/<str:provider>/", billing_views.webhook),
    path("staff/orders/", billing_views.staff_orders),
    path("", include("catalog.urls")),
]

handler404 = "catalog.views.not_found"
