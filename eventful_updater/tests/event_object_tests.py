from unittest import TestCase
from event_object import EventObject

class TestEventObject(TestCase):

    #TODO Setup event object

    def test_event_object_init(self):
        event = EventObject('asdf', 'aaaf', 'asdf', 'asdf', 'asdf', 'asdf', 'afff')
        self.assertEqual('aaaf', event.date)
        self.assertEqual('afff', event.state)

    def test_event_object_create_performers(self):
        event = EventObject('asdf', 'aaaf', 'asdf', 'asdf', 'asdf', 'asdf', 'afff')
        event.create_performers('crumbs')
        self.assertEqual('crumbs', event.performers)
