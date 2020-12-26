#!/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import time
from pathlib import Path
import logging


def strftime():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def mkdir(path):
    path = Path(path)
    if not path.parent.exists():
        path.parent.mkdir()
        sys.stdout.write('新建%s' % path.parent)


def daemon(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as err:
        sys.stderr.write(f'_FORK #1 {err}')
        sys.exit(1)
    os.chdir('/')
    os.umask(0)
    os.setsid()
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as err:
        sys.stderr.write(f'_FORK #2 {err}')
        sys.exit(1)
    sys.stderr.flush()
    sys.stdout.flush()
    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'w')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


def test_write():
    logging.info(f'pid is {os.getpid()}')
    while True:
        logging.info(time.time())
        time.sleep(1)


if __name__ == '__main__':
    log_path = f'/var/log/python-{time.strftime("%Y-%m-%d")}/d.log'
    mkdir(log_path)
    DATEFMT = '%Y-%m-%d %H:%M:%S'
    FORMAT = '%(asctime)s %(name)s %(levelname)s [line: %(lineno)d] %(message)s'
    logging.basicConfig(filename=log_path,
                        datefmt=DATEFMT,
                        format=FORMAT,
                        level=logging.DEBUG)
    daemon(stdout=log_path)
    test_write()
