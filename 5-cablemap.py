# -*- coding:utf-8 -*-
from pyshp import shapefile
from coord.universal import gauss2wgs, ll2mc
from coord.china import wgs2gcj

src_root = 'E:/shp/'
dst_root = 'E:/shp-3857/'
encoding = 'gbk'


# pms导出数据有一定概率 shape.shp 和 record.dbf 记录数量不等，需重新导数据。
shp_files = {
    "Polyline": [
        # "XNGIS_SUBSTATION",
        # "XNGIS_CABLE_SECT",
        # "XNGIS_PIPE",
        # "XNGIS_ROAD_PIPE",
        # "XNGIS_STATION_PIPE",
        # "XNGIS_WORK_WELL",
        # "XNGIS_CABLE_CHANGEPOS_BOX",
        "XNGIS_CABLE_BRIDGE",
        # "XNGIS_CABLE_SILO",
        # "XNGIS_STREET_CENTER",
        # "XNGIS_OVERHEAD_LINE",
        # "XNGIS_CABLE_TUNNEL",
    ],
    "Point": [
        # "XNGIS_CABLE_JOINT_ONLINE",
        # "XNGIS_WORK_WELL_COVER",
    ],
    # "Polygon":[  # 不存在 SHAPE@
    #     "XNGIS_CABLE_SHELF",
    #     "XNGIS_CABLE_TUNNEL",
    #     "XNGIS_SUBSTATION_ADDRESS",
    #     "XNGIS_CABLE_CHANNEL",
    # ]
}


def update(filename, shapeType=None):
    src = src_root + filename
    filename = filename.replace('XNGIS_', '')
    dst = dst_root + filename

    r = shapefile.Reader(src, encoding=encoding)
    w = shapefile.Writer(dst, encoding=encoding)
    w.fields = r.fields[1:]  # skip first deletion field

    if filename == 'SUBSTATION':

        # 增加属性字段
        w.field('VOLTAGE')

        for shaperec in r.iterShapeRecords():
            # 几何坐标转换
            poly = []
            for p in shaperec.shape.points:
                x, y = convert_point(p[0], p[1])
                poly.append([x, y])
            w.poly([poly])  # 转为polygon

            # 写属性字段
            voltage_le = shaperec.record['VOLTAGE_LE']
            voltage = ''
            if voltage_le == 17:
                voltage = "1000kV"
            elif voltage_le == 8:
                voltage = "unknown"
            elif voltage_le == 7:
                voltage = "500kV"
            elif voltage_le == 6:
                voltage = "220kV"
            elif voltage_le == 5:
                voltage = "110kV"

            w.record(*shaperec.record, voltage)

    elif filename == 'CABLE_SECT':

        w.field('CABLE_NAME')
        w.field('PHASE')
        # w.field('LABEL_0')  # 名称
        w.field('LABEL_1')  # 名称 + 段编号
        w.field('LABEL_2')  # 名称 + 相位 + 段编号

        for shaperec in r.iterShapeRecords():
            line = []
            for p in shaperec.shape.points:
                x, y = convert_point(p[0], p[1])
                line.append([x, y])
            w.line([line])

            gisdesc = shaperec.record['GISDESC']
            cable_name = gisdesc.replace("黄相", "").replace("绿相", "").replace("红相", "") \
                .upper() \
                .replace("A相", "").replace("B相", "").replace("C相", "") \
                .replace('（', '(').replace('）', ')')\
                .replace(' ', '')
            phase = ''
            if "黄相" in gisdesc or "A相" in gisdesc:
                phase = "黄相"
            elif "绿相" in gisdesc or "B相" in gisdesc:
                phase = "绿相"
            elif "红相" in gisdesc or "C相" in gisdesc:
                phase = "红相"

            label_1 = cable_name + ' ' + shaperec.record['NAME']
            label_2 = cable_name + phase + shaperec.record['NAME']
            w.record(*shaperec.record, cable_name, phase, label_1, label_2)

    elif filename == 'CABLE_JOINT_ONLINE':

        # 统计 'CABLE_SECT' 的所有电缆PID+对应名称+相位
        src_cable_sect = dst_root + 'CABLE_SECT'
        r0 = shapefile.Reader(src_cable_sect, encoding=encoding)

        arr_pid = []
        for shaperec in r0.iterShapeRecords():
            exists = False
            for a in arr_pid:
                if shaperec.record['PID'] == a["PID"]:
                    exists = True
                    break
            if not exists:
                a = {
                    "PID":          shaperec.record['PID'],
                    "CABLE_NAME":   shaperec.record['CABLE_NAME'],
                    "PHASE":        shaperec.record['PHASE']
                }
                arr_pid.append(a)

        w.field('CABLE_NAME')
        w.field('PHASE')
        # w.field('LABEL_0')  # 名称
        w.field('LABEL_1')  # 名称 + 接头编号
        w.field('LABEL_2')  # 名称 + 相位 + 接头编号

        for shaperec in r.iterShapeRecords():

            p = shaperec.shape.points[0]
            x, y = convert_point(p[0], p[1])
            w.point(x, y)

            name = shaperec.record['NAME'].replace(" ", "")  # 此字段为接头编号, 为空时使用GISDESC字段
            if name == "":
                shaperec.record['NAME'] = shaperec.record['GISDESC']

            cable_name = ''
            phase = ''
            for a in arr_pid:
                if shaperec.record['PID'] == a["PID"]:
                    cable_name = a["CABLE_NAME"]
                    phase = a["PHASE"]
                    break

            label_1 = cable_name + '#' + shaperec.record['NAME']
            label_2 = cable_name + phase + '#' + shaperec.record['NAME']
            w.record(*shaperec.record, cable_name, phase, label_1, label_2)

    elif filename == 'CABLE_SILO' or \
            filename == 'CABLE_BRIDGE' or \
            filename == 'CABLE_CHANGEPOS_BOX':

        for shaperec in r.iterShapeRecords():
            poly = []
            for p in shaperec.shape.points:
                x, y = convert_point(p[0], p[1])
                poly.append([x, y])
            w.poly([poly])  # 转为polygon
            w.record(*shaperec.record)

    else:
        if shapeType == 'Polyline':
            for shaperec in r.iterShapeRecords():
                line = []
                for p in shaperec.shape.points:
                    x, y = convert_point(p[0], p[1])
                    line.append([x, y])
                w.line([line])
                w.record(*shaperec.record)

        elif shapeType == 'Point':
            for shaperec in r.iterShapeRecords():
                p = shaperec.shape.points[0]
                x, y = convert_point(p[0], p[1])
                w.point(x, y)
                w.record(*shaperec.record)

    w.close()  # 保存


def convert_point(x, y):
    x, y = gauss2wgs(x, y)
    # x, y = wgs2gcj(x, y)
    x, y = ll2mc(x, y)
    return x, y


if __name__ == "__main__":

    for file in shp_files["Polyline"]:
        print(file)
        update(file, 'Polyline')

    for file in shp_files["Point"]:
        print(file)
        update(file, 'Point')
