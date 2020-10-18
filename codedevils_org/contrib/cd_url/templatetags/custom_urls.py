from django import template

from ..models import CustomUrl

register = template.Library()


@register.simple_tag
def custom_url(slug):
    """
    Returns a custom url based on the slug passed to the template tag. If
    the slug is not found, then a dead link is returned.

    Usage::

        {% load custom_urls %}
        {% custom_url 'slack' %}
    """

    try:
        return CustomUrl.objects.get(slug=slug).url
    except CustomUrl.DoesNotExist:
        return "#"
