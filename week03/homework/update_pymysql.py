#!/bin/python3
# -*- coding: utf-8 -*-
'''
查询语句作为作业内容提交
'''
import pymysql
from pymysql.cursors import DictCursor
from week03.homework.read_config import db_config

db_info = db_config()
con = pymysql.connect(**db_info)
try:
    with con.cursor(DictCursor) as  cursor:
        sql = '''select * from user where name = %s'''
        cursor.execute(sql, 'zhuyuan')
        print(cursor.fetchall())
except Exception as e:
    print(f'fetch error {e}')
finally:
    con.close()
