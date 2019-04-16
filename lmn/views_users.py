from django.shortcuts import render, redirect
from .models import Venue, Artist, Note, Show, CustomUser
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.utils import timezone



def user_profile(request, user_pk):
    user = CustomUser.objects.get(pk=user_pk)
    usernotes = Note.objects.filter(user=user.pk).order_by('posted_date').reverse()
    return render(request, 'lmn/users/user_profile.html', {'user' : user , 'notes' : usernotes })



@login_required
def my_user_profile(request):
    # TODO - editable version for logged-in user to edit own profile
    return redirect('lmn:user_profile', user_pk=request.user.pk)


def login_and_signup(request):
    signUpForm = UserRegistrationForm()
    if request.method == 'POST':
        loginForm = UserLoginForm(request.POST)
        next = ''
        if 'url' in request.POST.keys():
            next = request.POST['url']
        if loginForm.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            if next != "":
                return redirect(next)
            else:
                return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            message = 'Please enter a correct username and password. Note that both fields may be case-sensitive.'
            return render(request, 'registration/login.html', { 's_form' : signUpForm, 'l_form': loginForm,'message' : message } )

    else:
        loginForm = UserLoginForm()
        return render(request, 'registration/login.html', { 's_form' : signUpForm, 'l_form': loginForm} )



def register(request):
    signUpForm = UserRegistrationForm()
    loginForm = UserLoginForm()
    if request.method == 'POST':
        next = ''
        if 'url' in request.POST.keys():
            next = request.POST['url']
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            if next != "":
                return redirect(next)
            else:
                return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            message = 'Please check the data you entered'
            return render(request, 'registration/login.html', {'s_form': signUpForm, 'l_form': loginForm, 'message':message})
