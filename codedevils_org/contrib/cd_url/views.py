from django.http import HttpResponseNotFound
from django.shortcuts import redirect

from codedevils_org.contrib.cd_url.models import CustomUrl


def get_redirect(request, slug):
    """Redirects to the custom url corresponding to the slug."""
    try:
        link = CustomUrl.objects.get(slug__exact=slug)
        return redirect(link.url, permanent=False)
    except CustomUrl.DoesNotExist:
        return HttpResponseNotFound()
