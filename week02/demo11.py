#!/bin/python3
# -*- coding: utf-8 -*-
import threading
import time

rlock = threading.RLock()

def func():
    rlock.acquire()
    for i in range(3):
        time.sleep(2)
        print(i)
    rlock.release()
    return

def test():
    l = []
    for i in range(3):
        time.sleep(1)
        threading.Thread(target=func).start()
    print(rlock) # prints <_thread.RLock owner=140092805895936 count=1>
    print(rlock._is_owned()) #prints False
    if not rlock._is_owned():
        return 'finished' #returns 'finished'

test()