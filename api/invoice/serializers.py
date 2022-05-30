from rest_framework.serializers import ModelSerializer

from .models import Invoice
from ..tag.models import Tag


class InvoiceSerializer(ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'color', 'name', 'balance']

    def create(self, validated_data):
        validated_data.update({'creator': self.context['request'].user})
        invoice = super().create(validated_data=validated_data)
        Tag.objects.bulk_create([Tag(invoice=invoice, **default_tag) for default_tag in Invoice.DEFAULT_INVOICE_TAGS])
        return invoice
