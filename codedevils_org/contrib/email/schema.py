from graphene import Node, ObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.rest_framework.mutation import SerializerMutation
from graphene_django.types import DjangoObjectType

from codedevils_org.contrib.email.models import BlacklistDomain, BlacklistEmail
from codedevils_org.contrib.email.api.serializers import BlacklistDomainSerializer, BlacklistEmailSerializer


class BlacklistDomainNode(DjangoObjectType):
    class Meta:
        model = BlacklistDomain
        interfaces = (Node,)
        filter_fields = ["domain", "is_blocked", "blocked_until"]
        description = "Domains that are blacklisted from contacting CodeDevils or using CodeDevils' services"


class BlacklistDomainSerializerMutation(SerializerMutation):
    class Meta:
        serializer_class = BlacklistDomainSerializer
        lookup_field = "domain"
        model_operations = ["update", "patch"]
        description = "Change/update a blacklisted domain"


class BlacklistEmailNode(DjangoObjectType):
    class Meta:
        model = BlacklistEmail
        interfaces = (Node,)
        filter_fields = ["email", "is_blocked", "blocked_until"]
        description = "Emails that are blacklisted from contacting CodeDevils or using CodeDevils' services"


class BlacklistEmailSerializerMutation(SerializerMutation):
    class Meta:
        serializer_class = BlacklistEmailSerializer
        lookup_field = "email"
        model_operations = ["update", "patch"]
        description = "Change/update a blacklisted email"


class Query(object):
    domain = Node.Field(BlacklistDomainNode)
    domains = DjangoFilterConnectionField(BlacklistDomainNode)

    email = Node.Field(BlacklistEmailNode)
    emails = DjangoFilterConnectionField(BlacklistEmailNode)


class Mutation(ObjectType):
    update_domain = BlacklistDomainSerializerMutation.Field()
    update_email = BlacklistEmailSerializerMutation.Field()
