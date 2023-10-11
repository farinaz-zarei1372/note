from rest_framework import generics, viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.response import Response

from app.api.v3.serializers import NoteSerializer, CategorySerializer
from app.models import NoteModel, Category


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = "limit"
    page_size = 2
    max_page_size = 5


class NoteView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
               generics.UpdateAPIView):
    serializer_class = NoteSerializer
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['created_at']
    queryset = NoteModel.objects.all()

    class IsAdminOrReadOnly(BasePermission):
        SAFE_METHODS = ["GET"]

        def has_permission(self, request, view):
            print(request.user.is_superuser, request.method, request.user)
            if not request.user.is_superuser:
                return request.method in self.SAFE_METHODS
            else:
                return True

    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]



class CategoryView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                   generics.UpdateAPIView):
    serializer_class = CategorySerializer
    pagination_class = CustomPageNumberPagination
    ordering_fields = ['created_at']
    queryset = Category.objects.all()

    # class IsOwnerOrReadOnly(BasePermission):
    #     SAFE_METHODS = ["GET"]
    #
    #     def has_object_permission(self, request, view, obj):
    #         print(obj.owner.id, request.user)
    #         if not obj.owner.id == request.user.id:
    #             return request.method in self.SAFE_METHODS
    #         else:
    #             return True
    #
    # permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    permission_classes = [IsAuthenticated]
