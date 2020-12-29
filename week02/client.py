#!/bin/python3
# -*- coding: utf-8 -*-
import socket
'''
使用sockeet 编程实现客户端
'''
HOST = 'localhost'
PORT = 10000
def client():
    # ipv4  tcp
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    while True:
        # 发送消息
        data = input('input >')
        if data == 'exit':
            break
        s.sendall(data.encode('utf-8'))
        msg = s.recv(1024).decode('utf-8')
        print(msg)
    s.close()
if __name__ == '__main__':
    client()