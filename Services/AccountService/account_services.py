from rest_framework.authtoken.models import Token
from Account.models import User
from Material.models import Store

def auth_user(request):
    try:
        user_username = request.data.get("username")
        user = User.objects.get(name = user_username)
        token = Token.objects.create(user=user)
        return token.key
    except User.DoesNotExist:
        return False
    
def get_user(request):
    user = request.user
    if user.is_anonymous :
        return False
    return user

def get_stores(user):
    stores = Store.objects.filter(user=user)
    if not stores:
        return False
    return stores

def get_store(user,id):
    stores = Store.objects.filter(user=user)
    if not stores:
        return False
    try:
        store = stores.get(store_id=id)
        return store
    except:
        return False