from django.conf import settings
from .models import Venue, Artist, Note, Show, CustomUser
from .forms import VenueSearchForm, NewNoteForm, ArtistSearchForm, UserRegistrationForm
from django.shortcuts import render, redirect, get_object_or_404


from .models import Venue, Artist, Note, Show, CustomUser, UserProfile
from .forms import UserRegistrationForm, UserProfileForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone



def user_profile(request, user_pk):
    user = CustomUser.objects.get(pk=user_pk)
    usernotes = Note.objects.filter(user=user.pk).order_by('posted_date').reverse()
    try:
        profile = get_object_or_404(UserProfile, userId=user.pk)
        return render(request, 'lmn/users/user_profile.html', {'user': user, 'notes': usernotes, 'profile': profile})
    except Http404:
        return render(request, 'lmn/users/user_profile.html', {'user': user, 'notes': usernotes})




@login_required
def my_user_profile(request):
    # TODO - editable version for logged-in user to edit own profile
    return redirect('lmn:user_profile', user_pk=request.user.pk)



def register(request):

    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            profile = UserProfile(userId=user.pk)
            profile.save()
            login(request, user)
            return redirect('lmn:homepage')

        else :
            message = 'Please check the data you entered'
            return render(request, 'registration/register.html', { 'form' : form , 'message' : message } )


    else:
        form = UserRegistrationForm()
        return render(request, 'registration/register.html', { 'form' : form } )



def logout_user(request):
    logout_message = 'You have logged out. Come back soon!'
    logout(request)
    return render(request, 'lmn/home.html', {'logout_message': logout_message})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        try:
            instance = get_object_or_404(UserProfile, userId=request.user)
            form = UserProfileForm(request.POST, instance=instance)
            if form.is_valid():
                profile = form.save()
                return redirect('lmn:my_user_profile')
            else:
                message = 'Please check the data you entered'
                return render(request, 'lmn/users/edit_profile.html', {'form': form, 'message': message})
        except Http404:
            form = UserProfileForm(request.POST)
            if form.is_valid():
                profile = form.save()
                return redirect('lmn:my_user_profile')
            else:
                message = 'Please check the data you entered'
                return render(request, 'lmn/users/edit_profile.html', {'form': form, 'message': message})
    else:
        form = UserProfileForm(initial={'userId': request.user})
        return render(request, 'lmn/users/edit_profile.html', {'form': form})
