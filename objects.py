#!/usr/bin/env python

from datetime import datetime

class File():
    """ Object to record information about stored files."""
    def __init__(self, name, sha1, modified, data):
        self.name = name
        self.sha1 = sha1
        # Parse date without timezone (the last 6 characters)
        self.modified = datetime.strptime(modified[:-6], "%Y-%m-%dT%H:%M:%S")
        self.bin = data

    def all(self):
        """ Returns tuple of all attributes in above order."""
        return (self.name, self.sha1, self.modified, self.bin)

    def dict_all(self):
        """ Returns a dictionary representation of all attributes."""
        return {"name": self.name,
                "sha1": self.sha1,
                "modified": self.modified,
                "bin": self.bin
                }
