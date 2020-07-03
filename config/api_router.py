from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter, SimpleRouter

from codedevils_org.users.api.views import UserViewSet
from codedevils_org.contrib.cd_url.api.views import CustomUrlViewSet
from config.drf import schema_view

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("links", CustomUrlViewSet)


app_name = "api"
urlpatterns = [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("docs/", login_required(schema_view.with_ui("redoc", cache_timeout=0)), name="schema-redoc")
] + router.urls
