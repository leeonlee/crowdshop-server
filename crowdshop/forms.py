from django.forms import ModelForm
from crowdshop.models import Task, MyUser
from django import forms

class TaskForm(ModelForm):
    owner = forms.ModelChoiceField(queryset=MyUser.objects.all(), to_field_name="venmo_id")
    class Meta:
        model = Task
        fields = ["owner", "title", "desc", "threshold", "reward",]

class ClaimForm(forms.Form):
    venmo_id = forms.CharField()
    token_venmo_id = forms.CharField()
    owner_venmo_id = forms.CharField()

    def clean(self):
        cleaned_data = super(ClaimForm, self).clean()
        venmo_id = cleaned_data.get("venmo_id", None)
        token_id = cleaned_data.get("token_venmo_id", None)
        owner_id = cleaned_data.get("owner_venmo_id", None)

        if not venmo_id or not token_id:
            return cleaned_data

        if venmo_id != token_id:
            self._errors["venmo_id"] = self.error_class(["Venmo ID does not match token user's Venmo ID."])

        if venmo_id == owner_id:
            self._errors["venmo_id"] = self.error_class(["Cannot claim your own tasks."])

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
