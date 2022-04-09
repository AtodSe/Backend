from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.permissions import IsAuthenticated

from .serializers import InvoiceSerializer

class InvoiceViewSet(mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        user = self.request.user
        return user.invoices.all()
