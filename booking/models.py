from django.db import models
from django.db.models.signals import pre_save
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404, reverse
from django.utils import timezone
from django.db.models.signals import post_save

import stripe

from billing.models import BillingProfile
from venue.models import Venue, BookingPurpose
from ams.utils import get_random_string_generator

User = settings.AUTH_USER_MODEL


class Quote(models.Model):
    """ booking requested quote Object """
    STATUS_TYPE = (
        ('review', 'Reviewing'),
        ('confirm', 'Confirmed'),
        ('booked', 'Booked'),
    )
    status = models.CharField(max_length=15, choices=STATUS_TYPE, default='review')

    name = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField()
    mobile_no = models.IntegerField(verbose_name="Mobile Number")
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    guest = models.PositiveIntegerField(blank=True, null=True, verbose_name='Number Of Guest')
    booking_purpose = models.ForeignKey(BookingPurpose, on_delete=models.SET_NULL, blank=True, null=True)

    total = models.DecimalField(decimal_places=2, max_digits=10, default="0")

    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)

    def __str__(self):
        return str(self.pk)

    def mark_booked(self):
        if self.status != 'booked':
            self.status = 'booked'
            self.save()
            return self.status


def quote_pre_save(sender, instance, *args, **kwargs):

    if instance.venue:
        # price pre_save in Total
        instance.total = instance.venue.price


pre_save.connect(quote_pre_save, sender=Quote)


class VenueBookingManager(models.Manager):
    """ Booking Manager """
    def get_or_new(self, request, quote_pk=None):
        quote_obj = get_object_or_404(Quote, pk=quote_pk)
        billing_profile, create = BillingProfile.objects.get_or_new(request)
        qs = self.get_queryset().filter(quote=quote_obj, billing_profile=billing_profile)
        # print(billing_profile)
        # print(qs.count())

        if qs.count() == 1:
            booking_obj = qs.first()
            booking_create = False
        else:
            booking_create = True
            booking_obj = self.create_booking(request, quote_pk=quote_pk)
        return booking_obj, booking_create

    def create_booking(self, request, quote_pk=None):
        quote_obj = get_object_or_404(Quote, pk=quote_pk)
        if request.user.is_authenticated:
            billing_profile, create = BillingProfile.objects.get_or_new(request)
            self.model.objects.create(quote=quote_obj, billing_profile=billing_profile, venue_id=quote_obj.venue.id)
        else:
            return redirect('account:login')


class VenueBooking(models.Model):
    """ Venue Booking or Ordered Object """
    STATUS_TYPE = (
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid')
    )

    status = models.CharField(max_length=15, choices=STATUS_TYPE, default='unpaid', blank=True, null=True)
    booking_id = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Unique Booking Id will Be auto Generate by System"
    )
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, blank=True, null=True)
    quote = models.OneToOneField(Quote, on_delete=models.CASCADE)

    venue_id = models.IntegerField(blank=True, null=True)
    booking_date = models.DateField(blank=True, null=True)
    guest = models.PositiveIntegerField(blank=True, null=True)

    sub_total = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)

    objects = VenueBookingManager()

    def __str__(self):
        return str(self.id)

    def get_absolute_edit_url(self):
        return reverse('booking:bookingUpdate', kwargs={'pk': self.pk})

    def mark_paid(self):
        if self.status != 'paid':
            self.status = 'paid'
            self.save()
            self.quote.mark_booked()
            print(self.quote.status)
            return self.status


def booking_pre_save(sender, instance, *args, **kwargs):
    # if instance.venue is not None:
    #     sub_total = instance.venue.price
    #     if instance.booking_type == 'first_half' or instance.booking_type == 'second_half':
    #         instance.sub_total = sub_total / 2
    #     else:
    #         instance.sub_total = sub_total
    #
    # if instance.sub_total >= 0:
    #     instance.total = instance.sub_total
    print('pre_save_raise now')
    instance.sub_total = instance.quote.total

    if instance.sub_total > 0:
        instance.total = instance.sub_total

    if instance.booking_date is None:
        instance.booking_date = instance.quote.booking_date

    if instance.guest is None:
        instance.guest = instance.quote.guest

    if instance.booking_id is None:
        instance.booking_id = get_random_string_generator()


pre_save.connect(booking_pre_save, sender=VenueBooking)


class Cart(models.Model):
    """ Venue Cart Object """
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    booking_purpose = models.CharField(max_length=25, blank=True, null=True)
    booking_type = models.CharField(max_length=30, blank=True, null=True)

    booking_date = models.DateField(auto_now=False, auto_now_add=False)

    sub_total = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)
    total = models.DecimalField(decimal_places=2, max_digits=8, blank=True, null=True)

    def __str__(self):
        return self.id + '{venue} by {user}'.format(venue=self.venue.name, user=self.user.email)

