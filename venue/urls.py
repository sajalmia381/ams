from django.urls import path
from .views import HomeView, VenueListView, VenueDetailView, VenueCreateView
from django_filters.views import FilterView
from django.contrib.auth.decorators import login_required

app_name = 'venue'

urlpatterns = [
    path('', HomeView.as_view(), name="homeUrl"),
    path('venue/', VenueListView.as_view(), name="venueListUrl"),
    # path('venue/', venue_list_view, name="venueListUrl"),
    path('venue/<int:pk>/', VenueDetailView.as_view(), name="venueDetailUrl"),
    path('venue/create', VenueCreateView.as_view(), name="venueCreate"),
]
