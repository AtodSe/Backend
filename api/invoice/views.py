from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


from .serializers import InvoiceSerializer
from ..transaction.models import Transaction
from ..transaction.serializers import TransactionSerializer

class InvoiceViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = InvoiceSerializer


    @action(methods=['get'], detail=True, serializer_class=TransactionSerializer)
    def transactions(self, request, *args, **kwargs):
        invoice = self.get_object()
        queryset = Transaction.objects.filter(reminder__in=invoice.reminders.all())

        has_tag = request.GET.get('has_tag', None)
        if has_tag:
            has_tag = has_tag.split(',')
            queryset = queryset.filter(tags__in=has_tag).distinct()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def perform_destroy(self, instance):
        for reminder in instance.reminders.all():
            for transaction in reminder.transactions.all():
                transaction.delete()
            reminder.delete()
        instance.delete()


    def get_queryset(self):
        user = self.request.user
        return user.invoices.all()
