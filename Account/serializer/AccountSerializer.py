from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username"]

class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","password"]

class UserAuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password=serializers.CharField()
    class Meta:
        model = User
        fields = ["username","password"]

    def get_username(obj):
        return obj.username

    def get_password(obj):
        return obj.password