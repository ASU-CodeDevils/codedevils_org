import pytest
from django.test import RequestFactory

from codedevils_org.users.api.views import UserViewSet
from codedevils_org.users.models import User

pytestmark = pytest.mark.django_db


class TestUserViewSet:
    def test_get_queryset(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        assert user in view.get_queryset()

    def test_me(self, user: User, rf: RequestFactory):
        view = UserViewSet()
        request = rf.get("/fake-url/")
        request.user = user

        view.request = request

        response = view.me(request)

        assert response.data == {
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "url": f"http://testserver/api/users/{user.username}/",
            "anonymous": user.anonymous,
            "bio": user.bio,
            "date_joined": user.date_joined,
            "dob": user.dob,
            "facebook_url": user.facebook_url,
            "first_name": user.first_name,
            "github_username": user.github_username,
            "id": user.id,
            "instagram_url": user.instagram_url,
            "is_active": user.is_active,
            "last_login": user.last_login,
            "last_name": user.last_name,
            "linkedin_url": user.linkedin_url,
            "receive_notifications": user.receive_notifications,
            "slack_username": user.slack_username,
            "twitter_username": user.twitter_username
        }
