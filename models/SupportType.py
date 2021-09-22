from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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

    def edit_url(self):
        return reverse("reference_object_update", kwargs={"item_id": self.id, "card_name": "support_type"})

    def display_data(self):
        return [self.name]

    @staticmethod
    def field_headers():
        return None
