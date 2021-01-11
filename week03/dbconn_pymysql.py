#!/bin/python3
# -*- coding: utf-8 -*-
import pymysql
from pymysql.cursors import DictCursor
host = '106.15.187.5'
user = 'root'
password = '123456'
charset = 'utf8mb4'
db = 'demo'
port = 3306
connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    port=port,
    charset=charset,
    db=db
)

try:
    # 创建游标对象
    with connection.cursor(DictCursor) as cursor:
        sql = '''select * from book where book_id=8'''
        cursor.execute(sql)
        print(cursor.fetchall())
    connection.commit()
except Exception as e:
    print(f'fetch error {e}')
finally:
    connection.close()
