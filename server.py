# Importing necessary libraries
import socket
from threading import Thread

# Declaring the global variables
IP_ADDRESS = '127.0.0.1'
PORT = 8000
SERVER = None
BUFFER_SIZE = 4096

# Creating an empty clients dictionary
clients = {}

# Setup function to initialize the server
def setup():
    # Printing the heading "IP MESSENGER" at the centre with the help of formatting
    print('\033[95m' + "{:^80}".format("IP MESSENGER") + '\033[0m')

    # Getting the global variables along with its values
    global SERVER
    global IP_ADDRESS
    global PORT

    # Creating a socket for the server
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binding the server to the IP address and the port number
    SERVER.bind((IP_ADDRESS, PORT))

    # Listening for maximum 100 incoming connections
    SERVER.listen(100)

    # Printing the waiting message at the centre with the help of formatting
    print('\033[93m' + "{:^80}".format("Waiting for incoming connections...") + '\033[0m')

    # Calling the accept connections function
    acceptConnections()

# Function to accept connections from the client
def acceptConnections():
    # Getting the global variables along with its values
    global SERVER
    global clients

    # Running an infinite loop to accept incoming connections
    while True:
        client, addr = SERVER.accept()
        client_name = client.recv(4096).decode().lower()
        clients[client_name] = {
            "client": client,
            "address": addr,
            "connected_with": "",
            "file_name": "",
            "file_size": 4096
        }

        print(f"Connection established with {client_name} : {addr}")
        thread = Thread(target=handleClient, args=(client, client_name,))
        thread.start()

# Create and start a thread on the server side
setup_thread = Thread(target=setup)
setup_thread.start()