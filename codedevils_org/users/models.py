import logging

from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group

from django_countries.fields import CountryField
from localflavor.us.models import USStateField

log = logging.getLogger("root")


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    image_24 = models.URLField(
        db_column="Image24",
        verbose_name=_("Image 24"),
        blank=True,
        null=True,
        help_text=_("User 24px profile image"),
    )
    image_512 = models.URLField(
        db_column="Image512",
        verbose_name=_("Image 512"),
        blank=True,
        null=True,
        help_text=_("User 512px profile image"),
    )

    # student information
    bio = models.TextField(
        db_column="Bio", blank=True, null=True, verbose_name=_("About")
    )
    dob = models.DateField(
        db_column="DateOfBirth", blank=True, null=True, verbose_name=_("Date of birth")
    )

    # locale
    city = models.CharField(
        db_column="City",
        blank=True,
        null=True,
        max_length=30,
        verbose_name=_("City"),
        help_text=_("The city that the user currently resides in"),
    )
    state = USStateField(
        db_column="State",
        blank=True,
        null=True,
        default="NA",
        verbose_name=_("State"),
        help_text=_("The state the city resides in (for inside the US only)"),
    )
    country = CountryField(
        db_column="Country",
        blank=True,
        null=True,
        default="--",
        verbose_name=_("Country"),
        help_text=_("The country the city resides in"),
    )

    # user names/social media links
    github_username = models.CharField(
        db_column="GithubUsername",
        blank=True,
        null=True,
        max_length=30,
        verbose_name=_("GitHub Username"),
        help_text=_("We use this to automatically enroll you in our GitHub projects."),
    )
    slack_id = models.CharField(
        db_column="SlackId",
        max_length=12,
        blank=True,
        null=True,
        help_text=_("ID assigned to this user on Slack")
    )
    twitter_username = models.CharField(
        db_column="TwitterUsername",
        blank=True,
        null=True,
        max_length=15,
        verbose_name=_("Twitter Username"),
        help_text="Just the username. This username will be appended to the Twitter"
        " URL.",
    )
    instagram_url = models.URLField(
        db_column="InstagramUrl", blank=True, null=True, verbose_name=_("Instagram URL")
    )
    facebook_url = models.URLField(
        db_column="FacebookUrl", blank=True, null=True, verbose_name=_("Facebook URL")
    )
    linkedin_url = models.URLField(
        db_column="LinkedInUrl", blank=True, null=True, verbose_name=_("LinkedIn URL")
    )

    # user preferences
    receive_notifications = models.BooleanField(
        db_column="ReceiveNotifications",
        default=False,
        verbose_name=_("Receive notifications"),
        help_text="Receive emails about the latest and greatest at CodeDevils!",
    )
    anonymous = models.BooleanField(
        db_column="IsAnonymous",
        default=True,
        blank=False,
        null=False,
        verbose_name=_("Anonymous"),
        help_text=_(
            "You have the option of keeping your account anonymous with CD. "
            "Selectingthis will ensure your account stays private and supported "
            "applications don't have access to your data"
        ),
    )

    def image(self):
        """Returns the 512px image by default."""
        return self.image_512

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        if self.name:
            return f"{self.name} ({self.username})"
        return f"{self.username}"


class OfficerPosition(models.Model):
    """
    Officer positions and their relative emails.
    """

    name = models.CharField(
        db_column="Name",
        max_length=40,
        help_text=_("Name of the position"),
        unique=True,
        verbose_name=_("Name"),
    )
    order = models.PositiveSmallIntegerField(
        db_column="Order",
        null=False,
        verbose_name=_("Order"),
        help_text=_(
            "The order of precedence of the position. For example, the "
            "President is 1, Vice President is 2, and so on."
        ),
    )
    sds_position = models.CharField(
        db_column="SDSPosition",
        blank=True,
        null=True,
        max_length=32,
        verbose_name=_("SunDevilSync Position"),
        help_text=_(
            "The name of the officer position as it is registered on SunDevilSync"
        ),
    )
    email = models.EmailField(
        db_column="OfficerEmail",
        blank=True,
        null=True,
        verbose_name=_("Email"),
        help_text=_("The email address associated to the Officer position"),
    )

    class Meta:
        ordering = ["order"]
        verbose_name = _("Officer position")
        verbose_name_plural = _("Officer positions")

    def __str__(self):
        if not self.email:
            return f"{self.name}"
        return f"{self.name} <{self.email}>"

    def _do_insert_in_order(self):
        """
        Maintains the ordering of positions by inserting/adding this position into the existing list
        of positions by order. It does so by inserting this position into a certain order, and
        incrementing subsequent positions.
        """
        log.debug(f"Runnig _do_insert_in_order for {self.name} (order {self.order})")
        positions = OfficerPosition.objects.filter(order__gte=self.order)

        # if no position exists at the order, no reordering is required
        if not positions or not positions.filter(order__exact=self.order):
            log.debug(f"No position found at {self.order}. No reordering required!")
            return

        positions = positions.order_by("order")
        name = self.name
        order_max_to_check = self.order + len(positions)

        log.debug(
            f"Analyzing {len(positions)} positions: {list(positions.values_list('name', 'order'))}"
        )
        for order in range(self.order, order_max_to_check):

            # performs a check for the next order in the list of positions. The filter works by:
            # | Excluding the name of the position we already changed the order of
            # | Excluding the original name of the position that triggered this workflow
            # | Getting the remaining order number
            # If there is a position at that order, the position's order is incremented and the
            # loop continues
            try:
                current_position = (
                    positions.exclude(name__exact=name)
                    .exclude(name__exact=self.name)
                    .get(order__exact=order)
                )
                current_position.order = order + 1
                current_position.save(stop_reorder=True)
                name = current_position.name
            # if the order does not exist at that position, and exception is thrown and the loop
            # is broken to ensure subsequent positions are not incremented if there is a gap between
            # this position and the next
            except OfficerPosition.DoesNotExist:
                break

    def save(self, stop_reorder: bool = False, *args, **kwargs):
        """
        Overrides the save method to add an ordering check. Reordering is done dynamically when the user selects
        a new order for this position. If the order number already exists, this position replaces that order and
        subsequent orders are incremented by 1 to keep ordering unique.

            :param stop_reorder: Stops the reordering of a position. This is used for stopping the saving of
                subsequent models when updating the order of one position.
        """
        # the self.pk check will return null if the model is not saved to the database yet, which makes the
        # insert run when the model is being created
        if not stop_reorder or not self.pk:
            self._do_insert_in_order()

        super().save(*args, **kwargs)


class Officer(models.Model):
    """
    An Officer is a club executive member that has a set of responsibilities. Each
    officer is assigned a position and an email, which is used by the system"s
    ticketing and communication to disconnect the requirement for an officer to
    use their personal email to conduct CodeDevils" business.
    """

    position = models.ForeignKey(
        OfficerPosition,
        db_column="Position",
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Position"),
    )
    user = models.ForeignKey(
        User,
        db_column="UserID",
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        help_text=_("The holder the position"),
    )
    personal_email = models.EmailField(
        db_column="PersonalEmail",
        blank=True,
        null=True,
        verbose_name=_("Personal email"),
        help_text=_(
            "The email address belonging to the student (generally <first name>."
            "<last name>@codedevils.org)"
        ),
    )
    quote = models.TextField(
        db_column="Quote",
        blank=True,
        null=True,
        verbose_name=_("Quote"),
        help_text=_("A cliche quote that truly defines who this being is"),
    )

    class Meta:
        managed = True
        db_table = "officer"
        ordering = ["position"]
        verbose_name = _("Officer")
        verbose_name_plural = _("Officers")

    def __init__(self, *args, **kwargs):
        """
        Overwritten method to add a field to track the original user for when an officer changes users. The
        original user needs to be tracked so changes between each transaction can be tracked. If the position"s
        user changes, then the correct privileges are administered to both the old and new position holder.
        """
        super().__init__(*args, **kwargs)
        self.__original_user = (
            None  # used to track transition between position from one user to another
        )

    def __str__(self):
        """
        Displays the officer with their first and last name. If the name is not available, then the position
        is displayed.
        """
        if not self.user.first_name:
            return f"{self.position.name}"
        return f"{self.position.name} - {self.user.first_name} {self.user.last_name}"

    def remove_original_user_priv(self):
        """
        Removes admin and officer privileges from the original user holding this position.
        """
        officer_group = Group.objects.filter(name__exact="Officer").first()
        user_officer = self.user.groups.all().filter(name__exact="Officer")
        if not user_officer:
            self.__original_user.groups.remove(officer_group)
            self.__original_user.is_staff = False
            self.__original_user.save()

    def _add_user_to_officers(self):
        """
        Gives the new user in this position officer privileges, which includes both making them admin on
        the website and adding them to the Officer group.
        """
        officer_group = Group.objects.filter(name__exact="Officer").first()
        user_officer = self.user.groups.all().filter(name__exact="Officer")
        if not user_officer:
            self.user.groups.add(officer_group)
            self.user.is_staff = True
            self.user.save()

    def save(self, *args, **kwargs):
        """
        Overrides model save method to be able to modify the status of the user being assigned the position.
        The new officer is added to the "Officer" group, while the old user is removed and is revoked staff
        status.
        """
        if not self.pk:
            self.__original_user = self.user
            log.debug(f"Officer added user {self.user.username}")
            self._add_user_to_officers()

        if self.__original_user and self.user != self.__original_user:
            log.debug(
                f"Removing officer {self.__original_user.username} privileges, adding {self.user.username}"
            )
            self.remove_original_user_priv()
            self.__original_user = self.user
            self._add_user_to_officers()

        super().save(*args, **kwargs)
