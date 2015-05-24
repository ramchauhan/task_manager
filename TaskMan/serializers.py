from rest_framework import serializers

from TaskMan.models import Tasks


class TasksSerializer(serializers.ModelSerializer):
    dead_line_date = serializers.DateField(format=None, input_formats=None)
    class Meta:
        model = Tasks
        fields = ('id', 'user', 'task', 'created_date', 'dead_line_date', 'is_completed')

