from django.forms import ModelForm
from crowdshop.models import Task

class TaskForm(ModelForm):
	class Meta:
		model = Task
		fields = [
			"title",
			"desc",
			"threshold",
			"reward",
			]
