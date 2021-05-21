from django.db import models

class Status(models.Model):

    # Fields

    name = models.CharField(
        max_length=20, help_text='Enter Status Type')

    def __str__(self):
        """String for representing the Campaign object (in Admin site etc.)."""
        return self.name
