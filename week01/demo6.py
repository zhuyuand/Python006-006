import sys
import os
import time

'''
实现守护进程
'''
def daemon(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as err:
        sys.stdout.write(f'_FORK #1 {err}')

    os.chdir('/')
    os.umask(0)
    # 会成为会话首进程（会话组长）和进程的组长，与原来会话和进程组脱离
    os.setsid()
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as err:
        sys.stdout.write(f'_FORK #2 {err}')

    # 重定向描述符
    sys.stdout.flush()
    sys.stderr.flush()

    si = open(stdin, 'r')
    so = open(stdout, 'a+')
    se = open(stderr, 'w')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
def test():
    sys.stdout.write(f'打印当前进程{os.getpid()}')
    while True:
        sys.stdout.write(f'{time.ctime()}\n')
        time.sleep(1)

if __name__ == '__main__':
    daemon(stdout='/tmp/test.txt')
    test()
