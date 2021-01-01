#!/bin/python3
# -*- coding: utf-8 -*-
import socket
'''
echo server
'''
HOST = 'localhost'
PORT = 10000


def recv_basic(the_socket):
    total_data = []
    while True:
        data = the_socket.recv(20480)
        if not data:
            break
        total_data.append(data)
    return ''.join(total_data)


def echo_server():
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        sock, addr = s.accept()
        print(f'客户端 {addr} 已连接')
        # 接受数据, 这里可以实现多线程
        while True:
            try:
                # 当客户端发送close时， 服务器会接受空字符串
                content = sock.recv(1024).decode('utf-8')
                content = recv_basic(sock)
                if not content:
                    break
                print(f'客户端 {addr}: {content}')
                sock.sendall(content.encode('utf-8'))
            except ConnectionResetError:
                print(f'客户端 {addr} 强制关闭')
                break
        print(f'客户端 {addr} 关闭连接')
        sock.close()


if __name__ == '__main__':
    echo_server()
