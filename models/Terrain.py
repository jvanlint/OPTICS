from django.db import models

class Terrain(models.Model):
	# Fields

	name = models.CharField(
		max_length=20, 
		help_text="Enter Terrain Map Name."
	)

	# Methods
	
	def __str__(self):
		return self.name
		
	# Metadata

	class Meta:
		ordering = ["-name"]
		verbose_name_plural = "Terrain"
