# -*- coding:utf-8 -*-
import shapefile

# 例1，增加一个点文件
e = shapefile.Editor(shapefile="shp/test.shp")
e.point(0,0,10,2)            #注意，这里如果没有z值(10,即高度值)和M值(2，即测量值)，编辑时可能会出现问题
e.record("Appended","Point")
e.save('shp/test.shp')

# 例2，增加一条线
# e = shapefile.Editor(shapefile="shapefiles/test/line.shp")
# e.line(parts=[[[10,5],[15,5],[15,1],[13,3],[11,1]]])
# e.record('Appended','Line')
# e.save('shapefiles/test/line')
#
# # 例3，增加一个多边形
# e = shapefile.Editor(shapefile="shapefiles/test/polygon.shp")
# e.poly(parts=[[[5.1,5],[9.9,5],[9.9,1],[7.5,3],[5.1,1]]])
# e.record("Appended","Polygon")
# e.save('shapefiles/test/polygon')

# 例4，删除第一个点
e = shapefile.Editor(shapefile="shp/test.shp")
e.delete(2)
e.save('shp/test.shp')

# 例5，删除最后一个多边形
# e = shapefile.Editor(shapefile="shapefiles/test/polygon.shp")
# e.delete(-1)
# e.save('shapefiles/test/polygon')
