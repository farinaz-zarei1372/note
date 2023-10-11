from django.urls import path, include

urlpatterns = [
    path("api/v3/", include("app.api.v3.urls"))

]
