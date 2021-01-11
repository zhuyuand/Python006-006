#!/bin/python3
# -*- coding: utf-8 -*-
import pymysql
host = '106.15.187.5'
user = 'root'
password = '123456'
database = 'demo'
port = 3306
charset = 'utf8mb4'
connection = pymysql.connect(host=host, user=user, password=password, port=port, database=database,  charset=charset)
try:
    # 创建游标
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = '''insert into SC values (%s, %s, %s)'''
        values = ('08', '01', '100')
        cursor.execute(sql, values)
    connection.commit()
except Exception as e:
    print(f'fetch error {e}')
finally:
    print(cursor.rowcount)
    connection.close()
