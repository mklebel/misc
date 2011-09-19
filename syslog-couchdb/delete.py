#!/usr/bin/python2

import couchdb
import sys

couch = couchdb.Server('http://localhost:5984/')
db = couch['syslog']
view = db.view('_design/syslog/_view/all')

for doc in view:
    try:
        d = doc.get('value')
        if d.get('hostname') == "localhost":
            print db.delete(d)
    except:
        continue
