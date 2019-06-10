from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseForbidden
from django.views.generic.edit import FormMixin

from django.views import generic
from .models import Venue, BookingPurpose
from .filters import VenueFilter
from .forms import VenueCreateForm
from booking.forms import VenueBookingForm, CartForm, QuoteForm
from billing.models import BillingProfile
from ams.utils import get_random_string_generator

class HomeView(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['booking_purpose'] = BookingPurpose.objects.all().order_by('name')[:6]
        context['popular_venues'] = Venue.objects.all()[:12]
        return context


class VenueListView(generic.ListView):
    queryset = Venue.objects.all()
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filters'] = VenueFilter(self.request.GET, queryset=Venue.objects.all())
        return context


class VenueDetailView(generic.DetailView, FormMixin):
    model = Venue
    form_class = QuoteForm

    def get_context_data(self, *args, **kwargs):
        context = super(VenueDetailView, self).get_context_data(**kwargs)
        object_city = context['object'].city
        object_pk = context['object'].pk
        context['similar_city_objects'] = Venue.objects.filter(city=object_city).exclude(pk=object_pk)[:3]
        # context['form'] = self.get_form() # note: default context in form mixin

        # print(dir(context['similar_city_objects']))
        # print(context['similar_city_objects'] is not None)
        # print(context['similar_city_objects'])
        # print(context['form'])
        return context

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Venue, pk=pk)

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        print(self.object)
        form = self.get_form()

        if form.is_valid():
            instance = form.save(commit=False)
            instance.venue = self.object
            print("form valid", instance)
            instance.save()
            return self.form_valid(form)
        else:
            print('form not valid', form.errors)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('booking:quote_success')

    # def post(self, request, *args, **kwargs):
    #     # When booking form submit
    #     if not request.user.is_authenticated:
    #         # check user is authenticated
    #         return redirect('account:login')
    #
    #     self.object = self.get_object()
    #
    #     form = self.get_form()
    #
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         print('form is not valid')
    #         return self.form_invalid(form)
    #
    # def form_valid(self, form):
    #     instance = form.save(commit=False)
    #     instance.billing_profile = BillingProfile.objects.get_or_new(self.request)[0]
    #     instance.venue = self.get_object()
    #     print(instance.pk)
    #     # instance.save()
    #     return super().form_valid(form)
    #
    # def get_success_url(self):
    #     return reverse('venue:venueDetailUrl', kwargs={'pk': self.object.pk})


# @method_decorator(login_required, name='dispatch')
class VenueCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = VenueCreateForm
    template_name = 'venue/venue_create_form.html'


# class VenueBookingView(generic.CreateView):
#     form_class = VenueBookingForm
#     template_name = 'venue/venue_booking_form.html'
#
#     def form_valid(self, form):
#         print(form.instance)
#         return super(VenueBookingView, self).form_valid(form)
#
#     def dispatch(self, request, *args, **kwargs):
#         print(kwargs)
#         print(args)
#         print(request)
#         return super(VenueBookingView, self).dispatch(request, *args, **kwargs)
#
#
# def venue_booking_view(request, pk):
#     template_name = 'venue/venue_booking_form.html'
#     instance = VenueBookingForm()
#     # print(dir(instance.fields.items))
#     # print(dir(request))
#     # print(request.user)
#     # print(dir(request.user))
#     # print(request.COOKIES)
#     context = {
#         'form': instance,
#     }
#     return render(request, template_name, context)
