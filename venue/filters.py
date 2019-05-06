from .models import Venue
import django_filters


class VenueFilter(django_filters.FilterSet):

    class Meta:
        model = Venue
        # fields = ['name'] #, 'city'
        # fields = {
        #     'name': ['icontains'],
        # }
        fields = ['city', 'booking_purpose', 'booking_type']
