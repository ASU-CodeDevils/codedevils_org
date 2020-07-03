from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from .serializers import BlacklistDomainSerializer, BlacklistEmailSerializer
from codedevils_org.contrib.email.models import BlacklistDomain, BlacklistEmail


class BlacklistDomainViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = BlacklistDomainSerializer
    queryset = BlacklistDomain.objects.all()
    lookup_field = "domain"

    def get_queryset(self):
        return self.queryset


class BlacklistEmailViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = BlacklistEmailSerializer
    queryset = BlacklistEmail.objects.all()
    lookup_field = "email"

    def get_queryset(self):
        return self.queryset
