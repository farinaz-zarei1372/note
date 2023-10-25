from django.contrib import admin
from taggit.admin import TaggedItemInline
from taggit.models import Tag

from .api.v1.serializers import MediaSerializer, CommentSerializer, AddressSerializer
from .models import NoteModel, Category, Comment, MediaModel, AddressModel


@admin.register(NoteModel)
class Noteadmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_by"]
    fields = ["title", "body", "category", "tags", "periority", "status", "allowed_users", "duedate", "alerttime",
              "created_by", "address", "image", "comment"]
    search_fields = ("category__name", "title")
    readonly_fields = ("image", "address", "created_by", "comment")

    def image(self, obj):
        list = []
        for item in obj.media.all():
            list.append(MediaSerializer(item).data["media"])
        return list

    def comment(self, obj):
        list = []
        for item in obj.comment.all():
            list.append(CommentSerializer(item).data["body"])
        return list

    def address(self, obj):
        list = []
        for i in obj.address.all():
            list.append(AddressSerializer(i).data)
        return list

    def get_queryset(self, request):
        return super().get_queryset(request).for_user(request.user)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)
        obj.allowed_users.add(request.user)


@admin.register(Category)
class Categoryadmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(AddressModel)
class Adressadmin(admin.ModelAdmin):
    list_display = ["id", "lat", "long"]


@admin.register(MediaModel)
class Mediaadmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    readonly_fields = ("title", "type", "size",)

    def save_model(self, request, obj, form, change):
        files = request.FILES.getlist("media")
        for file in files:
            obj.size = file.size
            obj.type = file.content_type
            obj.title = file.name
        return super().save_model(request, obj, form, change)


@admin.register(Comment)
class Commentadmin(admin.ModelAdmin):
    list_display = ["id", "created_by", "note"]
    readonly_fields = ("created_by",)

    def get_queryset(self, request):
        return super().get_queryset(request).for_user(request.user)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        return super().save_model(request, obj, form, change)
