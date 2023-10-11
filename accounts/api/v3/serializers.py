from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password1']

    def validate(self, attrs):
        if attrs["password"] != attrs['password1']:
            raise serializers.ValidationError("details:{passwords didnt match!}")
        try:
            validate_password(attrs["password"])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1")
        return User.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data["id"] = self.user.id
        validated_data["email"] = self.user.email
        # if not self.user.is_verified:
        #     raise serializers.ValidationError("user is not verified!")
        return validated_data


# class LoginSerializer(serializers.Serializer):
#     email = serializers.CharField()
#     password = serializers.CharField()
#
#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#
#         if email and password:
#             if User.objects.filter(email=email).exists():
#                 user = authenticate(email=email, password=password)
#
#             else:
#                 msg = _('this user is not registered.')
#                 raise serializers.ValidationError(msg)
#
#             if not user:
#                 msg = _('Unable to log in with provided credentials.')
#                 raise serializers.ValidationError(msg)
#
#         else:
#             msg = 'Must include "username" and "password".'
#             raise serializers.ValidationError(msg)
#
#         attrs['user'] = user
#         return attrs
#

# class LogoutSerializer(serializers.Serializer):
#     pass
