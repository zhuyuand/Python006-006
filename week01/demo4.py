import time
import os

#创建子进程前声明的变量
number = 7
try:
    pid = os.fork()

    if pid == 0:
        print("this is child process")
        number = number - 1
        time.sleep(5)
        print( number)
        while 1:
            pass
    else:
        print ("this is parent process")
except OSError as e:
    pass