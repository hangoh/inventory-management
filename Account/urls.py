from django.urls import path

from rest_framework.authtoken import views

from .views import UserViewSet,UserCreateViewSet

urlpatterns = [
    path("",UserViewSet.as_view({"get":"retrieve"}), name="user"),
    path("sign-out",UserViewSet.as_view({"post":"create"}), name="usersignout"),
    path("sign-up",UserCreateViewSet.as_view({"post":"create"}), name="usersignup"),
    path("auth-user",views.obtain_auth_token, name="authenticateuser"),
]

