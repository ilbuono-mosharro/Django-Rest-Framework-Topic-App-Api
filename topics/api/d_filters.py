from django_filters import rest_framework as filters
from ..models import Topic


class MyFilters(filters.FilterSet):
    subject = filters.CharFilter(field_name='subject', lookup_expr='icontains')
    body = filters.CharFilter(field_name='body', lookup_expr='icontains')

    class Meta:
        model = Topic
        fields = ['subject', 'body']
