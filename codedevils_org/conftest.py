import pytest

from codedevils_org.contrib.cd_url.models import CustomUrl
from codedevils_org.contrib.cd_url.test.factories import CustomUrlFactory
from codedevils_org.users.models import Officer, OfficerPosition, User
from codedevils_org.users.tests.factories import (
    OfficerFactory,
    OfficerPositionFactory,
    UserFactory,
)


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def position() -> OfficerPosition:
    return OfficerPositionFactory()


@pytest.fixture
def officer() -> Officer:
    return OfficerFactory()


@pytest.fixture
def custom_link() -> CustomUrl:
    return CustomUrlFactory()
