# Generated by Django 5.0 on 2024-02-22 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_alter_applicationtoken_application_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clickdetails',
            name='tx_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='clickdetails',
            name='tx_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='clicksummary',
            name='tx_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='sessions',
            name='tx_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='sessions',
            name='tx_time',
            field=models.TimeField(),
        ),
    ]
