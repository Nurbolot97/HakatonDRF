from django_filters import rest_framework as filters
from main.models import Engine


class EngineFilter(filters.FilterSet):

    price = filters.RangeFilter()

    class Meta:
        model = Engine
        fields = ['price',]