from django.db import models
from django.contrib.auth.models import User

class MissionFile (models.Model):
	
	# Values
	FILE_TYPES = (
		("MIZ", "Mission"),
		("LIB", "Liberation"),
		("COM", "CombatFlite"),
	)
	mission = models.ForeignKey('Mission', 
								 on_delete=models.CASCADE, 
								 null=True)
	name = models.CharField(
		max_length=100, verbose_name="File Name")
	mission_file = models.FileField(null=True)
	file_type = models.CharField(
		max_length=10, 
		choices=FILE_TYPES, 
		default="MIZ"
	)
	uploaded_by = models.ForeignKey(User, 
								null=True, 
								blank=True, 
								on_delete=models.SET_NULL, 
								verbose_name='File Uploader')
	date_uploaded = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ['-date_uploaded']
		verbose_name = 'Mission File'