from django.db import models

class Task(models.Model):
	task_name = models.CharField(
		max_length=10, 
		null=True
	)

	class Meta:
		ordering = ["task_name"]

	def __str__(self):
		return self.task_name