from django.contrib import admin
from django.urls import include, path
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import ObtainAuthToken

from core.serializers import EmailAuthTokenSerializer


@extend_schema_view(post=extend_schema(tags=["auth"]))
class TokenView(ObtainAuthToken):
    serializer_class = EmailAuthTokenSerializer


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/auth/token/", TokenView.as_view()),
    path("api/", include("core.urls")),
]
