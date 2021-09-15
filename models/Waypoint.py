from django.db import models

class Waypoint(models.Model):
	#Values
	WAYPOINT_TYPES = (
		("NAV", "NAV"),
		("IP", "IP"),
		("CAP", "CAP"),
		("STRIKE", "STRIKE"),
		("CAS", "CAS"),
		("DEAD", "DEAD"),
		("SEAD", "SEAD"),
		("BAI", "BAI"),
		("TAKEOFF", "TAKEOFF"),
		("LAND", "LAND"),
		("DIVERT", "DIVERT"),
	)
	
	# Fields

	flight = models.ForeignKey(
		"Flight", 
		on_delete=models.CASCADE, 
		null=True
	)
	name = models.CharField(
		max_length=50
	)
	number = models.IntegerField(
		default=1,
		help_text="A number representing the waypoint order.",
		verbose_name="waypoint number",
	)
	waypoint_type = models.ForeignKey(
		"WaypointType",
		on_delete=models.SET_NULL,
		null=True
	)
	lat = models.CharField(
		max_length=15, 
		null=True, 
		blank=True)
	long = models.CharField(
		max_length=15, 
		null=True, 
		blank=True
	)
	elevation = models.CharField(
		max_length=15, 
		null=True, 
		blank=True
	)
	tot = models.CharField(
		max_length=15, 
		null=True, 
		blank=True, 
		verbose_name="time on Target"
	)
	notes = models.TextField(
		help_text="Enter notes for the waypoint.", 
		null=True, 
		blank=True
	)

	
	def new(self, flightObject):
		new_waypoint_instance = Waypoint(
			flight = flightObject,
			name = self.name,
			number = self.number + 1,
			waypoint_type = self.waypoint_type,
			lat = self.lat,
			long = self.long,
			elevation = self.elevation,
			tot = self.tot,
			notes = self.notes
		)
		
		new_waypoint_instance.save()
	
	def copy(self):
		flightID = self.flight.id
		
		self.new(self.flight)
		
		return flightID
		
	def copyToFlight(self, flight):
		self.new(flight)