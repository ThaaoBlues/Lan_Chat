import socket
import os
import time
import sys
from multiprocessing import Process
import platform



class chat_client():
    
    #init variables
    def __init__(self,port,username,server_ip):
        self.port = port
        self.username= username
        self.server_ip = server_ip
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    #connecting to the chat and starting a process to recieve incoming messages
    def connect_to_chat(self):
        try:
            self.sock.connect((self.server_ip,self.port))
        except:
            print("Server offline, new try in 10 seconds...")
            time.sleep(10)
            self.connect_to_chat()
        recv_chat_process = Process(target = self.recv_chat)
        recv_chat_process.start()


    #function which receve the messages in real time (in a process called in the function just above)
    def recv_chat(self):
        while True:
            message = self.sock.recv(1024)
            if str(message) != "":
                #Windows and Linux have differents syystem commands, this is making me often loose some hair
                if platform.system() == "Windows":
                    os.system("cls")
                else:
                    os.system("clear")


                print("{}\n".format(message.decode('utf-8')))


    #function which sends the messages to the server
    def send_msg(self,message):
        try:
            if message != "" and message != "\n" and message != None and message.strip() != False:
                self.sock.send(bytes(str(self.username+" : "+message),'utf-8'))
        except:
            print("Error in message sending...")

