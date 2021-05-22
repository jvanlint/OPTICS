from django.db import models
from django.urls import reverse
from .target import Target

class Flight(models.Model):

    # Fields

    package = models.ForeignKey('Package', on_delete=models.CASCADE, null=True)
    
    callsign = models.CharField(max_length=200,
                                help_text='Enter Flight Callsign')
    
    radio_frequency = models.CharField(max_length=20,
                                       help_text='Enter Flight Frequency',
                                       blank=True, null=True)
    
    tacan = models.CharField(max_length=5,
                             help_text='Enter Flight TACAN (if applicable)',
                             blank=True, null=True)
    
    targets = models.ManyToManyField(Target, blank=True)

    # Time Hacks
    timehack_start = models.CharField(max_length=10,
                                      help_text='Enter time for flight takeoff.',
                                      null=True, blank=True,
                                      verbose_name="Takeoff Time")
    
    timehack_rdv1 = models.CharField(max_length=10,
                                     help_text='Enter time for flight rendevous point 1.',
                                     null=True, blank=True,
                                     verbose_name="Time RDV 1")
    
    timehack_rdv2 = models.CharField(max_length=10,
                                     help_text='Enter time for flight rendevous point 2.',
                                     null=True, blank=True,
                                     verbose_name="Time RDV 2")
    
    fuel_fob = models.CharField(max_length=10,
                                help_text='Fuel FOB',
                                null=True, blank=True,
                                verbose_name="Fuel FOB")
    
    fuel_joker = models.CharField(max_length=10,
                                  help_text='Fuel JOKER.',
                                  null=True, blank=True,
                                  verbose_name="Fuel JOKER")
    
    fuel_bingo = models.CharField(max_length=10,
                                  help_text='Fuel BINGO.',
                                  null=True, blank=True,
                                  verbose_name="Fuel BINGO")

    # Metadata

    class Meta:
        ordering = ['callsign']

    # Methods

    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.callsign
