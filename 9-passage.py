import psycopg2
import csv
import json


input_filepath = './通道及工地/一二级通道信息2018.csv'
encoding = 'gbk'


def read_csv():
    with open(input_filepath, 'r', encoding=encoding) as f:
        reader = csv.reader(f)

        is_title = True
        data = []
        for row in reader:
            if is_title:
                is_title = False
            else:
                item = convert_row(row)
                data.append(item)

        return data


def convert_row(row):
    item = {
        'id': row[0],
        'name': row[1],
        'level': row[2],
        'cables': row[3],
        'start_point': row[4],
        'end_point': row[5],
        'stations': row[6],
        'length': float(row[7])
    }
    cables = item['cables']

    cables = cables.replace('\\', ';').replace('、', ';').replace('，', ';').replace(',', ';')\
        .replace('（', '(').replace('）', ')').replace(' ', '')

    arr = cables.split(';')
    cables = ''
    for a in arr:
        cables = cables + a.upper().lstrip('110').lstrip('220').lstrip('500').lstrip('KV') + ';'
    cables = cables.rstrip(';')

    item['cables'] = cables
    return item


def connect_db():
    conn = psycopg2.connect(database="dl", user="postgres", password="yyz123", host="127.0.0.1")
    return conn


def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS passage_cables;''')
    # id serial PRIMARY KEY,
    cursor.execute('''CREATE TABLE passage_cables(
                passage_id integer PRIMARY KEY,
                NAME TEXT NOT NULL, 
                LEVEL TEXT,
                CABLES TEXT,
                START_POINT TEXT,
                END_POINT TEXT,
                STATIONS TEXT,
                LENGTH double precision );''')

    conn.commit()
    conn.close()


def insert_data(data):
    conn = connect_db()
    cursor = conn.cursor()
    for d in data:
        # nextval('public.passage_id_seq')
        cursor.execute('''INSERT INTO passage_cables VALUES 
            ({}, '{}', '{}', '{}', '{}', '{}', '{}', {});
            '''.format(int(d['id']), d['name'], d['level'], d['cables'], d['start_point'], d['end_point'],
                       d['stations'], d['length']))

    conn.commit()
    conn.close()


def create_table_single_cable():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS passage_single_cable;''')
    cursor.execute('''CREATE TABLE passage_single_cable(
                NAME TEXT NOT NULL, 
                LEVEL TEXT,
                CABLE TEXT,
                START_POINT TEXT,
                END_POINT TEXT,
                STATIONS TEXT,
                LENGTH double precision );''')

    conn.commit()
    conn.close()


def insert_data_single_cable(data):
    conn = connect_db()
    cursor = conn.cursor()
    for d in data:
        cables = d['cables'].split(";")
        for cable in cables:
            cursor.execute('''INSERT INTO passage_single_cable VALUES 
                ('{}', '{}', '{}', '{}', '{}', '{}', {});
                '''.format(d['name'], d['level'], cable, d['start_point'], d['end_point'], d['stations'], d['length']))

    conn.commit()
    conn.close()


if __name__ == "__main__":

    create_table()
    insert_data(read_csv())

    create_table_single_cable()
    insert_data_single_cable(read_csv())
