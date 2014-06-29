from django.db import models

# Create your models here.
class Person(models.Model):
	"""
	The person model will define a user of the application
	"""
	display_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255, unique=True)
	token = models.CharField(max_length = 50, unique=True)

class Task(models.Model):
	owner = models.ForeignKey(Person, related_name="tasks")
	title = models.CharField(max_length=255)
	desc = models.CharField(max_length=255)
	claimed_by = models.ForeignKey(Person, related_name="claimed_by", blank=True, null=True)
	threshold = models.IntegerField(default = 0)
	actual_price = models.IntegerField(default = 0)
	reward = models.IntegerField(default = 0)
	complete = models.BooleanField(default = False)
	timeStamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['-timeStamp']
