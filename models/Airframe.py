from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	date_created.hidden = True
	date_modified = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

	# Metadata

	class Meta:
		ordering = ["name"]

	# Methods

	def __str__(self):
		return self.name

	def edit_url(self):
		return reverse("reference_object_update", kwargs={"item_id": self.id, "table": "airframe"})
