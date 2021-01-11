#!/bin/python3
# -*- coding: utf-8 -*-
import pymysql

from week03.read_dbconfig import db_config

info = db_config()
conn = pymysql.connect(**info)
try:
    with conn.cursor() as cursor:
        sql = '''select * from SC where SId=%s'''
        values = (('01', ), ('02',))
        # values = ('99', '08')
        # cursor.execute(sql, values)
        cursor.executemany(sql, values)
    conn.commit()
except Exception as e:
    print(f'fetch error {e}')
finally:
    print(cursor.rowcount)
    conn.close()
