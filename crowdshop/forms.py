from django.forms import ModelForm
from crowdshop.models import Task, MyUser
from django import forms

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = ["title", "desc", "threshold", "reward",]

class ClaimForm(forms.Form):
	venmo_id = forms.CharField()
	user = forms.ModelChoiceField(queryset = MyUser.objects.all())

	def clean(self):
		cleaned_data = super(ClaimForm, self).clean()
		venmo_id = cleaned_data.get("venmo_id", None)
		user = cleaned_data.get("user", None)

		if not venmo_id or not user:
			return cleaned_data

		if venmo_id != user.venmo_id:
			self._errors["venmo_id"] = self.error_class(["Venmo ID does not match token user's Venmo ID"])

		return cleaned_data

class PaymentForm(forms.Form):
	amount = forms.IntegerField()
	task_id = forms.IntegerField()

	def clean_task_id(self):
		task_id = self.cleaned_data["task_id"]
		if not Task.objects.filter(pk=task_id).exists():
			raise forms.ValidationError("That id doesn't belong to any task.")
		return task_id

	def clean_amount(self):
		amount = self.cleaned_data["amount"]
		if amount > 0:
			return amount
		else:
			raise forms.ValidationError("Amount must be greater than 0.")
			return amount
