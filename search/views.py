from django.shortcuts import render
from venue.models import Venue
from django.views.generic import ListView
from django.db.models import Q


class SearchView(ListView):
    template_name = 'search/search_list.html'

    def get_queryset(self):
        print(self.request.GET)
        query = self.request.GET.get('q', None)
        if query is not None:
            return Venue.objects.filter(Q(name__icontains=query))
        return Venue.objects.all()
