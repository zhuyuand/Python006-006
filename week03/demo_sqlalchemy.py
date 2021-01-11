#!/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, MetaData
# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
info = 'mysql+pymysql://root:123456@106.15.187.5:3306/demo'
engine = create_engine(info, echo=True)
# 创建元数据
meta_data = MetaData(engine)
# 创建表格
book = Table('book', meta_data,
             Column('id', Integer, primary_key=True),
             Column('name', String(20),)
             )

author_name = Table('author', meta_data,
                    # 主键
                    Column('id', Integer, primary_key=True),
                    # 外键
                    Column('book_id', None, ForeignKey('book.id')),
                    Column('author_name', String(20), nullable=True)
                    )
try:
    meta_data.create_all()
except Exception as e:
    print(f'fetch error {e}')