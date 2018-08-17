#!/usr/bin/env python

from hashlib import sha1
from datetime import datetime
from traceback import print_exc
from flask import Flask, request, jsonify
import box_tools as box
import mysql_tools as mysql
import mongo_tools as mongo
from objects import File

# Connect to each data source
db_modules = (box, mysql, mongo)
for mod in db_modules:
    mod.connect()

app = Flask(__name__)
@app.route('/')
def index():
    return "REST service to upload files across Box.com, MySQL, and MongoDB."

@app.route('/api/uploadFile', methods=['GET', 'POST'])
def uploadFile():
    """ REST service to which files can be uploaded. """
    try:
        file_obj = request.files.get('file')
        file_name = file_obj.filename
        file_data = file_obj.stream.read()
        hash_obj = sha1()
        hash_obj.update(file_data)
        file_sha1 = hash_obj.hexdigest()
        file_modified = datetime.now()
        
        db_file = File(name=file_name,
                       sha1=file_sha1,
                       modified=file_modified,
                       data=file_data
                       )
        print("Received file to upload: %s" % file_name)
        
    
        # Upload file to each data source
        for mod in db_modules:
            mod_name = mod.__name__[:mod.__name__.index('_')]
            files = mod.get_files()
            print("Retrieved '%s' file list" % mod_name)
            if db_file.name not in [f.name for f in files]:
                mod.insert_file(db_file)
                print("Uploaded '%s' to '%s'" % (db_file.name, mod_name))
            else:
                ext_file = [f for f in files if f.name == db_file.name][0]
                if (ext_file.sha1 != db_file.sha1
                    and ext_file.modified < db_file.modified):
                    mod.update_file(db_file)
                    print("Updated '%s' on '%s'" % (db_file.name, mod_name))
                else:
                    print("'%s' skipped on '%s', newer version present already"
                          % (db_file.name, mod_name)
                          )
    
        return jsonify({"Status": "Uploaded to all databases successfully."})
    except:
        print_exc()
        return jsonify({"Status": "ERROR"})

# Start server
def main():
    app.run()

if __name__ == "__main__":
    main()
