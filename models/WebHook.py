from django.db import models

class WebHook(models.Model):
	service_name = models.CharField(max_length=30, 
							help_text='Enter the service/app the webhook is for', 
							verbose_name="Service Name")
	url = models.CharField(max_length=255, 
							help_text='Enter the web hook URL.', 
							verbose_name="Web Hook URL")
	class Meta:
		ordering = ['-service_name']