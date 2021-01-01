#!/bin/python3
# -*- coding: utf-8 -*-
from threading import Condition
from collections import deque
# from threading import RLock
from _thread import allocate_lock
from itertools import islice
from threading import RLock
from threading import Lock
import active as active


class Condition:
    def __init__(self, lock=None):
        if lock is None:
            # 默认使用可重入锁
            lock = RLock()
        self._lock = lock
        # Export the lock's acquire() and release() methods
        self.acquire = lock.acquire
        self.release = lock.release
        # If the lock defines _release_save() and/or _acquire_restore(),
        # these override the default implementations (which just call
        # release() and acquire() on the lock).  Ditto for _is_owned().
        try:
            self._release_save = lock._release_save
        except AttributeError:
            pass
        try:
            self._acquire_restore = lock._acquire_restore
        except AttributeError:
            pass
        try:
            self._is_owned = lock._is_owned
            # print(self._is_owned)
        except AttributeError:
            pass
        self._waiters = deque()

    def __enter__(self):
        return self._lock.__enter__()

    def __exit__(self, *args):
        return self._lock.__exit__(*args)

    def __repr__(self):
        return "<Condition(%s, %d)>" % (self._lock, len(self._waiters))

    def _release_save(self):
        self._lock.release()           # No state to save

    def _acquire_restore(self, x):
        self._lock.acquire()           # Ignore saved state

    def _is_owned(self):
        if self._lock.acquire(0):
            self._lock.release()
            return False
        else:
            return True

    def wait(self, timeout=None):
        # 判断递归锁是否是在当前线程中
        if not self._is_owned():
            raise RuntimeError("cannot wait on un-acquired lock")
        # 创建底层锁
        waiter = allocate_lock()
        # 获得底层锁
        waiter.acquire()
        # 放入双端队列中
        self._waiters.append(waiter)
        # 重入锁释放
        saved_state = self._release_save()
        gotit = False
        try:    # restore state no matter what (e.g., KeyboardInterrupt)
            if timeout is None:
                # 再次获得底层锁  堵塞
                waiter.acquire()
                gotit = True
            else:
                if timeout > 0:
                    gotit = waiter.acquire(True, timeout)
                else:
                    gotit = waiter.acquire(False)
            return gotit
        finally:
            # 重新获得重入锁(可能会堵塞)
            self._acquire_restore(saved_state)
            # 如果超时的话，则删除那个锁
            if not gotit:
                try:
                    self._waiters.remove(waiter)
                except ValueError:
                    pass

    def notify(self, n=1):
        """Wake up one or more threads waiting on this condition, if any.

        If the calling thread has not acquired the lock when this method is
        called, a RuntimeError is raised.

        This method wakes up at most n of the threads waiting for the condition
        variable; it is a no-op if no threads are waiting.

        """
        # 判断重入锁是否在当前线程中
        if not self._is_owned():
            raise RuntimeError("cannot notify on un-acquired lock")

        all_waiters = self._waiters
        # print(deque(islice(all_waiters, n)), '-----------')
        # 获取第n个底层锁
        # 友好的处理超过队列长度
        waiters_to_notify = deque(islice(all_waiters, n))
        # 如果为空
        if not waiters_to_notify:
            return
        for waiter in waiters_to_notify:
            # 松开锁，一定要删除队列中锁
            waiter.release()
            try:
                # 删除队列的锁
                all_waiters.remove(waiter)
            except ValueError:
                pass


if __name__ == '__main__':
    from threading import Thread, RLock
    lock = RLock()

    cond = Condition(lock)
    cond1 = Condition(lock)

    class Husband(Thread):
        def __init__(self):
            super().__init__(name='丈夫')
            self.cond = cond
            self.cond1 = cond1

        def run(self) -> None:
            # 获得底层锁
            self.cond.acquire()
            print('{} :1'.format(self.name))
            print('开始堵塞')
            self.cond.wait()  # 释放底层锁,并将分配一把锁存放在双端队列中，等待唤醒
            print('结束堵塞')
            print('111')

    class Wife(Thread):
        def __init__(self):
            super().__init__(name='妻子')
            self.cond = cond
            self.cond1 = cond1

        def run(self) -> None:
            # self.cond1.acquire()
            # 获得底层所
            self.cond.acquire()  # 等谁使用wait
            print('{} :1'.format(self.name))
            self.cond.release()
            self.cond1.release()

    class Son(Thread):
        def __init__(self):
            super().__init__(name='儿子')
            self.cond = cond
            self.cond1 = cond1

        def run(self) -> None:
            # 获得底层所

            self.cond1.acquire()  # 等谁使用wait
            # self.cond.acquire()
            print('{} :1'.format(self.name))
            # self.cond.release()
            print(self.cond._is_owned())
            self.cond.notify()


    wife = Wife()
    husband = Husband()
    son = Son()
    husband.start()
    wife.start()
    son.start()
