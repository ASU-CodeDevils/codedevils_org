from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Open API schema for redoc
schema_view = get_schema_view(
    openapi.Info(
        title=settings.DRF_YASG_TITLE,
        default_version=settings.DRF_YASG_DEFAULT_VERSION,
        description=settings.DRF_YASG_DESCRIPTION,
        terms_of_service=settings.DRF_YASG_TERMS_OF_SERVICE,
        contact=openapi.Contact(email=settings.DRF_YASG_CONTACT_EMAIL),
        license=openapi.License(name=settings.DRF_YASG_LICENSE),
        x_logo={"url": settings.DRF_YASG_LOGO, "backgroundColor": None},
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
