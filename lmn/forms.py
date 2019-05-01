from django import forms
from .models import Note, CustomUser, UserProfile

from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError


class VenueSearchForm(forms.Form):
    search_name = forms.CharField(label='Venue Name', max_length=200)


class ArtistSearchForm(forms.Form):
    search_name = forms.CharField(label='Artist Name', max_length=200)


class NewNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ('title', 'text', 'rating', 'image')


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


    def clean_username(self):

        username = self.cleaned_data['username']

        if not username:
            raise ValidationError('Please enter a username')

        if CustomUser.objects.filter(username__iexact=username).exists():
            raise ValidationError('A user with that username already exists')

        return username


    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name:
            raise ValidationError('Please enter your first name')

        return first_name


    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name:
            raise ValidationError('Please enter your last name')

        return last_name


    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError('Please enter an email address')

        if CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError('A user with that email address already exists')

        return email


    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    YEARS = [x for x in range(1940, 2021)]
    birthday = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))
    userId = forms.ModelChoiceField(queryset=CustomUser.objects.filter(), widget=forms.HiddenInput())
    class Meta:
        model = UserProfile
        fields = ('favorite_band', 'birthday', 'userId')

