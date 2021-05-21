from django.db import models
from django.urls import reverse

class Aircraft(models.Model):

    # Fields

    type = models.ForeignKey('Airframe', on_delete=models.CASCADE, null=True)
    
    flight = models.ForeignKey('Flight', on_delete=models.CASCADE, null=True)
    
    pilot = models.CharField(max_length=30,
                             help_text='Enter Pilot Name',
                             null=True, blank=True)
    
    rio_wso = models.CharField(max_length=30,
                               help_text='Enter RIO/WSO Name',
                               null=True, blank=True)
    
    tailcode = models.CharField(max_length=20,
                                help_text='Enter A/C tail code.',
                                null=True, blank=True)
    
    flight_lead = models.BooleanField(default=False)
    package_lead = models.BooleanField(default=False)

    # Metadata

    class Meta:
        ordering = ['type']

    # Methods

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])
