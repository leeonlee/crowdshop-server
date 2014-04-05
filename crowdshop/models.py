from django.db import models
from django.contrib.auth.models import User
from django import forms

# Create your models here.
class LoginForm(forms.Form):
	username = forms.CharField(label=('Username'), max_length=30)
	password = forms.CharField(label=('Password'), widget=forms.PasswordInput(render_value=False), max_length=30)

# Create your models here.
class Task(models.Model):
	owner = models.ForeignKey(User, related_name="owner")
	title = models.CharField(max_length=255)
	desc = models.CharField(max_length=255)
	claimed_by = models.ForeignKey(User, related_name="claimed_by", blank=True, null=True)
	threshold = models.IntegerField()
	timeStamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.title
