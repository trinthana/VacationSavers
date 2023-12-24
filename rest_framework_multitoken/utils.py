from .models import MultiToken


def get_user_primary_token(user):
    try:
        return MultiToken.objects.filter(user=user, is_active=True).latest("created")
    except MultiToken.DoesNotExist:
        return None
