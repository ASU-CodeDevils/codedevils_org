from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class CustomUrl(models.Model):
    """
    Defines a model to store customer urls. The urls are access via their slug using a custom
    template tag.
    """
    INTERVALS = (
        ("HOURS", "HOURS"),
        ("DAYS", "DAYS"),
        ("MONTHS", "MONTHS")
    )

    name = models.CharField(db_column="Name", blank=False, null=False, max_length=50)
    url = models.URLField(db_column="Url", blank=False, null=False)
    slug = models.SlugField(db_column="Slug", blank=False, null=False, unique=True, max_length=20,
                            help_text=_("The string used to reference the URL from within a Django template. "
                                        "The slug can only contain letters, numbers, underscores and hyphens."))
    last_updated = models.DateTimeField(db_column="LastUpdated", auto_now=True,
                                        verbose_name=_("Last Updated"),
                                        help_text=_("Used to send notifications to administrators when the link "
                                                    "needs to be updated"))
    notify_in = models.PositiveSmallIntegerField(db_column="NotifyIn", blank=True, null=True, default=12,
                                                 verbose_name=_("Notify in"),
                                                 help_text=_("The number of hours, days or months until managers are "
                                                             "notified to update the link."))
    notify_interval = models.CharField(db_column="NotifyInterval", blank=True, null=True, choices=INTERVALS,
                                       max_length=6, default="MONTHS", verbose_name=_("Notify interval"),
                                       help_text=_("The interval (hours, days months) of ``notify_in``. Note that "
                                                   "months are assumed to be 30 days."))
    acknowledged = models.BooleanField(db_column="Acknowledged", null=False, default=True,
                                       verbose_name=_("Acknowledged"),
                                       help_text=_("Used to flag if this link has been acknowledged as up-to-date. "
                                                   "If not, managers are notified that the links need to be updated."))

    def get_interval_in_hours(self):
        """Utility method to take the """
        if self.notify_interval != "HOURS":
            hours = self.notify_in * 24 if self.notify_interval == "DAYS" else self.notify_in * 720
            return hours
        return self.notify_in
    
    def get_absolute_url(self):
        return reverse("cd_url:shortcut", kwargs={"slug": self.slug})

    class Meta:
        managed = True
        db_table = "custom_url"
        ordering = ["name"]
        verbose_name = _("Custom URL")
        verbose_name_plural = _("Custom URLs")

    def __str__(self):
        return self.name
