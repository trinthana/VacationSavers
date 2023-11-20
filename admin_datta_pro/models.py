from django.db import models

# Create your models here.
from auditlog.registry import auditlog


class MyModel(models.Model):
    pass
    # Model definition goes here

auditlog.register(MyModel)
