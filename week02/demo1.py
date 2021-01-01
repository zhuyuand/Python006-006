#!/bin/python3
# -*- coding: utf-8 -*-
from queue import Queue
from threading import Thread

'''
消费者和生产者
1.生产者 -> 包子
2.消费者 -> 吃掉

'''
def producer(que):
    data = 0
    while data < 20:
        data += 1
        que.put(data)
    # 告诉消费者我生产完了
    que.task_done()

def consumer(que):
    while True:
        '''怎么样知道生产完了呢？'''
        try:
            data = que.get_nowait()
            print(data)
        except Exception as e:
            pass
        else:
            if que.empty():

                break



que = Queue()

t1 = Thread(target=consumer, args=(que,))
t2 = Thread(target=producer, args=(que,))
t1.start()
t2.start()
que.join()
print('结束')


