from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # 3rd party apps URLs
    path("__debug__/", include("debug_toolbar.urls")),
]
