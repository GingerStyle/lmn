import json

from .models import Venue, Artist

from django.shortcuts import render
from django.http import HttpResponse


def homepage(request):
    return render(request, 'lmn/home.html')

# Code at https://medium.com/@ninajlu/django-ajax-jquery-search-autocomplete-d4b4bf6494dd
def autocompleteModel(request, query_type):
    if request.is_ajax():
        q = request.GET.get('term', '')
        if query_type is 'Venue':
            search_qs = Venue.objects.filter(name__icontains=q)
        elif query_type is 'Artist':
            search_qs = Artist.objects.filter(name__icontains=q)
        results=[]
        for r in search_qs:
            results.append(r.name)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
