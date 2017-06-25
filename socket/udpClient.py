#!/usr/bin/python
# -*- encoding:utf-8 -*-
##udp client build

import socket
target_host = "127.0.0.1"
target_port=80

#build udp client 
client =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# send any data.
client.sendto("this is test.",(target_host,target_port))

data,addr=client.recvfrom(4096)

print data
print addr