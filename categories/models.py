from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _

from utils import compress_image, get_upload_path


class Category(models.Model):
    """Represents a category"""

    name = models.CharField(verbose_name=_('Category name'), max_length=255)
    description = models.TextField(verbose_name=_('Category description'),
                                   blank=True)

    slug = models.SlugField(max_length=255, editable=False)
    icon = models.ImageField(verbose_name=_('Category icon'),
                             upload_to=get_upload_path,
                             blank=True)

    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               related_name='categories',
                               on_delete=models.CASCADE)

    _prev_icon = None
    _prev_name = None

    class Meta:
        db_table = 'categories'
        ordering = ['name', ]

    def __str__(self):
        return self.name

    def validate_unique(self, exclude=None):
        if not self.pk or self.name.lower() != self._prev_name.lower():
            qs = Category.objects.annotate(name_lower=Lower('name')) \
                .filter(name_lower=self.name.lower(),
                        author=self.author)

            if qs.exists():
                raise ValidationError(
                    {'name': ValidationError(
                        _('A category with the same name already exists.'),
                        code='invalid')})
        return super().validate_unique(exclude=exclude)

    def save(self, *args, **kwargs):
        if not self.slug or self._prev_name != self.name:
            self.slug = slugify(self.name)

        if self.icon and self.icon != self._prev_icon:
            self.icon = compress_image(self.icon, size=(200, 200))

        super(Category, self).save(*args, **kwargs)
        self._prev_icon = self.icon
        self._prev_name = self.name

    def get_absolute_url(self):
        return reverse('categories:category-detail',
                       kwargs={'slug': self.slug})

    def get_upload_path(self, filename):
        return settings.ICONS_FOLDER.format(username=self.author.username,
                                            category=self.name,
                                            filename=filename)
