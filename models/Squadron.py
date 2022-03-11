from django.db import models


class Squadron(models.Model):
    """Squadron model.
    A list of squadrons for users to be associated with
    """

    squadron_name = models.CharField(
        max_length=50,
        verbose_name="Squadron Name",
        unique=True,
        blank=False,
    )
    squadron_url = models.URLField(verbose_name="Squadron Website", null=True)

    def __str__(self):
        return self.squadron_name

    @classmethod
    def get_default_pk(cls):
        squadron, created = cls.objects.get_or_create(
            pk=1, defaults=dict(squadron_name="None")
        )
        return squadron.pk

    class Meta:
        db_table = "user_squadron"
