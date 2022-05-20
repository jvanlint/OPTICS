from django.db import models
from django.contrib.auth.models import User


class WaypointType(models.Model):
    # choices
    # These DCS mappings are most probably very incomplete, as pydcs seems to
    # build this field from a number of places. Perhaps I have the wrong field here
    # for what we really want.
    class DCSWaypointTypes(models.TextChoices):
        Not_Mapped = 'Not Mapped'
        TakeOffParking = 'TakeOffParking'
        TakeOffParkingHot = 'TakeOffParkingHot'
        Turning_Point = 'Turning Point'

    name = models.CharField(max_length=10, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    dcs_mapping = models.CharField(
        max_length=50,
        choices=DCSWaypointTypes.choices,
        default=DCSWaypointTypes.Not_Mapped,
    )

    class Meta:
        verbose_name = "Waypoint Type"
        ordering = ["name"]

    def __str__(self):
        """String for representing the WaypointType object (in Admin site etc.)."""
        return self.name
