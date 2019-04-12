from django.db import models

BOOKING_TYPE = (
    ('full day', 'Full Day'),
    ('first Half', 'First Half'),
    ('second Half', 'Second Half'),
)


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
    name = models.CharField(max_length=250)
    seating_capacity = models.PositiveIntegerField()
    address = models.CharField(max_length=300)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    zip_code = models.PositiveIntegerField()
    booking_type = models.CharField(choices=BOOKING_TYPE, max_length=15)
    booking_purpose = models.ManyToManyField(BookingPurpose)
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.name