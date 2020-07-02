"""Used to store any custom view actions or context for pages."""
import logging
import requests

from django.contrib import messages
from django.core.validators import validate_email, ValidationError
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _

from codedevils_org.contrib.email.utils import send_contact_us_email, email_is_blacklisted

logger = logging.getLogger("")


def home(request):
    """Provides context to visiting the home page."""
    return render(request, "pages/home.html")


def about(request):
    """Provides context to visiting the about page."""
    return render(request, "pages/about.html", context={"title": _("About")})


def workspace(request):
    """Provides context to visiting the workspace page."""
    return render(request, "pages/workspace.html")


def contact_us(request):
    """View function for the Contact Us page."""
    context = {"title": _("Contact Us")}

    # POST request
    if request.method == "POST":
        csrf_token = request.POST.get("csrfmiddlewaretoken")
        # no csrf token means the POST request was performed from outside the browser, which
        # is normally a means of spam or DOS attacks
        if not csrf_token:
            return HttpResponseForbidden("Not permitted to perform this action")

        contact_email = request.POST.get("Contact[email]")
        contact_subject = request.POST.get("Contact[subject]")
        contact_message = request.POST.get("Contact[message]")

        # check that the fields are filled in
        email_error = _("Please enter your email") if not contact_email else None
        subject_error = _("Please enter a subject") if not contact_subject else None
        message_error = _("Please enter a message") if not contact_message else None

        # check that the email is valid
        if not email_error:
            try:
                validate_email(contact_email)
            except ValidationError:
                email_error = _("Your email is invalid")

        # check that the email is not blacklisted
        if email_is_blacklisted(contact_email):
            email_error = _("There was an issue with this email address")

        if email_error or subject_error or message_error:
            context.update({
                "email_error": email_error,
                "subject_error": subject_error,
                "message_error": message_error,
                "email": contact_email,
                "subject": contact_subject,
                "message": contact_message
            })
            return render(request, "pages/contactus.html", context=context)

        # no error, send email
        send_contact_us_email(subject=contact_subject, reply_to=contact_email, body=contact_message)

        # log the contact
        logger.info(f"Contact message sent from {contact_email} to contact email")
        messages.info(request, message=_("Your message has been received and we will email you back soon."))
        return redirect("home")

    # default behavior is to return to the Contact Us page
    return render(request, "pages/contactus.html", context=context)


def test_email(request):
    context = {
        "title": "Title",
        "preheader": "This is a subtitle",
        "body": [
            "This is the first paragraph",
            "This is the next",
        ],
        "call_to_action": {
            "link": "https://codedevils.org",
            "text": "Visit the website",
        },
        "post_call_to_action": [
            "This is another paragraph",
            "I feel this paragraph",
        ]
    }

    return render(request, "email/base.html", context=context)
