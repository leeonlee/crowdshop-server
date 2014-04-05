from django.db import models
from django import forms

# Create your models here.
class LoginForm(forms.Form):
	username = forms.CharField(label=('Username'), max_length=30)
	password = forms.CharField(label=('Password'), widget=forms.PasswordInput(render_value=False), max_length=30)