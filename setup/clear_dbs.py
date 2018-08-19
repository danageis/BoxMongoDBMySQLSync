#!/usr/bin/env python

from configparser import ConfigParser
from pymongo import MongoClient
from mysql.connector import connect

config = ConfigParser()
config.read('../config.ini')
host = config['MySQL']['HostIP']
user = config['MySQL']['Username']
passwd = config['MySQL']['Password']
database = config['MySQL']['Database']

con = connect(host=host,
              user=user,
              passwd=passwd,
              database=database
              )
c = con.cursor()
c.execute('delete from files where id > 0')
print("MySQL files deleted.")

ip = config['MongoDB']['HostIP']
port = int(config['MongoDB']['HostPort'])
client = MongoClient(ip, port)
db = client.FinalProject
coll = db.Files
coll.delete_many({})
print("MongoDB files deleted.")
