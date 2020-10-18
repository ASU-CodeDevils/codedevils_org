from django.contrib import admin

from codedevils_org.contrib.email.models import BlacklistDomain, BlacklistEmail


@admin.register(BlacklistEmail)
class BlacklistEmailAdmin(admin.ModelAdmin):
    """ModelAdmin for blacklisted emails."""

    list_display = ("email", "is_blocked", "blocked_until")
    list_filter = ("email", "blocked_until")


@admin.register(BlacklistDomain)
class BlacklistDomainAdmin(admin.ModelAdmin):
    """ModelAdmin for blacklisted emails."""

    list_display = ("domain", "is_blocked", "blocked_until")
    list_filter = ("domain", "blocked_until")
