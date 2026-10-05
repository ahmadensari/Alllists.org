from django.contrib import admin
from billing import views as billing_views
from outreach import views as outreach_views
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/login/", RedirectView.as_view(url="/account/login/?next=/admin/", query_string=False)),
    path("admin/", admin.site.urls),
    path("account/", include("accounts.urls")),
    path("account/subscription/", billing_views.subscription_page),
    path("account/orders/<str:ref>/", billing_views.order_page),
    path("account/orders/<str:ref>/invoice/", billing_views.invoice_page),
    path("staff/revenue/", billing_views.staff_revenue),
    path("webhooks/payments/<str:provider>/", billing_views.webhook),
    path("staff/orders/", billing_views.staff_orders),
    path("webhooks/messaging/<str:provider>/", outreach_views.messaging_webhook),
    path("", include("catalog.urls")),
]

handler404 = "catalog.views.not_found"
