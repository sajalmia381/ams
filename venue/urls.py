from django.urls import path
from .views import HomeView, VenueListView, VenueDetailView

app_name = 'venue'

urlpatterns = [
    path('', HomeView.as_view(), name="homeUrl"),
    path('venue/', VenueListView.as_view(), name="venueListUrl"),
    path('venue/<pk>/', VenueDetailView.as_view(), name="venueDetailUrl"),
]
