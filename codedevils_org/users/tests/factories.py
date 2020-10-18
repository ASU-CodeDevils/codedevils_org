import random
from typing import Any, Sequence

import factory
from django.contrib.auth import get_user_model

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


class UserFactory(factory.DjangoModelFactory):

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    name = factory.Faker("name")

    @factory.post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else factory.Faker(
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


class OfficerPositionFactory(factory.DjangoModelFactory):

    name = factory.Faker("name")
    order = factory.Faker("pyint")
    sds_position = factory.LazyFunction(_get_position)
    email = factory.Faker("email")

    class Meta:
        model = OfficerPosition
        django_get_or_create = ["name"]


class OfficerFactory(factory.DjangoModelFactory):

    position = factory.SubFactory(factory=OfficerPositionFactory)
    user = factory.SubFactory(factory=UserFactory)
    personal_email = factory.Faker("email")
    quote = factory.Faker("text")

    class Meta:
        model = Officer
        django_get_or_create = ["user", "position"]
