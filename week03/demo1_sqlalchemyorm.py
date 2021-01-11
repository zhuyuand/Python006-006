#!/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Table, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
engine = create_engine(
    'mysql+pymysql://root:123456@106.15.187.5:3306/demo',
    echo=True)
Base = declarative_base(engine)


class BookTable(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), index=True)


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    book_id = Column(None, ForeignKey('book.id'))
    # 唯一、不可为空
    name = Column(String(20), nullable=True, unique=True)
    create_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    updata_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


try:
    Base.metadata.create_all()
except Exception as e:
    print(f'fetch error {e}')
