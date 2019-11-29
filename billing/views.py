from django.shortcuts import render, reverse, redirect
from django.conf import settings
from django.utils.http import is_safe_url
from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_protect
from django.views import generic

from django.contrib.auth.decorators import login_required

import stripe

from .models import BillingProfile, Card

STRIPE_PUB_KEY = getattr(settings, 'STRIPE_PUB_KEY', None)

@login_required
def card_method_view(request):
    """ Booking Checkout View """
    template_name = 'billing/card-method.html'

    api_end_url = reverse('billing:card_method_endpoint')

    billing_profile, billing_profile_create = BillingProfile.objects.get_or_new(request)
    if not billing_profile:
        return redirect('account:dashboard')

    # print(request.POST.get('next'))
    # if request.method == "POST":
    #     print(request.POST)
    #     print(request.POST['stripeToken'])
    # print(request.method)

    next_url = None

    next_ = request.GET.get('next')
    next_referer = request.META.get('HTTP_REFERER')

    if is_safe_url(next_, request.get_host()):
        next_url = next_
    elif next_referer:
        next_url = next_referer
    print(next_url)
    context = {
        'stripe_pub_key': STRIPE_PUB_KEY,
        'next_url': next_url,
        'api_end_url': api_end_url
    }

    return render(request, template_name, context)


class CardMethodView(generic.TemplateView):
    template_name = 'billing/card-method.html'

    def get_context_data(self, **kwargs):
        request = self.request
        context = super(CardMethodView, self).get_context_data(**kwargs)

        api_end_url = reverse('billing:card_method_endpoint')

        billing_profile, billing_profile_create = BillingProfile.objects.get_or_new(request)
        if not billing_profile:
            return redirect('account:dashboard')

        next_url = None
        next_post = request.POST.get('next')
        next_ = request.GET.get('next')

        print(next_)
        if is_safe_url(next_, request.get_host()):
            next_url = next_
            print(next_url)

        context['api_end_url'] = api_end_url
        context['stripe_pub_key'] = STRIPE_PUB_KEY
        context['next_url'] = next_url
        return context


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

        return JsonResponse({'message': 'Successfully! Your Card Added'})
    return HttpResponse("error", status=401)