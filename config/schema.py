"""Defines the schema for graphene"""
import graphene
from graphene_django.debug import DjangoDebug

import codedevils_org.users.schema
import codedevils_org.contrib.cd_url.schema
import codedevils_org.contrib.email.schema


class Query(
        codedevils_org.users.schema.Query,
        codedevils_org.contrib.cd_url.schema.Query,
        codedevils_org.contrib.email.schema.Query,
        graphene.ObjectType,
):
    debug = graphene.Field(DjangoDebug, name="_debug")


schema = graphene.Schema(query=Query)
