from rest_framework.mixins import (
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from codedevils_org.contrib.cd_url.models import CustomUrl

from .serializers import CustomUrlSerializer


class CustomUrlViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = CustomUrlSerializer
    queryset = CustomUrl.objects.all()
    lookup_field = "slug"

    def get_queryset(self):
        return self.queryset
