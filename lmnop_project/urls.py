"""LMNOPsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from lmn import views, views_users

from django.urls import path, include, re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from lmn.views_autocomplete import VenueAutocomplete


urlpatterns = [
    path('admin/', admin.site.urls),    #Admin site

    path('', include('lmn.urls') ),

    # Django Autocomplete-light calls reverse() on this path without passing a urlconfig
    # argument. An easy fix is to list paths called on by Autocomplete here. 
    re_path(r'^venue-autocomplete/$',
        VenueAutocomplete.as_view(),
         name='venue-autocomplete',)

]
