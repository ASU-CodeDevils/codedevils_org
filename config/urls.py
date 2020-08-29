from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django_cas_ng import views as cas_views

from codedevils_org import page_views

# locale
urlpatterns = i18n_patterns(
    path("", page_views.home, name="home"),
    path("about/", page_views.about, name="about"),
    path("contactus/", page_views.contact_us, name="contactus"),
    path("workspace/", page_views.workspace, name="workspace"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # cas log in
    path("login/", cas_views.LoginView.as_view(), name="cas_ng_login"),
    path("logout/", cas_views.LogoutView.as_view(), name="cas_ng_logout"),
    # User management
    path("users/", include("codedevils_org.users.urls", namespace="users")),
    # rosetta translation page
    path("rosetta/", include("rosetta.urls")),
    # custom urls
    path("", include("codedevils_org.contrib.cd_url.urls", namespace="cd_url")),
)

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.

    urlpatterns += [
        # custom error pages for debugging in development
        # these will be replaced by the server's error pages
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
