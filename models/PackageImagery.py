from django.db import models
from django_resized import ResizedImageField

class PackageImagery(models.Model):
	package = models.ForeignKey(
		"Package", 
		on_delete=models.CASCADE, 
		null=True
	)
	caption = models.CharField(
		max_length=100, 
		null=True
	)
	image = ResizedImageField(
		verbose_name="Package Imagery",
		size=[1500, 1200],
		upload_to="campaign/mission/package_images/",
		help_text="Upload image for package.",
		null=True,
		blank=True,
	)