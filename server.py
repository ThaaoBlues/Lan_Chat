import socket
import os
import time
import sys
from multiprocessing import Process, Manager

class chat_server():
    
    #initialize variables and files
    def __init__(self,port,max_hosts):
        self.port = port
        self.max_hosts = max_hosts
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.accept_process = ""
        self.broadcast_process = ""
        with open("last_msg.data.Blue","w") as f:
            f.close()


    #starts the server and launch the process to accept connections
    def start_server(self):
        self.hosts = Manager().list()
        self.sock.bind(('127.0.0.1', self.port))
        self.accept_process = Process(target = self.accept_hosts)
        self.accept_process.start()
        print("Server is now online.")
        self.accept_process.join()
        

    #funtion of the process accept_hosts_process to...yeah it's accepting hosts while the server is running
    def accept_hosts(self):
        self.sock.listen(self.max_hosts)
        while True:
            client, address = self.sock.accept()
            self.hosts.append(address[0])
            self.broadcast_process = Process(target = self.broadcast, args = (client,len(self.hosts)))
            self.broadcast_process.start()
            print("[+]user connected :: addr : {} hostname : {}".format(address[0],socket.gethostbyaddr(address[0])[0]))
            print("[!]Users are now {}/{}".format(len(self.hosts),self.max_hosts))


    #recieve and send the messages
    def broadcast(self,client,client_pos):
        while True:
            if len(self.hosts) >= 1:
                with open("last_msg.data.Blue","r") as f:
                    try:
                        client.send(bytes(f.read(),'utf-8'))
                        f.close()
                    except:
                        #exit if the user is dsconnected and remove a
                        self.hosts.pop(client_pos-1)
                        print("[x]Host number {} as left the chat".format(client_pos))
                        exit(1)

                try:
                    message = client.recv(1024)
                    if message != "":
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
       
