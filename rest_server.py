#!/usr/bin/env python

from hashlib import sha1
from datetime import datetime
from traceback import print_exc
from flask import Flask, request, jsonify
import box_tools as box
import mysql_tools as mysql
import mongo_tools as mongo
from objects import File

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
    
        for mod in db_modules:
            print("<DEBUG> type(bin):", type(db_file.bin))
            mod.insert_file(db_file)
    
        return jsonify({"Status": "Uploaded to all databases successfully."})
    except:
        print_exc()
        return jsonify({"Status": "ERROR"})

# Start server
def main():
    app.run()

if __name__ == "__main__":
    main()
