from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext as _

from utils import compress_image, get_upload_path


class User(AbstractUser):
    """User profile"""

    email = models.EmailField(blank=False, unique=True)
    profile_photo = models.ImageField(verbose_name=_('Profile photo'),
                                      upload_to=get_upload_path,
                                      blank=True)

    _prev_photo = None
    _prev_password = None

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.profile_photo and self._prev_photo != self.profile_photo:
            self.profile_photo = compress_image(self.profile_photo)

        if self.pk and self._prev_password != self.password:
            self.set_password(self.password)

        super(User, self).save(*args, **kwargs)
        self._prev_photo = self.profile_photo
        self._prev_password = self.password

    def get_absolute_url(self):
        return reverse('accounts:user-profile')

    def get_upload_path(self, filename):
        return settings.PHOTOS_FOLDER.format(username=self.username,
                                             filename=filename)
