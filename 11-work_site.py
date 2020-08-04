import psycopg2
import csv


input_filepath = './通道及工地/一级工地清单2018四季度2018121.csv'
encoding = 'gbk'


def read_csv():
    with open(input_filepath, 'r', encoding=encoding) as f:
        reader = csv.reader(f)

        is_title = True
        data = []
        for row in reader:
            if is_title:
                is_title = False
                continue
            else:
                item = convert_row(row)
                data.append(item)

        return data


def convert_row(row):
    item = {
        'id': row[0],
        'name': row[2],  # 工程
        'desc': row[1] + ';',  # 班组， 位置， 蹲守人员， 监控
    }

    for i in range(3, len(row)):
        item['desc'] = item['desc'] + row[i] + ';'
    item['desc'] = item['desc'].rstrip(';')

    return item


def connect_db():
    conn = psycopg2.connect(database="dl", user="postgres", password="yyz123", host="127.0.0.1")
    return conn


def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS work_site;
                CREATE TABLE work_site(
                id SERIAL NOT NULL PRIMARY KEY, 
                name text,
                description text, 
                cables text, 
                geom geometry(POLYGON, 3857)
                );''')

    conn.commit()
    conn.close()


def insert_data(data):
    conn = connect_db()
    cursor = conn.cursor()
    for d in data:
        cursor.execute('''INSERT INTO work_site VALUES 
            ({}, '{}', '{}', NULL, NULL);
            '''.format(int(d['id']), d['name'], d['desc']))

    conn.commit()
    conn.close()


if __name__ == "__main__":

    create_table()
    insert_data(read_csv())
