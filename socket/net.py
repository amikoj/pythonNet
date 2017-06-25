# /usr/bin/python
# -*- encoding:utf-8 -*-
import getopt,sys,socket


client =False
server =False
target=""
port=""
mode=""



def main():
    global client
    global server
    global target
    global port
    global mode
    
    try:
        opts,params=getopt.getopt(sys.argv[1:],"c:s:t:h:p:m",["client","server","target","port","mode"])
    except getopt.GetoptError as error:
        print str(error)
        sys.exit(0)
        
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
            port=arg
            
    if not len(type):
        print "type is necessnary."
        SystemExit(BaseException("Missing specified connection type."))
            
    if client:
        start_client(mode)
    else:
        start_server(mode)


def start_client(mode="tcp"):
    '''
    start up connection client .
    '''
    if type == "tcp":
        client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((target,port))
        a=raw_input("input your text what you want to send:")
        if len(a):
            client.send(a)
        while True:
            client.recv();
    
    
def start_server(mode='tcp'):
    '''
     start up connection server
    '''


if __name__ == "__main__":
    if not len(sys.argv[1:]):
        print "not exists params."
        sys.exit(0)
    else:
        main()