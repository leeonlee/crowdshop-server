from django.db import models

# Create your models here.
class Task(models.Model):
	owner = models.ForeignKey(User)
	title = models.CharField(max_length=255)
	desc = models.CharField(max_length=255)
	claimed_by = models.ForeignKey(User)
	threshold = models.IntegerField()
