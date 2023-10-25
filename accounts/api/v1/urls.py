from django.urls import path

from .views import LoginView, RegistrationView, ProfileView

urlpatterns = [path("login/", LoginView.as_view(), name="login"),
               path("signup/", RegistrationView.as_view(), name="signup"),
               path('profile/', ProfileView.as_view({"get": "retrieve", "patch": "partial_update"}), name='profile')
               ]
