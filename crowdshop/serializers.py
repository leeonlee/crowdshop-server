from django.contrib.auth.models import User
from crowdshop.models import Task
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'first_name', 'last_name')

class TaskSerializer(serializers.HyperlinkedModelSerializer):
	owner = serializers.RelatedField(many=False, read_only=True)
	owner_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
	claimed_by = serializers.RelatedField(many=False, read_only=True)
	claimed_by_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

	class Meta:
		model = Task
		fields = ('owner', 'owner_id', 'title', 'desc', 'threshold', 'timeStamp', 'claimed_by', 'claimed_by_id')

