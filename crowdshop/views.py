import json
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from crowdshop.models import Task, State, MyUser
from crowdshop.serializers import UserDetailSerializer, UserDetailSerializer, TaskDetailSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import renderers, generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.conf import settings
from crowdshop.forms import TaskForm, PayForm, ClaimForm
import workflow
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response

@api_view(["GET"])
def auth(request):
    code = request.GET["code"]

    data = {
        "client_id" : settings.APP_ID,
        "client_secret" : settings.APP_SECRET,
        "code" : code,
    }

    response = requests.post(settings.VENMO_URL, data).json()
    if not response.has_key("error"):
        email = response["user"]["email"]
        venmo_id = response["user"]["id"]
        first_name = response["user"]["first_name"]
        last_name = response["user"]["last_name"]
        username = response["user"]["username"]

        user, created = MyUser.objects.get_or_create(venmo_id = venmo_id)
        token, created = Token.objects.get_or_create(user=user)

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        response["crowdshop_token"] = token.key

        results = json.dumps(response)
        return HttpResponse(results, content_type="application/json")

@api_view(("POST",))
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated,))
def claim_task(request):
    form = ClaimForm(request.POST)
    if form.is_valid():
        user = request.user
        task = Task.objects.get(form.cleaned_data["task_id"])

        if user == task.owner:
            return Response({"errors": "Cannot claim your own tasks"}, status = status.HTTP_400_BAD_REQUEST)

        if task.state.name == "Open":
            task.claimed_by = user
            task.state = task.state.next_state
            task.save()

            return Response({}, status = status.HTTP_200_OK)

        else:
            return Response({"errors": "Task already claimed"}, status = status.HTTP_400_BAD_REQUEST)
    else:
        return Response(form.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(("POST",))
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated,))
def pay_task(request):
    user = request.user
    form = PaymentForm(request.POST)

    if form.is_valid():
        task = Task.objects.get(pk = form.cleaned_data["task_id"])
        amount = form.cleaned_data["amount"]
        if task.state.name != "Claimed":
            return Response({"errors": "This task cannot be paid for right now."}, status = status.HTTP_400_BAD_REQUEST)

        if task.claimed_by != user:
            return Response({"errors": "You did not claim this task."}, status = status.HTTP_400_BAD_REQUEST)

        task.actual_price = amount
        task.state = task.state.next_state
        task.save()
        return Response({}, status = status.HTTP_200_OK)

    else:
        return Response(form.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(("GET",))
def index(request):
    return HttpResponse("hi")

@api_view(('GET',))
def api_root(request, format=None):
        print request.user
        print request.auth
	return Response({
		'users': reverse('userlist', request=request, format=format),
		'tasks': reverse('tasks', request=request, format=format),
	})

class UserList(generics.ListCreateAPIView):
	queryset = MyUser.objects.all()
	paginate_by = 10
	serializer_class = UserDetailSerializer

class UserDetail(generics.RetrieveAPIView):
	paginate_by = 10
	queryset = MyUser.objects.all()
	serializer_class = UserDetailSerializer

"""
class UserTasks(generics.ListAPIView):
	paginate_by = 10
	serializer_class = TaskListSerializer

	def get_queryset(self):
		username = self.kwargs['username']
		owner = User.objects.get(username=username)
		return Task.objects.filter(owner=owner)
"""

#@authentication_classes((TokenAuthentication, ))
#@permission_classes((IsAuthenticated,))
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer

    def create(self, request):
        form = TaskForm(request.DATA)
        if form.is_valid():
            task = form.save(commit=False)
            task.state = State.objects.get(name="Open")
            task.save()
            serializer = TaskDetailSerializer(task)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        task = self.get_object()
        user = request.user
        token_id = user.venmo_id
        data = request.DATA.copy()
        data["token_venmo_id"] = token_id
        data["owner_venmo_id"] = task.owner.venmo_id
        data["task"] = pk

        if task.state.name == "Open":
            form = ClaimForm(data)
            if form.is_valid():
                task.claimed_by = user
                task.state = task.state.next_state
                task.save()
                serializer = TaskDetailSerializer(task)
                return Response(serializer.data)
            else:
                return Response(form.errors, status = status.HTTP_400_BAD_REQUEST)

        elif task.state.name == "Claimed":
            form = PayForm(data)
            if form.is_valid():
                task.actual_price = form.cleaned_data["amount"]
                task.state = task.state.next_state
                task.save()
                serializer = TaskDetailSerializer(task)
                return Response(serializer.data)
            else:
                return Response(form.errors, status = status.HTTP_400_BAD_REQUEST)

'''
class Tasks(generics.ListCreateAPIView):
    paginate_by = 10
    def create(request, *args, **kwargs):
        print request
        print kwargs
        print args[0].__dict__
        print args[0].POST
        return Http404

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
'''
