import json

from .models import Venue

from django.shortcuts import render
from django.http import HttpResponse


def homepage(request):
    return render(request, 'lmn/home.html')

def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        search_qs = Venue.objects.filter(name__istartswith=q)
        results=[]
        for r in search_qs:
            results.append(r.name)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
