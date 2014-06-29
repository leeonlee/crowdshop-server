from django.contrib import admin
from crowdshop.models import Task, State, Person

# Register your models here.
admin.site.register(Task)
admin.site.register(State)
admin.site.register(Person)
