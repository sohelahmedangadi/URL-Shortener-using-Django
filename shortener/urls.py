from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("created/<str:short_code>/", views.link_created, name="link_created"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/<str:short_code>/stats/", views.link_stats, name="link_stats"),
    path("dashboard/<str:short_code>/toggle/", views.toggle_link_active, name="toggle_link_active"),
    path("dashboard/<str:short_code>/delete/", views.delete_link, name="delete_link"),
    # Catch-all short code redirect MUST stay last: anything above this line
    # takes priority so route names like "dashboard" never get treated as a code.
    path("<str:short_code>/", views.redirect_short_url, name="redirect_short_url"),
]
