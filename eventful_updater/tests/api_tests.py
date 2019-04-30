from unittest import TestCase
from api_request import EventfulAPI
import os

class TestEventfulAPI(TestCase):

    EVENTFUL_KEY = os.environ['EVENTFUL_KEY']
    eventful_api = EventfulAPI()

    def test_get_events_200_response(self):
        res = self.eventful_api.get_response(self.EVENTFUL_KEY)
        self.assertTrue(res)

