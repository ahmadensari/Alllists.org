from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.world, name="world"),
    path("healthz", views.healthz),
    path("robots.txt", views.robots_txt),
    path("sitemap.xml", views.sitemap_index),
    path("sitemaps/<str:cc>-<int:n>.xml", views.sitemap_shard),
    path("prefs/", views.prefs, name="prefs"),
    path("_f/near-you/", views.frag_near_you),
    path("_f/list/", views.frag_list),
    path("_f/entry/<str:uid>/", views.frag_entry),
    path("e/<str:uid>/", views.entry_page),
    path("e/<str:uid>/<slug:slug>/", views.entry_page),
    re_path(r"^(?P<path>[\w\-]+(?:/[\w\-]+)*)/$", views.dispatch, name="dispatch"),
]
