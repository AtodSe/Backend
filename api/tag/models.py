from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth import get_user_model

from ..invoice.models import Invoice
from core.models import SoftDeleteModel

class Tag(SoftDeleteModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=32, null=False, blank=False)
    icon = models.CharField(max_length=7, default='i000000', validators=[RegexValidator(regex=r'^i[0-9]{6}$', message='icon must be in this format ixxxxxx', code='icon_regex')])
    color = models.CharField(max_length=7, default='#070707', validators=[RegexValidator(regex=r'^#([0-9a-fA-F]{2}){3}$', message='color must be in this format #xxxxxx', code='hex_regex')])
    created_at = models.DateTimeField(auto_now_add=True, editable=False)  
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'tags'
