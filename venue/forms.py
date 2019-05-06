from django import forms
from .models import (VenueBooking, Venue)


class VenueCreateForm(forms.ModelForm):

    class Meta:
        model = Venue
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name: '}),
            'seating_capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Seating Capacity: '}),
            'standing_capacity': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Standing Capacity: '}
            ),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address: '}),
            'zip_code': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code: '}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price For Full Day: '}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Write Description for Your Venue'}
            ),

            'image': forms.FileInput(attrs={'class': 'btn btn-primary btn-block'}),

            'booking_purpose': forms.CheckboxSelectMultiple()
        }


class VenueBookingForm(forms.ModelForm):
    class Meta:
        model = VenueBooking
        # fields = ('booking_type', 'booking_date', )
        fields = '__all__'
