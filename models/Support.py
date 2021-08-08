from django.db import models

class Support(models.Model):
	#Values
	
	SUPPORT_TYPES = (
		("AWACS", "AWACS"),
		("TANKER", "TANKER"),
		("JTAC", "JTAC"),
		("CARRIER", "CARRIER"),
		("LHA", "LHA"),
		("ABM", "ABM"),
		("AIRFIELD", "AIRFIELD"),
	)
	
	# Fields

	mission = models.ForeignKey(
		"Mission", 
		on_delete=models.CASCADE, 
		null=True
	)
	callsign = models.CharField(
		max_length=50
	)
	support_type = models.CharField(
		max_length=10, 
		choices=SUPPORT_TYPES,
		null=True
	)
	player_name = models.CharField(
		max_length=30, 
		null=True, 
		blank=True
	)
	frequency = models.CharField(
		max_length=10, 
		null=True, 
		blank=True
	)
	tacan = models.CharField(
		max_length=10, 
		null=True, 
		blank=True
	)
	altitude = models.CharField(
		max_length=10, 
		null=True, 
		blank=True
	)
	speed = models.CharField(
		max_length=10, 
		null=True, 
		blank=True
	)
	brc = models.CharField(
		max_length=10, 
		null=True, 
		blank=True
	)
	icls = models.CharField(
		max_length=10, 
		null=True, 
		blank=True
	)
	notes = models.TextField(
		help_text="Enter notes for support resource.", 
		null=True, 
		blank=True
	)
	
	def new(self, missionObject):
		new_support_instance = Support(
			mission = missionObject,
			callsign = self.callsign,
			support_type = self.support_type,
			player_name = self.player_name,
			frequency = self.frequency,
			tacan = self.tacan,
			altitude = self.altitude,
			speed = self.speed,
			brc = self.brc,
			icls = self.icls,
			notes = self.notes,
		)
		
		new_support_instance.save()
	
	def copy(self):
		missionID = self.mission.id 
		self.new(self.mission)
		return missionID 
	
	def copyToMission(self, mission):
		missionID = self.mission.id 
		self.new(mission)
		return missionID