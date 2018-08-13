#!/usr/bin/env python

import box_tools as box
import mysql_tools as mysql
import mongo_tools as mongo

def sync():
    """ Synchronize files across all 3 databases (Box.com/MySQL/MongoDB)."""
    modules = (box, mysql, mongo)
    sources = ['box', 'mysql', 'mongo']
    files, to_add, to_update = {}, {}, {}
    for i in range(3):
        # Connect to source, get files, and create dicts for uploads and updates
        modules[i].connect()
        files[sources[i]] = modules[i].get_files()
        to_add[sources[i]], to_update[sources[i]] = [], []

    def process(src_name):
        """ Process files to update/upload for each data source.

        src_name (str): name of source to check for (box/mysql/mongo)
        """
        nonlocal to_add, to_update
        others_names = [s for s in sources if s != src_name]
        src_files = files[src_name]
        other_files = files[other_names[0]] + files[other_names[1]]

        for other in other_files:
            if other.name not in [f.name for f in src_files]:
                to_add[src_name].append(other)
            else:
                src = [f for f in src_files if f.name == other.name][0]
                if other.sha1 != src.sha1 and other.modified > src.modified:
                    to_update[src_name].append(other)

    # Populate lists of files to be updated/added to each platform
    for name in sources: process(name)

    # Upload new files and update existing ones as needed
    for i in range(3):
        module, name = modules[i], sources[i]
        for f in to_add[name]: module.insert_file(f)
        for f in to_update[name]: module.update_file(f)
