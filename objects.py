#!/usr/bin/env python

from datetime import datetime

class File():
    """ Object to record information about stored files."""
    def __init__(self, name, sha1, modified, data):
        self.name = name
        self.sha1 = sha1
        self.modified = self.parse_datetime(modified)
        self.bin = data

    def all(self):
        """ Returns tuple of all attributes in above order."""
        return (self.name, self.sha1, self.modified, self.bin)

    def parse_datetime(self, dt):
        """ Parse date without timezone.
        If from Box.com directly, dt will be string with specific format.
        Otherwise, dt will already be a datetime.datetime object.
        
        Return (datetime.datetime): datetime object parsed without timezone.
        """
        if isinstance(dt, str):
            return datetime.strptime(dt[:-6], "%Y-%m-%dT%H:%M:%S")
        elif isinstance(dt, datetime):
            return dt
        else:
            raise TypeError("Must be Box formatted str or datetime object")

    def __repr__(self):
        return "<File object '%s': %s>" % (str(self.name), str(self.sha1)[:6])
