from django.db import models


class Squadron(models.Model):
    """Squadron model.
    A list of squadrons for
    users to be associated with
    """

    squadron_name = models.CharField(max_length=50, verbose_name="Squadron Name", unique=True, blank=False)
    squadron_url = models.URLField(verbose_name="Squadron Website", null=True)

    def __str__(self):
        return self.squadron_name

    class Meta:
        db_table = "user_squadron"

