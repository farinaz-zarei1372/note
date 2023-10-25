import django_filters

from app.models import NoteModel, Category


class NoteFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='category__name',
        lookup_expr='contains',
    )
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='contains',
    )
    tag = django_filters.CharFilter(
        field_name='tag',
        lookup_expr='contains',
    )
    user = django_filters.CharFilter(
        field_name='created_by',
        lookup_expr='exact',
    )

    class Meta:
        model = NoteModel
        fields = ["category", "tag", "title", "user"]


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='contains',
    )

    class Meta:
        model = Category
        fields = ["name"]
