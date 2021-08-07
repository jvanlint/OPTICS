from django.db import models

class Package(models.Model):
	# Fields

	mission = models.ForeignKey(
		"Mission", 
		on_delete=models.
		CASCADE, 
		null=True
	)
	name = models.CharField(
		max_length=200, 
		help_text="Enter Package Name", 
		verbose_name="Package Name"
	)
	frequency = models.CharField(
		max_length=10,
		help_text="Enter Package Frequency",
		verbose_name="Package Frequency",
		null=True,
		blank=True,
	)
	summary = models.TextField(
		help_text="Use this field to describe the overall objectives for the package.",
		null=True,
		blank=True,
		verbose_name="Summary of package objective",
	)
	package_coordination = models.TextField(
		help_text="Use this field to enter in any notes that the package lead might need to use to coordinate other members of the package,",
		null=True,
		blank=True,
		verbose_name="Notes for package co-ordination",
	)

	# Metadata

	class Meta:
		ordering = ["-name"]

	# Methods

	def __str__(self):
		return self.name
	
	def new(self, missionObject):
		new_package_instance = Package(
			mission = missionObject,
			name = self.name,
			frequency = self.frequency,
			summary = self.summary,
			package_coordination = self.package_coordination
		)
		
		new_package_instance.save()
		
		package_flights = self.flight_set.all()
		if package_flights:
			for flight in package_flights:
				flight.copyToPackage(new_package_instance)
	
	def copy(self):
		missionID = self.mission.id 
		self.new(self.mission)
		return missionID 
	
	def copyToMission(self, mission):
		missionID = self.mission.id 
		self.new(mission)
		return missionID