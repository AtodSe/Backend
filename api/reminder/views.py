from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from .serializers import ReminderSerializer
from ..invoice.models import Invoice

class ReminderViewset(mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReminderSerializer


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        used_tag = request.GET.get('used_tag', None)

        if used_tag:
            used_tag = used_tag.split(',')
            queryset = queryset.filter(transactions__tags__in=used_tag).distinct()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
