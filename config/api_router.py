from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework.routers import DefaultRouter, SimpleRouter

from codedevils_org.users.api.views import UserViewSet
from codedevils_org.contrib.cd_url.api.views import CustomUrlViewSet
from codedevils_org.contrib.email.api.views import BlacklistDomainViewSet, BlacklistEmailViewSet
from config.drf import schema_view

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("links", CustomUrlViewSet)
router.register("blacklist_domains", BlacklistDomainViewSet)
router.register("blacklist_emails", BlacklistEmailViewSet)


app_name = "api"
urlpatterns = [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("docs/", login_required(schema_view.with_ui("redoc", cache_timeout=0)), name="schema-redoc"),
    # GraphQL
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
] + router.urls
