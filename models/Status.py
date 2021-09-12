from django.db import models
from django.contrib.auth.models import User

class Status(models.Model):
	# Fields

	name = models.CharField(
		max_length=20, 
		help_text="Enter Status Type"
	)
	date_created = models.DateTimeField(
		auto_now_add=True, 
		null=True
	)
	date_modified = models.DateTimeField(null=True)
	user = models.ForeignKey(
		User, 
		on_delete=models.CASCADE, 
		null=True
	)
	
	# Methods
	
	def __str__(self):
		return self.name
	
	# Metadata
	
	class Meta:
		verbose_name = "Campaign Status"
		verbose_name_plural = "Campaign Status"

