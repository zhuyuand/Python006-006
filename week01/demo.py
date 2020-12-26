#!/bin/python3
import os
import sys
from datetime import timedelta
# 打开文件
fd = os.open("foo.txt", os.O_RDWR | os.O_CREAT)
print(fd)
# 写入字符串
os.write(fd, "This is test".encode('utf-8'))

# 文件描述符为 1000
fd2 = 1000
os.dup2(fd, fd2)

# 在新的文件描述符上插入数据
os.lseek(fd2, 0, 0)
str = os.read(fd2, 100)
print("读取的字符串是 : ", str)

# 关闭文件
os.close(fd)

print("关闭文件成功!!")
