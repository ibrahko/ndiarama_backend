from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.http import JsonResponse, HttpResponse

from django.conf import settings
from django.conf.urls.static import static

def api_root(request):
    return HttpResponse('{"status": "ok", "service": "NDIARAMA API"}', 
                        content_type="application/json", 
                        status=200)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', api_root),
    path("api/core/", include("apps.core.urls")),
    path("api/media/", include("apps.mediaapp.urls")),
    path("api/services/", include("apps.services.urls")),
    path("api/community/", include("apps.community.urls")),
    path("api/communication/", include("apps.communication.urls")),
    path("api/", include("apps.api.urls")),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)