from django.contrib import admin
from .models import State, City, BookingPurpose, Venue

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
