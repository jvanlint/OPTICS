from django.db import models
from django_resized import ResizedImageField

class FlightImagery(models.Model):
	flight = models.ForeignKey(
		"Flight", 
		on_delete=models.CASCADE, 
		null=True
	)
	caption = models.CharField(
		max_length=100, 
		null=True
	)
	image = ResizedImageField(
		verbose_name="Flight Imagery",
		size=[1500, 1200],
		upload_to="campaign/mission/flight_images/",
		help_text="Upload image for flight.",
		null=True,
		blank=True,
	)