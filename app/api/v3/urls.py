from django.urls import path, include
from rest_framework import routers

from app.api.v3.views import NoteView, CategoryView

router = routers.DefaultRouter()
router.register(r'note', NoteView, basename="noteview")
router.register(r'category', CategoryView, basename="categoryview")
urlpatterns = router.urls
