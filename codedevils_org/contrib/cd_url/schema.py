"""Defines the GraphQL schema for custom URLs."""

from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from .models import CustomUrl


class CustomUrlNode(DjangoObjectType):
    """Provides links to all CodeDevils custom URLs."""
    class Meta:
        model = CustomUrl
        interfaces = (Node,)
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "slug": ["exact"]
        }


class Query(object):
    link = Node.Field(CustomUrlNode)
    links = DjangoFilterConnectionField(CustomUrlNode)
