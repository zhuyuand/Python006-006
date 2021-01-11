#!/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, ForeignKey
info = 'mysql+pymysql://root:123456@106.15.187.5:3306/demo'
engine = create_engine(info, echo=True)
# 创建元数据
meta_data = MetaData(engine)

book = Table('book', meta_data,
             Column('id', Integer, primary_key=True),
             Column('name', String(20))
             )

author = Table('author', meta_data,
               Column('id', Integer, primary_key=True),
               Column('book_id', None, ForeignKey('book.id')),
               Column('author_name', String(20), nullable=True)
               )
try:
    meta_data.create_all()
except Exception as e:
    print(f'fetch error {e}')
