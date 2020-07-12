import socket
import os
import time
import sys
from multiprocessing import Process, Manager
from requests import get

class chat_server():
    
    #initialize variables and files
    def __init__(self,port,max_hosts, get_msg):
        
        #recv_function is a parameter for a custom message displaying function, put "" if you want to let the default function.
        self.recv_function = get_msg
        
        
        self.port = port
        self.max_hosts = max_hosts
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.accept_process = ""
        self.broadcast_process = ""
        self.hosts_number = 0
        with open("last_msg.data.Blue","w") as f:
            f.close()


    #starts the server and launch the process to accept connections
    def start_server(self):
        self.hosts_number = Manager().Value('i',0)
        self.sock.bind(('', self.port))
        self.accept_process = Process(target = self.accept_hosts)
        self.accept_process.start()
        print("[+]Server is now online.")
        print("[+]Listening on : (Private IP) {} || (Public IP) {}".format(socket.gethostbyname_ex(socket.gethostname())[2],get('https://api.ipify.org').text))
        self.accept_process.join()
        

    #funtion of the process accept_hosts_process to...yeah it's accepting hosts while the server is running
    def accept_hosts(self):
        self.sock.listen(self.max_hosts)
        while True:
            client, address = self.sock.accept()
            self.hosts_number.value += 1
            self.broadcast_process = Process(target = self.broadcast, args = (client,self.hosts_number))
            self.broadcast_process.start()
            print("[+]user connected :: addr : {}".format(address[0]))
            print("[!]Users are now {}/{}".format(self.hosts_number.value,self.max_hosts))
   

    #recieve and send the messages
    def broadcast(self,client,client_pos):
        while True:
            if self.hosts_number.value >= 1:
                with open("last_msg.data.Blue","r") as f:
                    try:
                        client.send(bytes(f.read(),'utf-8'))
                        f.close()
                    except:
                        #exit if the user is dsconnected and remove it from the count
                        print("[x]Host number {} as left the chat".format(client_pos.value))
                        self.hosts_number.value -= 1
                        print("[!]Users are now {}/{}".format(self.hosts_number.value,self.max_hosts))
                        exit(1)
             

                try:
                    message = client.recv(1024)
                    
                    #handle custom message displaying function
                    if self.recv_function and self.recv_function != "" and self.recv_function != None:
                        with open("last_msg.data.Blue","a") as f:
                            if "[REFRESH FLAG]" in message.decode('utf-8'):
                                print(message.decode('utf-8'))
                            else:
                                f.write("{}\n".format(message.decode('utf-8')))
                                f.close()

                        result = getattr(sys.modules[__name__],self.recv_function)(message=message)
                    else:
                        if message != "":
                            if "[REFRESH FLAG]" in message.decode('utf-8'):
                                print(message.decode('utf-8'))
                            else :
                                print(message.decode('utf-8'))
                                with open("last_msg.data.Blue","a") as f:
                                    f.write("{}\n".format(message.decode('utf-8')))
                                    f.close()
                    
                except:
                    pass

    #function to shutdown the server but this is useless you will always click on the red cross
    def shutdown_server(self):
        self.broadcast_process.terminate()
        self.accept_process.terminate()
        os.remove("last_msg.data.Blue")
