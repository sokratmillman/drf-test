from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers


class SignupSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data["password"] = make_password(
            validated_data.get("password"))
        return super(SignupSerializer, self).create(validated_data)

    class Meta:
        model = User
        fields = ['username', 'password']


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password']
