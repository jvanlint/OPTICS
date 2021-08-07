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
	waypoint_type = models.CharField(
		max_length=10, 
		choices=WAYPOINT_TYPES, 
		null=True)
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
