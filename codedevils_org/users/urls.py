from django.urls import path

from codedevils_org.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    user_unsubscribe_redirect_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
    path("~unsubscribe/", view=user_unsubscribe_redirect_view, name="unsubscribe"),
]
