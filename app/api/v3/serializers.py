from django.core import exceptions
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from app.models import NoteModel, Category


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteModel
        fields = '__all__'
        read_only_fields = ["created_by"]

    def validate(self, attrs):
        attrs["created_by"] = self.context.get("request").user
        return attrs


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
