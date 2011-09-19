#!/usr/bin/python2

from random import randrange
import couchdb
import pdb


couch = couchdb.Server('http://localhost:5984/')
db = couch['warehouse']

comp = dict()
comp[0] = 'Lerz'
comp[1] = 'ExtofUs'
comp[2] = 'Meh'
comp[3] = 'Klebel Bros.'
comp[4] = 'Zaeden Master'

profile = dict()
profile[0] = 'channel'
profile[1] = 'flat'
profile[2] = 'solid'
profile[3] = 'pipe'
profile[4] = 'u_channel' 

grade = dict()
grade[0] = 'T6'
grade[1] = 'A36'
grade[2] = 'galvanized'
grade[3] = '1045'
grade[4] = '1018'

doc = dict()

for x in range(1000):
    doc['company'] = comp[randrange(0,4)]
    doc['profile'] = profile[randrange(0,4)]
    doc['length'] = randrange(1,10)
    doc['width'] = randrange(1,10)
    doc['thickness'] = randrange(1,3)
    doc['stock_length'] = randrange(600,1000)
    doc['grade'] = grade[randrange(0,4)]
    print(db.create(doc))
