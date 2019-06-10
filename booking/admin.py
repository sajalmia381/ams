from django.contrib import admin
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

        context = {
            'email': 'email',
            'confirm_link': 'path'
        }

        # try:
        #     message = get_template('booking/email/quote_confirm.txt')
        # except template.TemplateDoesNotExist:
        #     message = "You request of booking is confirm to ready for booking. please complete booking"

        subject = "booking confirmed"
        message = get_template('booking/email/quote_confirm.txt').render(context)
        from_email = getattr(settings, 'EMAIL_HOST_USER', None)
        to_email = []
        html_message = get_template('booking/email/quote_confirm.html').render(context)
        for obj in queryset:
            to_email.append(obj.email)

        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, to_email, html_message=html_message)
            except BadHeaderError:
                pass

    make_status_confirm.short_description = "Make Status Confirm"

    def make_status_review(self, request, queryset):
        queryset.update(status='review')

    make_status_review.short_description = "Make Status Review"


admin.site.register(Quote, QuoteAdmin)