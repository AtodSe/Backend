from rest_framework.routers import DefaultRouter

from .views import InvoiceViewSet
from ..tag.views import TagViewset
from ..reminder.views import ReminderViewset
from ..transaction.views import TransactionViewset

router = DefaultRouter()
router.register(r'', InvoiceViewSet, basename='invoices')
router.register(r'(?P<invoice_id>\d+)/tags', TagViewset, basename='invoice-tags')
router.register(r'(?P<invoice_id>\d+)/reminders', ReminderViewset, basename='invoice-reminders')
router.register(r'(?P<invoice_id>\d+)/reminders/(?P<reminder_id>\d+)/transactions', TransactionViewset, basename='invoice-reminder-transactions')

urlpatterns = router.urls

urlpatterns += []
