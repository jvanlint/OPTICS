from django.db import models
from django_resized import ResizedImageField

class MissionImagery(models.Model):
	mission = models.ForeignKey(
		"Mission", 
		on_delete=models.CASCADE, 
		null=True
	)
	caption = models.CharField(
		max_length=100, 
		null=True
	)
	image = ResizedImageField(
		verbose_name="Mission Imagery",
		size=[1500, 1200],
		upload_to="campaign/mission/mission_images/",
		help_text="Upload image for mission.",
		null=True,
		blank=True,
	)