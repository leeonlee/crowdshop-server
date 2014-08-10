from django.forms import ModelForm
from crowdshop.models import Task, MyUser
from django import forms

class TaskForm(ModelForm):
    owner = forms.ModelChoiceField(queryset=MyUser.objects.all(), to_field_name="venmo_id")
    token_id = forms.CharField()
    class Meta:
        model = Task
        fields = ["owner", "title", "desc", "threshold", "reward",]

    def clean(self):
        cleaned_data = super(TaskForm, self).clean()
        if any(self.errors):
            return cleaned_data

        owner = cleaned_data.get("owner")
        token_id = cleaned_data.get("token_id")
        if owner.venmo_id != token_id:
            self._errors["owner"] = self.error_class(["You cannot create tasks for other users"])

        return cleaned_data

class MasterForm(forms.Form):
    """
    Form for the update methods to use since they will all require at least these fields
    Also provides default clean method where it checks the token id against the passed venmo id
    venmo_id - venmo id passed in by client to be matched against token id
    token_id - venmo id found from token passed by client
    task - task to update
    """
    venmo_id = forms.CharField()
    token_venmo_id = forms.CharField()
    task = forms.ModelChoiceField(queryset=Task.objects.all())

    def get_default_fields(self, cleaned_data):
        """
        Return the venmo_id and owner_id field from the cleaned data, respectively
        """
        venmo_id = cleaned_data.get("venmo_id")
        owner_id = cleaned_data.get("task").owner.venmo_id
        return venmo_id, owner_id

    def clean(self):
        cleaned_data = super(MasterForm, self).clean()
        venmo_id, owner_id = self.get_default_fields(cleaned_data)
        token_id = cleaned_data.get("token_venmo_id")
        if any(self.errors):
            return

        if venmo_id != token_id:
            print venmo_id, token_id
            self._errors["venmo_id"] = self.error_class(["Venmo ID does not match token user's Venmo ID."])

        return cleaned_data

class ClaimForm(MasterForm):
    """
    Allows a user other than the owner to claim a task
    """
    def clean(self):
        if any(self.errors):
            return
        cleaned_data = super(ClaimForm, self).clean()
        venmo_id, owner_id = self.get_default_fields(cleaned_data)

        if venmo_id == owner_id:
            self._errors["venmo_id"] = self.error_class(["Cannot claim your own tasks."])

        return cleaned_data
class PayForm(MasterForm):
    """
    Allows the claimer to enter the amount they paid for the task
    paid - amount paid by claimer 
    """
    paid = forms.IntegerField(min_value=0)
    def clean(self):
        if any(self.errors):
            return

        cleaned_data = super(PayForm, self).clean()
        task = cleaned_data.get("task")
        venmo_id, owner_id = self.get_default_fields(cleaned_data)

        if task.claimed_by.venmo_id != venmo_id:
            self._errors["task"] = self.error_class(["You did not claim this task."])

        return cleaned_data

class ResolveForm(MasterForm):
    """
    Resolves a task, meaning it has been complete
    """
    def clean(self):
        if any(self.errors):
            return
        cleaned_data = super(ResolveForm, self).clean()
        venmo_id, owner_id = self.get_default_fields(cleaned_data)

        if venmo_id != owner_id:
            self._errors["venmo_id"] = self.error_class(["Only the owner of the task can resolve it."])
            
        return cleaned_data
