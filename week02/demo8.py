#!/bin/python3
# -*- coding: utf-8 -*-
from threading import Condition, Thread

cond = Condition()


class Husband(Thread):
    def __init__(self, cond):
        super().__init__(name='丈夫')
        self.cond = cond

    def run(self) -> None:
        # 获得底层锁
        self.cond.acquire()
        print('{} :亲爱的你知道今天是什么日子嘛'.format(self.name))
        self.cond.wait()  # 释放底层锁,并将分配一把锁存放在双端队列中，等待唤醒

        # 唤醒后再次获得底层锁
        print('{} :是我又爱你的一天'.format(self.name))
        self.cond.notify()
        self.cond.wait()  # 只有wait释放底层锁

        print('{}: 你知道我忍你很久了'.format(self.name))
        self, cond.notify()  # 将双端队列的锁删除
        self.cond.wait()  # 释放底层锁,并将分配一把锁存放在双端队列中，等待唤醒

        # 唤醒后再次获得底层所
        print(self.name, self.cond._is_owned())
        self.cond.release()


class Wife(Thread):
    def __init__(self, cond):
        super().__init__(name='妻子')
        self.cond = cond

    def run(self) -> None:
        # 获得底层所
        self.cond.acquire()
        print('{} :什么日子'.format(self.name))

        self.cond.notify()  # 将双端队列的锁删除
        self.cond.wait()
        print('{} :老公我爱你'.format(self.name))
        self.cond.notify()
        self.cond.wait()  # 释放底层锁,并将分配一把锁存放在双端队列中，等待唤醒

        # 唤醒后再次获得底层所
        print('{}: 那有怎么样'.format(self.name))
        self.cond.notify()
        print(self.name, self.cond._is_owned())
        self.cond.release()


if __name__ == '__main__':
    wife = Wife(cond)
    husband = Husband(cond)
    husband.start()
    wife.start()
