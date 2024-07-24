import django_filters
from ..models import Order

class OrderFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name='time', lookup_expr='gte', input_formats=['%Y-%m-%dT%H:%M:%S%z'])
    end_date = django_filters.DateTimeFilter(field_name='time', lookup_expr='lte', input_formats=['%Y-%m-%dT%H:%M:%S%z'])

    class Meta:
        model = Order
        fields = ['start_date', 'end_date']
