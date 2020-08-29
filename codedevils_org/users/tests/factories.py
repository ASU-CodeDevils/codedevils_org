import random

from typing import Any, Sequence

import factory
from django.contrib.auth import get_user_model
from factory import (
    DjangoModelFactory,
    Faker,
    post_generation,
    SubFactory,
)

from codedevils_org.users.models import Officer, OfficerPosition


def _get_position():
    choices = [
        "President",
        "Vice President",
        "Secretary",
        "Webmaster",
        "Events Coordinator",
    ]
    return random.choice(choices)


class UserFactory(DjangoModelFactory):

    username = Faker("user_name")
    email = Faker("email")
    name = Faker("name")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).generate(extra_kwargs={})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]


class OfficerPositionFactory(DjangoModelFactory):

    name = Faker("name")
    order = Faker("pyint")
    sds_position = factory.LazyFunction(_get_position)
    email = Faker("email")

    class Meta:
        model = OfficerPosition
        django_get_or_create = ["name"]


class OfficerFactory(DjangoModelFactory):

    position = SubFactory(factory=OfficerPositionFactory)
    user = SubFactory(factory=UserFactory)
    personal_email = Faker("email")
    quote = Faker("text")

    class Meta:
        model = Officer
        django_get_or_create = ["user", "position"]
