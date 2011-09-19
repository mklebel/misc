#!/usr/bin/python2

import pyexiv2, datetime

help(date)

metadata = pyexiv2.ImageMetadata('../../../../IMG_1525.JPG')
metadata.read()
tag = metadata['Exif.Image.DateTime'].value
print tag
print datetime.date.__add__(tag)
   
