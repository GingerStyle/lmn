import json

from lmn.views import autocompleteModel

from django.test import TestCase, client

class TestAutocompleteView(TestCase):

    fixtures = ['testing_artists', 'testing_venues', 'testing_shows']

    # django.db.utils.ProgrammingError: relation "auth_group" does not exist
    def test_not_ajax_req_fails(self):
        res1 = self.client.get('/ajax_calls/search/venue-query')
        res2 = self.client.get('/ajax_calls/search/venue-query')


        self.assertContains(res1, 'fail')
        self.assertContains(res2, 'fail')

    def test_ajax_req_200(self):
        res1 = self.client.get('/ajax_calls/search/venue-query',
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        res2 = self.client.get('/ajax_calls/search/artist-query',
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res2.status_code, 200)

    def test_ajax_req_404(self):
        res = self.client.get('/ajax_calls/search/bad-query',
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(res.status_code, 404)

    # This test fails. I think res contains an empty body for some reason.
    def test_queries_return_proper_info(self):
        res = self.client.post('/ajax_calls/search/venue-query',
                               {'term': 'Turf'})

        self.assertContains(res.json(), "The Turf Club")
