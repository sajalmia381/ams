from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views import generic
from .models import Venue, BookingPurpose
from .filters import VenueFilter
from .forms import VenueCreateForm, VenueBookingForm


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
        print(self.request.GET)
        print('filter', context['filters'])
        return context

    # def get_queryset(self):
    #     if self.request.method == "GET" and self.request.GET:
    #         if '?' in self.request.GET:
    #             return self.filters
    #     return Venue.objects.all()


def venue_list_view(request):
    template_name = 'venue/venue_list.html'
    filter_list = VenueFilter(request.GET, queryset=Venue.objects.all())
    # print(type(filter_list))
    # print(dir(filter_list))
    # print(filter_list.filter_queryset)
    # print(type(filter_list.filter_queryset))
    # print(filter_list.queryset)

    object_list = filter_list.queryset
    context = {
        'object_list': object_list,
        'filters': filter_list,
    }
    return render(request, template_name, context)


class VenueDetailView(generic.DetailView):
    model = Venue

    def get_context_data(self, *args, **kwargs):
        context = super(VenueDetailView, self).get_context_data(**kwargs)
        return context

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Venue, pk=pk)


@method_decorator(login_required, name='dispatch')
class VenueCreateView(generic.CreateView):
    form_class = VenueCreateForm
    template_name = 'venue/venue_create_form.html'


class VenueBookingView(generic.CreateView):
    form_class = VenueBookingForm
    template_name = 'venue/venue_booking_form.html'

    def form_valid(self, form):
        print(form.instance)
        return super(VenueBookingView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        print(kwargs)
        print(args)
        print(request)
        return super(VenueBookingView, self).dispatch(request, *args, **kwargs)


def venue_booking_view(request, pk):
    template_name = 'venue/venue_booking_form.html'
    instance = VenueBookingForm()
    # print(dir(instance.fields.items))
    # print(dir(request))
    # print(request.user)
    # print(dir(request.user))
    # print(request.COOKIES)
    context = {
        'form': instance,
    }
    return render(request, template_name, context)
