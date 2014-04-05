from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
	owner = models.ForeignKey(User, related_name="owner")
	title = models.CharField(max_length=255)
	desc = models.CharField(max_length=255)
	claimed_by = models.ForeignKey(User, related_name="claimed_by", blank=True, null=True)
	threshold = models.IntegerField()

	def __unicode__(self):
		return self.title
