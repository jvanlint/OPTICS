from django.db import models
from django.contrib.auth.models import User


class AirframeDefaults(models.Model):
    airframe_type = models.ForeignKey("Airframe", on_delete=models.CASCADE, null=True)

    callsign = models.CharField(
        max_length=20,
        help_text="Call sign for this type of airframe.",
        null=False,
        blank=False,
    )

    default_radio_freq = models.CharField(
        max_length=15, help_text="Default radio frequency.", null=False, blank=False
    )

    laser_code = models.CharField(
        max_length=10, help_text="Default laser code.", null=False, blank=False
    )

    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_created.hidden = True
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Metadata

    class Meta:
        ordering = ["-airframe_type", "-callsign"]
        verbose_name = "Airframe Defaults"
        verbose_name_plural = "Airframe Defaults"
