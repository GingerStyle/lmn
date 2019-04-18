class EventObject():

    def __init__(self, event_id, date, title, venue_id, venue_name, city, state):
        self.event_id = event_id
        self.date = date
        self.title = title
        self.venue_id = venue_id
        self.venue_name = venue_name
        self.city = city
        self.state = state

    def create_performers(self, performers):
        self.performers = performers

    def __str__(self):
        return '================\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n================'.format(self.event_id, self.date, self.title, self.venue_id, self.venue_name, self.city, self.state)
