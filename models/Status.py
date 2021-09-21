from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Status(models.Model):
    # Fields
    name = models.CharField(max_length=20, help_text="Enter Status Type")
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    # Methods
    def __str__(self):
        return self.name

    def edit_url(self):
        return reverse(
            "reference_object_update", kwargs={"item_id": self.id, "table": "status"}
        )

    def display_data(self):
        # data = {}
        # if fields_to_display:
        #     for field_name in fields_to_display:
        #         value = self._meta.get_field(field_name).value_from_object(self)
        #         data.update({field_name: value})
        #     return data
        # else:
        return {"name": self.name}

    @staticmethod
    def field_headers():
        return ["Name"]

    class Meta:
        verbose_name = "Campaign Status"
        verbose_name_plural = "Campaign Status"
