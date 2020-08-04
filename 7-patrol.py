import csv
from pyshp import shapefile
from coord.universal import *
from coord.china import *


input_filepath = './巡更点/巡更点.csv'
output_filepath = 'D:/develop/GIS/DataFile/additional-3857/PATROL'
encoding = 'gbk'

# 点号 点名 纬度	经度	大地高	X	Y	H	班组	ID
i_lat, i_lng, i_x, i_y, i_no, i_group = -1, -1, -1, -1, -1, -1


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
                find_col_index(title)
            else:
                # 坐标转换，合并字段
                item = convert_row(row)
                data.append(item)

        return data


def find_col_index(title):
    i = -1
    for cell in title:
        i = i + 1
        if "纬度" in cell:
            global i_lat
            i_lat = i
        elif "经度" in cell:
            global i_lng
            i_lng = i
        elif "X" in cell:
            global i_x
            i_x = i
        elif "Y" in cell:
            global i_y
            i_y = i

        elif "点名" in cell:
            global i_no
            i_no = i
        elif "班组" in cell:
            global i_group
            i_group = i

    print(title)
    print(i_no, i_lat, i_lng, i_x, i_y, i_group)


def convert_row(row):
    # 把坐标以外的字段放到description中
    name = row[i_no] + '_' + row[i_group]
    item = {'name': name, 'no': row[i_no], 'group': row[i_group], 'latlng': []}

    # 坐标转换
    # 使用城市坐标
    # x, y = row[i_y], row[i_x]
    # x, y = float(x), float(y)
    # x, y = gauss2wgs(x, y)
    # x, y = wgs2gcj(x, y)
    # x, y = ll2mc(x, y)

    # 使用经纬度坐标
    x, y = row[i_lat], row[i_lng]
    x, y = x.strip('N'), y.strip('E')
    x, y = angular2decimal(x), angular2decimal(y)
    # x, y = wgs2gcj(x, y)
    x, y = ll2mc(x, y)

    item['latlng'] = [x, y]
    return item


def angular2decimal(it):
    [degree, it] = it.split('°')
    [minute, second] = it.strip('"').split("'")
    decimal = float(degree) + float(minute) / 60 + float(second) / 3600
    return decimal


# 写入shapefile
def write_shp(content):
    w = shapefile.Writer(output_filepath, shapeType=shapefile.POINT, encoding=encoding)
    w.autoBalance = 1
    w.field('NAME', 'C', '255')
    w.field('ID', 'C', '255')
    w.field('GROUP', 'C', '255')
    for item in content:
        w.point(item['latlng'][0], item['latlng'][1])
        w.record(item['name'], item['no'], item['group'])


if __name__ == "__main__":

    write_shp(read_csv())
