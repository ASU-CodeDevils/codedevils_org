import logging
from typing import List, Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import BadHeaderError, send_mail
from django.template.loader import render_to_string

from codedevils_org.contrib.email.models import BlacklistDomain, BlacklistEmail
from config import celery_app

Attachments: List[str] = None
EmailList = Union[list, str]
EmailBody = Union[list, str]
User = get_user_model()
logger = logging.getLogger("")


@celery_app.task()
def send_email(
        subject: str,
        text_content: str = None,
        from_email: str = settings.DEFAULT_FROM_EMAIL,
        to: EmailList = None,
        reply_to: EmailList = None,
        html_content: str = None,
) -> None:
    """
    Wrapper for the built-in django send_mail util.

        :param subject: The email subject.
        :param text_content: The plain-text email message.
        :param from_email: The from email address, default is the `EMAIL_HOST_USER`.
        :param to: The list of email recipients. If a string, it sends an email to only that email.
            If None, it will send a mass email to all users who opt to receive notifications.
        :param reply_to: The email to reply to, default is None.
        :param html_content: The html message.
    """

    # set the list of recipients if not already set
    if not to:
        to = list(
            User.objects.filter(
                is_active=True, receieve_notifications=True
            ).values_list("email", flat=True)
        )
    elif isinstance(to, str):
        to = [to]

    # set the reply to
    if reply_to and isinstance(reply_to, str):
        reply_to = [reply_to]

    try:
        send_mail(
            subject=subject,
            message=text_content,
            html_message=html_content,
            recipient_list=to,
            from_email=from_email
        )
    except BadHeaderError as bhe:
        logger.error(f"Header injection attempt: {bhe}")
        raise


def send_templated_email(
        subject: str,
        template: str,
        template_context: dict = None,
        from_email: str = settings.EMAIL_HOST_USER,
        to: EmailList = None,
):
    """
    Sends a templated email message.

        :param subject: The email subject.
        :param template: The email template to generate the email from.
        :param template_context: Parameters of the email template.
        :param from_email: The from email address, default is the `EMAIL_HOST_USER`.
    """
    try:
        text_content = render_to_string(f"email/text/{template}.txt", template_context)
        html_content = render_to_string(f"email/html/{template}.html", template_context)
    except FileNotFoundError as fnfe:
        logger.error("Email template not found: %s", fnfe)
        raise

    send_email.delay(
        subject=subject,
        from_email=from_email,
        to=to,
        text_content=text_content,
        html_content=html_content,
    )


def send_contact_us_email(subject: str, body: str, reply_to: str):
    """
    Sends the email from the Contact Us page to the designated officer.

    Args:
        subject (str): The email subject.
        body (str): The email body to place in the template.
        reply_to (str): The email of the person contacting support.
    """
    body = ["Someone has contacted CodeDevils from the website:", body]
    context = {"title": subject, "body": body}
    send_templated_email(
        subject=subject,
        to=settings.EMAIL_INFO,
        from_email=reply_to,
        template="contact_us",
        template_context=context,
    )


def email_is_blacklisted(email: str):
    """Returns True if the email is blacklisted, False if not."""
    # first check the email
    if BlacklistEmail.objects.filter(email__exact=email).exists():
        return True

    # then check the domain
    domain = email.split("@")[1]
    if BlacklistDomain.objects.filter(domain__exact=domain).exists():
        return True

    return False
