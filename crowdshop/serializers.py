from django.contrib.auth.models import User
from crowdshop.models import Task
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name')

class TaskSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Task
		fields = ('owner', 'title', 'id', 'desc', 'threshold', 'actual_price', 'reward', 'complete', 'timeStamp', 'claimed_by')
		depth = 1

