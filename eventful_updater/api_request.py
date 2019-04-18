import json

from event_object import EventObject

import requests
from requests.exceptions import HTTPError

URL = 'http://api.eventful.com/json/events/search'

class EventfulAPI():

    def get_response(self, key):
        """
        Query Eventful API for music events around Minneapolis
        """
        parameters = {'l': 'Minneapolis', 'c': 'music', 'app_key': {key}}

        try:
            res = requests.get(URL, params=parameters)
            res.raise_for_status()
        except HTTPError as http_err:
            print('HTTP error: {}'.format(http_err))
        except Exception as exc:
            print('Exception: {}'.format(exc))
        else:
            return res

    def package_events(self, res):
        event_list = json.loads(res.text)['events']['event']
        packaged_events = []

        for event in event_list:
            event_obj = EventObject(event['id'],
                                    event['start_time'],
                                    event['title'],
                                    event['venue_id'],
                                    event['venue_name'],
                                    event['city_name'],
                                    event['region_abbr'])
            packaged_events.append(event_obj)

        return packaged_events

import os
import json

key = os.environ['EVENTFUL_KEY']
eventful_api = EventfulAPI()
res = eventful_api.get_response(key)
events = eventful_api.package_events(res)

for event in events:
    print(str(event))
