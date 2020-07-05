import logging
import pytest

from codedevils_org.users.models import User, Officer, OfficerPosition
from .factories import OfficerPositionFactory

pytestmark = pytest.mark.django_db
logger = logging.getLogger("factory")


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/en-us/users/{user.username}/"


def test_user_str(user: User):
    assert str(user) == f"{user.name} ({user.username})"
    user.name = None
    assert str(user) == user.username


def test_officer_position_str(position: OfficerPosition):
    assert str(position) == f"{position.name} <{position.email}>"
    position.email = None
    assert str(position) == position.name


def test_officer_str(officer: Officer):
    assert str(officer) == f"{officer.position.name}"
    officer.user.first_name = "Sandy"
    officer.user.last_name = "Cheeks"
    assert str(officer) == f"{officer.position.name} - {officer.user.first_name} {officer.user.last_name}"


def test_officer_position_list_ordering():
    # create 5 officer positions
    positions = []
    for i in range(5):
        positions.append(OfficerPositionFactory(order=i+1))

    assert len(positions) == 5

    # position in the index (i) is the same as the order + 1
    assert positions[0].order == 1
    assert positions[2].order == 3

    # test the saving of the order to ensure the orders are incremented appropriately
    positions[2].order = 1
    positions[2].save()
    assert positions[2].order == 1
    # assert positions[0].order == 2
