from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path

maps = {}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": maps}, name="django.contrib.sitemaps.views.sitemap"),
]
