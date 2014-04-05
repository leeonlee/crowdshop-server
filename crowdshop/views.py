from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets
from crowdshop.models import Task
from crowdshop.serializers import UserSerializer, TaskSerializer
from django.contrib.auth.models import User
from rest_framework import generics

# Create your views here.
def index(request):
	return render_to_response("crowdshop/index.html", RequestContext(request))

class UserViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows users to be viewed or edited
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer

class TaskViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows tasks to be viewed or edited
	"""
	queryset = Task.objects.all()
	serializer_class = TaskSerializer

class TaskList(generics.ListAPIView):
	serializer_class = TaskSerializer

	def get_queryset(self):
		return Task.objects.filter(claimed_by=None)
