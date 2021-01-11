#!/bin/python3
# -*- coding: utf-8 -*-
from dbutils.pooled_db import PooledDB
from dbutils.pooled_db import PooledDB
import pymysql

'''
    def __init__(
            self, creator, mincached=0, maxcached=0,
            maxshared=0, maxconnections=0, blocking=False,
            maxusage=None, setsession=None, reset=True,
            failures=None, ping=1,
            *args, **kwargs):
'''
dbconfig = {
    'host': '106.15.187.5',
    'user': 'root',
    'password': '123456',
    'charset': 'utf8mb4',
    'port': 3306,
    'database': 'demo',
    'maxconnections': 0,  # 最大连接数
    'mincached': 4,  # 初始化时，连接池至少创建的链接
    'maxcached': 0,  # 连接池最多空闲的链接， 0不限制
    'maxusage': 5,  # 每个链接最多被重复使用的次数，None表示无限制
    'blocking': True  # 线程池中如果没有可用的连接后是否堵塞等待
}
pool = PooledDB(pymysql, **dbconfig)
conn = pool.connection()
cur = conn.cursor()
SQL = "select * from book"
cur.execute(SQL)
f = cur.fetchall()
print(f)
cur.close()
conn.close()
try:
    with conn.cursor() as cur:
        sql = 'select * from book'
        cur.execute(sql)
        print(cur.fetchall())
    conn.commit()
except Exception as e:
    print(e)
finally:
    conn.close()
