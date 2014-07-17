from django.forms import ModelForm
from crowdshop.models import Task
from django import forms

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ["title", "desc", "threshold", "reward",]

class PaymentForm(forms.Form):
	amount = forms.IntegerField()
	task_id = forms.IntegerField()

	def clean_task_id(self):
		task_id = self.cleaned_data["task_id"]
		if Task.objects.filter(pk=task_id).exists():
			return task_id
		else:
			raise forms.ValidationError("That id doesn't belong to any task.")
			return task_id

	def clean_amount(self):
		amount = self.cleaned_data["amount"]
		if amount > 0:
			return amount
		else:
			raise forms.ValidationError("Amount must be greater than 0.")
			return amount
