#!/usr/bin/python2

from random import randrange
import couchdb
import pdb


couch = couchdb.Server('http://localhost:5984/')
db = couch['warehouse']
#help(couchdb.http)
results = db.view('non_beam/all', limit=3)

foo = list()

for result in results:
    foo.append(result.id)
print(foo)
