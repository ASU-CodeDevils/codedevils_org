"""Defines the GraphQL schema for custom URLs."""

import graphene

from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation
from graphene_django.types import DjangoObjectType

from codedevils_org.users.models import User, Officer, OfficerPosition
from codedevils_org.users.api.serializers import UserSerializer, OfficerSerializer, OfficerPositionSerializer


class UserNode(DjangoObjectType):
    """
    User information who are not marked anonymous. The actualCount will have the total number of members,
    and the resulting data will be non-anonymous users.
    """
    actual_count = graphene.String()

    class Meta:
        model = User
        interfaces = (Node,)
        lookup_field = "username"
        filter_fields = {
            "username": ["exact"],
            "first_name": ["exact", "icontains", "istartswith"],
            "last_name": ["exact", "icontains", "istartswith"],
            "email": ["exact", "icontains", "istartswith"],
            "name": ["icontains", "istartswith"],
            "anonymous": ["exact"],
            "receive_notifications": ["exact"],
            "city": ["exact", "icontains", "istartswith"],
            "state": ["exact", "icontains", "istartswith"],
            "country": ["exact", "icontains", "istartswith"]
        }

    def resolve_actual_count(self):
        return User.objects.all().count()

    @classmethod
    def get_queryset(cls, queryset, info):
        """Overrides the default queryset to filter anyone who wishes to remain anonymous."""
        return queryset.filter(anonymous=False)


class UserSerializerMutation(SerializerMutation):
    class Meta:
        serializer_class = UserSerializer
        lookup_field = "username"
        model_operations = ["update", "patch"]
        description = "Change/update user information"


class OfficerPositionNode(DjangoObjectType):
    class Meta:
        model = OfficerPosition
        interfaces = (Node,)
        lookup_field = "name"
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "sds_position": ["exact", "icontains", "istartswith"],
            "email": ["exact", "icontains", "istartswith"],
        }
        description = "Officer positions (i.e. President, VP, etc)"


class OfficerPositionSerializerMutation(SerializerMutation):
    class Meta:
        serializer_class = OfficerPositionSerializer
        lookup_field = "name"
        model_operations = ["update", "patch"]
        description = "Change/update officer position information"


class DeleteOfficerPositionMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Meta:
        description = "Delete an officer position"

    class Arguments:
        name = graphene.String()

    @classmethod
    def mutate(cls, **kwargs):
        obj = OfficerPosition.objects.get(name=kwargs["name"])
        obj.delete()
        return cls(ok=True)


class OfficerNode(DjangoObjectType):
    class Meta:
        model = Officer
        interfaces = (Node,)
        filter_fields = {
            "personal_email": ["exact", "icontains", "istartswith"],
        }
        description = "CodeDevils officers"


class OfficerSerializerMutation(SerializerMutation):
    class Meta:
        serializer_class = OfficerSerializer
        model_operations = ["update", "patch"]
        description = "Change/update officer information"


class Query(graphene.ObjectType):
    user = Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)

    officer = Node.Field(OfficerNode)
    officers = DjangoFilterConnectionField(OfficerNode)

    officer_position = Node.Field(OfficerNode)
    officer_positions = DjangoFilterConnectionField(OfficerNode)


class Mutation(graphene.ObjectType):
    update_user = UserSerializerMutation.Field()
    update_officer = OfficerSerializerMutation.Field()
    update_officer_position = OfficerPositionSerializerMutation.Field()
    delete_officer_position = DeleteOfficerPositionMutation.Field()
