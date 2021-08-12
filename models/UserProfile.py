from django.db import models
from django.utils import timezone
from django_resized import ResizedImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings


# Set the user email field to unique
User._meta.get_field("email")._unique = True


class UserProfile(models.Model):
    """Profile data about a user.
    Timezone info stored here
    https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
    """

    user = models.OneToOneField(
        User,
        primary_key=True,
        verbose_name="user",
        related_name="profile",
        on_delete=models.CASCADE,
    )
    profile_image = ResizedImageField(
        verbose_name="User profile image.",
        size=[200, 200],
        upload_to="user/profilepics/",
        help_text="User profile image file.",
        null=True,
        blank=True,
        default="assets/img/avatars/pilot1.png",
    )
    timezone = models.CharField(
        max_length=256, blank=True, null=True, default=settings.TIME_ZONE
    )
    callsign = models.CharField(max_length=256, blank=True, null=True, unique=True)

    def __str__(self):
        return self.user.username

    def is_admin(self):
        return self.user.groups.filter(name="admin").exists()

    def is_planner(self):
        return self.user.groups.filter(name="planner").exists()

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            if request.user.is_superuser:
                return True
            else:
                if obj.creator != request.user:
                    return False
                else:
                    return True

    class Meta:
        db_table = "user_profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
