if __name__ == "__main__":

    #init chat client
    client1 = chat_client(port = 8835, username = "ThaaoBlues", server_ip = "127.0.0.1", get_msg = "")

    #connect to the server
    client1.connect_to_chat()

    #infinite loop to send messages 
    #with a refresh delay to not call all the print functions at the same time
    while True:
        time.sleep(0.5)     
        client1.send_msg(message = input("You : "))
