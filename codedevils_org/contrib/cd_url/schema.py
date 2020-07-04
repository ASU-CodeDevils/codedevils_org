"""Defines the GraphQL schema for custom URLs."""

from graphene import Node, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation
from graphene_django.types import DjangoObjectType

from codedevils_org.contrib.cd_url.models import CustomUrl
from codedevils_org.contrib.cd_url.api.serializers import CustomUrlSerializer


class CustomUrlNode(DjangoObjectType):
    """Provides links to all CodeDevils custom URLs."""
    class Meta:
        model = CustomUrl
        interfaces = (Node,)
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "slug": ["exact"]
        }
        description = "Links to CodeDevils different online services"


class CustomUrlSerializerMutation(SerializerMutation):
    class Meta:
        serializer_class = CustomUrlSerializer
        lookup_field = "slug"
        model_operations = ["update", "patch"]
        description = "Change/update a custom link"


class Query(object):
    link = Node.Field(CustomUrlNode)
    links = DjangoFilterConnectionField(CustomUrlNode)


class Mutation(ObjectType):
    update_link = CustomUrlSerializerMutation.Field()
