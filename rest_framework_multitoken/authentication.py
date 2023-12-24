from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

from .models import MultiToken


class MultiTokenAuthentication(TokenAuthentication):
    model = MultiToken

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)

        if not token.is_active:
            raise exceptions.AuthenticationFailed(_("Token inactive or deleted."))

        return (user, token)
