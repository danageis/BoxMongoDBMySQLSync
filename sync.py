#!/usr/bin/env python

import box_tools as box
import mysql_tools as mysql
import mongo_tools as mongo

def sync_down():
    """ Get synchronized list of all files from all 3 sources.

    Return (list of DBFile): DBFiles for each up-to-date file.
    """
    box_files = box.get_files()
    mysql_files = mysql.get_files()
    mongo_files = mongo.get_files()

    synced_files = box_files
    for db_file in mysql_files:
        if db_file.name not in [f.name for f in synced_files]:
            synced_files.append(db_file)
        else:
            old = [f for f in synced_files if f.name == db_file.name][0]
            if db_file.sha1 != old.sha1 and db_file.modified > old.modified:
                
