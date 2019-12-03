from django import forms
from booking.models import VenueBooking, Cart, Quote
from billing.models import BillingProfile


class VenueBookingForm(forms.ModelForm):

    # def __init__(self, quote_pk=None, *args, **kwargs):
    #     """ Initial date """
    #     super(VenueBookingForm, self).__init__(*args, **kwargs)
    #     print(self.fields['quote'])
        # print(self.fields[''])
        # print(kwargs)
        # if self.fields['sub_total']:
        #     print(dir(self.fields['sub_total']))
        #     print("sub_total", self.fields['sub_total'].clean)

    class Meta:
        model = VenueBooking

        fields = '__all__'
        widgets = {
            # 'quote': forms.SelectMultiple(attrs={'readonly': 'readonly'}),
            # 'billing_profile': forms.TextInput(attrs={'readonly': 'readonly'}),
            'sub_total': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'total': forms.NumberInput(attrs={'readonly': 'readonly'})
        }


class VenueBookingUpdate(forms.ModelForm):

    class Meta:
        model = VenueBooking
        fields = '__all__'

    sub_total = forms.DecimalField(widget=forms.NumberInput(attrs={'readonly': 'readonly'}))


class CartForm(forms.ModelForm):

    class Meta:
        model = Cart
        fields = ('booking_date', 'total')

        widgets = {
            'booking_date': forms.DateInput(attrs={'class': 'form-control date_calender_view'})
        }


class QuoteForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(QuoteForm, self).__init__(*args, **kwargs)
    #     print(user)

    class Meta:
        model = Quote
        fields = ['booking_date', 'booking_purpose', 'guest', 'name', 'email', 'mobile_no']

    # def clean_booking_date(self):
    #     date = self.cleaned_data.get('booking_date')
    #     print(dir(self))
    #     # booking date list create
    #     booked_date_list = []
    #     booked_obj = VenueBooking.objects.all()
    #     for obj in booked_obj:
    #         booked_date_list.append(obj.booking_date.strftime("%Y-%m-%d"))
    #
    #     if date.strftime("%Y-%m-%d") in booked_date_list:
    #         raise forms.ValidationError("This venue is already booked at this date")
    #     return date