from crowdshop.models import Task, MyUser
from rest_framework import serializers
class UserListSerializer(serializers.HyperlinkedModelSerializer):
	"""
	Serializer for displaying user's information
	"""
	class Meta:
		model = MyUser
		fields = ('url', 'id', 'username', 'first_name', 'last_name')

class TaskDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying details of a task
    """
    owner = UserListSerializer(many=False)
    claimed_by = UserListSerializer(many=False)
    state = serializers.SlugRelatedField(many=False, slug_field="name")
    class Meta:
        model = Task
        fields = ('owner', 'title', 'id', 'desc', 'threshold', 'paid', 'reward', 'timeStamp', 'claimed_by', "state")
        depth = 1

class UserTaskDetailSerializer(serializers.HyperlinkedModelSerializer):
    """
    Displays all of a user's tasks
    """
    class Meta:
        model = Task
        fields = ('title', 'id', 'url')

class UserDetailSerializer(serializers.ModelSerializer):
    """
    Display details of a user
    """
    tasks = UserTaskDetailSerializer(many=True)
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'first_name', 'last_name', 'tasks')
