from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth import get_user_model

from core.models import SoftDeleteModel

class Invoice(SoftDeleteModel):
    DEFAULT_INVOICE_TAGS = ({
            "name": "خوراک",
            "color": "#FFAE34",
            "icon": "i000001"
        },
        {
            "name": "وسایل نقلیه",
            "color": "#8371F1",
            "icon": "i000002"
        },
        {
            "name": "درمان",
            "color": "#64C7FF",
            "icon": "i000003"
        },
        {
            "name": "بهداشت",
            "color": "#FF819F",
            "icon": "i000004"
        },
        {
            "name": "تحصیلات",
            "color": "#FF9F47",
            "icon": "i000005"
        },
        {
            "name": "حقوق",
            "color": "#BA76EF",
            "icon": "i000006"
        },
        {
            "name": "پوشاک",
            "color": "#9BC93A",
            "icon": "i000007"
        },
        {
            "name": "ورزش",
            "color": "#49A8FF",
            "icon": "i000008"
        },
        {
            "name": "خوار و بار",
            "color": "#34B969",
            "icon": "i000009"
        },
        {
            "name": "سایر",
            "color": "#FF607C",
            "icon": "i000010"
        }
    )

    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='invoices')
    name = models.CharField(max_length=32, null=False)
    color = models.CharField(max_length=7, default='#070707', validators=[RegexValidator(regex=r'^#([0-9a-fA-F]{2}){3}$', message='color must be in this format #xxxxxx', code='hex_regex')])
    balance = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)   
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'invoices'
