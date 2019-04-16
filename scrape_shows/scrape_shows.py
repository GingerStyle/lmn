"""
This module scrapes event information from the calendar section of First Avenue's website.
Each event will be torn apart, have its pieces put into a list, and used to update a postgres database.
"""

from bs4 import BeautifulSoup
import requests

def make_soup(url):
    html = requests.get(url)
    return BeautifulSoup(html.text, 'html.parser')

def assemble_event(event, date):
    print(event.prettify())


def iterate_siblings(soup):
    """
    Iterate over calendar DIV's, assembling one event at a time.
    """
    calendar = soup.find(class_='view-content')
    date = None
    for child in calendar.children:
        # <h3> tags contain the date of the events between it and the next <h3>.
        if str(child)[0:2] == '<h':
            date = child.span.text
        elif str(child)[0:2] == '<d':
            assemble_event(child, date)



soup = make_soup('https://first-avenue.com/calendar/all/2019')
iterate_siblings(soup)
