from django.test import TestCase, Client

from django.urls import reverse
from django.contrib import auth
from lmn.forms import UserRegistrationForm
from lmn.models import Venue, Artist, Note, Show, UserProfile
from lmn.models import CustomUser
from django.contrib.auth import authenticate
import re, datetime
from datetime import timezone

class TestAddNoteUnauthentictedUser(TestCase):

    fixtures = [ 'testing_artists', 'testing_venues', 'testing_shows' ]  # Have to add artists and venues because of foreign key constrains in show

    def test_add_note_unauthenticated_user_redirects_to_login(self):
        response = self.client.get( '/notes/add/1/', follow=True)  # Use reverse() if you can, but not required.
        # Should redirect to login; which will then redirect to the notes/add/1 page on success.
        self.assertRedirects(response, '/accounts/login/?next=/notes/add/1/')


class TestUserProfile(TestCase):
    fixtures = [ 'testing_user_profiles.json', 'testing_users', 'testing_artists', 'testing_venues', 'testing_shows', 'testing_notes' ]  # Have to add artists and venues because of foreign key constrains in show
    def test_showing_user_profile(self):
        user = CustomUser.objects.get(pk='1')
        profile = UserProfile.objects.get(userId=user)
        self.client.force_login(user)
        response = self.client.get(reverse('lmn:my_user_profile'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"Favorite Band: {profile.favorite_band}")

    def test_user_without_user_profile(self):
        user = CustomUser.objects.get(pk='3')
        self.client.force_login(user)
        response = self.client.get(reverse('lmn:my_user_profile'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have not updated your user profile. Press the pencil icon to update it.")

    def test_update_existing_profile(self):
        user = CustomUser.objects.get(pk='1')
        oldProfile = UserProfile.objects.get(userId=user.pk)
        self.client.force_login(user)
        response = self.client.post(reverse('lmn:edit_profile'), {'userId': user.pk, 'birthday': '1998-05-12',
                                                                    'favorite_band': 'Wiz Khalifa'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,  'lmn/users/user_profile.html')
        newProfile = UserProfile.objects.get(userId=user.pk)
        self.assertNotEqual(newProfile.favorite_band, oldProfile.favorite_band)
        self.assertNotContains(response, "You have not updated your user profile. Press the pencil icon to update it.")
        self.assertContains(response, f"Favorite Band: {newProfile.favorite_band}")

    # verify correct list of reviews for a user
    def test_user_profile_show_list_of_their_notes(self):
        # get user profile for user 2. Should have 2 reviews for show 1 and 2.
        response = self.client.get(reverse('lmn:user_profile', kwargs={'user_pk':2}))
        notes_expected = list(Note.objects.filter(user=2))
        notes_provided = list(response.context['notes'])
        self.assertTemplateUsed('lmn/users/user_profile.html')
        self.assertEqual(notes_expected, notes_provided)

        # test notes are in date order, most recent first.
        # Note PK 3 should be first, then PK 2
        first_note = response.context['notes'][0]
        self.assertEqual(first_note.pk, 3)

        second_note = response.context['notes'][1]
        self.assertEqual(second_note.pk, 2)


    def test_user_with_no_notes(self):
        response = self.client.get(reverse('lmn:user_profile', kwargs={'user_pk':3}))
        self.assertFalse(response.context['notes'])


class TestUserAuthentication(TestCase):

    ''' Some aspects of registration (e.g. missing data, duplicate username) covered in test_forms '''
    ''' Currently using much of Django's built-in login and registration system'''

    def test_user_registration_logs_user_in(self):
        response = self.client.post(reverse('lmn:register'), {'username':'sam12345', 'email':'sam@sam.com', 'password1':'feRpj4w4pso3az', 'password2':'feRpj4w4pso3az', 'first_name':'sam', 'last_name' : 'sam'}, follow=True)

        # Assert user is logged in - one way to do it...
        user = auth.get_user(self.client)
        self.assertEqual(user.username, 'sam12345')

        # This works too. Don't need both tests, added this one for reference.
        # sam12345 = User.objects.filter(username='sam12345').first()
        # auth_user_id = int(self.client.session['_auth_user_id'])
        # self.assertEqual(auth_user_id, sam12345.pk)


    def test_user_registration_redirects_to_correct_page(self):
        # TODO If user is browsing site, then registers, once they have registered, they should
        # be redirected to the last page they were at, not the homepage.
        response = self.client.post(reverse('lmn:register'), {'username':'sam12345', 'email':'sam@sam.com', 'password1':'feRpj4w4pso3az@1!2', 'password2':'feRpj4w4pso3az', 'first_name':'sam', 'last_name' : 'sam'}, follow=True)

        self.assertRedirects(response, reverse('lmn:homepage'))   # FIXME Fix code to redirect to last page user was on before registration.
        self.assertContains(response, 'sam12345')  # Homepage has user's name on it


class TestRegistrationUser(TestCase):
    def test_form_render_registration_template(self):
        response = self.client.post(reverse('lmn:register'), {'username': 'qaalib101','email': 'qaalibomer@gmail.com','first_name': 'qaalib', 'last_name': 'farah',
                                          'password1': 'feRpj4w4pso3az', 'password2': 'feRpj4w4pso3az'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lmn/users/user_profile.html')


class TestLogoutUser(TestCase):

    def test_logout_message(self):
        self.client.post(reverse('lmn:register'),
                                    {'username': 'sam12345', 'email': 'sam@sam.com', 'password1': 'feRpj4w4pso3az',
                                     'password2': 'feRpj4w4pso3az', 'first_name': 'sam', 'last_name': 'sam'},
                                    follow=True)
        user = auth.get_user(self.client)
        response = self.client.post(reverse('lmn:logout'), follow=True)
        logged_out = response.wsgi_request.user
        self.assertNotEqual(user, logged_out)
        self.assertTemplateUsed(response, 'lmn/home.html')
        self.assertContains(response, 'You have logged out. Come back soon!')

