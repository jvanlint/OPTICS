from django.db import models
from django.contrib.auth.models import User

class CombatFliteFile (models.Model):
	mission = models.ForeignKey('Mission', 
								 on_delete=models.CASCADE, 
								 null=True)
	name = models.CharField(max_length=100, 
							help_text='Enter CombatFlite File Name', 
							verbose_name="Combat Flight File Name")
	combatflite_file = models.FileField(null=True)
	uploaded_by = models.ForeignKey(User, 
								null=True, 
								blank=True, 
								on_delete=models.SET_NULL, 
								verbose_name='CombatFlite File Uploader')
	date_uploaded = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		ordering = ['-date_uploaded']
		verbose_name = 'Combat Flite File'