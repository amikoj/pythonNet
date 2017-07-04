# /usr/bin/python
# -*- encoding:utf-8 -*-
import getopt,sys,socket,threading


client =False
server =False
target="127.0.0.1"
port=9000
mode="tcp"



def main():
    global client
    global server
    global target
    global port
    global mode
    
    try:
        opts,params=getopt.getopt(sys.argv[1:],"csh:t:p:m:",["client","server","help","target","port","mode"])
    except getopt.GetoptError as error:
        print str(error)
        sys.exit(0)
    print opts
    for opt,arg in opts:
        if opt in ("-c","--client"):
            client=True
        if opt in ("-s","--server"):
            server=True
        if opt in ("-m","--mode"):
            mode=arg
        if opt in ("-t","--target"):
            target=arg
        if opt in ("-p","--port"):
            port=int(arg)
            
    if not len(mode):
        print "type is necessnary."
        SystemExit(BaseException("Missing specified connection mode."))
            
    if client:
        start_client(mode.strip())
    else:
        start_server(mode.strip())


def start_client(mode="tcp"):
    global target
    global port
    buffer=""
    response=""
    '''
    start up connection client .
    '''
    if mode == "tcp":
        print "Tcp socket client.target is %s,and port is %d" %(target,port)
        client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((target,port))
        a=raw_input("input your text what you want to send:")
        if len(a):
            client.send(a)
       
        while True:
            response=client.recv(2048)
            buffer+=response
            a=""
            while  len(response)<2048:
                print "Received buffer:%s" % buffer
                a=raw_input("send to server:")
                if len(a):
                    if a== "close":
                        client.close()
                    else:                    
                        client.send(a)                  
                response=""
                buffer=""
                break 
    elif mode == "udp":
        print "Udp socket client.target is %s,and port is %d" % (target,port)
        client=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        a=raw_input("input your text what you want to send:")
        if len(a):
            client.sendto(a,(target,port))
        while True:
            response,addr=client.recvfrom(4096)
            buffer+=response
            a=""
            while len(response) <4096:
                print "Received buffer:%s" % buffer
                a=raw_input("send to server:")
                if len(a):
                    if a=="close":
                        client.close()
                    else:
                        client.sendto(a,addr)                    
                response=""
                buffer=""
                break
                    
                
    
    
def start_server(mode='tcp'):
    global target
    global port
    '''
     start up connection server
    '''
    print "mode:",mode
    if mode == "tcp":
        print "Tcp socket server."
        server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server_socket.bind((target,port))
        server_socket.listen(5)
        while True:
            client_socket,addr=server_socket.accept()
            client_handler=threading.Thread(target=handler_socket,args=(client_socket,addr,mode))
            client_handler.start()           
        
    elif mode == "udp":
        print "Udp socket server"
        server_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
        server_socket.bind((target,port)) 
        client_handler=threading.Thread(target=handler_socket,args=(server_socket,None,mode))
        client_handler.start()    


def handler_socket(client_socket,addr,mode="tcp"):
    '''
    server handler client_socket
    '''
    response=""
    content=""
    if mode=="tcp":
        print "Accepted tcp connection from:%s:%d" % (addr[0],addr[1])
        while True:
            response=client_socket.recv(2048)
            content+=response
            while len(response)<2048:
                print "content:%s" % content
                a=raw_input("send to:")
                if len(a):
                    if a== "close":
                        client_socket.close()
                    else:                    
                        client_socket.send(a)                
                response=""
                content=""
                break
           
            
        
    elif mode == "udp":
        print "Accepted udp connection from"
        while True:
            response,addr0=client_socket.recvfrom(2048)
            content+=response
            while len(response) <2048:
                print "content:%s" % content
                a=raw_input("send to:")
                if len(a):
                    if a== "close":
                        client_socket.close()
                    else:
                        client_socket.sendto(a,addr0)                  
                response=""
                content=""
                break
           
        

if __name__ == "__main__":
    if not len(sys.argv[1:]):
        print "not exists params."
        sys.exit(0)
    else:
        main()