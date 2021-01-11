#!/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData, Integer, String, Table, Column, ForeignKey
import pymysql
# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
info = 'mysql+pymysql://root:123456@106.15.187.5:3306/demo'
# 开启调试模式
engine = create_engine(info, echo=True)

# 创建元数据
meta_data = MetaData(engine)
# 每张表必须有个关键字
book_table = Table(
    'book', meta_data,
    Column('id', Integer, primary_key=True),
    Column('name', String(20))
)
author_table = Table(
    'author', meta_data,
    Column('id', Integer, primary_key=True),
    Column('book_id', None, ForeignKey('book.id')),
    Column('author_name', String(20), nullable=False)
)
try:
    meta_data.create_all()
except Exception as e:
    print(f'fetch error {e}')
