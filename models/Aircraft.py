from django.db import models
from django.contrib.auth.models import User

class Aircraft(models.Model):
	# Fields

	type = models.ForeignKey(
		"Airframe", 
		on_delete=models.CASCADE, 
		null=True
	)
	flight = models.ForeignKey(
		"Flight", 
		on_delete=models.CASCADE, 
		null=True
	)
	pilot = models.ForeignKey(
		User,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		related_name="user_pilot",
	)
	rio_wso = models.ForeignKey(
		User, 
		null=True, 
		blank=True, 
		on_delete=models.SET_NULL, 
		related_name="user_rio"
	)
	tailcode = models.CharField(
		max_length=20, 
		help_text="Enter A/C tail code.", 
		null=True, 
		blank=True
	)
	flight_lead = models.BooleanField(
		default=False
	)
	package_lead = models.BooleanField(
		default=False
	)

	# Metadata

	class Meta:
		ordering = ["-flight_lead", "-pilot"]
		verbose_name = "Aircraft"
		verbose_name_plural = "Aircraft"

	# Methods

	def multicrew(self):
		return self.type.multicrew