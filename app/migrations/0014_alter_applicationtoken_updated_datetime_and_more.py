# Generated by Django 5.0 on 2023-12-13 04:42


import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_applicationtoken_updated_datetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationtoken',
            name='updated_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='subscriptionhistory',
            name='subscribed_package',
            field=models.CharField(blank=True, choices=[('PREMIER', 'Premier Savings Plan'), ('ELITE', 'Elite Savings Plan'), ('ULTIMATE', 'Ultimate Savings Bundle')], default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='subscriptionhistory',
            name='updated_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='subscribed_package',
            field=models.CharField(blank=True, choices=[('PREMIER', 'Premier Savings Plan'), ('ELITE', 'Elite Savings Plan'), ('ULTIMATE', 'Ultimate Savings Bundle')], default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='updated_datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
