#!/usr/bin/python
# -*- encoding:utf-8 -*-

import socket

target_host = "127.0.0.1"
target_port = 9999


#build a socket client
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#connect to client
client.connect((target_host,target_port))


client.send("GET / HTTP/1.1\r\nHost: www.baidu.com\r\n\r\n")

reponse = client.recv(4096)

print reponse