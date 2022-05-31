from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.db.models import Sum

from .models import Reminder


class ReminderSerializer(ModelSerializer):
    spent_percentage = SerializerMethodField()

    class Meta:
        model = Reminder
        fields = ['id', 'color', 'icon', 'name', 'balance', 'todo', 'spent_percentage', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['updated_at', 'created_at']

    def get_spent_percentage(self, reminder):
        return reminder.transactions.aggregate(Sum('price', default=0))['price__sum'] / reminder.balance * -100.0
