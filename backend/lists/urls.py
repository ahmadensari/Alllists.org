from django.urls import path, re_path

from . import views

handler404 = "lists.views.not_found"

urlpatterns = [
    path("", views.home, name="home"),
    path("healthz", views.healthz),
    path("prefs/", views.prefs, name="prefs"),
    path("enquiry/", views.enquiry, name="enquiry"),
    path("e/<int:pk>/", views.entry_page, name="entry"),
    path("e/<int:pk>/<str:kind>/", views.report, name="report"),
    re_path(r"^p/(?P<path>[\w\-/]+?)/l/(?P<type_slug>[\w\-]+)/$", views.list_page, name="list"),
    re_path(r"^p/(?P<path>[\w\-/]+)/$", views.place_page, name="place"),
]
