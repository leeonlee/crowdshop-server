from crowdshop.models import Task, MyUser
from rest_framework import serializers

class UserDetailSerializer(serializers.ModelSerializer):
	"""
	Serializer for displaying all users
	Also used to display brief information of a user
	"""
	class Meta:
		model = MyUser
		fields = ('venmo_id', 'username', 'first_name', 'last_name')


class TaskDetailSerializer(serializers.ModelSerializer):
	"""
	Serializer for displaying details of a task
	"""
	owner = UserDetailSerializer(many=False)
	claimed_by = UserDetailSerializer(many=False)
	class Meta:
		model = Task
		fields = ('owner', 'title', 'id', 'desc', 'threshold', 'actual_price', 'reward', 'timeStamp', 'claimed_by', "state")
        depth = 1

class UserTaskSerializer(serializers.ModelSerializer):
	"""
	Serializer for displaying all of a user's tasks
	Used to elminate redundancy in showing the owner's information
	"""
	claimed_by = UserDetailSerializer(many=False)
	class Meta:
		model = Task
		fields = ('title', 'id', 'desc', 'reward', 'timeStamp', 'claimed_by')

class UserDetailSerializer(serializers.ModelSerializer):
	"""
	Serializer for displaying user's information
	"""
	tasks = UserTaskSerializer(many=True)
	class Meta:
		model = MyUser
		fields = ('id', 'username', 'first_name', 'last_name', 'tasks')
