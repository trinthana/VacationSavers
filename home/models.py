from django.db import models
from django.contrib.auth.models import User, AbstractUser

class UserProfile(models.Model):
    user              = models.OneToOneField(User, on_delete=models.CASCADE)
    website           = models.URLField(default='', blank=True)
    phone             = models.CharField(max_length=20,default='', blank=True)
    address           = models.TextField(default='', blank=True)
    zipcode           = models.CharField(max_length=10, default='', blank=True)
    bio               = models.TextField(default='', blank=True)
    image             = models.URLField(default='')

class UserToken(models.Model):
    user              = models.ForeignKey(User, on_delete=models.CASCADE)
    site              = models.CharField(max_length=20,default='', blank=True)
    token             = models.CharField(max_length=30,default='', blank=True)

   