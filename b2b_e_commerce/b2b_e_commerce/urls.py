from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('merchant/',include('merchant.urls')),
    path('api/schema/',SpectacularAPIView.as_view(), name = 'api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name = 'api-schema'), name = 'api-docs'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]


if settings.DEBUG:
    urlpatterns+static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT,
    )