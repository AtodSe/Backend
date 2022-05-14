from rest_framework.serializers import ModelSerializer

from .models import Transaction


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'color', 'icon', 'name', 'price', 'transaction_at', 'created_at', 'updated_at']
        read_only_fields = ['updated_at', 'created_at']
