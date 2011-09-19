#!/usr/bin/python2 

import shapelib, dbflib, shptree, couchdb, sys

couch = couchdb.Server('http://localhost:5984/')
db_known = couch['sd_roads_unpaved_known']

foo = dbflib.DBFFile('SD/TR_L_nstri.dbf')

#help(foo)
field_count = foo.field_count()
record_count = foo.record_count()

count = 0
while(count < record_count):
    record = foo.read_record(count)
    if record.get('ROADNAME') <> "UNKNOWN" and (record.get('SURFACE_TY') <> 0 and record.get('SURFACE_TY') <> 9 and record.get('SURFACE_TY') <> 8) and record.get('CITY_CODE') <> "999":
        db_known.create(record)
    count = count + 1
