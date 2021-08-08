from django.db import models
from django_resized import ResizedImageField

class Target(models.Model):
	# Fields

	mission = models.ForeignKey(
		"Mission", 
		on_delete=models.CASCADE, 
		null=True
	)
	name = models.CharField(
		max_length=50, 
		help_text="Enter target name", 
		verbose_name="Target Name"
	)
	lat = models.CharField(
		max_length=200,
		help_text="Enter target latitude",
		verbose_name="Target Latitude",
		null=True,
		blank=True,
	)
	long = models.CharField(
		max_length=200,
		help_text="Enter target longitude.",
		verbose_name="Target Longitude",
		null=True,
		blank=True,
	)
	elev = models.CharField(
		max_length=200,
		help_text="Enter target elevation.",
		verbose_name="Target Elevation",
		null=True,
		blank=True,
	)
	notes = models.TextField(
		help_text="Any notes relevant to the target.",
		null=True,
		blank=True,
		verbose_name="Notes on Target",
	)
	target_image = ResizedImageField(
		verbose_name="Target Image",
		size=[1500, 1200],
		upload_to="campaign/mission/target_images/",
		help_text="Upload image of the target.",
		null=True,
		blank=True,
	)

	# Metadata

	class Meta:
		ordering = ["name"]

	# Methods

	def __str__(self):
		return self.name
		
	def new(self, missionObject):
		new_target_instance = Target(
			mission = missionObject,
			name = self.name,
			lat = self.lat,
			long = self.long,
			elev = self.elev,
			notes = self.notes,
			target_image = self.target_image
		)
		
		new_target_instance.save()
	
	def copy(self):
		missionID = self.mission.id 
		self.new(self.mission)
		return missionID 
	
	def copyToMission(self, mission):
		missionID = self.mission.id 
		self.new(mission)
		return missionID