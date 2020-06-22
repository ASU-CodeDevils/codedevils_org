from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUrl(models.Model):
    """
    Defines a model to store customer urls. The urls are access via their slug using a custom
    template tag.
    """

    name = models.CharField(db_column='Name', blank=False, null=False, max_length=50)
    url = models.URLField(db_column='Url', blank=False, null=False)
    slug = models.SlugField(db_column='Slug', blank=False, null=False, unique=True, max_length=20,
                            help_text=_('The string used to reference the URL from within a Django template. The slug can'
                                        ' only contain letters, numbers, underscores and hyphens.'))

    class Meta:
        managed = True
        db_table = 'custom_url'
        ordering = ['name']
        verbose_name = _('Custom URL')
        verbose_name_plural = _('Custom URLs')

    def __str__(self):
        return _(self.name)
