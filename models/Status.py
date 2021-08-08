from django.db import models

class Status(models.Model):
	# Fields

	name = models.CharField(
		max_length=20, 
		help_text="Enter Status Type"
	)
	
	# Methods
	
	def __str__(self):
		return self.name
	
	# Metadata
	
	class Meta:
		verbose_name = "Campaign Status"
		verbose_name_plural = "Campaign Status"

