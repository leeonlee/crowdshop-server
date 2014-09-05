import json
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets
from crowdshop.models import Task, State, MyUser
from crowdshop.serializers import UserDetailSerializer, UserListSerializer, TaskDetailSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import renderers, generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.conf import settings
from crowdshop.forms import TaskForm, PayForm, ClaimForm, ResolveForm
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

@api_view(("GET",))
def index(request):
    return HttpResponse("hi")

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('userlist', request=request, format=format),
        'tasks': reverse('tasks', request=request, format=format),
    })

class UserViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        else:
            return UserListSerializer
    queryset = MyUser.objects.all()
    serializer_class = UserListSerializer
    paginate_by = 10

@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated,))
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer

    def create(self, request):
        request.DATA["token_id"] = request.user.venmo_id
        print request.DATA
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
                task.paid = form.cleaned_data["paid"]
                task.state = task.state.next_state
                task.save()
                serializer = TaskDetailSerializer(task)
                return Response(serializer.data)
            else:
                return Response(form.errors, status = status.HTTP_400_BAD_REQUEST)

        elif task.state.name == "Paid":
            form = ResolveForm(data)
            if form.is_valid():
                task.state = task.state.next_state
                task.save()
                serializer = TaskDetailSerializer(task)
                return Response(serializer.data)
            else:
                return Response(form.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)
