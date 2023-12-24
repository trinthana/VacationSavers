from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    token = models.CharField(max_length=255, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',  # Use a custom related_name
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set_permissions',  # Use a custom related_name
        related_query_name='user',
    )
