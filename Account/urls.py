from django.urls import path
from Account.views import authenticateUser,getStore,getStores

urlpatterns = [
    path('auth/',authenticateUser, name="authenticateUser"),
    path('store/',getStores, name="store"),
    path('store/<int:id>',getStore, name="store_id"),
]