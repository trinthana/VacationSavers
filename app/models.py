from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone


class PackageChoices(models.TextChoices):     
    PREMIER = 'PREMIER', 'Premier Savings Plan'
    ELITE = 'ELITE', 'Elite Savings Plan'
    ULTIMATE = 'ULTIMATE', 'Ultimate Savings Bundle'

class ApplicationChoices(models.TextChoices):     
    ACCESS = "ACCESS", "Access Development"
    ARRIVIA = "ARRIVIA", "Arrivia"
    EXPEDIA = "EXPEDIA", "Expedia"
    BOOKING = "BOOKING", "Booking.com"
    BEDSOPIA = "BEDSOPIA", "Bedsopia"
    YALAGO = "YALAGO", "Yalago"
    WORLDIA = "WORLDIA", "Worldia"
    CRUISEWAFCH = "CRUISEWATCH", "Cruisewatch"
    CRUISEDIRECT = "CRUISEDIRECT", "CruiseDirect"
    DREAMLINES = "DREAMLINES", "Dreamlines"
    CARTRAWLER = "CARTRAWLER", "CarTrawler"
    TOURRADAR = "TOURRADAR", "TourRadar"
    GETYOURGUIDE = "GETYOURGUIDE", "GetYourGuide"
    GADVENGER = "GADVENGER", "G Advengers"
    TICKETNETWORK = "TICKETNETWORK", "Ticket Network"
    INTERLNKD = "INTERLNKD", "InterLNKD"
    GLOBATECH = "GLOBATECH", "GlobalTech"
    TALIXO = "TALIXO", "Talixo"
    WELCOME = "WELCOME", "Welcome Pick Ups"
    TRANSFERZ = "TRANSFERZ", "Transferz"
    HOLIBOB = "HOLIBOB", "Holibob"
    SERVANTRIP = "SERVANTRIP", "Servantrip"
    NEZASA = "NEZASA", "Nezasa"



class UserProfile(models.Model):

    user                = models.OneToOneField(User, on_delete=models.CASCADE)
    address             = models.TextField(default='', blank=True)
    postal_code         = models.CharField(max_length=10, default='', blank=True)
    phone               = models.CharField(max_length=20, default='', blank=True)
    image_file          = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    token               = models.TextField(default='', blank=True)
    subscribed_package  = models.CharField(max_length=10, default='', blank=True, choices=PackageChoices.choices)
    subscribed_date     = models.DateField(null=True, blank=True)
    expired_date        = models.DateField(null=True, blank=True)
    updated_datetime    = models.DateTimeField(default=timezone.now)

class SubscriptionHistory(models.Model):

    user                = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribed_package  = models.CharField(max_length=10, default='', blank=True, choices=PackageChoices.choices)
    subscribed_date     = models.DateField(null=True)
    expired_date        = models.DateField(null=True)
    updated_datetime    = models.DateTimeField(default=timezone.now)

class ApplicationToken(models.Model):

    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    application         = models.CharField(max_length=20,default='', blank=True, choices=ApplicationChoices.choices)
    token               = models.CharField(max_length=50,default='', blank=True)
    custom1             = models.TextField(default='', blank=True)
    custom2             = models.TextField(default='', blank=True)
    custom3             = models.TextField(default='', blank=True)
    updated_datetime    = models.DateTimeField(default=timezone.now)

