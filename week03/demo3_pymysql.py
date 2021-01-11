#!/bin/python3
# -*- coding: utf-8 -*-
import pymysql
host = '106.15.187.5'
user = 'root'
password = '123456'
database = 'demo'
port = 3306
charset = 'utf8mb4'
connection = pymysql.connect(host=host, user=user, password=password, database=database, port=port, charset=charset)
try:
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = '''insert into users (email, password) VALUES (%s, %s)'''
        cursor.execute(sql, ('10', '1234'))
    connection.commit()
except Exception as e:
    print(f'fetch error {e}')
finally:
    connection.close()