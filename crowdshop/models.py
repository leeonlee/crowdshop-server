from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
	venmo_id = models.CharField(max_length=30, unique=True)

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
	owner = models.ForeignKey(MyUser, related_name="tasks")
	title = models.CharField(max_length=255)
	desc = models.CharField(max_length=255)
	claimed_by = models.ForeignKey(MyUser, related_name="claimed_by", blank=True, null=True)
	threshold = models.IntegerField(default = 0)
	paid = models.IntegerField(blank = True, null=True)
	reward = models.IntegerField(default = 0)
	timeStamp = models.DateTimeField(auto_now=True)
	state = models.ForeignKey(State, related_name="tasks", null=True, blank=True)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['-timeStamp']
