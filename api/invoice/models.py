from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth import get_user_model

from core.models import SoftDeleteModel

class Invoice(SoftDeleteModel):
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='invoices')
    name = models.CharField(max_length=32, null=False)
    color = models.CharField(max_length=7, default='#070707', validators=[RegexValidator(regex=r'^#([0-9a-fA-F]{2}){3}$', message='color must be in this format #xxxxxx', code='hex_regex')])
    balance = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)   
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'invoices'
