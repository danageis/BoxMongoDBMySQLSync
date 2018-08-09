#!/usr/bin/env python

from boxsdk.object.file import File as BoxFile
from objects import DBFile
from box_auth import start_session

""" GLOBAL VARIABLES """
# Box folder ID for the directory in which files are stored
folder_id = 52318493988

# Box.com session client for file access
client = start_session()

""" GLOBAL FUNCTIONS """

def get_box_file(file_id):
    """ Get the data and metadata for a file stored on Box.

    file_id (int): numeric ID of file to get.

    Returns (DBFile): object containing data/metadata for the file.
    """
    file_obj = client.file(file_id).get()
    return DBFile(file_obj.name,
                  file_obj.sha1,
                  file_obj.modified_at,
                  file_obj.content()
                  )

def get_files():
    """ Get a list of all file data/metadata in the Box folder."""
    files = []
    for entity in client.folder(folder_id).get_items(limit=None):
        if type(entity) == BoxFile:
            files.append(get_box_file(entity.id))
    return files

""" Functions to upload/update data in files on Box,
        either from binary data streams or local files.

    data (binary): binary data comprising a file.
    name (str): name to give to file.
    file_id (int): numeric ID of file to update on Box.
"""
upload_data = lambda data, name: client.folder(folder_id).upload_stream(data, name)
upload_file = lambda path: client.folder(folder_id).upload(path)
update_data = lambda data, file_id: client.file(file_id).update_contents_with_stream(data)
update_file = lambda path, file_id: client.file(file_id).update_contents(path)

def sync_up_data(db_f):
    """ Synchronize a file up to Box (upgrade or upload new as necessary).

    client (boxsdk.Client): client object to interact on Box with.
    db_file (DBFile): file object containing data/metadata of a single file.
    """
    on_box = get_all_box_files()
    if db_file.name in [f.name for f in on_box]:
        box_file = [f for f in on_box if f.name == db_file.name][0]
        if db_file.sha1 != box_file.sha1 and db_file.modified > box_file.modified:
            update_data(db_file.bin, db_file.id)
    else:
        upload_data(db_file.bin, db_file.name)
