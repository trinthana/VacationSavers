from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import permissions


class IsValidUserToken(permissions.BasePermission):
    """
    Custom permission to check if the token in the Authorization header is valid.
    """

    def has_permission(self, request, view):
        auth = TokenAuthentication()
        try:
            user_auth_tuple = auth.authenticate(request)
            if user_auth_tuple is not None:
                # Token is valid, attach user to request and allow access
                request.user = user_auth_tuple[0]
                return True
        except AuthenticationFailed:
            return False

        return False
