from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from app.api.v1.serializers import NoteSerializer, CategorySerializer, CommentSerializer, MediaSerializer, \
    AddressSerializer
from app.filters import NoteFilter, CategoryFilter
from app.models import NoteModel, Category, Comment, MediaModel, AddressModel
from rest_framework.filters import SearchFilter, OrderingFilter

from app.permissions import IsOwnerOrReadOnly


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "limit"
    page_size = 2
    max_page_size = 5


class CustomUpdateAPIView:

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class NoteView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
               CustomUpdateAPIView, mixins.DestroyModelMixin):
    serializer_class = NoteSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['created_at']
    queryset = NoteModel.objects.all()
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    filterset_class = NoteFilter

    # def get_queryset(self):
    #     return super().get_queryset().for_user(self.request.user)


class CategoryView(viewsets.GenericViewSet, mixins.ListModelMixin):
    serializer_class = CategorySerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['created_at']
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_class = CategoryFilter


class AddressView(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin, CustomUpdateAPIView):
    serializer_class = AddressSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['created_at']
    queryset = AddressModel.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_fields = ("note",)


# class TagView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, CustomUpdateAPIView,
#               mixins.DestroyModelMixin):
#     serializer_class = TagSerializer
#     pagination_class = CustomPageNumberPagination
#     ordering_fields = ['created_at']
#     queryset = posts = Post.objects.filter(tags__slug=tag)
#     permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]


class MediaView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                CustomUpdateAPIView, mixins.DestroyModelMixin):
    serializer_class = MediaSerializer
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['created_at']
    queryset = MediaModel.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_fields = ("note",)


class CommentView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, CustomUpdateAPIView,
                  mixins.DestroyModelMixin):
    serializer_class = CommentSerializer
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['created_at']
    queryset = Comment.objects.all()
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ("note",)
