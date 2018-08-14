#!/usr/bin/env python

from requests import post

# Enter the path to the file to upload
file_path = None

# URL to REST upload file service
url = 'http://localhost:5000/api/uploadFile'

def main():
    payload = {'file': open(file_path, 'rb')}
    response = post(url, files=payload, stream=True)

if __name__ == "__main__":
    main()
