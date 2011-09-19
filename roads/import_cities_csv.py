#!/usr/bin/python2 

import csv, couchdb, sys

couch = couchdb.Server('http://localhost:5984/')
db = couch['sd_cities']

reader = csv.reader(open("SD/cities.csv", "rb"))
city = dict()

for row in reader:    
    city['code'] = row[0]
    city['name'] = row[1]        
    print db.create(city)
