from django.db import models

class Terrain(models.Model):

    # Fields

    name = models.CharField(
        max_length=20, help_text='Enter Terrain Map Name.')

    def __str__(self):
        """String for representing the Campaign object (in Admin site etc.)."""
        return self.name
