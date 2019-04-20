from django.shortcuts import get_object_or_404
from django.views import generic
from .models import Venue


class HomeView(generic.TemplateView):
    template_name = 'home.html'


class VenueListView(generic.ListView):
    queryset = Venue.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VenueListView, self).get_context_data(**kwargs)
        return context


class VenueDetailView(generic.DetailView):
    model = Venue

    def get_context_data(self, *args, **kwargs):
        context = super(VenueDetailView, self).get_context_data(**kwargs)
        return context

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Venue, pk=pk)