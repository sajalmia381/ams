from django.shortcuts import render, reverse, redirect, HttpResponse
from booking.models import VenueBooking
from billing.models import BillingProfile
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from venue.models import Venue
from .forms import VenueBookingForm, VenueBookingUpdate
from .models import VenueBooking, Quote

STRIPE_PUB_KEY = getattr(settings, 'STRIPE_PUB_KEY', None)


def booking_view(request, quote_pk):
    """ Booking Form View """
    template_name = 'booking/booking_view.html'

    if Quote.objects.get(pk=quote_pk).status == 'review':
        return HttpResponse("Quote is not review yet, Please wait it will confirm very soon")

    billing_profile, billing_profile_create = BillingProfile.objects.get_or_new(request)
    booking_obj, booking_create = VenueBooking.objects.get_or_new(request, quote_pk=quote_pk)

    if request.method == "POST":
        if billing_profile.has_card:
            card_obj = billing_profile.get_cards().first()
            billing_profile.charge(booking_obj, card=card_obj)
            booking_obj.mark_paid()
            return redirect('booking:checkout_success')

    context = {
        "booking_obj": booking_obj,
        "billing_profile": billing_profile,
    }

    return render(request, template_name, context)


@login_required
def booking_form_view(request, quote_pk):
    """ Booking Form View """
    template_name = 'booking/booking_form_view.html'

    # booking_obj, booking_create = VenueBooking.objects.get_or_new(request, quote_pk=pk)

    # print(dir(booking_obj))
    # print(booking_obj.billing_profile)
    # print(booking_create)
    # if booking_obj.booking_date is None:
    #     print(True)
    # initial = {
    #     # 'venue': pk,
    #     'billing_profile': request.user,
    #     'sub_total': Venue.objects.filter(pk=pk).first().price,
    #     'total': Venue.objects.filter(pk=pk).first().price,
    # }
    # form = VenueBookingForm
    # # print(dir(form.fields['venue']))
    #
    # if form.is_valid():
    #     print("Form Valid")
    #     instance = form.save(commit=False)
    #     instance.save()
    #     return reverse('booking:checkout')
    # else:
    #     print("form Not Valid")
    #     print(form.data)
    # print(booking_obj.venue.pk)
    if Quote.objects.get(pk=quote_pk).status == 'review':
        return HttpResponse("Quote is not review yet, Please wait it will confirm very soon")

    initial = {
        'quote': quote_pk,
        'billing_profile': request.user,
        'sub_total': Quote.objects.get(pk=quote_pk).total,
        'total': Quote.objects.get(pk=quote_pk).total
    }
    form = VenueBookingForm(initial=initial)
    # print('request Post', request.POST)
    # print(dir(form.fields['total']))
    if request.method == "POST":
        print(request.POST)
        form = VenueBookingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('booking:checkout')
        else:
            print("errors", form.errors)
            print(form.non_field_errors)
    context = {
        'form': form,
        # "booking_obj": booking_obj,
    }

    return render(request, template_name, context)


class BookingUpdate(UpdateView):
    model = VenueBooking
    template_name = 'booking/booking_update.html'
    form_class = VenueBookingUpdate

    def get_context_data(self, **kwargs):
        context = super(BookingUpdate, self).get_context_data(**kwargs)
        return context


def booking_update_view(request, pk):
    booking_obj, booking_create = VenueBooking.objects.get_or_new(request, venue_pk=pk)
    # print('update', request)
    # form = VenueBookingForm(request.POST)
    # print(dir(form))
    # if form.is_valid():
    #     print(form)
    # else:
    #     print('else', form)
    print('Update Page')
    return redirect('booking:checkout')


def checkout_view(request):
    """ Booking Checkout View """
    template_name = 'booking/checkout.html'
    if request.method == "POST":
        print(request.POST)
        print(request.POST['stripeToken'])

    context = {
        'stripe_pub_key': STRIPE_PUB_KEY,
    }

    return render(request, template_name, context)


def checkout_success(request):
    return render(request, 'booking/checkout_success.html')


class QuoteView(LoginRequiredMixin, ListView):
    model = Quote
    template_name = 'booking/quote_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuoteView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        user = self.request.user
        return Quote.objects.filter(email=user.email)


def quote_success(request):
    """" After quote Request send it will Confirm"""
    return render(request, 'booking/quote_success.html')
