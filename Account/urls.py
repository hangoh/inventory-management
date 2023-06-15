from django.urls import path

from rest_framework.authtoken import views

from .views import UserView,UserCreateView

urlpatterns = [
    path("",UserView.as_view({"get":"retrieve"}), name="user"),
    path("sign-out/",UserView.as_view({"post":"create"}), name="usersignout"),
    path("sign-up/",UserCreateView.as_view({"post":"create"}), name="usersignup"),
    path('auth-user/',views.obtain_auth_token, name="authenticateuser"),
]

