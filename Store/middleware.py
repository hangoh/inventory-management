from django.urls import resolve

from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token

from Store.models import Store

def return_response(response):
    response.accepted_renderer = JSONRenderer()
    response.accepted_media_type = "application/json"
    response.renderer_context = {}
    response.render()
    return response

def check_store(user,store_uuid):
    if user is None:
        return Response({"error":"Anonymous User"}, status = status.HTTP_403_FORBIDDEN)
    store = Store.objects.get(store_uuid = store_uuid)
    if not (store.user == user):
        return Response({"error":"This store is not associate with you"}, status = status.HTTP_403_FORBIDDEN)
    return None


class CheckStoreMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response 

    def __call__(self, request):
        resolved_path = resolve(request.path_info)
        try:
            store_uuid = resolved_path.kwargs.get("store_uuid")
            header_token = request.META.get('HTTP_AUTHORIZATION', None)
            user = None 
            if header_token is not None:
                try:
                    token = header_token.split()
                    token_obj = Token.objects.get(key = token[1])
                    user = token_obj.user
                except Token.DoesNotExist:
                    response = Response({"error":"No Auth Credentials Provided"}, status = status.HTTP_401_UNAUTHORIZED)
                    return return_response(response)
            if check_store(user,store_uuid):
                response = check_store(user,store_uuid)
                return return_response(response)
        except:
            pass
        response = self.get_response(request)
        return response