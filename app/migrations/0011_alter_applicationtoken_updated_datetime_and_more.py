# Generated by Django 4.2.7 on 2023-12-10 23:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_applicationtoken_updated_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationtoken',
            name='updated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 10, 23, 23, 39, 53283, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='subscriptionhistory',
            name='updated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 10, 23, 23, 39, 53496, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='updated_datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 10, 23, 23, 39, 52747, tzinfo=datetime.timezone.utc)),
        ),
    ]
