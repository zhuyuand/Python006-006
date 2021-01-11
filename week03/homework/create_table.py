#!/bin/python3
# -*- coding: utf-8 -*-
'''
用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
'''

from sqlalchemy import Column, create_engine, String, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from week03.homework.custom_enum import Gender, Edu
from datetime import datetime
from sqlalchemy.orm import session
db_curl = 'mysql+pymysql://root:123456@106.15.187.5:3306/demo?charset=utf8mb4'
engine = create_engine(db_curl, echo=True)
Base = declarative_base(engine)

class UserTable(Base):
    __tablename__ = 'user'
    id = Column(Integer(), primary_key=True)
    age = Column(Integer())
    name = Column(String(15))
    sex = Column(Enum(Gender), default=Gender.male)
    edu = Column(Enum(Edu), default=Edu.undergraduate)
    birthday = Column(DateTime(), default=datetime.now)
    create_on = Column(DateTime(), default=datetime.now)
    update_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

# try:
#     Base.metadata.create_all()
# except Exception as e:
#     print(f'fetch error {e}')
# 创建会话
SessionClass = session.sessionmaker(engine)
session = SessionClass()
user1 = UserTable(age=20, name='zhuyuan')
session.add(user1)
session.commit()

