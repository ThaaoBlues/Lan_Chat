from lan_chat.chat_client import chat_client
import time

if __name__ == "__main__":

    #init chat client
    client1 = chat_client(port = 8835, username = input("Choose an username : "),server_ip = input("server IP address : "), get_msg = "")

    #connect to the server
    client1.connect_to_chat()

    #infinite loop to send messages 
    #with a refresh delay to not call all the print functions at the same time
    while True:
        time.sleep(0.5)     
        client1.send_msg(message = input("You : "))
