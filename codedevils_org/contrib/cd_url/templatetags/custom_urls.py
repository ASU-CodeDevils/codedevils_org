from django import template
from django.conf import settings
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


@register.simple_tag
def google_analytics_tracking_id():
    """
    Returns the Google Analytics tracking ID as defined in settings as GOOGLE_ANALYTICS_TRACKING_ID. Note that in
    production this should always return the corresponding tracking ID, but testing locally will return None if
    not set.

    Usage:
        {% load custom_urls %}
        {% google_analytics_tracking_id %}
    """
    return getattr(settings, "GOOGLE_ANALYTICS_TRACKING_ID", None)
