#!/usr/bin/env python

from pymongo import MongoClient

""" GLOBAL VARIABLES """
# Host IP and port of MongoDB instance
ip = 'localhost'
port = 27017

""" GLOBAL FUNCTIONS """
def connect_db():
    """ Connect to MongoDB database."""
    return MongoClient(ip, port)
