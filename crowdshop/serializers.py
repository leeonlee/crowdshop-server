from django.contrib.auth.models import User
from crowdshop.models import Task
from rest_framework import serializers

class TaskListSerializer(serializers.ModelSerializer):
	owner = serializers.SlugRelatedField(many=False, slug_field='username')	
	claimed_by = serializers.RelatedField(many=False)
	class Meta:
		model = Task
		fields = ('owner', 'title', 'id', 'desc', 'reward', 'timeStamp', 'claimed_by')

class TaskSerializer(serializers.ModelSerializer):
	owner = serializers.RelatedField(many=False)
	claimed_by = serializers.RelatedField(many=False)
	class Meta:
		model = Task
		fields = ('owner', 'title', 'id', 'desc', 'threshold', 'actual_price', 'reward', 'timeStamp', 'claimed_by')

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name')

class UserDetailSerializer(serializers.ModelSerializer):
	tasks = TaskSerializer(many=True)
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name', 'tasks')
