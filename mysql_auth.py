#!/usr/bin/env python

from mysql.connector import connect

""" GLOBAL FUNCTIONS """
def connect_db():
    """ Connect to MySQL DB and return a cursor for file access."""
    connection = connect(host='localhost',
                         user='root',
                         passwd='sqlpassword',
                         database='finalproject'
                         )
    return connection
