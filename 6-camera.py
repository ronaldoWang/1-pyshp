import csv
from pyshp import shapefile
from coord.universal import *
from coord.china import *


input_filepath = './通道可视化设备/通道可视化设备明细1129.csv'
output_filepath = 'D:/develop/GIS/DataFile/additional-3857/CAMERA'
encoding = 'gbk'

i_lat, i_lng = 0, 0
i_no, i_loc, i_man = 0, 0, 0  # 编号，地址，厂家字段索引


def read_csv():
    # 读取csv格式文件
    with open(input_filepath, 'r', encoding=encoding) as f:
        reader = csv.reader(f)

        is_title = True
        data = []
        for row in reader:
            # 获取字段名
            if is_title:
                is_title = False
                title = row
                fine_col_index(title)
            else:
                # 坐标转换，合并字段
                item = convert_row(row)
                data.append(item)

        return data


def fine_col_index(title):
    i = -1
    for cell in title:
        i = i + 1
        if "纬度" in cell:
            global i_lat
            i_lat = i
        if "经度" in cell:
            global i_lng
            i_lng = i

        if "摄像机编号" in cell:
            global i_no
            i_no = i
        if "监控点描述" in cell:
            global i_loc
            i_loc = i
        if "设备厂家" in cell:
            global i_man
            i_man = i

    print(title)
    print(i_no, i_loc, i_lat, i_lng, i_man)


def convert_row(row):
    # 把坐标以外的字段放到description中
    desc = ''
    i = 0
    for cell in row:
        # des = des + title[i] + ':' + cell + ';'  # 字段过长会导致shp无法导入
        desc = desc + cell + ';'
        i = i + 1
    desc = desc.rstrip(';')

    name = row[i_man] + '_' + row[i_loc]  # 厂家+地址
    item = {'desc': desc, 'name': name, 'id': int(row[i_no]), 'latlng': []}

    # 坐标转换
    x, y = row[i_lat], row[i_lng]
    x, y = x.strip('N'), y.strip('E')
    x, y = float(x), float(y)

    if row[i_man] == '泰锌':  # '泰锌'使用百度地图， 为bd09坐标
        x, y = bd2wgs(x, y)
    # x, y = wgs2gcj(x, y)
    x, y = ll2mc(x, y)

    item['latlng'] = [x, y]
    return item


# 写入 shapefile
def write_shp(content):
    w = shapefile.Writer(output_filepath, shapeType=shapefile.POINT, encoding=encoding)
    w.autoBalance = 1                   # Autobalancing is NOT turned on by default
    w.field('DESCRIPTION', 'C', '255')  # C代表数据类型为字符串，长度最大为255
    w.field('NAME', 'C', '255')
    w.field('ID', 'C', '255')
    for item in content:
        w.point(item['latlng'][0], item['latlng'][1])

        if len(item['desc']) > 255:
            print('超出字段允许长度', item['des'])

        w.record(item['desc'], item['name'], item['id'])


if __name__ == "__main__":

    write_shp(read_csv())
