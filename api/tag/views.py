from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from .serializers import TagSerializer
from ..invoice.models import Invoice

class TagViewset(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TagSerializer


    def perform_create(self, serializer):
        invoice_id = self.kwargs.get('invoice_id')
        serializer.save(invoice_id=invoice_id)


    def get_queryset(self):
        invoice_id = self.kwargs.get('invoice_id')
        try:
            return Invoice.objects.get(id=invoice_id).tags.all()
        except Invoice.DoesNotExist:
            raise NotFound({'invoice': 'not found'})
