import random
import factory
from factory import DjangoModelFactory, Faker

from codedevils_org.contrib.cd_url.models import CustomUrl


def _get_interval_choice():
    """Returns a random interval choice."""
    interval = [f[0] for f in CustomUrl.INTERVALS]
    return random.choice(interval)


class CustomUrlFactory(DjangoModelFactory):

    slug = Faker("slug")
    name = Faker("name")
    url = Faker("url")
    last_updated = Faker("date")
    notify_in = Faker("pyint")
    notify_interval = factory.LazyFunction(_get_interval_choice)

    class Meta:
        model = CustomUrl
        django_get_or_create = ["slug"]
