"""Defines the schema for graphene"""
import graphene
from graphene_django.debug import DjangoDebug

from codedevils_org.users import schema as user_schema
from codedevils_org.contrib.cd_url import schema as cdurl_schema
from codedevils_org.contrib.email import schema as email_schema
from config.graphene import auth as auth_schema


class Query(
    user_schema.Query,
    cdurl_schema.Query,
    email_schema.Query,
    auth_schema.Query,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(
    user_schema.Mutation,
    cdurl_schema.Mutation,
    email_schema.Mutation,
    graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=Query, mutation=Mutation)
