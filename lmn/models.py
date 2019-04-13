from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import datetime
from django.conf import settings
from django.contrib.postgres import fields
# Every model gets a primary key field by default.

# Users, venues, shows, artists, notes

# User is provided by Django. The email field is not unique by
# default, so add this to prevent more than one user with the same email.


''' A music artist '''
class Artist(models.Model):
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return "Artist: " + self.name


''' A venue, that hosts shows. '''
class Venue(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True)
    city = models.CharField(max_length=200, blank=False)
    state = models.CharField(max_length=2, blank=False)  # What about international?

    def __str__(self):
        return 'Venue name: {} in {}, {}'.format(self.name, self.city, self.state)


''' A show - one artist playing at one venue at a particular date. '''
class Show(models.Model):
    show_date = models.DateTimeField(blank=False)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return 'Show with artist {} at {} on {}'.format(self.artist, self.venue, self.show_date)


''' One user's opinion of one show. '''
class Note(models.Model):
    show = models.ForeignKey(Show, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(max_length=1000, blank=False)
    posted_date = models.DateTimeField(blank=False)


    def publish(self):
        posted_date = datetime.datetime.today()
        self.save()

    def __str__(self):
        return 'Note for user ID {} for show ID {} with title {} text {} posted on {}'.format(self.user, self.show, self.title, self.text, self.posted_date)


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password):

        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    username = fields.CICharField(max_length=128, blank=False, unique=True)
    email = fields.CICharField(max_length=128, unique=True, blank=False)
    first_name = models.CharField(max_length=128, blank=False)
    last_name = models.CharField(max_length=128, blank=False)
    objects = MyUserManager()


    def __str__(self):
        return self.username
