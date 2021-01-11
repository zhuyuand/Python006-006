#!/bin/python3
# -*- coding: utf-8 -*-
import pymysql

host = '106.15.187.5'
user = 'root'
password = '123456'
database = 'demo'
charset = 'utf8mb4'
port = 3306
connection = pymysql.connect(host=host, user=user, password=password, database=database, port=port)
with connection:
    pass
try:
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = '''insert into users (email, password) VALUES (%s, %s)'''
        cursor.execute(sql, ('my', '12345'))
        cursor.fetchone()
    connection.commit()
except Exception as e:
    print(f'fetch error {e}')
finally:
    connection.close()