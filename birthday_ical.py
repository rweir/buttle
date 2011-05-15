#!/usr/bin/python

from optparse import OptionParser
from datetime import datetime, date
import os.path
import string

from icalendar import Calendar, Event, UTC

from buttle.parser import parse_line

parser = OptionParser()
parser.add_option("-i", "--input", dest="input",
                  help="path to bbdb file", metavar="FILE", default=os.path.expanduser("~/.bbdb"))
parser.add_option("-o", "--output", dest="output",
                  help="output path for ical file", metavar="FILE", default="birthdays.ics")

(options, args) = parser.parse_args()

def build_vcal_item(data):
    event = Event()
    name = " ".join(data[name] for name in ['firstname', 'lastname'] if data[name])
    summary = "%s's Birthday" % name
    d = data['random']['anniversary']
    now = date(date.today().year, d.month, d.day)
    if now > date.today():
        d = date(now.year, d.month, d.day)
    else:
        d = date(now.year + 1, d.month, d.day)
    event.add('summary', summary)
    event.add('dtstart', d)
    event.add('dtend', d)
    event.add('dtstamp', datetime.now(UTC))
    event['uid'] = "buttle/" + ''.join(c for c in summary if c in string.ascii_letters + string.digits).lower() + "-" + data['random']['anniversary'].isoformat()
    return event

calendar = Calendar()
calendar.add('version', '2.0')
calendar.add('prodid', '-//buttle//ertius.org//')

with open(options.input) as f:
        for line in f:
            data = parse_line(line)
            if data and 'anniversary' in data['random']:
                event = build_vcal_item(data)
                calendar.add_component(event)

with open(options.output, 'w') as output:
    output.write(calendar.as_string()[:-2])
