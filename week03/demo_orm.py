#!/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
info = 'mysql+pymysql://root:123456@106.15.187.5:3306/demo'
engine = create_engine(info, echo=True)
Base = declarative_base(engine)
class BookTable(Base):
    __tablename__ = 'bookorm'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))

class AuthorTable(Base):
    __tablename__ = 'authororm'
    id = Column(Integer, primary_key=True)
    book_id = Column(None, ForeignKey('bookorm.id'))
    name = Column(String(15), nullable=True, unique=True)
    create_on = Column(DateTime(), default=datetime.now)
    update_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
try:
    Base.metadata.create_all()
except Exception as e:
    print(f'fetch error {e}')
