from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.shortcuts import redirect

User = settings.AUTH_USER_MODEL

import stripe
stripe.api_key = 'sk_test_zHe2wZES61XlUKWWM9yUqk2P00GCKl0hWw'


def set_default_email_address():
    """Set Billing Profile email if"""


class BillingProfileManager(models.Manager):
    """ Billing Profile Manager """

    def get_or_new(self, request):
        user = request.user
        if user.is_authenticated:
            obj, create = BillingProfile.objects.get_or_create(user=user, email=user.email)
        else:
            return redirect('account:login')
        return obj, create


class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()

    is_active = models.BooleanField(default=True)

    # stripe
    customer_id = models.CharField(max_length=120, blank=True, null=True)

    timestamp = models.DateTimeField(auto_now=True)
    update_on = models.DateTimeField(auto_now_add=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.user.email

    def set_user(self):
        """ Set Billing user instance of Authenticated User"""
        print(self.request.user.is_authenticated())


def billing_profile_customer_create(sender, instance, *args, **kwargs):
    """ Create stripe Customer in stripe, and stripe id as Billing profile customer id"""
    if not instance.customer_id and instance.email:
        customer = stripe.Customer.create(email=instance.email)
        print(customer)
        instance.customer_id = customer.id


pre_save.connect(billing_profile_customer_create, sender=BillingProfile)


def user_create_receiver(sender, instance, created, *args, **kwargs):
    """ User Billing Profile Created """
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_create_receiver, sender=User)


# class Card(models.Model):
#