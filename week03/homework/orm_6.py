#!/bin/python3
# -*- coding: utf-8 -*-
'''

张三给李四通过网银转账 100 极客币，现有数据库中三张表：

一张为用户表，包含用户 ID 和用户名字，
另一张为用户资产表，包含用户 ID 用户总资产，
第三张表为审计用表，记录了转账时间，转账 id，被转账 id，转账金额。

请合理设计三张表的字段类型和表结构；
请实现转账 100 极客币的 SQL(可以使用 pymysql 或 sqlalchemy-orm 实现)，张三余额不足，转账过程中数据库 crash 等情况需保证数据一致性。
'''
import pymysql
from sqlalchemy import Column, create_engine, String, DateTime, DECIMAL, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decimal import Decimal
from week03.homework.read_config import db_config

Base = declarative_base()


class UserTable(Base):
    '''用户表'''
    __tablename__ = 'user_info'
    id = Column(Integer(), primary_key=True)
    name = Column(String(20))


class AssetTable(Base):
    '''资产表'''
    __tablename__ = 'user_asset'
    user_id = Column(Integer(), primary_key=True, nullable=False)
    asset = Column(DECIMAL(19, 4), nullable=False)


class RecordTable(Base):
    '''审计用表  记录了转账时间，转账 id，被转账 id，转账金额'''
    __tablename__ = 'record'
    id = Column(Integer(), primary_key=True, nullable=False)
    from_id = Column(Integer(), nullable=False)
    to_id = Column(Integer(), nullable=False)
    money = Column(DECIMAL(19, 4), nullable=False)


def transfer_accounts(self, other, deal):
    db_info = db_config()
    conn = pymysql.connect(**db_info)
    try:
        with conn.cursor() as cursor:
            sql = '''select id from user_info where name=%s'''
            cursor.execute(sql, self)
            self_id = cursor.fetchone()
            cursor.execute(sql, other)
            other_id = cursor.fetchone()
            if self_id and other_id:
                self_id = self_id[0]
                other_id = other_id[0]
            else:
                raise Exception(f'{self} or {other} not exit')
            sql = '''select asset from user_asset where user_id=%s'''
            cursor.execute(sql, self_id)
            self_money = cursor.fetchone()[0]
            if self_money < deal:
                print(f'{self} has not enough money to give {other}')
            else:
                sql = '''insert into record(from_id, to_id, money) VALUES (%s, %s, %s)'''
                values = (self_id, other_id, Decimal(deal))
                cursor.execute(sql, values)
                sql = '''update user_asset set asset=%s where user_id=%s'''
                values = (self_money - Decimal(deal), self_id)
                cursor.execute(sql, values)
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()


if __name__ == '__main__':
    # 新建表格
    # db_curl = 'mysql+pymysql://root:123456@106.15.187.5:3306/demo?charset=utf8mb4'
    # engine = create_engine(db_curl, echo=True)
    # # Base.metadata.create_all(engine)
    # SessionClass = sessionmaker(engine)
    # session = SessionClass()
    # # 造数据
    # user_1 = UserTable(name='李四')
    # user_2 = UserTable(name='张三')
    # session.add_all([user_1, user_2])
    # session.commit()
    # 请实现转账 100 极客币的 SQL(可以使用 pymysql 或 sqlalchemy-orm 实现)，张三余额不足，转账过程中数据库
    # crash 等情况需保证数据一致性。
    transfer_accounts('张三', '李四', 10)
