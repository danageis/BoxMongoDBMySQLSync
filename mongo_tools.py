#!/usr/bin/env python

from mongo_auth import connect_db

""" GLOBAL VARIABLES """
client = connect_db()
db = client.FinalProject
coll = db.Files

""" GLOBAL FUNCTIONS """
