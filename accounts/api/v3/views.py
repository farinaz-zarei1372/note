from django.contrib.auth import login, logout
from django.shortcuts import redirect
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.api.v3.serializers import RegistrationSerializer, LoginSerializer, LogoutSerializer


class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data["email"])
        return Response(serializer.errors)

class CustomObtainPairTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            return Response(serializer.data["email"])
        else:
            return Response(serializer.errors)


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")
