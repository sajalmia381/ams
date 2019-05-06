from django.contrib import admin
from .models import State, City, BookingPurpose, Venue, VenueBooking

from django.db import models
from django.forms.widgets import CheckboxSelectMultiple, CheckboxInput

admin.site.register(State)

admin.site.register(City)

admin.site.register(BookingPurpose)


class VenueAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }


admin.site.register(Venue, VenueAdmin)


class VenueBookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'venue']
    readonly_fields = ('booking_id', )
    # formfield_overrides = {
    #     models.DateField: {'widget': }
    # }
    exclude = ('booking_id', )

    # def get_readonly_fields(self, request, obj=None):
    #     return ['booking_id']


admin.site.register(VenueBooking, VenueBookingAdmin)