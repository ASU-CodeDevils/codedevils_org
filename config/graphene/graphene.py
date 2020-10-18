"""
This is an authentication wrapper for GraphQL to be able to use the same TokenAuthentication
as used in django rest framework.
"""
import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated


class AuthenticatedGraphQLView(GraphQLView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def authenticate_request(self, request):
        for auth_class in self.authentication_classes:
            auth_tuple = auth_class().authenticate(request)
            if auth_tuple:
                request.user, request.token = auth_tuple
                break

    def check_permissions(self, request):
        for permission_class in self.permission_classes:
            if not permission_class().has_permission(request, self):
                return False

        # check the user has a token
        try:
            Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            return False

        return True

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        try:
            self.authenticate_request(request)
            has_permission = self.check_permissions(request)
            if not has_permission:
                return HttpResponse(
                    json.dumps({"errors": ["permission denied"]}),
                    status=status.HTTP_403_FORBIDDEN,
                    content_type="application/json",
                )
        except AuthenticationFailed as auth_failed_error:
            return HttpResponse(
                json.dumps({"errors": [str(auth_failed_error)]}),
                status=status.HTTP_401_UNAUTHORIZED,
                content_type="application/json",
            )
        return super(AuthenticatedGraphQLView, self).dispatch(request, *args, **kwargs)


private_graphql_view = AuthenticatedGraphQLView.as_view(graphiql=True)
