from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, mixins
from accounts.api.v1.serializers import RegistrationSerializer, ProfileSerializer
from accounts.models import Profile
from app.api.v1.views import CustomUpdateAPIView


class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data["email"])
        return Response(serializer.errors)


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class ProfileView(viewsets.GenericViewSet, CustomUpdateAPIView, mixins.RetrieveModelMixin):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        object = get_object_or_404(self.queryset, user=self.request.user)
        return object
