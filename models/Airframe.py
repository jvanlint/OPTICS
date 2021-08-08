from django.db import models

class Airframe(models.Model):
	# Fields

	name = models.CharField(
		max_length=200, 
		help_text="Enter Airframe Name"
	)
	stations = models.IntegerField(
		default=2
	)
	multicrew = models.BooleanField(
		default=False
	)

	# Metadata

	class Meta:
		ordering = ["name"]

	# Methods

	def __str__(self):
		return self.name