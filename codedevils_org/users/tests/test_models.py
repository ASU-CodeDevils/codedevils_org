import pytest

from codedevils_org.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/en-us/users/{user.username}/"
