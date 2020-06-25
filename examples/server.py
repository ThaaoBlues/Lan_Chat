from lan_chat.chat_server import chat_server

if __name__ == "__main__":
    #create an object server, specify the port to use and the maximum number of hosts.
    server1 = chat_server(port = 8835, max_hosts = 10, get_msg = "")

    print("Starting server...")
    #litteraly starting the server like I said above
    server1.start_server()
