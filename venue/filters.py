from .models import Venue
import django_filters
from django_filters.widgets import RangeWidget


class VenueFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Venue
        # fields = ['name'] #, 'city'
        # fields = {
        #     'name': ['icontains'],
        # }
        # fields = ['city', 'booking_purpose', 'booking_type', 'price']
        fields = {
            'city': ['exact'],
            'booking_purpose': ['exact'],
            'price': ['lt', 'gt'],
        }
