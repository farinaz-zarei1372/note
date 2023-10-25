from django.core import exceptions
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from taggit.serializers import (TagListSerializerField, TaggitSerializer)
from app.models import NoteModel, Category, Comment, MediaModel, AddressModel


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaModel
        fields = ["id", "media", "note"]
        read_only_fields = ["size", "title", "type"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["size"] = instance.size
        rep.pop("note")
        rep["title"] = instance.title
        rep["type"] = instance.type
        return rep

    def validate(self, attrs):
        files = self.context.get("request").FILES.getlist("media")
        for file in files:
            attrs["title"] = file.name
            attrs["size"] = file.size
            attrs["type"] = file.content_type
        return attrs

    def get_absolute_url(self, instance):
        request = self.context.get('request')
        return request.build_absolute_uri(instance.id)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["created_at", "updated_at"]


# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NoteModel.objects.all()
#         exclude = ["created_at", "updated_at"]


class NoteSerializer(TaggitSerializer, serializers.ModelSerializer):
    category = serializers.SlugRelatedField(many=True, slug_field="id", queryset=Category.objects.all())
    media = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    binary_files = serializers.FileField(required=False)
    tags = TagListSerializerField()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["category"] = CategorySerializer(instance.category, many=True).data
        return rep

    def get_address(self, instance):
        return AddressSerializer(instance.address, many=True).data

    def get_media(self, instance):
        list = []
        for item in instance.media.all():
            list.append(MediaSerializer(item).data)
        return list

    def get_comment(self, instance):
        list = []
        for item in instance.comment.all():
            list.append(CommentSerializer(item).data)
        return list

    class Meta:
        model = NoteModel
        fields = ["id", "title", "body", "created_by", "status", "category", "tags", "periority", "status",
                  "allowed_users", "duedate", "alerttime", "media", "binary_files", "address", "created_at",
                  "updated_at", "comment"]
        read_only_fields = ["created_by"]

    def validate(self, attrs):
        attrs["allowed_users"].append(self.context.get("request").user)
        return attrs

    def create(self, validated_data):
        validated_data["created_by"] = self.context.get("request").user
        validated_data.pop("binary_files")
        instance = super().create(validated_data)
        files = self.context.get("request").FILES.getlist("binary_files")
        for file in files:
            if not MediaModel.objects.filter(note=instance, media=file).exists():
                MediaModel.objects.create(note=instance, media=file, size=file.size, type=file.content_type,
                                          title=file.name)
        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ["created_at", "updated_at"]
        read_only_fields = ["created_by"]

    def create(self, validated_data):
        validated_data["created_by"] = self.context.get("request").user
        return super().create(validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.pop("note")
        return rep


class AddressSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.pop("note")
        return rep

    class Meta:
        model = AddressModel
        exclude = ["created_at", "updated_at"]
