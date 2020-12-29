#!/bin/python3
# -*- coding: utf-8 -*-
import socket
HOST = 'localhost'
PORT = 10000
def server():
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        print(f'用户 {addr}')
        while True:
            msg = conn.recv(1024)
            print(msg.decode('utf-8'))
            if not msg:
                break
            conn.sendall(msg)
        conn.close()
if __name__ == '__main__':
    server()