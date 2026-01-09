from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, permissions, viewsets

from core.models import Item
from core.permissions import IsReporterOrReadOnly
from core.serializers import ItemSerializer


@extend_schema_view(
    list=extend_schema(tags=["items"]),
    retrieve=extend_schema(tags=["items"]),
    create=extend_schema(tags=["items"]),
    update=extend_schema(tags=["items"]),
    partial_update=extend_schema(tags=["items"]),
    destroy=extend_schema(tags=["items"]),
)
class ItemViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsReporterOrReadOnly]

    def get_queryset(self):
        queryset = Item.objects.select_related("reporter").all().order_by("-created_at")
        params = self.request.query_params

        status = params.get("status")
        if status:
            queryset = queryset.filter(status=status)

        reporter = params.get("reporter")
        mine = params.get("mine")
        if reporter == "me" or (mine and mine.lower() in {"1", "true", "yes"}):
            if self.request.user.is_authenticated:
                queryset = queryset.filter(reporter=self.request.user)
            else:
                return Item.objects.none()

        query = params.get("q")
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(location__icontains=query)
                | Q(category__icontains=query)
                | Q(contact_info__icontains=query)
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)
