# Generated by Django 4.0.3 on 2022-04-09 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]