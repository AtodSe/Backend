from rest_framework.serializers import ModelSerializer

from .models import Invoice


class InvoiceSerializer(ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'color', 'name', 'balance']

    def create(self, validated_data):
        validated_data.update({'creator': self.context['request'].user})
        return super().create(validated_data=validated_data)
