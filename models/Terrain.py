from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Terrain(models.Model):
	# Fields

	name = models.CharField(
		max_length=20, 
		help_text="Enter Terrain Map Name."
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

	def edit_url(self):
		return reverse("reference_object_update", kwargs={"item_id": self.id, "table": "terrain"})

	# Metadata

	class Meta:
		ordering = ["-name"]
		verbose_name_plural = "Terrain"
