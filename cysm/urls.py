from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from registeration.urls import urlpatterns as reg_urls
from program.urls import urlpatterns as program_urls
from userauth.urls import urlpatterns as userauth_urls

urlpatterns = [
   
    # YOUR PATTERNS
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),

    path("admin/", admin.site.urls),
    path("reg/", include(reg_urls)),
    path("program/", include(program_urls)),
    path("user_auth/", include(userauth_urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)