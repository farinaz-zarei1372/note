from django.urls import path, include

urlpatterns = [
    path('api/v3/', include("accounts.api.v3.urls"))
]
