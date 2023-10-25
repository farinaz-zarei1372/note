from django.urls import path
from rest_framework import routers

from app.api.v1.views import NoteView, CategoryView, CommentView, MediaView, AddressView

router = routers.DefaultRouter()
router.register(r'note', NoteView, basename="noteview")
router.register(r'category', CategoryView, basename="categoryview")
router.register(r'comment', CommentView, basename="commentview")
router.register(r'media', MediaView, basename="mediaview")
router.register(r'address', AddressView, basename="addressview")
# path("tag", NoteView.get_tag, name="tagview")
urlpatterns = router.urls
