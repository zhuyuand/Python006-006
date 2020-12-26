#!/usr/bin/env python
import sys
import os
import time

'''
手动编写一个daemon进程
'''


# 运行进程时，会默认打开三个描述符，标准输入，标准输出，错误输出
# 三个描述符，是在linux当中事先定义好的 0       1           2
# 默认的时候，这三个文件标志符都指向/dev/null（俗称黑洞）
# tty是终端，null是空设备，一般程序产生输出以后，不想让内容输出到终端，可以输出到null，
# 通过输出重定向把正确的结果输出到null,错误结果输出到终端
def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    # 子进程过多，可能会创建失败
    try:

        # 创建子进程
        pid = os.fork()
        print('创建子进程', pid)

        if pid > 0:
            # pid>0，认定这个进程就是我们的父进程，其他的子进程可以继续运行
            # 0代表子进程，非0表示父进程
            # 父进程先于子进程exit，会使子进程变为孤儿进程，
            # 这样子进程成功被init（1号进程）这个用户级守护进程收养
            print(os.getppid())
            sys.exit(0)
            print(os.getppid())

    except OSError as err:
        # 终端输出
        sys.stderr.write('_Fork #1 failed: {0}\n'.format(err))
        sys.exit(1)

    # 从父进程环境脱离
    # decouple from parent environment
    # chdir确认进程不占用任何目录，否则不能umount
    # daemon会一直运行下去
    os.chdir("/")
    # 调用umask(0)拥有写任何文件的权限，避免继承自父进程的umask被修改导致自身权限不足
    os.umask(0)
    # setsid调用成功后，进程成为新的会话组长和新的进程组长，并与原来的登录会话和进程组脱离
    os.setsid()

    # 第二次fork
    # try:
    #     pid = os.fork()
    #     if pid > 0:
    #         # 第二个父进程退出
    #         sys.exit(0)
    # except OSError as err:
    #     sys.stderr.write('_Fork #2 failed: {0}\n'.format(err))
    #     sys.exit(1)
    #
    # # 重定向标准文件描述符
    # sys.stdout.flush()
    # sys.stderr.flush()
    #
    # si = open(stdin, 'r')
    # so = open(stdout, 'a+')
    # se = open(stderr, 'w')
    #
    # # dup2函数原子化关闭和复制文件描述符
    # os.dup2(si.fileno(), sys.stdin.fileno())
    # os.dup2(so.fileno(), sys.stdout.fileno())
    # os.dup2(se.fileno(), sys.stderr.fileno())

os.umask()
# 每秒显示一个时间戳
def test():
    sys.stdout.write('Daemon started with pid %d\n' % os.getpid())
    while True:
        now = time.strftime("%X", time.localtime())
        sys.stdout.write(f'{time.ctime()}\n')
        sys.stdout.flush()
        time.sleep(1)


if __name__ == "__main__":
    # daemon进程脱离终端，一般进程去print打印，打印到标准输出上（就是你当前的终端）
    # 把标准输出改成文件，输出的内容自动打印到文件里面，改变标准输出方便我们调试程序
    daemonize('/dev/null', '/Users/edz/Downloads/demo/d1.log', '/dev/null')
    # 应用程序由他打印日志， 把日志打印到指定的文件内
    # test()
