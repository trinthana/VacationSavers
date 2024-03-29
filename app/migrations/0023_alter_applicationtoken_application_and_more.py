# Generated by Django 5.0 on 2024-02-22 09:57

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_clickdetails_tx_date_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationtoken',
            name='application',
            field=models.CharField(blank=True, choices=[('ACCESS', 'Access Development'), ('ACCESSIFRAME', 'Access Development Iframe'), ('ACCESSDEAL', 'Access Development Deals'), ('ARRIVIA', 'Arrivia Cruise'), ('EXPEDIA', 'Expedia'), ('BOOKING', 'Booking.com'), ('BEDSOPIA', 'Bedsopia'), ('YALAGO', 'Yalago'), ('WORLDIA', 'Worldia Car'), ('CRUISEWATCH', 'Cruisewatch'), ('CRUISEDIRECT', 'CruiseDirect'), ('DREAMLINES', 'Dreamlines'), ('CARTRAWLER', 'CarTrawler'), ('TOURRADAR', 'TourRadar'), ('GETYOURGUIDE', 'GetYourGuide'), ('GADVENGER', 'G Advengers'), ('TIMETOTICKET', 'Time To Ticket'), ('TICKETNETWORK', 'Ticket Network'), ('INTERLNKD', 'InterLNKD'), ('GLOBATECH', 'GlobalTech'), ('TALIXO', 'Talixo'), ('WELCOME', 'Welcome Pick Ups'), ('TRANSFERZ', 'Transferz'), ('HOLIBOB', 'Holibob'), ('SERVANTRIP', 'Servantrip'), ('NEZASA', 'Nezasa'), ('GTN', 'GTN Vacation Rental'), ('VSFLIGHT', 'VacationSavers Flight'), ('DUNHILL', 'DUNHILL Special Deals')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='clickdetails',
            name='application',
            field=models.CharField(blank=True, choices=[('ACCESS', 'Access Development'), ('ACCESSIFRAME', 'Access Development Iframe'), ('ACCESSDEAL', 'Access Development Deals'), ('ARRIVIA', 'Arrivia Cruise'), ('EXPEDIA', 'Expedia'), ('BOOKING', 'Booking.com'), ('BEDSOPIA', 'Bedsopia'), ('YALAGO', 'Yalago'), ('WORLDIA', 'Worldia Car'), ('CRUISEWATCH', 'Cruisewatch'), ('CRUISEDIRECT', 'CruiseDirect'), ('DREAMLINES', 'Dreamlines'), ('CARTRAWLER', 'CarTrawler'), ('TOURRADAR', 'TourRadar'), ('GETYOURGUIDE', 'GetYourGuide'), ('GADVENGER', 'G Advengers'), ('TIMETOTICKET', 'Time To Ticket'), ('TICKETNETWORK', 'Ticket Network'), ('INTERLNKD', 'InterLNKD'), ('GLOBATECH', 'GlobalTech'), ('TALIXO', 'Talixo'), ('WELCOME', 'Welcome Pick Ups'), ('TRANSFERZ', 'Transferz'), ('HOLIBOB', 'Holibob'), ('SERVANTRIP', 'Servantrip'), ('NEZASA', 'Nezasa'), ('GTN', 'GTN Vacation Rental'), ('VSFLIGHT', 'VacationSavers Flight'), ('DUNHILL', 'DUNHILL Special Deals')], default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='clickdetails',
            name='http_headers',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='clickdetails',
            name='remote_addr',
            field=models.CharField(blank=True, default='', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='clickdetails',
            name='remote_host',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='clickdetails',
            name='tx_date',
            field=models.DateField(default=datetime.date(2024, 2, 22)),
        ),
        migrations.AlterField(
            model_name='clickdetails',
            name='tx_time',
            field=models.TimeField(default=datetime.time(9, 57, 53, 718807)),
        ),
        migrations.AlterField(
            model_name='clickdetails',
            name='tx_url',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='clicksummary',
            name='application',
            field=models.CharField(blank=True, choices=[('ACCESS', 'Access Development'), ('ACCESSIFRAME', 'Access Development Iframe'), ('ACCESSDEAL', 'Access Development Deals'), ('ARRIVIA', 'Arrivia Cruise'), ('EXPEDIA', 'Expedia'), ('BOOKING', 'Booking.com'), ('BEDSOPIA', 'Bedsopia'), ('YALAGO', 'Yalago'), ('WORLDIA', 'Worldia Car'), ('CRUISEWATCH', 'Cruisewatch'), ('CRUISEDIRECT', 'CruiseDirect'), ('DREAMLINES', 'Dreamlines'), ('CARTRAWLER', 'CarTrawler'), ('TOURRADAR', 'TourRadar'), ('GETYOURGUIDE', 'GetYourGuide'), ('GADVENGER', 'G Advengers'), ('TIMETOTICKET', 'Time To Ticket'), ('TICKETNETWORK', 'Ticket Network'), ('INTERLNKD', 'InterLNKD'), ('GLOBATECH', 'GlobalTech'), ('TALIXO', 'Talixo'), ('WELCOME', 'Welcome Pick Ups'), ('TRANSFERZ', 'Transferz'), ('HOLIBOB', 'Holibob'), ('SERVANTRIP', 'Servantrip'), ('NEZASA', 'Nezasa'), ('GTN', 'GTN Vacation Rental'), ('VSFLIGHT', 'VacationSavers Flight'), ('DUNHILL', 'DUNHILL Special Deals')], default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='clicksummary',
            name='tx_date',
            field=models.DateField(default=datetime.date(2024, 2, 22)),
        ),
        migrations.CreateModel(
            name='Sessions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(max_length=40)),
                ('tx_date', models.DateField(default=datetime.date(2024, 2, 22))),
                ('tx_time', models.TimeField(default=datetime.time(9, 57, 53, 719352))),
                ('browser_family', models.TextField(blank=True, default='', null=True)),
                ('browser_version_string', models.TextField(blank=True, default='', null=True)),
                ('browser_version', models.TextField(blank=True, default='', null=True)),
                ('os_family', models.TextField(blank=True, default='', null=True)),
                ('os_version_string', models.TextField(blank=True, default='', null=True)),
                ('os_version', models.TextField(blank=True, default='', null=True)),
                ('is_bot', models.BooleanField(default=False)),
                ('is_pc', models.BooleanField(default=False)),
                ('is_mobile', models.BooleanField(default=False)),
                ('is_tablet', models.BooleanField(default=False)),
                ('is_touch_capable', models.BooleanField(default=False)),
                ('is_ios', models.BooleanField(default=False)),
                ('is_android', models.BooleanField(default=False)),
                ('is_linux', models.BooleanField(default=False)),
                ('is_windows', models.BooleanField(default=False)),
                ('is_mac', models.BooleanField(default=False)),
                ('login_datetime', models.DateTimeField(null=True)),
                ('logout_datetime', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
