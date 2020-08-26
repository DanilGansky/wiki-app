from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _

from utils import compress_image, get_html_from_markdown, get_upload_path


class SharedPagesManager(models.Manager):
    def get_queryset(self):
        return super(SharedPagesManager, self).get_queryset() \
            .filter(is_shared=True)


class Page(models.Model):
    """Represents a page"""

    title = models.CharField(verbose_name=_('Page title'), max_length=255)
    description = models.TextField(verbose_name=_('Page description'),
                                   blank=True)

    slug = models.SlugField(max_length=255, editable=False)
    category = models.ForeignKey(to='categories.Category',
                                 related_name='pages',
                                 on_delete=models.CASCADE)

    content_markup = models.TextField(verbose_name=_('Content (Markdown)'))
    content_markup_html = models.TextField(editable=False)
    background_image = models.ImageField(verbose_name=_('Page background'),
                                         upload_to=get_upload_path,
                                         blank=True)

    is_shared = models.BooleanField(verbose_name=_('Shared?'), default=False)
    tags = ArrayField(models.CharField(max_length=30), blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               related_name='pages',
                               on_delete=models.SET_NULL,
                               null=True)

    objects = models.Manager()
    shared = SharedPagesManager()

    _prev_background = None
    _prev_title = None

    class Meta:
        db_table = 'pages'
        ordering = ['date_update', ]

    def __str__(self):
        return self.title

    def validate_unique(self, exclude=None):
        if not self.pk or self.title.lower() != self._prev_title.lower():
            qs = Page.objects.annotate(title_lower=Lower('title')) \
                .filter(title_lower=self.title.lower(),
                        author=self.author)

            if qs.exists():
                raise ValidationError(
                    {'title': ValidationError(
                        _('A page with the same title already exists.'),
                        code='invalid')})
        return super().validate_unique(exclude=exclude)

    def save(self, *args, **kwargs):
        if not self.slug or self._prev_title != self.title:
            self.slug = slugify(self.title)

        if (self.background_image and
                self._prev_background != self.background_image):
            self.background_image = compress_image(self.background_image)

        self.content_markup_html = get_html_from_markdown(self.content_markup)
        super(Page, self).save(*args, **kwargs)
        self._prev_background = self.background_image
        self._prev_title = self.title

    def get_absolute_url(self):
        return reverse('pages:page-detail',
                       kwargs={'slug': self.slug})

    def get_upload_path(self, filename):
        return settings.BACKGROUNDS_FOLDER \
            .format(username=self.author.username,
                    page=self.title,
                    filename=filename)
