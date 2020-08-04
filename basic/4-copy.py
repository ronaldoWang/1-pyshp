# -*- coding:utf-8 -*-
import shapefile

# Adding from an existing Shape object

r = shapefile.Reader('shp/test')

w = shapefile.Writer()
w.autoBalance = 1
w = shapefile.Writer(r.shapeType)

w.fields = r.fields[1:]  # skip first deletion field

# adding existing Shape objects
for shaperec in r.iterShapeRecords():
    w.record(*shaperec.record)
    w.shape(shaperec.shape)

# or GeoJSON dicts
# for shaperec in r.iterShapeRecords():
#     w.record(*shaperec.record)
#     w.shape(shaperec.shape.__geo_interface__)

# w.close()
w.save('shp/copy')
