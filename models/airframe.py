from django.db import models
from django.urls import reverse

class Airframe(models.Model):

    # Fields

    name = models.CharField(max_length=200,
                            help_text='Enter Airframe Name')
    
    stations = models.IntegerField(default=2)

    # Metadata

    class Meta:
        ordering = ['name']

    # Methods

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.name
