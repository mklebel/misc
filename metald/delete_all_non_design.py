#!/usr/bin/python2 

import sys
from couchdbkit import *

server = Server()
db = server.get_or_create_db('tree')

docs = db.view('tree/all').all();

for doc in docs:
    print db.delete_doc(doc.get('id'))
