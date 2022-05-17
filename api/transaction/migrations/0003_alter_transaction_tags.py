# Generated by Django 4.0.3 on 2022-05-17 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0003_alter_tag_icon'),
        ('transaction', '0002_transaction_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='tags',
            field=models.ManyToManyField(null=True, related_name='transactions', to='tag.tag'),
        ),
    ]
