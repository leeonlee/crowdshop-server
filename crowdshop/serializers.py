from django.contrib.auth.models import User
from crowdshop.models import Task
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username',)

class TaskSerializer(serializers.HyperlinkedModelSerializer):
	owner = serializers.RelatedField(many=False, read_only=True)
	class Meta:
		model = Task
		fields = ('owner', 'title', 'desc', 'threshold', 'timeStamp')
