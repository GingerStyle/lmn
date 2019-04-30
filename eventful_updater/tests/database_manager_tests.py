from unittest import TestCase

from event_object import EventObject
import database_manager.*

class TestDatabaseManager(TestCase):

    def test_upsert_show_no_artists(self):
        event = EventObject('E0-001-125874574-4',
                            '2019-11-29 14:00:00',
                            'Big Event',
                            'V0-001-000176408-9',
                            'Orchestra Hall',
                            'Minneapolis',
                            'MN')
        upsert_show(event)
