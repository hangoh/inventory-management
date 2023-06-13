from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

def get_user(request):
    user = request.user
    if user.is_anonymous :
        return False
    return user

def create_user(serializer):
    user = User.objects.create_user(username = serializer.data["username"], password = serializer.data["password"])
    if(user): 
        token = Token.objects.create(user=user)
        return token
    return False

def sign_out_user(user):
    if user:
        token = Token.objects.get(user=user)
        token.delete()
        return True
    return False


