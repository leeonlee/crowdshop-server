import json
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from crowdshop.models import Task
from crowdshop.serializers import UserSerializer, TaskSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
	return render_to_response("crowdshop/index.html", RequestContext(request))

@csrf_exempt
def loginview(request):
	results = {'success':'invalid'}
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				results['success'] = 'success'
				results['id'] = user.id
				results['username'] = user.username
				results['first_name'] = user.first_name
				results['last_name'] = user.last_name

	response = json.dumps(results)
	return HttpResponse(response, content_type='application/json')

@csrf_exempt
def createTask(request):
	results = {'success':'invalid'}
	if request.method == 'POST':
			username = request.POST.get('username')
			title = request.POST.get('title')
			desc = request.POST.get('desc')
			threshold = request.POST.get('threshold')
			reward = request.POST.get('reward')
			task = Task.objects.create(
				owner = User.objects.get(username = username),
				title = title,
				desc = desc, 
				threshold = threshold,
				reward = reward,
			)
			results = {
				'success':'success',
				'owner': task.owner.username,
				'id': task.id,
				'title': task.title,
				'desc': task.desc,
				'threshold': task.threshold,
				'reward': reward,
			}
	response = json.dumps(results)
	return HttpResponse(response, content_type='application/json')

@csrf_exempt
def claimTask(request):
	results = {'success':'invalid'}
	if request.method == 'POST':
			task_id = request.POST.get('task_id')
			claimed_by = request.POST.get('username')
			claimee = User.objects.get(username = claimed_by)
			task = Task.objects.get(id = task_id)
			task.claimed_by = claimee
			task.save()
			results = {
				'success':'success',
			}
	response = json.dumps(results)
	return HttpResponse(response, content_type='application/json')

@csrf_exempt
def confirmPurchase(request):
	results = {'success':'invalid'}
	if request.method == 'POST':
			task_id = request.POST.get('task_id')
			actual_price = request.POST.get('actual_price')
			task = Task.objects.get(id = task_id)
			if int(actual_price) > task.threshold:
				pass
			else:
				task.actual_price = actual_price
				task.save()
				results = {
					'success': 'success',
				}
	response = json.dumps(results)
	return HttpResponse(response, content_type='application/json')

@csrf_exempt
def completeDeal(request):
	results = {'success':'invalid'}
	if request.method == 'POST':
			task_id = request.POST.get('task_id')
			task = Task.objects.get(id = task_id)
			task.complete = True
			task.save()
			results = {
				'success':'success',
			}
	response = json.dumps(results)
	return HttpResponse(response, content_type='application/json')

def venmoWebHook(request):
	response = request.GET.get('venmo_challenge')
	# results = {'success':'invalid', 'venmo_challenge': venmo}
	# response = json.dumps(results)
	return HttpResponse(response, content_type='text/plain')

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

class OpenTasks(generics.ListAPIView):
	serializer_class = TaskSerializer
	def get_queryset(self):
		username = self.kwargs['username']
		owner = User.objects.get(username = username)
		return Task.objects.filter(claimed_by=None).exclude(owner = owner)

class RequestedTasks(generics.ListAPIView):
	serializer_class = TaskSerializer
	def get_queryset(self):
		username = self.kwargs['username']
		owner = User.objects.get(username = username)
		return Task.objects.filter(owner = owner)

class ClaimedTasks(generics.ListAPIView):
	serializer_class = TaskSerializer
	def get_queryset(self):
		username = self.kwargs['username']
		owner = User.objects.get(username = username)
		return Task.objects.filter(claimed_by = owner)


