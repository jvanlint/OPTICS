from django.db import models
# Required for Generic Keys for Comments
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Comment(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	comment = models.TextField()
	date_created = models.DateTimeField(auto_now_add=True)

	# Below the mandatory fields for generic relation
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey()

	class Meta:
		ordering = ['-date_created']
