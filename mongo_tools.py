#!/usr/bin/env python

from configparser import ConfigParser
from pymongo import MongoClient
from objects import File

""" GLOBAL VARIABLES """
config = ConfigParser()
config.read('config.ini')
ip = config['MongoDB']['HostIP']
port = int(config['MongoDB']['HostPort'])
client = None
db = None
collection = None

""" GLOBAL FUNCTIONS """
def connect():
    """ Connect to MongoDB instance and get database and collection. """
    global client, db, collection
    client = MongoClient(ip, port)
    db = client.FinalProject
    collection = db.Files

def insert_file(db_file):
    """ Add a File object to the Mongo DB."""
    collection.insert_one(db_file.__dict__)

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
    """ Get a single file (name) from MongoDB as a File object."""
    results = collection.find_one({"name": name})
    return File(name=results['name'],
                sha1=results['sha1'],
                modified=results['modified'],
                data=results['bin']
                )

def get_files():
    """ Return list of all Files from Mongo."""
    files = []
    for result in collection.find():
        files.append(File(name=result['name'],
                          sha1=result['sha1'],
                          modified=result['modified'],
                          data=result['bin']
                          )
                     )
    return files
