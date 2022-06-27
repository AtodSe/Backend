from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField
from django.db.models import Sum
from django.utils.timezone import now, timedelta

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
        return Transaction.objects.filter(reminder__in=obj.reminders.all(), price__gte=0).aggregate(Sum('price', default=0))['price__sum']


    def get_total_spent(self, obj):
        return -Transaction.objects.filter(reminder__in=obj.reminders.all(), price__lt=0).aggregate(Sum('price', default=0))['price__sum']


    def create(self, validated_data):
        validated_data.update({'creator': self.context['request'].user})
        invoice = super().create(validated_data=validated_data)
        Tag.objects.bulk_create([Tag(invoice=invoice, **default_tag) for default_tag in Invoice.DEFAULT_INVOICE_TAGS])
        return invoice


class InvoiceStatisticsSerializer(ModelSerializer):
    PERSIAN_WEEK_DAYS = [
        None,
        'ی',
        'د',
        'س',
        'چ',
        'پ',
        'ج',
        'ش'
    ]
    weekly_spent_and_gain = SerializerMethodField()

    class Meta:
        model = Invoice
        fields = ['weekly_spent_and_gain']

    def get_weekly_spent_and_gain(self, invoice):
        queryset = Transaction.objects.filter(
                reminder__in=invoice.reminders.all(),
                transaction_at__gte=now() - timedelta(days=7)
                ).values('transaction_at__week_day')
        spent_queryset = queryset.all().filter(price__lt=0).annotate(total=Sum('price')).all()
        gain_queryset = queryset.all().filter(price__gte=0).annotate(total=Sum('price')).all()
        weekly_spent = { spent['transaction_at__week_day']:spent['total'] for spent in spent_queryset}
        weekly_gain = { gain['transaction_at__week_day']:gain['total'] for gain in gain_queryset }
        return { 
                self.PERSIAN_WEEK_DAYS[day]: {
                    'gain': weekly_gain.get(day, 0),
                    'spent': -weekly_spent.get(day,0)
                } for day in range(1,8)
            }
