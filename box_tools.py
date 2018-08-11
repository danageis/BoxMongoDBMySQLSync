#!/usr/bin/env python

from boxsdk.object.file import File as BoxFile
from objects import DBFile
from box_auth import start_session

""" GLOBAL VARIABLES """
# Box folder ID for the directory in which files are stored
folder_id = 52318493988

# Box.com session client for file access
client = start_session()

# List of all files in the Box.com folder
box_files = [f for f in client.folder(folder_id).get_items(limit=None)
             if type(f) == BoxFile
             ]

""" GLOBAL FUNCTIONS """
def insert_box_file(db_file):
    """ Upload a DBFile object to Box.com."""
    client.folder(folder_id).upload_stream(db_file.bin, db_file.name)

def update_box_file(db_file):
    """ Update a file on Box.com with a DBFile object."""
    file_id = [f.id for f in box_files if f.name == db_file.name][0]
    client.file(file_id).update_contents_with_stream(db_file.bin)

def get_box_file_by_id(file_id):
    """ Get DBFile from Box.com based on Box file id."""
    file_obj = client.file(file_id).get()
    return DBFile(file_obj.name,
                  file_obj.sha1,
                  file_obj.modified_at,
                  file_obj.content()
                  )

def get_box_file(name):
    """ Get DBFile for file stored on Box.com, searched by filename."""
    file_id = [f.id for f in box_files if f.name == name][0]
    return get_box_file_by_id(file_id)

def get_box_files():
    """ Get a list of all DBFile's in the Box folder."""
    return [get_box_file_by_id(f.id) for f in box_files]
