from django.db import models
from django_resized import ResizedImageField
from django.urls import reverse


class Target(models.Model):

    # Fields

    mission = models.ForeignKey('Mission', on_delete=models.CASCADE, null=True)
    
    name = models.CharField(max_length=50,
                            help_text='Enter target name',
                            verbose_name="Target Name")
    
    lat = models.CharField(max_length=200,
                           help_text='Enter target latitude',
                           verbose_name="Target Latitude",
                           null=True, blank=True)
    
    long = models.CharField(max_length=200,
                            help_text='Enter target longitude.',
                            verbose_name="Target Longitude",
                            null=True, blank=True)
    
    elev = models.CharField(max_length=200,
                            help_text='Enter target elevation.',
                            verbose_name="Target Elevation",
                            null=True, blank=True)
    
    notes = models.TextField(help_text='Any notes relevant to the target.',
                             null=True, blank=True,
                             verbose_name="Notes on Target")
    
    target_image = ResizedImageField(verbose_name='Target Image',
                                     size=[1500, 1200],
                                     upload_to='campaign/mission/target_images/',
                                     help_text='Upload image of the target.',
                                     null=True, blank=True)
    
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
