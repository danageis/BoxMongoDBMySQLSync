#!/usr/bin/env python

from mongo_auth import connect_db
from objects import DBFile

""" GLOBAL VARIABLES """
client = connect_db()
db = client.FinalProject
collection = db.Files

""" GLOBAL FUNCTIONS """
def insert_file(db_file):
    """ Add a DBFile object to the Mongo DB."""
    collection.insert_one(db_file.dict_all())

def update_file(db_file):
    """ Update the contents of a MongoDB file."""
    collection.update_one({"name": db_file.name},
                          {"$set": {"sha1": db_file.sha1,
                                    "modified": db_file.modified,
                                    "bin:": db_file.bin
                                    }
                           }
                          )

def get_file(name):
    """ Get a single file (name) from MongoDB as a DBFile object."""
    results = collection.find_one({"name": name})
    return DBFile(name=results['name'],
                  sha1=results['sha1'],
                  modified=results['modified'],
                  data=results['bin']
                  )

def get_files():
    """ Return list of all DBFiles from Mongo."""
    files = []
    for result in collection.find():
        files.append(DBFile(name=result['name'],
                     sha1=result['sha1'],
                     modified=result['modified'],
                     data=result['bin']
                     )
