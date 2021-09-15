from django.db import models
from django.contrib.auth.models import User


class SupportType(models.Model):
    name = models.CharField(max_length=10, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        """String for representing the SupportType object (in Admin site etc.)."""
        return self.name
