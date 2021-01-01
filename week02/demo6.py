#!/bin/python3
# -*- coding: utf-8 -*-
from threading import Condition
# from threading import RLock
# lock = RLock()
# # 当前线程中
# lock.acquire()
# # print(lock.acquire(0))
# def _is_owned():
#     if lock.acquire(0):
#         lock.release()
#         print(False)
#     else:
#         print(True)
from threading import Condition
# 使用重入锁
con = Condition()
# 1. 别的未释放，获取不了
# 2.












# con = Condition()
# # 获得锁
# # con.acquire()
# # print(con.acquire())
# # print(con.acquire())
# print(con.acquire())
# # print(con.acquire(0))
# print(con._is_owned())
# print(con.acquire(0))
# con.wait()