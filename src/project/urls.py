from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("", view=views.HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("units/", include("units.urls")),
    path("employees/", include("employees.urls")),
    path("authorships/", include("authorships.urls")),
    path("articles/", include("articles.urls")),
]
