from django.contrib.auth.models import User
from crowdshop.models import Task
from rest_framework import serializers

class TaskListSerializer(serializers.ModelSerializer):
	owner = serializers.SlugRelatedField(many=False, slug_field='username')	
	class Meta:
		model = Task
		fields = ('owner', 'title', 'id', 'desc', 'reward', 'timeStamp')

class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		fields = ('owner', 'title', 'id', 'desc', 'threshold', 'actual_price', 'reward', 'timeStamp')

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name')

class UserDetailSerializer(serializers.ModelSerializer):
	tasks = TaskSerializer(many=True)
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name', 'tasks')
