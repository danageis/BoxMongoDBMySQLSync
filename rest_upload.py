#!/usr/bin/env python

import sys
from requests import post
from configparser import ConfigParser

# Get path to upload from as the first argument to the script
if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    # If argument not given, then use default path (based on config.ini)
    config = ConfigParser()
    config.read('config.ini')
    file_path = config['REST']['UploadPath']

# URL to REST upload file service
url = 'http://localhost:5000/api/uploadFile'

def main():
    payload = {'file': open(file_path, 'rb')}
    response = post(url, files=payload, stream=True)

if __name__ == "__main__":
    main()
