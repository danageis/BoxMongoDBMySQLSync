#!/usr/bin/env python

import os
from hashlib import sha1 as func_sha1
from datetime import datetime

class File():
    """ Object to record information about stored files."""
    def __init__(self, name, sha1, modified, data):
        self.name = name
        self.sha1 = sha1
        self.modified = self.parse_datetime(modified)
        self.bin = data

    @classmethod
    def from_path(cls, path):
        """ Constructor to create File object from file at path. """
        name = os.path.basename(path)
        sha1_obj = func_sha1()
        with open(path, 'rb') as in_file:
            data = in_file.read()
            sha1_obj.update(data)
        sha1 = sha1_obj.hexdigest()
        modified = datetime.now()
        return cls(name, sha1, modified, data)
                   

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
        """ Represent as string by filename and first 6 characters of hash."""
        return "<File object '%s': %s>" % (str(self.name), str(self.sha1)[:6])
