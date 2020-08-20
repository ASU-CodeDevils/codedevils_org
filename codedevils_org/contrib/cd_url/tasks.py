from datetime import timedelta

from django.core.mail import mail_managers
from django.utils import timezone

from codedevils_org.contrib.cd_url.models import CustomUrl
from config import celery_app


@celery_app.task()
def notify_of_expired_links():
    """
    Notifies managers of any links that have not been updated in the specified time frame.
    This task when run on an hourly interval will repeatedly remind managers to update the
    link at the interval specified (i.e. every 1 hour, 6 months, etc).
    """
    links_to_check = []
    urls = CustomUrl.objects.all()
    for url in urls:
        last_updated = url.last_updated
        hours = url.get_interval_in_hours()
        today = timezone.now()

        if last_updated + timedelta(hours=hours) <= today:
            url.acknowledged = False
            url.save()
            links_to_check.append(f"{url.name} <{url.url}>")

    if links_to_check:
        url_list = ", ".join(links_to_check)
        mail_managers(
            subject="Notification of Expired Links",
            message="The following links may require updating. To update, visit "
            "https://www.qa.codedevils.org/en-us/admin/cd_url/customurl/ "
            " and update the list: " + url_list,
        )
