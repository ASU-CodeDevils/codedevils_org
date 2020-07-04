"""Defines the GraphQL schema for custom URLs."""

from graphene import Node, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation
from graphene_django.types import DjangoObjectType

from codedevils_org.users.models import User, Officer, OfficerPosition
from codedevils_org.users.api.serializers import UserSerializer


class UserNode(DjangoObjectType):
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
        description = "User relay node"

    @classmethod
    def get_queryset(cls, queryset, info):
        """Overrides the default queryset to redact personal info if the user wishes to remain anonymous."""
        REDACTED = "REDACTED"
        if queryset.filter(anonymous=True).exists():
            for user in queryset.filter(anonymous=True):
                user.username = REDACTED
                user.first_name = REDACTED
                user.last_name = REDACTED
                user.name = REDACTED
                user.dob = REDACTED
                user.bio = REDACTED
        return queryset


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


class OfficerNode(DjangoObjectType):
    class Meta:
        model = Officer
        interfaces = (Node,)
        filter_fields = {
            "personal_email": ["exact", "icontains", "istartswith"],
        }
        description = "CodeDevils officers"


class Query(object):
    user = Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)

    officer = Node.Field(OfficerNode)
    officers = DjangoFilterConnectionField(OfficerNode)

    officer_position = Node.Field(OfficerNode)
    officer_positions = DjangoFilterConnectionField(OfficerNode)


class Mutation(ObjectType):
    update_user = UserSerializerMutation.Field()
