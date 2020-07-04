from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import authentication, permissions
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.views import APIView

from codedevils_org.users.api.views import UserViewSet, OfficerViewSet, OfficerPositionViewSet
from codedevils_org.contrib.cd_url.api.views import CustomUrlViewSet
from codedevils_org.contrib.email.api.views import BlacklistDomainViewSet, BlacklistEmailViewSet
from config.drf import schema_view
from config.graphene.graphene import private_graphql_view

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("officers", OfficerViewSet)
router.register("positions", OfficerPositionViewSet)
router.register("links", CustomUrlViewSet)
router.register("blacklist_domains", BlacklistDomainViewSet)
router.register("blacklist_emails", BlacklistEmailViewSet)

# test API view
class TestView(APIView):
    """Test API endpoint view."""
    authentication_classes = [authentication.TokenAuthentication]
    permissions_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({"message": "test"}, content_type="application/json")


app_name = "api"
urlpatterns = [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("docs/", login_required(schema_view.with_ui("redoc", cache_timeout=0)), name="schema-redoc"),
    # GraphQL
    path("graphql/", csrf_exempt(private_graphql_view)),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    # test endpoint
    path("test/", TestView.as_view(), name="test")
] + router.urls
