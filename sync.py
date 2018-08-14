#!/usr/bin/env python

from traceback import print_exc
import box_tools as box
import mysql_tools as mysql
import mongo_tools as mongo

def work(string):
    """ Print working text to shell, without ending line. """
    print(("%s..." % string).ljust(70), end="", flush=True)

def end(): print("Complete!")
def space(): print("")

def sync(verbose=True):
    """ Synchronize files across all 3 databases (Box.com/MySQL/MongoDB).
    
    verbose (bool): If true (default), print messages to shell while syncing.
    """
    v = verbose
    modules = (box, mysql, mongo)
    sources = ['Box.com', 'MySQL', 'MongoDB']
    files, to_add, to_update = {}, {}, {}
    for i in range(3):
        # Connect to source
        if v: work("Connecting to %s" % sources[i])
        modules[i].connect()
        if v: end()
        # Get files and create dicts for uploads and updates
        if v: work("Getting files from %s" % sources[i])
        files[sources[i]] = modules[i].get_files()
        to_add[sources[i]], to_update[sources[i]] = [], []
        if v: end()
    if v: space()

    def process(src_name):
        """ Process files to update/upload for each data source.

        src_name (str): name of source to check for (box/mysql/mongo)
        """
        nonlocal to_add, to_update
        other_names = [s for s in sources if s != src_name]
        src_files = files[src_name]
        other_files = files[other_names[0]] + files[other_names[1]]

        for other in other_files:
            if (other.name not in [f.name for f in src_files]
                and other.name not in [f.name for f in to_add[src_name]]):
                to_add[src_name].append(other)
            else:
                try:
                    src = [f for f in src_files if f.name == other.name][0]
                except IndexError:
                    src = [f for f in to_add[src_name]
                           if f.name == other.name][0]
                if other.sha1 != src.sha1 and other.modified > src.modified:
                    if other.name not in [f.name for f in to_update[src_name]]:
                        to_update[src_name].append(other)
                    else:
                        other_src = [f for f in to_update[src_name]
                                     if f.name == other.name][0]
                        if (other.sha1 != other_src.sha1
                            and other.modified > other_src.modified):
                            to_update[src_name].remove(other_src)
                            to_update[src_name].append(other)


    # Populate lists of files to be updated/added to each platform
    for name in sources:
        if v: work("Checking %s files for changes" % name)
        process(name)
        if v: end()
    if v: space()

    # Upload new files and update existing ones as needed
    for i in range(3):
        module, name = modules[i], sources[i]
        for f in to_add[name]:
            if v: work("Uploading '%s' to %s" % (f.name, name))
            module.insert_file(f)
            if v: end()
        for f in to_update[name]:
            if v: work("Updating '%s' on %s" % (f.name, name))
            module.update_file(f)
            if v: end()

    if v:
        space()
        print(" SYNCHRONIZATION COMPLETE ".center(79, '~'))

if __name__ == '__main__':
    try:
        sync()
    except:
        print_exc()
    finally:
        input("\nPress Enter to exit...")
