from django.db import models
from django.urls import reverse

class Package(models.Model):

    # Fields

    mission = models.ForeignKey('Mission', on_delete=models.CASCADE, null=True)
    
    name = models.CharField(max_length=200,
                            help_text='Enter Package Name',
                            verbose_name="Package Name")
    
    frequency = models.CharField(max_length=10,
                                 help_text='Enter Package Frequency',
                                 verbose_name="Package Frequency",
                                 null=True, blank=True)
    
    description = models.TextField(help_text='Enter Mission Description/Situation.',
                                   null=True, blank=True,
                                   verbose_name="Description of package objective")
  # Metadata

    class Meta:
        ordering = ['-name']

    # Methods

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the Campaign object (in Admin site etc.)."""
        return self.name