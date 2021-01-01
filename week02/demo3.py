#!/bin/python3
# -*- coding: utf-8 -*-
import time
def a(i):
    print('a',i)
    time.sleep(2)
def b(i):
    print('b',i)
import threading
thread_a = []
thread_b = []
for i in range(2000):
    thread = threading.Thread(target=a, args=(i,))
    thread.start()
    thread_a.append(thread)
for i in range(20):
    thread = threading.Thread(target=b, args=(i,))
    thread.start()
    thread_a.append(thread)
for i in thread_b:
    i.join()
print('joining b')
for i in thread_a:
    i.join()
print('joining a')

