#!/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import time
def daemon(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"FORK #1 ERROR {e}")
        sys.exit(1)
    os.chdir('/')
    os.umask(0)
    os.setsid()
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"FORK #1 ERROR {e}")
        sys.exit(1)

    sys.stdout.flush()
    sys.stderr.flush()
    si = open(stdin, encoding='utf-8', mode='r')
    so = open(stdout, encoding='utf-8', mode='a+')
    se = open(stderr, encoding='utf-8', mode='w')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
def t():
    sys.stdout.write(f'打印当前进程{os.getpid()}\n')
    while True:
        now = time.strftime('%Y-%m-%d %H:%M:S')
        sys.stdout.write(f'{now}\n')
        time.sleep(1)


