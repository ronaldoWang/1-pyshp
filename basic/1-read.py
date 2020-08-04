# -*- coding:utf-8 -*-
import shapefile


# AttributeError: __enter__
# with shapefile.Reader("shp/nyc_roads.shp") as shp:
#     print(shp)

sf = shapefile.Reader("shp/XNGIS_SUBSTATION.shp")
print(sf.shapeType)

# Reading Geometry
# shapes = sf.shapes()
# print(len(shapes))

# # 边界坐标
# bbox = shapes[3].bbox
# print(['%.3f' % coord for coord in bbox])

# 属性名称
# for name in dir(shapes[3]):
#     print(name)

# # 点
# shape = shapes[0].points[0]
# print(['%.3f' % coord for coord in shape])
#
# # Reading Records
records = sf.records()
rec = sf.record(3)
print(rec)
print(str(rec[6], encoding="gbk"))  # pms shp 中文为gbk编码

fields = sf.fields
print(fields)

# Reading Geometry and Records Simultaneously
# shapeRecs = sf.shapeRecords()
# shapeRec = sf.shapeRecord(3)
#
# print(shapeRec.record[1:3])
#
# points = shapeRec.shape.points[0:2]
# print(points)






