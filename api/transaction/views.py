from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from .serializers import TransactionSerializer
from ..invoice.models import Invoice
from ..reminder.models import Reminder

class TransactionViewset(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer


    def perform_create(self, serializer):
        reminder_id = self.kwargs.get('reminder_id')
        serializer.save(reminder_id=reminder_id)


    def get_queryset(self):
        invoice_id = self.kwargs.get('invoice_id')
        reminder_id = self.kwargs.get('reminder_id')
        try:
            return Invoice.objects.get(id=invoice_id).reminders.get(id=reminder_id).transactions.all()
        except Invoice.DoesNotExist:
            raise NotFound({'invoice': 'not found'})
        except Reminder.DoesNotExist:
            raise NotFound({'reminder': 'not found'})
