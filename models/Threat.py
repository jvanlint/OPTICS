from django.db import models

class Threat(models.Model):
	
	# Values
	THREAT_TYPES = (
		("AAA", "AAA"),
		("SAM", "SAM"),
		("AIR", "AIR"),
		("NAVAL", "NAVAL"),
		("GROUND", "GROUND"),
	)
	
	# Fields

	mission = models.ForeignKey(
		"Mission", 
		on_delete=models.CASCADE, 
		null=True
	)
	threat_name = models.ForeignKey(
		"ThreatReference", 
		on_delete=models.CASCADE, 
		null=True
	)
	name = models.CharField(
		max_length=60
	)
	threat_type = models.CharField(
		max_length=10, 
		choices=THREAT_TYPES, 
		null=True
	)
	description = models.TextField(
		help_text="Enter Threat Description/Situation.",
		default="Threat description to be added here.",
	)
	
	def new(self, missionObject):
		new_threat_instance = Threat(
			mission = missionObject,
			threat_name = self.threat_name,
			name = self.name,
			threat_type = self.threat_type,
			description = self.description,
		)
		
		new_threat_instance.save()
	
	def copy(self):
		missionID = self.mission.id 
		self.new(self.mission)
		return missionID 
	
	def copyToMission(self, mission):
		missionID = self.mission.id 
		self.new(mission)
		return missionID