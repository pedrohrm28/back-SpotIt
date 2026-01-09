from django.urls import path
from rest_framework.routers import DefaultRouter

from core.views import GroupViewSet, ItemViewSet, PermissionViewSet, StatsView, UserViewSet


router = DefaultRouter()
router.register("items", ItemViewSet, basename="item")
router.register("usuarios", UserViewSet, basename="user")
router.register("grupos", GroupViewSet, basename="group")
router.register("permissoes", PermissionViewSet, basename="permission")

urlpatterns = [
    path("stats/", StatsView.as_view(), name="stats"),
] + router.urls
