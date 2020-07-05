import pytest
from django.test import Client

from codedevils_org.contrib.cd_url.views import get_redirect
from codedevils_org.contrib.cd_url.models import CustomUrl

pytestmark = pytest.mark.django_db


# class TestCustomUrlViews:
#     """
#     Returns that the url is redirected to the appropriate url based on the slug.
#     """

#     def test_get_links_redirect(self, custom_link: CustomUrl):
#         client = Client()
#         slug = custom_link.slug
#         response = client.get(f"/{slug}/", follow=False)
#         assert response.status_code == 302
