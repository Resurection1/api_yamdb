from rest_framework import serializers
from .models import MyUser


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'email', 'username',
                  'is_admin', 'is_staff', 'is_active')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                "The username 'me' is not allowed.")
        if MyUser.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with that username already exists.")
        return value

    def validate_email(self, value):
        if MyUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with that email already exists.")
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
