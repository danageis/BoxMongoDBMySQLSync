#!/usr/bin/env python

from boxsdk.object.file import File as BoxFile
from objects import DBFile
from box_auth import start_session

""" GLOBAL VARIABLES """
# Box folder ID for the directory in which files are stored
folder_id = 52318493988

# Box.com session client for file access
client = None

# List of all files in the Box.com folder
box_files = None

""" GLOBAL FUNCTIONS """
def connect():
    """ Connect to Box.com and get a list of all files available. """
    global client, box_files
    client = start_session()
    box_files = [f for f in client.folder(folder_id).get_items(limit=None)
                 if type(f) == BoxFile
                 ]

def insert_file(db_file):
    """ Upload a DBFile object to Box.com."""
    client.folder(folder_id).upload_stream(db_file.bin, db_file.name)

def update_file(db_file):
    """ Update a file on Box.com with a DBFile object."""
    file_id = [f.id for f in box_files if f.name == db_file.name][0]
    client.file(file_id).update_contents_with_stream(db_file.bin)

def get_file_by_id(file_id):
    """ Get DBFile from Box.com based on Box file id."""
    file_obj = client.file(file_id).get()
    return DBFile(file_obj.name,
                  file_obj.sha1,
                  file_obj.modified_at,
                  file_obj.content()
                  )

def get_file(name):
    """ Get DBFile for file stored on Box.com, searched by filename."""
    file_id = [f.id for f in box_files if f.name == name][0]
    return get_file_by_id(file_id)

def get_files():
    """ Get a list of all DBFile's in the Box folder."""
    return [get_file_by_id(f.id) for f in box_files]
