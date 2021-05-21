from django.db import models
from django_resized import ResizedImageField
from django.urls import reverse


class Campaign(models.Model):

    # Fields

    name = models.CharField(max_length=200,
                            help_text='The Campaign Name.')
    
    description = models.TextField(help_text='A brief description used for display purposes on selection screens.',
                                   default="Campaign description to be added here.")
    
    dcs_map = models.ForeignKey('Terrain',
                                on_delete=models.CASCADE,
                                null=True,
                                verbose_name="dcs Terrain")
    
    start_date = models.DateField(help_text='Proposed Start Date of Campaign.',
                                  blank=True,
                                  null=True,
                                  verbose_name="Expected Start Date")
    
    campaignImage = ResizedImageField(verbose_name='Campaign Image Thumbnail.',
                                      size=[500, 300],
                                      upload_to='campaign/thumbnails/',
                                      help_text='Campaign Image File.',
                                      null=True, blank=True)
    
    status = models.ForeignKey('Status', on_delete=models.CASCADE, null=True)
    
    created_by = models.CharField(max_length=200,
                                  help_text='Name of campaign creator.',
                                  null=True, blank=True)
    
    situation = models.TextField(help_text='A detailed overview of the background and situation for the campaign.',
                                 null=True, blank=True)
    
    aoImage = ResizedImageField(verbose_name='area of Operations Image',
                                size=[1500, 1200],
                                upload_to='campaign/ao_images',
                                help_text='An image of the Area of Operations.',
                                null=True, blank=True)

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
