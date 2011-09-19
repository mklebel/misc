#!/usr/bin/python2 

import couchdb, sys


def get_city_name(db_cities, code):
    view = db_cities.view('_design/all/_view/city_codes', key=code)
    for doc in view:
        return doc.get('value')


def get_county_name(db_counties, code):
    view = db_counties.view('_design/all/_view/county_codes', key=code)
    for doc in view:
        return doc.get('value')

#############################################################################

couch = couchdb.Server('http://localhost:5984/')

db_roads_known = couch['sd_roads_unpaved_known']
db_cities = couch['sd_cities']
db_counties = couch['sd_counties']

view = db_roads_known.view('_design/all/_view/roads_unpaved_known')

count = 0
for doc in view:
    # all of these without city codes are highways or interstates
    if doc.value.get('CITY_CODE') <> "":
        CITY_NAME = get_city_name(db_cities, doc.value.get('CITY_CODE'))
        COUNTY_NAME = get_county_name(db_counties, doc.value.get('COUNTY_COD'))

        update_doc = doc.value
        update_doc['_id'] = doc.value.get('_id')
        update_doc['_rev'] = doc.value.get('_rev') 
        update_doc['CITY_NAME'] = CITY_NAME
        update_doc['COUNTY_NAME'] = COUNTY_NAME

        db_roads_known.save(update_doc)
        count = count + 1
        print count
