# Generated by Django 4.1.5 on 2023-02-07 03:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_general', '0003_coursemodel_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coursemodel',
            name='image',
        ),
    ]
