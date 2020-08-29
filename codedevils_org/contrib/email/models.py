import logging

from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger("")


class BlacklistAbstract(models.Model):
    """Provides an abstract base model for blacklisted models."""

    is_blocked = models.BooleanField(
        db_column="Blocked",
        null=False,
        default=True,
        verbose_name=_("Is blocked"),
        help_text=_("Blocks this email from contacting CodeDevils."),
    )
    blocked_until = models.DateTimeField(
        db_column="BlockedUntil",
        blank=True,
        null=True,
        verbose_name=_("Blocked until"),
        help_text=_(
            "The date and time the email is blocked until. If not specified, "
            "this email is blocked indefinitely."
        ),
    )

    class Meta:
        abstract = True


class BlacklistDomain(BlacklistAbstract):
    """All blacklisted email domains."""

    domain = models.CharField(
        db_column="Domain",
        blank=False,
        null=False,
        max_length=253,
        verbose_name=_("Domain"),
        help_text=_(
            "The domain of email addresses to blacklist. This does not include "
            "subdomains as this would inadvertantly block valid domains (see "
            "documentation for more)."
        ),
    )

    class Meta:
        managed = True
        db_table = "blacklist_domain"
        ordering = ["domain"]
        verbose_name = _("Blacklisted Domain")
        verbose_name_plural = _("Blacklisted Domains")

    def __str__(self):
        return self.domain

    def save(self, *args, **kwargs):
        """Overrides the save method to check the blocked until date."""
        if self.blocked_until >= datetime.now():
            self.is_blocked = False
            logger.error(f"A domain has been unblocked: {self.domain}")
        super().save(*args, **kwargs)


class BlacklistEmail(BlacklistAbstract):
    """Blacklist of emails to be blocked from the Contact Us page."""

    email = models.EmailField(
        db_column="Email", blank=False, null=False, unique=True, verbose_name=_("Email")
    )

    class Meta:
        managed = True
        db_table = "blacklist_email"
        ordering = ["email"]
        verbose_name = _("Blacklisted Email")
        verbose_name_plural = _("Blacklisted Emails")

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """Overrides the save method to check the blocked until date."""
        if self.blocked_until >= datetime.now():
            self.is_blocked = False
            logger.error(f"An email has been unblocked: {self.email}")
        super().save(*args, **kwargs)
