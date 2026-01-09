from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Item


class StatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = {
            "items_total": Item.objects.count(),
            "items_recovered": Item.objects.filter(status=Item.Status.RETURNED).count(),
            "active_users": get_user_model().objects.filter(is_active=True).count(),
        }
        return Response(data)
