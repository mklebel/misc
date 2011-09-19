#!/usr/bin/python2 

import csv, sys
from datetime import datetime, date, time
from couchdbkit import *

server = Server()
db = server.get_or_create_db('tree')

class Piecetree(Document):
      author = "Mitch Klebel"
      date = datetime.utcnow()

Piecetree.set_db(db)

reader = csv.reader(open("metal_definitions.csv", "rb"), delimiter=";")

for row in reader:    
    piece = dict()
    piece['material'] = row[0]
    piece['shape'] = row[1]
    piece['profile'] = row[2]
    print db.save_doc(piece)
