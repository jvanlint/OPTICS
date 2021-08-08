from django.db import models
from .Target import *
#from .Aircraft import *

class Flight(models.Model):
	# Fields

	package = models.ForeignKey(
		"Package", 
		on_delete=models.CASCADE, 
		null=True
	)
	callsign = models.CharField(
		max_length=200, 
		help_text="Enter Flight Callsign"
	)
	task = models.ForeignKey(
		"Task", 
		on_delete=models.CASCADE, 
		null=True
	)
	flight_coordination = models.TextField(
		help_text="Use this field to enter in any notes that the flight lead might need to use to coordinate other members of the flight,",
		null=True,
		blank=True,
		verbose_name="Notes for flight co-ordination",
	)
	radio_frequency = models.CharField(
		max_length=20, 
		help_text="Enter Flight Frequency", 
		blank=True, 
		null=True
	)
	tacan = models.CharField(
		max_length=5,
		help_text="Enter Flight TACAN (if applicable)",
		blank=True,
		null=True,
	)
	targets = models.ManyToManyField(
		Target, 
		blank=True
	)

	# Time Hacks
	timehack_start = models.CharField(
		max_length=10,
		help_text="Enter time for flight takeoff.",
		null=True,
		blank=True,
		verbose_name="Takeoff Time",
	)
	timehack_rdv1 = models.CharField(
		max_length=10,
		help_text="Enter time for flight rendevous point 1.",
		null=True,
		blank=True,
		verbose_name="Time RDV 1",
	)
	timehack_rdv2 = models.CharField(
		max_length=10,
		help_text="Enter time for flight rendevous point 2.",
		null=True,
		blank=True,
		verbose_name="Time RDV 2",
	)
	fuel_fob = models.CharField(
		max_length=10,
		help_text="Fuel FOB",
		null=True,
		blank=True,
		verbose_name="Fuel FOB",
	)
	fuel_joker = models.CharField(
		max_length=10,
		help_text="Fuel JOKER.",
		null=True,
		blank=True,
		verbose_name="Fuel JOKER",
	)
	fuel_bingo = models.CharField(
		max_length=10,
		help_text="Fuel BINGO.",
		null=True,
		blank=True,
		verbose_name="Fuel BINGO",
	)

	# Metadata

	class Meta:
		ordering = ["callsign"]

	# Methods

	def __str__(self):
		return self.callsign
		
	def new(self, packageObject):
		new_flight_instance = Flight(
			package = packageObject,
			callsign = self.callsign,
			task = self.task,
			flight_coordination = self.flight_coordination,
			radio_frequency = self.radio_frequency,
			tacan = self.tacan,
			timehack_start = self.timehack_start,
			timehack_rdv1 = self.timehack_rdv1,
			timehack_rdv2 = self.timehack_rdv2,
			fuel_fob = self.fuel_fob,
			fuel_joker = self.fuel_joker,
			fuel_bingo = self.fuel_bingo,
		)
		
		new_flight_instance.save()
		
		flight_aircraft = self.aircraft_set.all()
		if flight_aircraft:
			for aircraft in flight_aircraft:
				aircraft.copyToFlight(new_flight_instance)
		
		flight_waypoints = self.waypoint_set.all()
		if flight_waypoints:
			for waypoint in flight_waypoints:
				waypoint.copyToFlight(new_flight_instance)
		
	def copy(self):
		packageID = self.package.id
		
		self.new(self.package)
		
		return packageID
	
	def copyToPackage(self, package):
		packageID = self.package.id
		
		self.new(package)
		
		return packageID