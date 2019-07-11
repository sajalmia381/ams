from django.contrib import admin
from .models import BillingProfile, Charge, Card
import stripe

admin.site.register(BillingProfile)


class CardAdmin(admin.ModelAdmin):

    actions = ['card_delete']

    def card_delete(self, request, queryset):
        pass


admin.site.register(Card, CardAdmin)


admin.site.register(Charge)