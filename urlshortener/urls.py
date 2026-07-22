from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    # shortener.urls owns the root, including the catch-all "/<short_code>/"
    # redirect route, so it must be included last.
    path("", include("shortener.urls")),
]
