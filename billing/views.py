from django.shortcuts import render, reverse, redirect
from django.conf import settings
from django.utils.http import is_safe_url
from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_protect

import stripe

from .models import BillingProfile, Card

STRIPE_PUB_KEY = getattr(settings, 'STRIPE_PUB_KEY', None)


def card_method_view(request):
    """ Booking Checkout View """
    template_name = 'billing/card-method.html'

    if request.method == "POST":
        print(request.POST)
        print(request.POST['stripeToken'])
    print(request.method)

    api_end_url = reverse('billing:card_method_endpoint')

    billing_profile, billing_profile_create = BillingProfile.objects.get_or_new(request)

    if not billing_profile:
        return redirect('account:dashboard')

    next_url = None
    next_ = request.GET.get('next')
    print(next_)
    if is_safe_url(next_, request.get_host()):
        next_url = next_
        print(next_url)
    context = {
        'stripe_pub_key': STRIPE_PUB_KEY,
        'next_url': next_url,
        'api_end_url': api_end_url
    }

    return render(request, template_name, context)


def card_method_view_api(request):
    if request.method == "POST" and request.is_ajax():
        # print("post", request.POST)
        # print("ajax", request.is_ajax())

        billing_profile, billing_profile_create = BillingProfile.objects.get_or_new(request)
        if not billing_profile:
            return HttpResponse('Billing not found')

        token = request.POST.get('token')
        # print('token ', token)
        if token is not None:
            card = Card.objects.add_new(billing_profile, token)
            print(card)

        return JsonResponse({'message': 'this is success url done'})
    return HttpResponse("error", status=401)