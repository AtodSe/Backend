# Generated by Django 4.0.3 on 2022-05-29 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='todo',
            field=models.TextField(blank=True),
        ),
    ]
