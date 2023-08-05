""" 
Prior to use, you must install mongodb:

https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

Then change the data directory (if necessary) by:

1. Editing /etc/mongod.conf and change the dbPath field to the desired location.
2. Stop and restart mongodb (and optionally check the status)

sudo systemctl stop mongod
sudo systemctl start mongod
sudo systemctl status mongod
"""

from pymongo import MongoClient


def add_source(src):
    '''
    Takes a source dictionary and adds it to the 'sources' database.

    Arguments:
        src (dict): Source information to add to the database.
    '''
    if len(src) == 0:
        print('You tried to add a new domain to the sources database, but content is empty.')
    else:
        client = MongoClient()
        db = client['exid']
        return db['sources'].insert_one(src)


def add_content(item):
    if len(item) == 0:
        print('You tried to add a new item to the content database, but item is empty.')
    else:
        client = MongoClient()
        db = client['exid']
        return db['content'].insert_one(item)


