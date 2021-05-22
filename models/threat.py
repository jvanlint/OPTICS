from django.db import models
from django.urls import reverse

class Threat(models.Model):

    # Fields

    mission = models.ForeignKey('Mission', on_delete=models.CASCADE, null=True)

    THREAT_TYPES = (
        ('AAA', 'AAA'),
        ('SAM', 'SAM'),
        ('AIR', 'AIR'),
        ('NAVAL', 'NAVAL'),
        ('GROUND', 'GROUND'),

    )

    name = models.CharField(max_length=60)
    threat_type = models.CharField(max_length=10, choices=THREAT_TYPES, null=True)
    description = models.TextField(help_text='Enter Threat Description/Situation.',
                                   default="Threat description to be added here.")
