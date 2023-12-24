from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from .models import MultiToken


class ObtainMultiToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = MultiToken.objects.get_or_create(user=user, is_active=True)
        return Response({"token": token.key})


obtain_multi_token = ObtainAuthToken.as_view()
