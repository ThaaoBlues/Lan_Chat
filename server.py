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
        self.hosts_number = 0
        with open("last_msg.data.Blue","w") as f:
            f.close()


    #starts the server and launch the process to accept connections
    def start_server(self):
        self.hosts_number = Manager().Value('i',0)
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
            self.hosts_number.value += 1
            self.broadcast_process = Process(target = self.broadcast, args = (client,self.hosts_number))
            self.broadcast_process.start()
            print("[+]user connected :: addr : {} hostname : {}".format(address[0],socket.gethostbyaddr(address[0])[0]))
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
     
