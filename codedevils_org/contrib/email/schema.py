import graphene

from graphene import Node
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


class DeleteBlacklistDomainMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Meta:
        description = "Delete a blacklisted domain"

    class Arguments:
        domain = graphene.String()

    @classmethod
    def mutate(cls, **kwargs):
        obj = BlacklistDomain.objects.get(domain=kwargs["domain"])
        obj.delete()
        return cls(ok=True)


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


class DeleteBlacklistEmailMutation(graphene.Mutation):
    ok = graphene.Boolean()

    class Meta:
        description = "Delete a blacklisted email"

    class Arguments:
        email = graphene.String()

    @classmethod
    def mutate(cls, **kwargs):
        obj = BlacklistEmail.objects.get(email=kwargs["email"])
        obj.delete()
        return cls(ok=True)


class Query(object):
    domain = Node.Field(BlacklistDomainNode)
    domains = DjangoFilterConnectionField(BlacklistDomainNode)

    email = Node.Field(BlacklistEmailNode)
    emails = DjangoFilterConnectionField(BlacklistEmailNode)


class Mutation(graphene.ObjectType):
    update_domain = BlacklistDomainSerializerMutation.Field()
    update_email = BlacklistEmailSerializerMutation.Field()
    delete_blacklist_domain = DeleteBlacklistDomainMutation.Field()
    delete_blacklist_email = DeleteBlacklistEmailMutation.Field()
