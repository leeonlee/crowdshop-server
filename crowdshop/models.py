from django.db import models

# Create your models here.
class Person(models.Model):
	"""
	The person model will define a user of the application
	"""
	display_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255, unique=True)
	token = models.CharField(max_length = 50, unique=True)

class State(models.Model):
	"""
	States to represent the workflow of a task
	Opened, claimed, paid, resolved
	"""
	name = models.CharField(max_length=255)
	next_state = models.OneToOneField("self", related_name="previous_state", null=True)

	def __unicode__(self):
		return self.name

class Task(models.Model):
	"""
	Tasks models to represent the needs of a user
	"""
	owner = models.ForeignKey(Person, related_name="tasks")
	title = models.CharField(max_length=255)
	desc = models.CharField(max_length=255)
	claimed_by = models.ForeignKey(Person, related_name="claimed_by", blank=True, null=True)
	threshold = models.IntegerField(default = 0)
	actual_price = models.IntegerField(default = 0)
	reward = models.IntegerField(default = 0)
	complete = models.BooleanField(default = False)
	timeStamp = models.DateTimeField(auto_now=True)
	state = models.ForeignKey(State, related_name="tasks")

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['-timeStamp']
