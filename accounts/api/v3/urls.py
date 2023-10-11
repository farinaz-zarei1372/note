from django.urls import path, include

from accounts.api.v3.views import LoginView, RegistrationView, LogoutView

urlpatterns = [path("login/", LoginView.as_view(), name="login"),
               path("signup/", RegistrationView.as_view(), name="signup"),
               path("logout/", LogoutView.as_view(), name="signup"),

               ]
