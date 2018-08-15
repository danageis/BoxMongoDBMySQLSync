#!/usr/bin/env python

from requests import post
from configparser import ConfigParser

# Read path to the file to upload from config file
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
