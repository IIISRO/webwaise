# Generated by Django 4.1.7 on 2023-04-16 09:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=15, verbose_name='full name')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('order_amount', models.IntegerField(verbose_name='amount')),
                ('order_name', models.CharField(max_length=200, verbose_name='order name')),
                ('order_desc', models.TextField(verbose_name='order description')),
                ('is_payed', models.BooleanField(default=False, verbose_name='is payed')),
                ('is_done', models.BooleanField(default=False, verbose_name='is done')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('link', models.CharField(max_length=200, verbose_name='link')),
                ('review', models.TextField(verbose_name='review')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
