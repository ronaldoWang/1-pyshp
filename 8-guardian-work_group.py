# -*- coding:utf-8 -*-
from pyshp import shapefile
from coord.universal import gauss2wgs, ll2mc
from coord.china import wgs2gcj


src_root = './护线员及班组分区/'
# filename = 'GUARDIAN'
filename = "WORK_GROUP"

dst_root = 'D:/develop/GIS/DataFile/additional-3857/'
encoding = 'gbk'


def update():
    src = src_root + filename
    dst = dst_root + filename

    r = shapefile.Reader(src, encoding=encoding)
    w = shapefile.Writer(dst, encoding=encoding)
    w.fields = r.fields[1:]  # skip first deletion field

    for shaperec in r.iterShapeRecords():
        # print(shaperec.shape.shapeType == shapefile.POLYGON)
        poly = []
        for p in shaperec.shape.points:
            x, y = convert_point(p[0], p[1])
            poly.append([x, y])
        w.poly([poly])
        w.record(*shaperec.record)

    w.close()  # 保存


def convert_point(x, y):
    x, y = gauss2wgs(x, y)
    # x, y = wgs2gcj(x, y)
    x, y = ll2mc(x, y)
    return x, y


if __name__ == "__main__":

    update()
