import json
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from crowdshop.models import Task
from crowdshop.serializers import UserListSerializer, UserDetailSerializer, TaskDetailSerializer, TaskListSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.conf import settings
from django.http import Http404
import requests

def index(request):
	if request.method != "GET":
		raise Http404

	code = request.GET.get("code", "")
	if not code: raise Http404
	data = {
		"client_id" : settings.APP_ID,
		"client_secret" : settings.APP_SECRET,
		"code" : code,
	}

	response = requests.post(settings.VENMO_URL, data).json()
	print settings.APP_ID
	print settings.APP_SECRET
	print response
	token = json.dumps(response["access_token"])
	return HttpResponse(token, content_type='application/json')

@api_view(('GET',))
def api_root(request, format=None):
	return Response({
		'users': reverse('userlist', request=request, format=format),
		'tasks': reverse('tasklist', request=request, format=format),
	})

class UserList(generics.ListCreateAPIView):
	queryset = User.objects.all()
	paginate_by = 10
	serializer_class = UserListSerializer

class UserDetail(generics.RetrieveAPIView):
	paginate_by = 10
	queryset = User.objects.all()
	serializer_class = UserDetailSerializer

class UserTasks(generics.ListAPIView):
	paginate_by = 10
	serializer_class = TaskListSerializer

	def get_queryset(self):
		username = self.kwargs['username']
		owner = User.objects.get(username=username)
		return Task.objects.filter(owner=owner)

class TaskList(generics.ListCreateAPIView):
	paginate_by = 10
	def get_queryset(self):
		queryset = Task.objects.all()
		id_filter = self.request.QUERY_PARAMS.get('id', None)
		username = self.request.QUERY_PARAMS.get('username', None)
		exclude_user = self.request.QUERY_PARAMS.get('exclude_user', None)
		exclude_id = self.request.QUERY_PARAMS.get('exclude_id', None)
		claimed = self.request.QUERY_PARAMS.get('claimed', None)
		claimed_by_user = self.request.QUERY_PARAMS.get('claimed_by_user', None)
		claimed_by_id = self.request.QUERY_PARAMS.get('claimed_by_id', None)
		
		if id_filter is not None:
			queryset = queryset.filter(owner = User.objects.get(id=id_filter))

		if username is not None:
			queryset = queryset.filter(owner = User.objects.get(username=username))

		if exclude_user is not None:
			queryset = queryset.exclude(owner = User.objects.get(username=exclude_user))

		if exclude_id is not None:
			queryset = queryset.exclude(owner = User.objects.get(id=exclude_id))

		if claimed is not None:
			if claimed == "false":
				queryset = queryset.filter(claimed_by_user = None)
			elif claimed == "true":
				queryset = queryset.exclude(claimed_by_user = None)

		if claimed_by_user is not None:
			queryset = queryset.filter(claimed_by = User.objects.get(username=claimed_by_user))

		if claimed_by_id is not None:
			queryset = queryset.filter(claimed_by = User.objects.get(id=claimed_by_id))

		return queryset

	serializer_class = TaskListSerializer

class TaskDetail(generics.RetrieveAPIView):
	paginate_by = 10
	queryset = Task.objects.all()
	serializer_class = TaskDetailSerializer

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
				'reward': task.reward,
				'complete': task.complete,
				'timeStamp': task.timeStamp.isoformat(),
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



'''
@api_view(('POST',))
def claimTask(request):	
	results = {'success':'invalid'}
	print request.POST.get("message")
	return Response({"message": "Hello world"})

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
	serializer_class = UserListSerializer

class TaskViewSet(viewsets.ModelViewSet):
	"""
	API endpoint that allows tasks to be viewed or edited
	"""
	queryset = Task.objects.all()
	serializer_class = TaskDetailSerializer

class TaskList(generics.ListAPIView):
	serializer_class = TaskDetailSerializer
	def get_queryset(self):
		return Task.objects.filter(claimed_by=None)

class OpenTasks(generics.ListAPIView):
	serializer_class = TaskDetailSerializer
	def get_queryset(self):
		username = self.kwargs['username']
		owner = User.objects.get(username = username)
		return Task.objects.filter(claimed_by=None).exclude(owner = owner)

class RequestedTasks(generics.ListAPIView):
	serializer_class = TaskDetailSerializer
	def get_queryset(self):
		username = self.kwargs['username']
		owner = User.objects.get(username = username)
		return Task.objects.filter(owner = owner)

class ClaimedTasks(generics.ListAPIView):
	serializer_class = TaskDetailSerializer
	def get_queryset(self):
		username = self.kwargs['username']
		owner = User.objects.get(username = username)
		return Task.objects.filter(claimed_by = owner)

'''
