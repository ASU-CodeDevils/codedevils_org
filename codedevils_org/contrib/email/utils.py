import logging
from typing import List, Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from config import celery_app
from codedevils_org.contrib.email.models import BlacklistDomain, BlacklistEmail

Attachments: List[str] = None
EmailList = Union[list, str]
EmailBody = Union[list, str]
User = get_user_model()
logger = logging.getLogger("")


@celery_app.task()
def send_email(subject: str,
               text_content: str = None,
               from_email: str = settings.EMAIL_HOST_USER,
               to: EmailList = None,
               reply_to: EmailList = None,
               html_content: str = None,
               attachments: Attachments = None) -> None:
    """
    Wrapper for the built-in django send_mail util.

        :param subject: The email subject.
        :param text_content: The plain-text email message.
        :param from_email: The from email address, default is the `EMAIL_HOST_USER`.
        :param to: The list of email recipients. If a string, it sends an email to only that email.
            If None, it will send a mass email to all users who opt to receive notifications.
        :param reply_to: The email to reply to, default is None.
        :param html_content: The html message.
        :param attachments: A list of attachments by name. These can be referential or complete URLs.
    """

    # set the list of recipients if not already set
    if not to:
        to = list(User.objects.filter(is_active=True, receieve_notifications=True).values_list("email", flat=True))
    elif isinstance(to, str):
        to = [to]

    # set the reply to
    if reply_to and isinstance(reply_to, str):
        reply_to = [reply_to]

    email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=to, reply_to=reply_to)

    # attach html content
    if html_content:
        email.attach_alternative(html_content, "text/html")
        email.content_subtype = "html"

    # attach files
    if attachments:
        for attachment in attachments:
            email.attach_file(attachment)

    email.send()


def send_templated_email(subject: str,
                         template: str,
                         template_context: dict = None,
                         from_email: str = settings.EMAIL_HOST_USER,
                         to: EmailList = None,
                         reply_to: EmailList = None,
                         attachments: Attachments = None):
    """
    Sends a templated email message.

        :param subject: The email subject.
        :param template: The email template to generate the email from.
        :param template_context: Parameters of the email template.
        :param from_email: The from email address, default is the `EMAIL_HOST_USER`.
    """
    try:
        html_content = render_to_string(f"email/{template}.html", template_context)
        text_content = strip_tags(html_content)
    except FileNotFoundError as fnfe:
        logger.error("Email template not found: %s", fnfe)
        raise

    send_email.delay(subject=subject, from_email=from_email, to=to, reply_to=reply_to,
                     text_content=text_content, html_content=html_content, attachments=attachments)


def send_contact_us_email(subject: str, reply_to: str, body: str):
    """
    Sends the email from the Contact Us page to the designated officer.

        :param subject: The email subject.
        :param reply_to: The person's email who filled in the contact form.
        :param body: The email body to place in the template.
    """
    body = ["Someone has contacted CodeDevils from the website:", body]
    context = {"title": subject, "body": body}
    send_templated_email(subject=subject, to=settings.EMAIL_INFO, reply_to=reply_to,
                         template="contact_us", template_context=context)


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
