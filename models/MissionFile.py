from django.db import models
from django.contrib.auth.models import User

class MissionFile (models.Model):
	mission = models.ForeignKey('Mission', 
								 on_delete=models.CASCADE, 
								 null=True)
	name = models.CharField(
		max_length=100, help_text='Enter Mission File Name', verbose_name="Misison File Name")
	mission_file = models.FileField(null=True)
	uploaded_by = models.ForeignKey(User, 
								null=True, 
								blank=True, 
								on_delete=models.SET_NULL, 
								verbose_name='Mission File Uploader')
	date_uploaded = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ['-date_uploaded']
		verbose_name = 'Mission File'