from django.urls import path

from codedevils_org.contrib.cd_url.views import get_redirect

app_name = "cd_url"
urlpatterns = [path("<str:slug>/", view=get_redirect, name="shortcut")]
