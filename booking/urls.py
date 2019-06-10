from django.urls import path
from .views import checkout_view, booking_view, booking_form_view, quote_success, QuoteView  # cart_view, booking_view, BookingUpdate
from venue.views import VenueDetailView

app_name = 'booking'
urlpatterns = [
    # path('venue/<int:pk>/booking/', booking_view, name="bookingForm"),
    # path('venue/<int:pk>/booking/', BookingUpdate.as_view(), name="bookingForm"),
    # path('booking/<int:pk>/', BookingUpdate.as_view(), name="bookingUpdate"),
    # path('venue/<int:pk>/booking/update/', booking_view, name="bookingFormUpdate"),
    path('checkout/', checkout_view, name='checkout'),
    # path('cart/', cart_view, name='cart_create'),


    path('quote-success/', quote_success, name='quote_success'),
    path('booking/<int:quote_pk>/', booking_view, name="booking_form"),
    path('booking/create/<int:quote_pk>/', booking_form_view, name="booking_form"),

    path('dashboard/quote/', QuoteView.as_view(), name='quote_list'),
]