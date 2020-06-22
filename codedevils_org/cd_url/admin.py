from django.contrib import admin


class CustomUrlAdmin(admin.ModelAdmin):
    """ModelAdmin for custom urls."""
    list_display = ('name', 'url')
    list_filter = ('name',)