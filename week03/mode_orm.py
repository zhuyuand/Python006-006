#!/bin/python3
# -*- coding: utf-8 -*-
from sqlalchemy import and_, or_, not_
from sqlalchemy import func
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# 创建引擎
dburl = 'mysql+pymysql://root:123456@106.15.187.5:3306/demo?charset=utf8mb4'
engine = create_engine(dburl, echo=True)

# 创建会话
SessionClass = sessionmaker(bind=engine)
session = SessionClass()

Base = declarative_base(engine)
try:
    pass
except Exception as e:
    pass


class BookTable(Base):
    __tablename__ = 'book'
    book_id = Column(Integer(), primary_key=True)
    book_name = Column(String(20), index=True)

    def __repr__(self):
        return self.__class__.__name__ + \
               '(' + ', '.join(f'{k}: {v}' for k, v in self.__dict__.items() if not k.startswith('_')) + ')'


class AuthorTable(Base):
    __tablename__ = 'author'
    user_id = Column(Integer(), autoincrement=True, primary_key=True)
    author_name = Column('name', String(20), unique=True, nullable=True)
    create_on = Column(DateTime(), default=datetime.now)
    update_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


# 实例化 前提必须必有需要有表
# book = BookTable(book_name='一千零一夜')
# print(book)
# session.add(book)


# first  不会报错   多个取第一个  没有None
# sclar  0/1个  多了报错
# one 必须一个   多了/没有报错
# print(session.query(BookTable.book_id).all())

# 倒叙
# res = session.query(BookTable.book_id, BookTable.book_name).order_by(BookTable.book_id.desc())

# 聚合函数
# res = session.query(BookTable).filter(BookTable.book_id == 9).first()
# res = session.query(func.count(BookTable.book_id)).first()

# 条件判断
# res = session.query(BookTable).filter(or_(BookTable.book_id == 1,
#                                          BookTable.book_id == 9)).delete()
# id = 7删除
res = session.query(BookTable).filter(BookTable.book_id == 7).update({BookTable.book_name: '1234111'})
print(res)
session.commit()

# try:
#     Base.metadata.create_all()
# except Exception as e:
#     print(e)
