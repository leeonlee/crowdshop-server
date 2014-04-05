import json
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
<<<<<<< HEAD
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
=======
from rest_framework import viewsets
from crowdshop.models import Task
from crowdshop.serializers import UserSerializer, TaskSerializer
from django.contrib.auth.models import User
from rest_framework import generics
>>>>>>> models

# Create your views here.
def index(request):
	return render_to_response("crowdshop/index.html", RequestContext(request))

<<<<<<< HEAD
def login(request):
	results = {'success':'invalid'}
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					results['success'] = 'success'
				else:
					results['success'] = 'validate'

	response = json.dumps(results)
	return HttpResponse(response, content_type='application/json')
=======
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
>>>>>>> models
