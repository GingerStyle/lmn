from django.test import TestCase, Client
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import auth

from lmn.models import Venue, Artist, Note, Show, LikeNote
from lmn.models import CustomUser

import re, datetime
from datetime import timezone

class MostPopularShow(TestCase):
    fixtures = ['testing_likenotes', 'testing_users', 'testing_artists', 'testing_venues', 'testing_shows',
                'testing_notes']
    def test_show_with_most_notes(self):
        user = CustomUser.objects.first()
        self.client.force_login(user)
        response = self.client.get(reverse('lmn:popular_shows'), follow=True)
        self.assertNotContains(response, 'No shows.')
        self.assertEqual(response.status_code, 200)
        first = response.context['shows'][0]
        show = Show.objects.get(pk=2)
        self.assertEqual(first.pk, show.pk)
