import psycopg2
import csv


input_filepath = './外破隐患点/外破隐患点信息.csv'
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
        'name': row[2],
        'desc': '',
    }

    for i in range(1, len(row)):
        item['desc'] = item['desc'] + row[i] + ';'
    item['desc'] = item['desc'].rstrip(';')

    return item


def connect_db():
    conn = psycopg2.connect(database="dl", user="postgres", password="yyz123", host="127.0.0.1")
    return conn


def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS external_force_damage;
                CREATE TABLE external_force_damage(
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
        cursor.execute('''INSERT INTO external_force_damage VALUES 
            ({}, '{}', '{}', NULL);
            '''.format(int(d['id']), d['name'], d['desc']))

    conn.commit()
    conn.close()


if __name__ == "__main__":

    create_table()
    insert_data(read_csv())
