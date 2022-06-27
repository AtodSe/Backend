from django.core.validators import RegexValidator
from django.db import models
from django.utils.timezone import now

from ..reminder.models import Reminder
from ..tag.models import Tag
from core.models import SoftDeleteModel

class Transaction(SoftDeleteModel):
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE, related_name='transactions')
    name = models.CharField(max_length=32, null=False, blank=False)
    icon = models.CharField(max_length=7, default='i000000', validators=[RegexValidator(regex=r'^i[0-9]{6}$', message='icon must be in this format ixxxxxx', code='icon_regex')])
    color = models.CharField(max_length=7, default='#070707', validators=[RegexValidator(regex=r'^#([0-9a-fA-F]{2}){3}$', message='color must be in this format #xxxxxx', code='hex_regex')])
    price = models.BigIntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True, related_name='transactions')
    transaction_at = models.DateTimeField(default=now)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)  
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'transactions'
