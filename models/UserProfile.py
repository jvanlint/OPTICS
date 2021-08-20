from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_resized import ResizedImageField
from airops.models import Squadron


class UserProfile(models.Model):
    """Profile data about a user.
    Timezone, Profile_image, Squadron info stored here
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
        upload_to=f"user/profile_images/{User.pk}/",
        help_text="User profile image file.",
        null=False,
        blank=False,
        default="assets/img/avatars/pilot1.png",
    )
    timezone = models.CharField(default=settings.TIME_ZONE, max_length=100)
    squadron = models.ForeignKey(
        Squadron,
        on_delete=models.PROTECT,
        verbose_name="Squadron",
        null=False,
        default=Squadron.objects.get(pk=1),
    )

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

    @property  # https://code.djangoproject.com/ticket/13327
    def image_url(self):
        if self.profile_image and hasattr(self.profile_image, "url"):
            self.profile_image.storage.base_url = settings.STATIC_URL
            return self.profile_image.url
        else:
            self.profile_image = "assets/img/avatars/pilot1.png"

    class Meta:
        db_table = "user_profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


#
# @receiver(post_delete, sender=User)
# def clear_user_profile_picture(sender, instance, deleted, **kwargs):
#     if deleted:
#         pass
#         # TODO: Delete the file after user is removed
#         # if "avatars" not in UserProfile.image_url:
#         #     with UserProfile.profile_image as f:
#         #         picture_file = File(f)
#         #         picture_file.delete()
