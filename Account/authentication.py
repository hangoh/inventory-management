from django.core.exceptions import ObjectDoesNotExist

from rest_framework.authentication import TokenAuthentication,SessionAuthentication
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
    

class CustomSessionAuthentication(SessionAuthentication):
    def authenticate(self, request):
        user = super().authenticate(request)
        if user is None:
            raise AuthenticationFailed("Authentication Token Not Provided")
        store_uuid = request.parser_context["kwargs"].get("store_uuid")
        if store_uuid is not None:
            try:
                store = Store.objects.get(store_uuid = store_uuid)
                if not store.user == user[0]:
                    raise AuthenticationFailed("Invalid Store UUID")
            except ObjectDoesNotExist:
                raise ObjectDoesNotExist("Store Not Found")
        return user
    

class CheckIfAuthenticate(SessionAuthentication):
    def authenticate(self, request):
        user = super().authenticate(request)
        if user is None:
            return 
        return user