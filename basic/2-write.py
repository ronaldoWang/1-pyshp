# -*- coding:utf-8 -*-
import shapefile


# Writing Shapefiles
w = shapefile.Writer()
w.autoBalance = 1  # Autobalancing is NOT turned on by default
w = shapefile.Writer(shapefile.POINT)
# Adding Geometry
w.point(1, 1)
w.point(2, 2)
# Adding Records
w.field('NAME', 'C', '40')  #'SECOND_FLD'为字段名称，C代表数据类型为字符串，长度为40
w.record('First Point')
w.record('Second Point')
w.save('shp/test')
