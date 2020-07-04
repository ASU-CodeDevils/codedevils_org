from datetime import datetime

from codedevils_org.contrib.email.models import BlacklistDomain, BlacklistEmail
from config import celery_app


@celery_app.task()
def unblock_expired_blacklistings():
    """
    Some timestamps are set on blacklisted until their time stamp is hit.
    This task is for unblocking those at their given date within whatever
    time interval you choose to perform the task.
    """
    blacklisted_emails = BlacklistEmail.objects.filter(is_blocked=True,
                                                       blocked_until__isnull=False,
                                                       blocked_until__gte=datetime.now())
    blacklisted_domains = BlacklistDomain.objects.filter(is_blocked=True,
                                                         blocked_until__isnull=False,
                                                         blocked_until__gte=datetime.now())
    if blacklisted_emails:
        blacklisted_emails.update(is_blocked=False)
    if blacklisted_domains:
        blacklisted_domains.update(is_blocked=False)
