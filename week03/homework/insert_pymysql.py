#!/bin/python3
# -*- coding: utf-8 -*-
import pymysql
from pymysql.cursors import DictCursor

from week03.homework.read_config import db_config
from week03.homework.custom_enum import Edu, Gender
from datetime import datetime

db_info = db_config()
print(db_info)
conn = pymysql.connect(**db_info)
try:
    with conn.cursor(DictCursor) as cur:
        sql = '''insert into user(age, name, sex, edu, birthday, create_on, update_on) values (%s, %s, %s, %s, %s,%s, %s )'''
        values = (
            (20, '123', Gender.woman.name, Edu.doctor.name, datetime(1995, 10, 8), datetime.now(), datetime.now()),
            (21, '1234', Gender.male.name, Edu.master.name, datetime(1995, 11, 9), datetime.now(), datetime.now()),
            (22, '12356', Gender.woman.name, Edu.undergraduate.name, datetime(1995, 12, 10), datetime.now(), datetime.now()),
        )
        cur.executemany(sql, values)
    conn.commit()
except Exception as e:
    print(f'fetch error {e}')
finally:
    conn.close()
