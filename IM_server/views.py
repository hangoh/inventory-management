from django.core.exceptions import ObjectDoesNotExist

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import AuthenticationFailed

from Store.models import Store


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        credentials = super().authenticate(request)
        if credentials is None:
            raise AuthenticationFailed("Authentication Token Not Provided")
        user,token = credentials
        store_uuid = request.parser_context["kwargs"].get("store_uuid")
        if store_uuid is not None:
            try:
                store = Store.objects.get(store_uuid = store_uuid)
                if not store.user.id == user.id:
                    raise AuthenticationFailed("Invalid Store UUID")
            except ObjectDoesNotExist:
                raise ObjectDoesNotExist("Store Not Found")
        return user,token


class BaseAuthenticatedViewSet(ModelViewSet):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]