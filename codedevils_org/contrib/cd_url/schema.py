"""Defines the GraphQL schema for custom URLs."""

import graphene
from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation
from graphene_django.types import DjangoObjectType

from codedevils_org.contrib.cd_url.api.serializers import CustomUrlSerializer
from codedevils_org.contrib.cd_url.models import CustomUrl


class CustomUrlNode(DjangoObjectType):
    """Provides links to all CodeDevils custom URLs."""

    class Meta:
        model = CustomUrl
        interfaces = (Node,)
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "slug": ["exact"],
        }
        description = "Links to CodeDevils different online services"


class CustomUrlSerializerMutation(SerializerMutation):
    class Meta:
        serializer_class = CustomUrlSerializer
        lookup_field = "slug"
        model_operations = ["update", "patch"]
        description = "Change/update a custom link"


class DeleteCustomUrlMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Meta:
        description = "Delete a custom link"

    class Arguments:
        slug = graphene.String()

    @classmethod
    def mutate(cls, **kwargs):
        obj = CustomUrl.objects.get(slug=kwargs["slug"])
        obj.delete()
        return cls(ok=True)


class Query(object):
    link = graphene.Node.Field(CustomUrlNode)
    links = DjangoFilterConnectionField(CustomUrlNode)


class Mutation(graphene.ObjectType):
    update_link = CustomUrlSerializerMutation.Field()
    delete_link = DeleteCustomUrlMutation.Field()
