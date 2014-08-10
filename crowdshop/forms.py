from django.forms import ModelForm
from crowdshop.models import Task, MyUser
from django import forms

class TaskForm(ModelForm):
    owner = forms.ModelChoiceField(queryset=MyUser.objects.all(), to_field_name="venmo_id")
    class Meta:
        model = Task
        fields = ["owner", "title", "desc", "threshold", "reward",]

class ClaimForm(forms.Form):
    """
    venmo_id - venmo_id passed in by client
    token_venmo_id - venmo_id found from the token passed in by client
    owner_veno_mid - tasks's owner's venmo id
    """
    venmo_id = forms.CharField()
    token_venmo_id = forms.CharField()
    owner_venmo_id = forms.CharField()

    def clean(self):
        if any(self.errors):
            return
        cleaned_data = super(ClaimForm, self).clean()
        venmo_id = cleaned_data.get("venmo_id")
        token_id = cleaned_data.get("token_venmo_id")
        owner_id = cleaned_data.get("owner_venmo_id")

        if not venmo_id or not token_id:
            return cleaned_data

        if venmo_id != token_id:
            self._errors["venmo_id"] = self.error_class(["Venmo ID does not match token user's Venmo ID."])

        if venmo_id == owner_id:
            self._errors["venmo_id"] = self.error_class(["Cannot claim your own tasks."])

        return cleaned_data
class PayForm(forms.Form):
    """
    amount - amount paid by claimer 
    venmo_id - venmo_id passed by client
    token_venmo_id - venmo_id found in token
    task - task to be edited
    """
    amount = forms.IntegerField(min_value=0)
    token_venmo_id = forms.CharField()
    venmo_id = forms.CharField()
    task = forms.ModelChoiceField(queryset=Task.objects.all())

    def clean(self):
        if any(self.errors):
            return

        cleaned_data = super(PayForm, self).clean()
        venmo_id = cleaned_data.get("venmo_id")
        token_venmo_id = cleaned_data.get("token_venmo_id")
        task = cleaned_data.get("task")

        if venmo_id != token_venmo_id:
            self._errors["venmo_id"] = self.error_class(["Venmo ID does not match token user's Venmo ID."])

        if task.claimed_by.venmo_id != venmo_id:
            self._errors["task"] = self.error_class(["You did not claim this task"])

        return cleaned_data
