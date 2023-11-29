import django_filters
from .models import GatheringPost


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    tag = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = GatheringPost
        fields = ["title", "tag", "status"]
