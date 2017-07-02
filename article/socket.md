## python中Socket的使用

### 说明
前一段时间学习python网络编程，完成简单的通过python实现网络通信的功能。现在，将python中Socket
通信的基本实现过程做一个记录备份.

### Socket通信
python 中的socket通信较为简单，仅需要几行代码就可实现。和一般的网络通信一样，通信方式分为udp和tcp两种方式，两种方式的处理也略有不同。tcp通信为传输控制协议(Transmission control Protocol),是一种面向连接、可靠的、基于字节流的传输层通信协议(TCP/IP协议簇划分的通信协议的其中一层);udp通信为用户数据报协议(User Datagram Protocol)，是一种面向无连接、不可靠的、基于报文的传输层通信协议。就是TCP／IP中的两种传输层通信协议，有关TCP／IP和TCP、UDP的详细介绍视情况而定看是否需要单独介绍，由于内容涉及较广，个人并不能完全完整详细的介绍仔细。


python网络通信需要导入一个socket模块来支持通信过程。socket通信分为客户端和服务端。服务端负责监听当前设备接口的信息发送情况，客户端实现通过ip和接口向目的主机发送信息的功能。接下来，主要看python中的tcp、udp的通信方法.

1) tcp
    服务端代码如下:

```
    import socket

    #socket.AF_INET：ipv4,socket.SOCK_STREAM：tcp
    server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((target,port))
    server_socket.listen(5)
    while True:
       client_socket,addr=server_socket.accept()
       client_handler=threading.Thread(target=handler_socket,args=(client_socket,addr,mode))
       client_handler.start()

    def handler_socket(client_socket,addr,mode="tcp"):
    response=""
    content=""
    print "Accepted tcp connection from:%s:%d" % (addr[0],addr[1])
    while True:
        response=client_socket.recv(2048)
        content+=response
        while len(response)<2048:
            print "content:%s" % content
            response=""
            content=""
        a=raw_input("send to:")
        if len(a):
            client_socket.send(a)
```


客户端代码:


```

    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((target,port))
    a=raw_input("input your text what you want to send:")
       if len(a):
           client.send(a)

       while True:
           buffer=""
           response=""
           a=""
           while "\n" not in response:
               response=client.recv(2048)
               buffer+=response
           print "Received buffer:%s" % buffer
           a=raw_input("send to server:")
           if len(a):
               client.send(a)


     ```


2) udp
   服务段代码:

   ```
   #socket.AF_INET：ipv4,socket.SOCK_STREAM：udp
   sever_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
   server_socket.bind((target,port))
   server_socket.listen(5)
   while True:
        client_socket,addr=server_socket.accept()
        client_handler=threading.Thread(target=handler_socket,args=(client_socket,addr,mode))
        client_handler.start()
   pass

   def handler_socket(client_socket,addr,mode="tcp"):
    '''
    server handler client_socket
    '''
    response=""
    content=""
    print "Accepted udp connection from:%s:%d" % (addr[0],addr[1])
    while True:
        response=client_socket.recvfrom(2048)
        content+=response
        while len(response) <2048:
            print "content:%s" % content
            response=""
            content=""
            a=raw_input("send to:")
            if len(a):
                client_socket.sendto(a,addr)

   ```

客户端代码

```
    client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    a=raw_input("input your text what you want to send:")
    if len(a):
        client.sendto(a,(target,port))
    while True:
        buffer=""
        response=""
        a=""
        while "" in response:
            response,addr=client.recvfrom(4096)
        print "Received buffer:%s" % buffer
        a=raw_input("send to server:")
        if len(a):
            client.send(a)

```


如上为基本的实现tcp/udp实现socket同学的基础用法，我写了一个可选tcp/udp socket通信的的实例代码在[github](https://github.com/fishly),源码地址为:[socket通信](https://github.com/fishly/pythonNet/blob/master/socket/net.py)


[enjoytoday,enjoycoding](http://www.enjoytoday.cn/)
