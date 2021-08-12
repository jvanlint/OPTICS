import os
from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings

# Import special image library that allows resizing of images on upload.
from django_resized import ResizedImageField

from django.urls import reverse

# Import User model to enable user as field in other models
from django.contrib.auth.models import User


class Profile(models.Model):
    default_avatar = os.path.join(settings.STATIC_ROOT, "optics/img/avatars/pilot1.png")
    # Fields

    user = models.OneToOneField(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE)

    profile_image = ResizedImageField(verbose_name='User profile image.',
                                      size=[200, 200],
                                      upload_to='user/profilepics/',
                                      help_text='User profile image file.',
                                      null=True,
                                      blank=True,
                                      default=default_avatar)
