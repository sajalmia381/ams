from django.urls import path
from .views import HomeView, VenueListView, VenueDetailView, venue_list_view, VenueCreateView, VenueBookingView, venue_booking_view
from django_filters.views import FilterView
from django.contrib.auth.decorators import login_required

app_name = 'venue'

urlpatterns = [
    path('', HomeView.as_view(), name="homeUrl"),
    path('venue/', login_required(VenueListView.as_view()), name="venueListUrl"),
    # path('venue/', venue_list_view, name="venueListUrl"),
    path('venue/<pk>/', VenueDetailView.as_view(), name="venueDetailUrl"),
    path('venue/create', VenueCreateView.as_view(), name="venueCreate"),
    path('venue/<pk>/booking', VenueBookingView.as_view(), name="venueBooking"),
    # path('venue/<pk>/booking', venue_booking_view, name="venueBooking"),
]
