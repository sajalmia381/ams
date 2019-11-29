from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import booking_view, booking_form_view, quote_success, QuoteView, checkout_success  # checkout_view, booking_view, BookingUpdate
from venue.views import VenueDetailView

app_name = 'booking'
urlpatterns = [
    # path('venue/<int:pk>/booking/', booking_view, name="bookingForm"),
    # path('venue/<int:pk>/booking/', BookingUpdate.as_view(), name="bookingForm"),
    # path('booking/<int:pk>/', BookingUpdate.as_view(), name="bookingUpdate"),
    # path('venue/<int:pk>/booking/update/', booking_view, name="bookingFormUpdate"),
    # path('checkout/', checkout_view, name='checkout'),
    # path('cart/', cart_view, name='cart_create'),

    path('quote-success/', quote_success, name='quote_success'),
    path('booking/<int:quote_pk>/', booking_view, name="booking_obj"),
    path('booking/create/<int:quote_pk>/', booking_form_view, name="booking_form"),
    path('checkout/success', checkout_success, name='checkout_success'),

    path('dashboard/quote/', QuoteView.as_view(), name='quote_list'),
]