import pytest

from django.test import RequestFactory

from codedevils_org.contrib.cd_url.models import CustomUrl
from codedevils_org.contrib.cd_url.views import get_redirect

pytestmark = pytest.mark.django_db


class TestCustomUrlViews:
    """
    Returns that the url is redirected to the appropriate url based on the slug.
    """

    def test_get_links_redirect(self, custom_link: CustomUrl, rf: RequestFactory):
        slug = custom_link.slug
        rf.get(f"/en-us/{slug}/")
        response = get_redirect(rf, slug=slug)
        assert response.status_code == 302
        assert response.url == custom_link.url
