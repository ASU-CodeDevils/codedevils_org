from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import CustomUrlSerializer
from codedevils_org.contrib.cd_url.models import CustomUrl


class CustomUrlViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = CustomUrlSerializer
    queryset = CustomUrl.objects.all()
    lookup_field = "slug"

    def get_queryset(self):
        return self.queryset
