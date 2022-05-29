from rest_framework.serializers import ModelSerializer

from .models import Reminder


class ReminderSerializer(ModelSerializer):
    class Meta:
        model = Reminder
        fields = ['id', 'color', 'icon', 'name', 'balance', 'todo', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['updated_at', 'created_at']
