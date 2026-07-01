# Generated manually

import django.db.models.deletion
import django.utils.timezone
import uuid

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailUnsubscribe',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),
                ('token', models.UUIDField(
                    default=uuid.uuid4,
                    editable=False,
                    unique=True
                )),
                ('is_unsubscribed', models.BooleanField(default=False)),
                ('unsubscribed_datetime', models.DateTimeField(
                    blank=True,
                    null=True
                )),
                ('updated_datetime', models.DateTimeField(
                    default=django.utils.timezone.now
                )),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL
                )),
            ],
        ),
    ]