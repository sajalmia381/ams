from django.contrib import admin
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.template.loader import get_template
from django import template

from .models import VenueBooking, Cart, Quote
admin.site.register(VenueBooking)

admin.site.register(Cart)


class QuoteAdmin(admin.ModelAdmin):
    list_display = ['pk', 'venue', 'email', 'mobile_no', 'booking_date', 'status']
    actions = ['make_status_confirm', 'make_status_review']

    def make_status_confirm(self, request, queryset):
        queryset.update(status='confirm')
        print(queryset)
        # print(dir(queryset))
        # next_url = reverse('booking:booking_obj', kwargs={'pk': queryset.get('quote')})
        # print(next_url)
        context = {
            'email': 'Clint',
            'confirm_link': 'Example link of booking',
        }

        # try:
        #     message = get_template('booking/email/quote_confirm.txt')
        # except template.TemplateDoesNotExist:
        #     message = "You request of booking is confirm to ready for booking. please complete booking"

        to_email = []

        if queryset.exists():
            for obj in queryset:
                to_email.append(obj.email)
                # context['email'] = obj.email
                # context['confirm_link'] = settings.BASE_URL + reverse('booking:booking_obj', kwargs={'quote_pk': obj.pk})

        subject = "booking confirmed"
        message = get_template('booking/email/quote_confirm.txt').render(context)
        from_email = getattr(settings, 'EMAIL_HOST_USER', None)
        html_message = get_template('booking/email/quote_confirm.html').render(context)

        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, to_email, html_message=html_message)
                pass
            except BadHeaderError:
                pass

    make_status_confirm.short_description = "Make Status Confirm"

    def make_status_review(self, request, queryset):
        queryset.update(status='review')

    make_status_review.short_description = "Make Status Review"


admin.site.register(Quote, QuoteAdmin)
