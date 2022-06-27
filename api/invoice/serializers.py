from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField
from django.db.models import Sum

from .models import Invoice
from ..transaction.models import Transaction
from ..tag.models import Tag


class InvoiceSerializer(ModelSerializer):
    total_gain = SerializerMethodField()
    total_spent = SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ['id', 'color', 'name', 'balance', 'total_spent', 'total_gain']


    def get_total_gain(self, obj):
        return Transaction.objects.filter(reminder__in=obj.reminders.values('id'), price__gte=0).aggregate(Sum('price', default=0))['price__sum']


    def get_total_spent(self, obj):
        return -Transaction.objects.filter(reminder__in=obj.reminders.values('id'), price__lt=0).aggregate(Sum('price', default=0))['price__sum']


    def create(self, validated_data):
        validated_data.update({'creator': self.context['request'].user})
        invoice = super().create(validated_data=validated_data)
        Tag.objects.bulk_create([Tag(invoice=invoice, **default_tag) for default_tag in Invoice.DEFAULT_INVOICE_TAGS])
        return invoice
