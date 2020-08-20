from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth import admin as auth_admin
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from codedevils_org.users.models import Officer, OfficerPosition
from codedevils_org.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        ("User", {"fields": ("name",)}),
        (
            "About",
            {"fields": ("city", "state", "country", "bio"), "classes": ("collapse",)},
        ),
        (
            "Links",
            {
                "fields": (
                    "image_24",
                    "image_512",
                    "github_username",
                    "slack_username",
                    "twitter_username",
                    "instagram_url",
                    "facebook_url",
                    "linkedin_url",
                )
            },
        ),
        ("Preferences", {"fields": ("anonymous", "receive_notifications")}),
    ) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


@admin.register(OfficerPosition)
class OfficerPositionAdmin(admin.ModelAdmin):
    empty_value_display = "-----"
    list_display = ["name", "sds_position", "order"]
    actions = ["rebase_order"]

    def changelist_view(self, request, extra_context=None):
        """
        Overwrites the changelist view to allow custom actions to be deleted when no items in the
        list are selected.
        """
        if "action" in request.POST and request.POST["action"] in self.actions:
            if not request.POST.getlist(admin.ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                post.update({admin.ACTION_CHECKBOX_NAME: 0})
                request._set_post(post)
        return super(OfficerPositionAdmin, self).changelist_view(request, extra_context)

    def rebase_order(self, request, queryset):
        """
        Rebase the list starting at the highest order, rebasing that value at 1 and subsequent values
        as increments of 1.
        """
        positions = OfficerPosition.objects.all()
        if not positions:
            self.message_user(
                request=request,
                message=_("There are no positions to rebase"),
                level=messages.WARNING,
            )
        else:
            order = 1
            for position in positions.order_by("order"):
                position.order = order
                position.save(stop_reorder=True)
                order = order + 1
            self.message_user(
                request=request,
                message=_("Position orders successfully rebased"),
                level=messages.SUCCESS,
            )

    rebase_order.short_description = _("Rebase order starting at 1")


@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    empty_value_display = "-----"
    list_display = ["user", "position"]

    def get_position(self, officer):
        return officer.position.name

    get_position.short_description = _("Position")
    get_position.admin_order_field = "position__name"

    def delete_queryset(self, request, queryset):
        """
        Override the delete_queryset method to invoke the delete() method of the Officer model.
        Without overriding, the individual methods would not be called, but instead a buld delete.
        See https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.delete_queryset
        for more information.
        """
        if not self.has_delete_permission(request):
            raise PermissionDenied

        for officer in queryset:
            officer.remove_original_user_priv()
            officer.delete(using=None, keep_parents=False)
        return super().delete_queryset(request, queryset)
