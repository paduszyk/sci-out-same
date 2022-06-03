from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("units/", include("units.urls")),
    path("employees/", include("employees.urls")),
]
