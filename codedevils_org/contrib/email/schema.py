from graphene import Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from .models import BlacklistDomain, BlacklistEmail


class BlacklistDomainNode(DjangoObjectType):
    class Meta:
        model = BlacklistDomain
        interfaces = (Node,)
        filter_fields = ["domain", "is_blocked", "blocked_until"]
        description = "Domains that are blacklisted from contacting CodeDevils or using CodeDevils' services"


class BlacklistEmailNode(DjangoObjectType):
    class Meta:
        model = BlacklistEmail
        interfaces = (Node,)
        filter_fields = ["email", "is_blocked", "blocked_until"]
        description = "Emails that are blacklisted from contacting CodeDevils or using CodeDevils' services"


class Query(object):
    domain = Node.Field(BlacklistDomainNode)
    domains = DjangoFilterConnectionField(BlacklistDomainNode)

    email = Node.Field(BlacklistEmailNode)
    emails = DjangoFilterConnectionField(BlacklistEmailNode)
