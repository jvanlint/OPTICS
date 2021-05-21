from django.db import models

class Support(models.Model):

    # Fields

    mission = models.ForeignKey('Mission', on_delete=models.CASCADE, null=True)

    THREAT_TYPES = (
        ('AWACS', 'AWACS'),
        ('TANKER', 'TANKER'),
        ('JTAC', 'JTAC'),
        ('CARRIER', 'CARRIER'),

    )

    callsign = models.CharField(max_length=50)
    support_type = models.CharField(max_length=10, choices=THREAT_TYPES, null=True)
    frequency = models.CharField(max_length=10, null=True, blank=True)
    tacan = models.CharField(max_length=10, null=True, blank=True)
    altitude = models.CharField(max_length=10, null=True, blank=True)
    speed = models.CharField(max_length=10, null=True, blank=True)
    brc = models.CharField(max_length=10, null=True, blank=True)
    icls = models.CharField(max_length=10, null=True, blank=True)

    notes = models.TextField(help_text='Enter notes for support resource.', null=True, blank=True)
