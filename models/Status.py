from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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

	def edit_url(self):
		return reverse("reference_object_update", kwargs={"item_id": self.id, "table": "status"})

	def get_fields(self):  # https://stackoverflow.com/a/59237767/16148276
		return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]

	# Metadata
	
	class Meta:
		verbose_name = "Campaign Status"
		verbose_name_plural = "Campaign Status"

