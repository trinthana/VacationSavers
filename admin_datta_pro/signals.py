from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework_multitoken.models import MultiToken
from django.contrib.sessions.models import Session
from django.utils import timezone
from datetime import datetime, timedelta
from app.models import UserProfile, SubscriptionHistory, PackageChoices
from .threadlocals import thread_locals

def get_session_data(session_key):
    try:
        session = Session.objects.get(session_key=session_key, expire_date__gt=timezone.now())
        session_data = session.get_decoded()
        return session_data
    except Session.DoesNotExist:
        return None
    
@receiver(post_save, sender=User)
def validate_token(sender, instance, created, **kwargs):
    print('thread_locals signal = ', thread_locals)
    request = thread_locals.request #getattr(thread_locals, 'request', None)
    print('thread_locals.token = ', thread_locals.token )

    session_key = request.session.session_key
    try:
        session_token = thread_locals.token
    except:
        session_token = None

    if created:
        # Check if the 'token' field is provided in the user instance
        if session_token is not None and session_token != '' : 

            # Create UserProfile data with PREMIER subscription plan
            user_profile, created = UserProfile.objects.get_or_create(user=instance)
            user_profile.subscribed_package = PackageChoices.PREMIER
            user_profile.subscribed_date = datetime.now()
            user_profile.expired_date = datetime.now() + timedelta(days=365)
            user_profile.token = session_token
            user_profile.save()
        
            thread_locals.token = None

        else :
            # Create blank UserProfile
            user_profile, created = UserProfile.objects.get_or_create(user=instance)
            user_profile.save()
            
            
