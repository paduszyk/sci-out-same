from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path("admin/", admin.site.urls),
    # 3rd party apps URLs
    path("__debug__/", include("debug_toolbar.urls")),
    # Project apps URLs
    path("units/", include("units.urls")),
    path("employees/", include("employees.urls")),
]

urlpatterns = (
    urlpatterns
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

admin.site.site_header = _("Baza dorobku pracowników")
admin.site.site_title = _("BDP")
admin.site.index_title = _("Administracja")
