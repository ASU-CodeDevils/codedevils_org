import graphene

from django.contrib.auth import get_user_model

from graphene_django.types import DjangoObjectType
from rest_framework.authtoken.models import Token

User = get_user_model()


class AuthToken(DjangoObjectType):
    class Meta:
        model = Token
        description = "Authorization token needed for the GraphQL endpoint"


class Query(graphene.ObjectType):
    token = graphene.Field(
        AuthToken,
        username=graphene.String(required=True),
        password=graphene.String(required=True),
    )

    def resolve_token(self, info, username, password):
        user = User.objects.get(username__exact=username)
        password_checks = user.check_password(password)
        if password_checks:
            return Token.objects.get(user=user)
        else:
            raise Token.DoesNotExist("invalid token")
