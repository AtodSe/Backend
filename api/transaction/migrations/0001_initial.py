# Generated by Django 4.0.3 on 2022-05-14 11:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reminder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(default=None, null=True)),
                ('name', models.CharField(max_length=32)),
                ('icon', models.CharField(default='i000000', max_length=7, validators=[django.core.validators.RegexValidator(code='icon_regex', message='icon must be in this format ixxxxxx', regex='^i[0-9]{6}$')])),
                ('color', models.CharField(default='#070707', max_length=7, validators=[django.core.validators.RegexValidator(code='hex_regex', message='color must be in this format #xxxxxx', regex='^#([0-9a-fA-F]{2}){3}$')])),
                ('price', models.BigIntegerField(default=0)),
                ('transaction_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reminder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='reminder.reminder')),
            ],
            options={
                'db_table': 'transactions',
                'managed': True,
            },
        ),
    ]
