#!/bin/python3
# -*- coding: utf-8 -*-
import pymysql
from pymysql.cursors import DictCursor
import logging

host = '106.15.187.5'
user = 'root'
password = '123456'
port = 3306
charset = 'utf8mb4'
database = 'demo'
connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port,
    charset=charset)
try:
    with connection.cursor(DictCursor) as cursor:
        # "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        sql = '''insert into users (email, password) values (%s, %s)'''
        cursor.execute(sql, ('1064997626', '12345'))
        cursor.fetchone()
    connection.commit()
except Exception as e:
    print(f'fetch error {e}')
finally:
    connection.close()
