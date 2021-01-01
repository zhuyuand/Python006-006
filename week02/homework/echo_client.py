#!/bin/python3
# -*- coding: utf-8 -*-
import socket
'''
echo client
'''


def echo_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 10000))
    while True:
        content = input('input>')
        if content == 'exit':
            break
        s.sendall(content.encode('utf-8'))
        content = s.recv(1024)
        print(f'服务器:{content.decode()}')
    # 关闭连接
    s.close()


if __name__ == '__main__':
    echo_client()
