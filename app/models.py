from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_user_agents.utils import get_user_agent
import json


def default_tx_date():
    return timezone.now().date()

def default_tx_time():
    return timezone.now().time()

class EventChoices (models.TextChoices):     
    FIRSTLOGIN = 'FIRSTLOGIN', 'First Login'
    WINTERSALE = 'WINTERSALE', 'Winter Sales'
    SUMMERSALE = 'SUMMERSALE', 'Summer Sales'
    HALLOWEEN = 'HALLOWEEN', 'Halloween Sales'

class PackageChoices(models.TextChoices):     
    PREMIER = 'PREMIER', 'Premier Savings Plan'
    ELITE = 'ELITE', 'Elite Savings Plan'
    ULTIMATE = 'ULTIMATE', 'Ultimate Savings Bundle'

class ApplicationChoices(models.TextChoices):     
    ACCESS = "ACCESS", "Access Development"
    ACCESSIFRAME = "ACCESSIFRAME", "Access Development Iframe"
    ACCESSDEAL = "ACCESSDEAL", "Access Development Deals"
    ARRIVIA = "ARRIVIA", "Arrivia Cruise"
    EXPEDIA = "EXPEDIA", "Expedia"
    BOOKING = "BOOKING", "Booking.com"
    BEDSOPIA = "BEDSOPIA", "Bedsopia"
    YALAGO = "YALAGO", "Yalago"
    WORLDIA = "WORLDIA", "Worldia Car"
    CRUISEWAFCH = "CRUISEWATCH", "Cruisewatch"
    CRUISEDIRECT = "CRUISEDIRECT", "CruiseDirect"
    DREAMLINES = "DREAMLINES", "Dreamlines"
    CARTRAWLER = "CARTRAWLER", "CarTrawler"
    TOURRADAR = "TOURRADAR", "TourRadar"
    GETYOURGUIDE = "GETYOURGUIDE", "GetYourGuide"
    GADVENGER = "GADVENGER", "G Advengers"
    TIMETOTICKET = "TIMETOTICKET", "Time To Ticket"
    TICKETNETWORK = "TICKETNETWORK", "Ticket Network"
    INTERLNKD = "INTERLNKD", "InterLNKD"
    GLOBATECH = "GLOBATECH", "GlobalTech"
    TALIXO = "TALIXO", "Talixo"
    WELCOME = "WELCOME", "Welcome Pick Ups"
    TRANSFERZ = "TRANSFERZ", "Transferz"
    HOLIBOB = "HOLIBOB", "Holibob"
    SERVANTRIP = "SERVANTRIP", "Servantrip"
    NEZASA = "NEZASA", "Nezasa"
    GTN = "GTN", "GTN Vacation Rental"
    VSFLIGHT = "VSFLIGHT", "VacationSavers Flight"
    DUNHILL = "DUNHILL", "DUNHILL Special Deals"



class UserProfile(models.Model):

    user                = models.OneToOneField(User, on_delete=models.CASCADE)
    address             = models.TextField(default='', blank=True)
    city                = models.TextField(default='', blank=True)
    state_code          = models.CharField(max_length=2, default='', blank=True)
    country_code        = models.CharField(max_length=2, default='', blank=True)
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
    token               = models.CharField(max_length=200,default='', blank=True)
    custom1             = models.TextField(default='', blank=True)
    custom2             = models.TextField(default='', blank=True)
    custom3             = models.TextField(default='', blank=True)
    updated_datetime    = models.DateTimeField(default=timezone.now)

class ClickDetails(models.Model):

    user                = models.ForeignKey(User, on_delete=models.CASCADE)
    application         = models.CharField(max_length=20, default='', blank=True, choices=ApplicationChoices.choices)
    tx_date              = models.DateField()
    tx_time              = models.TimeField()
    tx_url              = models.TextField(default='', blank=True, null=True)
    remote_host         = models.TextField(default='', blank=True, null=True)
    remote_addr         = models.CharField(max_length=15, default='', blank=True, null=True)
    http_headers        = models.TextField(default='', blank=True, null=True)
    updated_datetime    = models.DateTimeField(default=timezone.now)

    class Meta:
        # Define unique_together constraint to prevent duplication
        unique_together = [['user', 'application', 'tx_date', 'tx_time']]
    
    @classmethod
    def add(self, request, application, tx_url):

        """
        Class method to store user click details.
        """
        # Retrieve the ClickDetails instance based on application and tx_date
        headers = request.META
        remote_host = headers.get('REMOTE_HOST')
        remote_addr = headers.get('REMOTE_ADDR')

        click_details, created = self.objects.get_or_create(
            user=request.user,
            application=application,
            tx_date=default_tx_date(),
            tx_time=default_tx_time(),
            defaults={
                'tx_url': tx_url,
                'remote_host': remote_host,
                'remote_addr': remote_addr,
                'http_headers': headers
            }
        )
        if created:
            click_details.save()
            ClickSummary.increase(application, default_tx_date())
   
class ClickSummary(models.Model):

    application         = models.CharField(max_length=20, default='', blank=True, null=True, choices=ApplicationChoices.choices)
    tx_date             = models.DateField()
    tx_counted          = models.BigIntegerField(default=0)

    @classmethod
    def increase(self, application, tx_date=default_tx_date(), increment_value=1):
        """
        Class method to increment tx_counted for a specific ClickSummary instance.
        """
        # Retrieve the ClickSummary instance based on application and tx_date
        click_summary,created  = self.objects.get_or_create(application=application, tx_date=tx_date)
        if created:
            # Create new record with default = 1
            click_summary.tx_counted = 1
            click_summary.save()
        else:
            # Increment tx_counted by the specified increment_value
            click_summary.tx_counted += increment_value
            click_summary.save()

class Sessions(models.Model):

    session_key                 = models.CharField(max_length=40, null=False)
    user                        = models.TextField(max_length=40, null=False)
    tx_date                     = models.DateField()
    tx_time                     = models.TimeField()
    remote_addr                 = models.CharField(max_length=15, default='', blank=True, null=True)
    browser_family              = models.TextField(default='', blank=True, null=True)
    browser_version_string      = models.TextField(default='', blank=True, null=True)
    os_family                   = models.TextField(default='', blank=True, null=True)
    os_version_string           = models.TextField(default='', blank=True, null=True)
    is_bot                      = models.BooleanField(default=False)
    is_pc                       = models.BooleanField(default=False)
    is_mobile                   = models.BooleanField(default=False)
    is_tablet                   = models.BooleanField(default=False)
    is_touch_capable            = models.BooleanField(default=False)
    is_ios                      = models.BooleanField(default=False)
    is_android                  = models.BooleanField(default=False)
    is_linux                    = models.BooleanField(default=False)
    is_windows                  = models.BooleanField(default=False)
    is_mac                      = models.BooleanField(default=False)
    login_datetime              = models.DateTimeField(null=True)
    logout_datetime             = models.DateTimeField(null=True)

    @classmethod
    def add(self, request, session_key):

        """
        Class method to store session data.
        """
        user_agent = get_user_agent(request)
        client_ip = request.META.get('REMOTE_ADDR')
        tx_date                     = default_tx_date(),
        sessions = self.objects.create(
            session_key                 = session_key,
            user                        = request.user.username,
            tx_date                     = default_tx_date(),
            tx_time                     = default_tx_time(),
            remote_addr                 = client_ip,
            browser_family              = user_agent.browser.family,
            browser_version_string      = user_agent.browser.version_string,
            os_family                   = user_agent.os.family,
            os_version_string           = user_agent.os.version_string,
            is_bot                      = user_agent.is_bot,
            is_pc                       = user_agent.is_pc,
            is_mobile                   = user_agent.is_mobile,
            is_tablet                   = user_agent.is_tablet,
            is_touch_capable            = user_agent.is_touch_capable,
            is_ios                      = user_agent.os.family == 'iOS',
            is_android                  = user_agent.os.family == 'Android',
            is_linux                    = user_agent.os.family == 'Linux',
            is_windows                  = user_agent.os.family == 'Windows',
            is_mac                      = user_agent.os.family == 'Mac OS X',
            login_datetime              = timezone.now(),
            logout_datetime             = None
        )

        # Create/Update device summary
        device_summary,created  = SummaryDevices.objects.get_or_create(tx_date=default_tx_date())
        if created:
            # Create new record with default = 1
            device_summary.tx_date = default_tx_date()
            device_summary.desktop = (1 if user_agent.is_pc else 0)
            device_summary.mobile = (1 if user_agent.is_mobile else 0)
            device_summary.tablet = (1 if user_agent.is_tablet else 0)
            device_summary.save()
        else:
            # Increment count by the specified increment_value
            device_summary.desktop += (1 if user_agent.is_pc else 0)
            device_summary.mobile += (1 if user_agent.is_mobile else 0)
            device_summary.tablet += (1 if user_agent.is_tablet else 0)
            device_summary.save()

        # Create/Update OS summary
        os_summary,created  = SummaryOS.objects.get_or_create(tx_date=default_tx_date())
        if created:
            # Create new record with default = 1
            os_summary.tx_date = default_tx_date()
            os_summary.ios = (1 if user_agent.os.family == 'iOS' else 0)
            os_summary.android = (1 if user_agent.os.family == 'Android' else 0)
            os_summary.linux = (1 if user_agent.os.family == 'Linux' else 0)
            os_summary.windows = (1 if user_agent.os.family == 'Windows' else 0)
            os_summary.mac = (1 if user_agent.os.family == 'Mac OS X' else 0)
            os_summary.save()
        else:
            # Increment count by the specified increment_value
            os_summary.ios += (1 if user_agent.os.family == 'iOS' else 0)
            os_summary.android += (1 if user_agent.os.family == 'Android' else 0)
            os_summary.linux += (1 if user_agent.os.family == 'Linux' else 0)
            os_summary.windows += (1 if user_agent.os.family == 'Windows' else 0)
            os_summary.mac += (1 if user_agent.os.family == 'Mac OS X' else 0)
            os_summary.save()

        # Create/Update browser family
        browser_summary,created  = SummaryBrowsers.objects.get_or_create(tx_date=default_tx_date(), browser_family=user_agent.browser.family)
        if created:
            browser_summary.tx_date = default_tx_date()
            browser_summary.browser_summary = user_agent.browser.family
            browser_summary.count = 1
            browser_summary.save()
        else:
            browser_summary.count += 1
            browser_summary.save()

    @classmethod
    def logout(self, request, session_key):
        sessions = self.objects.filter(session_key=session_key)
        print("session_key = ", session_key)
        print("sessions.count = ", sessions.count())
        if sessions.count() > 0:
            sessions.logout_datetime = timezone.now()
            sessions.update()
        

class SummaryDevices(models.Model):
    tx_date             = models.DateField()
    desktop             = models.IntegerField(default=0)
    mobile              = models.IntegerField(default=0)
    tablet              = models.IntegerField(default=0)

class SummaryOS(models.Model):
    tx_date             = models.DateField()
    ios                 = models.IntegerField(default=0)
    android             = models.IntegerField(default=0)
    linux               = models.IntegerField(default=0)
    windows             = models.IntegerField(default=0)
    mac                 = models.IntegerField(default=0)

class SummaryBrowsers(models.Model):
    tx_date             = models.DateField()
    browser_family      = models.TextField(default='', blank=True, null=True)
    count               = models.IntegerField(default=0)

class EventParticipations(models.Model):

    user                = models.OneToOneField(User, on_delete=models.CASCADE)
    event               = models.CharField(max_length=10, default='', blank=True, choices=EventChoices.choices)
    updated_datetime    = models.DateTimeField(default=timezone.now)
