# Generated by Django 4.1.7 on 2023-04-18 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_order_deposit_alter_order_payed_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='deposit',
        ),
    ]
