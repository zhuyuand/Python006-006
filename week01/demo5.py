#!/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import time
def daemon(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    try:
        # 创建子进程
        pid = os.fork()
        if pid > 0:
            # 推出父进程
            sys.exit(0)
    except OSError:
        sys.exit(1)

    # 切换目录，当前进程暂用目录
    os.chdir('/')
    # 文件权限, 补码
    os.umask(0)
    # 成为新的会话组长和进程组长
    sys.stdout.write(f'{os.getpid()}\n')
    os.setsid()
    sys.stdout.write(f'{os.getpid()}')
    #
    # # 首进程可能会打开终端, 保证守护进程不再是会话的首进程
    # 只会话首进程才可以打开终端设备
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError:
        sys.exit(1)
    # 描述符重定向
    sys.stderr.flush()
    sys.stdout.flush()

    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stdout, 'w')
    # fd 复制为fd2
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

def test():
    sys.stdout.write(f'当前进程{os.getpid()}')
    while True:
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        # sys.stdout.write(f'{now}\n')
        sys.stdout.flush()
        time.sleep(1)
if __name__ == '__main__':
    daemon(stdout='/tmp/daemon_test.txt')
    test()

