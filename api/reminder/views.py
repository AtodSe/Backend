from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from .serializers import ReminderSerializer
from ..invoice.models import Invoice

class ReminderViewset(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReminderSerializer


    def perform_create(self, serializer):
        invoice_id = self.kwargs.get('invoice_id')
        serializer.save(invoice_id=invoice_id)


    def perform_destroy(self, instance):
        for transaction in instance.transactions.all():
            transaction.delete()
        instance.delete()


    def get_queryset(self):
        invoice_id = self.kwargs.get('invoice_id')
        try:
            return Invoice.objects.get(id=invoice_id).reminders.all()
        except Invoice.DoesNotExist:
            raise NotFound({'invoice': 'not found'})
