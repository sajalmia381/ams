from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save

# third party
from multiselectfield import MultiSelectField

from ams.utils import get_random_string_generator


class State(models.Model):

    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class City(models.Model):

    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class BookingPurpose(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Venue(models.Model):

    BOOKING_TYPE = (
        ('full_day', 'Full Day'),
        ('first_half', 'First Half'),
        ('second_half', 'Second Half'),
    )

    # Model Field
    name = models.CharField(max_length=250)
    seating_capacity = models.PositiveIntegerField()
    standing_capacity = models.PositiveIntegerField(default=3100)
    address = models.CharField(max_length=300)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    zip_code = models.PositiveIntegerField()
    booking_type = MultiSelectField(choices=BOOKING_TYPE)
    booking_purpose = models.ManyToManyField(BookingPurpose)
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('venue:venueDetailUrl', kwargs={'pk': self.pk})


class VenueBooking(models.Model):
    booking_id = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Unique Booking Id will Be auto Generate by System"
    )
    name = models.CharField(max_length=30)
    mobile_no = models.IntegerField(blank=True)
    email = models.EmailField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    # booking_purposse
    # booking_type
    booking_date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.booking_id


def booking_id_pre_save(sender, instance, *args, **kwargs):
    if instance.booking_id is None:
        instance.booking_id = get_random_string_generator()


pre_save.connect(booking_id_pre_save, sender=VenueBooking)