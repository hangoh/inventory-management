from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username"]


class UserAuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password=serializers.CharField(style = {"input_type": "password"})
    class Meta:
        model = User
        fields = ["username","password"]

    def get_username(obj):
        return obj.username

    def get_password(obj):
        return obj.password