# Generated by Django 4.1.7 on 2023-04-17 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('webdevelopment', 'webdevelopment'), ('iosapp', 'iosapp'), ('androidapp', 'androidapp'), ('uiux', 'uiux'), ('logodesign', 'logodesign')], max_length=50, null=True),
        ),
    ]
