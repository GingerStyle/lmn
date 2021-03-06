from django.test import TestCase, Client

from django.urls import reverse
from django.contrib import auth

from lmn.models import Venue, Artist, Note, Show
from django.contrib.auth.models import CustomUser

import re, datetime
from datetime import timezone

class TestArtistViews(TestCase):

    fixtures = ['testing_artists', 'testing_venues', 'testing_shows']

    def test_all_artists_displays_all_alphabetically(self):
        response = self.client.get(reverse('lmn:artist_list'))

        # .* matches 0 or more of any character. Test to see if
        # these names are present, in the right order

        regex = '.*ACDC.*REM.*Yes.*'
        response_text = str(response.content)

        self.assertTrue(re.match(regex, response_text))
        self.assertEqual(len(response.context['artists']), 3)


    def test_artists_search_clear_link(self):
        response = self.client.get( reverse('lmn:artist_list') , {'search_name' : 'ACDC'} )

        # There is a clear link, it's url is the main venue page
        all_artists_url = reverse('lmn:artist_list')
        self.assertContains(response, all_artists_url)


    def test_artist_search_no_search_results(self):
        response = self.client.get( reverse('lmn:artist_list') , {'search_name' : 'Queen'} )
        self.assertNotContains(response, 'Yes')
        self.assertNotContains(response, 'REM')
        self.assertNotContains(response, 'ACDC')
        # Check the length of artists list is 0
        self.assertEqual(len(response.context['artists']), 0)


    def test_artist_search_partial_match_search_results(self):

        response = self.client.get(reverse('lmn:artist_list'), {'search_name' : 'e'})
        # Should be two responses, Yes and REM
        self.assertContains(response, 'Yes')
        self.assertContains(response, 'REM')
        self.assertNotContains(response, 'ACDC')
        # Check the length of artists list is 2
        self.assertEqual(len(response.context['artists']), 2)


    def test_artist_search_one_search_result(self):

        response = self.client.get(reverse('lmn:artist_list'), {'search_name' : 'ACDC'} )
        self.assertNotContains(response, 'REM')
        self.assertNotContains(response, 'Yes')
        self.assertContains(response, 'ACDC')
        # Check the length of artists list is 1
        self.assertEqual(len(response.context['artists']), 1)


    def test_correct_template_used_for_artists(self):
        # Show all
        response = self.client.get(reverse('lmn:artist_list'))
        self.assertTemplateUsed(response, 'lmn/artists/artist_list.html')

        # Search with matches
        response = self.client.get(reverse('lmn:artist_list'), {'search_name' : 'ACDC'} )
        self.assertTemplateUsed(response, 'lmn/artists/artist_list.html')
        # Search no matches
        response = self.client.get(reverse('lmn:artist_list'), {'search_name' : 'Non Existant Band'})
        self.assertTemplateUsed(response, 'lmn/artists/artist_list.html')

        # Artist detail
        response = self.client.get(reverse('lmn:artist_detail', kwargs={'artist_pk':1}))
        self.assertTemplateUsed(response, 'lmn/artists/artist_detail.html')

        # Artist list for venue
        response = self.client.get(reverse('lmn:artists_at_venue', kwargs={'venue_pk':1}))
        self.assertTemplateUsed(response, 'lmn/artists/artist_list_for_venue.html')


    def test_artist_detail(self):

        ''' Artist 1 details displayed in correct template '''
        # kwargs to fill in parts of url. Not get or post params

        response = self.client.get(reverse('lmn:artist_detail', kwargs={'artist_pk' : 1} ))
        self.assertContains(response, 'REM')
        self.assertEqual(response.context['artist'].name, 'REM')
        self.assertEqual(response.context['artist'].pk, 1)


    def test_get_artist_that_does_not_exist_returns_404(self):
        response = self.client.get(reverse('lmn:artist_detail', kwargs={'artist_pk' : 10} ))
        self.assertEqual(response.status_code, 404)


    def test_venues_played_at_most_recent_shows_first(self):
        ''' For each artist, display a list of venues they have played shows at '''

        # Artist 1 (REM) has played at venue 2 (Turf Club) on two dates

        url = reverse('lmn:venues_for_artist', kwargs={'artist_pk':1})
        response = self.client.get(url)
        shows = list(response.context['shows'].all())
        show1, show2 = shows[0], shows[1]
        self.assertEqual(2, len(shows))

        self.assertEqual(show1.artist.name, 'REM')
        self.assertEqual(show1.venue.name, 'The Turf Club')

        expected_date = datetime.datetime(2017, 2, 2, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(0, (show1.show_date - expected_date).total_seconds())

        self.assertEqual(show2.artist.name, 'REM')
        self.assertEqual(show2.venue.name, 'The Turf Club')
        expected_date = datetime.datetime(2017, 1, 2, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(0, (show2.show_date - expected_date).total_seconds())

        # Artist 2 (ACDC) has played at venue 1 (First Ave)

        url = reverse('lmn:venues_for_artist', kwargs={'artist_pk':2})
        response = self.client.get(url)
        shows = list(response.context['shows'].all())
        show1 = shows[0]
        self.assertEqual(1, len(shows))

        self.assertEqual(show1.artist.name, 'ACDC')
        self.assertEqual(show1.venue.name, 'First Avenue')
        expected_date = datetime.datetime(2017, 1, 21, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(0, (show1.show_date - expected_date).total_seconds())

        # Artist 3 , no shows

        url = reverse('lmn:venues_for_artist', kwargs={'artist_pk':3})
        response = self.client.get(url)
        shows = list(response.context['shows'].all())
        self.assertEqual(0, len(shows))
