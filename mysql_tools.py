#!/usr/bin/env python

from mysql_auth import connect_db

""" GLOBAL VARIABLES """
connection = connect_db()
c = connection.cursor()

def insert_file(db_file):
    """ Insert a DBFile object into the Files table."""
    # Assign ID to 1 greater than the current number of rows
    c.execute('select count(*) from files')
    _id = (c.fetchone()[0] + 1, )

    # Insert data from db_file as a new row
    c.execute('insert into files values (%s, %s, %s, %s, %s)',
              _id + db_file.all()
              )
    connection.commit()

def update_file(db_file):
    """ Updates the file in-place for an existing file in the table."""
    c.execute('update files set sha1=%s, modified=%s, bin=%s where filename=%s',
              (db_file.sha1, db_file.modified, db_file.bin, db_file.name)
              )
