import pytest
from django.urls import resolve, reverse

from codedevils_org.users.models import User

pytestmark = pytest.mark.django_db


def test_detail(user: User):
    assert (
        reverse("users:detail", kwargs={"username": user.username})
        == f"/en-us/users/{user.username}/"
    )
    assert resolve(f"/en-us/users/{user.username}/").view_name == "users:detail"


def test_update():
    assert reverse("users:update") == "/en-us/users/~update/"
    assert resolve("/en-us/users/~update/").view_name == "users:update"


def test_redirect():
    assert reverse("users:redirect") == "/en-us/users/~redirect/"
    assert resolve("/en-us/users/~redirect/").view_name == "users:redirect"


def test_unsubscribe(user: User):
    user.receive_notifications = True
    user.save()

    assert reverse("users:unsubscribe") == "/en-us/users/~unsubscribe/"
    # TODO this needs to resolve to the end user
    # assert resolve("/en-us/users/~unsubscribe/").view_name == "users:unsubscribe"
    # assert not user.receive_notifications
