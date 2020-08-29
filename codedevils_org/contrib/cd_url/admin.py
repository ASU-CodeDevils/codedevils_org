from django.contrib import admin
from codedevils_org.contrib.cd_url.models import CustomUrl


@admin.register(CustomUrl)
class CustomUrlAdmin(admin.ModelAdmin):
    """ModelAdmin for custom urls."""

    list_display = ("name", "url", "last_updated", "acknowledged")
    list_filter = ("name", "acknowledged")
