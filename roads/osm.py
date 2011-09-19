#!/usr/bin/python2 

import shapelib, dbflib, shptree, couchdb, sys

foo = dbflib.DBFFile('SD/TR_L_nstri.dbf')

#help(foo)
field_count = foo.field_count()
record_count = foo.record_count()

count = 0
while(count < record_count):
    record = foo.read_record(count)
    if record.get('ROADNAME') <> "UNKNOWN" and record.get('SURFACE_TY') <> 0 and record.get('CITY_CODE') <> "999":
        print record
    count = count + 1
