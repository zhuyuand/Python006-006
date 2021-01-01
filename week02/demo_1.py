#!/bin/python3
# -*- coding: utf-8 -*-
import time
from queue import Queue
import threading
q = Queue(20)
q1 = Queue(20)
for i in range(20):
    q.put(i)


def de(i):
    '''生产者'''
    print(f'生产者线程{i}开始')
    while not q.empty():
        try:
            time.sleep(2)
            data = q.get_nowait()

            print(f'生产 {data}')
            q1.put(data)
            q.task_done()
        except Exception as e:
            pass
    print(f'生产者线程{i}结束')


def da(i):
    '''消费者'''
    print(f'消费者线程{i}开始')
    while flag or q1.qsize() > 0:
        try:
            time.sleep(5)
            data = q1.get_nowait()
            print(f'消费 {data}')
            q1.task_done()
        except Exception as e:
            pass
    # flg=False
    print(f'消费者线程{i}结束')


flag = True
for i in range(3):
    thread = threading.Thread(target=de, args=(i, ))
    thread1 = threading.Thread(target=da, args=(i, ))
    thread.start()
    thread1.start()
q.join()
print(f'q1还有{q1.unfinished_tasks}任务没完成')
flag = False

q1.join()
print('主线程结束')
