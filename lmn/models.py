from django.db import models
from django.conf import settings
from django.contrib.postgres import fields
from django.contrib.auth.models import AbstractUser, BaseUserManager
import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Every model gets a primary key field by default.

# Users, venues, shows, artists, notes

# User is provided by Django. The email field is not unique by
# default, so add this to prevent more than one user with the same email.



''' A music artist '''
class Artist(models.Model):
    name = models.CharField(max_length=200, blank=False);

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
    title = models.CharField(max_length=100, blank=False)
    show_date = models.DateTimeField(blank=False)
    artists = models.ManyToManyField(Artist)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)

    def __str__(self):
        return '{} with artist {} at {} on {}'.format(self.title, self.artists, self.venue, self.show_date)


''' One user's opinion of one show. '''
class Note(models.Model):
    Rating = (
        (1, 'Poor'),
        (2, 'Average'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent')
    )
    show = models.ForeignKey(Show, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    text = models.TextField(max_length=1000, blank=False)
    posted_date = models.DateTimeField(blank=False)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    rating = models.IntegerField(choices=Rating, default=3)
    likes = models.IntegerField(null=True, default=0)

    def add_dislike(self):
        self.likes -= 1
        self.save()

    def add_like(self):
        self.likes += 1
        self.save()

    def publish(self):
        self.posted_date = datetime.datetime.today()
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
    username = models.CharField(max_length=128, blank=False, unique=True)
    email = models.CharField(max_length=128, unique=True, blank=False)
    first_name = models.CharField(max_length=128, blank=False)
    last_name = models.CharField(max_length=128, blank=False)
    objects = MyUserManager()


    def __str__(self):
        return self.username



class UserProfile(models.Model):
    favorite_band = models.CharField(max_length=128, blank=True)
    birthday = models.DateField(blank=True)
    userId = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return "{}'s profile".format(self.userId)


class LikeNote(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    value = models.IntegerField(null=True, blank=True, default=0)

    def dislike(self):
        self.value = -1
        self.save()

    def like(self):
        self.value = 1
        self.save()

