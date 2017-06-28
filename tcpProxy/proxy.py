# /usr/bin/python
# -*- encoding:utf-8 -*-

# Python network related practice case
import sys,socket,threading








def main():
    if len(sys.argv[1:]) !=5:
        print "Usage: ./proxy.py [local_host] [local_port] [remote_host] [remote_post] [receiver_first]"
        print "Example: ./prxoy.py localhost 9000 www.enjoytoday.cn 9000 True"
        sys.exit(0)
        
    local_host=sys.argv[1]
    local_port=int(sys.argv[2])
    remote_host=sys.argv[3]
    remote_port=int(sys.argv[4])
    receiver_first=sys.argv[5]
    
    if "True" in receiver_first:
        receiver_first=True
    else:
        receiver_first=False
        server_loop(local_host,local_port,remote_host,remote_port,receiver_first)






def server_loop(local_host,local_port,remote_host,remote_port,receiver_first):
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    try:
        server.bind((local_host,local_port))
    except BaseException as error:
        print "socket binded %s:%d failed, get exception:%s"%(local_host,local_port,str(error))
        sys.exit(0)
    
    print "[*] Listening on %s:%d " % (local_host,local_port)
    
    server.listen(8)
    
    while True:
        client_socket,addr =server.accept()
        
        #Receiver client request of send message.
        print "[==>] Received incoming connection from %s:%d" %(addr[0],addr[1])
        
        proxy_thread=threading.Thread(proxy_handler,args=(client_socket,remote_host,remote_port,receiver_first))
        proxy_thread.start()
                
        
        
def proxy_handler(client_socket,remote_host,remote_port,receiver_first):
    remote_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remote_socket.connect((remote_host,remote_port))
    # receiver ip data from remote host
    if receiver_first:
        remote_buffer=receiver_from(remote_socket)
        hexdump(remote_buffer)
        
        remote_buffer=response_handler(remote_buffer)
        
        if len(remote_buffer):
            print "[==>] Sending %d bytes to localhost." % len(remote_buffer)
            client_socket.send(remote_buffer)
            
    while True:
        local_buffer=receiver_from(client_socket)
        
        if len(local_buffer):
            print "[==>] Received %d bytes from localhost." % len(local_buffer)
            hexdump(local_buffer)
            
            #send reuqest of local request
            local_buffer=request_handler(local_buffer)
            
            # send to remote host
            remote_socket.send(local_buffer)
            print "[==>] Send to remote."
            
        remote_buffer=receiver_from(remote_socket)
        
        if len(remote_buffer):
            print "[==>] Received %d bytes from remote." % len(remote_buffer)
            hexdump(remote_buffer)
            
            remote_buffer=response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print "[==>] Sent to localhost."
            
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print "[==>] No more data.Closing connections."
            
            break
    
    
    
def receiver_from(remote_socket):
    buffer = ""
    # set receiver delay of remote_socket
    remote_socket.settimeout(2)
    
    try:
        while True:
            data =remote_socket.recv(4096)
            if not data:
                break
            buffer+=data
    except:
        print "[*] remote_socket recv failed."
        pass
    return buffer



def hexdump(src,length=16):
    result=[]
    digits =4 if isinstance(src,unicode) else 2
    
    #xrange creator step is length
    for i in xrange(0,len(src),length):
        s = src[i:i+length]
        hexa= b' '.join(["%0*X" % (digits,ord(x)) for x in s])
        text=b' '.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b"%04X %-*s %s" % (i,length*(digits+1),hexa,text))
        
    print b'\n'.join(result)
    
    
    
def response_handler(remote_buffer):
    #listener
    return remote_buffer


def request_handler(buffer):
    
    #listener
    return buffer


main()